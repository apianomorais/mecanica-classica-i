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


  /* =================================================================
     5. O foguete: o logaritmo, a queima e os estágios
     As três perguntas que o módulo 5 responde, cada uma numa vista:
     por que a razão de massas precisa ser absurda, o que a gravidade
     cobra enquanto o motor queima, e por que ninguém põe carga em
     órbita com um estágio só. A conta dos estágios idênticos é a mesma
     forma fechada que o foguete.py confere contra uma busca numérica.
     ================================================================= */
  REGISTRO.foguete = function (raiz) {
    var est = { ve: 2942, razao: 5, taxa: 400, eps: 0.10, vista: 'equacao' };

    var G0 = 9.80665;
    var ORBITA = 9400;        // delta-v típico para a órbita baixa, com perdas
    var M0 = 50000, MF = 10000;

    function dv(ve, r) { return ve * Math.log(r); }

    /* n estágios idênticos, com a mesma fração estrutural: cada um
       multiplica a massa pela mesma razão. */
    function dvEstagios(ve, eps, razaoCarga, n) {
      var r = Math.pow(razaoCarga, 1 / n);
      return n * ve * Math.log(r / (1 + eps * (r - 1)));
    }

    var corpo = moldura(raiz, 'O foguete, e por que ele é quase todo tanque');

    var c0 = el('div', { class: 'controles' });
    corpo.appendChild(c0);
    opcoes(c0, [
      { rot: 'A equação', v: 'equacao' },
      { rot: 'Durante a queima', v: 'queima' },
      { rot: 'Estágios', v: 'estagios' }
    ], 0, function (v) { est.vista = v; montar(); desenhar(); });

    var c1 = el('div', { class: 'controles' });
    corpo.appendChild(c1);

    var cv = el('canvas');
    corpo.appendChild(cv);
    var painel = cartoes(corpo, [
      { rot: 'a', k: 'a' }, { rot: 'b', k: 'b' },
      { rot: 'c', k: 'c' }, { rot: 'd', k: 'd' }
    ]);
    var rots = corpo.querySelectorAll('.cartao-num .rot');
    function rotulos(l) {
      l.forEach(function (t, i) { if (rots[i]) rots[i].textContent = t; });
    }
    var texto = el('div', { class: 'nota' });
    corpo.appendChild(texto);

    function fmt(x, c) {
      var v = x.toFixed(c === undefined ? 0 : c);
      return v.replace('.', ',').replace('-', '\u2212');
    }

    /* A G.curva limita y ao intervalo do quadro, o que desenha um traço
       reto colado na borda quando a função sai dele. Aqui o trecho de
       fora é simplesmente interrompido. */
    function tracar(g, f, cor, esp, tracejado) {
      var ct = g.ct, dentro = false;
      ct.save();
      ct.strokeStyle = cor; ct.lineWidth = esp || 2;
      if (tracejado) ct.setLineDash(tracejado);
      ct.beginPath();
      for (var i = 0; i <= 500; i++) {
        var x = g.xmin + (g.xmax - g.xmin) * i / 500, y = f(x);
        if (!isFinite(y) || y < g.ymin || y > g.ymax) { dentro = false; continue; }
        if (!dentro) { ct.moveTo(g.X(x), g.Y(y)); dentro = true; }
        else ct.lineTo(g.X(x), g.Y(y));
      }
      ct.stroke(); ct.restore();
    }
    function fmtm(x, c) {
      return x.toFixed(c === undefined ? 0 : c).replace('.', '{,}');
    }

    /* cada vista pede deslizantes diferentes, de modo que eles são
       refeitos na troca */
    function montar() {
      c1.innerHTML = '';
      deslizante(c1, 'Velocidade de exaustão \\(v_e\\)', 1800, 4600, 1, est.ve,
        function (v) { est.ve = v; desenhar(); },
        function (v) { return fmt(v) + ' m/s (Isp ' + fmt(v / G0) + ' s)'; });
      if (est.vista === 'equacao') {
        deslizante(c1, 'Razão de massas \\(m_0/m_f\\)', 1.2, 25, 0.1, est.razao,
          function (v) { est.razao = v; desenhar(); },
          function (v) { return fmt(v, 1); });
      } else if (est.vista === 'queima') {
        deslizante(c1, 'Taxa de queima', 100, 1600, 10, est.taxa,
          function (v) { est.taxa = v; desenhar(); },
          function (v) { return fmt(v) + ' kg/s'; });
      } else {
        deslizante(c1, 'Fração estrutural \\(\\epsilon\\)', 0.04, 0.25, 0.005,
          est.eps, function (v) { est.eps = v; desenhar(); },
          function (v) { return fmt(100 * v, 1) + ' %'; });
      }
      tipografar(c1);
    }

    /* ---------------- vista 1: a equação ---------------- */
    function vistaEquacao() {
      var g = G.eixos(cv, {
        altura: 290, xmin: 1, xmax: 25, ymin: 0, ymax: 12000,
        divY: 6, marcasX: G.marcasLineares(1, 25, 6, 0),
        rotX: 'razão de massas (massa inicial sobre massa final)',
        rotY: 'Δv  (km/s)',
        formataY: function (v) { return fmt(v / 1000, 1); }
      });
      var ct = g.ct;

      /* a faixa de delta-v que a órbita baixa exige */
      ct.save();
      ct.fillStyle = 'rgba(29,95,126,.07)';
      ct.fillRect(g.x0, g.y0, g.x1 - g.x0, g.Y(ORBITA) - g.y0);
      ct.restore();
      ct.save();
      ct.strokeStyle = G.COR.vinho; ct.lineWidth = 1.6; ct.setLineDash([6, 4]);
      ct.beginPath(); ct.moveTo(g.x0, g.Y(ORBITA)); ct.lineTo(g.x1, g.Y(ORBITA));
      ct.stroke(); ct.restore();
      rotulo(ct, 'órbita baixa: 9400 m/s, com perdas',
             g.x0 + 10, g.Y(ORBITA) - 12, G.COR.vinho, 'left');

      /* duas referências químicas fixas, para a escolhida ter contexto */
      tracar(g, function (r) { return dv(2942, r); }, G.COR.clara, 1.4, [5, 4]);
      tracar(g, function (r) { return dv(4414, r); }, G.COR.clara, 1.4, [5, 4]);
      rotulo(ct, 'querosene, 2942', g.X(20.5), g.Y(dv(2942, 20.5)) + 15,
             G.COR.suave);
      rotulo(ct, 'hidrogênio, 4414', g.X(9.2), g.Y(dv(4414, 9.2)) - 13,
             G.COR.suave);
      tracar(g, function (r) { return dv(est.ve, r); }, G.COR.mestra, 2.8);

      var y = dv(est.ve, est.razao);
      ct.save();
      ct.strokeStyle = G.COR.bronze; ct.lineWidth = 1.2; ct.setLineDash([3, 3]);
      ct.beginPath();
      ct.moveTo(g.X(est.razao), g.y1); ct.lineTo(g.X(est.razao), g.Y(y));
      ct.lineTo(g.x0, g.Y(y));
      ct.stroke(); ct.restore();
      ct.fillStyle = G.COR.bronze;
      ct.beginPath(); ct.arc(g.X(est.razao), g.Y(y), 6, 0, 6.2832); ct.fill();

      var propelente = 1 - 1 / est.razao;
      rotulos(['Δv alcançado', 'Propelente', 'O que não é propelente',
               'Razão para 9400 m/s']);
      painel({
        a: fmt(y) + ' m/s',
        b: fmt(100 * propelente, 1) + ' % da massa',
        c: fmt(100 / est.razao, 1) + ' %',
        d: fmt(Math.exp(ORBITA / est.ve), 1) + ' : 1'
      });

      texto.innerHTML =
        '<p>A curva é \\(\\Delta v = v_e\\ln(m_0/m_f)\\), e o logaritmo é o '
        + 'vilão de toda a engenharia espacial. Com a razão escolhida, '
        + '\\(' + fmtm(est.razao, 1) + '\\), o propelente é '
        + fmt(100 * propelente, 1) + ' % da massa que sai do chão, e sobram '
        + fmt(100 / est.razao, 1) + ' % para tanque, motor, estrutura e '
        + 'carga útil, tudo junto.</p>'
        + '<p>Para dobrar o \\(\\Delta v\\) não basta dobrar o propelente: é '
        + 'preciso <strong>elevar ao quadrado</strong> a razão de massas. De '
        + '10 para 100, de 20 para 400. Só há duas saídas, e as duas aparecem '
        + 'nas outras vistas: aumentar \\(v_e\\), que é química, e parar de '
        + 'carregar tanque vazio, que é estagiamento.</p>'
        + '<p>A linha tracejada em vinho são os 9400 m/s que a órbita baixa '
        + 'exige, já contando as perdas por gravidade e arrasto. Com o '
        + '\\(v_e\\) escolhido, chegar lá pede uma razão de '
        + fmt(Math.exp(ORBITA / est.ve), 1) + ' para 1, isto é, uma máquina '
        + 'em que tudo o que não é combustível cabe em '
        + fmt(100 / Math.exp(ORBITA / est.ve), 1) + ' % da massa.</p>';
      tipografar(texto);
    }

    /* ---------------- vista 2: durante a queima ---------------- */
    function vistaQueima() {
      var tq = (M0 - MF) / est.taxa;
      var g = G.eixos(cv, {
        altura: 290, xmin: 0, xmax: tq, ymin: 0,
        ymax: Math.max(1000, 1.15 * est.ve * Math.log(M0 / MF)),
        divY: 5, marcasX: G.marcasLineares(0, tq, 5, 0),
        rotX: 'tempo desde a ignição (s)', rotY: 'velocidade (km/s)',
        formataY: function (v) { return fmt(v / 1000, 1); }
      });
      var ct = g.ct;

      function vIdeal(t) { return est.ve * Math.log(M0 / (M0 - est.taxa * t)); }
      tracar(g, vIdeal, G.COR.clara, 2.2, [6, 4]);
      tracar(g, function (t) { return vIdeal(t) - G0 * t; }, G.COR.mestra, 2.8);

      /* a perda, como faixa entre as duas curvas */
      ct.save();
      ct.fillStyle = 'rgba(140,47,57,.10)';
      ct.beginPath();
      var n = 160, i;
      for (i = 0; i <= n; i++) {
        var t = tq * i / n;
        ct.lineTo(g.X(t), g.Y(Math.min(g.ymax, vIdeal(t))));
      }
      for (i = n; i >= 0; i--) {
        var t2 = tq * i / n;
        ct.lineTo(g.X(t2), g.Y(Math.max(0, vIdeal(t2) - G0 * t2)));
      }
      ct.closePath(); ct.fill(); ct.restore();

      rotulo(ct, 'sem gravidade', g.X(0.62 * tq), g.Y(vIdeal(0.62 * tq)) - 14,
             G.COR.suave);
      rotulo(ct, 'o que sobra', g.X(0.78 * tq),
             g.Y(vIdeal(0.78 * tq) - G0 * 0.78 * tq) + 16, G.COR.mestra);
      rotulo(ct, 'perda por gravidade', g.X(0.34 * tq),
             (g.Y(vIdeal(0.34 * tq)) + g.Y(vIdeal(0.34 * tq) - G0 * 0.34 * tq)) / 2,
             G.COR.vinho);

      var ideal = est.ve * Math.log(M0 / MF);
      var tw = est.ve * est.taxa / (M0 * G0);
      var aFim = est.ve * est.taxa / MF / G0;
      rotulos(['Δv ideal', 'Perda, g·t', 'Empuxo / peso na partida',
               'Aceleração no fim']);
      painel({
        a: fmt(ideal) + ' m/s',
        b: fmt(G0 * tq) + ' m/s',
        c: fmt(tw, 2) + (tw < 1 ? ' <small>não decola</small>' : ''),
        d: fmt(aFim, 1) + ' g'
      });

      texto.innerHTML =
        '<p>Enquanto o motor queima, a gravidade desconta \\(g\\) de cada '
        + 'segundo de aceleração, e a conta é direta: a perda vale exatamente '
        + '\\(g\\,t_q = ' + fmtm(G0 * tq) + '\\) m/s, a área em rosa. Por isso '
        + 'queimar depressa rende mais: o mesmo propelente, gasto em menos '
        + 'tempo, entrega mais velocidade.</p>'
        + '<p>O limite não é da física, é da estrutura e da tripulação. Com a '
        + 'taxa escolhida, a aceleração no fim da queima chega a '
        + fmt(aFim, 1) + ' g, porque o empuxo é constante e a massa só '
        + 'diminui. É por isso que os motores são estrangulados ou desligados '
        + 'antes do fim, e não por falta de combustível.</p>'
        + '<p>No outro extremo há um piso: se o empuxo não vence o peso, o '
        + 'foguete não sai do chão. O cartão mostra a razão empuxo/peso na '
        + 'partida, e abaixo de 1 a curva desta tela descreve um veículo que '
        + 'fica na plataforma gastando propelente.</p>';
      tipografar(texto);
    }

    /* ---------------- vista 3: estágios ---------------- */
    function vistaEstagios() {
      var g = G.eixos(cv, {
        altura: 290, xmin: 0.2, xmax: 12, ymin: 0, ymax: 16000,
        divY: 8, marcasX: G.marcasLineares(0.2, 12, 5, 1),
        rotX: 'carga útil, em % da massa total', rotY: 'Δv  (km/s)',
        formataY: function (v) { return fmt(v / 1000, 0); }
      });
      var ct = g.ct;

      ct.save();
      ct.strokeStyle = G.COR.vinho; ct.lineWidth = 1.6; ct.setLineDash([6, 4]);
      ct.beginPath(); ct.moveTo(g.x0, g.Y(ORBITA)); ct.lineTo(g.x1, g.Y(ORBITA));
      ct.stroke(); ct.restore();
      rotulo(ct, 'órbita baixa', g.x1 - 52, g.Y(ORBITA) - 12, G.COR.vinho);

      var cores = [G.COR.clara, G.COR.mestra, G.COR.bronze];
      [1, 2, 3].forEach(function (n, i) {
        tracar(g, function (pc) {
          return dvEstagios(est.ve, est.eps, 100 / pc, n);
        }, cores[i], n === 1 ? 2 : 2.6);
        /* cada rótulo num x diferente, à esquerda, onde as três curvas
           ainda estão bem separadas */
        var xr = [2.6, 1.5, 0.75][i];
        rotulo(ct, n === 1 ? '1 estágio' : n + ' estágios', g.X(xr),
               g.Y(dvEstagios(est.ve, est.eps, 100 / xr, n)) + (i ? -14 : 15),
               cores[i]);
      });

      /* o teto de um estágio só, com carga útil nula */
      var teto = est.ve * Math.log(1 / est.eps);
      ct.save();
      ct.strokeStyle = G.COR.suave; ct.lineWidth = 1.1; ct.setLineDash([3, 3]);
      ct.beginPath(); ct.moveTo(g.x0, g.Y(teto)); ct.lineTo(g.x1, g.Y(teto));
      ct.stroke(); ct.restore();
      rotulo(ct, 'teto de um estágio: vₑ ln(1/ε) = ' + fmt(teto),
             g.X(3.2), g.Y(teto) + 15, G.COR.suave, 'left');

      /* a carga útil que cada arranjo leva à órbita baixa */
      function cargaParaOrbita(n) {
        var a = 0.01, b = 60;          // em porcentagem
        if (dvEstagios(est.ve, est.eps, 100 / a, n) < ORBITA) return null;
        for (var i = 0; i < 60; i++) {
          var m = (a + b) / 2;
          if (dvEstagios(est.ve, est.eps, 100 / m, n) > ORBITA) a = m; else b = m;
        }
        return a;
      }
      var c1p = cargaParaOrbita(1), c2p = cargaParaOrbita(2),
          c3p = cargaParaOrbita(3);
      rotulos(['Carga à órbita, 1 estágio', 'com 2 estágios',
               'com 3 estágios', 'Teto de um estágio só']);
      painel({
        a: c1p ? fmt(c1p, 2) + ' %' : 'nenhuma',
        b: c2p ? fmt(c2p, 2) + ' %' : 'nenhuma',
        c: c3p ? fmt(c3p, 2) + ' %' : 'nenhuma',
        d: fmt(teto) + ' m/s'
      });

      texto.innerHTML =
        '<p>Com \\(\\epsilon = ' + fmtm(100 * est.eps, 1) + '\\) %, um estágio '
        + 'só não passa de \\(v_e\\ln(1/\\epsilon) = ' + fmtm(teto) + '\\) m/s '
        + '<em>nem com carga útil nula</em>, porque o tanque vazio e o motor '
        + 'vão junto até o fim. É a linha cinza pontilhada, e ela não depende '
        + 'da carga: é um teto, e nenhuma engenharia de tanque o levanta sem '
        + 'mexer em \\(\\epsilon\\).</p>'
        + '<p>O que o estagiamento faz é parar de carregar tanque vazio no '
        + 'meio do caminho. Cada estágio descartado tira do veículo uma massa '
        + 'que não serve mais para nada, e o ganho aparece justamente onde a '
        + 'carga útil é pequena, que é o caso real.</p>'
        + (c1p
            ? '<p>Neste ajuste, um estágio só ainda chegaria à órbita com '
              + fmt(c1p, 2) + ' % de carga, o que é otimismo de tanque.</p>'
            : '<p>Neste ajuste, <strong>um estágio só não chega à órbita com '
              + 'carga nenhuma</strong>: a curva de um estágio passa inteira '
              + 'abaixo da linha vinho. Dois estágios levam '
              + (c2p ? fmt(c2p, 2) + ' %' : 'nada') + ' e três levam '
              + (c3p ? fmt(c3p, 2) + ' %' : 'nada') + ' da massa total. '
              + 'É essa diferença, e não a elegância, que explica por que '
              + 'todo foguete que já pôs carga em órbita tinha estágios.</p>');
      tipografar(texto);
    }

    function desenhar() {
      if (est.vista === 'equacao') vistaEquacao();
      else if (est.vista === 'queima') vistaQueima();
      else vistaEstagios();
    }

    montar();
    registrarRedesenho(desenhar);
  };


  /* =================================================================
     6. O oscilador harmônico, e onde ele deixa de valer
     As três coisas que o módulo 6 precisa mostrar e que texto nenhum
     mostra bem: que as duas constantes são as mesmas duas escritas de
     outro jeito, que o período não depende da amplitude (e que isso é
     particularidade da parábola), e quanto exatamente custa a
     aproximação de ângulo pequeno no pêndulo.
     ================================================================= */
  REGISTRO.oscilador = function (raiz) {
    var est = { x0: 0.8, v0: 1.2, w: 3.0, vista: 'solucao', graus: 30 };

    var G0 = 9.80665;

    function amplitude() { return Math.hypot(est.x0, est.v0 / est.w); }
    function fase() { return Math.atan2(est.v0 / est.w, est.x0); }

    /* Período exato do pêndulo, pela integral elíptica completa, com a
       regra do ponto médio: a mesma conta do oscilador.py. */
    function razaoPendulo(th0, n) {
      n = n || 2000;
      var k = Math.sin(th0 / 2), passo = (Math.PI / 2) / n, soma = 0;
      for (var i = 0; i < n; i++) {
        var u = passo * (i + 0.5), s = k * Math.sin(u);
        soma += 1 / Math.sqrt(1 - s * s);
      }
      return (soma * passo) * 2 / Math.PI;      // T / T0
    }
    function serie(th0) {
      return 1 + th0 * th0 / 16 + 11 * Math.pow(th0, 4) / 3072;
    }

    var corpo = moldura(raiz, 'O oscilador harmônico, e o preço de sair dele');

    var c0 = el('div', { class: 'controles' });
    corpo.appendChild(c0);
    opcoes(c0, [
      { rot: 'A solução', v: 'solucao' },
      { rot: 'Isocronismo', v: 'isocronismo' },
      { rot: 'O pêndulo de verdade', v: 'pendulo' }
    ], 0, function (v) { est.vista = v; montar(); desenhar(); });

    var c1 = el('div', { class: 'controles' });
    corpo.appendChild(c1);

    var cv = el('canvas');
    corpo.appendChild(cv);
    var painel = cartoes(corpo, [
      { rot: 'a', k: 'a' }, { rot: 'b', k: 'b' },
      { rot: 'c', k: 'c' }, { rot: 'd', k: 'd' }
    ]);
    var rots = corpo.querySelectorAll('.cartao-num .rot');
    function rotulos(l) {
      l.forEach(function (t, i) { if (rots[i]) rots[i].textContent = t; });
    }
    var texto = el('div', { class: 'nota' });
    corpo.appendChild(texto);

    function fmt(x, c) {
      var v = x.toFixed(c === undefined ? 2 : c);
      if (/^-0(\.0*)?$/.test(v)) v = v.slice(1);
      return v.replace('.', ',').replace('-', '\u2212');
    }
    function fmtm(x, c) {
      var v = x.toFixed(c === undefined ? 2 : c);
      if (/^-0(\.0*)?$/.test(v)) v = v.slice(1);
      return v.replace('.', '{,}');
    }

    /* uma porcentagem que pode ser minúscula: em notação decimal ela
       apareceria como 0,000 e não diria nada */
    function pct(v) {
      if (v === 0) return '0 %';
      if (v >= 0.01) return fmt(v, 2) + ' %';
      var e = Math.floor(Math.log(v) / Math.LN10);
      var mant = v / Math.pow(10, e);
      return fmt(mant, 1) + '×10<sup>' + e + '</sup> %';
    }

    function tracar(g, f, cor, esp, tracejado) {
      var ct = g.ct, dentro = false;
      ct.save();
      ct.strokeStyle = cor; ct.lineWidth = esp || 2;
      if (tracejado) ct.setLineDash(tracejado);
      ct.beginPath();
      for (var i = 0; i <= 600; i++) {
        var x = g.xmin + (g.xmax - g.xmin) * i / 600, y = f(x);
        if (!isFinite(y) || y < g.ymin || y > g.ymax) { dentro = false; continue; }
        if (!dentro) { ct.moveTo(g.X(x), g.Y(y)); dentro = true; }
        else ct.lineTo(g.X(x), g.Y(y));
      }
      ct.stroke(); ct.restore();
    }

    function montar() {
      c1.innerHTML = '';
      if (est.vista === 'pendulo') {
        deslizante(c1, 'Amplitude \\(\\theta_0\\)', 1, 175, 1, est.graus,
          function (v) { est.graus = v; desenhar(); },
          function (v) { return fmt(v, 0) + '°'; });
      } else {
        /* as condições iniciais só mudam alguma coisa na primeira vista:
           na segunda, as quatro amplitudes são fixas de propósito */
        if (est.vista === 'solucao') {
          deslizante(c1, 'Posição inicial \\(x_0\\)', -2, 2, 0.05, est.x0,
            function (v) { est.x0 = v; desenhar(); },
            function (v) { return fmt(v) + ' m'; });
          deslizante(c1, 'Velocidade inicial \\(v_0\\)', -4, 4, 0.05, est.v0,
            function (v) { est.v0 = v; desenhar(); },
            function (v) { return fmt(v) + ' m/s'; });
        }
        deslizante(c1, 'Frequência \\(\\omega\\)', 1, 6, 0.05, est.w,
          function (v) { est.w = v; desenhar(); },
          function (v) { return fmt(v) + ' rad/s'; });
      }
      tipografar(c1);
    }

    /* ---------------- vista 1: a solução ---------------- */
    function vistaSolucao() {
      var A = amplitude(), ph = fase(), T = 2 * Math.PI / est.w;
      /* a escala segue a amplitude: fixa, ela esconderia o movimento
         pequeno e cortaria o grande */
      var lim = Math.max(0.5, 1.25 * A);
      var g = G.eixos(cv, {
        altura: 300, xmin: 0, xmax: 3 * T, ymin: -lim, ymax: lim,
        divY: 4, marcasX: G.marcasLineares(0, 3 * T, 6, 1),
        rotX: 'tempo (s)', rotY: 'posição (m)',
        formataY: function (v) { return fmt(v, 1); }
      });
      var ct = g.ct;

      /* as duas parcelas, e a soma delas */
      tracar(g, function (t) { return est.x0 * Math.cos(est.w * t); },
             G.COR.clara, 1.5, [5, 4]);
      tracar(g, function (t) { return (est.v0 / est.w) * Math.sin(est.w * t); },
             G.COR.ambar, 1.5, [5, 4]);
      tracar(g, function (t) { return A * Math.cos(est.w * t - ph); },
             G.COR.mestra, 2.8);

      /* a amplitude e a fase, marcadas na figura */
      ct.save();
      ct.strokeStyle = G.COR.suave; ct.lineWidth = 1; ct.setLineDash([2, 3]);
      [A, -A].forEach(function (y) {
        ct.beginPath(); ct.moveTo(g.x0, g.Y(y)); ct.lineTo(g.x1, g.Y(y));
        ct.stroke();
      });
      ct.restore();
      rotulo(ct, 'C = ' + fmt(A) + ' m', g.x1 - 10, g.Y(A) - 12, G.COR.suave,
             'right');

      var tpico = ph / est.w;
      while (tpico < 0) tpico += T;
      ct.save();
      ct.strokeStyle = G.COR.bronze; ct.lineWidth = 1.6;
      ct.beginPath(); ct.moveTo(g.X(tpico), g.Y(0)); ct.lineTo(g.X(tpico), g.Y(A));
      ct.stroke(); ct.restore();
      ct.fillStyle = G.COR.bronze;
      ct.beginPath(); ct.arc(g.X(tpico), g.Y(A), 5, 0, 6.2832); ct.fill();
      rotulo(ct, 'primeiro máximo', g.X(tpico) + 8, g.Y(A) - 14, G.COR.bronze,
             'left');

      rotulo(ct, 'x₀ cos ωt', g.X(0.42 * T),
             g.Y(est.x0 * Math.cos(est.w * 0.42 * T)) - 13, G.COR.suave);
      rotulo(ct, '(v₀/ω) sen ωt', g.X(1.18 * T),
             g.Y((est.v0 / est.w) * Math.sin(est.w * 1.18 * T)) + 15,
             G.COR.ambar);

      rotulos(['Amplitude C', 'Fase φ', 'Período T', 'Energia por kg']);
      painel({
        a: fmt(A) + ' m',
        b: fmt(180 * ph / Math.PI, 1) + '°',
        c: fmt(T, 3) + ' s',
        d: fmt(0.5 * est.w * est.w * A * A, 3) + ' J/kg'
      });

      texto.innerHTML =
        '<p>As duas curvas tracejadas são as parcelas que vêm das condições '
        + 'iniciais: \\(x_0\\cos\\omega t\\), que vale \\(x_0\\) em '
        + '\\(t = 0\\) e tem derivada nula ali, e '
        + '\\((v_0/\\omega)\\sen\\omega t\\), que começa em zero com a '
        + 'inclinação certa. A soma das duas é a curva cheia.</p>'
        + '<p>E a soma é <strong>outro cosseno</strong>, com amplitude '
        + '\\(C = \\sqrt{x_0^2 + (v_0/\\omega)^2} = ' + fmtm(A) + '\\) m e '
        + 'fase \\(\\varphi = ' + fmtm(180 * ph / Math.PI, 1) + '^\\circ\\). '
        + 'As constantes continuam sendo duas, porque a equação é de segunda '
        + 'ordem; o que muda é o par escolhido. O programa confere que as '
        + 'duas formas coincidem em \\(10^{-17}\\) m ao longo de cinquenta '
        + 'mil instantes.</p>'
        + '<p>Mexa em \\(x_0\\) e em \\(v_0\\) e observe o que <em>não</em> '
        + 'muda: o espaçamento dos máximos. A amplitude e a fase dependem de '
        + 'como o movimento começou; o período, não. Ele é propriedade da '
        + 'mola e da massa, e de mais nada.</p>';
      tipografar(texto);
    }

    /* ---------------- vista 2: isocronismo ---------------- */
    function vistaIsocronismo() {
      var T = 2 * Math.PI / est.w;
      var g = G.eixos(cv, {
        altura: 300, xmin: 0, xmax: 2.2 * T, ymin: -1.15, ymax: 1.15,
        divY: 4, marcasX: G.marcasLineares(0, 2.2 * T, 5, 1),
        rotX: 'tempo (s)', rotY: 'posição, em frações da amplitude',
        formataY: function (v) { return fmt(v, 1); }
      });
      var ct = g.ct;

      /* quatro amplitudes diferentes do MESMO oscilador */
      var cores = [G.COR.mestra, G.COR.azul, G.COR.bronze, G.COR.ambar];
      [1, 0.6, 0.3, 0.12].forEach(function (a, i) {
        tracar(g, function (t) { return a * Math.cos(est.w * t); },
               cores[i], i === 0 ? 2.6 : 1.8);
      });

      /* as linhas verticais onde todas cruzam o zero ao mesmo tempo */
      ct.save();
      ct.strokeStyle = G.COR.vinho; ct.lineWidth = 1.2; ct.setLineDash([4, 4]);
      for (var k = 0; k * T / 2 + T / 4 < 2.2 * T; k++) {
        var tc = T / 4 + k * T / 2;
        ct.beginPath(); ct.moveTo(g.X(tc), g.y0); ct.lineTo(g.X(tc), g.y1);
        ct.stroke();
      }
      ct.restore();
      rotulo(ct, 'todas cruzam o zero juntas', g.X(T / 4) + 8, g.y0 + 14,
             G.COR.vinho, 'left');

      rotulos(['Período, qualquer amplitude', 'Amplitudes desenhadas',
               'Diferença entre os períodos', 'No poço duplo do módulo 4']);
      painel({
        a: fmt(T, 4) + ' s',
        b: '1 : 0,6 : 0,3 : 0,12',
        c: '0 <small>em todas as casas</small>',
        d: 'muda com E'
      });

      texto.innerHTML =
        '<p>As quatro curvas são o <strong>mesmo</strong> oscilador, soltado '
        + 'de quatro amplitudes diferentes, numa razão de oito para um entre '
        + 'a maior e a menor. Elas cruzam o zero exatamente juntas, e chegam '
        + 'aos extremos exatamente juntas. É o isocronismo, e foi o que '
        + 'Galileu notou olhando um lustre.</p>'
        + '<p>A razão é a forma da força. Com \\(F = -kx\\), dobrar a '
        + 'amplitude dobra a distância a percorrer e dobra a força em cada '
        + 'ponto, de modo que o corpo anda o dobro em velocidade dobrada, e o '
        + 'tempo sai igual. O cancelamento é exato só para a parábola: o '
        + 'programa mostra períodos idênticos em nove casas com amplitudes '
        + 'de 1 cm a 10 m.</p>'
        + '<p>Convém guardar que isso é <em>particularidade</em>, e não regra '
        + 'de oscilações. O poço duplo do módulo 4 tem período que cresce com '
        + 'a energia, e o pêndulo de verdade, na vista seguinte, também. '
        + 'Isocronismo é privilégio de quem fica perto do fundo.</p>';
      tipografar(texto);
    }

    /* ---------------- vista 3: o pêndulo ---------------- */
    function vistaPendulo() {
      var g = G.eixos(cv, {
        altura: 300, xmin: 0, xmax: 175, ymin: 1, ymax: 2.6,
        divY: 8, marcasX: G.marcasLineares(0, 175, 7, 0),
        rotX: 'amplitude θ₀ (graus)', rotY: 'T / T₀',
        formataY: function (v) { return fmt(v, 1); }
      });
      var ct = g.ct;

      /* a aproximação de ângulo pequeno é a reta em 1 */
      ct.save();
      ct.strokeStyle = G.COR.suave; ct.lineWidth = 1.3; ct.setLineDash([5, 4]);
      ct.beginPath(); ct.moveTo(g.x0, g.Y(1)); ct.lineTo(g.x1, g.Y(1));
      ct.stroke(); ct.restore();
      rotulo(ct, 'aproximação de ângulo pequeno: T = T₀', g.x0 + 10,
             g.Y(1) - 13, G.COR.suave, 'left');

      tracar(g, function (gr) { return serie(gr * Math.PI / 180); },
             G.COR.ambar, 1.8, [5, 4]);
      tracar(g, function (gr) { return razaoPendulo(gr * Math.PI / 180, 400); },
             G.COR.mestra, 2.8);
      rotulo(ct, 'exato (integral elíptica)', g.X(118),
             g.Y(razaoPendulo(118 * Math.PI / 180, 400)) - 14, G.COR.mestra);
      rotulo(ct, 'série até θ⁴', g.X(150),
             g.Y(Math.min(2.55, serie(150 * Math.PI / 180))) + 15, G.COR.ambar);

      /* a faixa em que a aproximação erra menos de 1 % */
      ct.save();
      ct.fillStyle = 'rgba(29,95,126,.07)';
      var lim = 0;
      for (var gr = 1; gr <= 175; gr++) {
        if (razaoPendulo(gr * Math.PI / 180, 300) < 1.01) lim = gr;
      }
      ct.fillRect(g.x0, g.y0, g.X(lim) - g.x0, g.y1 - g.y0);
      ct.restore();
      rotulo(ct, 'erro < 1 %', g.X(lim / 2), g.y0 + 16, G.COR.suave);

      var th = est.graus * Math.PI / 180;
      var r = razaoPendulo(th, 4000), rs = serie(th);
      ct.fillStyle = G.COR.bronze;
      ct.beginPath(); ct.arc(g.X(est.graus), g.Y(Math.min(g.ymax, r)), 6, 0,
                             6.2832);
      ct.fill();

      var T0 = 2 * Math.PI * Math.sqrt(1 / G0);
      rotulos(['T exato, pêndulo de 1 m', 'Erro de usar T₀',
               'Erro da série até θ⁴', 'Limite do erro de 1 %']);
      painel({
        a: fmt(T0 * r, 4) + ' s',
        b: fmt(100 * (r - 1), 2) + ' %',
        c: pct(100 * Math.abs(rs - r) / r),
        d: fmt(lim, 0) + '°'
      });

      texto.innerHTML =
        '<p>A equação do pêndulo é '
        + '\\(\\ddot\\theta = -(g/L)\\sen\\theta\\), e ela <strong>não</strong> '
        + 'é a do oscilador harmônico. Vira a dele quando se troca '
        + '\\(\\sen\\theta\\) por \\(\\theta\\), o que custa menos de 1 % até '
        + fmt(lim, 0) + '°, e é por isso que o pêndulo serve para medir '
        + '\\(g\\) com cronômetro de mão.</p>'
        + '<p>Com \\(\\theta_0 = ' + fmt(est.graus, 0) + '^\\circ\\), o '
        + 'período verdadeiro é ' + fmt(100 * (r - 1), 2) + ' % maior que '
        + '\\(T_0 = 2\\pi\\sqrt{L/g}\\). A curva cheia é a integral elíptica '
        + 'completa, calculada por quadratura; a tracejada em âmbar é a série '
        + '\\(1 + \\theta_0^2/16 + 11\\theta_0^4/3072\\), que acompanha bem '
        + 'até uns 60° e depois desiste.</p>'
        + '<p>Perto de 180° o período dispara. O pêndulo colocado '
        + 'exatamente em pé é um equilíbrio instável, e levar uma '
        + 'eternidade para sair dele é a mesma coisa que o tempo infinito da '
        + 'separatriz do módulo 4. Harmônico e caótico não são mundos '
        + 'separados: são o mesmo sistema em amplitudes diferentes, e o '
        + 'módulo 9 continua essa conversa.</p>';
      tipografar(texto);
    }

    function desenhar() {
      if (est.vista === 'solucao') vistaSolucao();
      else if (est.vista === 'isocronismo') vistaIsocronismo();
      else vistaPendulo();
    }

    montar();
    registrarRedesenho(desenhar);
  };


  /* =================================================================
     7. Oscilações amortecidas
     A terceira vista é a razão de este componente existir: ela mostra,
     medindo, que o amortecimento crítico NÃO é o mais rápido para
     voltar ao repouso, ao contrário do que quase todo livro afirma.
     O ótimo é ligeiramente subamortecido, e fica exatamente onde o
     primeiro repique tem o tamanho da tolerância exigida.
     ================================================================= */
  REGISTRO.amortecido = function (raiz) {
    var est = { z: 0.3, tol: 0.02, vista: 'regimes' };

    var W0 = 1.0;            // tudo em unidades de omega0

    function x(t, z) {
      if (z < 1) {
        var w1 = Math.sqrt(1 - z * z);
        return Math.exp(-z * t) * (Math.cos(w1 * t) + (z / w1) * Math.sin(w1 * t));
      }
      if (Math.abs(z - 1) < 1e-9) return Math.exp(-t) * (1 + t);
      var r = Math.sqrt(z * z - 1), r1 = -z + r, r2 = -z - r;
      return (-r2 * Math.exp(r1 * t) + r1 * Math.exp(r2 * t)) / (r1 - r2);
    }

    /* tempo de acomodação: último instante em que |x| ainda excede a
       tolerância. Varrido no tempo, e não resolvido em forma fechada,
       porque a última saída da faixa pode ser em qualquer semiciclo */
    function acomodacao(z, tol) {
      var dt = 0.004, ultimo = 0;
      for (var t = 0; t < 40; t += dt) {
        if (Math.abs(x(t, z)) > tol) ultimo = t;
      }
      return ultimo;
    }

    /* o ótimo em forma fechada: exp(-pi z / sqrt(1-z^2)) = tol */
    function otimoPrevisto(tol) {
      var L = -Math.log(tol) / Math.PI;
      return Math.sqrt(L * L / (1 + L * L));
    }

    var corpo = moldura(raiz, 'Amortecimento: os três regimes, e qual deles para mais depressa');

    var c0 = el('div', { class: 'controles' });
    corpo.appendChild(c0);
    opcoes(c0, [
      { rot: 'Os três regimes', v: 'regimes' },
      { rot: 'O decaimento e o Q', v: 'qualidade' },
      { rot: 'Qual para mais depressa', v: 'acomodacao' }
    ], 0, function (v) { est.vista = v; montar(); desenhar(); });

    var c1 = el('div', { class: 'controles' });
    corpo.appendChild(c1);

    var cv = el('canvas');
    corpo.appendChild(cv);
    var painel = cartoes(corpo, [
      { rot: 'a', k: 'a' }, { rot: 'b', k: 'b' },
      { rot: 'c', k: 'c' }, { rot: 'd', k: 'd' }
    ]);
    var rots = corpo.querySelectorAll('.cartao-num .rot');
    function rotulos(l) {
      l.forEach(function (t, i) { if (rots[i]) rots[i].textContent = t; });
    }
    var texto = el('div', { class: 'nota' });
    corpo.appendChild(texto);

    function fmt(v, c) {
      var s = v.toFixed(c === undefined ? 2 : c);
      if (/^-0(\.0*)?$/.test(s)) s = s.slice(1);
      return s.replace('.', ',').replace('-', '−');
    }
    function fmtm(v, c) {
      var s = v.toFixed(c === undefined ? 2 : c);
      if (/^-0(\.0*)?$/.test(s)) s = s.slice(1);
      return s.replace('.', '{,}');
    }

    function tracar(g, f, cor, esp, tracejado) {
      var ct = g.ct, dentro = false;
      ct.save();
      ct.strokeStyle = cor; ct.lineWidth = esp || 2;
      if (tracejado) ct.setLineDash(tracejado);
      ct.beginPath();
      for (var i = 0; i <= 700; i++) {
        var u = g.xmin + (g.xmax - g.xmin) * i / 700, y = f(u);
        if (!isFinite(y) || y < g.ymin || y > g.ymax) { dentro = false; continue; }
        if (!dentro) { ct.moveTo(g.X(u), g.Y(y)); dentro = true; }
        else ct.lineTo(g.X(u), g.Y(y));
      }
      ct.stroke(); ct.restore();
    }

    function montar() {
      c1.innerHTML = '';
      if (est.vista === 'acomodacao') {
        deslizante(c1, 'Tolerância exigida', 0.002, 0.10, 0.001, est.tol,
          function (v) { est.tol = v; desenhar(); },
          function (v) { return fmt(100 * v, 1) + ' % do deslocamento'; });
      } else {
        deslizante(c1, 'Amortecimento \\(\\gamma/\\omega_0\\)', 0.02, 2.5, 0.01,
          est.z, function (v) { est.z = v; desenhar(); },
          function (v) {
            return fmt(v) + (v < 0.99 ? ' (subamortecido)'
                   : v > 1.01 ? ' (superamortecido)' : ' (crítico)');
          });
      }
      tipografar(c1);
    }

    /* ---------------- vista 1: os três regimes ---------------- */
    function vistaRegimes() {
      var g = G.eixos(cv, {
        altura: 300, xmin: 0, xmax: 18, ymin: -1.1, ymax: 1.1,
        divY: 4, marcasX: G.marcasLineares(0, 18, 7, 0),
        rotX: 'tempo, em unidades de 1/ω₀', rotY: 'posição / x₀',
        formataY: function (v) { return fmt(v, 1); }
      });
      var ct = g.ct;

      /* os outros dois regimes, de fundo */
      tracar(g, function (t) { return x(t, 0.1); }, 'rgba(29,95,126,.25)', 1.5);
      tracar(g, function (t) { return x(t, 1); }, G.COR.clara, 1.6, [5, 4]);
      tracar(g, function (t) { return x(t, 2.5); }, G.COR.clara, 1.6, [2, 3]);
      rotulo(ct, 'γ/ω₀ = 0,1', g.X(14.2), g.Y(x(14.2, 0.1)) - 14, G.COR.suave);
      rotulo(ct, 'crítico', g.X(3.1), g.Y(x(3.1, 1)) - 13, G.COR.suave);
      rotulo(ct, 'γ/ω₀ = 2,5', g.X(5.4), g.Y(x(5.4, 2.5)) - 14, G.COR.suave);

      /* o envelope do caso escolhido */
      if (est.z < 1) {
        var amp = 1 / Math.sqrt(1 - est.z * est.z);
        ct.save();
        ct.strokeStyle = G.COR.vinho; ct.lineWidth = 1.3; ct.setLineDash([4, 4]);
        [1, -1].forEach(function (s) {
          ct.beginPath();
          for (var i = 0; i <= 300; i++) {
            var t = 18 * i / 300, y = s * amp * Math.exp(-est.z * t);
            if (Math.abs(y) > 1.05) continue;
            ct.lineTo(g.X(t), g.Y(y));
          }
          ct.stroke();
        });
        ct.restore();
        rotulo(ct, 'envelope', g.X(8.4),
               g.Y(amp * Math.exp(-est.z * 8.4)) - 13, G.COR.vinho);
      }

      tracar(g, function (t) { return x(t, est.z); }, G.COR.mestra, 2.8);

      var w1 = est.z < 1 ? Math.sqrt(1 - est.z * est.z) : 0;
      rotulos(['Regime', 'ω₁ / ω₀', 'Período, em T₀', 'Fator de qualidade Q']);
      painel({
        a: est.z < 0.99 ? 'subamortecido'
           : est.z > 1.01 ? 'superamortecido' : 'crítico',
        b: w1 ? fmt(w1, 4) : 'não oscila',
        c: w1 ? fmt(1 / w1, 3) : '—',
        d: fmt(1 / (2 * est.z), 3)
      });

      texto.innerHTML =
        '<p>A equação é \\(\\ddot{x} + 2\\gamma\\dot{x} + \\omega_0^2 x = 0\\), '
        + 'e o que decide tudo é o sinal de '
        + '\\(\\gamma^2 - \\omega_0^2\\). As três soluções não se parecem: uma '
        + 'tem seno dentro de uma exponencial, outra tem um \\(t\\) '
        + 'multiplicando a exponencial, a terceira é soma de duas '
        + 'exponenciais. São a mesma solução, escrita conforme o sinal.</p>'
        + (est.z < 1
          ? '<p>No regime escolhido o sistema oscila, mas <strong>mais devagar '
            + 'que o oscilador livre</strong>: \\(\\omega_1 = \\omega_0'
            + '\\sqrt{1-(\\gamma/\\omega_0)^2} = ' + fmtm(w1, 4)
            + '\\,\\omega_0\\), de modo que o período fica '
            + fmt(100 * (1 / w1 - 1), 1) + ' % maior. O amortecimento não '
            + 'encolhe só a amplitude: ele atrasa o relógio, e é por isso que '
            + 'um pêndulo dentro de óleo não serve para medir o tempo.</p>'
          : '<p>Aqui não há oscilação nenhuma: o corpo volta ao repouso sem '
            + 'cruzar o zero uma única vez. Não é que a oscilação seja rápida '
            + 'demais para ser vista, é que ela não existe, porque as duas '
            + 'raízes da equação característica são reais.</p>')
        + '<p>O programa confere as três fórmulas contra a integração '
        + 'numérica da mesma equação: a maior diferença é de '
        + '\\(10^{-13}\\) m. A integração não sabe em que regime está, e '
        + 'acha a mesma curva nos três.</p>';
      tipografar(texto);
    }

    /* ---------------- vista 2: o decaimento e o Q ---------------- */
    function vistaQualidade() {
      var z = Math.min(est.z, 0.95);
      var w1 = Math.sqrt(1 - z * z), T1 = 2 * Math.PI / w1;
      /* a janela acompanha o decaimento: com amortecimento forte, seis
         períodos deixariam cinco deles vazios */
      var tmax = Math.min(40, 6.5 * T1, 4.2 / z);
      var g = G.eixos(cv, {
        altura: 300, xmin: 0, xmax: tmax,
        ymin: -1.1, ymax: 1.1, divY: 4,
        marcasX: G.marcasLineares(0, tmax, 6, 0),
        rotX: 'tempo, em unidades de 1/ω₀', rotY: 'posição / x₀',
        formataY: function (v) { return fmt(v, 1); }
      });
      var ct = g.ct;

      tracar(g, function (t) { return x(t, z); }, G.COR.mestra, 2.2);

      /* os picos sucessivos, e a razão constante entre eles */
      var amp = 1 / w1, anterior = null;
      for (var k = 0; k < 7; k++) {
        var tp = k * T1;
        if (tp > g.xmax) break;
        var xp = x(tp, z);
        ct.fillStyle = G.COR.bronze;
        ct.beginPath(); ct.arc(g.X(tp), g.Y(xp), 5, 0, 6.2832); ct.fill();
        if (anterior !== null && k === 1) {
          rotulo(ct, '÷ ' + fmt(Math.exp(z * T1), 2), g.X(tp) - 2,
                 g.Y(xp) - 16, G.COR.bronze);
        }
        anterior = xp;
      }

      ct.save();
      ct.strokeStyle = G.COR.vinho; ct.lineWidth = 1.3; ct.setLineDash([4, 4]);
      ct.beginPath();
      for (var i = 0; i <= 300; i++) {
        var t = g.xmax * i / 300, y = amp * Math.exp(-z * t);
        if (y > g.ymax) continue;
        ct.lineTo(g.X(t), g.Y(y));
      }
      ct.stroke(); ct.restore();
      rotulo(ct, 'envelope', g.X(0.55 * g.xmax),
             g.Y(amp * Math.exp(-z * 0.55 * g.xmax)) - 13, G.COR.vinho);

      var Qp = Math.PI / (z * T1);        // = w1 / (2 z)
      var Qf = 1 / (2 * z);
      var u = 2 * Math.PI / Qp;
      var Qe = 2 * Math.PI / (1 - Math.exp(-u));

      rotulos(['Q = ω₀/2γ', 'Q pelos picos', 'Q pela energia',
               'Energia perdida por ciclo']);
      painel({
        a: fmt(Qf, 3),
        b: fmt(Qp, 3),
        c: fmt(Qe, 3),
        d: fmt(100 * (1 - Math.exp(-u)), 1) + ' %'
      });

      texto.innerHTML =
        '<p>De um pico ao seguinte a amplitude é sempre dividida pelo '
        + '<strong>mesmo fator</strong>, \\(e^{\\gamma T_1} = '
        + fmtm(Math.exp(z * T1), 3) + '\\), e é por isso que o logaritmo '
        + 'dessa razão, chamado decremento logarítmico, é a maneira prática '
        + 'de medir amortecimento: basta uma régua e dois picos.</p>'
        + '<p>Os três cartões trazem três definições de \\(Q\\) que os livros '
        + 'costumam tratar como a mesma, e elas dão três números. '
        + '\\(Q\\) pelos picos vale \\(\\omega_1/2\\gamma\\), e não '
        + '\\(\\omega_0/2\\gamma\\), porque o decremento mede o período '
        + 'verdadeiro: a razão entre os dois é exatamente '
        + '\\(\\sqrt{1-(\\gamma/\\omega_0)^2}\\).</p>'
        + '<p>E \\(Q\\) pela energia é maior que os dois, porque a perda por '
        + 'ciclo vale \\(1 - e^{-2\\pi/Q}\\) e não \\(2\\pi/Q\\): a segunda é '
        + 'a primeira linearizada. O erro é de cerca de \\(\\pi/Q\\), o que '
        + 'significa 3 % mesmo num oscilador com \\(Q = 100\\). O programa '
        + 'verifica as duas diferenças em forma fechada, casa por casa.</p>';
      tipografar(texto);
    }

    /* ---------------- vista 3: quem para mais depressa ---------------- */
    function vistaAcomodacao() {
      var g = G.eixos(cv, {
        altura: 300, xmin: 0.2, xmax: 2.2, ymin: 0, ymax: 22,
        divY: 5, marcasX: G.marcasLineares(0.2, 2.2, 5, 1),
        rotX: 'amortecimento  γ / ω₀', rotY: 'tempo até parar  (1/ω₀)',
        formataY: function (v) { return fmt(v, 0); }
      });
      var ct = g.ct;

      /* a curva do tempo de acomodação, medida ponto a ponto */
      var melhor = { t: 1e9, z: 0 }, pontos = [];
      for (var i = 0; i <= 100; i++) {
        var z = 0.2 + 2.0 * i / 100;
        var t = acomodacao(z, est.tol);
        pontos.push([z, t]);
        if (t < melhor.t) { melhor = { t: t, z: z }; }
      }
      ct.save();
      ct.strokeStyle = G.COR.mestra; ct.lineWidth = 2.8;
      ct.beginPath();
      pontos.forEach(function (p, k) {
        var py = g.Y(Math.min(p[1], g.ymax));
        if (k === 0) ct.moveTo(g.X(p[0]), py); else ct.lineTo(g.X(p[0]), py);
      });
      ct.stroke(); ct.restore();

      /* o crítico, e o ótimo de verdade */
      var tc = acomodacao(1, est.tol);
      ct.save();
      ct.strokeStyle = G.COR.suave; ct.lineWidth = 1.3; ct.setLineDash([5, 4]);
      ct.beginPath(); ct.moveTo(g.X(1), g.y0); ct.lineTo(g.X(1), g.y1);
      ct.stroke(); ct.restore();
      ct.fillStyle = G.COR.suave;
      ct.beginPath(); ct.arc(g.X(1), g.Y(tc), 5, 0, 6.2832); ct.fill();
      rotulo(ct, 'crítico', g.X(1) + 10, g.Y(tc) - 14, G.COR.suave, 'left');

      ct.fillStyle = G.COR.vinho;
      ct.beginPath(); ct.arc(g.X(melhor.z), g.Y(melhor.t), 6, 0, 6.2832);
      ct.fill();
      rotulo(ct, 'o mais rápido', g.X(melhor.z), g.Y(melhor.t) + 17,
             G.COR.vinho);

      var prev = otimoPrevisto(est.tol);
      rotulos(['O mais rápido está em', 'Previsto pela fórmula',
               'Crítico demora', 'Repique no ótimo']);
      painel({
        a: 'γ/ω₀ = ' + fmt(melhor.z),
        b: 'γ/ω₀ = ' + fmt(prev, 3),
        c: '+' + fmt(100 * (tc / melhor.t - 1), 0) + ' %',
        d: fmt(100 * est.tol, 1) + ' %'
      });

      texto.innerHTML =
        '<p>Quase todo livro diz que o amortecimento crítico é o que leva o '
        + 'sistema de volta ao repouso mais depressa. A curva mostra que '
        + '<strong>não é</strong>: o mínimo está em '
        + '\\(\\gamma/\\omega_0 = ' + fmtm(melhor.z) + '\\), e o crítico '
        + 'demora ' + fmt(100 * (tc / melhor.t - 1), 0) + ' % a mais.</p>'
        + '<p>O enunciado correto tem uma letra miúda que costuma ser '
        + 'omitida: o crítico é o mais rápido <em>entre os que não '
        + 'ultrapassam o repouso</em>. Se um repique couber dentro da '
        + 'tolerância exigida, vale a pena deixá-lo acontecer, porque o '
        + 'sistema chega lá antes.</p>'
        + '<p>Daí sair uma regra de projeto exata: o ótimo é onde o primeiro '
        + 'repique tem o tamanho da tolerância, isto é, onde '
        + '\\(e^{-\\pi z/\\sqrt{1-z^2}} = \\) tolerância. Para '
        + fmt(100 * est.tol, 1) + ' %, isso dá \\(z = ' + fmtm(prev, 3)
        + '\\), que é o que a medida mostra. Aperte a tolerância e veja o '
        + 'ótimo caminhar para o crítico: no limite de tolerância zero, o '
        + 'livro volta a ter razão.</p>'
        + '<p>É também por isso que a suspensão de um carro é projetada em '
        + 'torno de 0,7, e não em 1,0.</p>';
      tipografar(texto);
    }

    function desenhar() {
      if (est.vista === 'regimes') vistaRegimes();
      else if (est.vista === 'qualidade') vistaQualidade();
      else vistaAcomodacao();
    }

    montar();
    registrarRedesenho(desenhar);
  };


  /* =================================================================
     8. Oscilações forçadas
     Três coisas que só ficam claras mexendo: que os picos da amplitude,
     da velocidade e da potência estão em frequências DIFERENTES, que o
     transiente pode ultrapassar o estacionário quase ao dobro, e que a
     resposta a uma força qualquer sai de uma convolução com a função de
     Green, sem resolver nada de novo.
     ================================================================= */
  REGISTRO.forcado = function (raiz) {
    var est = { gama: 0.15, w: 3.6, forca: 'pulso', vista: 'curva' };

    var W0 = 4.0, F0 = 1.0;

    function amp(w, g) {
      var a = W0 * W0 - w * w, b = 2 * g * w;
      return F0 / Math.sqrt(a * a + b * b);
    }
    function faseDe(w, g) {
      return Math.atan2(2 * g * w, W0 * W0 - w * w);
    }

    var corpo = moldura(raiz, 'Forçar o oscilador: a ressonância, o transiente e a força qualquer');

    var c0 = el('div', { class: 'controles' });
    corpo.appendChild(c0);
    opcoes(c0, [
      { rot: 'A curva de ressonância', v: 'curva' },
      { rot: 'O transiente', v: 'transiente' },
      { rot: 'Uma força qualquer', v: 'green' }
    ], 0, function (v) { est.vista = v; montar(); desenhar(); });

    var c1 = el('div', { class: 'controles' });
    corpo.appendChild(c1);

    var cv = el('canvas');
    corpo.appendChild(cv);
    var painel = cartoes(corpo, [
      { rot: 'a', k: 'a' }, { rot: 'b', k: 'b' },
      { rot: 'c', k: 'c' }, { rot: 'd', k: 'd' }
    ]);
    var rots = corpo.querySelectorAll('.cartao-num .rot');
    function rotulos(l) {
      l.forEach(function (t, i) { if (rots[i]) rots[i].textContent = t; });
    }
    var texto = el('div', { class: 'nota' });
    corpo.appendChild(texto);

    function fmt(v, c) {
      var s = v.toFixed(c === undefined ? 2 : c);
      if (/^-0(\.0*)?$/.test(s)) s = s.slice(1);
      return s.replace('.', ',').replace('-', '\u2212');
    }
    function fmtm(v, c) {
      var s = v.toFixed(c === undefined ? 2 : c);
      if (/^-0(\.0*)?$/.test(s)) s = s.slice(1);
      return s.replace('.', '{,}');
    }

    function tracar(g, f, cor, esp, tracejado) {
      var ct = g.ct, dentro = false;
      ct.save();
      ct.strokeStyle = cor; ct.lineWidth = esp || 2;
      if (tracejado) ct.setLineDash(tracejado);
      ct.beginPath();
      for (var i = 0; i <= 700; i++) {
        var u = g.xmin + (g.xmax - g.xmin) * i / 700, y = f(u);
        if (!isFinite(y) || y < g.ymin || y > g.ymax) { dentro = false; continue; }
        if (!dentro) { ct.moveTo(g.X(u), g.Y(y)); dentro = true; }
        else ct.lineTo(g.X(u), g.Y(y));
      }
      ct.stroke(); ct.restore();
    }

    function montar() {
      c1.innerHTML = '';
      deslizante(c1, 'Amortecimento \\(\\gamma\\)', 0.05, 2.9, 0.05, est.gama,
        function (v) { est.gama = v; desenhar(); },
        function (v) { return fmt(v) + '  (Q = ' + fmt(W0 / (2 * v), 1) + ')'; });
      if (est.vista === 'transiente') {
        deslizante(c1, 'Frequência da força \\(\\omega\\)', 2.0, 6.0, 0.01,
          est.w, function (v) { est.w = v; desenhar(); },
          function (v) { return fmt(v) + ' rad/s'; });
      }
      if (est.vista === 'green') {
        opcoes(c1, [
          { rot: 'Pulso', v: 'pulso' },
          { rot: 'Dente de serra', v: 'dente' },
          { rot: 'Marteladas', v: 'martelo' }
        ], ['pulso', 'dente', 'martelo'].indexOf(est.forca),
          function (v) { est.forca = v; desenhar(); });
      }
      tipografar(c1);
    }

    /* ---------------- vista 1: a curva de ressonância ---------------- */
    function vistaCurva() {
      var g = est.gama;
      var wa = W0 * W0 > 2 * g * g ? Math.sqrt(W0 * W0 - 2 * g * g) : null;

      /* cada curva normalizada pelo próprio máximo: o que interessa aqui
         é ONDE está o pico, e não quanto ele vale */
      var maxA = wa ? amp(wa, g) : amp(0.001, g);
      var maxV = W0 * amp(W0, g);
      var maxP = g * Math.pow(W0 * amp(W0, g), 2);

      var gr = G.eixos(cv, {
        altura: 300, xmin: 1.5, xmax: 7.0, ymin: 0, ymax: 1.15,
        divY: 4, marcasX: G.marcasLineares(1.5, 7.0, 6, 1),
        rotX: 'frequência da força  ω  (rad/s)',
        rotY: 'cada curva no seu máximo',
        formataY: function (v) { return fmt(v, 1); }
      });
      var ct = gr.ct;

      tracar(gr, function (w) { return amp(w, g) / maxA; }, G.COR.mestra, 2.8);
      tracar(gr, function (w) { return w * amp(w, g) / maxV; },
             G.COR.bronze, 2.2);
      tracar(gr, function (w) {
        return g * Math.pow(w * amp(w, g), 2) / maxP;
      }, G.COR.vinho, 2.2, [6, 4]);

      /* os picos, marcados */
      ct.save();
      ct.strokeStyle = G.COR.suave; ct.lineWidth = 1.1; ct.setLineDash([3, 3]);
      ct.beginPath(); ct.moveTo(gr.X(W0), gr.y0); ct.lineTo(gr.X(W0), gr.y1);
      ct.stroke(); ct.restore();
      rotulo(ct, 'ω₀', gr.X(W0), gr.y1 - 14, G.COR.suave);

      if (wa) {
        ct.fillStyle = G.COR.mestra;
        ct.beginPath(); ct.arc(gr.X(wa), gr.Y(1), 6, 0, 6.2832); ct.fill();
        rotulo(ct, 'pico de x', gr.X(wa) - 10, gr.Y(1) - 15, G.COR.mestra,
               'right');
      }
      ct.fillStyle = G.COR.bronze;
      ct.beginPath(); ct.arc(gr.X(W0), gr.Y(1), 5, 0, 6.2832); ct.fill();
      rotulo(ct, 'pico de v e de P', gr.X(W0) + 12, gr.Y(1) - 15,
             G.COR.bronze, 'left');

      /* a largura a meia altura da curva de potência */
      ct.save();
      ct.strokeStyle = G.COR.vinho; ct.lineWidth = 1.4;
      ct.beginPath();
      ct.moveTo(gr.X(Math.sqrt(W0 * W0 + g * g) - g), gr.Y(0.5));
      ct.lineTo(gr.X(Math.sqrt(W0 * W0 + g * g) + g), gr.Y(0.5));
      ct.stroke(); ct.restore();
      rotulo(ct, 'largura = 2γ', gr.X(W0), gr.Y(0.5) + 16, G.COR.vinho);

      rotulos(['Pico da amplitude', 'Pico da velocidade e da potência',
               'Largura a meia altura', 'Fator de qualidade']);
      painel({
        a: wa ? fmt(wa, 4) : 'não há pico',
        b: fmt(W0, 4),
        c: fmt(2 * g, 3),
        d: fmt(W0 / (2 * g), 2)
      });

      texto.innerHTML =
        '<p>As três curvas são do mesmo oscilador, cada uma normalizada pelo '
        + 'próprio máximo, porque aqui o que importa é <em>onde</em> está o '
        + 'pico. A amplitude tem máximo em '
        + (wa
            ? '\\(\\sqrt{\\omega_0^2-2\\gamma^2} = ' + fmtm(wa, 3) + '\\)'
            : '\\(\\sqrt{\\omega_0^2-2\\gamma^2}\\)')
        + ', abaixo de \\(\\omega_0\\). A velocidade e a potência absorvida '
        + 'têm máximo <strong>exatamente</strong> em \\(\\omega_0 = 4\\), em '
        + 'qualquer amortecimento.</p>'
        + '<p>São três ressonâncias diferentes, e a pergunta "qual é a '
        + 'frequência de ressonância" só tem resposta depois de dizer '
        + 'ressonância <em>de quê</em>. Quem projeta para não quebrar olha o '
        + 'pico da amplitude; quem projeta para transferir energia, como uma '
        + 'antena ou um forno de micro-ondas, olha o da potência.</p>'
        + (wa
          ? '<p>Aumente \\(\\gamma\\) e veja o pico da amplitude caminhar '
            + 'para a esquerda até sumir em \\(\\gamma = \\omega_0/\\sqrt2 = '
            + fmtm(W0 / Math.SQRT2, 3) + '\\), onde a curva passa a só '
            + 'decrescer. Os outros dois picos não se mexem.</p>'
          : '<p>Com este amortecimento a amplitude <strong>não tem mais '
            + 'pico</strong>: passou de \\(\\omega_0/\\sqrt2 = '
            + fmtm(W0 / Math.SQRT2, 3) + '\\) e a curva só decresce. Os picos '
            + 'da velocidade e da potência continuam em \\(\\omega_0\\), '
            + 'imperturbáveis.</p>')
        + '<p>A barra vinho é a largura a meia altura da curva de potência, e '
        + 'ela vale \\(2\\gamma\\) exatamente, de onde '
        + '\\(Q = \\omega_0/\\text{largura}\\). É assim que se mede \\(Q\\) '
        + 'em laboratório: varrendo a frequência, sem desligar nada nem '
        + 'cronometrar decaimento.</p>';
      tipografar(texto);
    }

    /* ---------------- vista 2: o transiente ---------------- */
    function vistaTransiente() {
      var g = est.gama, w = est.w;
      var A = amp(w, g), ph = faseDe(w, g);
      var w1 = g < W0 ? Math.sqrt(W0 * W0 - g * g) : 0;

      /* solução exata: estacionário mais transiente, com x(0)=0, v(0)=0 */
      var Ax = A * Math.cos(ph), Av = A * w * Math.sin(ph);
      var B1 = -Ax, B2 = w1 ? (-Av - g * B1) / w1 : 0;
      function x(t) {
        var trans = Math.exp(-g * t) * (B1 * Math.cos(w1 * t)
                                        + B2 * Math.sin(w1 * t));
        return A * Math.cos(w * t - ph) + trans;
      }

      var tmax = Math.min(140, 7 / g);
      var pico = 0;
      for (var i = 0; i <= 4000; i++) pico = Math.max(pico, Math.abs(x(tmax * i / 4000)));
      var lim = 1.15 * Math.max(pico, A);

      var gr = G.eixos(cv, {
        altura: 300, xmin: 0, xmax: tmax, ymin: -lim, ymax: lim,
        divY: 4, marcasX: G.marcasLineares(0, tmax, 6, 0),
        rotX: 'tempo (s)', rotY: 'posição (m)',
        formataY: function (v) { return fmt(v, 1); }
      });
      var ct = gr.ct;

      ct.save();
      ct.strokeStyle = G.COR.suave; ct.lineWidth = 1.2; ct.setLineDash([5, 4]);
      [A, -A].forEach(function (y) {
        ct.beginPath(); ct.moveTo(gr.x0, gr.Y(y)); ct.lineTo(gr.x1, gr.Y(y));
        ct.stroke();
      });
      ct.restore();
      rotulo(ct, 'amplitude estacionária', gr.x1 - 10, gr.Y(A) - 13,
             G.COR.suave, 'right');

      tracar(gr, x, G.COR.mestra, 2);

      rotulos(['Amplitude estacionária', 'Maior amplitude do transiente',
               'Quanto ultrapassa', 'Período do batimento']);
      painel({
        a: fmt(A, 4) + ' m',
        b: fmt(pico, 4) + ' m',
        c: '+' + fmt(100 * (pico / A - 1), 1) + ' %',
        d: Math.abs(w - W0) > 1e-9
          ? fmt(2 * Math.PI / Math.abs(W0 - w), 1) + ' s' : '—'
      });

      texto.innerHTML =
        '<p>O oscilador parte do repouso, e o que se vê é a soma de duas '
        + 'coisas: o <strong>estacionário</strong>, que oscila na frequência '
        + 'da força e dura para sempre, e o <strong>transiente</strong>, que '
        + 'oscila em \\(\\omega_1\\) e morre como \\(e^{-\\gamma t}\\). O '
        + 'transiente é o problema do módulo 7, intacto: ele não sabe nada '
        + 'sobre a força, só sobre o sistema.</p>'
        + '<p>Duas senoides de frequências parecidas produzem '
        + '<strong>batimento</strong>, e por isso o começo ultrapassa o '
        + 'regime permanente: aqui, '
        + fmt(100 * (pico / A - 1), 1) + ' % acima. Quanto menor o '
        + 'amortecimento, maior o excesso, e no limite \\(\\gamma \\to 0\\) '
        + 'ele tende ao <em>dobro</em> da amplitude final.</p>'
        + '<p>Essa é uma armadilha de projeto real: quem dimensiona uma '
        + 'estrutura pela resposta de regime permanente subestima o pico, e '
        + 'pode errar por um fator 2. O primeiro minuto de uma máquina '
        + 'ligando é mais perigoso que a hora seguinte inteira.</p>'
        + '<p>Repare também que o tempo até estabilizar quase não muda quando '
        + 'se mexe em \\(\\omega\\): ele vale cerca de '
        + '\\(\\ln(1/0{,}02) = 3{,}9\\) constantes \\(1/\\gamma\\), '
        + 'porque quem precisa morrer é o transiente.</p>';
      tipografar(texto);
    }

    /* ---------------- vista 3: uma força qualquer ---------------- */
    function vistaGreen() {
      var g = Math.min(est.gama, 2.0);
      var w1 = Math.sqrt(W0 * W0 - g * g);
      var tmax = 20, n = 2400, dt = tmax / n;

      function f(t) {
        if (est.forca === 'pulso') return (t >= 1 && t <= 2) ? 1 : 0;
        if (est.forca === 'dente') return (t % 2) - 1;
        var s = 0.06, soma = 0;
        [2.0, 5.5, 6.2].forEach(function (t0) {
          soma += Math.exp(-Math.pow((t - t0) / s, 2));
        });
        return soma;
      }

      /* convolução discreta: x_i = dt * soma_j G(t_i - t_j) f(t_j) */
      var fs = [], gs = [], i, j;
      for (i = 0; i <= n; i++) {
        fs.push(f(i * dt));
        gs.push(Math.exp(-g * i * dt) * Math.sin(w1 * i * dt) / w1);
      }
      var xs = [], maxx = 1e-9;
      for (i = 0; i <= n; i++) {
        var soma = 0;
        for (j = 0; j <= i; j++) soma += gs[i - j] * fs[j];
        xs.push(soma * dt);
        maxx = Math.max(maxx, Math.abs(xs[i]));
      }

      var gr = G.eixos(cv, {
        altura: 310, xmin: 0, xmax: tmax, ymin: -1.3, ymax: 1.3,
        divY: 4, marcasX: G.marcasLineares(0, tmax, 6, 0),
        rotX: 'tempo (s)', rotY: 'normalizados',
        formataY: function (v) { return fmt(v, 1); }
      });
      var ct = gr.ct;

      /* a força, em escala própria */
      var maxf = 1e-9;
      fs.forEach(function (v) { maxf = Math.max(maxf, Math.abs(v)); });
      ct.save();
      ct.strokeStyle = G.COR.ambar; ct.lineWidth = 1.8;
      ct.beginPath();
      for (i = 0; i <= n; i++) ct.lineTo(gr.X(i * dt), gr.Y(fs[i] / maxf));
      ct.stroke(); ct.restore();
      rotulo(ct, 'a força', gr.X(0.3 * tmax), gr.Y(1.12), G.COR.ambar, 'left');

      /* a função de Green, de fundo */
      ct.save();
      ct.strokeStyle = G.COR.clara; ct.lineWidth = 1.4; ct.setLineDash([4, 4]);
      ct.beginPath();
      for (i = 0; i <= n; i++) ct.lineTo(gr.X(i * dt), gr.Y(gs[i] * w1 * 0.5));
      ct.stroke(); ct.restore();
      rotulo(ct, 'G(t), a resposta a um impulso', gr.X(0.06 * tmax),
             gr.Y(-1.14), G.COR.suave, 'left');

      /* a resposta */
      ct.save();
      ct.strokeStyle = G.COR.mestra; ct.lineWidth = 2.6;
      ct.beginPath();
      for (i = 0; i <= n; i++) ct.lineTo(gr.X(i * dt), gr.Y(xs[i] / maxx));
      ct.stroke(); ct.restore();
      /* o rótulo vai no maior pico da resposta, onde não há mais nada */
      var ipico = 0;
      for (i = 0; i <= n; i++) if (Math.abs(xs[i]) > Math.abs(xs[ipico])) ipico = i;
      rotulo(ct, 'a resposta', gr.X(ipico * dt) + 12,
             gr.Y(xs[ipico] / maxx) - 6, G.COR.mestra, 'left');

      rotulos(['Força escolhida', 'Maior deslocamento',
               'Tempo de memória', 'Quantos ciclos de memória']);
      painel({
        a: est.forca === 'pulso' ? 'pulso retangular'
           : est.forca === 'dente' ? 'dente de serra' : 'três marteladas',
        b: fmt(maxx, 4) + ' m',
        c: fmt(1 / g, 2) + ' s',
        d: fmt(w1 / (2 * Math.PI * g), 2)
      });

      texto.innerHTML =
        '<p>A equação é linear, e isso dá de graça o caso geral. Se a resposta '
        + 'a um <em>impulso</em> em \\(t=0\\) é conhecida, chamada função de '
        + 'Green, então qualquer força é uma fila de impulsos e a resposta é '
        + 'a soma das respostas:</p>'
        + '<p>\\[ G(t) = \\frac{e^{-\\gamma t}\\sen\\omega_1 t}{\\omega_1}, '
        + '\\qquad x(t) = \\int_{-\\infty}^{t} G(t-s)\\,f(s)\\,ds. \\]</p>'
        + '<p>A curva cheia é essa integral, calculada aqui mesmo. Nenhuma das '
        + 'três forças tem qualquer parentesco com uma senoide, e nenhuma '
        + 'precisou de solução nova: a conta é sempre a mesma convolução. O '
        + 'programa confere o resultado contra a integração direta da equação '
        + 'e mede o erro caindo com o passo, de primeira ordem para as forças '
        + 'com salto e de segunda para as suaves.</p>'
        + '<p>Repare no limite inferior da integral: a resposta em \\(t\\) só '
        + 'depende da força <em>antes</em> de \\(t\\), porque \\(G\\) é nula '
        + 'para argumento negativo. É a causalidade escrita como propriedade '
        + 'de uma função, e o oscilador tem memória de cerca de '
        + '\\(1/\\gamma = ' + fmtm(1 / g, 2) + '\\) s: o que aconteceu antes '
        + 'disso já não importa.</p>'
        + '<p>Essa ideia não fica na mecânica. A função de Green é a mesma '
        + 'ferramenta de circuitos, de propagação de ondas, de difusão de '
        + 'calor e, com outro nome, do propagador da teoria quântica de '
        + 'campos. O oscilador amortecido é o exemplo mais barato dela.</p>';
      tipografar(texto);
    }

    function desenhar() {
      if (est.vista === 'curva') vistaCurva();
      else if (est.vista === 'transiente') vistaTransiente();
      else vistaGreen();
    }

    montar();
    registrarRedesenho(desenhar);
  };


  /* =================================================================
     9. Retratos de fase
     O módulo muda a pergunta: em vez de "qual é x(t)", pergunta-se
     "que tipos de movimento existem". As três vistas são as três
     respostas que o plano de fase dá sem resolver nada: o retrato
     inteiro do pêndulo com a separatriz, a classificação dos pontos
     fixos pela matriz 2x2, e o ciclo-limite, que é um tipo de
     movimento que não existe em sistema linear nenhum.
     ================================================================= */
  REGISTRO.retratos = function (raiz) {
    var est = { gama: 0.0, mu: 1.0, fixo: 'centro', vista: 'pendulo' };

    /* ---- campos ---- */
    function fPend(th, om, g) {
      return [om, -Math.sin(th) - 2 * g * om];
    }
    function fVdp(x, y, mu) {
      return [y, mu * (1 - x * x) * y - x];
    }

    function rk4(f, x, y, dt) {
      var k1 = f(x, y);
      var k2 = f(x + dt * k1[0] / 2, y + dt * k1[1] / 2);
      var k3 = f(x + dt * k2[0] / 2, y + dt * k2[1] / 2);
      var k4 = f(x + dt * k3[0], y + dt * k3[1]);
      return [x + dt * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6,
              y + dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6];
    }

    function trajeto(f, x0, y0, dt, n) {
      var pts = [[x0, y0]], x = x0, y = y0;
      for (var i = 0; i < n; i++) {
        var p = rk4(f, x, y, dt);
        x = p[0]; y = p[1];
        if (!isFinite(x) || !isFinite(y) || Math.abs(y) > 1e4) break;
        pts.push([x, y]);
      }
      return pts;
    }

    var corpo = moldura(raiz, 'O plano de fase: todos os movimentos de uma vez');

    var c0 = el('div', { class: 'controles' });
    corpo.appendChild(c0);
    opcoes(c0, [
      { rot: 'O pêndulo inteiro', v: 'pendulo' },
      { rot: 'Perto de um ponto fixo', v: 'linear' },
      { rot: 'O ciclo-limite', v: 'ciclo' }
    ], 0, function (v) { est.vista = v; montar(); desenhar(); });

    var c1 = el('div', { class: 'controles' });
    corpo.appendChild(c1);

    var cv = el('canvas');
    corpo.appendChild(cv);
    var painel = cartoes(corpo, [
      { rot: 'a', k: 'a' }, { rot: 'b', k: 'b' },
      { rot: 'c', k: 'c' }, { rot: 'd', k: 'd' }
    ]);
    var rots = corpo.querySelectorAll('.cartao-num .rot');
    function rotulos(l) {
      l.forEach(function (t, i) { if (rots[i]) rots[i].textContent = t; });
    }
    var texto = el('div', { class: 'nota' });
    corpo.appendChild(texto);

    function fmt(v, c) {
      var s = v.toFixed(c === undefined ? 2 : c);
      if (/^-0(\.0*)?$/.test(s)) s = s.slice(1);
      return s.replace('.', ',').replace('-', '\u2212');
    }
    function fmtm(v, c) {
      var s = v.toFixed(c === undefined ? 2 : c);
      if (/^-0(\.0*)?$/.test(s)) s = s.slice(1);
      return s.replace('.', '{,}');
    }

    function linha(g, pts, cor, esp, tracejado) {
      var ct = g.ct, dentro = false;
      ct.save();
      ct.strokeStyle = cor; ct.lineWidth = esp || 1.6;
      if (tracejado) ct.setLineDash(tracejado);
      ct.beginPath();
      for (var i = 0; i < pts.length; i++) {
        var x = pts[i][0], y = pts[i][1];
        if (x < g.xmin || x > g.xmax || y < g.ymin || y > g.ymax) {
          dentro = false; continue;
        }
        if (!dentro) { ct.moveTo(g.X(x), g.Y(y)); dentro = true; }
        else ct.lineTo(g.X(x), g.Y(y));
      }
      ct.stroke(); ct.restore();
    }

    function montar() {
      c1.innerHTML = '';
      if (est.vista === 'ciclo') {
        deslizante(c1, 'Não linearidade \\(\\mu\\)', 0.05, 4, 0.05, est.mu,
          function (v) { est.mu = v; desenhar(); },
          function (v) { return fmt(v); });
      } else {
        deslizante(c1, 'Amortecimento \\(\\gamma\\)', 0, 1.2, 0.01, est.gama,
          function (v) { est.gama = v; desenhar(); },
          function (v) {
            return v === 0 ? 'nenhum (conservativo)' : fmt(v);
          });
      }
      if (est.vista === 'linear') {
        opcoes(c1, [
          { rot: 'O fundo, θ = 0', v: 'centro' },
          { rot: 'O alto, θ = π', v: 'sela' }
        ], est.fixo === 'centro' ? 0 : 1,
          function (v) { est.fixo = v; desenhar(); });
      }
      tipografar(c1);
    }

    /* ---------------- vista 1: o pêndulo inteiro ---------------- */
    function vistaPendulo() {
      var g = est.gama;
      var f = function (th, om) { return fPend(th, om, g); };
      var gr = G.eixos(cv, {
        altura: 330, xmin: -1.6 * Math.PI, xmax: 1.6 * Math.PI,
        ymin: -3.2, ymax: 3.2, divY: 4,
        marcasX: [{ v: -Math.PI, r: '−π' }, { v: 0, r: '0' },
                  { v: Math.PI, r: 'π' }],
        rotX: 'ângulo θ', rotY: 'velocidade angular ω',
        formataY: function (v) { return fmt(v, 0); }
      });
      var ct = gr.ct;

      /* órbitas de libração, de dentro para fora */
      [0.4, 0.9, 1.4, 1.8, 1.96].forEach(function (om0) {
        linha(gr, trajeto(f, 0, om0, 0.01, 4000), G.COR.clara, 1.5);
      });
      /* órbitas de rotação, nos dois sentidos */
      [2.1, 2.5, 3.0].forEach(function (om0) {
        linha(gr, trajeto(f, -1.6 * Math.PI, om0, 0.01, 2500), G.COR.clara, 1.5);
        linha(gr, trajeto(f, 1.6 * Math.PI, -om0, 0.01, 2500), G.COR.clara, 1.5);
      });

      /* a separatriz: sai da sela e volta a ela */
      if (g === 0) {
        linha(gr, trajeto(f, 0, 1.9999999, 0.005, 6000), G.COR.vinho, 2.4);
        linha(gr, trajeto(f, 0, -1.9999999, 0.005, 6000), G.COR.vinho, 2.4);
        rotulo(ct, 'separatriz', gr.X(0), gr.Y(2.0) - 14, G.COR.vinho);
      } else {
        /* com atrito ela deixa de ser fechada: o que sobra é a
           variedade estável da sela, a fronteira entre as bacias */
        [1, -1].forEach(function (s) {
          var pts = trajeto(function (th, om) {
            var d = fPend(th, om, g);
            return [-d[0], -d[1]];          // integra para trás no tempo
          }, Math.PI - s * 1e-6, s * 1e-6 * 0.6, 0.01, 2200);
          linha(gr, pts, G.COR.vinho, 2.2);
        });
        rotulo(ct, 'fronteira das bacias', gr.X(0.1), gr.Y(2.55),
               G.COR.vinho);
      }

      /* os pontos fixos */
      [-1, 0, 1].forEach(function (k) {
        var x = 2 * Math.PI * k;
        if (x >= gr.xmin && x <= gr.xmax) {
          ct.fillStyle = g === 0 ? G.COR.mestra : G.COR.bronze;
          ct.beginPath(); ct.arc(gr.X(x), gr.Y(0), 6, 0, 6.2832); ct.fill();
        }
        var xs = Math.PI * (2 * k + 1);
        if (xs >= gr.xmin && xs <= gr.xmax) {
          ct.strokeStyle = G.COR.vinho; ct.lineWidth = 2.4;
          ct.beginPath();
          ct.moveTo(gr.X(xs) - 6, gr.Y(0) - 6); ct.lineTo(gr.X(xs) + 6, gr.Y(0) + 6);
          ct.moveTo(gr.X(xs) - 6, gr.Y(0) + 6); ct.lineTo(gr.X(xs) + 6, gr.Y(0) - 6);
          ct.stroke();
        }
      });
      rotulo(ct, g === 0 ? 'centro' : 'foco estável', gr.X(0), gr.Y(0) + 20,
             g === 0 ? G.COR.mestra : G.COR.bronze);
      rotulo(ct, 'sela', gr.X(Math.PI), gr.Y(0) + 20, G.COR.vinho);

      rotulos(['Fundo do poço', 'Alto', 'Energia da separatriz',
               'Tipos de movimento']);
      painel({
        a: g === 0 ? 'centro' : 'foco estável',
        b: 'sela',
        c: g === 0 ? 'e = 2, exata' : 'não se conserva',
        d: g === 0 ? 'libração e rotação' : 'tudo para no fundo'
      });

      texto.innerHTML = g === 0
        ? '<p>Cada curva é um movimento inteiro, e o plano traz todos de uma '
          + 'vez. Dentro da curva vinho o pêndulo <strong>libra</strong>: vai '
          + 'e volta, e a curva se fecha. Fora dela ele <strong>roda</strong>: '
          + 'passa por cima e \\(\\theta\\) cresce sem limite. Não há um '
          + 'terceiro tipo.</p>'
          + '<p>A curva vinho é a <strong>separatriz</strong>, em '
          + '\\(e = 2\\) exatamente, e ela não é um movimento como os outros: '
          + 'o pêndulo leva tempo <em>infinito</em> para chegar ao alto. Duas '
          + 'condições iniciais que diferem em \\(10^{-6}\\) na velocidade, '
          + 'uma de cada lado dela, fazem coisas qualitativamente diferentes '
          + 'para sempre. É a primeira vez no curso que uma diferença '
          + 'minúscula decide um destino.</p>'
          + '<p>Repare que o retrato se repete a cada \\(2\\pi\\): o plano é '
          + 'na verdade um cilindro, porque \\(\\theta\\) e '
          + '\\(\\theta+2\\pi\\) são o mesmo estado.</p>'
        : '<p>Com atrito as curvas deixam de se fechar: toda trajetória '
          + 'termina num dos mínimos, que viraram <strong>focos '
          + 'estáveis</strong>. A energia não se conserva, de modo que as '
          + 'curvas atravessam as linhas de energia constante em vez de '
          + 'segui-las.</p>'
          + '<p>A separatriz some, e no lugar dela fica a curva vinho: a '
          + '<strong>fronteira entre bacias de atração</strong>, que é o '
          + 'conjunto das condições iniciais que terminam exatamente na sela. '
          + 'De um lado dela o pêndulo para num mínimo, do outro no seguinte. '
          + 'O programa mede essas fronteiras: a primeira está em '
          + '\\(\\omega_0\\) entre 2,60 e 2,65.</p>'
          + '<p>As selas continuam onde estavam, e continuam selas em '
          + 'qualquer amortecimento. O equilíbrio de cabeça para baixo é '
          + 'instável por geometria, e não por falta de atrito.</p>';
      tipografar(texto);
    }

    /* ---------------- vista 2: perto de um ponto fixo ---------------- */
    function vistaLinear() {
      var g = est.gama, sela = est.fixo === 'sela';
      var th0 = sela ? Math.PI : 0;
      var f = function (th, om) { return fPend(th, om, g); };

      /* a jacobiana do pêndulo, em forma fechada */
      var a21 = sela ? 1 : -1;            // -cos(theta0)
      var J = [[0, 1], [a21, -2 * g]];
      var tr = J[0][0] + J[1][1], det = J[0][0] * J[1][1] - J[0][1] * J[1][0];
      var disc = tr * tr - 4 * det;

      var R = 0.9;
      var gr = G.eixos(cv, {
        altura: 330, xmin: -R, xmax: R, ymin: -R, ymax: R, divY: 4,
        marcasX: G.marcasLineares(-R, R, 5, 1),
        rotX: sela ? 'θ − π' : 'θ', rotY: 'ω',
        formataY: function (v) { return fmt(v, 1); }
      });
      var ct = gr.ct;

      /* campo de direções, que é o que a equação diz em cada ponto */
      ct.save();
      ct.strokeStyle = G.COR.grade; ct.lineWidth = 1.2;
      for (var i = -4; i <= 4; i++) {
        for (var j = -4; j <= 4; j++) {
          var px = i * R / 4.5, py = j * R / 4.5;
          var d = f(th0 + px, py);
          var m = Math.hypot(d[0], d[1]);
          if (m < 1e-9) continue;
          var L = 0.1 * R;
          seta(ct, gr.X(px - L * d[0] / m / 2), gr.Y(py - L * d[1] / m / 2),
               gr.X(px + L * d[0] / m / 2), gr.Y(py + L * d[1] / m / 2),
               G.COR.grade, 1.2);
        }
      }
      ct.restore();

      /* trajetórias de verdade, lançadas a distâncias diferentes: todas
         ao mesmo raio dariam a mesma órbita no caso conservativo, que é
         o que acontece quando se esquece de variar a energia */
      [0.18, 0.36, 0.54, 0.72, 0.9].forEach(function (frac) {
        [0, Math.PI].forEach(function (ang) {
          var r0 = frac * R;
          var pts = trajeto(f, th0 + r0 * Math.cos(ang), r0 * Math.sin(ang),
                            0.01, 2600).map(function (p) {
            return [p[0] - th0, p[1]];
          });
          linha(gr, pts, G.COR.clara, 1.6);
        });
      });

      /* os autovetores, quando são reais */
      var tipo, lam1, lam2;
      if (disc > 0) {
        lam1 = (tr + Math.sqrt(disc)) / 2;
        lam2 = (tr - Math.sqrt(disc)) / 2;
        [[lam1, G.COR.vinho, 'instável'], [lam2, G.COR.mestra, 'estável']]
          .forEach(function (par) {
            var lam = par[0];
            /* autovetor de [[0,1],[a21,-2g]]: (1, lam) */
            var vx = 1 / Math.hypot(1, lam), vy = lam / Math.hypot(1, lam);
            ct.save();
            ct.strokeStyle = par[1]; ct.lineWidth = 2.4;
            ct.beginPath();
            ct.moveTo(gr.X(-R * vx), gr.Y(-R * vy));
            ct.lineTo(gr.X(R * vx), gr.Y(R * vy));
            ct.stroke(); ct.restore();
            rotulo(ct, par[2], gr.X(0.78 * R * vx), gr.Y(0.78 * R * vy) - 12,
                   par[1]);
          });
        tipo = (lam1 * lam2 < 0) ? 'sela'
             : (lam1 < 0 ? 'nó estável' : 'nó instável');
      } else {
        lam1 = lam2 = tr / 2;
        tipo = Math.abs(tr) < 1e-9 ? 'centro'
             : (tr < 0 ? 'foco estável' : 'foco instável');
      }

      ct.fillStyle = G.COR.tinta;
      ct.beginPath(); ct.arc(gr.X(0), gr.Y(0), 6, 0, 6.2832); ct.fill();

      var desc = disc > 0
        ? fmt(lam1, 3) + ' e ' + fmt(lam2, 3)
        : fmt(tr / 2, 3) + ' ± ' + fmt(Math.sqrt(-disc) / 2, 3) + 'i';
      rotulos(['Ponto fixo', 'Traço e determinante', 'Autovalores', 'Tipo']);
      painel({
        a: sela ? 'θ = π' : 'θ = 0',
        b: 'tr = ' + fmt(tr, 2) + ', det = ' + fmt(det, 2),
        c: desc,
        d: tipo
      });

      texto.innerHTML =
        '<p>Perto de um ponto fixo, o campo é quase linear, e quem decide '
        + 'tudo é a matriz das derivadas:</p>'
        + '<p>\\[ J = \\begin{pmatrix} 0 & 1 \\\\ '
        + (sela ? '+1' : '-1') + ' & -2\\gamma \\end{pmatrix}, \\qquad '
        + '\\operatorname{tr}J = ' + fmtm(tr, 2) + ', \\qquad '
        + '\\det J = ' + fmtm(det, 2) + '. \\]</p>'
        + (disc > 0
          ? '<p>O discriminante é positivo, de modo que os autovalores são '
            + '<strong>reais</strong>, e as retas coloridas são os '
            + 'autovetores. Repare no que as trajetórias fazem: elas chegam '
            + 'pela direção estável e saem pela instável, e nenhuma delas '
            + 'alcança o ponto fixo. O programa mostra que a direção de saída '
            + 'não depende de por onde a trajetória entrou, e que o desvio em '
            + 'relação ao autovetor cai com o <em>quadrado</em> da distância: '
            + 'a trajetória é tangente a ele.</p>'
          : '<p>O discriminante é negativo, de modo que os autovalores são '
            + '<strong>complexos conjugados</strong>, e não há autovetor real '
            + 'nenhum para desenhar: a trajetória gira. A parte real '
            + 'vale \\(-\\gamma\\) e decide se a espiral fecha para dentro '
            + '(estável) ou abre para fora. Com \\(\\gamma = 0\\) ela é '
            + 'exatamente nula, as órbitas se fecham e o ponto é um '
            + '<strong>centro</strong>.</p>')
        + '<p>O centro é o caso delicado: ele é o único tipo cuja '
        + 'classificação a linearização <em>não</em> garante. Parte real nula '
        + 'quer dizer que os termos não lineares, que a matriz descartou, '
        + 'decidem. No pêndulo eles não estragam nada, porque a energia se '
        + 'conserva; em geral, podem transformar o centro numa espiral lenta '
        + 'para qualquer um dos dois lados.</p>';
      tipografar(texto);
    }

    /* ---------------- vista 3: o ciclo-limite ---------------- */
    function vistaCiclo() {
      var mu = est.mu;
      var f = function (x, y) { return fVdp(x, y, mu); };
      var lim = Math.max(3.2, 1.2 * mu + 1.6);
      var gr = G.eixos(cv, {
        altura: 330, xmin: -3.2, xmax: 3.2, ymin: -lim, ymax: lim, divY: 4,
        marcasX: G.marcasLineares(-3, 3, 5, 0),
        rotX: 'x', rotY: 'velocidade',
        formataY: function (v) { return fmt(v, 1); }
      });
      var ct = gr.ct;

      var dt = Math.min(0.004, 0.02 / Math.max(1, mu));
      var n = Math.round(Math.max(60, 25 * mu) / dt);

      /* o ciclo: parte de cima dele e desenha só o último pedaço */
      var ciclo = trajeto(f, 2, 0, dt, n);
      var corte = Math.floor(ciclo.length * 0.75);
      linha(gr, ciclo.slice(corte), G.COR.mestra, 2.8);

      /* uma de dentro e uma de fora, com o transiente inteiro */
      linha(gr, trajeto(f, 0.05, 0, dt, n), G.COR.bronze, 1.5);
      linha(gr, trajeto(f, 3.0, 0, dt, Math.round(n / 2)), G.COR.ambar, 1.5);

      ct.fillStyle = G.COR.vinho;
      ct.beginPath(); ct.arc(gr.X(0), gr.Y(0), 5, 0, 6.2832); ct.fill();
      rotulo(ct, 'foco instável', gr.X(0) + 10, gr.Y(0) - 12, G.COR.vinho,
             'left');
      rotulo(ct, 'de dentro', gr.X(-1.1), gr.Y(0.25 * lim), G.COR.bronze);
      rotulo(ct, 'de fora', gr.X(2.1), gr.Y(-0.45 * lim), G.COR.ambar);
      rotulo(ct, 'o ciclo-limite', gr.X(0), gr.Y(0.86 * lim), G.COR.mestra);

      /* amplitude e período medidos */
      var ult = ciclo.slice(Math.floor(ciclo.length * 0.6));
      var amp = 0;
      ult.forEach(function (p) { amp = Math.max(amp, Math.abs(p[0])); });
      var zeros = [];
      for (var i = 0; i + 1 < ult.length; i++) {
        if (ult[i][0] < 0 && ult[i + 1][0] >= 0) zeros.push(i * dt);
      }
      var T = zeros.length >= 2
        ? (zeros[zeros.length - 1] - zeros[0]) / (zeros.length - 1) : NaN;

      rotulos(['Amplitude do ciclo', 'Período', 'A origem é',
               'T / μ  (limite 1,6137)']);
      painel({
        a: fmt(amp, 4),
        b: isFinite(T) ? fmt(T, 3) : '—',
        c: 'foco instável',
        d: isFinite(T) ? fmt(T / mu, 3) : '—'
      });

      texto.innerHTML =
        '<p>A equação é \\(\\ddot{x} - \\mu(1-x^2)\\dot{x} + x = 0\\), e o '
        + 'truque está no sinal: o amortecimento é <strong>negativo</strong> '
        + 'para \\(|x| &lt; 1\\), isto é, bombeia energia perto da origem, e '
        + 'positivo para \\(|x| &gt; 1\\), isto é, dissipa longe dela. Nem o '
        + 'repouso nem a amplitude grande sobrevivem, e entre os dois sobra '
        + 'uma órbita fechada.</p>'
        + '<p>Essa órbita é o <strong>ciclo-limite</strong>, e ela é '
        + '<em>única</em> e atrai todo mundo. As duas curvas finas partem de '
        + '\\(x = 0{,}05\\) e de \\(x = 3\\), e terminam na mesma curva: o '
        + 'programa mostra que as amplitudes coincidem em \\(10^{-9}\\).</p>'
        + '<p>Isso é uma <strong>oscilação autossustentada</strong>, e é '
        + 'coisa que sistema linear nenhum faz. No módulo 6 a amplitude vinha '
        + 'das condições iniciais e qualquer valor servia; aqui ela é '
        + 'propriedade do sistema, e o sistema a impõe de volta se for '
        + 'perturbado. É por isso que relógios, corações e neurônios podem '
        + 'funcionar: eles precisam de um ritmo que se restabeleça sozinho '
        + 'depois de um empurrão.</p>'
        + '<p>Com \\(\\mu\\) pequeno o ciclo é quase um círculo de raio 2 e o '
        + 'período é quase \\(2\\pi\\). Com \\(\\mu\\) grande ele vira uma '
        + 'oscilação de <strong>relaxação</strong>: cargas lentas seguidas de '
        + 'quedas rápidas, com \\(T \\simeq (3-2\\ln 2)\\mu\\). O mesmo '
        + 'amortecimento negativo do flutter do módulo 8, com a diferença de '
        + 'que aqui a não linearidade o segura.</p>';
      tipografar(texto);
    }

    function desenhar() {
      if (est.vista === 'pendulo') vistaPendulo();
      else if (est.vista === 'linear') vistaLinear();
      else vistaCiclo();
    }

    montar();
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
