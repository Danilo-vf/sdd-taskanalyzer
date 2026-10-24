# sdd-taskanalyzer

Módulo TaskAnalyzer desenvolvido com Spec-Driven Development (SDD) e assistência de IA, para a disciplina Bootcamp III.

## O que faz
Analisa uma lista de tarefas e calcula: total de tarefas, concluídas e pendentes, tempo médio de conclusão em horas (geral e por prioridade) e taxa de atraso percentual.

## Estrutura do repositório
- CONTEXT_RULES.md: regras de governança para agentes de IA
- specs/task_analyzer_spec.md: especificação SDD (contrato e cenários de aceite)
- src/task_analyzer.py: código gerado via IA e homologado por humano
- tests/test_harness.py: testes automatizados com pytest
- requirements.txt: dependências autorizadas

## Como executar
Requer Python 3.11 ou superior.

    pip install -r requirements.txt
    python -m pytest -v

## Status do build
Testes: 9 passed (pytest), cobrindo os Cenários 1 e 2 e casos de borda.

## Fluxo de trabalho
Branch principal `main` e branches de funcionalidade (`feature/*`) integradas por Pull Request, com revisão humana contra o CONTEXT_RULES.md.
