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
    var est = { v0: 50, ang: 45, k: 0.004, dt: 0.2, vista: 'traj' };
    var g = 9.81;

    /* ---- o sistema de equações ----
       O estado é u = [x, y, vx, vy] e a derivada é f(u). Escrever
       assim, como vetor, é o que permite usar o MESMO passo de Euler
       para qualquer número de equações. */
    function f(u, k) {
      var vx = u[2], vy = u[3];
      var v = Math.sqrt(vx * vx + vy * vy);
      return [vx, vy, -k * v * vx, -g - k * v * vy];
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
      traco(ref.pts, G.COR.mestra, 2.4);
      traco(eu.pts, G.COR.bronze, 2);

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
        { texto: 'referência (RK4, Δt = 0,5 ms)', cor: G.COR.mestra },
        { texto: 'Euler, Δt escolhido', cor: G.COR.bronze },
        { texto: 'parábola sem arrasto', cor: '#b9c6c2' }
      ]);

      var err = Math.abs(eu.alcance - ref.alcance);
      rotulos(['Alcance (Euler)', 'Alcance (referência)', 'Erro', 'Passos']);
      painel({
        ae: fmt(eu.alcance, 2) + ' m',
        ar: fmt(ref.alcance, 2) + ' m',
        er: fmt(err, 2) + ' m (' + fmt(100 * err / ref.alcance, 1) + '%)',
        np: String(eu.passos)
      });

      texto.innerHTML =
        '<p>A curva tracejada é a parábola de sempre, a que vale quando não há '
        + 'ar. Com arrasto, o alcance cai de ' + fmt(semAr, 1) + ' m para '
        + fmt(ref.alcance, 1) + ' m, e a trajetória perde a simetria: a subida '
        + 'é mais longa que a descida, e a queda fica mais íngreme. Nenhuma '
        + 'fórmula fechada descreve essa curva.</p>'
        + '<p>A curva em bronze é o que o método de Euler produz com o passo '
        + 'escolhido. Diminua \\(\\Delta t\\) e ela encosta na referência; '
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
      var ref = vref.alcance;
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
               'Alcance de referência', 'Método']);
      painel({
        ae: fmt(mE, 2),
        ar: fmt(mR, 2),
        er: fmt(ref, 2) + ' m',
        np: 'RK4, Δt = 50 µs'
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
