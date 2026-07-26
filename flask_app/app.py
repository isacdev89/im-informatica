# -*- coding: utf-8 -*-
"""
I&M Informática — aplicação Flask
Site institucional + área do cliente + painel administrativo, com
banco de dados SQLite (SQLAlchemy) e proteção contra CSRF / XSS / SQL Injection.

Como rodar localmente:
    pip install -r requirements.txt
    python app.py
Acesse http://localhost:5000

Login administrativo padrão (criado automaticamente na primeira execução):
    usuário: admin
    senha:   im@admin123   (TROQUE a senha em produção — ver README.md)
"""
import os
import uuid
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from werkzeug.utils import secure_filename
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)
from flask_wtf import CSRFProtect

from models import (
    db, AdminUser, ClientUser, Service, PortfolioItem, Testimonial,
    BlogPost, DownloadItem, ContactMessage, ServiceRecord, Quote, Setting
)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'iminformatica.db')}"
)
# Estrutura preparada para PostgreSQL: defina DATABASE_URL=postgresql://...
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
# Em produção com HTTPS, habilite também:
# app.config["SESSION_COOKIE_SECURE"] = True

# --- upload de imagens e vídeos (portfólio, blog, depoimentos) ---
app.config["MAX_CONTENT_LENGTH"] = 60 * 1024 * 1024  # limite de 60 MB por upload
UPLOAD_ROOT = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_IMAGE_EXT = {"png", "jpg", "jpeg", "webp", "gif"}
ALLOWED_VIDEO_EXT = {"mp4", "webm", "mov"}

os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)
for sub in ("portfolio", "blog", "depoimentos"):
    os.makedirs(os.path.join(UPLOAD_ROOT, sub), exist_ok=True)


def _ext(filename):
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def save_media(file_storage, subfolder, allow_video=True):
    """Valida e salva um arquivo enviado (imagem ou vídeo).
    Retorna (media_type, filename) ou (None, None) se não houver arquivo válido."""
    if not file_storage or not file_storage.filename:
        return None, None
    ext = _ext(file_storage.filename)
    if ext in ALLOWED_IMAGE_EXT:
        media_type = "imagem"
    elif allow_video and ext in ALLOWED_VIDEO_EXT:
        media_type = "video"
    else:
        return None, None
    filename = f"{uuid.uuid4().hex}.{ext}"
    dest_dir = os.path.join(UPLOAD_ROOT, subfolder)
    os.makedirs(dest_dir, exist_ok=True)
    file_storage.save(os.path.join(dest_dir, secure_filename(filename)))
    return media_type, filename


def delete_media(subfolder, filename):
    if not filename:
        return
    path = os.path.join(UPLOAD_ROOT, subfolder, filename)
    if os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass

db.init_app(app)
csrf = CSRFProtect(app)  # protege todos os formulários POST contra CSRF

login_manager = LoginManager(app)
login_manager.login_view = "admin_login"


@login_manager.user_loader
def load_user(user_id):
    """Suporta dois tipos de sessão: admin:<id> e client:<id>."""
    if user_id.startswith("admin:"):
        return AdminUser.query.get(int(user_id.split(":")[1]))
    if user_id.startswith("client:"):
        return ClientUser.query.get(int(user_id.split(":")[1]))
    return None


def get_settings():
    rows = Setting.query.all()
    data = {s.key: s.value for s in rows}
    data.setdefault("empresa_nome", "I&M Informática")
    data.setdefault("whatsapp", "5592994235355")
    data.setdefault("email_contato", "isacdev.santos@gmail.com")
    data.setdefault("endereco", "Rua Buiuçu, Nº 40 — Bairro Tancredo Neves, CEP 69724-010 — AM")
    data.setdefault("facebook", "https://www.facebook.com/isac.santos.239022")
    data.setdefault("instagram", "https://www.instagram.com/isac.idss/")
    data.setdefault("linkedin", "https://www.linkedin.com/in/isac-da-silva-santos-b223a7189/")
    return data


