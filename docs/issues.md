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