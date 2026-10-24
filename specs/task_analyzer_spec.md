# Especificação SDD - TaskAnalyzer

## 1. Propósito
O TaskAnalyzer analisa uma lista de tarefas e calcula métricas de produtividade: totais, tempo médio de conclusão (geral e por prioridade) e taxa de atraso.

## 2. Contrato da função
Função pública: analyze_tasks(tasks: list[dict]) -> dict
Exceção pública: TaskValidationError (herda de ValueError)

### Entrada: cada tarefa é um dicionário com as chaves
- id (int, maior que 0)
- titulo (str, não vazio)
- prioridade (str): "baixa", "media" ou "alta"
- status (str): "concluida" ou "pendente"
- data_criacao (datetime)
- data_prazo (datetime)
- data_conclusao (datetime ou None; obrigatória quando status é "concluida")

### Saída: dicionário com as chaves
- total_tarefas (int)
- total_concluidas (int)
- total_pendentes (int)
- tempo_medio_conclusao_horas (dict com as chaves "geral", "baixa", "media", "alta", valores float)
- taxa_atraso_percentual (float)

## 3. Regras de negócio
- Tempo de conclusão = data_conclusao - data_criacao, em horas.
- Médias consideram apenas tarefas concluídas.
- Uma tarefa concluída está em atraso se data_conclusao > data_prazo.
- taxa_atraso_percentual = (concluídas em atraso / total de concluídas) x 100.
- Valores float são arredondados em 2 casas decimais.
- Lista vazia, ou sem tarefas concluídas, retorna 0.0 em todas as médias e na taxa de atraso, sem lançar exceção.
- Divisão por zero deve ser sempre prevenida.

## 4. Validações (lançam TaskValidationError)
- Campo obrigatório ausente.
- prioridade ou status fora dos valores permitidos.
- data_conclusao anterior a data_criacao.
- Tarefa "concluida" sem data_conclusao.

## 5. Cenários de aceite
Cenário 1 (Sucesso): dado um conjunto de tarefas válidas, quando analyze_tasks é executada, então retorna as métricas corretas (totais, tempo médio geral e por prioridade, taxa de atraso).
Cenário 2 (Erro): dado uma tarefa com data_conclusao anterior a data_criacao, quando analyze_tasks é executada, então lança TaskValidationError com mensagem clara.
Cenário 3 (Borda): dado uma lista vazia ou apenas com tarefas pendentes, quando analyze_tasks é executada, então retorna 0.0 nas médias e na taxa de atraso, sem exceção.