@app.context_processor
def inject_globals():
    return {"settings": get_settings(), "now": datetime.utcnow()}


# ---------------------------------------------------------------------------
# SITE PÚBLICO
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    services = Service.query.order_by(Service.order).all()
    portfolio = PortfolioItem.query.order_by(PortfolioItem.order).all()
    testimonials = Testimonial.query.order_by(Testimonial.order).all()
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).limit(6).all()
    downloads = DownloadItem.query.all()
    return render_template(
        "index.html", services=services, portfolio=portfolio,
        testimonials=testimonials, posts=posts, downloads=downloads
    )


@app.route("/blog/<int:post_id>")
def blog_detalhe(post_id):
    post = BlogPost.query.get_or_404(post_id)
    outros = (
        BlogPost.query.filter(BlogPost.id != post.id)
        .order_by(BlogPost.created_at.desc())
        .limit(3)
        .all()
    )
    return render_template("blog_post.html", post=post, outros=outros)


@app.route("/api/contato", methods=["POST"])
@csrf.exempt  # chamado via fetch() do front-end; validado por dados obrigatórios abaixo
def api_contato():
    data = request.get_json(silent=True) or request.form
    nome = (data.get("nome") or "").strip()
    mensagem = (data.get("mensagem") or "").strip()
    if not nome or not mensagem:
        return jsonify({"ok": False, "error": "Nome e mensagem são obrigatórios."}), 400
    msg = ContactMessage(
        nome=nome[:120],
        telefone=(data.get("telefone") or "").strip()[:40],
        email=(data.get("email") or "").strip()[:150],
        mensagem=mensagem[:2000],
    )
    db.session.add(msg)
    db.session.commit()
    return jsonify({"ok": True})


# ---------------------------------------------------------------------------
# ÁREA DO CLIENTE
# ---------------------------------------------------------------------------
@app.route("/cliente")
def cliente_home():
    if current_user.is_authenticated and isinstance(current_user, ClientUser):
        return redirect(url_for("cliente_dashboard"))
    return render_template("cliente/login.html")


@app.route("/cliente/cadastro", methods=["POST"])
def cliente_cadastro():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    phone = request.form.get("phone", "").strip()
    password = request.form.get("password", "")
    if not (name and email and password):
        flash("Preencha todos os campos.", "error")
        return redirect(url_for("cliente_home"))
    if ClientUser.query.filter_by(email=email).first():
        flash("Este e-mail já está cadastrado.", "error")
        return redirect(url_for("cliente_home"))
    user = ClientUser(name=name, email=email, phone=phone)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect(url_for("cliente_dashboard"))


@app.route("/cliente/login", methods=["POST"])
def cliente_login():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    user = ClientUser.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        return redirect(url_for("cliente_dashboard"))
    flash("E-mail ou senha inválidos.", "error")
    return redirect(url_for("cliente_home"))


@app.route("/cliente/dashboard")
@login_required
def cliente_dashboard():
    if not isinstance(current_user, ClientUser):
        abort(403)
    records = ServiceRecord.query.filter_by(client_id=current_user.id).order_by(ServiceRecord.date.desc()).all()
    quotes = Quote.query.filter_by(client_id=current_user.id).all()
    downloads = DownloadItem.query.all()
    return render_template("cliente/dashboard.html", records=records, quotes=quotes, downloads=downloads)


@app.route("/cliente/logout")
@login_required
def cliente_logout():
    logout_user()
    return redirect(url_for("cliente_home"))


# ---------------------------------------------------------------------------
# PAINEL ADMINISTRATIVO
# ---------------------------------------------------------------------------
def admin_required():
    if not (current_user.is_authenticated and isinstance(current_user, AdminUser)):
        abort(403)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = AdminUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("admin_dashboard"))
        flash("Usuário ou senha inválidos.", "error")
    return render_template("admin/login.html")


@app.route("/admin/logout")
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for("admin_login"))


