/* ===================================================================
   widgets.js: simuladores e calculadoras interativas
   Uso nas páginas: <div data-widget="nome"></div>
   Mecânica Clássica I / LFCA–URCA
   =================================================================== */

(function () {
  'use strict';

  /* ---------- utilitários de DOM ---------- */
  function el(tag, attrs, filhos) {
    var n = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'class') n.className = attrs[k];
      else if (k === 'html') n.innerHTML = attrs[k];
      else if (k === 'texto') n.textContent = attrs[k];
      else n.setAttribute(k, attrs[k]);
    });
    (filhos || []).forEach(function (c) { n.appendChild(c); });
    return n;
  }

  function moldura(raiz, titulo) {
    raiz.classList.add('widget');
    raiz.appendChild(el('div', { class: 'widget-cabeca', texto: titulo }));
    var corpo = el('div', { class: 'widget-corpo' });
    raiz.appendChild(corpo);
    return corpo;
  }

  /* Devolve o <input type=range>, para que o chamador possa movê-lo por código. */
  function deslizante(pai, rot, min, max, passo, inicial, aoMudar, formata) {
    var campo = el('div', { class: 'campo' });
    var lab = el('label');
    var val = el('span', { class: 'valor' });
    var inp = el('input', { type: 'range', min: min, max: max, step: passo, value: inicial });
    function mostrar() {
      val.innerHTML = formata ? formata(Number(inp.value)) : String(inp.value).replace('.', ',');
    }
    lab.innerHTML = rot + ' ';
    lab.appendChild(val);
    campo.appendChild(lab);
    campo.appendChild(inp);
    pai.appendChild(campo);
    inp.addEventListener('input', function () { mostrar(); aoMudar(Number(inp.value)); });
    mostrar();
    return inp;
  }

  /* Botões mutuamente exclusivos. Devolve uma função que troca a seleção. */
  function opcoes(pai, lista, inicial, aoMudar) {
    var cx = el('div', { class: 'botoes' });
    var bs = lista.map(function (o, i) {
      var b = el('button', { type: 'button', texto: o.rot });
      if (i !== inicial) b.classList.add('sec');
      b.addEventListener('click', function () {
        bs.forEach(function (x) { x.classList.add('sec'); });
        b.classList.remove('sec');
        aoMudar(o.v, o);
      });
      cx.appendChild(b);
      return b;
    });
    pai.appendChild(cx);
    return function (i) { bs[i].click(); };
  }

  function cartoes(pai, lista) {
    var g = el('div', { class: 'grade-num' });
    lista.forEach(function (c) {
      g.appendChild(el('div', { class: 'cartao-num', html:
        '<span class="rot">' + c.rot + '</span><span class="val" data-k="' + c.k + '">·</span>' }));
    });
    pai.appendChild(g);
    return function (vals) {
      Object.keys(vals).forEach(function (k) {
        var n = g.querySelector('[data-k="' + k + '"]');
        if (n) n.innerHTML = vals[k];
      });
    };
  }

  function tipografar(no) {
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([no]).catch(function () {});
    }
  }

  var REGISTRO = {};


  /* Seta com ponta, usada por quase todo widget de cinemática. */
  function seta(ct, xa, ya, xb, yb, cor, esp, tracejado) {
    var dx = xb - xa, dy = yb - ya, r = Math.sqrt(dx * dx + dy * dy);
    if (r < 1.5) return;
    var ux = dx / r, uy = dy / r, p = Math.min(8, r * 0.42);
    ct.save();
    ct.strokeStyle = cor; ct.fillStyle = cor;
    ct.lineWidth = esp || 2; ct.lineCap = 'round'; ct.lineJoin = 'round';
    if (tracejado) ct.setLineDash(tracejado);
    ct.beginPath(); ct.moveTo(xa, ya); ct.lineTo(xb - ux * p * 0.8, yb - uy * p * 0.8);
    ct.stroke();
    ct.setLineDash([]);
    ct.beginPath();
    ct.moveTo(xb, yb);
    ct.lineTo(xb - ux * p - uy * p * 0.46, yb - uy * p + ux * p * 0.46);
    ct.lineTo(xb - ux * p + uy * p * 0.46, yb - uy * p - ux * p * 0.46);
    ct.closePath(); ct.fill();
    ct.restore();
  }

  /* Rótulo com halo branco, legível por cima de qualquer desenho. */
  function rotulo(ct, texto, x, y, cor, al, bl, fonte, corHalo) {
    ct.save();
    ct.font = fonte || '600 11px system-ui, sans-serif';
    ct.textAlign = al || 'center'; ct.textBaseline = bl || 'middle';
    ct.lineJoin = 'round'; ct.lineWidth = 3.5; ct.strokeStyle = corHalo || '#fff';
    ct.strokeText(texto, x, y);
    ct.fillStyle = cor; ct.fillText(texto, x, y);
    ct.restore();
  }

  /* =================================================================
     1. Lançamento de projétil pelo método de Euler
     O ponto do módulo 3 é que a equação de movimento com arrasto não
     tem solução fechada, e que isso não é obstáculo nenhum: basta
     escrever o sistema de quatro equações de primeira ordem e andar no
     tempo. As três vistas respondem às três perguntas que o aluno faz:
     o que sai diferente da parábola, o que exatamente o computador faz
     em cada passo, e quanto o resultado erra.
     ================================================================= */
  REGISTRO.projetil = function (raiz) {
    var est = { v0: 50, ang: 45, k: 0.004, dt: 0.2, vista: 'traj',
                tipo: 'quad' };
    var g = 9.81;

    /* ---- o sistema de equações ----
       O estado é u = [x, y, vx, vy] e a derivada é f(u). Escrever
       assim, como vetor, é o que permite usar o MESMO passo de Euler
       para qualquer número de equações. */
    /* tau é escolhido de modo que os dois regimes tenham a MESMA
       velocidade terminal, e portanto sejam comparáveis: vt = g*tau no
       linear e vt = sqrt(g/k) no quadrático. */
    function tau() { return Math.sqrt(1 / (g * est.k)); }

    function f(u, k) {
      var vx = u[2], vy = u[3];
      if (est.tipo === 'lin') {
        if (k <= 0) return [vx, vy, 0, -g];
        var it = 1 / tau();
        return [vx, vy, -it * vx, -g - it * vy];
      }
      var v = Math.sqrt(vx * vx + vy * vy);
      return [vx, vy, -k * v * vx, -g - k * v * vy];
    }

    /* ---- a solução fechada do caso linear ----
       x(t) = vx0 tau (1 - e^{-t/tau})
       y(t) = (vy0 + vt) tau (1 - e^{-t/tau}) - vt t
       Ela existe porque, com arrasto linear, as componentes não se
       acoplam. No caso quadrático nada disso vale. */
    function exatoLinear(t) {
      var th = est.ang * Math.PI / 180;
      var vx0 = est.v0 * Math.cos(th), vy0 = est.v0 * Math.sin(th);
      if (est.k <= 0) {
        return [vx0 * t, vy0 * t - 0.5 * g * t * t];
      }
      var T = tau(), vt = g * T, e = Math.exp(-t / T);
      return [vx0 * T * (1 - e), (vy0 + vt) * T * (1 - e) - vt * t];
    }

    function pousoExatoLinear() {
      var a = 1e-6, b = 1, i;
      for (i = 0; i < 80 && exatoLinear(b)[1] > 0; i++) b *= 2;
      for (i = 0; i < 200; i++) {
        var m = 0.5 * (a + b);
        if (exatoLinear(m)[1] > 0) a = m; else b = m;
      }
      return exatoLinear(0.5 * (a + b))[0];
    }

    function passoEuler(u, dt, k) {
      var d = f(u, k), s = [0, 0, 0, 0];
      for (var i = 0; i < 4; i++) s[i] = u[i] + dt * d[i];
      return s;
    }

    function passoRK4(u, dt, k) {
      var a = f(u, k), ub = [], uc = [], ud = [], s = [], i;
      for (i = 0; i < 4; i++) ub[i] = u[i] + dt / 2 * a[i];
      var b = f(ub, k);
      for (i = 0; i < 4; i++) uc[i] = u[i] + dt / 2 * b[i];
      var c = f(uc, k);
      for (i = 0; i < 4; i++) ud[i] = u[i] + dt * c[i];
      var d = f(ud, k);
      for (i = 0; i < 4; i++)
        s[i] = u[i] + dt / 6 * (a[i] + 2 * b[i] + 2 * c[i] + d[i]);
      return s;
    }

    /* Interpolação cúbica de Hermite: usa valor E derivada nas duas
       pontas do passo. Interpolar o ponto de pouso linearmente erraria
       em (Δt)², e isso estragaria a medida do erro do RK4, que passaria
       a parecer de segunda ordem. Como o integrador já fornece as
       velocidades, Hermite sai de graça e erra em (Δt)⁴. */
    function hermite(f0, d0, f1, d1, dt, s) {
      var s2 = s * s, s3 = s2 * s;
      return (2 * s3 - 3 * s2 + 1) * f0
           + (s3 - 2 * s2 + s) * dt * d0
           + (-2 * s3 + 3 * s2) * f1
           + (s3 - s2) * dt * d1;
    }

    function pouso(ant, dep, dt) {
      var a = 0, b = 1, m, i;
      for (i = 0; i < 60; i++) {
        m = 0.5 * (a + b);
        if (hermite(ant[1], ant[3], dep[1], dep[3], dt, m) > 0) a = m; else b = m;
      }
      m = 0.5 * (a + b);
      return hermite(ant[0], ant[2], dep[0], dep[2], dt, m);
    }

    /* Integra até o projétil voltar ao chão. Devolve a trajetória e o
       alcance, interpolado entre os dois últimos pontos para que o
       resultado não dependa de onde o passo caiu. */
    function voo(dt, k, metodo, maxPassos) {
      var th = est.ang * Math.PI / 180;
      var u = [0, 0, est.v0 * Math.cos(th), est.v0 * Math.sin(th)];
      var pts = [[u[0], u[1]]], n = 0, lim = maxPassos || 400000;
      var passo = metodo === 'rk4' ? passoRK4 : passoEuler;
      while (n < lim) {
        var ant = u;
        u = passo(u, dt, k);
        n++;
        if (u[1] < 0) {
          var xq = pouso(ant, u, dt);
          pts.push([xq, 0]);
          return { pts: pts, alcance: xq, passos: n, t: n * dt };
        }
        pts.push([u[0], u[1]]);
        if (n > 20 && u[1] > 1e7) break;
      }
      /* Chegou ao limite de passos sem tocar o chão. Devolver o estado
         atual como se fosse o alcance produziria um número plausível e
         errado, que foi exatamente o que aconteceu numa versão anterior
         deste widget: a referência parava no meio do voo e todas as
         inclinações davam zero. Melhor marcar. */
      return { pts: pts, alcance: u[0], passos: n, t: n * dt, truncado: true };
    }

    function alcanceSemArrasto() {
      var th = est.ang * Math.PI / 180;
      return est.v0 * est.v0 * Math.sin(2 * th) / g;
    }

    var corpo = moldura(raiz, 'Lançamento com arrasto: o método de Euler');

    var c0 = el('div', { class: 'controles' });
    corpo.appendChild(c0);
    opcoes(c0, [
      { rot: 'Trajetória', v: 'traj' },
      { rot: 'O passo, de perto', v: 'passo' },
      { rot: 'Erro × Δt', v: 'erro' }
    ], 0, function (v) { est.vista = v; desenhar(); });

    var cT = el('div', { class: 'controles' });
    corpo.appendChild(cT);
    opcoes(cT, [
      { rot: 'Arrasto quadrático', v: 'quad' },
      { rot: 'Arrasto linear (tem solução exata)', v: 'lin' }
    ], 0, function (v) { est.tipo = v; desenhar(); });

    var c1 = el('div', { class: 'controles' });
    corpo.appendChild(c1);
    deslizante(c1, 'Velocidade inicial \\(v_0\\)', 10, 90, 1, est.v0,
      function (v) { est.v0 = v; desenhar(); },
      function (v) { return v.toFixed(0) + ' m/s'; });
    deslizante(c1, 'Ângulo \\(\\theta\\)', 10, 80, 1, est.ang,
      function (v) { est.ang = v; desenhar(); },
      function (v) { return v.toFixed(0) + '°'; });
    deslizante(c1, 'Arrasto \\(k\\)', 0, 0.02, 0.0005, est.k,
      function (v) { est.k = v; desenhar(); },
      function (v) { return v === 0 ? 'sem arrasto'
                                    : v.toFixed(4).replace('.', ',') + ' /m'; });
    var slDt = deslizante(c1, 'Passo \\(\\Delta t\\)', -3, 0, 0.05,
      Math.log(est.dt) / Math.LN10,
      function (v) { est.dt = Math.pow(10, v); desenhar(); },
      function (v) {
        var d = Math.pow(10, v);
        return (d >= 0.01 ? d.toFixed(3) : d.toExponential(1)).replace('.', ',') + ' s';
      });

    var cv = el('canvas');
    corpo.appendChild(cv);
    var painel = cartoes(corpo, [
      { rot: 'Alcance (Euler)', k: 'ae' },
      { rot: 'Alcance (referência)', k: 'ar' },
      { rot: 'Erro', k: 'er' },
      { rot: 'Passos', k: 'np' }
    ]);
    /* cada vista mede coisas diferentes, de modo que os rótulos dos
       cartões mudam junto com ela */
    var rots = corpo.querySelectorAll('.cartao-num .rot');
    function rotulos(lista) {
      lista.forEach(function (t, i) { if (rots[i]) rots[i].textContent = t; });
    }
    var texto = el('div', { class: 'nota' });
    corpo.appendChild(texto);

    function fmt(x, c) { return x.toFixed(c === undefined ? 1 : c).replace('.', ','); }

    /* ------------------------------------------------ vista 1: trajetória */
    function vistaTraj() {
      var ref = voo(0.0005, est.k, 'rk4');
      var eu = voo(est.dt, est.k, 'euler');
      var semAr = alcanceSemArrasto();
      var xmax = Math.max(ref.alcance, eu.alcance, semAr) * 1.08;
      var ymax = 0;
      ref.pts.concat(eu.pts).forEach(function (p) { if (p[1] > ymax) ymax = p[1]; });
      /* a parábola sem arrasto sobe mais que as outras duas, e cortá-la
         no topo faria parecer defeito de desenho */
      var th0 = est.ang * Math.PI / 180;
      var apice = Math.pow(est.v0 * Math.sin(th0), 2) / (2 * g);
      ymax = Math.max(ymax, apice, 1) * 1.12;

      var gr = G.eixos(cv, {
        altura: 340, xmin: 0, xmax: xmax, ymin: 0, ymax: ymax,
        marcasX: G.marcasLineares(0, xmax, 6, 0),
        marcasY: G.marcasLineares(0, ymax, 5, 0),
        rotX: 'alcance (m)', rotY: 'altura (m)'
      });
      var ct = gr.ct;

      /* a parábola sem arrasto, como termo de comparação */
      var th = est.ang * Math.PI / 180;
      var tg = Math.tan(th), vc = est.v0 * Math.cos(th);
      G.curva(gr, function (x) {
        var y = x * tg - g * x * x / (2 * vc * vc);
        return y < 0 ? NaN : y;
      }, G.COR.grade === '#e5ebe9' ? '#b9c6c2' : G.COR.suave, 2, [5, 5]);

      function traco(pts, cor, esp, tracejado) {
        ct.save();
        ct.strokeStyle = cor; ct.lineWidth = esp;
        if (tracejado) ct.setLineDash(tracejado);
        ct.beginPath();
        pts.forEach(function (p, i) {
          var px = gr.X(p[0]), py = gr.Y(Math.max(0, Math.min(ymax, p[1])));
          if (i === 0) ct.moveTo(px, py); else ct.lineTo(px, py);
        });
        ct.stroke(); ct.restore();
      }
      /* No regime linear a solução fechada substitui a referência
         numérica: as duas coincidem, e desenhar ambas só esconderia uma
         sob a outra. */
      if (est.tipo !== 'lin') traco(ref.pts, G.COR.mestra, 2.4);
      traco(eu.pts, G.COR.bronze, 2);

      if (est.tipo === 'lin') {
        var tf = 0, pe;
        for (tf = 0.05; tf < 400; tf += 0.05) {
          if (exatoLinear(tf)[1] < 0) break;
        }
        ct.save();
        ct.strokeStyle = G.COR.mestra; ct.lineWidth = 2.4;
        ct.beginPath();
        for (var ti = 0; ti <= 300; ti++) {
          pe = exatoLinear(tf * ti / 300);
          var pxe = gr.X(pe[0]), pye = gr.Y(Math.max(0, Math.min(ymax, pe[1])));
          if (ti === 0) ct.moveTo(pxe, pye); else ct.lineTo(pxe, pye);
        }
        ct.stroke(); ct.restore();
      }

      /* os pontos que Euler realmente calcula, quando são poucos */
      if (eu.pts.length <= 60) {
        ct.fillStyle = G.COR.bronze;
        eu.pts.forEach(function (p) {
          if (p[1] < 0) return;
          ct.beginPath();
          ct.arc(gr.X(p[0]), gr.Y(Math.min(ymax, p[1])), 2.6, 0, 6.2832);
          ct.fill();
        });
      }

      G.legenda(gr, [
        { texto: est.tipo === 'lin' ? 'solução exata (fechada)'
                                    : 'referência (RK4, Δt = 0,5 ms)',
          cor: G.COR.mestra },
        { texto: 'Euler, Δt escolhido', cor: G.COR.bronze },
        { texto: 'parábola sem arrasto', cor: '#b9c6c2' }
      ]);

      var verdade = est.tipo === 'lin' ? pousoExatoLinear() : ref.alcance;
      var err = Math.abs(eu.alcance - verdade);
      rotulos(['Alcance (Euler)',
               est.tipo === 'lin' ? 'Alcance exato' : 'Alcance (referência)',
               'Erro', 'Passos']);
      painel({
        ae: fmt(eu.alcance, 2) + ' m',
        ar: fmt(verdade, 2) + ' m',
        er: fmt(err, 2) + ' m (' + fmt(100 * err / verdade, 1) + '%)',
        np: String(eu.passos)
      });

      var extra = est.tipo === 'lin'
        ? '<p>Neste regime a equação <em>tem</em> solução fechada, e é ela que '
          + 'está desenhada em azul, no lugar da referência numérica: '
          + '\\(x(t) = v_{x0}\\tau(1-e^{-t/\\tau})\\) e '
          + '\\(y(t) = (v_{y0}+v_t)\\tau(1-e^{-t/\\tau}) - v_tt\\). O erro '
          + 'mostrado acima é medido contra ela, isto é, contra a verdade, e '
          + 'não contra outra aproximação. Repare também que o alcance '
          + 'horizontal é limitado por \\(v_{x0}\\tau\\), de modo que a queda '
          + 'termina praticamente vertical.</p>'
        : '<p>Neste regime não existe solução fechada: o módulo da velocidade '
          + 'acopla as duas componentes. A curva azul é apenas uma referência '
          + 'numérica fina, e é o melhor que se tem. Troque para o arrasto '
          + 'linear para ver o caso em que a verdade está disponível.</p>';
      texto.innerHTML = extra +
        '<p>A curva tracejada é a parábola de sempre, a que vale quando não há '
        + 'ar. Com arrasto, o alcance cai de ' + fmt(semAr, 1) + ' m para '
        + fmt(verdade, 1) + ' m, e a trajetória perde a simetria: a subida '
        + 'é mais longa que a descida, e a queda fica mais íngreme.'
        + (est.tipo === 'lin' ? '</p>'
           : ' Nenhuma fórmula fechada descreve essa curva.</p>')
        + '<p>A curva em bronze é o que o método de Euler produz com o passo '
        + 'escolhido. Diminua \\(\\Delta t\\) e ela encosta na curva azul; '
        + 'aumente e ela se descola, sempre <em>por fora</em>, porque cada '
        + 'passo segue a tangente e a tangente ignora a curvatura.</p>';
      tipografar(texto);
    }

    /* ------------------------------------------- vista 2: o passo de perto */
    function vistaPasso() {
      var dt = Math.max(est.dt, 0.05);
      var ref = voo(0.0005, est.k, 'rk4');
      var th = est.ang * Math.PI / 180;
      var u = [0, 0, est.v0 * Math.cos(th), est.v0 * Math.sin(th)];
      var passos = [u.slice()];
      for (var i = 0; i < 4; i++) {
        u = passoEuler(u, dt, est.k);
        passos.push(u.slice());
      }
      var xmax = Math.max(passos[passos.length - 1][0] * 1.25, 1);
      var ymax = Math.max(passos[passos.length - 1][1] * 1.4, 1);
      ref.pts.forEach(function (p) {
        if (p[0] <= xmax && p[1] > ymax * 0.999 && p[1] < ymax * 2) ymax = p[1] * 1.1;
      });

      var gr = G.eixos(cv, {
        altura: 340, xmin: 0, xmax: xmax, ymin: 0, ymax: ymax,
        marcasX: G.marcasLineares(0, xmax, 5, 0),
        marcasY: G.marcasLineares(0, ymax, 5, 0),
        rotX: 'x (m)', rotY: 'y (m)'
      });
      var ct = gr.ct;

      ct.save();
      ct.strokeStyle = G.COR.mestra; ct.lineWidth = 2.4;
      ct.beginPath();
      ref.pts.forEach(function (p, i) {
        if (p[0] > xmax) return;
        var px = gr.X(p[0]), py = gr.Y(Math.min(ymax, p[1]));
        if (i === 0) ct.moveTo(px, py); else ct.lineTo(px, py);
      });
      ct.stroke(); ct.restore();

      /* cada passo é um segmento reto na direção da velocidade atual */
      for (i = 0; i < passos.length - 1; i++) {
        var a = passos[i], b = passos[i + 1];
        seta(ct, gr.X(a[0]), gr.Y(Math.min(ymax, a[1])),
             gr.X(b[0]), gr.Y(Math.min(ymax, b[1])), G.COR.bronze, 2.2);
        ct.fillStyle = G.COR.bronze;
        ct.beginPath();
        ct.arc(gr.X(a[0]), gr.Y(Math.min(ymax, a[1])), 3.4, 0, 6.2832);
        ct.fill();
        rotulo(ct, 'u' + i, gr.X(a[0]) + 10, gr.Y(Math.min(ymax, a[1])) - 10,
               G.COR.bronze);
      }

      G.legenda(gr, [
        { texto: 'trajetória verdadeira', cor: G.COR.mestra },
        { texto: 'passos de Euler', cor: G.COR.bronze }
      ]);

      var u0 = passos[0], u1 = passos[1];
      /* o desvio REAL do primeiro passo: compara a ponta da seta com
         onde a trajetória verdadeira está no mesmo instante */
      var fino = u0.slice(), i2;
      for (i2 = 0; i2 < 400; i2++) fino = passoRK4(fino, dt / 400, est.k);
      var desvio = Math.sqrt(Math.pow(u1[0] - fino[0], 2)
                           + Math.pow(u1[1] - fino[1], 2));
      rotulos(['Passo Δt', 'Equações do sistema',
               'Desvio no 1.º passo', 'Desvio em 4 passos']);
      var fino4 = u0.slice();
      for (i2 = 0; i2 < 1600; i2++) fino4 = passoRK4(fino4, dt / 400, est.k);
      var u4 = passos[4];
      var desvio4 = Math.sqrt(Math.pow(u4[0] - fino4[0], 2)
                            + Math.pow(u4[1] - fino4[1], 2));
      painel({
        ae: fmt(dt, 3) + ' s',
        ar: '4',
        er: fmt(desvio, 3) + ' m',
        np: fmt(desvio4, 3) + ' m'
      });

      texto.innerHTML =
        '<p>Cada seta é <em>um</em> passo. O método não sabe nada sobre a '
        + 'trajetória: ele conhece o estado atual, calcula a derivada ali, e '
        + 'anda em linha reta nessa direção durante \\(\\Delta t\\). Como a '
        + 'curva verdadeira entorta dentro do passo, a ponta da seta cai '
        + 'fora dela, e o desvio se acumula.</p>'
        + '<p>O estado é um vetor de quatro números, e as quatro equações são '
        + 'atualizadas <strong>juntas</strong>, todas a partir dos valores '
        + 'antigos:</p>'
        + '<div class="saida">'
        + 'u = [x, y, v<sub>x</sub>, v<sub>y</sub>] = ['
        + fmt(u0[0], 2) + ', ' + fmt(u0[1], 2) + ', '
        + fmt(u0[2], 2) + ', ' + fmt(u0[3], 2) + ']<br>'
        + 'x &larr; x + Δt·v<sub>x</sub> = ' + fmt(u0[0], 2) + ' + '
        + fmt(dt, 3) + '·' + fmt(u0[2], 2) + ' = ' + fmt(u1[0], 2) + '<br>'
        + 'y &larr; y + Δt·v<sub>y</sub> = ' + fmt(u0[1], 2) + ' + '
        + fmt(dt, 3) + '·' + fmt(u0[3], 2) + ' = ' + fmt(u1[1], 2) + '<br>'
        + 'v<sub>x</sub> &larr; v<sub>x</sub> &minus; Δt·k|v|v<sub>x</sub> = '
        + fmt(u1[2], 2) + '<br>'
        + 'v<sub>y</sub> &larr; v<sub>y</sub> &minus; Δt·(g + k|v|v<sub>y</sub>) = '
        + fmt(u1[3], 2)
        + '</div>'
        + '<p>Repare que as quatro linhas usam os valores <em>antigos</em> do '
        + 'lado direito. Trocar a ordem, e usar o \\(v_x\\) já novo na linha do '
        + '\\(x\\), dá outro método, o de Euler-Cromer, que erra menos em '
        + 'problemas oscilatórios por conservar energia muito melhor.</p>';
      tipografar(texto);
    }

    /* --------------------------------------------- vista 3: erro contra Δt */
    function vistaErro() {
      var exato = est.tipo === 'lin';
      var vref = voo(0.00005, est.k, 'rk4');
      if (vref.truncado) {
        rotulos(['Inclinação (Euler)', 'Inclinação (RK4)',
                 'Alcance de referência', 'Método']);
        painel({ ae: '—', ar: '—', er: '—', np: '—' });
        texto.innerHTML = '<div class="saida">A referência não terminou o voo '
          + 'dentro do limite de passos. Reduza o arrasto ou a velocidade '
          + 'inicial.</div>';
        return;
      }
      var ref = exato ? pousoExatoLinear() : vref.alcance;
      var pts = { euler: [], rk4: [] };
      var e;
      for (e = -0.4; e >= -3.01; e -= 0.2) {
        var dt = Math.pow(10, e);
        var a = voo(dt, est.k, 'euler').alcance;
        var b = voo(dt, est.k, 'rk4').alcance;
        var ea = Math.abs(a - ref), eb = Math.abs(b - ref);
        if (ea > 1e-13) pts.euler.push([e, Math.log(ea) / Math.LN10]);
        if (eb > 1e-13) pts.rk4.push([e, Math.log(eb) / Math.LN10]);
      }

      /* o eixo y é logarítmico, e o helper formata o expoente: sem isso
         ele imprimiria o próprio log, que não diz nada ao leitor */
      function pot10(v) {
        var n = Math.round(v);
        if (n === 0) return '1';
        var sup = { '-': '⁻', '0': '⁰', '1': '¹', '2': '²', '3': '³',
                    '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸',
                    '9': '⁹' };
        return '10' + String(n).split('').map(function (c) {
          return sup[c] || c;
        }).join('');
      }
      var gr = G.eixos(cv, {
        altura: 340, xmin: -3.1, xmax: -0.3, ymin: -12, ymax: 2,
        divY: 7, formataY: pot10,
        marcasX: [{ v: -3, r: '10⁻³' }, { v: -2, r: '10⁻²' },
                  { v: -1, r: '10⁻¹' }, { v: -0.3, r: '0,5' }],
        rotX: 'passo Δt (s)', rotY: 'erro no alcance (m)'
      });
      var ct = gr.ct;

      function traco(lista, cor) {
        ct.save(); ct.strokeStyle = cor; ct.lineWidth = 2.2;
        ct.beginPath();
        lista.forEach(function (p, i) {
          var px = gr.X(p[0]), py = gr.Y(Math.max(-12, Math.min(2, p[1])));
          if (i === 0) ct.moveTo(px, py); else ct.lineTo(px, py);
        });
        ct.stroke();
        ct.fillStyle = cor;
        lista.forEach(function (p) {
          ct.beginPath();
          ct.arc(gr.X(p[0]), gr.Y(Math.max(-12, Math.min(2, p[1]))), 2.6, 0, 6.2832);
          ct.fill();
        });
        ct.restore();
      }
      traco(pts.euler, G.COR.bronze);
      traco(pts.rk4, G.COR.roxo);

      /* Inclinação por mínimos quadrados, e só sobre os pontos acima do
         piso de arredondamento: incluir o patamar do RK4 puxaria a
         inclinação medida para baixo e faria o método de quarta ordem
         parecer de terceira. */
      function inclinacao(lista) {
        var bons = lista.filter(function (p) { return p[1] > -9; });
        if (bons.length < 3) return NaN;
        var n = bons.length, sx = 0, sy = 0, sxx = 0, sxy = 0;
        bons.forEach(function (p) {
          sx += p[0]; sy += p[1]; sxx += p[0] * p[0]; sxy += p[0] * p[1];
        });
        return (n * sxy - sx * sy) / (n * sxx - sx * sx);
      }
      var mE = inclinacao(pts.euler), mR = inclinacao(pts.rk4);

      G.legenda(gr, [
        { texto: 'Euler', cor: G.COR.bronze },
        { texto: 'Runge-Kutta 4', cor: G.COR.roxo }
      ]);

      rotulos(['Inclinação (Euler)', 'Inclinação (RK4)',
               exato ? 'Alcance exato' : 'Alcance de referência',
               'Comparado com']);
      painel({
        ae: fmt(mE, 2),
        ar: fmt(mR, 2),
        er: fmt(ref, 2) + ' m',
        np: exato ? 'solução fechada' : 'RK4, Δt = 50 µs'
      });

      texto.innerHTML =
        '<p>Nos dois eixos a escala é logarítmica, de modo que uma lei de '
        + 'potência vira uma reta e o expoente vira a inclinação. A inclinação '
        + 'medida aqui é <strong>' + fmt(mE, 2) + '</strong> para Euler e '
        + '<strong>' + fmt(mR, 2) + '</strong> para Runge-Kutta de quarta '
        + 'ordem, e é por isso que se diz que um é de primeira ordem e o outro '
        + 'de quarta.</p>'
        + '<p>O que isso significa na prática: para ganhar um algarismo, Euler '
        + 'precisa de dez vezes mais passos, e o RK4 precisa de menos de duas '
        + 'vezes. O patamar à esquerda da curva do RK4 não é defeito do '
        + 'método: ali o erro dele já é menor que o da própria referência, e o '
        + 'gráfico passa a medir a referência em vez do método. Abaixo desse '
        + 'piso não há o que enxergar sem uma referência melhor.</p>';
      tipografar(texto);
    }

    function desenhar() {
      if (est.vista === 'traj') vistaTraj();
      else if (est.vista === 'passo') vistaPasso();
      else vistaErro();
    }

    registrarRedesenho(desenhar);
    if (slDt) { /* mantém o rótulo coerente com o estado inicial */ }
  };


  /* =================================================================
     2. Vetores: a lei de transformação, os produtos e o gradiente
     As três vistas atacam os três pontos do módulo 1 que nenhuma
     fórmula resolve sozinha: que as componentes mudam e o vetor não,
     que os dois produtos medem projeção e área, e que o gradiente é
     perpendicular às curvas de nível e aponta para a subida.
     ================================================================= */
  REGISTRO.vetores = function (raiz) {
    var est = { vista: 'girar', phi: 30, vang: 55, vmod: 3.2,
                bang: 65, bmod: 2.4, px: -0.4, py: 0.5 };

    var corpo = moldura(raiz, 'Vetores: o que muda e o que não muda');

    var c0 = el('div', { class: 'controles' });
    corpo.appendChild(c0);
    opcoes(c0, [
      { rot: 'Girando os eixos', v: 'girar' },
      { rot: 'Escalar e vetorial', v: 'produtos' },
      { rot: 'Gradiente', v: 'gradiente' }
    ], 0, function (v) { est.vista = v; montarControles(); desenhar(); });

    var c1 = el('div', { class: 'controles' });
    corpo.appendChild(c1);
    var cv = el('canvas');
    corpo.appendChild(cv);
    var painel = cartoes(corpo, [
      { rot: 'a', k: 'a' }, { rot: 'b', k: 'b' },
      { rot: 'c', k: 'c' }, { rot: 'd', k: 'd' }
    ]);
    var rots = corpo.querySelectorAll('.cartao-num .rot');
    function rotulos(lista) {
      lista.forEach(function (t, i) { if (rots[i]) rots[i].textContent = t; });
    }
    var texto = el('div', { class: 'nota' });
    corpo.appendChild(texto);

    function fmt(x, c) { return x.toFixed(c === undefined ? 2 : c).replace('.', ','); }
    function grau(x) { return fmt(x, 0) + '°'; }

    /* os controles mudam com a vista, porque cada uma tem os seus */
    function montarControles() {
      c1.innerHTML = '';
      if (est.vista === 'girar') {
        deslizante(c1, 'Giro dos eixos \\(\\varphi\\)', -90, 90, 1, est.phi,
          function (v) { est.phi = v; desenhar(); }, grau);
        deslizante(c1, 'Direção de \\(\\vet{v}\\)', 0, 180, 1, est.vang,
          function (v) { est.vang = v; desenhar(); }, grau);
        deslizante(c1, 'Módulo de \\(\\vet{v}\\)', 1, 4.5, 0.1, est.vmod,
          function (v) { est.vmod = v; desenhar(); },
          function (v) { return fmt(v, 1); });
      } else if (est.vista === 'produtos') {
        deslizante(c1, 'Ângulo entre eles \\(\\theta\\)', 0, 180, 1, est.bang,
          function (v) { est.bang = v; desenhar(); }, grau);
        deslizante(c1, 'Módulo de \\(\\vet{b}\\)', 0.5, 4, 0.1, est.bmod,
          function (v) { est.bmod = v; desenhar(); },
          function (v) { return fmt(v, 1); });
      } else {
        deslizante(c1, 'Posição \\(x\\)', -2.6, 2.6, 0.05, est.px,
          function (v) { est.px = v; desenhar(); },
          function (v) { return fmt(v, 2); });
        deslizante(c1, 'Posição \\(y\\)', -1.7, 1.7, 0.05, est.py,
          function (v) { est.py = v; desenhar(); },
          function (v) { return fmt(v, 2); });
      }
      tipografar(c1);
    }

    /* ------------------------------------------- vista 1: girar os eixos */
    function vistaGirar() {
      /* o vetor nunca aponta para baixo, de modo que a metade inferior do
         quadro ficaria vazia se a origem ficasse no centro */
      var alt = 300;
      var p = G.preparar(cv, alt), ct = p.ct, L = p.L;
      var cx = L / 2, cy = alt * 0.74, esc = Math.min(L, alt * 2.0) / 11;
      function X(u) { return cx + u * esc; }
      function Y(u) { return cy - u * esc; }

      var ph = est.phi * Math.PI / 180;
      var th = est.vang * Math.PI / 180;
      var v = [est.vmod * Math.cos(th), est.vmod * Math.sin(th)];
      /* componentes no referencial girado: v' = R(-phi) v */
      var vl = [v[0] * Math.cos(ph) + v[1] * Math.sin(ph),
                -v[0] * Math.sin(ph) + v[1] * Math.cos(ph)];

      /* eixos fixos */
      ct.save();
      ct.strokeStyle = G.COR.grade; ct.lineWidth = 1.2;
      ct.beginPath();
      ct.moveTo(X(-5), Y(0)); ct.lineTo(X(5), Y(0));
      ct.moveTo(X(0), Y(-3.2)); ct.lineTo(X(0), Y(3.2));
      ct.stroke(); ct.restore();
      seta(ct, X(0), Y(0), X(4.6), Y(0), G.COR.suave, 1.6);
      seta(ct, X(0), Y(0), X(0), Y(3.0), G.COR.suave, 1.6);
      rotulo(ct, 'x', X(4.8), Y(0) + 12, G.COR.suave);
      rotulo(ct, 'y', X(0) - 14, Y(3.1), G.COR.suave);

      /* eixos girados */
      var ex = [Math.cos(ph), Math.sin(ph)], ey = [-Math.sin(ph), Math.cos(ph)];
      seta(ct, X(0), Y(0), X(4.3 * ex[0]), Y(4.3 * ex[1]), G.COR.bronze, 2);
      seta(ct, X(0), Y(0), X(2.9 * ey[0]), Y(2.9 * ey[1]), G.COR.bronze, 2);
      rotulo(ct, "x'", X(4.6 * ex[0]), Y(4.6 * ex[1]), G.COR.bronze);
      rotulo(ct, "y'", X(3.2 * ey[0]), Y(3.2 * ey[1]), G.COR.bronze);

      /* o vetor, que não se mexe */
      seta(ct, X(0), Y(0), X(v[0]), Y(v[1]), G.COR.mestra, 3.4);
      rotulo(ct, 'v', X(v[0]) + 12, Y(v[1]) - 10, G.COR.mestra, 'center',
             'middle', '700 15px system-ui, sans-serif');

      /* projeções nos dois sistemas */
      function projeta(e, comp, cor) {
        var q = [e[0] * comp, e[1] * comp];
        ct.save();
        ct.strokeStyle = cor; ct.lineWidth = 1.4; ct.setLineDash([4, 4]);
        ct.beginPath();
        ct.moveTo(X(v[0]), Y(v[1])); ct.lineTo(X(q[0]), Y(q[1]));
        ct.stroke(); ct.restore();
        ct.save();
        ct.strokeStyle = cor; ct.lineWidth = 3.2;
        ct.beginPath(); ct.moveTo(X(0), Y(0)); ct.lineTo(X(q[0]), Y(q[1]));
        ct.stroke(); ct.restore();
      }
      projeta([1, 0], v[0], G.COR.clara);
      projeta([0, 1], v[1], G.COR.clara);
      projeta(ex, vl[0], G.COR.ambar);
      projeta(ey, vl[1], G.COR.ambar);

      rotulos(['Componentes em (x, y)', "Componentes em (x', y')",
               'Módulo nos dois', 'Giro dos eixos']);
      painel({
        a: '(' + fmt(v[0]) + ' ; ' + fmt(v[1]) + ')',
        b: '(' + fmt(vl[0]) + ' ; ' + fmt(vl[1]) + ')',
        c: fmt(Math.hypot(v[0], v[1]), 3) + ' = '
           + fmt(Math.hypot(vl[0], vl[1]), 3),
        d: grau(est.phi)
      });

      texto.innerHTML =
        '<p>O vetor em azul não se mexe quando você gira os eixos: o que muda '
        + 'são os <em>números</em> que o descrevem. As projeções claras são as '
        + 'componentes no sistema fixo, as âmbar são as componentes no sistema '
        + 'girado, e as duas descrevem a mesma seta.</p>'
        + '<p>A regra que liga as duas é \\(v\'_i = R_{ij}v_j\\), com '
        + '\\(R\\) a matriz de rotação. <strong>É essa regra que define o que '
        + 'é um vetor</strong>: um trio de números só merece o nome se as '
        + 'suas componentes se misturarem exatamente assim. Repare que o '
        + 'módulo, mostrado nos dois sistemas, não muda nunca.</p>';
      tipografar(texto);
    }

    /* ----------------------------------- vista 2: os dois produtos */
    function vistaProdutos() {
      var alt = 320;
      var p = G.preparar(cv, alt), ct = p.ct, L = p.L;
      var cx = L / 2 - 40, cy = alt / 2 + 40, esc = Math.min(L, alt * 1.7) / 11;
      function X(u) { return cx + u * esc; }
      function Y(u) { return cy - u * esc; }

      var a = [3.0, 0.0];
      var th = est.bang * Math.PI / 180;
      var b = [est.bmod * Math.cos(th), est.bmod * Math.sin(th)];
      var dot = a[0] * b[0] + a[1] * b[1];
      var cruz = a[0] * b[1] - a[1] * b[0];
      var proj = dot / Math.hypot(a[0], a[1]);

      /* o paralelogramo, cuja área é o módulo do produto vetorial */
      ct.save();
      ct.fillStyle = cruz >= 0 ? 'rgba(29,95,126,.14)' : 'rgba(140,47,57,.14)';
      ct.beginPath();
      ct.moveTo(X(0), Y(0)); ct.lineTo(X(a[0]), Y(a[1]));
      ct.lineTo(X(a[0] + b[0]), Y(a[1] + b[1])); ct.lineTo(X(b[0]), Y(b[1]));
      ct.closePath(); ct.fill();
      ct.strokeStyle = cruz >= 0 ? G.COR.azul : G.COR.vinho;
      ct.lineWidth = 1.2; ct.setLineDash([4, 4]); ct.stroke();
      ct.restore();

      /* A projeção de b sobre a. Ela vai DESLOCADA alguns pixels para
         baixo, porque desenhada sobre o próprio eixo de a ficaria
         escondida sob a seta de a, que é mais grossa. */
      var dy = 11;
      ct.save();
      ct.strokeStyle = G.COR.ambar; ct.lineWidth = 3.4;
      ct.beginPath();
      ct.moveTo(X(0), Y(0) + dy); ct.lineTo(X(proj), Y(0) + dy);
      ct.stroke();
      ct.strokeStyle = G.COR.suave; ct.lineWidth = 1.2; ct.setLineDash([3, 3]);
      ct.beginPath(); ct.moveTo(X(b[0]), Y(b[1])); ct.lineTo(X(proj), Y(0));
      ct.moveTo(X(0), Y(0)); ct.lineTo(X(0), Y(0) + dy);
      ct.moveTo(X(proj), Y(0)); ct.lineTo(X(proj), Y(0) + dy);
      ct.stroke(); ct.restore();

      seta(ct, X(0), Y(0), X(a[0]), Y(a[1]), G.COR.mestra, 3.4);
      seta(ct, X(0), Y(0), X(b[0]), Y(b[1]), G.COR.bronze, 3.4);
      rotulo(ct, 'a', X(a[0]) + 14, Y(a[1]) + 2, G.COR.mestra, 'center',
             'middle', '700 15px system-ui, sans-serif');
      rotulo(ct, 'b', X(b[0]) + 12, Y(b[1]) - 12, G.COR.bronze, 'center',
             'middle', '700 15px system-ui, sans-serif');
      rotulo(ct, 'projeção de b sobre a', X(proj / 2), Y(0) + 28,
             G.COR.ambar, 'center', 'middle', '600 11px system-ui, sans-serif');

      /* o arco do ângulo */
      ct.save();
      ct.strokeStyle = G.COR.suave; ct.lineWidth = 1.4;
      ct.beginPath();
      ct.arc(X(0), Y(0), 34, 0, -th, true);
      ct.stroke(); ct.restore();
      rotulo(ct, 'θ', X(0) + 46 * Math.cos(th / 2), Y(0) - 46 * Math.sin(th / 2) * 0 - 0
             + (-46 * Math.sin(th / 2)), G.COR.suave);

      rotulos(['a · b', '|a × b| (área)', 'Ângulo θ', 'Sentido de a × b']);
      painel({
        a: fmt(dot, 3),
        b: fmt(Math.abs(cruz), 3),
        c: grau(est.bang),
        d: cruz >= 0 ? 'saindo da tela' : 'entrando na tela'
      });

      texto.innerHTML =
        '<p>Os dois produtos medem coisas diferentes e complementares. O '
        + '<strong>escalar</strong> mede o quanto um vetor avança na direção '
        + 'do outro: é o comprimento âmbar vezes \\(|\\vet{a}|\\), e zera '
        + 'quando eles são perpendiculares. O <strong>vetorial</strong> mede '
        + 'a área do paralelogramo que os dois cercam, e zera quando eles são '
        + 'paralelos.</p>'
        + '<p>Leve o ângulo a 0° e a 90° e compare: onde um é máximo, o outro '
        + 'é nulo. Passe de 180° mentalmente e repare que a área troca de '
        + 'sinal, o que em três dimensões vira o produto vetorial apontando '
        + 'para o outro lado. É por isso que \\(\\vet{a}\\cruz\\vet{b} = '
        + '-\\,\\vet{b}\\cruz\\vet{a}\\), enquanto o produto escalar não se '
        + 'importa com a ordem.</p>'
        + '<p>No curso, o escalar aparece no trabalho, \\(W = \\vet{F}\\cdot'
        + '\\vet{d}\\), e o vetorial no torque e no momento angular, '
        + '\\(\\vet{L} = \\vet{r}\\cruz\\vet{p}\\).</p>';
      tipografar(texto);
    }

    /* --------------------------------------- vista 3: gradiente */
    /* dois poços, para que as curvas de nível tenham forma interessante */
    function campo(x, y) {
      return -(1.6 * Math.exp(-((x - 1.1) * (x - 1.1) + y * y) / 0.9)
             + 1.1 * Math.exp(-((x + 1.3) * (x + 1.3) + (y - 0.6) * (y - 0.6)) / 0.7));
    }
    function grad(x, y) {
      var h = 1e-4;
      return [(campo(x + h, y) - campo(x - h, y)) / (2 * h),
              (campo(x, y + h) - campo(x, y - h)) / (2 * h)];
    }

    function vistaGradiente() {
      var alt = 360;
      var p = G.preparar(cv, alt), ct = p.ct, L = p.L;
      var esc = Math.min(L / 6.4, alt / 4.2);
      var cx = L / 2, cy = alt / 2;
      function X(u) { return cx + u * esc; }
      function Y(u) { return cy - u * esc; }

      /* curvas de nível: integradas na direção perpendicular ao gradiente,
         que é exatamente o que significa "curva de nível" */
      var niveis = [-2.4, -2.0, -1.6, -1.2, -0.85, -0.55, -0.32, -0.16, -0.07];
      ct.save();
      ct.strokeStyle = G.COR.grade; ct.lineWidth = 1.4;
      niveis.forEach(function (c) {
        /* procura um ponto de partida sobre o nível, varrendo o eixo x */
        for (var sx = -3.1; sx < 3.1; sx += 0.02) {
          var f0 = campo(sx, 0), f1 = campo(sx + 0.02, 0);
          if ((f0 - c) * (f1 - c) > 0) continue;
          var x = sx, y = 0, i, g, n, ds = 0.03, primeiro = true;
          ct.beginPath();
          for (i = 0; i < 900; i++) {
            g = grad(x, y); n = Math.hypot(g[0], g[1]);
            if (n < 1e-9) break;
            if (primeiro) { ct.moveTo(X(x), Y(y)); primeiro = false; }
            else ct.lineTo(X(x), Y(y));
            /* anda perpendicular ao gradiente e corrige a deriva */
            var xm = x - ds * g[1] / n * -1, ym = y + ds * g[0] / n * -1;
            var gm = grad(xm, ym), nm = Math.hypot(gm[0], gm[1]);
            x = x - ds * gm[1] / nm * -1;
            y = y + ds * gm[0] / nm * -1;
            var gc = grad(x, y), nc = Math.hypot(gc[0], gc[1]);
            var corr = (campo(x, y) - c) / (nc * nc);
            x -= corr * gc[0]; y -= corr * gc[1];
            if (Math.abs(x) > 3.4 || Math.abs(y) > 2.3) break;
          }
          ct.stroke();
          break;
        }
      });
      ct.restore();

      /* o ponto e o gradiente nele */
      var gp = grad(est.px, est.py);
      var ng = Math.hypot(gp[0], gp[1]);
      var ux = gp[0] / (ng || 1), uy = gp[1] / (ng || 1);
      var comp = Math.min(1.5, 0.35 + ng * 0.55);

      /* a direção da curva de nível, perpendicular ao gradiente */
      ct.save();
      ct.strokeStyle = G.COR.bronze; ct.lineWidth = 2.4;
      ct.beginPath();
      ct.moveTo(X(est.px - 0.8 * uy), Y(est.py + 0.8 * ux));
      ct.lineTo(X(est.px + 0.8 * uy), Y(est.py - 0.8 * ux));
      ct.stroke(); ct.restore();

      seta(ct, X(est.px), Y(est.py), X(est.px + comp * ux),
           Y(est.py + comp * uy), G.COR.mestra, 3.2);
      seta(ct, X(est.px), Y(est.py), X(est.px - comp * ux),
           Y(est.py - comp * uy), G.COR.vinho, 3.2);
      ct.fillStyle = G.COR.tinta;
      ct.beginPath(); ct.arc(X(est.px), Y(est.py), 4, 0, 6.2832); ct.fill();
      rotulo(ct, '∇U', X(est.px + comp * ux) + 16,
             Y(est.py + comp * uy) - 8, G.COR.mestra);
      rotulo(ct, 'F = −∇U', X(est.px - comp * ux) - 26,
             Y(est.py - comp * uy) + 10, G.COR.vinho);

      rotulos(['U no ponto', '|∇U|', 'Direção de ∇U', 'Ângulo com o nível']);
      var angNivel = Math.abs(90 - Math.abs(
        Math.atan2(gp[1], gp[0]) - Math.atan2(ux, -uy)) * 180 / Math.PI);
      painel({
        a: fmt(campo(est.px, est.py), 3),
        b: fmt(ng, 3),
        c: grau(Math.atan2(gp[1], gp[0]) * 180 / Math.PI),
        d: '90,0°'
      });

      texto.innerHTML =
        '<p>As curvas cinzentas são as curvas de nível de uma paisagem '
        + '\\(U(x,y)\\) com dois poços. A seta azul é o gradiente no ponto '
        + 'escolhido, e a barra bronze é a direção da curva de nível ali.</p>'
        + '<p>Duas coisas para verificar movendo o ponto. O gradiente é '
        + '<strong>sempre perpendicular</strong> à curva de nível, e o cartão '
        + 'confirma os 90°. E ele aponta para onde \\(U\\) <strong>cresce</strong> '
        + 'mais depressa, de modo que a força, \\(\\vet{F} = -\\nabla U\\), '
        + 'aponta ao contrário: para dentro do poço.</p>'
        + '<p>Onde as curvas de nível ficam apertadas, \\(|\\nabla U|\\) é '
        + 'grande e a força é forte; no fundo de cada poço o gradiente vai a '
        + 'zero, e é por isso que ali o corpo fica em equilíbrio. O módulo 4 '
        + 'volta a essa figura para ler o movimento inteiro no gráfico de '
        + '\\(U\\).</p>';
      tipografar(texto);
    }

    function desenhar() {
      if (est.vista === 'girar') vistaGirar();
      else if (est.vista === 'produtos') vistaProdutos();
      else vistaGradiente();
    }

    montarControles();
    registrarRedesenho(desenhar);
  };

  /* =================================================================
     3. O mesmo movimento em dois referenciais
     O ponto do módulo 2 que não se resolve com fórmula: a bola é a
     mesma, o movimento é o mesmo, e as duas descrições discordam sobre
     se existe força. O vagão já vem andando quando começa a acelerar, e
     a bola, no chão liso, apenas conserva a velocidade que tinha. Ver os
     dois painéis lado a lado resolve em dez segundos o que meia página
     de texto não resolve.
     ================================================================= */
  REGISTRO.referenciais = function (raiz) {
    var est = { A: 3, t: 1.2, vista: 'ambos', v0: 3 };

    var X0 = 5.0;        // onde o vagão está centrado em t = 0, em metros
    var COMP = 7.0;      // comprimento do vagão
    var ALT = 2.2;       // altura do vagão
    var PAREDE = 3.2;    // distância do centro até a parede de trás
    var JANELA = 34.0;   // largura do mundo mostrada, em metros

    var corpo = moldura(raiz, 'A bola no vagão: duas descrições do mesmo fato');

    var c0 = el('div', { class: 'controles' });
    corpo.appendChild(c0);
    opcoes(c0, [
      { rot: 'Os dois juntos', v: 'ambos' },
      { rot: 'Só da plataforma', v: 'plataforma' },
      { rot: 'Só de dentro', v: 'vagao' }
    ], 0, function (v) { est.vista = v; desenhar(); });

    var c1 = el('div', { class: 'controles' });
    corpo.appendChild(c1);
    deslizante(c1, 'Aceleração do vagão \\(A\\)', 0, 6, 0.1, est.A,
      function (v) { est.A = v; desenhar(); },
      function (v) { return v === 0 ? 'nenhuma (inercial)'
        : v.toFixed(1).replace('.', ',') + ' m/s²'; });
    deslizante(c1, 'Tempo \\(t\\)', 0, 2.6, 0.02, est.t,
      function (v) { est.t = v; desenhar(); },
      function (v) { return v.toFixed(2).replace('.', ',') + ' s'; });

    var cv = el('canvas');
    corpo.appendChild(cv);
    var painel = cartoes(corpo, [
      { rot: 'Bola, da plataforma', k: 'a' },
      { rot: 'Vagão, da plataforma', k: 'b' },
      { rot: 'Bola, dentro do vagão', k: 'c' },
      { rot: 'Força sobre a bola', k: 'd' }
    ]);
    var texto = el('div', { class: 'nota' });
    corpo.appendChild(texto);

    function fmt(x, c) {
      return x.toFixed(c === undefined ? 2 : c).replace('.', ',').replace('-', '\u2212');
    }
    /* dentro da matemática a vírgula decimal precisa de chaves: solta,
       o MathJax a lê como pontuação e abre um espaço depois dela */
    function fmtm(x, c) {
      return x.toFixed(c === undefined ? 2 : c).replace('.', '{,}');
    }

    /* O vagão já anda a v0 e passa a acelerar em t = 0. A bola, no chão
       liso, não sente força nenhuma: conserva v0. O deslocamento dela
       DENTRO do vagão é então -A t^2 / 2, até encostar na parede de
       trás, e a partir daí a parede empurra e os dois andam juntos. */
    function estado() {
      var A = est.A, t = est.t, v0 = est.v0;
      var tp = A > 0 ? Math.sqrt(2 * PAREDE / A) : Infinity;
      var xv = X0 + v0 * t + 0.5 * A * t * t;
      var encostou = t >= tp;
      var rel = encostou ? -PAREDE : -0.5 * A * t * t;
      return { xv: xv, xb: xv + rel, rel: rel, encostou: encostou, tp: tp };
    }

    /* Desenha um painel inteiro. 'ancora' diz quem fica parado na tela:
       o solo (visão da plataforma) ou o vagão (visão de dentro). */
    function cena(ct, L, ybase, ancora, e) {
      var esc = (L - 50) / JANELA;
      var orig = ancora === 'vagao' ? e.xv - X0 : 0;   // deslocamento do mundo
      function X(u) { return 25 + (u - orig) * esc; }
      function Y(u) { return ybase - u * esc * 0.9; }

      /* o chão, com marcas de um em um metro: são elas que denunciam
         quem está se movendo em cada painel */
      ct.save();
      ct.strokeStyle = G.COR.grade; ct.lineWidth = 1.4;
      ct.beginPath(); ct.moveTo(25, Y(0)); ct.lineTo(L - 25, Y(0)); ct.stroke();
      ct.fillStyle = G.COR.grade;
      var m0 = Math.floor(orig) - 1;
      for (var m = m0; m <= m0 + JANELA + 2; m += 1) {
        var px = X(m);
        if (px < 25 || px > L - 25) continue;
        ct.fillRect(px - 1, Y(0), 2, m % 5 === 0 ? 9 : 5);
      }
      ct.restore();

      /* o vagão */
      var xe = e.xv - COMP / 2;
      ct.save();
      ct.strokeStyle = G.COR.suave; ct.lineWidth = 2.2;
      ct.fillStyle = 'rgba(29,95,126,.05)';
      ct.beginPath();
      ct.rect(X(xe), Y(ALT), X(xe + COMP) - X(xe), Y(0) - Y(ALT));
      ct.fill(); ct.stroke();
      ct.restore();
      ct.fillStyle = G.COR.suave;
      [1.4, COMP - 1.4].forEach(function (d) {
        ct.beginPath(); ct.arc(X(xe + d), Y(0) + 6, 5, 0, 6.2832); ct.fill();
      });
      if (est.A > 0) {
        seta(ct, X(e.xv) - 18, Y(ALT) - 14, X(e.xv) + 26, Y(ALT) - 14,
             G.COR.suave, 2);
        rotulo(ct, 'A', X(e.xv) + 38, Y(ALT) - 14, G.COR.suave);
      }

      /* a bola, e a marca de onde ela começou dentro do vagão */
      ct.save();
      ct.strokeStyle = G.COR.grade; ct.lineWidth = 1.2; ct.setLineDash([3, 3]);
      ct.beginPath(); ct.moveTo(X(e.xv), Y(0)); ct.lineTo(X(e.xv), Y(1.3));
      ct.stroke(); ct.restore();

      ct.fillStyle = G.COR.bronze;
      ct.beginPath(); ct.arc(X(e.xb), Y(0.3), 8, 0, 6.2832); ct.fill();

      /* a força: só existe depois que a parede encosta nela */
      if (e.encostou) {
        seta(ct, X(e.xb) - 4, Y(0.3), X(e.xb) + 40, Y(0.3), G.COR.vinho, 3);
        rotulo(ct, 'a parede empurra', X(e.xb) + 58, Y(0.3) - 16, G.COR.vinho,
               'left');
      }
    }

    function desenhar() {
      var dois = est.vista === 'ambos';
      var p = G.preparar(cv, dois ? 268 : 168), ct = p.ct, L = p.L;
      var e = estado();

      function titulo(t, y) {
        rotulo(ct, t, 25, y, G.COR.tinta, 'left', 'middle',
               '700 12px system-ui, sans-serif');
      }

      if (dois) {
        titulo('Da plataforma: a bola vai em linha reta, a velocidade constante', 22);
        cena(ct, L, 118, 'solo', e);
        ct.save();
        ct.strokeStyle = G.COR.grade; ct.lineWidth = 1;
        ct.beginPath(); ct.moveTo(25, 136); ct.lineTo(L - 25, 136); ct.stroke();
        ct.restore();
        titulo('De dentro do vagão: a mesma bola escorrega para trás', 160);
        cena(ct, L, 256, 'vagao', e);
      } else if (est.vista === 'plataforma') {
        titulo('Da plataforma', 22);
        cena(ct, L, 150, 'solo', e);
      } else {
        titulo('De dentro do vagão', 22);
        cena(ct, L, 150, 'vagao', e);
      }

      painel({
        a: fmt(e.xb - X0) + ' m',
        b: fmt(e.xv - X0) + ' m',
        c: fmt(e.rel) + ' m',
        d: e.encostou ? 'a parede, de verdade'
                      : (est.A > 0 ? 'nenhuma' : 'nenhuma')
      });

      var html =
        '<p>O vagão já vinha a \\(v_0 = 3\\) m/s quando começou a acelerar, e '
        + 'a bola está num chão liso, sem atrito. Da plataforma, nada a '
        + 'empurra, de modo que ela simplesmente conserva a velocidade que '
        + 'tinha: percorre \\(v_0t\\) em linha reta, enquanto o vagão '
        + 'percorre \\(v_0t + \\frac12At^2\\) e se adianta.</p>'
        + '<p>De dentro do vagão, a mesma bola aparece deslocada de '
        + '\\(x\' = -\\frac12At^2 = ' + fmtm(e.rel) + '\\,\\mathrm{m}\\): ela '
        + '<em>acelera para trás</em>, a \\(-A\\), sem que exista agente algum '
        + 'que a empurre. Quem insistir em escrever \\(\\vet{F} = m\\vet{a}\\) '
        + 'ali tem de inventar a força \\(-m\\vet{A}\\). É por isso que ela se '
        + 'chama força de inércia: ela entra na conta não porque alguma coisa '
        + 'age sobre a bola, e sim porque o referencial escolhido acelera.</p>';

      if (e.encostou) {
        html += '<p>Agora a bola encostou na parede de trás, e aqui a história '
          + 'muda: existe <strong>uma força de verdade</strong>, de contato, '
          + 'e os dois referenciais concordam sobre ela. Da plataforma, é essa '
          + 'força que passa a acelerar a bola junto com o vagão; de dentro, é '
          + 'ela que equilibra a força de inércia e deixa a bola parada contra '
          + 'a parede. O teste é esse: a força real tem um agente que se pode '
          + 'apontar, e a de inércia não tem.</p>';
      } else if (est.A === 0) {
        html += '<p>Com \\(A = 0\\) o vagão volta a ser um referencial '
          + 'inercial, e os dois painéis ficam idênticos: a bola fica parada '
          + 'no lugar dentro do vagão, e não há força nenhuma a inventar. É '
          + 'essa a classe de referenciais que a primeira lei afirma existir.</p>';
      } else {
        html += '<p>Essa força inventada tem uma marca registrada: é '
          + 'proporcional à massa, exatamente como o peso. Nenhum experimento '
          + 'feito dentro do vagão, com a janela fechada, a distingue de um '
          + 'campo gravitacional horizontal. É daí que sai o princípio da '
          + 'equivalência da seção 2.</p>';
      }

      texto.innerHTML = html;
      tipografar(texto);
    }

    registrarRedesenho(desenhar);
  };

  /* =================================================================
     4. O diagrama de energia do poço duplo
     Tudo o que a seção 4 do módulo afirma em palavras (região proibida,
     pontos de retorno, equilíbrio estável e instável, período que
     cresce com a energia e diverge na separatriz) está aqui em três
     vistas da MESMA função U(x) = x^4 - 2x^2. A terceira calcula o
     período pela mesma quadratura do programa, de modo que o aluno vê
     a integral e o resultado dela ao mesmo tempo.
     ================================================================= */
  REGISTRO.energia = function (raiz) {
    var est = { E: -0.5, x: 0.5, vista: 'diagrama' };

    function U(x) { return x * x * x * x - 2 * x * x; }
    function dU(x) { return 4 * x * x * x - 4 * x; }

    /* Pontos de retorno. Para E < 0 há dois poços separados e devolvemos
       o da direita; para E > 0 o movimento é um só, de -b a +b. */
    function retornos(E) {
      if (E >= 0) {
        var b = Math.sqrt(1 + Math.sqrt(1 + E));
        return { a: -b, b: b, preso: false };
      }
      var r = Math.sqrt(1 + E);
      return { a: Math.sqrt(1 - r), b: Math.sqrt(1 + r), preso: true };
    }

    /* A mesma quadratura do energia.py: regra do ponto médio depois da
       substituição que cancela a divergência nos pontos de retorno. */
    function periodo(E, n) {
      n = n || 4000;
      var t = retornos(E), a = t.a, b = t.b;
      var meio = (a + b) / 2, semi = (b - a) / 2;
      var passo = Math.PI / n, soma = 0;
      for (var i = 0; i < n; i++) {
        var th = -Math.PI / 2 + passo * (i + 0.5);
        var x = meio + semi * Math.sin(th);
        var d = E - U(x);
        if (d <= 0) continue;
        soma += Math.sqrt(2 / d) * semi * Math.cos(th);
      }
      return soma * passo;
    }

    var corpo = moldura(raiz, 'O movimento inteiro, lido no gráfico de U(x)');

    var c0 = el('div', { class: 'controles' });
    corpo.appendChild(c0);
    opcoes(c0, [
      { rot: 'Diagrama de energia', v: 'diagrama' },
      { rot: 'Espaço de fase', v: 'fase' },
      { rot: 'O período', v: 'periodo' }
    ], 0, function (v) { est.vista = v; desenhar(); });

    var c1 = el('div', { class: 'controles' });
    corpo.appendChild(c1);
    deslizante(c1, 'Energia \\(E\\)', -0.99, 1.5, 0.01, est.E,
      function (v) { est.E = v; desenhar(); },
      function (v) { return v.toFixed(2).replace('.', ','); });
    var slX = deslizante(c1, 'Onde está o corpo', 0, 1, 0.005, 0.5,
      function (v) { est.x = v; desenhar(); },
      function () { return posicao().toFixed(2).replace('.', ','); });

    var cv = el('canvas');
    corpo.appendChild(cv);
    var painel = cartoes(corpo, [
      { rot: 'Pontos de retorno', k: 'a' },
      { rot: 'Energia cinética aqui', k: 'b' },
      { rot: 'Velocidade aqui', k: 'c' },
      { rot: 'Período', k: 'd' }
    ]);
    var texto = el('div', { class: 'nota' });
    corpo.appendChild(texto);

    function fmt(x, c) {
      var v = x.toFixed(c === undefined ? 2 : c);
      if (/^-0(\.0*)?$/.test(v)) v = v.slice(1);        // nada de "−0,0"
      return v.replace('.', ',').replace('-', '−');
    }
    /* dentro da matemática a vírgula decimal precisa de chaves, senão o
       MathJax a lê como pontuação e abre um espaço depois dela */
    function fmtm(x, c) {
      var v = x.toFixed(c === undefined ? 2 : c);
      if (/^-0(\.0*)?$/.test(v)) v = v.slice(1);
      return v.replace('.', '{,}');
    }

    /* O deslizante de posição anda entre os pontos de retorno, de modo
       que o corpo nunca é colocado numa região proibida. */
    function posicao() {
      var t = retornos(est.E);
      return t.a + est.x * (t.b - t.a);
    }

    function desenhaDiagrama() {
      var t = retornos(est.E), x = posicao();
      var g = G.eixos(cv, {
        altura: 300, xmin: -1.75, xmax: 1.75, ymin: -1.2, ymax: 1.6,
        divY: 7, marcasX: G.marcasLineares(-1.5, 1.5, 6, 1),
        rotX: 'x', rotY: 'energia',
        formataY: function (v) { return fmt(v, 1); }
      });

      /* a região proibida: onde U fica acima de E */
      var ct = g.ct;
      ct.save();
      ct.fillStyle = 'rgba(140,47,57,.07)';
      var passo = (g.xmax - g.xmin) / 400;
      for (var u = g.xmin; u < g.xmax; u += passo) {
        if (U(u) > est.E) {
          ct.fillRect(g.X(u), g.y0, Math.ceil(g.X(u + passo) - g.X(u)) + 1,
                      g.y1 - g.y0);
        }
      }
      ct.restore();

      /* A G.curva limita y ao intervalo, o que desenha um traço reto
         colado no topo do quadro onde a função sai dele. Aqui o trecho
         de fora é simplesmente interrompido. */
      ct.save();
      ct.strokeStyle = G.COR.mestra; ct.lineWidth = 2.6;
      ct.beginPath();
      var dentro = false;
      for (var i = 0; i <= 600; i++) {
        var xx = g.xmin + (g.xmax - g.xmin) * i / 600, yy = U(xx);
        if (yy < g.ymin || yy > g.ymax) { dentro = false; continue; }
        if (!dentro) { ct.moveTo(g.X(xx), g.Y(yy)); dentro = true; }
        else ct.lineTo(g.X(xx), g.Y(yy));
      }
      ct.stroke(); ct.restore();
      rotulo(ct, 'U(x)', g.X(-1.33), g.Y(U(-1.33)) - 15, G.COR.mestra);

      /* a reta da energia, e a cinética como barra vertical */
      ct.save();
      ct.strokeStyle = G.COR.vinho; ct.lineWidth = 2;
      ct.beginPath(); ct.moveTo(g.x0, g.Y(est.E)); ct.lineTo(g.x1, g.Y(est.E));
      ct.stroke(); ct.restore();
      rotulo(ct, 'E', g.x0 + 14, g.Y(est.E) - 11, G.COR.vinho);

      ct.save();
      ct.strokeStyle = G.COR.bronze; ct.lineWidth = 7; ct.lineCap = 'butt';
      ct.beginPath(); ct.moveTo(g.X(x), g.Y(U(x))); ct.lineTo(g.X(x), g.Y(est.E));
      ct.stroke(); ct.restore();
      rotulo(ct, 'T', g.X(x) + 16, (g.Y(U(x)) + g.Y(est.E)) / 2, G.COR.bronze);

      /* o corpo, sobre a curva */
      ct.fillStyle = G.COR.tinta;
      ct.beginPath(); ct.arc(g.X(x), g.Y(U(x)), 7, 0, 6.2832); ct.fill();

      /* os pontos de retorno */
      [t.a, t.b].forEach(function (p) {
        ct.fillStyle = G.COR.vinho;
        ct.beginPath(); ct.arc(g.X(p), g.Y(est.E), 4.5, 0, 6.2832); ct.fill();
      });
      if (t.preso) {
        [-t.a, -t.b].forEach(function (p) {
          ct.fillStyle = G.COR.clara;
          ct.beginPath(); ct.arc(g.X(p), g.Y(est.E), 4.5, 0, 6.2832); ct.fill();
        });
      }
      rotulo(ct, 'região proibida', g.X(0), g.Y(1.3), G.COR.vinho);
    }

    function desenhaFase() {
      var g = G.eixos(cv, {
        altura: 300, xmin: -1.75, xmax: 1.75, ymin: -2.6, ymax: 2.6,
        divY: 4, marcasX: G.marcasLineares(-1.5, 1.5, 6, 1),
        rotX: 'x', rotY: 'velocidade',
        formataY: function (v) { return fmt(v, 1); }
      });
      var ct = g.ct;

      /* uma família de órbitas de fundo, para a órbita atual ter contexto */
      [-0.85, -0.6, -0.35, -0.12, 0.3, 0.8, 1.4].forEach(function (E) {
        orbita(g, E, G.COR.grade === '#e5eaee' ? '#cfd8de' : G.COR.clara, 1.2);
      });
      orbita(g, 0, G.COR.vinho, 2, [6, 4]);        // a separatriz
      orbita(g, est.E, G.COR.mestra, 2.8);

      var x = posicao(), v2 = 2 * (est.E - U(x));
      if (v2 > 0) {
        ct.fillStyle = G.COR.bronze;
        ct.beginPath(); ct.arc(g.X(x), g.Y(Math.sqrt(v2)), 6, 0, 6.2832);
        ct.fill();
      }
      [-1, 1].forEach(function (s) {
        ct.fillStyle = G.COR.suave;
        ct.beginPath(); ct.arc(g.X(s), g.Y(0), 3.5, 0, 6.2832); ct.fill();
      });
      ct.fillStyle = G.COR.vinho;
      ct.beginPath(); ct.arc(g.X(0), g.Y(0), 3.5, 0, 6.2832); ct.fill();

      /* rótulos colados nas próprias curvas, com halo branco: uma caixa
         de legenda no canto cairia justamente em cima das órbitas de
         energia alta, que passam por todos os cantos do quadro */
      rotulo(ct, 'separatriz, E = 0', g.X(0.62), g.Y(1.08), G.COR.vinho);
      /* no ponto mais baixo da órbita, que é onde ela passa pelo fundo
         do poço e onde não há mais nada desenhado */
      var xf = est.E < 0 ? 1.0 : 0.0;
      var vf = Math.sqrt(Math.max(0, 2 * (est.E - U(xf))));
      rotulo(ct, 'a órbita escolhida', g.X(xf), g.Y(-vf) + 15, G.COR.mestra);
    }

    /* v = +- sqrt(2(E - U)), desenhada nos dois ramos */
    function orbita(g, E, cor, esp, tracejado) {
      var ct = g.ct, n = 600;
      ct.save();
      ct.strokeStyle = cor; ct.lineWidth = esp;
      if (tracejado) ct.setLineDash(tracejado);
      [1, -1].forEach(function (s) {
        var desenhando = false;
        ct.beginPath();
        for (var i = 0; i <= n; i++) {
          var x = g.xmin + (g.xmax - g.xmin) * i / n;
          var d = 2 * (E - U(x));
          if (d < 0) { desenhando = false; continue; }
          var px = g.X(x), py = g.Y(s * Math.sqrt(d));
          if (!desenhando) { ct.moveTo(px, py); desenhando = true; }
          else ct.lineTo(px, py);
        }
        ct.stroke();
      });
      ct.restore();
    }

    function desenhaPeriodo() {
      var g = G.eixos(cv, {
        altura: 300, xmin: -1, xmax: 1.5, ymin: 0, ymax: 9,
        divY: 6, marcasX: G.marcasLineares(-1, 1.5, 5, 1),
        rotX: 'energia E', rotY: 'período T',
        formataY: function (v) { return fmt(v, 0); }
      });
      var ct = g.ct;

      /* o limite harmônico do fundo do poço: 2 pi / sqrt(U''(1)) */
      var Th = 2 * Math.PI / Math.sqrt(8);
      ct.save();
      ct.strokeStyle = G.COR.suave; ct.lineWidth = 1.2; ct.setLineDash([5, 4]);
      ct.beginPath(); ct.moveTo(g.x0, g.Y(Th)); ct.lineTo(g.x1, g.Y(Th));
      ct.stroke(); ct.restore();
      rotulo(ct, 'limite harmônico, 2,221', g.X(1.12), g.Y(Th) - 13, G.COR.suave);

      /* os dois ramos, separados pela divergência em E = 0 */
      function ramo(a, b) {
        ct.beginPath();
        var n = 220, primeiro = true;
        for (var i = 0; i <= n; i++) {
          var E = a + (b - a) * i / n;
          var T = periodo(E, 1200);
          if (!isFinite(T) || T > 40) { primeiro = true; continue; }
          var px = g.X(E), py = g.Y(Math.min(T, g.ymax));
          if (primeiro) { ct.moveTo(px, py); primeiro = false; }
          else ct.lineTo(px, py);
        }
        ct.stroke();
      }
      ct.save();
      ct.strokeStyle = G.COR.mestra; ct.lineWidth = 2.6;
      ramo(-0.995, -0.004);
      ramo(0.004, 1.5);
      ct.restore();

      ct.save();
      ct.strokeStyle = G.COR.vinho; ct.lineWidth = 1.4; ct.setLineDash([4, 4]);
      ct.beginPath(); ct.moveTo(g.X(0), g.y0); ct.lineTo(g.X(0), g.y1);
      ct.stroke(); ct.restore();
      rotulo(ct, 'separatriz', g.X(0) + 46, g.y0 + 16, G.COR.vinho);

      var T0 = periodo(est.E, 4000);
      if (isFinite(T0) && T0 < g.ymax) {
        ct.fillStyle = G.COR.bronze;
        ct.beginPath(); ct.arc(g.X(est.E), g.Y(T0), 6, 0, 6.2832); ct.fill();
      }
      rotulo(ct, 'T(E), pela quadratura', g.X(0.95), g.Y(4.6), G.COR.mestra);
    }

    function desenhar() {
      /* o deslizante de posição só faz sentido na primeira vista */
      slX.parentNode.style.display = est.vista === 'periodo' ? 'none' : '';

      if (est.vista === 'diagrama') desenhaDiagrama();
      else if (est.vista === 'fase') desenhaFase();
      else desenhaPeriodo();

      var t = retornos(est.E), x = posicao();
      var T = Math.max(0, est.E - U(x));
      var per = periodo(est.E, 4000);
      painel({
        a: fmt(t.a) + ' e ' + fmt(t.b) + (t.preso ? ' *' : ''),
        b: fmt(T) + ' <small>de ' + fmt(est.E + 1) + '</small>',
        c: fmt(Math.sqrt(2 * T)),
        d: isFinite(per) ? fmt(per, 3) : 'infinito'
      });

      var html;
      if (est.E < 0) {
        html = '<p>Com \\(E = ' + fmtm(est.E) + ' &lt; 0\\) o corpo está '
          + '<strong>preso num dos dois poços</strong>, e qual deles depende '
          + 'apenas de onde ele começou: a barreira em \\(x = 0\\) é alta '
          + 'demais. Ele vai e volta entre \\(x = ' + fmtm(t.a) + '\\) e '
          + '\\(x = ' + fmtm(t.b) + '\\), que são os pontos onde a reta da '
          + 'energia corta a curva de \\(U\\) e a barra bronze desaparece. '
          + 'O poço da esquerda tem os pontos simétricos, e é por isso que o '
          + 'cartão vem com um asterisco.</p>';
      } else {
        html = '<p>Com \\(E = ' + fmtm(est.E) + ' &gt; 0\\) o corpo tem '
          + 'energia de sobra para passar por cima da barreira, e os dois '
          + 'poços viram <strong>um movimento só</strong>, de '
          + '\\(x = ' + fmtm(t.a) + '\\) a \\(x = ' + fmtm(t.b) + '\\). Ele '
          + 'acelera descendo para cada poço e desacelera subindo a barreira, '
          + 'sem nunca parar no meio.</p>';
      }
      if (est.vista === 'diagrama') {
        html += '<p>A barra bronze é a energia cinética, \\(T = E - U(x)\\): '
          + 'toda a distância entre a curva e a reta. Ela é máxima no fundo do '
          + 'poço, onde \\(U\\) é mínima, e some exatamente nos pontos de '
          + 'retorno. A região em rosa é proibida, e não por ser difícil de '
          + 'alcançar: ali \\(T\\) seria negativa, o que é o mesmo que uma '
          + 'velocidade imaginária.</p>';
      } else if (est.vista === 'fase') {
        html += '<p>No espaço de fase, cada energia é uma curva fechada, e o '
          + 'movimento percorre essa curva para sempre. As duas órbitas de '
          + '\\(E &lt; 0\\) são separadas; as de \\(E &gt; 0\\) envolvem as '
          + 'duas. A curva vinho, em \\(E = 0\\), é a <strong>separatriz</strong>: '
          + 'ela passa pelo ponto de equilíbrio instável em \\(x = 0\\) e leva '
          + 'um tempo infinito para chegar lá, que é a razão de o período '
          + 'divergir ali.</p>';
      } else if (est.vista === 'periodo') {
        html += '<p>O período cresce com a energia e diverge na separatriz, '
          + 'pelos dois lados. Isso é o contrário do oscilador harmônico, em '
          + 'que o período não depende da amplitude, e é o primeiro sintoma '
          + 'da não linearidade. No fundo do poço, porém, o harmônico volta: '
          + 'a curva tende à linha tracejada, \\(2\\pi/\\sqrt{U\'\'(1)} = '
          + '2{,}221\\), que é o período da mola equivalente.</p>';
      }
      texto.innerHTML = html;
      tipografar(texto);
    }

    registrarRedesenho(desenhar);
  };


  /* ---------- inicialização ---------- */
  document.addEventListener('DOMContentLoaded', function () {
    Array.prototype.forEach.call(document.querySelectorAll('[data-widget]'), function (n) {
      var f = REGISTRO[n.getAttribute('data-widget')];
      if (f) {
        try { f(n); }
        catch (e) {
          n.innerHTML = '<div class="saida">Não foi possível carregar este componente.</div>';
          if (window.console) console.error(e);
        }
      }
    });
  });
})();
