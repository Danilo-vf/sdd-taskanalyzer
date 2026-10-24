# CONTEXT_RULES - Regras de Governança para Agentes de IA

Estas regras são a fonte da verdade para qualquer assistente de IA que gere código neste repositório.

## Diretrizes Arquiteturais (Obrigatórias)
- Usar Python 3.11 ou superior.
- Usar type hints em 100% das funções e parâmetros.
- Seguir o princípio de Responsabilidade Única (SRP) e o PEP 8.
- Documentar módulos, classes e funções com docstrings no padrão Google.
- Manter funções pequenas, coesas e com um único propósito.
- Tratar erros com exceções específicas e mensagens claras.
- Usar o módulo padrão `logging` para registrar eventos relevantes.
- Usar nomes de variáveis e funções descritivos.

## Proibições Explícitas
- Não usar bibliotecas externas não autorizadas (apenas a biblioteca padrão e pytest).
- Não alterar, remover ou adaptar os cenários de teste.
- Não alterar a estrutura de pastas do repositório.
- Não persistir dados em arquivos ou bancos de dados.
- Não alterar a assinatura (nome e parâmetros) das funções públicas sem autorização.
- Não gerar código sem testes correspondentes.
- Não inserir código duplicado ou desnecessário.
- Não assumir comportamentos que não estejam em specs/task_analyzer_spec.md.

## Regras de Interação com a IA
- Fornecer sempre o contexto completo (este arquivo e a especificação) antes de pedir código.
- Revisar criticamente todo código gerado antes de aceitar.
- Rejeitar respostas que violem qualquer proibição acima.
- Em caso de dúvida sobre o contrato, perguntar em vez de assumir