@app.route("/admin")
@login_required
def admin_dashboard():
    admin_required()
    counts = {
        "clientes": ClientUser.query.count(),
        "servicos": Service.query.count(),
        "artigos": BlogPost.query.count(),
        "portfolio": PortfolioItem.query.count(),
        "mensagens": ContactMessage.query.filter_by(is_read=False).count(),
        "depoimentos": Testimonial.query.count(),
    }
    return render_template("admin/dashboard.html", counts=counts)


# ---- Clientes -------------------------------------------------------------
@app.route("/admin/clientes")
@login_required
def admin_clientes():
    admin_required()
    items = ClientUser.query.order_by(ClientUser.created_at.desc()).all()
    return render_template("admin/clientes.html", items=items)


@app.route("/admin/clientes/<int:item_id>/excluir", methods=["POST"])
@login_required
def admin_clientes_excluir(item_id):
    admin_required()
    obj = ClientUser.query.get_or_404(item_id)
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for("admin_clientes"))


# ---- Serviços ---------------------------------------------------------------
@app.route("/admin/servicos", methods=["GET", "POST"])
@login_required
def admin_servicos():
    admin_required()
    if request.method == "POST":
        db.session.add(Service(
            icon=request.form.get("icon", "fa-screwdriver-wrench").strip(),
            title=request.form.get("title", "").strip(),
            description=request.form.get("description", "").strip(),
            order=Service.query.count(),
        ))
        db.session.commit()
        return redirect(url_for("admin_servicos"))
    items = Service.query.order_by(Service.order).all()
    return render_template("admin/servicos.html", items=items)


@app.route("/admin/servicos/<int:item_id>/excluir", methods=["POST"])
@login_required
def admin_servicos_excluir(item_id):
    admin_required()
    db.session.delete(Service.query.get_or_404(item_id))
    db.session.commit()
    return redirect(url_for("admin_servicos"))


# ---- Artigos (Blog) ---------------------------------------------------------
@app.route("/admin/artigos", methods=["GET", "POST"])
@login_required
def admin_artigos():
    admin_required()
    if request.method == "POST":
        _, cover_file = save_media(request.files.get("cover"), "blog", allow_video=False)
        db.session.add(BlogPost(
            category=request.form.get("category", "").strip(),
            title=request.form.get("title", "").strip(),
            description=request.form.get("description", "").strip(),
            content=request.form.get("content", "").strip(),
            cover_image=cover_file,
        ))
        db.session.commit()
        return redirect(url_for("admin_artigos"))
    items = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template("admin/artigos.html", items=items)


@app.route("/admin/artigos/<int:item_id>/excluir", methods=["POST"])
@login_required
def admin_artigos_excluir(item_id):
    admin_required()
    obj = BlogPost.query.get_or_404(item_id)
    delete_media("blog", obj.cover_image)
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for("admin_artigos"))


# ---- Portfólio / Galeria -----------------------------------------------------
@app.route("/admin/portfolio", methods=["GET", "POST"])
@login_required
def admin_portfolio():
    admin_required()
    if request.method == "POST":
        media_type, media_file = save_media(request.files.get("media"), "portfolio", allow_video=True)
        db.session.add(PortfolioItem(
            category=request.form.get("category", "computadores").strip(),
            label=request.form.get("label", "").strip(),
            title=request.form.get("title", "").strip(),
            description=request.form.get("description", "").strip(),
            media_type=media_type or "cor",
            media_file=media_file,
            order=PortfolioItem.query.count(),
        ))
        db.session.commit()
        return redirect(url_for("admin_portfolio"))
    items = PortfolioItem.query.order_by(PortfolioItem.order).all()
    return render_template("admin/portfolio.html", items=items)


@app.route("/admin/portfolio/<int:item_id>/excluir", methods=["POST"])
@login_required
def admin_portfolio_excluir(item_id):
    admin_required()
    obj = PortfolioItem.query.get_or_404(item_id)
    delete_media("portfolio", obj.media_file)
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for("admin_portfolio"))


