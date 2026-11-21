# Configuração passo a passo

Tempo estimado: 20 a 30 minutos.

## 1. O que você precisa

| Item | Para quê |
|---|---|
| [Claude Code](https://claude.com/claude-code) no app desktop (Windows ou Mac) | Roda o agente e agenda a execução diária |
| Extensão **Claude in Chrome** no Chrome (ou outro navegador Chromium, como Brave) | O agente navega com as **suas** sessões já logadas |
| Contas nas plataformas (Gupy, InfoJobs, CIEE, Nube…) | Você faz login uma vez; o agente nunca digita senha |
| Conector do **Gmail** (opcional) | Ler e-mails de processos seletivos |
| Python 3.10+ (opcional) | Rodar o validador da planilha |

## 2. Prepare a pasta

```bash
git clone https://github.com/kaiokkj-dev/olheiro.git
cd olheiro
cp modelos/regras-agente.exemplo.md regras-agente.md
cp modelos/candidaturas.exemplo.csv candidaturas.csv
```

No Windows (PowerShell), troque `cp` por `Copy-Item`.

Depois:

1. Edite `regras-agente.md` com o seu perfil. Seja específico: o agente **só** pode
   afirmar o que estiver ali. Liste os projetos com a stack e quando usar cada um.
2. Apague as linhas de exemplo de `candidaturas.csv` (deixe só o cabeçalho).
3. Coloque o PDF do seu currículo na pasta.

`regras-agente.md`, `candidaturas.csv` e `*.pdf` estão no `.gitignore`, então não vão
para o GitHub por engano.

## 3. Faça login nas plataformas

Abra o navegador onde a extensão Claude in Chrome está instalada e entre em cada
plataforma da seção 2 das regras. O agente usa essas sessões. Se alguma pedir login no
meio da execução, ele marca `precisa_voce` e segue para a próxima.

## 4. Crie a tarefa agendada

1. Abra `tarefa/olheiro-diario.md` e troque `{{PASTA}}`, `{{NOME}}` e `{{CV}}`.
2. No Claude Code, abra a pasta do projeto e peça:
   > Crie uma tarefa agendada chamada `olheiro-diario`, todo dia às 9h, com este prompt: *(cole o conteúdo do arquivo)*
3. Rode a tarefa uma vez manualmente e acompanhe. Ajuste as regras com base no que
   ver (ex.: uma resposta de formulário que sempre trava).

Dica: as permissões das ferramentas (navegador, e-mail, notificação) são pedidas na
primeira execução. Aprove com você presente, antes de deixar rodar sozinho.

## 5. Veja o painel

Abra `painel/index.html` no navegador e clique em **Abrir candidaturas.csv**. O painel
mostra resumo por status, filtros por plataforma, busca e prazos dos próximos 7 dias em
vermelho. O arquivo é lido só no seu navegador; nada é enviado para lugar nenhum.

## 6. Valide a planilha

```bash
python scripts/validar_csv.py candidaturas.csv
```

Aponta data fora do formato, status desconhecido, nota inválida, descartada sem motivo
e links repetidos.

## Problemas comuns

| Sintoma | O que fazer |
|---|---|
| "extensão não conectada" | Abra o navegador e confira se a extensão está ativa e logada |
| Toda vaga da Gupy vira `precisa_voce` | A sessão da Gupy expirou; entre de novo no navegador |
| Página do CIEE em branco | Entre pelo login e navegue só pelo menu |
| Notificação não chega no celular | O push precisa do Remote Control ligado no app |
| Candidatura com resposta errada | Adicione a resposta certa na seção 1 das regras |
