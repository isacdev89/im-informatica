/* ==========================================================================
   I&M INFORMÁTICA — main.js
   ========================================================================== */
document.addEventListener('DOMContentLoaded', () => {

  /* ---------- ANO NO RODAPÉ ---------- */
  document.getElementById('year').textContent = new Date().getFullYear();

  /* ---------- NAVBAR SCROLL ---------- */
  const navbar = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 30);
    backToTop.classList.toggle('show', window.scrollY > 500);
  });

  /* ---------- MENU MOBILE ---------- */
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  navToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
  navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => navLinks.classList.remove('open')));

  /* ---------- TEMA CLARO/ESCURO ---------- */
  const themeToggle = document.getElementById('themeToggle');
  const root = document.body;
  const applyTheme = (theme) => {
    root.setAttribute('data-theme', theme);
    themeToggle.innerHTML = theme === 'dark' ? '<i class="fa-solid fa-moon"></i>' : '<i class="fa-solid fa-sun"></i>';
    try { localStorage.setItem('im_theme', theme); } catch (e) {}
  };
  let savedTheme = 'dark';
  try { savedTheme = localStorage.getItem('im_theme') || 'dark'; } catch (e) {}
  applyTheme(savedTheme);
  themeToggle.addEventListener('click', () => {
    applyTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
  });

  /* ---------- REVEAL ON SCROLL ---------- */
  const revealEls = document.querySelectorAll('.reveal');
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('in'); io.unobserve(entry.target); } });
  }, { threshold: .15 });
  revealEls.forEach(el => io.observe(el));

  /* ---------- CONTADORES DO HERO ---------- */
  const counters = document.querySelectorAll('[data-count]');
  const countIO = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = +el.dataset.count;
      let current = 0;
      const step = Math.max(1, Math.ceil(target / 60));
      const tick = () => {
        current += step;
        if (current >= target) { el.textContent = target; return; }
        el.textContent = current;
        requestAnimationFrame(tick);
      };
      tick();
      countIO.unobserve(el);
    });
  }, { threshold: .5 });
  counters.forEach(c => countIO.observe(c));

  /* ---------- BARRAS DO PAINEL DE DIAGNÓSTICO ---------- */
  const diagIO = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.querySelectorAll('.diag-fill').forEach(bar => { bar.style.width = bar.dataset.fill + '%'; });
      diagIO.unobserve(entry.target);
    });
  }, { threshold: .3 });
  const panel = document.querySelector('.diagnostic-panel');
  if (panel) diagIO.observe(panel);

  /* ==========================================================================
     DADOS
     ========================================================================== */
  const SERVICES = [
    { icon:'fa-broom', title:'Formatação', desc:'Formatação completa com backup prévio dos seus arquivos.' },
    { icon:'fa-window-restore', title:'Instalação do Windows', desc:'Instalação e ativação de qualquer versão do Windows.' },
    { icon:'fa-microchip', title:'Upgrade de SSD', desc:'Troca de HD por SSD para ganho real de velocidade.' },
    { icon:'fa-wind', title:'Limpeza preventiva', desc:'Limpeza física interna para evitar superaquecimento.' },
    { icon:'fa-desktop', title:'Montagem de computadores', desc:'Montagem sob medida conforme seu uso e orçamento.' },
    { icon:'fa-laptop', title:'Manutenção de notebooks', desc:'Diagnóstico e reparo de hardware e software.' },
    { icon:'fa-network-wired', title:'Configuração de redes', desc:'Redes cabeadas e Wi-Fi estáveis para casa e empresa.' },
    { icon:'fa-database', title:'Backup', desc:'Rotinas de backup automático local e em nuvem.' },
    { icon:'fa-file-shield', title:'Recuperação de arquivos', desc:'Recuperação de dados apagados ou corrompidos.' },
    { icon:'fa-virus-slash', title:'Remoção de vírus', desc:'Remoção de vírus, malwares e programas indesejados.' },
    { icon:'fa-download', title:'Instalação de programas', desc:'Instalação e configuração dos programas que você usa.' },
    { icon:'fa-headset', title:'Atendimento remoto', desc:'Suporte à distância, rápido e sem sair de casa.' },
    { icon:'fa-lightbulb', title:'Consultoria em TI', desc:'Orientação técnica para decisões de tecnologia.' },
    { icon:'fa-code', title:'Desenvolvimento de sistemas', desc:'Sistemas web sob medida para o seu negócio.' },
    { icon:'fa-globe', title:'Desenvolvimento de sites', desc:'Sites profissionais, rápidos e otimizados para SEO.' },
    { icon:'fa-file-lines', title:'Currículos profissionais', desc:'Currículos modernos que ajudam você a se destacar.' },
  ];

  const PORTFOLIO = [
    { cat:'computadores', label:'Computadores', title:'Montagem Gamer Ryzen 5', desc:'Montagem completa com refrigeração otimizada e cabeamento organizado.' },
    { cat:'notebooks', label:'Notebooks', title:'Recuperação de Notebook Dell', desc:'Troca de tela, upgrade de SSD e limpeza interna completa.' },
    { cat:'sistemas', label:'Sistemas', title:'Sistema de Gestão de Estoque', desc:'Painel web para controle de produtos, clientes e financeiro.' },
    { cat:'sites', label:'Sites', title:'Site Institucional', desc:'Site responsivo com SEO completo para pequena empresa local.' },
    { cat:'redes', label:'Redes', title:'Rede Corporativa Wi-Fi', desc:'Cobertura total de rede com múltiplos pontos de acesso.' },
    { cat:'computadores', label:'Computadores', title:'Upgrade de Escritório', desc:'Substituição de HDs por SSDs em 12 computadores.' },
    { cat:'sistemas', label:'Sistemas', title:'Sistema de Atendimento Automatizado', desc:'Respostas automáticas via WhatsApp para suporte técnico.' },
    { cat:'sites', label:'Sites', title:'Loja Virtual', desc:'E-commerce simples com catálogo e contato direto via WhatsApp.' },
    { cat:'notebooks', label:'Notebooks', title:'Manutenção Preventiva em Lote', desc:'Limpeza e troca de pasta térmica em notebooks corporativos.' },
    { cat:'redes', label:'Redes', title:'Cabeamento Estruturado', desc:'Organização e certificação de rede cabeada em escritório.' },
  ];

  const DIFERENCIAIS = [
    { icon:'fa-bolt', title:'Atendimento rápido' },
    { icon:'fa-shield-halved', title:'Garantia' },
    { icon:'fa-hand-holding-dollar', title:'Orçamento gratuito' },
    { icon:'fa-house-laptop', title:'Atendimento remoto' },
    { icon:'fa-people-arrows', title:'Atendimento presencial' },
    { icon:'fa-user-gear', title:'Suporte especializado' },
    { icon:'fa-lock', title:'Segurança dos dados' },
  ];

  const TESTIMONIALS = [
    { name:'Carla Mendes', role:'Cliente residencial', text:'Meu computador voltou a funcionar como novo. Atendimento rápido e explicaram tudo com paciência.' },
    { name:'Roberto Silva', role:'Comerciante local', text:'Contratei o desenvolvimento do sistema da minha loja e ficou exatamente como eu precisava.' },
    { name:'Juliana Costa', role:'Cliente corporativo', text:'A rede da empresa nunca mais caiu depois da configuração feita pela equipe da I&M.' },
    { name:'Marcos Almeida', role:'Cliente residencial', text:'Recuperaram fotos que eu achava perdidas para sempre. Muito profissionais.' },
  ];

  const BLOG = [
    { cat:'Segurança', date:'12 Jul 2026', title:'5 sinais de que seu PC está infectado', desc:'Aprenda a identificar sinais de vírus antes que causem danos maiores.' },
    { cat:'Dicas', date:'02 Jul 2026', title:'Como prolongar a vida útil do seu notebook', desc:'Cuidados simples que fazem grande diferença no dia a dia.' },
    { cat:'Inteligência Artificial', date:'20 Jun 2026', title:'IA no suporte técnico: o que muda para você', desc:'Como a automação está tornando o suporte mais rápido e acessível.' },
    { cat:'Mercado de TI', date:'05 Jun 2026', title:'Por que investir em backup automático', desc:'Entenda os riscos de não ter uma rotina de backup configurada.' },
    { cat:'Tecnologia', date:'22 Mai 2026', title:'SSD vs HD: vale a pena migrar?', desc:'Comparativo de desempenho, custo e durabilidade entre as duas tecnologias.' },
    { cat:'Informática', date:'10 Mai 2026', title:'Redes Wi-Fi: como eliminar pontos cegos', desc:'Dicas práticas para uma cobertura de rede sem falhas em casa ou na empresa.' },
  ];

  const DOWNLOADS = [
    { icon:'fa-print', name:'Drivers de Impressora (pacote geral)', size:'42 MB' },
    { icon:'fa-shield-halved', name:'Antivírus recomendado (gratuito)', size:'180 MB' },
    { icon:'fa-file-zipper', name:'Utilitário de compactação', size:'6 MB' },
    { icon:'fa-broom', name:'Ferramenta de limpeza de disco', size:'11 MB' },
    { icon:'fa-book', name:'Manual: primeiros socorros de TI', size:'PDF · 2 MB' },
    { icon:'fa-network-wired', name:'Guia de configuração de redes', size:'PDF · 3 MB' },
  ];

  /* ---------- RENDER: SERVIÇOS ---------- */
  const servicesGrid = document.getElementById('servicesGrid');
  servicesGrid.innerHTML = SERVICES.map(s => `
    <div class="service-card glass reveal">
      <div class="service-icon"><i class="fa-solid ${s.icon}"></i></div>
      <h3>${s.title}</h3>
      <p>${s.desc}</p>
      <a href="#contato" class="btn btn-ghost btn-sm">Solicitar</a>
    </div>`).join('');

  /* ---------- RENDER: PORTFÓLIO ---------- */
  const gradients = ['linear-gradient(135deg,#0F1D3A,#2F6BFF)','linear-gradient(135deg,#0A1128,#00E5FF)','linear-gradient(135deg,#16274A,#2F6BFF)','linear-gradient(135deg,#05070D,#0F1D3A)'];
  const portfolioGrid = document.getElementById('portfolioGrid');
  function renderPortfolio(filter) {
    const items = filter === 'all' ? PORTFOLIO : PORTFOLIO.filter(p => p.cat === filter);
    portfolioGrid.innerHTML = items.map((p, i) => `
      <div class="portfolio-item reveal in" data-cat="${p.cat}" data-index="${PORTFOLIO.indexOf(p)}">
        <div class="portfolio-thumb" style="background:${gradients[i % gradients.length]}"><span>${p.label.toUpperCase()}</span></div>
        <div class="portfolio-cap"><b>${p.title}</b><small>${p.label}</small></div>
      </div>`).join('');
    portfolioGrid.querySelectorAll('.portfolio-item').forEach(el => el.addEventListener('click', () => openLightbox(+el.dataset.index)));
  }
  renderPortfolio('all');
  document.querySelectorAll('#filterRow .filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#filterRow .filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderPortfolio(btn.dataset.filter);
    });
  });

  /* ---------- LIGHTBOX ---------- */
  const lightbox = document.getElementById('lightbox');
  function openLightbox(index) {
    const p = PORTFOLIO[index];
    document.getElementById('lightboxThumb').style.background = gradients[index % gradients.length];
    document.getElementById('lightboxThumb').textContent = p.label.toUpperCase();
    document.getElementById('lightboxCat').textContent = p.label;
    document.getElementById('lightboxTitle').textContent = p.title;
    document.getElementById('lightboxDesc').textContent = p.desc;
    lightbox.classList.add('open');
  }
  document.getElementById('lightboxClose').addEventListener('click', () => lightbox.classList.remove('open'));
  lightbox.addEventListener('click', (e) => { if (e.target === lightbox) lightbox.classList.remove('open'); });

  /* ---------- RENDER: DIFERENCIAIS ---------- */
  document.getElementById('diffGrid').innerHTML = DIFERENCIAIS.map(d => `
    <div class="diff-card glass reveal"><i class="fa-solid ${d.icon}"></i><h4>${d.title}</h4></div>`).join('');

  /* ---------- RENDER + CARROSSEL: DEPOIMENTOS ---------- */
  const testiSlides = document.getElementById('testiSlides');
  const testiDots = document.getElementById('testiDots');
  testiSlides.innerHTML = TESTIMONIALS.map(t => `
    <div class="testi-slide">
      <div class="testi-card glass">
        <div class="testi-stars">★★★★★</div>
        <p class="testi-text">"${t.text}"</p>
        <div class="testi-person">
          <div class="testi-avatar">${t.name.split(' ').map(n=>n[0]).slice(0,2).join('')}</div>
          <div><b>${t.name}</b><span>${t.role}</span></div>
        </div>
      </div>
    </div>`).join('');
  testiDots.innerHTML = TESTIMONIALS.map((_, i) => `<button class="testi-dot ${i===0?'active':''}" data-i="${i}"></button>`).join('');
  let testiIndex = 0;
  function goToSlide(i) {
    testiIndex = i;
    testiSlides.style.transform = `translateX(-${i*100}%)`;
    testiDots.querySelectorAll('.testi-dot').forEach((d, idx) => d.classList.toggle('active', idx === i));
  }
  testiDots.querySelectorAll('.testi-dot').forEach(d => d.addEventListener('click', () => goToSlide(+d.dataset.i)));
  setInterval(() => goToSlide((testiIndex + 1) % TESTIMONIALS.length), 5500);

  /* ---------- RENDER: BLOG ---------- */
  document.getElementById('blogGrid').innerHTML = BLOG.map(b => `
    <article class="blog-card glass reveal">
      <div class="blog-thumb" style="background:linear-gradient(135deg,#0A1128,#2F6BFF);">${b.cat.toUpperCase()}</div>
      <div class="blog-body">
        <span class="blog-meta">${b.date}</span>
        <h3>${b.title}</h3>
        <p>${b.desc}</p>
        <a href="#" class="blog-link">Ler artigo <i class="fa-solid fa-arrow-right"></i></a>
      </div>
    </article>`).join('');

  /* ---------- RENDER: DOWNLOADS ---------- */
  document.getElementById('dlGrid').innerHTML = DOWNLOADS.map(d => `
    <div class="dl-card glass reveal">
      <div class="dl-icon"><i class="fa-solid ${d.icon}"></i></div>
      <div class="dl-info"><b>${d.name}</b><span>${d.size}</span></div>
      <a href="#" class="dl-btn" title="Baixar"><i class="fa-solid fa-download"></i></a>
    </div>`).join('');

  // re-observe newly injected reveal elements
  document.querySelectorAll('.reveal:not(.in)').forEach(el => io.observe(el));

  /* ---------- FORMULÁRIO DE CONTATO ---------- */
  const contactForm = document.getElementById('contactForm');
  const formSuccess = document.getElementById('formSuccess');
  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      nome: document.getElementById('nome').value,
      telefone: document.getElementById('telefone').value,
      email: document.getElementById('email').value,
      mensagem: document.getElementById('mensagem').value,
    };
    // tenta enviar para o backend Flask (/api/contato), se existir; caso contrário apenas confirma visualmente
    try {
      await fetch('/api/contato', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
    } catch (err) { /* versão estática sem backend: segue apenas com feedback visual */ }
    formSuccess.classList.add('show');
    contactForm.reset();
    setTimeout(() => formSuccess.classList.remove('show'), 6000);
  });

  /* ---------- VOLTAR AO TOPO ---------- */
  const backToTop = document.getElementById('back-to-top');
  backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

});
