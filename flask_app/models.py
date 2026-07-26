# -*- coding: utf-8 -*-
"""
Modelos de banco de dados — I&M Informática
Banco: SQLite (via SQLAlchemy). Estrutura preparada para migrar para
PostgreSQL futuramente: basta trocar SQLALCHEMY_DATABASE_URI em app.py,
os modelos abaixo não usam nenhum recurso exclusivo do SQLite.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class AdminUser(UserMixin, db.Model):
    """Usuário do painel administrativo."""
    __tablename__ = "admin_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        # prefixo para diferenciar de ClientUser no Flask-Login
        return f"admin:{self.id}"


class ClientUser(UserMixin, db.Model):
    """Usuário da área do cliente."""
    __tablename__ = "client_users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(30))
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)
    is_active_account = db.Column(db.Boolean, default=True)   # controle de acesso (bloquear/liberar)
    confirmation_email_sent = db.Column(db.Boolean, default=False)

    services = db.relationship("ServiceRecord", backref="client", lazy=True, cascade="all, delete-orphan")
    quotes = db.relationship("Quote", backref="client", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return f"client:{self.id}"


class Service(db.Model):
    """Serviço oferecido (cartão da seção Serviços)."""
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.String(50), default="fa-screwdriver-wrench")
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255))
    order = db.Column(db.Integer, default=0)


class PortfolioItem(db.Model):
    """Item da galeria de portfólio. Pode exibir uma imagem/vídeo enviado
    pelo painel administrativo, ou (na ausência de mídia) um fundo em
    gradiente com o rótulo da categoria."""
    __tablename__ = "portfolio_items"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(40), nullable=False)   # computadores | notebooks | sistemas | sites | redes
    label = db.Column(db.String(60), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(255))
    color = db.Column(db.String(120), default="linear-gradient(135deg,#0F1D3A,#2F6BFF)")
    media_type = db.Column(db.String(10), default="cor")   # "cor" | "imagem" | "video"
    media_file = db.Column(db.String(255))                  # nome do arquivo em static/uploads/portfolio
    order = db.Column(db.Integer, default=0)


class Testimonial(db.Model):
    """Depoimento de cliente."""
    __tablename__ = "testimonials"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120))
    text = db.Column(db.Text, nullable=False)
    stars = db.Column(db.Integer, default=5)
    photo = db.Column(db.String(255))  # nome do arquivo em static/uploads/depoimentos
    order = db.Column(db.Integer, default=0)


class BlogPost(db.Model):
    """Artigo do blog."""
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(60), nullable=False)
    title = db.Column(db.String(180), nullable=False)
    description = db.Column(db.String(280))
    content = db.Column(db.Text)
    cover_image = db.Column(db.String(255))  # nome do arquivo em static/uploads/blog
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DownloadItem(db.Model):
    """Arquivo disponível na área de downloads."""
    __tablename__ = "download_items"
    id = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.String(50), default="fa-download")
    name = db.Column(db.String(180), nullable=False)
    size = db.Column(db.String(40))
    url = db.Column(db.String(255), default="#")


class ContactMessage(db.Model):
    """Mensagem recebida pelo formulário de contato."""
    __tablename__ = "contact_messages"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(40))
    email = db.Column(db.String(150))
    mensagem = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ServiceRecord(db.Model):
    """Histórico de serviços de um cliente (Área do Cliente)."""
    __tablename__ = "service_records"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client_users.id"), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(30), default="Concluído")  # Concluído | Em andamento
    date = db.Column(db.DateTime, default=datetime.utcnow)


class Quote(db.Model):
    """Orçamento vinculado a um cliente."""
    __tablename__ = "quotes"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client_users.id"), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(40), default="Aguardando aprovação")
    valid_until = db.Column(db.DateTime)


class Ebook(db.Model):
    """Livro ou apostila digital à venda (catálogo — venda via WhatsApp,
    sem checkout automático)."""
    __tablename__ = "ebooks"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(40), default="Apostila")   # Livro | Apostila
    title = db.Column(db.String(180), nullable=False)
    description = db.Column(db.String(280))
    price = db.Column(db.String(30), default="A combinar")
    cover_image = db.Column(db.String(255))   # nome do arquivo em static/uploads/ebooks
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SoftwareCatalogItem(db.Model):
    """Item do catálogo de ISOs e programas — aponta para a página oficial
    do fabricante, o site não hospeda os instaladores."""
    __tablename__ = "software_catalog_items"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(40), default="Programa")   # Sistema Operacional | Programa | Driver
    icon = db.Column(db.String(50), default="fa-download")
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(255))
    official_url = db.Column(db.String(400), nullable=False)
    order = db.Column(db.Integer, default=0)


class Setting(db.Model):
    """Configurações gerais do site (chave/valor)."""
    __tablename__ = "settings"
    key = db.Column(db.String(60), primary_key=True)
    value = db.Column(db.String(255))
