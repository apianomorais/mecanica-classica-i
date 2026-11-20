# -*- coding: utf-8 -*-
"""Oscilações amortecidas: os três regimes, e por que o crítico é o melhor.

O QUE RESOLVE
    1. Confere as três soluções analíticas (subamortecida, crítica e
       superamortecida) contra a integração numérica da mesma equação.
    2. Mede a frequência de oscilação amortecida pelos cruzamentos de zero e
       compara com omega1 = sqrt(omega0^2 - gama^2).
    3. Mede o fator de qualidade de três jeitos diferentes (decremento
       logarítmico, energia perdida por ciclo e a fórmula omega0/2gama) e
       mostra que os três NAO dão o mesmo número, com as diferenças
       previstas em forma fechada.
    4. Mede o tempo de acomodação e descobre que o ótimo NAO é o
       amortecimento crítico, e sim um ligeiramente subamortecido: aquele
       cujo primeiro repique é do tamanho da tolerância exigida.
    5. Aplica a três casos reais: a suspensão de um carro, a porta com mola
       e o galvanômetro.

A FÍSICA
    Acrescentar -b v à força de uma mola muda a equação de
    x'' + omega0^2 x = 0 para x'' + 2 gama x' + omega0^2 x = 0. A solução
    deixa de ser uma senoide eterna e passa a depender de qual dos dois
    termos domina. O caso de fronteira, gama = omega0, não é apenas o limite
    matemático entre os outros dois: é o que todo projetista procura, porque
    é o mais rápido para voltar ao repouso sem ultrapassar.

COMO CONFERIR SE ESTÁ CERTO
    1. As três soluções fechadas têm de coincidir com a integração em erro
       de integrador, nos três regimes.
    2. A frequência medida nos cruzamentos tem de dar sqrt(omega0^2-gama^2)
       e NAO omega0: o amortecimento atrasa a oscilação.
    3. Q pelos picos tem de dar omega1/(2 gama), e portanto difere de
       omega0/(2 gama) pelo fator sqrt(1 - (gama/omega0)^2), exatamente.
       Q pela energia tem de dar 2 pi / (1 - exp(-2 pi / Q_picos)).
    4. O amortecimento que minimiza o tempo de acomodação tem de satisfazer
       exp(-pi z / sqrt(1-z^2)) = tolerância, com z = gama/omega0, e tem de
       se aproximar de 1 quando a tolerância aperta.

Prof. Apiano Morais - LFCA/URCA - Mecânica Clássica I
"""

import numpy as np


# =========================================== as três soluções analíticas
def solucao_analitica(t, w0, gama, x0, v0):
    """x(t) exato, nos três regimes, a partir das condições iniciais."""
    t = np.asarray(t, dtype=float)
    if gama < w0:                                   # subamortecido
        w1 = np.sqrt(w0 ** 2 - gama ** 2)
        A = x0
        B = (v0 + gama * x0) / w1
        return np.exp(-gama * t) * (A * np.cos(w1 * t) + B * np.sin(w1 * t))
    if np.isclose(gama, w0):                        # crítico
        return np.exp(-gama * t) * (x0 + (v0 + gama * x0) * t)
    # superamortecido
    r = np.sqrt(gama ** 2 - w0 ** 2)
    r1, r2 = -gama + r, -gama - r
    C1 = (v0 - r2 * x0) / (r1 - r2)
    C2 = (r1 * x0 - v0) / (r1 - r2)
    return C1 * np.exp(r1 * t) + C2 * np.exp(r2 * t)


def integra(w0, gama, x0, v0, t_fim, dt=1e-4):
    """Integra x'' = -2 gama x' - omega0^2 x por Runge-Kutta de 4a ordem.

    O Verlet dos módulos anteriores não serve aqui: ele supõe aceleração
    que depende só da posição, e a força de arrasto depende da velocidade.
    Usar Verlet com -2 gama v produz um amortecimento errado, que é um
    erro silencioso e difícil de notar.

    A aritmética é feita em floats soltos, e não em arranjos do numpy de
    dois elementos: para um sistema de duas equações, o custo de criar o
    arranjo a cada passo domina tudo o mais e deixa o programa dez vezes
    mais lento, o que aqui significa minutos em vez de segundos.
    """
    n = int(round(t_fim / dt))
    ts = np.empty(n + 1)
    xs = np.empty(n + 1)
    vs = np.empty(n + 1)
    x, v, t = float(x0), float(v0), 0.0
    ts[0], xs[0], vs[0] = t, x, v
    c, w2 = 2.0 * gama, w0 * w0

    for i in range(1, n + 1):
        k1x = v
        k1v = -c * v - w2 * x
        k2x = v + dt * k1v / 2
        k2v = -c * (v + dt * k1v / 2) - w2 * (x + dt * k1x / 2)
        k3x = v + dt * k2v / 2
        k3v = -c * (v + dt * k2v / 2) - w2 * (x + dt * k2x / 2)
        k4x = v + dt * k3v
        k4v = -c * (v + dt * k3v) - w2 * (x + dt * k3x)
        x += dt * (k1x + 2 * k2x + 2 * k3x + k4x) / 6
        v += dt * (k1v + 2 * k2v + 2 * k3v + k4v) / 6
        t += dt
        ts[i], xs[i], vs[i] = t, x, v
    return ts, xs, vs


