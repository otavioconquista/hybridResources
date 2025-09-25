# API de Matching de Vagas e Candidatos

Este projeto implementa uma solução web para realizar o matching entre vagas de emprego do nível júnior e candidatos possíveis, utilizando análise de texto e cobertura de competências. A API foi desenvolvida com [FastAPI](https://fastapi.tiangolo.com/) e pode ser utilizada para identificar os candidatos mais aderentes a uma vaga específica ou para processar múltiplas vagas de uma só vez através do input de um JSON.

A versão aqui apresentada é a free e com uma quantidade limitada de candidatos com formação em 2025. A versão premium é mais precisa e mais próxima das capacidades humanas, com pesquisa semântica/contextual, e com atualização semestral de candidatos. Versão premium disponível sob encomenda.

## Estrutura do repositório

- JSONs/
- Matching/
- Utils/
- api.py
- dataExploration.ipynb
- requirements.txt
- vercel.json

## Sumário

- [Hipótese](#hipótese)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Como usar](#como-usar)
  - [Endpoint `/match_vaga`](#endpoint-match_vaga)
  - [Endpoint `/match_vagas`](#endpoint-match_vagas)
- [Formato dos Dados](#formato-dos-dados)
- [Lógica de Matching](#lógica-de-matching)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Exemplo de Uso](#exemplo-de-uso)
- [Licença](#licença)

---

## Hipótese

Como analisado no arquivo dataExploration.py, a maior parte das vagas (40%) são do nível júnior. Ao automatizarmos o matching dos candidatos com as respectivas vagas, propomos dedicar a atenção dos funcionários de empresas de head hunting às vagas com mais nuances e especificidades, como é o caso de vagas de nível pleno, sênior ou de liderança.

Na Hybrid Resources propomos um paradigma de trabalho baseado em inteligência híbrida:

*Aos humanos, o complexo e subjetivo. Às máquinas, o simples e massivo.*

## Funcionalidades

- Recebe uma descrição de vaga e retorna os 3 candidatos mais aderentes.
- Recebe um arquivo JSON com múltiplas vagas e retorna os 3 melhores candidatos para cada vaga.
- Matching baseado em extração de competências e cálculo de cobertura de requisitos.

## Instalação

1. Clone o repositório:
   ```sh
   git clone <url-do-repositorio>
   cd <nome-da-pasta>