# ---- Usuários administradores -------------------------------------------------
@app.route("/admin/usuarios", methods=["GET", "POST"])
@login_required
def admin_usuarios():
    admin_required()
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username and password and not AdminUser.query.filter_by(username=username).first():
            user = AdminUser(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
        return redirect(url_for("admin_usuarios"))
    items = AdminUser.query.all()
    return render_template("admin/usuarios.html", items=items)


# ---- Mensagens -----------------------------------------------------------
@app.route("/admin/mensagens")
@login_required
def admin_mensagens():
    admin_required()
    items = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin/mensagens.html", items=items)


@app.route("/admin/mensagens/<int:item_id>/lida", methods=["POST"])
@login_required
def admin_mensagens_lida(item_id):
    admin_required()
    msg = ContactMessage.query.get_or_404(item_id)
    msg.is_read = True
    db.session.commit()
    return redirect(url_for("admin_mensagens"))


@app.route("/admin/mensagens/<int:item_id>/excluir", methods=["POST"])
@login_required
def admin_mensagens_excluir(item_id):
    admin_required()
    db.session.delete(ContactMessage.query.get_or_404(item_id))
    db.session.commit()
    return redirect(url_for("admin_mensagens"))


# ---- Depoimentos -----------------------------------------------------------
@app.route("/admin/depoimentos", methods=["GET", "POST"])
@login_required
def admin_depoimentos():
    admin_required()
    if request.method == "POST":
        _, photo_file = save_media(request.files.get("photo"), "depoimentos", allow_video=False)
        db.session.add(Testimonial(
            name=request.form.get("name", "").strip(),
            role=request.form.get("role", "").strip(),
            text=request.form.get("text", "").strip(),
            stars=int(request.form.get("stars", 5) or 5),
            photo=photo_file,
            order=Testimonial.query.count(),
        ))
        db.session.commit()
        return redirect(url_for("admin_depoimentos"))
    items = Testimonial.query.order_by(Testimonial.order).all()
    return render_template("admin/depoimentos.html", items=items)


@app.route("/admin/depoimentos/<int:item_id>/excluir", methods=["POST"])
@login_required
def admin_depoimentos_excluir(item_id):
    admin_required()
    obj = Testimonial.query.get_or_404(item_id)
    delete_media("depoimentos", obj.photo)
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for("admin_depoimentos"))


# ---- Configurações -----------------------------------------------------------
@app.route("/admin/configuracoes", methods=["GET", "POST"])
@login_required
def admin_configuracoes():
    admin_required()
    if request.method == "POST":
        for key in ("empresa_nome", "whatsapp", "email_contato", "endereco", "facebook", "instagram", "linkedin"):
            value = request.form.get(key, "").strip()
            setting = Setting.query.get(key)
            if setting:
                setting.value = value
            else:
                db.session.add(Setting(key=key, value=value))
        db.session.commit()
        flash("Configurações salvas com sucesso.", "success")
        return redirect(url_for("admin_configuracoes"))
    return render_template("admin/configuracoes.html", settings=get_settings())


# ---- Backup automático -----------------------------------------------------------
@app.route("/admin/backup", methods=["GET", "POST"])
@login_required
def admin_backup():
    admin_required()
    import shutil
    db_path = os.path.join(BASE_DIR, "instance", "iminformatica.db")
    backup_dir = os.path.join(BASE_DIR, "instance", "backups")
    os.makedirs(backup_dir, exist_ok=True)
    last_backup = None
    if request.method == "POST" and os.path.exists(db_path):
        stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        dest = os.path.join(backup_dir, f"iminformatica_{stamp}.db")
        shutil.copy2(db_path, dest)
        flash(f"Backup criado: {os.path.basename(dest)}", "success")
    backups = sorted(os.listdir(backup_dir), reverse=True) if os.path.isdir(backup_dir) else []
    return render_template("admin/backup.html", backups=backups)


