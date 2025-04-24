# Terminal Hacker RPG - Product Requirements Document (PRD)

## 📌 Visão Geral

### 🎯 Objetivo
Criar um jogo de RPG ambientado em um mundo cyberpunk, inteiramente jogável através de um terminal estilizado. O jogador assume o papel de um hacker contratado anonimamente para realizar invasões em sistemas de megacorporações, com narrativa e sistemas gerados de forma procedural.

### 🧠 Público-alvo
Jogadores que gostam de:
- Terminal/Linux
- Jogos de hacking
- RPGs narrativos e imersivos
- Estética cyberpunk
- Sistemas procedurais e expansíveis

---

## 🚀 Funcionalidades Principais (MVP)

### 1. Terminal Hacker
- Interface 100% baseada em terminal estilo Linux.
- Paleta de cores verde/preto ou âmbar/preto, com efeito CRT opcional.
- Prompt estilizado: `h4ck3r@voidnet:~$`.

### 2. Sistema de Comandos
Comandos disponíveis no MVP:
- `ls`, `cd`, `cat` — exploração de arquivos.
- `mail` — mensageiro com contratante.
- `bank` — consultar saldo em cripto.
- `hack` — iniciar invasão.
- `store` — acessar loja de programas.
- `help` — mostrar ajuda.

### 3. Missões e Contratante
- Missões geradas proceduralmente com objetivo, dificuldade e recompensa.
- Contratante interage via terminal usando app de mensagens.
- NPC pode ser alimentado por LLM (ex: GPT) para diálogos dinâmicos (opcional no MVP).

### 4. Invasões de Sistemas
- Simulador com múltiplas etapas: `scan`, `exploit`, `download`.
- Estrutura de arquivos gerada proceduralmente.
- Defesas aumentam com o progresso do jogador.

### 5. Loja de Softwares
- Comando `store` lista programas à venda.
- Exemplos:
  - `brute` — força bruta.
  - `sniff` — monitoramento de pacotes.
  - `cloak` — ofuscação de rastros.
- Programas melhoram desempenho nas invasões.

### 6. Banco
- Comando `bank` mostra saldo em `cybit` (criptomoeda).
- Recompensas automáticas após missões concluídas.

---

## ⚙️ Requisitos Técnicos

### Tecnologias sugeridas
- **Backend:** Python
- **Terminal UI:** [`rich`](https://github.com/Textualize/rich), [`prompt_toolkit`](https://github.com/prompt-toolkit/python-prompt-toolkit) ou [`textual`](https://github.com/Textualize/textual)
- **Banco de dados:** SQLite
- **LLM (opcional):** API GPT (OpenAI ou alternativa)

### Geração procedural
- Estruturas de arquivos em sistemas-alvo.
- Missões com alvo, objetivo, defesa, recompensa.
- Megacorporações e cidade fictícia com distritos.

---

## 💻 Exemplo de Uso no Terminal

```shell
h4ck3r@voidnet:~$ mail
[1] New message from: unknown@darkgrid.zz
> Your target is Neuronet Inc. Find their AI project logs.

h4ck3r@voidnet:~$ hack neuronet.ai
Scanning... OK
Exploiting port 443... OK
Accessing /vault/logs/... Download complete

h4ck3r@voidnet:~$ bank
Balance: 1.532 cybit
```

---

## 🗺️ Roadmap MVP

```markdown
| Fase     | Entregáveis                              | Tempo Estimado |
|----------|-------------------------------------------|----------------|
| Fase 1   | Interface de Terminal e comandos básicos  | 1 semana       |
| Fase 2   | Mensageiro com contratante e missões      | 1 semana       |
| Fase 3   | Simulador de invasão                      | 2 semanas      |
| Fase 4   | Loja com programas                        | 1 semana       |
| Fase 5   | Banco e sistema de recompensas            | 1 semana       |
| Fase 6   | Integração com LLM (opcional)             | 1 semana       |
```

---

## 🔮 Futuras Expansões (pós-MVP)

```markdown
- Sistema de rastreio e exposição (trace level).
- Facções e reputação.
- Cidade expandida com distritos únicos.
- Multi-terminal com sessões remotas.
- Multiplayer (local/LAN).
```

---

## 🧱 Stack Recomendada

```markdown
| Camada           | Tecnologia            | Justificativa                                                                 |
|------------------|-----------------------|------------------------------------------------------------------------------|
| **Linguagem**     | `Python`              | Alta produtividade, bibliotecas ricas para UI textual, geração procedural e APIs |
| **UI de Terminal**| `Textual` ou `Rich`   | Interfaces ricas em terminal, suporte a layout, cores, animações, efeitos CRT |
| **Gerador Procedural** | `random`, `numpy`, `faker`, etc. | Bibliotecas para criação de estruturas e conteúdo dinâmico |
| **LLM (opcional)** | `OpenAI API`, `local LLM`, `Ollama`, etc. | Para gerar falas/missões dinâmicas do contratante |
| **Persistência**  | `SQLite`              | Leve, embutido, ideal para armazenar histórico, missões e inventário |
| **Testes**        | `pytest`              | Framework simples para garantir estabilidade dos comandos e simulações |
| **Empacotamento** | `setuptools`, `poetry` | Para empacotar o jogo em CLI ou script de instalação |
| **Distribuição**  | `PyPI`, `brew`, `snap`, ou `docker` | Distribuição multiplataforma com setup mínimo |
| **Extra (futuro)**| `Websockets`, `ZeroMQ` | Comunicação para multiplayer local/remoto, se for expandir |
```