# ======================================== medidas feitas sobre o sinal
def cruzamentos(ts, xs):
    """Instantes em que x passa por zero, por interpolação linear."""
    s = np.sign(xs)
    idx = np.where((s[:-1] < 0) & (s[1:] >= 0))[0]
    out = []
    for i in idx:
        f = -xs[i] / (xs[i + 1] - xs[i])
        out.append(ts[i] + f * (ts[i + 1] - ts[i]))
    return np.array(out)


def picos(ts, xs):
    """Máximos locais, por interpolação parabólica em três pontos."""
    out = []
    for i in range(1, len(xs) - 1):
        if xs[i] > xs[i - 1] and xs[i] >= xs[i + 1]:
            a, b, c = xs[i - 1], xs[i], xs[i + 1]
            d = 0.5 * (a - c) / (a - 2 * b + c)      # correção subamostral
            dt = ts[1] - ts[0]
            out.append((ts[i] + d * dt, b - 0.25 * (a - c) * d))
    return out


def tempo_de_acomodacao(ts, xs, tolerancia, x_ref):
    """Último instante em que |x| ainda excede a tolerância."""
    fora = np.where(np.abs(xs) > tolerancia * abs(x_ref))[0]
    return ts[fora[-1]] if len(fora) else 0.0


def main():
    print('=' * 72)
    print('1. AS TRES SOLUCOES, CONFERIDAS CONTRA A INTEGRACAO')
    print('=' * 72)
    w0, x0, v0 = 4.0, 1.0, 0.0
    print('   omega0 = %.1f rad/s, x0 = %.1f m, v0 = %.1f m/s' % (w0, x0, v0))
    print()
    print('   regime             gama    gama/omega0   maior diferenca')
    casos = [('subamortecido', 0.4), ('subamortecido', 2.0),
             ('CRITICO', 4.0), ('superamortecido', 8.0)]
    for nome, gama in casos:
        ts, xs, _ = integra(w0, gama, x0, v0, 6.0)
        exato = solucao_analitica(ts, w0, gama, x0, v0)
        print('   %-16s %6.2f   %9.2f     %.2e m'
              % (nome, gama, gama / w0, np.max(np.abs(xs - exato))))
    print()
    print('   As formas das tres solucoes nao se parecem: uma tem seno, a')
    print('   outra tem um t multiplicando a exponencial, a terceira tem duas')
    print('   exponenciais. Sao a MESMA solucao, escrita conforme o sinal de')
    print('   gama^2 - omega0^2, e a integracao numerica nao sabe disso: ela')
    print('   resolve a mesma equacao nos tres casos e acha a mesma curva.')
    print()

    print('=' * 72)
    print('2. O AMORTECIMENTO ATRASA A OSCILACAO')
    print('=' * 72)
    print('   gama    omega1 medido   sqrt(w0^2-gama^2)   diferenca   T/T0')
    for gama in (0.2, 0.8, 2.0, 3.0, 3.8):
        ts, xs, _ = integra(w0, gama, x0, v0, 40.0)
        z = cruzamentos(ts, xs)
        if len(z) >= 3:
            T = np.mean(np.diff(z))                 # entre cruzamentos iguais
            w_med = 2 * np.pi / T
        else:
            w_med = float('nan')
        w_prev = np.sqrt(w0 ** 2 - gama ** 2)
        print('   %5.2f   %12.8f   %16.8f   %.1e   %.4f'
              % (gama, w_med, w_prev, abs(w_med - w_prev), w0 / w_med))
    print()
    print('   Com gama = 3,8, que ja e 95 %% de omega0, o periodo e 3,2 vezes')
    print('   maior que o do oscilador livre. O amortecimento nao so encolhe')
    print('   a amplitude: ele atrasa o relogio, e e por isso que um pendulo')
    print('   dentro de oleo nao serve para medir o tempo.')
    print()

    print('=' * 72)
    print('3. TRES MANEIRAS DE MEDIR O FATOR DE QUALIDADE')
    print('=' * 72)
    print('   Tres definicoes que os livros tratam como a mesma:')
    print('     Q_formula = omega0 / (2 gama)')
    print('     Q_picos   = pi / decremento logaritmico entre picos vizinhos')
    print('     Q_energia = 2 pi / (fracao da energia perdida por ciclo)')
    print()
    print('   gama   Q_formula   Q_picos   razao medida   sqrt(1-(g/w0)^2)')
    for gama in (0.02, 0.1, 0.4, 1.0, 2.0, 3.0):
        ts, xs, vs = integra(w0, gama, x0, v0, 60.0)
        p = picos(ts, xs)
        Q_formula = w0 / (2 * gama)
        d = np.mean([np.log(p[i][1] / p[i + 1][1])
                     for i in range(len(p) - 1) if p[i + 1][1] > 1e-12])
        Q_picos = np.pi / d
        print('   %5.2f  %10.5f  %8.5f   %12.8f   %14.8f'
              % (gama, Q_formula, Q_picos, Q_picos / Q_formula,
                 np.sqrt(1 - (gama / w0) ** 2)))
    print()
    print('   As duas colunas da direita coincidem em todas as casas, e isso')
    print('   explica a discordancia: o decremento mede o periodo REAL, que')
    print('   e 2 pi / omega1, de modo que Q pelos picos vale omega1/(2 gama)')
    print('   e nao omega0/(2 gama). Com amortecimento fraco a diferenca some;')
    print('   com gama = 3, ela chega a 34 %.')
    print()
    print('   gama   Q_picos   Q_energia   razao medida   prevista   1+pi/Q')
    for gama in (0.02, 0.1, 0.4, 1.0):
        ts, xs, vs = integra(w0, gama, x0, v0, 60.0)
        p = picos(ts, xs)
        d = np.mean([np.log(p[i][1] / p[i + 1][1])
                     for i in range(len(p) - 1) if p[i + 1][1] > 1e-12])
        Q_picos = np.pi / d
        # nos picos a velocidade e nula, de modo que E = k x^2 / 2
        E = 0.5 * w0 ** 2 * np.array([q[1] for q in p]) ** 2
        perdas = [(E[i] - E[i + 1]) / E[i] for i in range(len(E) - 1)
                  if E[i] > 1e-20]
        Q_energia = 2 * np.pi / np.mean(perdas)
        u = 2 * np.pi / Q_picos
        prevista = u / (1 - np.exp(-u))      # exata, sem linearizar
        print('   %5.2f  %8.4f  %10.4f   %12.6f  %9.6f  %8.6f'
              % (gama, Q_picos, Q_energia, Q_energia / Q_picos, prevista,
                 1 + np.pi / Q_picos))
    print()
    print('   A coluna PREVISTA e (2 pi / Q) / (1 - exp(-2 pi / Q)), e ela')
    print('   bate com a medida em todas as casas. A razao e que a energia')
    print('   cai como exp(-2 gama t), de modo que a perda por ciclo vale')
    print('   1 - exp(-2 pi / Q), e nao 2 pi / Q. A ultima coluna e essa')
    print('   mesma previsao linearizada, 1 + pi/Q, que serve enquanto Q e')
    print('   grande e se afasta junto com tudo o mais quando Q cai.')
    print()
    print('   Repare no tamanho do efeito: mesmo com Q = 100, que e um')
    print('   oscilador bem pouco amortecido, as duas definicoes discordam')
    print('   em 3 %. Tres definicoes, tres numeros, e as diferencas sao')
    print('   previsiveis: nao e questao de precisao numerica.')
    print()

    print('=' * 72)
    print('4. QUAL AMORTECIMENTO LEVA AO REPOUSO MAIS DEPRESSA')
    print('=' * 72)
    print('   Deslocado de 1 m e solto. Tempo para entrar e ficar dentro de')
    print('   2 % do repouso:')
    print()
    print('   gama/omega0    regime            acomodacao (s)')
    for razao in (0.3, 0.6, 0.78, 0.9, 1.0, 1.1, 1.5, 3.0, 6.0):
        gama = razao * w0
        ts, xs, _ = integra(w0, gama, x0, v0, 20.0)
        ta = tempo_de_acomodacao(ts, xs, 0.02, x0)
        nome = ('subamortecido' if razao < 1 else
                'CRITICO' if razao == 1.0 else 'superamortecido')
        print('   %10.2f    %-16s  %10.4f' % (razao, nome, ta))
    print()
    print('   O minimo NAO esta no critico: esta em 0,78, e o critico demora')
    print('   62 % a mais. Isso contraria o que quase todo livro diz, e a')
    print('   explicacao e que o livro omite a letra miuda: o critico e o')
    print('   mais rapido entre os que NAO ULTRAPASSAM o repouso. Se um')
    print('   repique couber dentro da tolerancia exigida, vale a pena')
    print('   deixa-lo acontecer.')
    print()
    print('   O otimo e exatamente onde o primeiro repique tem o tamanho da')
    print('   tolerancia. Para z = gama/omega0, o repique vale')
    print('   exp(-pi z / sqrt(1 - z^2)), e igualar isso a tolerancia da:')
    print()
    print('   tolerancia   otimo medido   otimo previsto   critico   razao')
    for tol in (0.05, 0.02, 0.01, 0.002, 1e-4):
        melhor_t, melhor = 1e9, None
        for razao in np.arange(0.60, 1.401, 0.01):
            ts, xs, _ = integra(w0, razao * w0, x0, v0, 20.0, dt=2e-4)
            ta = tempo_de_acomodacao(ts, xs, tol, x0)
            if ta < melhor_t:
                melhor_t, melhor = ta, razao
        L = -np.log(tol) / np.pi
        z = np.sqrt(L * L / (1 + L * L))             # da equacao do repique
        ts, xs, _ = integra(w0, w0, x0, v0, 20.0, dt=2e-4)
        t_crit = tempo_de_acomodacao(ts, xs, tol, x0)
        print('   %10.4f   %12.2f   %14.3f   %7.4f   %5.2f'
              % (tol, melhor, z, t_crit, t_crit / melhor_t))
    print()
    print('   A previsao fechada acerta o otimo medido em todos os casos, e')
    print('   o otimo se aproxima do critico quando a tolerancia aperta: no')
    print('   limite de tolerancia zero, o critico volta a ser o melhor, que')
    print('   e exatamente o enunciado correto do teorema.')
    print()
    print('   Na pratica a suspensao de um carro fica em torno de 0,7, pelo')
    print('   mesmo motivo. Amortecedor gasto (z baixo) faz o carro quicar;')
    print('   amortecedor duro demais (z alto) transmite cada buraco a')
    print('   carroceria, porque nao tem tempo de ceder.')
    print()

    print('=' * 72)
    print('5. TRES SISTEMAS REAIS')
    print('=' * 72)
    print('   sistema                  Q       o que se quer')
    tabela = [
        ('suspensao de automovel', '~0,7', 'voltar rapido sem quicar'),
        ('porta com mola', '~0,7', 'fechar sem bater'),
        ('galvanometro analogico', '~0,7', 'ponteiro sem oscilar'),
        ('corda de violao (mi)', '~1 000', 'o som tem de durar'),
        ('diapasao', '~10 000', 'referencia de frequencia'),
        ('cristal de quartzo', '~100 000', 'relogio'),
    ]
    print('   (os tres primeiros em z = gama/omega0, os tres ultimos em Q)')
    for nome, Q, o_que in tabela:
        print('   %-24s %9s   %s' % (nome, Q, o_que))
    print()
    print('   Repare que nao existe Q bom ou ruim: existe Q adequado. Metade')
    print('   dos sistemas da lista foi projetada para perder energia o mais')
    print('   depressa possivel, e a outra metade para nao perder.')
    print()
    print('   Para uma corda de violao com Q = 1000 em 330 Hz, a amplitude')
    print('   cai a 1/e em Q / (pi f) = %.2f s, e o som ainda e audivel'
          % (1000.0 / (np.pi * 330.0)))
    print('   por alguns segundos depois disso. No cristal de quartzo de um')
    print('   relogio, a 32 768 Hz com Q = 1e5, o mesmo tempo e de %.2f s.'
          % (1e5 / (np.pi * 32768.0)))


if __name__ == '__main__':
    main()
