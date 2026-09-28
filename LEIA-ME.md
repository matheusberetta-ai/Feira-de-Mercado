# Dashboard Financeiro — Feira de Mercado

Dashboard web da EESC Jr. & Produção Jr., com dados vindos direto do **Google Sheets** e acesso restrito a emails **@eescjr.com.br**.

**Como funciona:**
1. Você mantém a planilha financeira no Google Sheets (uma URL só, sempre a mesma).
2. Sempre que abrir o dashboard (ou clicar em "↻ Atualizar dados"), ele busca a versão mais recente da planilha automaticamente.
3. Só quem entrar com email **@eescjr.com.br** consegue ver o conteúdo.

O dashboard tem 5 seções: **Visão Geral · Empresas Fechadas · Fluxo de Caixa · Simulador · Gastos**.

---

## 🔧 Setup completo (fazer uma vez)

Se você já tem o dashboard rodando e só quer configurar Sheets + login, pule para o passo 2.

### Passo 1 — Publicar o site no GitHub Pages

*(Se já publicou antes, pule.)*

1. Crie um repositório em https://github.com/ (público) — sugestão: `feira-de-mercado`
2. Faça upload de **todos** os arquivos desta pasta (incluindo `.github/workflows/deploy.yml` e a pasta `assets/`)
3. **Settings → Pages → Source: GitHub Actions**
4. Aguarde ~1 min. Sua URL fica: `https://SEUUSUARIO.github.io/feira-de-mercado/`

### Passo 2 — Colocar a planilha no Google Sheets do domínio EESC Jr.

1. Faça login em https://drive.google.com com sua conta **@eescjr.com.br**
2. Se sua planilha ainda está em `.xlsx`:
   - Clique em **+ Novo → Upload de arquivo** → envie o `.xlsx`
   - Clique com botão direito no arquivo → **Abrir com → Planilhas Google**
   - Isso cria uma versão como Google Sheets. Pode deletar o `.xlsx` depois.
3. Se já está em outro domínio: **Arquivo → Fazer uma cópia** → mova a cópia para uma pasta do domínio `@eescjr.com.br`
4. Com a planilha aberta, clique em **Compartilhar** (canto superior direito)
5. Em **"Acesso geral"**, mude para **"Qualquer pessoa com o link"** e mantenha como **"Leitor"**
6. Clique em **Copiar link** e cole aqui num bloco de notas — vamos precisar
7. A URL vai ter esse formato:
   ```
   https://docs.google.com/spreadsheets/d/AQUI_TEM_UM_CODIGO_LONGO/edit#gid=0
   ```
   Guarde só o pedaço do meio (`AQUI_TEM_UM_CODIGO_LONGO`) — é o **SHEET_ID**.

> **Sobre segurança:** com "qualquer pessoa com o link" só vê quem tem o link. A trava real (só @eescjr.com.br) vem do login no dashboard, no próximo passo.

### Passo 3 — Criar o Client ID do Google (para a trava de login)

Este passo é feito **uma vez só**. Vai levar uns 10 minutos, mas é tudo apontar-e-clicar.

**3.1 — Criar o projeto**
1. Acesse https://console.cloud.google.com/
2. No topo, clique no seletor de projeto → **NOVO PROJETO**
3. Nome: `Feira de Mercado` · Organização: `eescjr.com.br` (se aparecer)
4. Criar. Espere ~30 segundos. Depois selecione esse projeto no seletor.

**3.2 — Configurar a tela de consentimento**
1. Menu (☰) → **APIs e serviços → Tela de permissão OAuth**
2. Tipo de usuário: **Interno** (aparece só se você é admin do Workspace — assim só quem tem `@eescjr.com.br` pode logar; se não aparecer "Interno", escolha "Externo" que também funciona)
3. Continuar
4. Preencha:
   - Nome do app: `Dashboard Feira de Mercado`
   - Email de suporte: seu email `@eescjr.com.br`
   - Email do desenvolvedor: seu email `@eescjr.com.br`
5. Salvar e continuar → pule "Escopos" (Salvar e continuar) → pule "Usuários" → Voltar ao painel

**3.3 — Criar o Client ID**
1. Menu (☰) → **APIs e serviços → Credenciais**
2. **+ CRIAR CREDENCIAIS → ID do cliente OAuth**
3. Tipo de aplicativo: **Aplicativo da Web**
4. Nome: `Dashboard Web`
5. Em **Origens JavaScript autorizadas → + ADICIONAR URI**, adicione:
   - `https://SEUUSUARIO.github.io` (a URL do seu GitHub Pages, sem barra no final)
   - `http://localhost:8765` (para testar localmente, opcional)
6. **Criar**
7. Vai aparecer uma janelinha com o **ID do cliente** — algo tipo `123456789012-abc...xyz.apps.googleusercontent.com`
8. **Copie esse ID inteiro** e guarde junto com o SHEET_ID.

### Passo 4 — Colocar os dois códigos no dashboard

