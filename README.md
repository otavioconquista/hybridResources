# API de Matching de Vagas e Candidatos

Este projeto implementa uma API para realizar o matching entre vagas de emprego e candidatos, utilizando análise de texto e cobertura de competências. A API foi desenvolvida com [FastAPI](https://fastapi.tiangolo.com/) e pode ser utilizada para identificar os candidatos mais aderentes a uma vaga ou para processar múltiplas vagas de uma só vez.

## Sumário

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

## Funcionalidades

- Recebe uma descrição de vaga e retorna os 3 candidatos mais aderentes.
- Recebe um arquivo JSON com múltiplas vagas e retorna os 3 melhores candidatos para cada vaga.
- Matching baseado em extração de competências e cálculo de cobertura de requisitos.

## Instalação

1. Clone o repositório:
   ```sh
   git clone <url-do-repositorio>
   cd <nome-da-pasta>