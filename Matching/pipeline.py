import spacy
import pandas as pd
from typing import List, Dict, Any

from Matching.scoring import coverage_score

TOP_N = 3

# ----------------------------
# Core: carregar modelo e calcular embeddings
# ----------------------------
nlp = spacy.load("pt_core_news_sm")

def extract_skills_spacy(text: str) -> set:
    doc = nlp(text or "")
    return set([token.lemma_.lower() for token in doc if token.pos_ == "NOUN" and not token.is_stop])

# ----------------------------
# Pipeline principal
# ----------------------------

def match_jobs_candidates(jobs: List[Dict[str,Any]], candidates: List[Dict[str,Any]]) -> Dict[str,Any]:
    job_texts = [j.get("descricao","") or j.get("title","") or "" for j in jobs]
    cand_texts = [c.get("perfil","") or c.get("summary","") or "" for c in candidates]

    job_skills_list = [extract_skills_spacy(t) for t in job_texts]
    cand_skills_list = [extract_skills_spacy(t) for t in cand_texts]

    m = len(jobs)
    n = len(candidates)
    combined_matrix = []
    for i in range(m):
        row = []
        for j in range(n):
            score = coverage_score(job_skills_list[i], cand_skills_list[j])
            row.append(score)
        combined_matrix.append(row)

    df = pd.DataFrame(combined_matrix,
                      index=[f"Vaga {j.get('id', idx)}" for idx,j in enumerate(jobs)],
                      columns=[f"Candidato {c.get('id', idx)}" for idx,c in enumerate(candidates)])

    top_matches = []
    for i, job in enumerate(jobs):
        row = df.iloc[i]
        ranked_idx = row.argsort()[::-1]
        top = []
        for k in ranked_idx[:TOP_N]:
            top.append({
                "cand_index": int(k),
                "cand_id": candidates[k].get("id"),
                "match_score": float(row.iloc[k]),
                "cand_skills": sorted(list(cand_skills_list[k])),
                "job_skills": sorted(list(job_skills_list[i]))
            })
        top_matches.append({
            "job_index": i,
            "job_id": job.get("id"),
            "top": top
        })

    return {
        "matrix_df": df,
        "top_matches": top_matches
    }