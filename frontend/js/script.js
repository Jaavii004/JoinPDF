// CURSOR
const cursor = document.getElementById('cursor');
const ring = document.getElementById('cursorRing');
let mx = 0, my = 0, rx = 0, ry = 0;
document.addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY;
    cursor.style.left = mx - 6 + 'px';
    cursor.style.top = my - 6 + 'px';
});
function animateRing() {
    rx += (mx - rx - 18) * 0.12;
    ry += (my - ry - 18) * 0.12;
    ring.style.left = rx + 'px';
    ring.style.top = ry + 'px';
    requestAnimationFrame(animateRing);
}
animateRing();
document.querySelectorAll('a,button,[onclick]').forEach(el => {
    el.addEventListener('mouseenter', () => {
        cursor.style.transform = 'scale(2)';
        ring.style.width = '50px';
        ring.style.height = '50px';
        ring.style.opacity = '0.5';
    });
    el.addEventListener('mouseleave', () => {
        cursor.style.transform = 'scale(1)';
        ring.style.width = '36px';
        ring.style.height = '36px';
        ring.style.opacity = '1';
    });
});

// NAV SCROLL
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 40);
});

// SCROLL REVEAL
const reveals = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
        if (e.isIntersecting) {
            e.target.classList.add('visible');
            // Animate progress bars
            e.target.querySelectorAll('.progress-fill').forEach(bar => {
                const t = bar.dataset.target;
                if (t) { bar.style.width = t; }
            });
            // Animate counters
            animateCounters(e.target);
            observer.unobserve(e.target);
        }
    });
}, { threshold: 0.1 });
reveals.forEach(el => observer.observe(el));

// Also watch bento items directly
document.querySelectorAll('.bento-item,.step-card,.glass-card,.review-card').forEach(el => {
    observer.observe(el);
});

// PROGRESS BARS via separate observer
const pbObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
        if (e.isIntersecting) {
            e.target.querySelectorAll('.progress-fill[data-target]').forEach(bar => {
                setTimeout(() => { bar.style.width = bar.dataset.target; }, 200);
            });
            pbObs.unobserve(e.target);
        }
    });
}, { threshold: 0.2 });
document.querySelectorAll('.bento-item').forEach(el => pbObs.observe(el));

// STATS COUNTER
function countUp(el, target, duration, suffix = '') {
    let start = 0;
    const step = target / (duration / 16);
    const timer = setInterval(() => {
        start += step;
        if (start >= target) { start = target; clearInterval(timer); }
        el.textContent = Math.floor(start).toLocaleString('es') + suffix;
    }, 16);
}
function animateCounters(container) { }
const statsObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
        if (e.isIntersecting) {
            const s1 = document.getElementById('stat1');
            const s3 = document.getElementById('stat3');
            if (s1) countUp(s1, 10247, 1800, '+');
            if (s3) countUp(s3, 3812, 1500, '+');
            statsObs.unobserve(e.target);
        }
    });
}, { threshold: 0.3 });
const statsRow = document.querySelector('.stats-row');
if (statsRow) statsObs.observe(statsRow);

// HERO PROGRESS BAR
function animateHeroBar() {
    const bar = document.getElementById('hero-bar');
    const pct = document.getElementById('hero-pct');
    if (!bar) return;
    let p = 0;
    const interval = setInterval(() => {
        p += 1.5;
        if (p > 100) { p = 100; clearInterval(interval); }
        bar.style.width = p + '%';
        if (pct) pct.textContent = Math.floor(p) + '%';
    }, 20);
}
setTimeout(animateHeroBar, 1200);

// BENTO MOUSE GRADIENT
document.querySelectorAll('.bento-item').forEach(el => {
    el.addEventListener('mousemove', e => {
        const rect = el.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 100;
        el.style.setProperty('--mx', x + '%');
        el.style.setProperty('--my', y + '%');
    });
});

// FAQ TOGGLE
function toggleFaq(el) {
    const item = el.parentElement;
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
}

// CONTEXT MENU FLOAT HIDE
setTimeout(() => {
    const cm = document.getElementById('contextMenuHint');
    if (cm) {
        cm.style.transition = 'opacity 0.5s';
        cm.style.opacity = '0';
        setTimeout(() => { cm.style.display = 'none'; }, 500);
    }
}, 4000);

// TICKER DUPLICATE for seamless loop (already duplicated in HTML)

// SCROLL PROGRESS
const progressEl = document.createElement('div');
progressEl.style.cssText = 'position:fixed;top:0;left:0;height:2px;background:var(--green);z-index:9999;transition:width 0.1s;width:0%;box-shadow:0 0 8px var(--green-glow);';
document.body.appendChild(progressEl);
window.addEventListener('scroll', () => {
    const pct = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
    progressEl.style.width = pct + '%';
});