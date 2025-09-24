from Matching.pipeline import match_jobs_candidates
import os, json

# ----------------------------
# Execução principal (se rodar diretamente)
# ----------------------------
if __name__ == "__main__":
    # tenta carregar jobs.json e candidates.json
    if os.path.exists("JSONs/jobs.json") and os.path.exists("JSONs/candidates.json"):
        with open("JSONs/jobs.json","r",encoding="utf-8") as f:
            jobs = json.load(f)
        with open("JSONs/candidates.json","r",encoding="utf-8") as f:
            candidates = json.load(f)
    else:
        print("Arquivos JSON não encontrados.")

    res = match_jobs_candidates(jobs, candidates)
    df = res["matrix_df"]
    # Mostra os 3 melhores matches para cada vaga
    for job_id, row in df.iterrows():
        top5 = row.nlargest(5)
        print(f"Vaga {job_id} - Top 5 candidatos:")
        for cand_id, score in top5.items():
            print(f"  Candidato {cand_id}: Score {score:.4f}")
        print()