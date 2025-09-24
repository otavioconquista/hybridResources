import json
import os

# Lê o JSON de vagas e filtra apenas as vagas cujo valor de "nivel profissional" for igual a "Júnior" ou "Analista"
def load_and_filter_jobs():
    # Path to the JSON file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, 'JSONs', 'vagas.json')

    # Read the JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            jobs = json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {json_path}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
        return None

    # Campos desejados
    info_fields = ["titulo_vaga"]
    perfil_fields = [
        "pais", "estado", "cidade", "nivel profissional",
        "nivel_ingles", "nivel_espanhol",
        "principais_atividades", "competencia_tecnicas_e_comportamentais"
    ]

    # Filter and select only required fields
    filtered_jobs = {}
    for job_id, job in jobs.items():
        perfil = job.get("perfil_vaga", {})
        if perfil.get("nivel profissional") in ["Júnior", "Analista"]:
            filtered_job = {
                "informacoes_basicas": {
                    k: v for k, v in job.get("informacoes_basicas", {}).items() if k in info_fields
                },
                "perfil_vaga": {
                    k: v for k, v in perfil.items() if k in perfil_fields
                }
            }
            filtered_jobs[job_id] = filtered_job

    return filtered_jobs

# Transforma o JSON em um mais simplificado com dois campos: id e descriçao. A descrição deverá ser formada por uma concatenção dos campos:
# "titulo_vaga", "pais", "estado", "cidade", "nivel profissional", "nivel_ingles", "nivel_espanhol", "principais_atividades", "competencia_tecnicas_e_comportamentais"

def transform_jobs(filtered_jobs):
    result = []
    for job_id, job in filtered_jobs.items():
        descricao = " | ".join([
            job.get("informacoes_basicas", {}).get("titulo_vaga", ""),
            "País: " + job.get("perfil_vaga", {}).get("pais", ""),
            "UF: " + job.get("perfil_vaga", {}).get("estado", ""),
            "Cidade: " + job.get("perfil_vaga", {}).get("cidade", ""),
            #job.get("perfil_vaga", {}).get("nivel profissional", ""),
            "Inglês: " + job.get("perfil_vaga", {}).get("nivel_ingles", ""),
            "Espanhol: " + job.get("perfil_vaga", {}).get("nivel_espanhol", ""),
            job.get("perfil_vaga", {}).get("principais_atividades", ""),
            job.get("perfil_vaga", {}).get("competencia_tecnicas_e_comportamentais", "")
        ])
        result.append({
            "id": job_id,
            "descricao": descricao
        })
    return result

filtered_jobs = load_and_filter_jobs()
if filtered_jobs is not None:
    jobs_list = transform_jobs(filtered_jobs)
    # Salva no formato de lista, não dicionário
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'JSONs', 'jobs.json')
    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(jobs_list, outfile, ensure_ascii=False, indent=4)
        print(f"Arquivo salvo em {output_path}")
else:
    print("No jobs to process.")