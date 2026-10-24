"""Test Harness do TaskAnalyzer: traduz os cenários de aceite da especificação."""

from datetime import datetime, timedelta
from typing import Any

import pytest

from src.task_analyzer import TaskValidationError, analyze_tasks

BASE = datetime(2026, 1, 1, 8, 0, 0)


def make_task(
    id_tarefa: int,
    prioridade: str,
    status: str,
    horas_ate_conclusao: float | None,
    horas_ate_prazo: float = 10.0,
) -> dict[str, Any]:
    """Cria uma tarefa válida para uso nos testes.

    Args:
        id_tarefa: Identificador da tarefa.
        prioridade: "baixa", "media" ou "alta".
        status: "concluida" ou "pendente".
        horas_ate_conclusao: Horas entre criação e conclusão, ou None.
        horas_ate_prazo: Horas entre criação e prazo.

    Returns:
        Dicionário de tarefa conforme a especificação.
    """
    conclusao = (
        BASE + timedelta(hours=horas_ate_conclusao)
        if horas_ate_conclusao is not None
        else None
    )
    return {
        "id": id_tarefa,
        "titulo": f"Tarefa {id_tarefa}",
        "prioridade": prioridade,
        "status": status,
        "data_criacao": BASE,
        "data_prazo": BASE + timedelta(hours=horas_ate_prazo),
        "data_conclusao": conclusao,
    }


@pytest.fixture
def tarefas_validas() -> list[dict[str, Any]]:
    """Conjunto de tarefas válidas com resultado conhecido."""
    return [
        make_task(1, "alta", "concluida", 4.0, 10.0),    # no prazo
        make_task(2, "alta", "concluida", 12.0, 10.0),   # atrasada
        make_task(3, "media", "concluida", 6.0, 10.0),   # no prazo
        make_task(4, "baixa", "concluida", 20.0, 10.0),  # atrasada
        make_task(5, "media", "pendente", None),
    ]


def test_cenario1_sucesso_totais(tarefas_validas: list[dict[str, Any]]) -> None:
    """Cenário 1: totais corretos."""
    resultado = analyze_tasks(tarefas_validas)
    assert resultado["total_tarefas"] == 5
    assert resultado["total_concluidas"] == 4
    assert resultado["total_pendentes"] == 1


def test_cenario1_sucesso_tempo_medio(tarefas_validas: list[dict[str, Any]]) -> None:
    """Cenário 1: tempo médio geral e por prioridade."""
    medias = analyze_tasks(tarefas_validas)["tempo_medio_conclusao_horas"]
    assert medias["geral"] == 10.5
    assert medias["alta"] == 8.0
    assert medias["media"] == 6.0
    assert medias["baixa"] == 20.0


def test_cenario1_sucesso_taxa_atraso(tarefas_validas: list[dict[str, Any]]) -> None:
    """Cenário 1: taxa de atraso (2 de 4 concluídas = 50%)."""
    assert analyze_tasks(tarefas_validas)["taxa_atraso_percentual"] == 50.0


def test_cenario2_data_conclusao_anterior_a_criacao() -> None:
    """Cenário 2: data_conclusao < data_criacao lança TaskValidationError."""
    tarefa = make_task(1, "alta", "concluida", -2.0)
    with pytest.raises(TaskValidationError, match="anterior"):
        analyze_tasks([tarefa])


def test_cenario2_concluida_sem_data_conclusao() -> None:
    """Cenário 2: tarefa concluída sem data_conclusao lança erro."""
    tarefa = make_task(1, "alta", "concluida", None)
    with pytest.raises(TaskValidationError):
        analyze_tasks([tarefa])


def test_cenario2_prioridade_invalida() -> None:
    """Cenário 2: prioridade fora dos valores permitidos lança erro."""
    tarefa = make_task(1, "urgente", "pendente", None)
    with pytest.raises(TaskValidationError, match="prioridade"):
        analyze_tasks([tarefa])


def test_cenario2_campo_ausente() -> None:
    """Cenário 2: campo obrigatório ausente lança erro."""
    tarefa = make_task(1, "alta", "pendente", None)
    del tarefa["data_prazo"]
    with pytest.raises(TaskValidationError, match="data_prazo"):
        analyze_tasks([tarefa])


def test_borda_lista_vazia() -> None:
    """Cenário 3: lista vazia retorna zeros, sem exceção."""
    resultado = analyze_tasks([])
    assert resultado["total_tarefas"] == 0
    assert resultado["tempo_medio_conclusao_horas"]["geral"] == 0.0
    assert resultado["taxa_atraso_percentual"] == 0.0


def test_borda_apenas_pendentes() -> None:
    """Cenário 3: apenas pendentes retorna 0.0 nas médias e na taxa."""
    tarefas = [make_task(1, "alta", "pendente", None), make_task(2, "baixa", "pendente", None)]
    resultado = analyze_tasks(tarefas)
    assert resultado["total_pendentes"] == 2
    assert resultado["total_concluidas"] == 0
    medias = resultado["tempo_medio_conclusao_horas"]
    assert all(valor == 0.0 for valor in medias.values())
    assert resultado["taxa_atraso_percentual"] == 0.0