# ---------------------------------------------------------------------------
# SEED — dados iniciais (executa apenas se as tabelas estiverem vazias)
# ---------------------------------------------------------------------------
def seed_data():
    if AdminUser.query.count() == 0:
        admin = AdminUser(username="admin")
        admin.set_password(os.environ.get("ADMIN_DEFAULT_PASSWORD", "im@admin123"))
        db.session.add(admin)

    if Service.query.count() == 0:
        services = [
            ("fa-broom", "Formatação", "Formatação completa com backup prévio dos seus arquivos."),
            ("fa-window-restore", "Instalação do Windows", "Instalação e ativação de qualquer versão do Windows."),
            ("fa-microchip", "Upgrade de SSD", "Troca de HD por SSD para ganho real de velocidade."),
            ("fa-wind", "Limpeza preventiva", "Limpeza física interna para evitar superaquecimento."),
            ("fa-desktop", "Montagem de computadores", "Montagem sob medida conforme seu uso e orçamento."),
            ("fa-laptop", "Manutenção de notebooks", "Diagnóstico e reparo de hardware e software."),
            ("fa-network-wired", "Configuração de redes", "Redes cabeadas e Wi-Fi estáveis para casa e empresa."),
            ("fa-database", "Backup", "Rotinas de backup automático local e em nuvem."),
            ("fa-file-shield", "Recuperação de arquivos", "Recuperação de dados apagados ou corrompidos."),
            ("fa-virus-slash", "Remoção de vírus", "Remoção de vírus, malwares e programas indesejados."),
            ("fa-download", "Instalação de programas", "Instalação e configuração dos programas que você usa."),
            ("fa-headset", "Atendimento remoto", "Suporte à distância, rápido e sem sair de casa."),
            ("fa-lightbulb", "Consultoria em TI", "Orientação técnica para decisões de tecnologia."),
            ("fa-code", "Desenvolvimento de sistemas", "Sistemas web sob medida para o seu negócio."),
            ("fa-globe", "Desenvolvimento de sites", "Sites profissionais, rápidos e otimizados para SEO."),
            ("fa-file-lines", "Currículos profissionais", "Currículos modernos que ajudam você a se destacar."),
        ]
        for i, (icon, title, desc) in enumerate(services):
            db.session.add(Service(icon=icon, title=title, description=desc, order=i))

    if PortfolioItem.query.count() == 0:
        colors = [
            "linear-gradient(135deg,#0F1D3A,#2F6BFF)", "linear-gradient(135deg,#0A1128,#00E5FF)",
            "linear-gradient(135deg,#16274A,#2F6BFF)", "linear-gradient(135deg,#05070D,#0F1D3A)",
        ]
        portfolio = [
            ("sistemas", "Sistemas", "Sistema de Inventário de TI (INVENTARIO-T.I.)",
             "Sistema completo em Django para controle de equipamentos de informática de unidades de saúde, com cadastro, histórico e relatórios."),
            ("sistemas", "Sistemas", "Sistema de Gestão para Loja Virtual",
             "Sistema local com PDV, controle de estoque, cadastro de clientes, controle de fiado e relatórios de vendas."),
            ("sistemas", "Sistemas", "Assistente Virtual Inteligente",
             "Assistente pessoal em Python com automação de tarefas, streaming de tela e respostas por voz em português."),
            ("computadores", "Computadores", "Manutenção e Suporte de Equipamentos de TI",
             "Manutenção preventiva e corretiva de computadores em unidades de saúde municipais, com diagnóstico de hardware e software."),
            ("redes", "Redes", "Suporte de Rede em Unidades de Saúde",
             "Configuração e suporte de rede para funcionamento estável de sistemas de saúde nas unidades municipais."),
            ("sistemas", "Treinamento", "Tutoriais e Treinamento para o Sistema e-SUS PEC",
             "Elaboração de tutoriais em PDF e vídeo para Agentes Comunitários de Saúde sobre o uso do e-SUS PEC."),
        ]
        for i, (cat, label, title, desc) in enumerate(portfolio):
            db.session.add(PortfolioItem(category=cat, label=label, title=title, description=desc,
                                          color=colors[i % len(colors)], order=i))

    if Testimonial.query.count() == 0:
        testimonials = [
            ("Carla Mendes", "Cliente residencial", "Meu computador voltou a funcionar como novo. Atendimento rápido."),
            ("Roberto Silva", "Comerciante local", "O sistema da minha loja ficou exatamente como eu precisava."),
            ("Juliana Costa", "Cliente corporativo", "A rede da empresa nunca mais caiu depois da configuração."),
        ]
        for i, (name, role, text) in enumerate(testimonials):
            db.session.add(Testimonial(name=name, role=role, text=text, stars=5, order=i))

    if BlogPost.query.count() == 0:
        posts = [
            ("Dicas", "Como organizar o inventário de equipamentos da sua empresa",
             "Por que um controle de patrimônio de TI evita prejuízo e retrabalho.",
             "Um inventário de TI bem feito é a diferença entre saber exatamente onde está cada "
             "computador, monitor e periférico — e perder tempo procurando ou comprando algo que já "
             "existe em outro setor. Manter um cadastro atualizado, com número de série, localização "
             "e responsável, facilita manutenções, troca de equipamentos com defeito e planejamento "
             "de compras futuras. Pequenas empresas e órgãos públicos que adotam esse controle "
             "reduzem custos e evitam extravio de material."),
            ("Segurança", "Backup: o cuidado que evita a perda total dos seus dados",
             "Boas práticas simples de backup para pequenas empresas e órgãos públicos.",
             "Perder arquivos importantes por falha de disco, vírus ou erro humano é mais comum do "
             "que parece — e na maioria das vezes é evitável. A regra mais simples de seguir é a "
             "\"3-2-1\": três cópias dos dados, em dois tipos de mídia diferentes, sendo uma delas "
             "fora do local principal (nuvem ou HD externo). Automatizar esse processo, mesmo que de "
             "forma básica, evita depender da memória de alguém para lembrar de fazer backup "
             "manualmente."),
            ("Sistemas", "Sistemas sob medida: quando vale a pena automatizar processos",
             "Como um sistema simples pode economizar horas de trabalho manual.",
             "Muita empresa ainda controla estoque, vendas ou atendimentos em planilhas ou até no "
             "papel. Um sistema sob medida, mesmo simples, elimina retrabalho, reduz erros de "
             "digitação e centraliza as informações em um só lugar. O investimento inicial costuma "
             "se pagar rápido quando se leva em conta o tempo economizado no dia a dia da equipe."),
            ("Dicas", "5 sinais de que é hora de atualizar seu computador ou notebook",
             "Sinais de lentidão que indicam necessidade de upgrade ou manutenção.",
             "Ventilador funcionando o tempo todo em alta rotação, programas travando ao abrir, "
             "tempo de inicialização cada vez mais longo, pouco espaço livre no disco e "
             "travamentos frequentes são sinais de que o equipamento precisa de atenção. Em "
             "muitos casos, uma limpeza física, upgrade de memória ou troca do disco por um SSD "
             "resolve o problema sem precisar comprar um equipamento novo."),
        ]
        for cat, title, desc, content in posts:
            db.session.add(BlogPost(category=cat, title=title, description=desc, content=content))

    if DownloadItem.query.count() == 0:
        downloads = [
            ("fa-print", "Drivers de Impressora (pacote geral)", "42 MB"),
            ("fa-shield-halved", "Antivírus recomendado (gratuito)", "180 MB"),
            ("fa-file-zipper", "Utilitário de compactação", "6 MB"),
            ("fa-book", "Manual: primeiros socorros de TI", "PDF · 2 MB"),
        ]
        for icon, name, size in downloads:
            db.session.add(DownloadItem(icon=icon, name=name, size=size))

    db.session.commit()


with app.app_context():
    db.create_all()
    seed_data()


# ---------------------------------------------------------------------------
# Cabeçalhos básicos de segurança (mitigação de XSS / clickjacking)
# ---------------------------------------------------------------------------
@app.errorhandler(413)
def file_too_large(e):
    flash("Arquivo muito grande. O limite é de 60 MB por envio.", "error")
    return redirect(request.referrer or url_for("admin_dashboard"))


@app.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG", "0") == "1")
