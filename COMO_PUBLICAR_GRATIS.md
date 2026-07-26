# Como publicar o site de graça (automático)

Este pacote já vem pronto para publicar sozinho, sem custo. Depois da
configuração inicial (feita **uma única vez**), qualquer atualização que
você enviar ao GitHub publica automaticamente.

Existem dois destinos, dependendo da versão que você quer publicar:

| Versão            | Onde publicar        | Custo | Fica sempre no ar? |
|-------------------|-----------------------|-------|---------------------|
| `static/`         | GitHub Pages          | Grátis | Sim, sempre         |
| `flask_app/`      | Render (free tier)    | Grátis | Dorme após 15 min sem acesso (acorda em ~30-60s no próximo acesso) |

Recomendação: publique a versão **estática** no GitHub Pages como o site
"oficial" da empresa (rápido, sempre no ar, sem custo nenhum), e use a
versão **Flask** no Render para demonstrar/testar a área do cliente e o
painel administrativo com banco de dados de verdade.

---

## Passo 0 — Uma única vez: preparar o GitHub

1. Crie uma conta gratuita em **https://github.com/join** (se ainda não tiver).
2. Instale o Git: **https://git-scm.com/downloads** (Windows: baixe e
   instale normalmente, próximo, próximo, concluir).
3. No GitHub, clique em **New repository** (botão verde), dê um nome
   (ex.: `im-informatica`), deixe como **Public**, NÃO marque nenhuma
   opção extra (sem README, sem .gitignore) e clique **Create repository**.
4. Copie o link do repositório que aparece na tela seguinte
   (algo como `https://github.com/seuusuario/im-informatica.git`).

## Passo 1 — Enviar o código (automático via .bat)

Dê dois cliques em **`publicar_no_github.bat`** (na pasta raiz deste
pacote). Ele vai pedir o link do repositório (copiado no passo acima) e
faz sozinho: `git init`, `git add`, `git commit` e `git push`. Na
primeira vez, o Windows pode abrir uma janela pedindo para você fazer
login no GitHub — faça o login normalmente.

> Sempre que você editar algo (textos, imagens, serviços) e quiser
> atualizar o site publicado, basta rodar este `.bat` de novo.

## Passo 2 — Site estático no GitHub Pages (automático depois de 1 clique)

1. No GitHub, abra o repositório → **Settings** → **Pages** (menu à esquerda).
2. Em **Source**, selecione **GitHub Actions**. É só isso — um clique.
3. Pronto. Este pacote já inclui o arquivo
   `.github/workflows/deploy-static.yml`, que publica automaticamente a
   pasta `static/` toda vez que você enviar código (passo 1). Em 1–2
   minutos o site estará em:
   `https://seuusuario.github.io/im-informatica/`
4. Da próxima vez, você só roda `publicar_no_github.bat` — a
   publicação acontece sozinha, sem repetir nenhum passo manual.

## Passo 3 — Versão completa (Flask) no Render (gratuito, sem cartão)

1. Crie uma conta gratuita em **https://render.com** (pode entrar direto
   com sua conta do GitHub — não pede cartão de crédito no plano free).
2. Clique em **New +** → **Blueprint**.
3. Escolha o repositório que você criou (`im-informatica`).
4. O Render encontra sozinho o arquivo `render.yaml` deste pacote e já
   preenche tudo: nome do serviço, comando de instalação, comando de
   início e o plano **Free**. Você só confirma clicando em **Apply** /
   **Create**.
5. Em 2–3 minutos o site estará no ar em um endereço assim:
   `https://im-informatica.onrender.com`
6. (Opcional, recomendado) Antes de clicar em criar, defina a variável
   `ADMIN_DEFAULT_PASSWORD` com uma senha sua — assim o usuário `admin`
   já nasce com a senha que você escolher, em vez da senha padrão do
   pacote.

### Atualizações automáticas
Depois de conectado, toda vez que você rodar `publicar_no_github.bat`
novamente, o Render detecta o novo código e republica sozinho — sem
nenhum passo manual adicional.

### Limitações do plano gratuito do Render (importante)
- O serviço **"dorme"** depois de 15 minutos sem visitas, e leva de 30
  a 60 segundos para "acordar" no próximo acesso. Normal e esperado no
  plano gratuito.
- O **disco não é permanente**: toda vez que o serviço reinicia ou você
  publica uma atualização, o banco de dados SQLite e as imagens/vídeos
  enviados pelo painel voltam ao estado original (dados de exemplo).
  Para um site de divulgação isso não é problema. Se no futuro você
  quiser guardar clientes e mensagens reais de forma permanente, será
  necessário um plano pago com disco persistente (a partir de poucos
  dólares/mês) — quando chegar essa hora, me avise que ajusto o projeto.
- Use a tela **Backup automático** do painel administrativo para baixar
  cópias do banco de dados sempre que quiser guardar os dados coletados.

---

## Alternativa sem GitHub: PythonAnywhere (também gratuito)
Se preferir não usar Git/GitHub para a versão Flask, o PythonAnywhere
permite subir a pasta `flask_app` direto pelo navegador (aba *Files*) e
rodar sem cartão de crédito. Veja o passo a passo em
`flask_app/README.md`.
