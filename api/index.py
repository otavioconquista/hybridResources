from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import sys

# Add the parent directory to the Python path to import from Matching module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Matching.pipeline import match_jobs_candidates

# Create Flask app instance for Vercel
app = Flask(__name__)

# Configure CORS for cross-origin requests
CORS(app, origins=['*'])

# Load candidates data (assuming it's static for now)
def load_candidates():
    """Load candidates from JSONs/candidates.json"""
    candidates_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "JSONs", "candidates.json")
    try:
        with open(candidates_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

@app.route("/match_vaga", methods=["POST"])
def match_single_job():
    """
    Endpoint to match a single job description against all candidates
    Expects FormData with 'descricao' field
    """
    try:
        # Get job description from form data
        descricao = request.form.get('descricao')
        if not descricao:
            return jsonify({"erro": "Campo 'descricao' é obrigatório"}), 400
        
        # Load candidates
        candidates = load_candidates()
        if not candidates:
            return jsonify({"erro": "Nenhum candidato encontrado"}), 500
        
        # Create job object
        job = {"id": "single_job", "descricao": descricao}
        jobs = [job]
        
        # Run matching pipeline
        result = match_jobs_candidates(jobs, candidates)
        
        # Extract top matches for the single job
        top_matches = result["top_matches"][0] if result["top_matches"] else {"top": []}
        
        # Format response
        response = {
            "job": job,
            "candidates_count": len(candidates),
            "top_matches": top_matches["top"]
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"erro": "Erro interno do servidor", "detalhes": str(e)}), 500

@app.route("/match_vagas", methods=["POST"])
def match_multiple_jobs():
    """
    Endpoint to match multiple jobs from uploaded JSON file against all candidates
    Expects FormData with 'file' field containing JSON file
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({"erro": "Nenhum arquivo enviado"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"erro": "Nenhum arquivo selecionado"}), 400
        
        # Read and parse JSON file
        try:
            file_content = file.read().decode('utf-8')
            jobs = json.loads(file_content)
        except json.JSONDecodeError:
            return jsonify({"erro": "Arquivo JSON inválido"}), 400
        except UnicodeDecodeError:
            return jsonify({"erro": "Erro de codificação do arquivo"}), 400
        
        if not isinstance(jobs, list):
            return jsonify({"erro": "O arquivo deve conter uma lista de vagas"}), 400
        
        if not jobs:
            return jsonify({"erro": "Nenhuma vaga encontrada no arquivo"}), 400
        
        # Load candidates
        candidates = load_candidates()
        if not candidates:
            return jsonify({"erro": "Nenhum candidato encontrado"}), 500
        
        # Run matching pipeline
        result = match_jobs_candidates(jobs, candidates)
        
        # Format response
        response = {
            "jobs_count": len(jobs),
            "candidates_count": len(candidates),
            "top_matches": result["top_matches"],
            "matrix_summary": {
                "shape": result["matrix_df"].shape,
                "columns": result["matrix_df"].columns.tolist(),
                "index": result["matrix_df"].index.tolist()
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"erro": "Erro interno do servidor", "detalhes": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "API is running"})

# Export the Flask app for Vercel
if __name__ == "__main__":
    app.run(debug=True)