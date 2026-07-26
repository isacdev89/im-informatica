# I&M Informática — Versão Flask (backend completo)

Site institucional com **área do cliente**, **painel administrativo** e
**banco de dados SQLite**, pronta para publicação gratuita em **Render**,
**Railway** ou **PythonAnywhere**.

## Tecnologias
- Python 3 + Flask
- Flask-SQLAlchemy (SQLite — estrutura pronta para migrar para PostgreSQL)
- Flask-Login (autenticação de administrador e de cliente)
- Flask-WTF (proteção CSRF em todos os formulários)
- Bootstrap 5 + Font Awesome + CSS/JS próprios (mesmo visual da versão estática)

## Como rodar localmente

```bash
cd flask_app
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Acesse **http://localhost:5000**

Na primeira execução o banco de dados é criado automaticamente em
`instance/iminformatica.db`, já populado com serviços, portfólio,
depoimentos, artigos e downloads de exemplo.

### Login administrativo padrão
```
URL:     /admin/login
Usuário: admin
Senha:   im@admin123
```
**Troque essa senha assim que possível**, criando um novo usuário em
"Usuários" no painel e removendo o padrão, ou definindo a variável de
ambiente `ADMIN_DEFAULT_PASSWORD` antes de rodar pela primeira vez.

### Área do Cliente
Os próprios clientes se cadastram em `/cliente`. Cada conta tem senha
protegida com hash (`werkzeug.security`) e visualiza histórico de
serviços, orçamentos e downloads liberados (dados de exemplo podem ser
inseridos diretamente no banco ou por uma futura tela administrativa
de vínculo cliente↔serviço).

## Upload de imagens e vídeos
No painel administrativo é possível enviar arquivos reais (guardados em
`static/uploads/...`) em três lugares:
- **Portfólio / Galeria** → imagem ou vídeo (`png, jpg, webp, gif, mp4, webm, mov`), exibido na home e no lightbox.
- **Artigos (Blog)** → imagem de capa (`png, jpg, webp, gif`).
- **Depoimentos** → foto do cliente (`png, jpg, webp, gif`).

Limite de 60 MB por arquivo (ajustável em `MAX_CONTENT_LENGTH` no `app.py`).
Ao excluir um item, o arquivo correspondente também é apagado do disco.

## Estrutura de pastas
```
flask_app/
├── app.py                 # rotas, autenticação, seed inicial
├── models.py               # modelos SQLAlchemy (SQLite)
├── requirements.txt
├── static/
│   ├── css/style.css        # design system (mesmo da versão estática)
│   └── js/main.js           # interações (tema, menu, filtros, carrossel...)
├── templates/
│   ├── base.html
│   ├── index.html            # home dinâmica (dados vêm do banco)
│   ├── cliente/               # login/cadastro e painel do cliente
│   └── admin/                  # painel administrativo (CRUD completo)
└── instance/
    └── iminformatica.db        # criado automaticamente (não versionar)
```

## Segurança implementada
- **CSRF**: todos os formulários POST usam token via Flask-WTF.
- **XSS**: Jinja2 escapa automaticamente todo conteúdo exibido nos templates.
- **SQL Injection**: todo acesso a dados passa pelo ORM (SQLAlchemy),
  nunca por SQL concatenado manualmente.
- **Senhas**: nunca armazenadas em texto puro — sempre com hash
  (`werkzeug.security.generate_password_hash`).
- Cabeçalhos básicos (`X-Content-Type-Options`, `X-Frame-Options`,
  `Referrer-Policy`) aplicados a toda resposta.

Antes de publicar em produção:
1. Defina uma `SECRET_KEY` forte e aleatória via variável de ambiente.
2. Habilite `SESSION_COOKIE_SECURE = True` (exige HTTPS).
3. Troque a senha padrão do usuário `admin`.

## Publicando gratuitamente

**Veja o guia completo (com automação) em `../COMO_PUBLICAR_GRATIS.md`.**
Resumo rápido:

### Render (recomendado — sem cartão de crédito)
Este pacote já inclui `render.yaml`, `Procfile` e `runtime.txt`. No
Render, use **New + → Blueprint**, aponte para o repositório e ele
configura tudo sozinho a partir do `render.yaml`. Publicações futuras
acontecem automaticamente a cada `git push`.

⚠️ **Atenção:** no plano gratuito do Render, o disco não é permanente —
o banco SQLite e as imagens/vídeos enviados voltam ao estado inicial a
cada reinício/nova publicação. Use a tela **Backup automático** do
painel para baixar cópias do banco quando quiser guardar dados reais.

### Railway
1. Suba esta pasta (`flask_app`) para um repositório no GitHub.
2. Crie um novo projeto apontando para o repositório (o `Procfile` já
   configura o comando de início automaticamente).

### PythonAnywhere
1. Faça upload da pasta `flask_app`.
2. Crie uma nova Web App (Flask), apontando o WSGI para `app.app`.
3. Rode `pip install -r requirements.txt` no console Bash do PythonAnywhere.

## Evoluções futuras sugeridas
- Migrar o banco para PostgreSQL (basta trocar `DATABASE_URL`).
- Tela administrativa para vincular serviços/orçamentos a um cliente específico.
- Upload real de imagens no portfólio e nos artigos do blog.
- Internacionalização (estrutura de textos já isolada nos templates).
