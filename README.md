# I&M Informática — Site Profissional

Projeto completo gerado a partir do PROMPT.pdf: site institucional moderno,
responsivo e otimizado para SEO da I&M Informática, com identidade visual
azul neon / azul escuro / glassmorphism, área do cliente e painel
administrativo.

## Testar com um clique (Windows)
- **`static/testar_site_local.bat`** — abre a versão estática no navegador.
- **`flask_app/instalar_e_rodar.bat`** — instala tudo (Python venv +
  dependências) e roda a versão completa com banco de dados, abrindo o
  navegador sozinho.

## Publicar de graça, automaticamente
Veja **`COMO_PUBLICAR_GRATIS.md`** — passo a passo (com um `.bat` que
envia o código pro GitHub sozinho) para deixar o site no ar sem custo,
usando GitHub Pages (versão estática) e Render (versão completa).

Este pacote entrega **duas versões prontas para publicação gratuita**:

## 1. `static/` — versão estática (HTML + CSS + JS)
Sem backend, 100% front-end. Ideal para publicar de graça no
**GitHub Pages** (ou qualquer hospedagem estática).
- `index.html` — página completa (hero, sobre, serviços, portfólio com
  filtro e lightbox, diferenciais, depoimentos em carrossel, blog,
  downloads, contato com mapa, WhatsApp flutuante).
- `cliente.html` — demonstração da área do cliente (login/cadastro/histórico).
- `admin.html` — demonstração do painel administrativo.
- Tema claro/escuro, animações e todo o conteúdo já preenchido com dados
  de exemplo — é só editar os arrays em `assets/js/main.js` para
  personalizar serviços, portfólio, depoimentos, blog e downloads.

**Publicar no GitHub Pages:**
1. Crie um repositório no GitHub e envie o conteúdo da pasta `static/`.
2. Em *Settings → Pages*, selecione a branch `main` e a pasta raiz `/`.
3. Pronto — o site fica no ar em `https://seuusuario.github.io/repositorio/`.

## 2. `flask_app/` — versão completa com backend (Python + SQLite)
Site dinâmico de verdade: banco de dados SQLite, cadastro/login de
clientes, painel administrativo com CRUD (clientes, serviços, artigos,
portfólio, usuários, mensagens, depoimentos, configurações e backup),
formulário de contato persistido no banco, e proteção contra CSRF, XSS
e SQL Injection. Veja `flask_app/README.md` para instruções detalhadas
de uso e publicação gratuita no **Render**, **Railway** ou
**PythonAnywhere**.

## Identidade visual
- **Paleta:** Azul Neon (`#00E5FF`), Azul Escuro (`#0A1128`), Branco, Preto, Cinza.
- **Tipografia:** Space Grotesk (títulos), Inter (texto), JetBrains Mono (dados/rótulos).
- **Elemento de assinatura:** painel de "diagnóstico do sistema" no hero,
  reforçando a identidade de suporte técnico em TI.
- Glassmorphism, gradientes, bordas arredondadas e animações suaves em
  toda a interface, com tema claro/escuro e respeito a
  `prefers-reduced-motion`.

## Novidades desta versão
- Dados de contato reais já preenchidos: e-mail, WhatsApp, endereço e
  links de Instagram, Facebook e LinkedIn (editáveis em *Configurações*
  no painel administrativo, na versão Flask).
- **Upload de imagens e vídeos** no painel administrativo (versão Flask):
  portfólio (imagem ou vídeo), capa dos artigos do blog e foto do
  cliente nos depoimentos — tudo salvo de verdade em disco e exibido no site.

## Como personalizar rapidamente
- **Textos e contatos:** troque o número de WhatsApp, e-mail e endereço
  (na versão estática: direto no `index.html`; na versão Flask: em
  *Configurações* no painel administrativo).
- **Serviços, portfólio, depoimentos, blog, downloads:** versão estática
  em `assets/js/main.js`; versão Flask, direto pelo painel administrativo.
- **Cores:** todos os tons ficam centralizados em variáveis CSS no topo
  de `assets/css/style.css` (`:root { --neon, --dark-0, ... }`).
