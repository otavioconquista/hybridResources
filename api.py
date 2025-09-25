from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil, os, json

from Matching.preparingJobs import load_and_filter_jobs, transform_jobs
from Matching.pipeline import match_jobs_candidates

app = FastAPI()

@app.post("/match")
async def match_vagas(file: UploadFile = File(...)):
    # 1. Recebe o JSON e salva como vagas.json
    base_dir = os.path.dirname(os.path.abspath(__file__))
    vagas_path = os.path.join(base_dir, "JSONs", "vagas.json")
    with open(vagas_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Faz as transformações corretas no JSON
    filtered_jobs = load_and_filter_jobs()
    if not filtered_jobs:
        return JSONResponse({"erro": "Erro ao carregar ou filtrar vagas."}, status_code=400)
    jobs_list = transform_jobs(filtered_jobs)

    # 3. Carrega candidatos
    candidates_path = os.path.join(base_dir, "JSONs", "candidates.json")
    if not os.path.exists(candidates_path):
        return JSONResponse({"erro": "Arquivo de candidatos não encontrado."}, status_code=400)
    with open(candidates_path, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    # 4. Aplica o matching
    res = match_jobs_candidates(jobs_list, candidates)
    df = res["matrix_df"]

    # 5. Monta resposta: top 3 candidatos para cada vaga
    top_matches = []
    for match in res["top_matches"]:
        top_matches.append({
            "vaga": match["job_id"],
            "top_candidatos": [
                {"candidato": c["cand_id"], "score": c["match_score"]}
                for c in match["top"]
            ]
        })

    # 6. Apaga o arquivo temporário de vagas
    if os.path.exists(vagas_path):
        os.remove(vagas_path)
        
    return {"top_matches": top_matches}

@app.get("/")
def root():
    return {"API de matching ativa. Insira '/docs' ao final da URL para acessar a funcionalidade."}

app_handler = app  # Para garantir compatibilidade com Vercel