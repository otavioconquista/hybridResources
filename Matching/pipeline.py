from typing import List, Dict, Any
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from config import (
    MODEL_NAME, TOP_N,
    DOMAIN_THRESHOLD, MIN_JOB_SKILLS_TO_REQUIRE
)

from Matching.textTreatments import (
    normalize_text,
    extract_skills_from_text
)

from Matching.scoring import (
    coverage_score,
    domain_similarity,
    combine_scores
)

from Matching.preparingJobs import load_and_filter_jobs, transform_jobs

# ----------------------------
# Core: carregar modelo e calcular embeddings
# ----------------------------
print("Carregando modelo de embeddings:", MODEL_NAME)
model = SentenceTransformer(MODEL_NAME)

def encode_texts(texts: List[str]) -> np.ndarray:
    texts_norm = [normalize_text(t) for t in texts]
    emb = model.encode(texts_norm, convert_to_numpy=True, show_progress_bar=False)
    return emb

# ----------------------------
# Pipeline principal
# ----------------------------

def match_jobs_candidates(jobs: List[Dict[str,Any]], candidates: List[Dict[str,Any]]) -> Dict[str,Any]:
    
    #load_and_filter_jobs()  # Garante que jobs.json está atualizado
    #transform_jobs(load_and_filter_jobs())

    # extrair textos
    job_texts = [j.get("descricao","") or j.get("title","") or "" for j in jobs]
    cand_texts = [c.get("perfil","") or c.get("summary","") or "" for c in candidates]

    # extrair skills por vaga e candidato (sets)
    job_skills_list = [extract_skills_from_text(t) for t in job_texts]
    cand_skills_list = [extract_skills_from_text(t) for t in cand_texts]

    # embeddings
    job_emb = encode_texts(job_texts)            # (m, d)
    cand_emb = encode_texts(cand_texts)          # (n, d)

    # centroid das vagas (domínio tech do batch)
    if len(job_emb) > 0:
        job_centroid = np.mean(job_emb, axis=0)
    else:
        job_centroid = None

    # matriz de similaridade (embeddings) jobs x cands
    emb_sim_matrix = cosine_similarity(job_emb, cand_emb)
    # garantir 0..1
    emb_sim_matrix = np.clip(emb_sim_matrix, 0.0, 1.0)

    m = len(jobs); n = len(candidates)
    combined_matrix = np.zeros((m,n))

    for i in range(m):
        for j in range(n):
            cov = coverage_score(job_skills_list[i], cand_skills_list[j])
            emb_sim = float(emb_sim_matrix[i,j])
            dom_sim = domain_similarity(cand_emb[j], job_centroid) if job_centroid is not None else 0.0

            # PRE-FILTRO:
            # - Se a vaga define skills (>= MIN_JOB_SKILLS_TO_REQUIRE) e o candidato não cobre nenhum => marcar 0
            # - Se o candidato não tem skills técnicas e também é semanticamente distante do centroid => 0
            cand_has_skills = len(cand_skills_list[j]) > 0
            job_requires_skills = len(job_skills_list[i]) >= MIN_JOB_SKILLS_TO_REQUIRE

            if job_requires_skills and cov == 0.0 and not cand_has_skills:
                score = 0.0
            elif not cand_has_skills and dom_sim < DOMAIN_THRESHOLD and cov == 0.0:
                # candidato sem skills técnicas e sem similaridade de domínio
                score = 0.0
            else:
                score = combine_scores(emb_sim, cov, dom_sim)

            combined_matrix[i,j] = score

    # escalar para 0..100
    combined_pct = (combined_matrix * 100).round(2)

    # montar DataFrame e top matches
    df = pd.DataFrame(combined_pct,
                      index=[f"Vaga {j.get('id', idx)}" for idx,j in enumerate(jobs)],
                      columns=[f"Candidato {c.get('id', idx)}" for idx,c in enumerate(candidates)])

    top_matches = []
    for i, job in enumerate(jobs):
        row = combined_pct[i]
        ranked_idx = np.argsort(row)[::-1]  # decrescente
        top = []
        for k in ranked_idx[:TOP_N]:
            top.append({
                "cand_index": int(k),
                "cand_id": candidates[k].get("id"),
                "match_pct": float(row[k]),
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