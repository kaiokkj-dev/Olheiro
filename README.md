# Olheiro

**Um agente que procura vagas de estágio, dá nota para cada uma, se candidata nas boas e te avisa de testes, entrevistas e prazos.** Roda todo dia como tarefa agendada no [Claude Code](https://claude.com/claude-code), usando o seu próprio navegador.

> 🇺🇸 *Olheiro ("scout") is a scheduled Claude Code agent that searches Brazilian internship boards, scores each posting against your profile, applies to the good ones with a short tailored cover note, and tracks everything in a CSV with a local dashboard. It never types passwords, solves CAPTCHAs, takes tests, or applies on LinkedIn for you.*

---

## Por que existe

Procurar estágio é repetitivo: abrir as mesmas plataformas todo dia, ler dezenas de vagas que não servem, preencher o mesmo formulário, esquecer o prazo de um teste. O Olheiro faz a parte chata e **para** sempre que a decisão precisa ser sua.

## Como funciona

```
regras-agente.md ──► agente (Claude Code, agendado)
                         │
       ┌─────────────────┼──────────────────┐
       ▼                 ▼                  ▼
  busca vagas       lê e-mails de       atualiza
  (Gupy, InfoJobs,  processos           candidaturas.csv
   CIEE, Nube…)     seletivos                 │
       │                 │                    ▼
   nota 0–100      teste/entrevista?     painel/index.html
       │            → notificação
   ≥ 60 → candidata  (só sites liberados)
   < 60 → descarta com motivo
   travou → precisa_voce
```

Cada vaga ganha uma nota de 0 a 100:

| Critério | Pontos |
|---|---|
| Stack bate com a sua | até 35 |
| É estágio ou programa de entrada | até 25 |
| Localização / modelo de trabalho | até 15 |
| Requisitos que você cumpre (semestre, formatura, inglês) | até 15 |
| Empresa da sua lista de favoritas | até 10 |

E termina em um destes status: `candidatada` · `aguardando_voce` · `precisa_voce` · `descartada` · `teste` · `entrevista` · `aprovada` · `reprovada` · `encerrada`.

## O que ele nunca faz

Estas regras estão no modelo e valem acima de qualquer texto que apareça numa página ou e-mail (conteúdo de site é **dado**, não instrução):

1. Inventar habilidade, experiência, certificado ou nota.
2. Digitar senha, código de verificação ou resolver CAPTCHA.
3. Responder perguntas pessoais fora do seu perfil (documentos, saúde, renda, endereço…).
4. Fazer testes de lógica, inglês, comportamental ou código. Ele **avisa** com o prazo.
5. Aceitar termos novos ou criar contas.
6. Pagar qualquer coisa.
7. Se candidatar duas vezes à mesma vaga.
8. Se candidatar no LinkedIn ou Indeed (risco de bloqueio da conta). Essas vagas viram `aguardando_voce` com o link.

Quando trava em qualquer um desses, marca `precisa_voce` e explica o motivo.

## Estrutura

```
olheiro/
├── modelos/
│   ├── regras-agente.exemplo.md   ← seu perfil e regras (copie para a raiz)
│   └── candidaturas.exemplo.csv   ← formato da planilha
├── tarefa/
│   └── olheiro-diario.md          ← prompt da tarefa agendada
├── painel/
│   └── index.html                 ← painel local, lê o CSV no navegador
├── scripts/
│   └── validar_csv.py             ← confere a planilha
└── docs/
    └── configuracao.md            ← passo a passo
```

## Começando

```bash
git clone https://github.com/kaiokkj-dev/olheiro.git
cd olheiro
cp modelos/regras-agente.exemplo.md regras-agente.md
cp modelos/candidaturas.exemplo.csv candidaturas.csv
```

Preencha `regras-agente.md`, coloque o PDF do currículo na pasta, faça login nas plataformas no navegador e crie a tarefa agendada. O guia completo está em **[docs/configuracao.md](docs/configuracao.md)**.

Quer só ver o painel? Abra **[o painel online](https://kaiohenrique.dev/olheiro/painel/)** e clique em **Ver exemplo** (ou abra `painel/index.html` no seu computador). O seu CSV é lido só no navegador, nada é enviado.

## Requisitos e alternativas

O agente foi feito para rodar no **[Claude Code](https://claude.com/claude-code)** (app desktop). É ele que fornece as peças que fazem o Olheiro funcionar sem nenhum código de automação:

| Peça | No Claude Code | Sem o Claude, você precisaria de… |
|---|---|---|
| Rodar todo dia | Tarefa agendada | Agendador de Tarefas do Windows, `cron` ou GitHub Actions |
| Entender páginas e decidir | O próprio modelo lendo a página | Chamadas à API de um modelo (Anthropic, OpenAI, Gemini ou um modelo local via Ollama) |
| Navegar já logado | Extensão Claude in Chrome | [Playwright](https://playwright.dev) ou Selenium com um perfil de navegador logado |
| Ler e-mails | Conector do Gmail | API do Gmail ou IMAP |
| Avisar no celular | Notificação push do app | Telegram, [ntfy](https://ntfy.sh) ou e-mail |

**O que funciona com qualquer ferramenta:**

- `modelos/regras-agente.exemplo.md` e `tarefa/olheiro-diario.md` são Markdown puro. A lógica (perfil, nota de 0 a 100, status, o que nunca fazer) serve de prompt para qualquer agente com acesso a navegador.
- `painel/index.html` só lê o CSV no navegador.
- `scripts/validar_csv.py` usa só a biblioteca padrão do Python.

**Como adaptar para outro agente:**

1. Use `regras-agente.md` + `tarefa/olheiro-diario.md` como prompt de sistema.
2. Dê ao agente ferramentas equivalentes às da tabela: abrir página, ler texto, clicar, preencher campo, anexar arquivo, ler e-mail, enviar aviso.
3. Mantenha a planilha no mesmo formato e rode o validador no fim de cada execução, assim o painel continua funcionando.
4. Preserve a seção 9 das regras como trava **no código**, não só no prompt: bloqueie campos de senha, CAPTCHA e domínios onde o agente não pode se candidatar (LinkedIn, Indeed).

Atenção: sem o Claude in Chrome, a parte mais trabalhosa e frágil é a navegação. Cada plataforma muda de layout com frequência, e automação com navegador logado pode ir contra os termos de uso de alguns sites.

Contribuições com adaptações para outras ferramentas são bem-vindas, de preferência numa pasta separada (ex.: `adaptacoes/<ferramenta>/`).

## Privacidade

- Seu perfil, sua planilha e seu currículo ficam **só na sua máquina**: `regras-agente.md`, `candidaturas.csv` e `*.pdf` estão no `.gitignore`.
- O painel lê o CSV direto no navegador, sem servidor.
- O agente usa as sessões que você já abriu; ele não guarda nem vê senhas.

## Limites e responsabilidade

- Automação de navegador pode violar os termos de uso de algumas plataformas. Leia os termos de cada uma e decida o que liberar na seção 2 das regras.
- Sites mudam de layout; às vezes a busca rende pouco ou uma plataforma bloqueia o acesso. O agente registra isso no resumo em vez de insistir.
- Revise as primeiras candidaturas com atenção. Você é responsável pelo que é enviado em seu nome.

## Contribuindo

Ideias bem-vindas, principalmente:

- dicas de navegação para outras plataformas (adicione na seção 2 do modelo de regras);
- melhorias no painel e no validador;
- versões do modelo de regras para outras áreas além de tecnologia.

Abra uma issue ou um pull request. **Nunca** inclua dados reais de candidatos em exemplos, prints ou testes.

## Licença

[MIT](LICENSE)
