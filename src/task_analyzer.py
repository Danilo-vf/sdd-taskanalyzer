"""Módulo TaskAnalyzer: análise de métricas de produtividade de tarefas."""

import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)

PRIORIDADES_VALIDAS: tuple[str, ...] = ("baixa", "media", "alta")
STATUS_VALIDOS: tuple[str, ...] = ("concluida", "pendente")
CAMPOS_OBRIGATORIOS: tuple[str, ...] = (
    "id",
    "titulo",
    "prioridade",
    "status",
    "data_criacao",
    "data_prazo",
)
SEGUNDOS_POR_HORA: float = 3600.0


class TaskValidationError(ValueError):
    """Erro lançado quando uma tarefa não respeita o contrato da especificação."""


def _validar_campos(task: dict[str, Any]) -> None:
    """Verifica a presença de todos os campos obrigatórios.

    Args:
        task: Dicionário que representa a tarefa.

    Raises:
        TaskValidationError: Se algum campo obrigatório estiver ausente.
    """
    for campo in CAMPOS_OBRIGATORIOS:
        if campo not in task:
            raise TaskValidationError(f"Campo obrigatório ausente: '{campo}'.")


def _validar_valores(task: dict[str, Any]) -> None:
    """Verifica tipos e valores permitidos dos campos da tarefa.

    Args:
        task: Dicionário que representa a tarefa.

    Raises:
        TaskValidationError: Se algum valor for inválido.
    """
    id_tarefa = task["id"]
    if not isinstance(id_tarefa, int) or isinstance(id_tarefa, bool) or id_tarefa <= 0:
        raise TaskValidationError(f"id inválido: {id_tarefa!r}. Deve ser inteiro maior que 0.")
    if not isinstance(task["titulo"], str) or not task["titulo"].strip():
        raise TaskValidationError(f"Tarefa {id_tarefa}: titulo não pode ser vazio.")
    if task["prioridade"] not in PRIORIDADES_VALIDAS:
        raise TaskValidationError(
            f"Tarefa {id_tarefa}: prioridade inválida {task['prioridade']!r}."
        )
    if task["status"] not in STATUS_VALIDOS:
        raise TaskValidationError(f"Tarefa {id_tarefa}: status inválido {task['status']!r}.")
    for campo in ("data_criacao", "data_prazo"):
        if not isinstance(task[campo], datetime):
            raise TaskValidationError(f"Tarefa {id_tarefa}: {campo} deve ser datetime.")


def _validar_conclusao(task: dict[str, Any]) -> None:
    """Verifica a consistência da data de conclusão da tarefa.

    Args:
        task: Dicionário que representa a tarefa.

    Raises:
        TaskValidationError: Se a conclusão estiver ausente, inválida ou
            anterior à data de criação.
    """
    id_tarefa = task["id"]
    data_conclusao = task.get("data_conclusao")
    if task["status"] == "concluida" and data_conclusao is None:
        raise TaskValidationError(f"Tarefa {id_tarefa}: concluída sem data_conclusao.")
    if data_conclusao is None:
        return
    if not isinstance(data_conclusao, datetime):
        raise TaskValidationError(f"Tarefa {id_tarefa}: data_conclusao deve ser datetime.")
    if data_conclusao < task["data_criacao"]:
        raise TaskValidationError(
            f"Tarefa {id_tarefa}: data_conclusao anterior a data_criacao."
        )


def validate_task(task: dict[str, Any]) -> None:
    """Valida uma tarefa completa conforme o contrato da especificação.

    Args:
        task: Dicionário que representa a tarefa.

    Raises:
        TaskValidationError: Se a tarefa violar qualquer regra de validação.
    """
    if not isinstance(task, dict):
        raise TaskValidationError("Cada tarefa deve ser um dicionário.")
    _validar_campos(task)
    _validar_valores(task)
    _validar_conclusao(task)


def _horas_de_conclusao(task: dict[str, Any]) -> float:
    """Calcula o tempo, em horas, entre criação e conclusão da tarefa.

    Args:
        task: Tarefa concluída e já validada.

    Returns:
        Tempo de conclusão em horas.
    """
    delta = task["data_conclusao"] - task["data_criacao"]
    return delta.total_seconds() / SEGUNDOS_POR_HORA


def _media(valores: list[float]) -> float:
    """Calcula a média arredondada em 2 casas, prevenindo divisão por zero.

    Args:
        valores: Lista de números.

    Returns:
        Média dos valores, ou 0.0 se a lista estiver vazia.
    """
    if not valores:
        return 0.0
    return round(sum(valores) / len(valores), 2)


def _taxa_atraso(concluidas: list[dict[str, Any]]) -> float:
    """Calcula o percentual de tarefas concluídas após o prazo.

    Args:
        concluidas: Lista de tarefas concluídas.

    Returns:
        Percentual de atraso com 2 casas, ou 0.0 se não houver concluídas.
    """
    if not concluidas:
        return 0.0
    atrasadas = sum(1 for t in concluidas if t["data_conclusao"] > t["data_prazo"])
    return round(atrasadas / len(concluidas) * 100, 2)


def analyze_tasks(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    """Analisa uma lista de tarefas e retorna métricas de produtividade.

    Args:
        tasks: Lista de tarefas, cada uma um dicionário conforme a especificação.

    Returns:
        Dicionário com total_tarefas, total_concluidas, total_pendentes,
        tempo_medio_conclusao_horas (geral e por prioridade) e
        taxa_atraso_percentual.

    Raises:
        TaskValidationError: Se alguma tarefa for inválida.
    """
    logger.info("Iniciando análise de %d tarefas.", len(tasks))
    for task in tasks:
        validate_task(task)

    concluidas = [t for t in tasks if t["status"] == "concluida"]
    horas_por_prioridade: dict[str, list[float]] = {p: [] for p in PRIORIDADES_VALIDAS}
    for task in concluidas:
        horas_por_prioridade[task["prioridade"]].append(_horas_de_conclusao(task))

    todas_as_horas = [h for horas in horas_por_prioridade.values() for h in horas]
    tempo_medio: dict[str, float] = {"geral": _media(todas_as_horas)}
    for prioridade, horas in horas_por_prioridade.items():
        tempo_medio[prioridade] = _media(horas)

    resultado: dict[str, Any] = {
        "total_tarefas": len(tasks),
        "total_concluidas": len(concluidas),
        "total_pendentes": len(tasks) - len(concluidas),
        "tempo_medio_conclusao_horas": tempo_medio,
        "taxa_atraso_percentual": _taxa_atraso(concluidas),
    }
    logger.info("Análise concluída: %s", resultado)
    return resultado
