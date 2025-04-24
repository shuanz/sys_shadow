# Issues

## Issue #6 - Implementação do Sistema Bancário

### Descrição
Implementar o sistema bancário do jogo com suporte a criptomoeda (cybit) e recompensas automáticas.

### Requisitos
- [x] Comando `bank` para mostrar saldo em cybit
- [x] Recompensas automáticas após missões concluídas
- [x] Histórico de transações
- [x] Persistência de dados bancários
- [x] Conversão entre créditos e cybit

### Implementação
- Criado módulo `src/core/bank.py` para gerenciar o sistema bancário
- Implementado sistema de transações com histórico
- Adicionado suporte a criptomoeda cybit
- Integrado com o sistema de missões para recompensas automáticas
- Adicionado persistência de dados em `bank_history.json`

### Status
✅ Concluído

### Data de Conclusão
2024-03-19

## Issue #7 - Integração com LLM

### Descrição
Implementar integração com Language Learning Models para diálogos dinâmicos com NPCs.

### Requisitos
- [x] Interface com LLM para geração de diálogos
- [x] Suporte a modelos locais e via API
- [x] Geração de diálogos para missões
- [x] Respostas dinâmicas de NPCs
- [x] Histórico de conversas
- [x] Persistência de diálogos

### Implementação
- Criado módulo `src/core/llm_interface.py` para gerenciar integração com LLM
- Implementado sistema de geração de diálogos
- Adicionado suporte a diferentes tipos de LLM
- Integrado com sistema de missões para diálogos dinâmicos
- Adicionado persistência de conversas em `conversation_history.json`

### Status
✅ Concluído

### Data de Conclusão
2024-03-19 