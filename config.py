# ----------------------------
# Configurações (ajuste conforme necessário)
# ----------------------------
MODEL_NAME = "multi-qa-MiniLM-L6-cos-v1"   # modelo rápido e eficaz
OUTPUT_DIR = "outputs"
TOP_N = 3

# Pesos para combinação (skill coverage tem maior importância)
W_SKILL = 0.60
W_EMBED = 0.35
W_DOMAIN = 0.05

# Pré-filtros
DOMAIN_THRESHOLD = 0.50      # similaridade ao centroid de vagas mínima para considerar domínio
MIN_JOB_SKILLS_TO_REQUIRE = 1  # se a vaga tem pelo menos 1 skill, exigimos coverage > 0 para candidato ser considerado

# Lista inicial de keywords tech (expanda conforme necessário)
TECH_KEYWORDS = {
    "python","py","java","javascript","js","node","nodejs","node.js","react","angular","vue",
    "typescript","ts","ruby","go","golang","c++","c#","csharp","dotnet","php",
    "sql","postgres","postgresql","mysql","mongodb","nosql",
    "aws","azure","gcp","google cloud","kubernetes","k8s","docker","spark","hadoop",
    "etl","airflow","kafka","redis","graphql","rest","api","terraform",
    "pytorch","tensorflow","scikit-learn","sklearn","ml","machine learning","data",
    "data engineer","data engineering","devops","sre","site reliability","qa","testing",
    "spring","springboot","spring boot","spring-boot","springboot",
    "react native","next.js","nextjs","nestjs","express","django","flask",
    "spark","pandas","numpy","scala","hive"
}