/* Dishaa Platinum — interactions */
(() => {
  const WA = "918169120942";
  const EMAIL = "sales@dishaaplatinum.com";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const store = {
    get() { try { return JSON.parse(localStorage.getItem("dishaa-tray") || "[]"); } catch { return []; } },
    set(v) { try { localStorage.setItem("dishaa-tray", JSON.stringify(v)); } catch {} },
  };

  /* header */
  const hdr = $(".hdr");
  const hasHero = document.body.dataset.hero === "dark";
  let lastY = 0;
  const onScroll = () => {
    const y = scrollY;
    hdr.classList.toggle("solid", y > 40 || !hasHero);
    hdr.classList.toggle("hide", y > 500 && y > lastY && !document.body.classList.contains("menu-open"));
    lastY = y;
  };
  addEventListener("scroll", onScroll, { passive: true }); onScroll();
  $(".burger")?.addEventListener("click", () => document.body.classList.toggle("menu-open"));
  $$(".mnav a").forEach(a => a.addEventListener("click", () => document.body.classList.remove("menu-open")));

  /* reveal */
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
  }), { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
  $$(".rv, .split-line.rv-s").forEach(el => io.observe(el));

  /* videos play only in view */
  const vio = new IntersectionObserver(es => es.forEach(e => {
    const v = e.target;
    if (e.isIntersecting) { v.play().catch(() => {}); } else v.pause();
  }), { threshold: 0.15 });
  $$("video[data-auto]").forEach(v => { v.muted = true; vio.observe(v); });

  /* hero slides: circular wipe, word entrances (anime.js), pointer parallax */
  const slides = $$(".slide"), dots = $$(".hero-dots button");
  const A = window.anime, calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const splitWords = el => [...el.childNodes].forEach(n => {
    if (n.nodeType === 3) {
      const f = document.createDocumentFragment();
      n.textContent.split(/(\s+)/).forEach(w => {
        if (!w) return;
        if (!w.trim()) { f.append(w); return; }
        const s = document.createElement("span"); s.className = "w"; s.textContent = w; f.append(s);
      });
      n.replaceWith(f);
    } else if (n.nodeType === 1 && !n.classList.contains("w")) splitWords(n);
  });
  $$(".bnr .ln, .bnr .g-2").forEach(splitWords);
  /* hero slide 1: auto-expanding collection panels */
  const ed = $(".bnr .ed"), eps = ed ? $$(".ep", ed) : [];
  let epI = 0, epT;
  const ED_MS = 2900;
  const epGo = n => {
    epI = (n + eps.length) % eps.length;
    eps.forEach((p, k) => { p.classList.toggle("on", k === epI); p.classList.remove("run"); });
    const cur = eps[epI]; cur.style.setProperty("--ed", ED_MS + "ms"); void cur.offsetWidth; cur.classList.add("run");
  };
  const epPlay = on => { clearInterval(epT); if (on && eps.length && !calm) epT = setInterval(() => epGo(epI + 1), ED_MS); };
  /* hero slide 3: collection showcase */
  const cs = $(".bnr .cs"), csL = cs ? [$$(".cs-item", cs), $$(".cs-tile", cs), $$(".cs-name", cs)] : [[], [], []];
  let csI = 0, csT; const CS_MS = 2100;
  const csGo = n => {
    const len = csL[0].length; if (!len) return; csI = (n + len) % len;
    csL.forEach(list => list.forEach((e, k) => e.classList.toggle("on", k === csI)));
    const t = csL[1][csI]; if (t) { t.style.setProperty("--cs", CS_MS + "ms"); t.classList.remove("on"); void t.offsetWidth; t.classList.add("on"); }
  };
  const csPlay = on => { clearInterval(csT); if (on && csL[0].length && !calm) csT = setInterval(() => csGo(csI + 1), CS_MS); };
  csL[1].forEach((t, k) => t.addEventListener("mouseenter", () => { csGo(k); csPlay(true); }));
  eps.forEach((p, k) => p.addEventListener("mouseenter", () => { if (matchMedia("(hover: hover)").matches) { epGo(k); epPlay(!heroPaused); } }));
  const enter = sl => {
    if (!A || calm) return;
    A.remove(sl.querySelectorAll(".w"));
    A({ targets: sl.querySelectorAll(".w"), translateY: ["0.8em", 0], rotate: [5, 0], opacity: [0, 1],
        delay: A.stagger(60, { start: 380 }), duration: 1200, easing: "easeOutExpo" });
    sl.querySelectorAll(".bstats b[data-n]").forEach(b => {
      const o = { v: 0 }, end = +b.dataset.n, sfx = b.dataset.s || "";
      A({ targets: o, v: end, round: 1, delay: 1000, duration: 1700, easing: "easeOutExpo", update: () => b.textContent = o.v.toLocaleString("en-IN") + sfx });
    });
    const g = sl.querySelectorAll(".g-meta span, .g-ctas > *, .bcta");
    if (g.length) A({ targets: g, translateY: [14, 0], opacity: [0, 1], delay: A.stagger(90, { start: 900 }), duration: 900, easing: "easeOutCubic" });
  };
  var heroPaused = false;
  if (slides.length > 1) {
    let i = 0, t, outT, seen = true;
    const frame = $(".bnr-frame");
    const dur = () => +slides[i].dataset.dur || 7000;
    const arm = () => { clearTimeout(t); if (!heroPaused) t = setTimeout(() => seen ? go(i + 1) : arm(), dur()); };
    const go = n => {
      const prev = i;
      i = (n + slides.length) % slides.length;
      if (prev !== i) {
        slides.forEach(s => s.classList.remove("out"));
        slides[prev].classList.remove("on"); slides[prev].classList.add("out");
        clearTimeout(outT); outT = setTimeout(() => slides[prev].classList.remove("out"), 1350);
      }
      dots.forEach(d => d.classList.remove("on"));
      slides[i].classList.add("on"); enter(slides[i]);
      if (slides[i] === ed) { epGo(0); epPlay(!heroPaused); } else epPlay(false);
      if (slides[i] === cs) { csGo(0); csPlay(!heroPaused); } else csPlay(false);
      const d = dots[i]; if (d) { d.style.setProperty("--dur", dur() + "ms"); void d.offsetWidth; d.classList.add("on"); }
      arm();
    };
    dots.forEach((d, n) => d.addEventListener("click", () => go(n)));
    $("[data-prev]")?.addEventListener("click", () => go(i - 1));
    $("[data-next]")?.addEventListener("click", () => go(i + 1));
    $("[data-hero-pause]")?.addEventListener("click", e => {
      heroPaused = !heroPaused; frame.classList.toggle("is-paused", heroPaused);
      e.currentTarget.setAttribute("aria-label", heroPaused ? "Play slideshow" : "Pause slideshow");
      if (heroPaused) { clearTimeout(t); epPlay(false); } else { go(i); }
    });
    if (frame) new IntersectionObserver(es => { seen = es[0].isIntersecting; }, { threshold: 0.25 }).observe(frame);
    let hx = 0;
    const hero = $(".bnr") || $(".hero");
    hero?.addEventListener("touchstart", e => hx = e.touches[0].clientX, { passive: true });
    hero?.addEventListener("touchend", e => { const dx = e.changedTouches[0].clientX - hx; if (Math.abs(dx) > 50) go(i + (dx < 0 ? 1 : -1)); });
    requestAnimationFrame(() => go(0));
    /* depth parallax that follows the pointer (desktop only) */
    if (frame && !calm && matchMedia("(hover: hover) and (min-width: 761px)").matches) {
      let tx = 0, ty = 0, cx = 0, cy = 0, raf = 0;
      const loop = () => {
        cx += (tx - cx) * 0.08; cy += (ty - cy) * 0.08;
        frame.style.setProperty("--px", cx.toFixed(2) + "px"); frame.style.setProperty("--py", cy.toFixed(2) + "px");
        raf = Math.abs(tx - cx) + Math.abs(ty - cy) > 0.05 ? requestAnimationFrame(loop) : 0;
      };
      frame.addEventListener("mousemove", e => {
        const r = frame.getBoundingClientRect();
        tx = ((e.clientX - r.left) / r.width - 0.5) * -22; ty = ((e.clientY - r.top) / r.height - 0.5) * -14;
        if (!raf) raf = requestAnimationFrame(loop);
      });
      frame.addEventListener("mouseleave", () => { tx = ty = 0; if (!raf) raf = requestAnimationFrame(loop); });
    }
  }

  /* spotlight deck (anime.js) */
  $$(".deck").forEach(deck => {
    const cards = $$(".dk-card", deck), tabs = $$(".dk-tab", deck), cnt = $(".dk-count b", deck), n = cards.length;
    const P = [{ x: 0, y: 0, s: 1, r: 0, o: 1 }, { x: 5, y: -4, s: .93, r: 2.5, o: .85 }, { x: 10, y: -8, s: .86, r: 5, o: .55 }];
    let k = 0, t, hold = false;
    const place = (c, pos, animate, thrown) => {
      c.dataset.pos = pos; const p = P[Math.min(pos, P.length - 1)];
      const to = { translateX: p.x + "%", translateY: p.y + "%", scale: p.s, rotate: p.r, opacity: p.o };
      if (!A || !animate || calm) { Object.assign(c.style, { transform: `translate(${p.x}%,${p.y}%) scale(${p.s}) rotate(${p.r}deg)`, opacity: p.o }); return; }
      A.remove(c);
      if (thrown) A({ targets: c, keyframes: [{ translateX: "-16%", translateY: "4%", rotate: -7, scale: .96, opacity: .9, duration: 380, easing: "easeOutCubic" }, { ...to, duration: 700, easing: "easeInOutQuart" }] });
      else A({ targets: c, ...to, duration: 950, easing: "spring(1, 80, 14, 0)" });
    };
    const set = (nk, animate = true) => {
      const fwd = ((nk - k + n) % n) === 1;
      const old = k; k = (nk + n) % n;
      cards.forEach((c, j) => place(c, (j - k + n) % n, animate, animate && fwd && j === old));
      tabs.forEach((b, j) => { b.classList.toggle("on", j === k); b.classList.remove("run"); });
      if (tabs[k]) { void tabs[k].offsetWidth; if (!hold) tabs[k].classList.add("run"); }
      if (cnt) cnt.textContent = String(k + 1).padStart(2, "0");
      clearTimeout(t); if (!hold) t = setTimeout(() => set(k + 1), 5500);
    };
    tabs.forEach((b, j) => b.addEventListener("click", () => set(j)));
    $("[data-dk-prev]", deck)?.addEventListener("click", () => set(k - 1));
    $("[data-dk-next]", deck)?.addEventListener("click", () => set(k + 1));
    $("[data-dk-pause]", deck)?.addEventListener("click", e => {
      hold = !hold; deck.classList.toggle("is-paused", hold);
      e.currentTarget.setAttribute("aria-label", hold ? "Play stories" : "Pause stories");
      if (hold) clearTimeout(t); else set(k, false);
    });
    let sx = 0;
    deck.addEventListener("touchstart", e => sx = e.touches[0].clientX, { passive: true });
    deck.addEventListener("touchend", e => { const dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 40) set(k + (dx < 0 ? 1 : -1)); });
    set(0, false);
  });

  /* collection showcase (Lumina-style): auto-advance, hover/click tabs */
  $$(".showcase").forEach(sc => {
    const stages = $$(".sc-stage", sc), tabs = $$(".sc-tab", sc), bar = $(".sc-bar i", sc);
    let i = 0, t, paused = false;
    const go = n => {
      i = (n + stages.length) % stages.length;
      stages.forEach((s, k) => s.classList.toggle("on", k === i));
      tabs.forEach((b, k) => { b.classList.toggle("on", k === i); b.setAttribute("aria-selected", k === i); });
      if (bar) { bar.classList.remove("run"); void bar.offsetWidth; if (!paused) bar.classList.add("run"); }
      clearTimeout(t); if (!paused) t = setTimeout(() => go(i + 1), 6000);
    };
    tabs.forEach((b, k) => { b.addEventListener("click", () => go(k)); b.addEventListener("mouseenter", () => go(k)); });
    sc.addEventListener("mouseenter", () => { paused = true; clearTimeout(t); bar && bar.classList.remove("run"); });
    sc.addEventListener("mouseleave", () => { paused = false; go(i); });
    if (!matchMedia("(prefers-reduced-motion: reduce)").matches) go(0);
  });

  /* stagger reveals inside grids */
  $$(".bento, .bento-tiles, .chips, .cards, .values, .pgrid, .zones, .ribbon").forEach(g =>
    [...g.children].forEach((el, k) => { if (el.classList.contains("rv")) el.style.transitionDelay = (k % 8) * 70 + "ms"; }));

  /* sparkles */
  $$(".sparkle").forEach(box => {
    const n = +box.dataset.n || 22;
    for (let k = 0; k < n; k++) {
      const i = document.createElement("i");
      i.style.left = Math.random() * 100 + "%"; i.style.top = Math.random() * 100 + "%";
      i.style.animationDelay = (Math.random() * 4).toFixed(2) + "s";
      const sz = (2 + Math.random() * 3).toFixed(1) + "px"; i.style.width = i.style.height = sz;
      box.append(i);
    }
  });

  /* statement word-by-word light */
  const st = $(".statement");
  if (st) {
    const words = [];
    const walk = node => [...node.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(w => {
          if (!w.trim()) { frag.append(w); return; }
          const s = document.createElement("span"); s.className = "w"; s.textContent = w; words.push(s); frag.append(s);
        });
        n.replaceWith(frag);
      } else if (n.nodeType === 1) walk(n);
    });
    walk(st);
    const light = () => {
      const r = st.getBoundingClientRect();
      const p = Math.min(1, Math.max(0, (innerHeight * 0.85 - r.top) / (r.height + innerHeight * 0.35)));
      const k = Math.round(p * words.length);
      words.forEach((w, j) => w.classList.toggle("lit", j < k));
    };
    addEventListener("scroll", light, { passive: true }); light();
  }

  /* counters */
  const cio = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    const el = e.target, end = +el.dataset.count, suf = el.dataset.suffix || "";
    const t0 = performance.now(), dur = 1800;
    const tick = t => {
      const p = Math.min(1, (t - t0) / dur), v = Math.round(end * (1 - Math.pow(1 - p, 4)));
      el.textContent = v.toLocaleString("en-IN") + suf;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick); cio.unobserve(el);
  }), { threshold: 0.5 });
  $$("[data-count]").forEach(el => cio.observe(el));

  /* reach map: light up the pin for the hovered direction */
  $$(".dirs .dir").forEach(d => {
    const pin = $(".pin." + d.dataset.pin);
    d.addEventListener("mouseenter", () => pin && pin.classList.add("lit"));
    d.addEventListener("mouseleave", () => pin && pin.classList.remove("lit"));
  });

  /* compass */
  const needle = $(".compass .needle");
  if (needle) {
    const ang = { n: 0, e: 90, s: 180, w: 270 };
    $$(".dir").forEach(d => d.addEventListener("mouseenter", () => needle.style.transform = `rotate(${ang[d.dataset.dir]}deg)`));
    let k = 0;
    const auto = setInterval(() => { needle.style.transform = `rotate(${k * 90}deg)`; k++; }, 2600);
    $(".compass-wrap").addEventListener("mouseenter", () => clearInterval(auto), { once: true });
  }

  /* toast */
  const toast = $(".toast");
  let tt;
  const say = html => { if (!toast) return; toast.innerHTML = html; toast.classList.add("on"); clearTimeout(tt); tt = setTimeout(() => toast.classList.remove("on"), 3200); };

  /* selection tray */
  const tray = $(".tray"), scrim = $(".scrim");
  const openTray = on => { tray.classList.toggle("on", on); scrim.classList.toggle("on", on); if (on) renderTray(); };
  $$("[data-open-tray]").forEach(b => b.addEventListener("click", e => { e.preventDefault(); openTray(true); }));
  $$("[data-close-tray]").forEach(b => b.addEventListener("click", () => openTray(false)));
  scrim?.addEventListener("click", () => { openTray(false); });
  const countEls = $$(".tray-btn i");
  const syncCount = () => {
    const n = store.get().length;
    countEls.forEach(c => { c.textContent = n; c.classList.toggle("has", n > 0); });
    $$(".pcard").forEach(c => c.querySelector(".add")?.classList.toggle("on", store.get().some(x => x.code === c.dataset.code)));
  };
  const toggleItem = it => {
    let list = store.get();
    const has = list.some(x => x.code === it.code);
    list = has ? list.filter(x => x.code !== it.code) : [...list, it];
    store.set(list); syncCount();
    say(has ? `Removed ${it.code} from your tray` : `Added ${it.code} to your selection tray · <a href="#" data-open-tray>View</a>`);
    $$(".toast [data-open-tray]").forEach(b => b.addEventListener("click", e => { e.preventDefault(); openTray(true); }));
    return !has;
  };
  const trayText = () => {
    const list = store.get();
    const lines = list.map((x, i) => `${i + 1}. ${x.code} — ${x.col} / ${x.cat}`);
    return `Hello Dishaa Platinum, I'd like details, weights and availability for these designs:\n\n${lines.join("\n")}\n\nStore name:\nCity:`;
  };
  function renderTray() {
    const list = store.get(), box = $(".tray-list");
    if (!box) return;
    box.innerHTML = list.length ? list.map(x => `
      <div class="tray-item"><img src="${x.img}" alt="" loading="lazy"><div><b>${x.code}</b><span>${x.col} · ${x.cat}</span></div>
      <button aria-label="Remove ${x.code}" data-rm="${x.code}">&times;</button></div>`).join("")
      : `<div class="tray-empty">Your tray is empty.<br>Tap the <b>+</b> on any design to shortlist it for your counter.</div>`;
    $$("[data-rm]", box).forEach(b => b.addEventListener("click", () => {
      store.set(store.get().filter(x => x.code !== b.dataset.rm)); syncCount(); renderTray();
    }));
    const n = $(".tray-n"); if (n) n.textContent = `${list.length} design${list.length === 1 ? "" : "s"} shortlisted`;
  }
  $("[data-tray-wa]")?.addEventListener("click", () => {
    if (!store.get().length) return say("Add a few designs first");
    open(`https://wa.me/${WA}?text=${encodeURIComponent(trayText())}`, "_blank", "noopener");
  });
  $("[data-tray-mail]")?.addEventListener("click", () => {
    if (!store.get().length) return say("Add a few designs first");
    location.href = `mailto:${EMAIL}?subject=${encodeURIComponent("Design enquiry — selection tray")}&body=${encodeURIComponent(trayText())}`;
  });
  $("[data-tray-clear]")?.addEventListener("click", () => { store.set([]); syncCount(); renderTray(); });
  syncCount();

  /* product grid: filters + load more */
  const grid = $(".pgrid");
  if (grid && $(".pdlb")) {
    const cards = $$(".pcard", grid), PAGE = 24;
    let cat = "all", aud = "all", shown = PAGE;
    const moreBtn = $("[data-more]");
    const fits = c => (aud === "all" || c.dataset.aud === aud) && (cat === "all" || c.dataset.cat === cat);
    const apply = () => {
      let n = 0, total = 0;
      cards.forEach(c => {
        const ok = fits(c);
        if (ok) total++;
        const vis = ok && n < shown; if (vis) n++;
        c.classList.toggle("hide", !vis);
      });
      if (moreBtn) moreBtn.parentElement.style.display = total > shown ? "" : "none";
    };
    $$(".chip").forEach(ch => ch.addEventListener("click", () => {
      $$(".chip").forEach(x => x.classList.remove("on")); ch.classList.add("on");
      cat = ch.dataset.cat; shown = PAGE; apply();
      const f = $(".filters"); if (f && f.getBoundingClientRect().top < 0) scrollTo({ top: grid.offsetTop - 160, behavior: "smooth" });
    }));
    /* Shop by: men / women / kids / couples */
    const audBtns = $$("[data-aud-btn]");
    const setAud = (a, scroll) => {
      aud = audBtns.some(b => b.dataset.audBtn === a) ? a : "all"; cat = "all"; shown = PAGE;
      audBtns.forEach(b => { const on = b.dataset.audBtn === aud; b.classList.toggle("on", on); b.setAttribute("aria-pressed", on); });
      $$(".chip").forEach(ch => {
        const k = ch.dataset.cat, n = cards.filter(c => (aud === "all" || c.dataset.aud === aud) && (k === "all" || c.dataset.cat === k)).length;
        ch.hidden = k !== "all" && !n; const i = ch.querySelector("i"); if (i) i.textContent = n;
        ch.classList.toggle("on", k === "all");
      });
      $$("[data-look]").forEach(f => f.hidden = !(aud === "all" ? f.dataset.lookAll !== undefined : f.dataset.look === aud));
      const line = $(".aud-line"), b = audBtns.find(x => x.dataset.audBtn === aud);
      if (line && b) line.innerHTML = b.dataset.line;
      apply();
      if (history.replaceState) history.replaceState(null, "", aud === "all" ? location.pathname : "#" + aud);
      if (scroll) scrollTo({ top: $(".audbar").getBoundingClientRect().top + scrollY - 100, behavior: "smooth" });
    };
    audBtns.forEach(b => b.addEventListener("click", () => setAud(b.dataset.audBtn, true)));
    if (audBtns.length) { setAud(location.hash.slice(1) || "all", false); addEventListener("hashchange", () => setAud(location.hash.slice(1), true)); }
    moreBtn?.addEventListener("click", () => { shown += PAGE; apply(); });
    apply();

    /* lightbox */
    const lb = $(".pdlb"), stage = $(".lb-stage img", lb), thumbs = $(".lb-thumbs", lb);
    let cur = 0, visible = [];
    const item = c => ({ code: c.dataset.code, cat: c.dataset.catlabel, col: c.dataset.col, img: JSON.parse(c.dataset.views)[0] });
    const show = idx => {
      visible = cards.filter(c => !c.classList.contains("hide"));
      cur = (idx + visible.length) % visible.length;
      const c = visible[cur], views = JSON.parse(c.dataset.views);
      stage.src = views[0]; stage.alt = `${c.dataset.col} ${c.dataset.catlabel} design ${c.dataset.code}`;
      thumbs.innerHTML = views.length > 1 ? views.map((v, i) => `<button class="${i ? "" : "on"}" data-v="${v}" aria-label="View ${i + 1}"><img src="${v}" alt=""></button>`).join("") : "";
      $$("button", thumbs).forEach(b => b.addEventListener("click", () => { stage.src = b.dataset.v; $$("button", thumbs).forEach(x => x.classList.remove("on")); b.classList.add("on"); }));
      $(".lb-code", lb).textContent = c.dataset.code;
      $(".lb-cat", lb).textContent = c.dataset.catlabel;
      $(".lb-col", lb).textContent = c.dataset.col;
      $(".lb-views", lb).textContent = views.length;
      const inTray = store.get().some(x => x.code === c.dataset.code);
      $(".lb-add", lb).innerHTML = inTray ? "Remove from tray" : "Add to selection tray <span class='ar'>+</span>";
      $(".lb-wa", lb).href = `https://wa.me/${WA}?text=${encodeURIComponent(`Hello Dishaa Platinum, please share weight, price and availability for design ${c.dataset.code} (${c.dataset.col} / ${c.dataset.catlabel}).`)}`;
    };
    const openLb = c => { visible = cards.filter(x => !x.classList.contains("hide")); show(visible.indexOf(c)); lb.classList.add("on"); document.body.style.overflow = "hidden"; };
    const closeLb = () => { lb.classList.remove("on"); document.body.style.overflow = ""; };
    cards.forEach(c => {
      c.addEventListener("click", e => {
        if (e.target.closest(".add")) { e.stopPropagation(); toggleItem(item(c)); return; }
        openLb(c);
      });
      c.addEventListener("keydown", e => { if (e.key === "Enter") openLb(c); });
    });
    $(".lb-add", lb)?.addEventListener("click", () => { toggleItem(item(visible[cur])); show(cur); });
    $(".lb-x", lb)?.addEventListener("click", closeLb);
    $(".lb-prev", lb)?.addEventListener("click", () => show(cur - 1));
    $(".lb-next", lb)?.addEventListener("click", () => show(cur + 1));
    addEventListener("keydown", e => {
      if (!lb.classList.contains("on")) return;
      if (e.key === "Escape") closeLb(); if (e.key === "ArrowLeft") show(cur - 1); if (e.key === "ArrowRight") show(cur + 1);
    });
    let sx = 0;
    lb.addEventListener("touchstart", e => sx = e.touches[0].clientX, { passive: true });
    lb.addEventListener("touchend", e => { const dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 60 && e.target.closest(".lb-stage")) show(cur + (dx < 0 ? 1 : -1)); });
  }

  /* photo lightbox (lookbook) */
  const plb = $(".plb");
  if (plb) {
    const figs = $$("figure[data-full]:not([data-dup])"); $$("figure[data-dup]").forEach(f => f.addEventListener("click", () => figs.find(g => g.dataset.full === f.dataset.full)?.click())); let cur = 0;
    const img = $(".lb-stage img", plb);
    const show = i => { cur = (i + figs.length) % figs.length; img.src = figs[cur].dataset.full; img.alt = figs[cur].querySelector("img")?.alt || ""; };
    figs.forEach((f, i) => f.addEventListener("click", () => { show(i); plb.classList.add("on"); document.body.style.overflow = "hidden"; }));
    const close = () => { plb.classList.remove("on"); document.body.style.overflow = ""; };
    $(".lb-x", plb).addEventListener("click", close);
    $(".lb-prev", plb).addEventListener("click", () => show(cur - 1));
    $(".lb-next", plb).addEventListener("click", () => show(cur + 1));
    addEventListener("keydown", e => { if (!plb.classList.contains("on")) return; if (e.key === "Escape") close(); if (e.key === "ArrowLeft") show(cur - 1); if (e.key === "ArrowRight") show(cur + 1); });
  }

  /* enquiry form -> WhatsApp / email */
  const form = $("#enquiry");
  if (form) {
    const compose = () => {
      const d = new FormData(form);
      const ints = d.getAll("interest").join(", ") || "—";
      return `New partner enquiry — Dishaa Platinum website\n\nName: ${d.get("name")}\nStore: ${d.get("store")}\nCity: ${d.get("city")}\nPhone: ${d.get("phone")}\nEmail: ${d.get("email") || "—"}\nI am: ${d.get("type")}\nInterested in: ${ints}\n\n${d.get("message") || ""}`;
    };
    form.addEventListener("submit", e => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      open(`https://wa.me/${WA}?text=${encodeURIComponent(compose())}`, "_blank", "noopener");
    });
    $("[data-mail]", form)?.addEventListener("click", () => {
      if (!form.reportValidity()) return;
      location.href = `mailto:${EMAIL}?subject=${encodeURIComponent("Partner enquiry — " + (new FormData(form).get("store") || ""))}&body=${encodeURIComponent(compose())}`;
    });
    const pre = new URLSearchParams(location.search).get("interest");
    if (pre) $$(`input[name=interest][value="${pre}"]`, form).forEach(i => i.checked = true);
  }
})();
