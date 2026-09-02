# Dashboard Financeiro — Feira de Mercado

Dashboard web profissional para acompanhar o resultado financeiro da Feira de Mercado, com dados que vêm direto da planilha Excel `Financeiro - FEIRA DE MERCADO.xlsx`.

O dashboard tem 5 seções:

- **Visão Geral** — KPIs principais (faturamento, gasto, resultado, equilíbrio, caixa) e gráficos de vendas por pacote / por EJ.
- **Empresas Fechadas** — tabela filtrável com todas as empresas que fecharam cota, valor contratado, custo do estande, margem e % recebido.
- **Fluxo de Caixa** — saldo acumulado mês a mês, entradas × saídas e identificação do pior mês.
- **Simulador** — para eventos futuros: você ajusta quantas cotas a mais de cada pacote pretende vender e vê o lucro/prejuízo projetado, além do **break-even** (quantas cotas ainda faltam para sair do zero).
- **Gastos** — composição do gasto previsto, pago vs. pendente, e detalhe de cada linha.

---

## 🧠 Antes de tudo: como isso funciona?

Sua planilha vira o dashboard em **três etapas**:

1. **A planilha Excel** (`Financeiro - FEIRA DE MERCADO.xlsx`) continua sendo a fonte da verdade. Você edita ela normalmente.
2. **Um script em Python** (`build.py`) lê a planilha e gera um arquivo `data.json` — que é a "versão traduzida" dos dados que o dashboard consegue entender.
3. **O dashboard** (`index.html`) é uma página web que lê o `data.json` e desenha os gráficos e tabelas.

Você tem duas formas de rodar essa "tradução":

- **Localmente** — dando duplo clique em `atualizar_dashboard.bat` (roda no seu computador).
- **Automaticamente pelo GitHub** — quando você sobe uma planilha nova, o GitHub roda o script sozinho e publica a nova versão do dashboard em uma URL pública.

---

## 💻 Uso local (no seu computador)

### Requisito único: Python

Você precisa ter o Python instalado uma vez. Se ainda não tem:

1. Baixe em https://www.python.org/downloads/
2. Rode o instalador e **marque a caixinha "Add Python to PATH"** (é o passo mais importante — sem isso o script não funciona).

### Para atualizar o dashboard:

1. Edite a planilha `Financeiro - FEIRA DE MERCADO.xlsx` normalmente.
2. Dê **duplo clique** em `atualizar_dashboard.bat`.
3. Isso vai:
   - Ler a planilha
   - Gerar um `data.json` novo
   - Abrir o dashboard automaticamente no seu navegador em `http://localhost:8765`
4. Enquanto quiser usar, deixe a janela preta aberta. Quando terminar, feche ela.

> **Por que precisa desse "servidor local"?** Navegadores modernos por segurança não deixam uma página HTML aberta direto do disco (`file://`) carregar um arquivo `.json`. O `atualizar_dashboard.bat` levanta um mini-servidor local que resolve isso. Alternativa: publique no GitHub Pages (próxima seção) e acesse de qualquer lugar.

---

## 🌐 Publicando no GitHub (dashboard online e automatizado)

Assim ele fica **acessível em qualquer lugar** por uma URL tipo `https://seunome.github.io/feira-de-mercado/`, e **atualiza sozinho** toda vez que você subir uma planilha nova.

### Passo 1 — Criar o repositório

1. Entre em https://github.com/ (você disse que já tem conta).
2. Canto superior direito, clique no **+** → **New repository**.
3. Preencha:
   - **Repository name:** `feira-de-mercado` (ou o nome que preferir)
   - **Public** (obrigatório se você quiser usar o GitHub Pages grátis)
   - **NÃO marque** "Add a README file" (já temos um)
4. Clique em **Create repository**.

### Passo 2 — Enviar os arquivos

Você vai ver uma tela do GitHub com várias instruções. Ignore as caixas com comandos e faça assim:

1. Ache a linha em azul que diz **"uploading an existing file"** (deve estar em algum lugar da tela). Clique nela.
   - Se não achou: no repositório vazio, clique em **Add file** → **Upload files**.
2. **Arraste todos os arquivos desta pasta** para a caixa do navegador. Deve incluir:
   - `index.html`
   - `data.json`
   - `build.py`
   - `atualizar_dashboard.bat`
   - `Financeiro - FEIRA DE MERCADO.xlsx`
   - `LEIA-ME.md`
   - `.gitignore`
   - A pasta `.github` inteira (contém a receita que faz o dashboard rebuildar sozinho)

   > ⚠️ Windows Explorer esconde a pasta `.github` por começar com ponto. Se você não vê ela: no Explorer, aba **Exibir → Mostrar → Itens ocultos**.