1. Abra o arquivo `config.js` desta pasta com o **Bloco de Notas** (clique direito → Abrir com → Bloco de Notas)
2. Substitua os dois `COLE_AQUI...`:
   ```js
   SHEET_ID: "1AbCd_seu_id_aqui_XyZ",
   OAUTH_CLIENT_ID: "123456789012-abc.apps.googleusercontent.com",
   ```
3. Salve o arquivo (Ctrl+S)
4. Faça upload do `config.js` atualizado no GitHub (na página do repositório, clique no arquivo → ícone de lápis → cole o conteúdo → Commit)
5. Aguarde ~1 min. Pronto.

### Passo 5 — Testar

1. Abra `https://SEUUSUARIO.github.io/feira-de-mercado/`
2. Clique em **Sign in with Google**
3. Entre com sua conta **@eescjr.com.br**
4. Dashboard carrega os dados da planilha em ~2 segundos ✅

Se entrar com outro email, ele bloqueia e mostra "Acesso restrito a @eescjr.com.br".

---

## 🔄 Uso do dia a dia

- **Editar dados:** edita a planilha no Google Sheets normalmente.
- **Ver mudanças:** abre o dashboard, clica em **↻ Atualizar dados** no canto inferior esquerdo. Ou espera 10 min (recarrega sozinho).
- **Compartilhar com o time:** só passa a URL do GitHub Pages. Cada pessoa faz login com o próprio email `@eescjr.com.br`.

---

## 📁 Arquivos desta pasta

| Arquivo | Para que serve |
|---|---|
| `index.html` | O dashboard |
| `config.js` | **⭐ Único arquivo que você edita** — SHEET_ID e OAUTH_CLIENT_ID |
| `assets/logo-m.png` | Logo da Feira de Mercado |
| `assets/banner-ejs.png` | Banner EESC Jr + Produção Jr |
| `data.json` | Snapshot local (usado como fallback offline) |
| `build.py` | Gera `data.json` a partir da planilha `.xlsx` local (uso offline) |
| `atualizar_dashboard.bat` | Regera `data.json` local + abre em `http://localhost:8765` |
| `Financeiro - FEIRA DE MERCADO.xlsx` | Cópia local da planilha (opcional, só para modo offline) |
| `LEIA-ME.md` | Este arquivo |

---

## ❓ Perguntas frequentes

**A planilha é vista por qualquer um que tenha o link?**
Tecnicamente sim, mas o dashboard só mostra os dados para quem entrar com email `@eescjr.com.br`. Se você quer uma trava real também na planilha (mais seguro), veja "Melhorias futuras" no fim.

**Se eu adicionar uma coluna nova na planilha, o dashboard quebra?**
Não quebra, mas essa coluna nova não aparece automaticamente. O dashboard lê colunas específicas (documentadas no `index.html`, seção "buscarNoSheets"). Se quiser adicionar coisas novas, me chama.

**Preciso rodar algum script?**
Não, no modo Sheets tudo é automático. O `build.py` só serve se você quiser ter uma cópia offline dos dados (backup ou testar sem internet).

**E se eu quiser trabalhar sem internet ou testar mudanças locais?**
Abre `config.js`, muda `OFFLINE_MODE: true`, salva, e abra `atualizar_dashboard.bat`. Ele lê o `.xlsx` local e gera `data.json`. O dashboard passa a usar essa versão local.

**Quantos usuários posso ter?**
Ilimitado. Não paga nada. Google Sheets aguenta a leitura sem problema.

**Preciso de servidor, hospedagem, banco de dados?**
Nada. Só o GitHub (grátis) e o Google (grátis).

---

## 🔒 Melhorias futuras de segurança (opcional)

Se um dia quiser fechar totalmente o acesso à planilha (não só ao dashboard):

- Compartilhe a planilha **só com o domínio @eescjr.com.br** em vez de "qualquer pessoa com link"
- Isso exige o dashboard usar OAuth com escopo `sheets.readonly` para ler
- É uma mudança de ~30 linhas no `index.html` — me chama que faço

---

## 🆘 Alguma coisa deu errado?

- **"O Client ID do Google ainda não foi configurado"** → você não editou `config.js` ainda, ou não subiu ele para o GitHub.
- **"Aba X não acessível (HTTP 404)"** → o nome da aba da planilha está diferente do esperado. As abas devem chamar-se: `Parâmetros`, `Vendas`, `Gastos Previstos`, `Gastos Realizados`, `Fluxo de Caixa`.
- **"Aba X não acessível (HTTP 401/403)"** → a planilha não está com o compartilhamento "qualquer pessoa com o link".
- **Login carrega infinito** → a URL do seu GitHub Pages não foi adicionada nas "Origens autorizadas" do OAuth Client ID (passo 3.3).
- **Dashboard mostra dados desatualizados** → clica em "↻ Atualizar dados" no canto inferior esquerdo.
- **Não sei o que fazer** → me manda o print da tela de erro.
