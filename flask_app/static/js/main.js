/* ==========================================================================
   I&M INFORMÁTICA — main.js (versão Flask)
   O conteúdo (serviços, portfólio, depoimentos, blog, downloads) já vem
   renderizado pelo servidor (Jinja2 + SQLite). Este arquivo cuida apenas
   das interações da interface.
   ========================================================================== */
document.addEventListener('DOMContentLoaded', () => {

  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- NAVBAR SCROLL ---------- */
  const navbar = document.getElementById('navbar');
  const backToTop = document.getElementById('back-to-top');
  window.addEventListener('scroll', () => {
    if (navbar) navbar.classList.toggle('scrolled', window.scrollY > 30);
    if (backToTop) backToTop.classList.toggle('show', window.scrollY > 500);
  });

  /* ---------- MENU MOBILE ---------- */
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  if (navToggle) {
    navToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
    navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => navLinks.classList.remove('open')));
  }

  /* ---------- TEMA CLARO/ESCURO ---------- */
  const themeToggle = document.getElementById('themeToggle');
  if (themeToggle) {
    const applyTheme = (theme) => {
      document.body.setAttribute('data-theme', theme);
      themeToggle.innerHTML = theme === 'dark' ? '<i class="fa-solid fa-moon"></i>' : '<i class="fa-solid fa-sun"></i>';
      try { localStorage.setItem('im_theme', theme); } catch (e) {}
    };
    let saved = 'dark';
    try { saved = localStorage.getItem('im_theme') || 'dark'; } catch (e) {}
    applyTheme(saved);
    themeToggle.addEventListener('click', () => applyTheme(document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'));
  }

  /* ---------- REVEAL ON SCROLL ---------- */
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('in'); io.unobserve(entry.target); } });
  }, { threshold: .15 });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  /* ---------- CONTADORES ---------- */
  const countIO = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = +el.dataset.count;
      let current = 0;
      const step = Math.max(1, Math.ceil(target / 60));
      const tick = () => { current += step; if (current >= target) { el.textContent = target; return; } el.textContent = current; requestAnimationFrame(tick); };
      tick();
      countIO.unobserve(el);
    });
  }, { threshold: .5 });
  document.querySelectorAll('[data-count]').forEach(c => countIO.observe(c));

  /* ---------- PAINEL DE DIAGNÓSTICO ---------- */
  const diagIO = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.querySelectorAll('.diag-fill').forEach(bar => { bar.style.width = bar.dataset.fill + '%'; });
      diagIO.unobserve(entry.target);
    });
  }, { threshold: .3 });
  const panel = document.querySelector('.diagnostic-panel');
  if (panel) diagIO.observe(panel);

  /* ---------- PORTFÓLIO: FILTRO ---------- */
  const filterBtns = document.querySelectorAll('#filterRow .filter-btn');
  const portfolioItems = document.querySelectorAll('#portfolioGrid .portfolio-item');
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const f = btn.dataset.filter;
      portfolioItems.forEach(item => {
        item.style.display = (f === 'all' || item.dataset.cat === f) ? '' : 'none';
      });
    });
  });

  /* ---------- LIGHTBOX (lê data-attributes do item clicado) ---------- */
  const lightbox = document.getElementById('lightbox');
  if (lightbox) {
    portfolioItems.forEach(el => {
      el.addEventListener('click', () => {
        const thumb = document.getElementById('lightboxThumb');
        const mediaType = el.dataset.mediaType;
        const mediaUrl = el.dataset.mediaUrl;
        thumb.innerHTML = '';
        thumb.style.background = el.dataset.color || 'linear-gradient(135deg,#0F1D3A,#2F6BFF)';
        if (mediaType === 'imagem' && mediaUrl) {
          const img = document.createElement('img');
          img.src = mediaUrl; img.alt = el.dataset.title || '';
          thumb.appendChild(img);
        } else if (mediaType === 'video' && mediaUrl) {
          const video = document.createElement('video');
          video.src = mediaUrl; video.controls = true; video.autoplay = true; video.muted = true;
          thumb.appendChild(video);
        } else {
          const span = document.createElement('span');
          span.textContent = (el.dataset.label || '').toUpperCase();
          thumb.appendChild(span);
        }
        document.getElementById('lightboxCat').textContent = el.dataset.label || '';
        document.getElementById('lightboxTitle').textContent = el.dataset.title || '';
        document.getElementById('lightboxDesc').textContent = el.dataset.desc || '';
        lightbox.classList.add('open');
      });
    });
    const closeLightbox = () => {
      lightbox.classList.remove('open');
      const vid = document.querySelector('#lightboxThumb video');
      if (vid) vid.pause();
    };
    const closeBtn = document.getElementById('lightboxClose');
    if (closeBtn) closeBtn.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', (e) => { if (e.target === lightbox) closeLightbox(); });
  }

  /* ---------- CARROSSEL DE DEPOIMENTOS ---------- */
  const testiSlides = document.getElementById('testiSlides');
  const testiDots = document.getElementById('testiDots');
  if (testiSlides && testiDots) {
    const dots = testiDots.querySelectorAll('.testi-dot');
    let testiIndex = 0;
    const total = testiSlides.children.length;
    function goToSlide(i) {
      testiIndex = i;
      testiSlides.style.transform = `translateX(-${i * 100}%)`;
      dots.forEach((d, idx) => d.classList.toggle('active', idx === i));
    }
    dots.forEach(d => d.addEventListener('click', () => goToSlide(+d.dataset.i)));
    if (total > 1) setInterval(() => goToSlide((testiIndex + 1) % total), 5500);
  }

  /* ---------- FORMULÁRIO DE CONTATO ---------- */
  const contactForm = document.getElementById('contactForm');
  const formSuccess = document.getElementById('formSuccess');
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const payload = {
        nome: document.getElementById('nome').value,
        telefone: document.getElementById('telefone').value,
        email: document.getElementById('email').value,
        mensagem: document.getElementById('mensagem').value,
      };
      try {
        const resp = await fetch('/api/contato', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (resp.ok) {
          formSuccess.classList.add('show');
          contactForm.reset();
          setTimeout(() => formSuccess.classList.remove('show'), 6000);
        }
      } catch (err) { console.error('Falha ao enviar mensagem', err); }
    });
  }

  /* ---------- VOLTAR AO TOPO ---------- */
  if (backToTop) backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

});