3. Role a página até o fim, escreva uma mensagem tipo *"primeiro envio"* e clique em **Commit changes**.

### Passo 3 — Ligar o GitHub Pages

O GitHub Pages é o serviço gratuito que hospeda seu dashboard.

1. No repositório, clique em **Settings** (aba lá em cima).
2. Menu esquerdo → **Pages**.
3. Em **Source**, escolha **GitHub Actions**.
4. Pronto. Não precisa mexer em mais nada.

### Passo 4 — Aguardar o primeiro build

1. Volte para a aba **Actions** do repositório.
2. Você vai ver um workflow chamado **"Publicar Dashboard"** rodando (ícone amarelo girando).
3. Espere terminar (dá ~1 minuto). Vira um ✅ verde quando pronto.
4. Volte em **Settings → Pages**. No topo vai aparecer:
   > **Your site is live at** `https://SEUNOME.github.io/feira-de-mercado/`
5. Esse é o link do seu dashboard! Salve nos favoritos.

### Como atualizar depois

Toda vez que a planilha mudar:

1. Vá até o repositório no GitHub.
2. Clique no arquivo `Financeiro - FEIRA DE MERCADO.xlsx`.
3. Ícone de lápis (canto direito) → escolha **"Upload files"** OU delete e faça upload de novo.
4. Confirme (**Commit changes**).
5. Em ~1 minuto o dashboard estará atualizado na URL pública. Não precisa mexer em mais nada — o GitHub roda o `build.py` sozinho e republica.

---

## ❓ Perguntas frequentes

**Preciso mexer no `data.json` na mão?**
Não. Ele é gerado automaticamente. Se você editar direto, será sobrescrito no próximo build.

**Posso mudar cores, textos, adicionar seções?**
Sim. É só editar `index.html` (é um único arquivo, todo comentado por seção). Se travar, é só me chamar.

**A planilha vai ficar pública se eu subir para um repo público?**
Sim. Quem souber a URL do repositório consegue baixar. Se isso for problema:
- Opção A: crie o repositório como **Private**. Aí o GitHub Pages exige uma conta paga (GitHub Pro).
- Opção B: em vez de subir a planilha, você mantém ela só localmente, roda `atualizar_dashboard.bat` para gerar o `data.json`, e sobe SÓ o `data.json`. Nesse caso, remova o passo "Regerar data.json" do arquivo `.github/workflows/deploy.yml`.

**O que é essa pasta `.github`?**
É uma receita para o GitHub. Diz: *"toda vez que alguém subir algo aqui, rode o `build.py` e publique o resultado no GitHub Pages."* Sem essa pasta, o site publicaria mas não se atualizaria sozinho.

**E se eu quiser adicionar/mudar empresas no simulador?**
As empresas fechadas vêm da aba **Vendas** da planilha. As cotas totais disponíveis vêm da aba **Parâmetros** (tabela de pacotes). Edite lá, rode a atualização, pronto.

---

## 📁 O que tem nesta pasta

| Arquivo | Para que serve |
|---|---|
| `Financeiro - FEIRA DE MERCADO.xlsx` | Sua planilha original — **fonte da verdade** |
| `index.html` | O dashboard em si (não edite se não souber HTML/JS) |
| `data.json` | Dados extraídos da planilha (gerado automaticamente) |
| `build.py` | Script que lê a planilha e gera o `data.json` |
| `atualizar_dashboard.bat` | Duplo clique para atualizar localmente |
| `.github/workflows/deploy.yml` | Receita da automação do GitHub |
| `.gitignore` | Diz ao Git para ignorar arquivos temporários |
| `LEIA-ME.md` | Este arquivo |

---

## 🆘 Alguma coisa deu errado?

- **"Python nao encontrado"** ao rodar o `.bat` → instalar o Python e marcar "Add to PATH".
- **Dashboard abre mas não mostra nada** → geralmente é o `data.json` faltando ou desatualizado. Rode o `.bat` de novo.
- **Workflow do GitHub falhou (X vermelho)** → clique nele, veja a mensagem de erro. Normalmente é a planilha com formato diferente do esperado.
- **Não sei mais o que fazer** → me manda a mensagem de erro exata, resolvo.
