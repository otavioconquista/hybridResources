from typing import Set

from config import (
    W_SKILL, W_EMBED, W_DOMAIN,
)

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# ----------------------------
# Scoring helpers
# ----------------------------
def coverage_score(job_skills: Set[str], cand_skills: Set[str]) -> float:
    # quanto dos requisitos da vaga o candidato cobre: len(inter)/len(job_skills)
    if not job_skills:
        return 0.0
    inter = job_skills.intersection(cand_skills)
    return len(inter) / len(job_skills)

def domain_similarity(candidate_emb: np.ndarray, centroid_emb: np.ndarray) -> float:
    if centroid_emb is None or candidate_emb is None:
        return 0.0
    sim = cosine_similarity(candidate_emb.reshape(1,-1), centroid_emb.reshape(1,-1))[0,0]
    return float(np.clip(sim, 0.0, 1.0))

def combine_scores(embed_sim: float, cov_score: float, dom_sim: float,
                   w_skill=W_SKILL, w_embed=W_EMBED, w_domain=W_DOMAIN) -> float:
    total = w_skill + w_embed + w_domain
    w_skill /= total; w_embed /= total; w_domain /= total
    combined = w_skill * cov_score + w_embed * embed_sim + w_domain * dom_sim
    return float(np.clip(combined, 0.0, 1.0))