from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
import shutil, os, json
from Matching.preparingJobs import load_and_filter_jobs, transform_jobs
from Matching.pipeline import match_jobs_candidates
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

# Configuração dos caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return FileResponse("public/index.html")

@app.post("/match_vaga")
async def match_vaga_text(descricao: str = Form(...)):
    try:
        # 1. Monta objeto de vaga temporário
        vaga = {"id": "vaga_unica", "descricao": descricao}

        # 2. Carrega candidatos
        candidates_path = os.path.join(PROJECT_ROOT, "JSONs", "candidates.json")
        if not os.path.exists(candidates_path):
            return JSONResponse(
                {"erro": "Arquivo de candidatos não encontrado."}, 
                status_code=400
            )
        
        with open(candidates_path, "r", encoding="utf-8") as f:
            candidates = json.load(f)

        # 3. Aplica o matching
        res = match_jobs_candidates([vaga], candidates)

        # 4. Monta resposta
        match = res["top_matches"][0]
        top_candidatos = [
            {"candidato": c["cand_id"], "score": c["match_score"]}
            for c in match["top"]
        ]
        return {"vaga": descricao, "top_candidatos": top_candidatos}
        
    except Exception as e:
        return JSONResponse(
            {"erro": "Erro ao processar a requisição", "detalhes": str(e)},
            status_code=500
        )

@app.post("/match_vagas")
async def match_vagas(file: UploadFile = File(...)):
    try:
        # 1. Salva arquivo temporário
        temp_dir = "/tmp" if os.path.exists("/tmp") else "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        vagas_path = os.path.join(temp_dir, "vagas.json")
        with open(vagas_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Processa vagas
        filtered_jobs = load_and_filter_jobs()
        if not filtered_jobs:
            return JSONResponse(
                {"erro": "Erro ao carregar ou filtrar vagas."}, 
                status_code=400
            )
            
        jobs_list = transform_jobs(filtered_jobs)

        # 3. Carrega candidatos
        candidates_path = os.path.join(PROJECT_ROOT, "JSONs", "candidates.json")
        if not os.path.exists(candidates_path):
            return JSONResponse(
                {"erro": "Arquivo de candidatos não encontrado."}, 
                status_code=400
            )
            
        with open(candidates_path, "r", encoding="utf-8") as f:
            candidates = json.load(f)

        # 4. Aplica matching e monta resposta
        res = match_jobs_candidates(jobs_list, candidates)
        top_matches = [
            {
                "vaga": match["job_id"],
                "top_candidatos": [
                    {"candidato": c["cand_id"], "score": c["match_score"]}
                    for c in match["top"]
                ]
            }
            for match in res["top_matches"]
        ]

        return {"top_matches": top_matches}

    except Exception as e:
        return JSONResponse(
            {"erro": "Erro ao processar a requisição", "detalhes": str(e)},
            status_code=500
        )

# Handler para Vercel
handler = Mangum(app)