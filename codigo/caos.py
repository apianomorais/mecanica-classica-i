# -*- coding: utf-8 -*-
"""Caos determinístico: o mapa logístico, Feigenbaum e o expoente de Lyapunov.

O QUE RESOLVE
    1. Acha os pontos fixos do mapa logístico e decide a estabilidade pelo
       critério |f'| < 1, conferindo contra a iteração.
    2. Localiza as bifurcações de duplicação de período pelos parâmetros
       superestáveis e mede a constante de Feigenbaum.
    3. Mede o expoente de Lyapunov em função do parâmetro e verifica o valor
       exato ln 2 em r = 4.
    4. Mostra que duas órbitas separadas por 1e-14 se afastam à taxa dada
       pelo expoente de Lyapunov, e calcula em quantas iterações a previsão
       se perde.
    5. Encontra a janela de período 3 e confere o início exato, 1 + sqrt(8).

A FÍSICA
    Caos não é desordem nem ruído: é sensibilidade exponencial às condições
    iniciais num sistema inteiramente determinístico. O mapa logístico é o
    exemplo mais barato que existe, com uma linha de conta por iteração, e
    tem tudo: pontos fixos, bifurcações, cascata, caos e janelas de ordem
    dentro do caos. O módulo 9 mostrou por que isso não cabe num plano de
    fase bidimensional, e é por isso que se começa por um mapa.

COMO CONFERIR SE ESTÁ CERTO
    1. A estabilidade prevista por |f'| < 1 tem de bater com o que a
       iteração faz.
    2. A primeira bifurcação tem de estar em r = 3 e a segunda em
       1 + sqrt(6) = 3,449490, com todas as casas.
    3. A razão entre intervalos sucessivos de bifurcação tem de convergir
       para 4,669201 (Feigenbaum).
    4. O expoente de Lyapunov em r = 4 tem de dar ln 2 = 0,693147.
    5. A janela de período 3 tem de começar em 1 + sqrt(8) = 3,828427.

Prof. Apiano Morais - LFCA/URCA - Mecânica Clássica I
"""

import numpy as np


# ================================================= o mapa e as suas derivadas
def f(x, r):
    return r * x * (1 - x)


def df(x, r):
    return r * (1 - 2 * x)


def itera(x0, r, n):
    """Devolve a órbita inteira, com n iterações."""
    xs = np.empty(n + 1)
    x = x0
    xs[0] = x
    for i in range(1, n + 1):
        x = r * x * (1 - x)
        xs[i] = x
    return xs


def orbita_final(x0, r, descarte=2000, guardar=1000):
    """Só o que sobra depois do transiente."""
    x = x0
    for _ in range(descarte):
        x = r * x * (1 - x)
    xs = np.empty(guardar)
    for i in range(guardar):
        x = r * x * (1 - x)
        xs[i] = x
    return xs


def periodo_da_orbita(xs, tol=1e-9, maximo=64):
    """Menor p tal que a órbita se repete com período p."""
    for p in range(1, maximo + 1):
        if np.max(np.abs(xs[p:] - xs[:-p])) < tol:
            return p
    return 0          # aperiódico dentro da tolerância


# ===================================== bifurcações pelos pontos superestáveis
def superestavel(n, a, b, tol=1e-14):
    """Parâmetro em que o ciclo de período 2^n contém x = 1/2.

    Esses são os parâmetros SUPERESTÁVEIS, em que a derivada do ciclo se
    anula (porque f'(1/2) = 0). Eles são melhores que os pontos de
    bifurcação para medir Feigenbaum: estão no meio de cada janela, são
    raízes simples de uma equação bem posta, e convergem para a mesma
    constante.

    Resolve g(r) = f^(2^n)(1/2) - 1/2 = 0 por bissecção.
    """
    m = 2 ** n

    def g(r):
        x = 0.5
        for _ in range(m):
            x = r * x * (1 - x)
        return x - 0.5

    ga, gb = g(a), g(b)
    if ga * gb > 0:
        return None
    for _ in range(200):
        c = 0.5 * (a + b)
        gc = g(c)
        if abs(b - a) < tol:
            break
        if ga * gc <= 0:
            b, gb = c, gc
        else:
            a, ga = c, gc
    return 0.5 * (a + b)


# ============================================== expoente de Lyapunov
def lyapunov(r, x0=0.3, descarte=3000, n=200000):
    """Média de ln|f'(x)| ao longo da órbita.

    Duas órbitas separadas por d0 se afastam como d0 exp(lambda n), de
    modo que lambda positivo significa sensibilidade exponencial. O
    cuidado numérico é descartar o transiente e evitar os pontos em que
    a derivada se anula, que dariam -infinito.
    """
    x = x0
    for _ in range(descarte):
        x = r * x * (1 - x)
    soma, contados = 0.0, 0
    for _ in range(n):
        d = abs(r * (1 - 2 * x))
        if d > 1e-300:
            soma += np.log(d)
            contados += 1
        x = r * x * (1 - x)
    return soma / contados


def main():
    print('=' * 72)
    print('1. PONTOS FIXOS E ESTABILIDADE')
    print('=' * 72)
    print('   O mapa x -> r x (1 - x) tem dois pontos fixos: x = 0 e')
    print('   x = 1 - 1/r. A estabilidade e decidida por |f\'(x)| < 1,')
    print('   que e o analogo discreto do criterio do modulo 9.')
    print()
    print('   r      x* = 1-1/r   f\'(x*)    previsao    orbita converge para')
    for r in (0.8, 1.5, 2.5, 2.9, 3.2):
        xe = 1 - 1 / r
        d = df(xe, r)
        prev = 'estavel' if abs(d) < 1 else 'instavel'
        xs = orbita_final(0.3, r, descarte=20000, guardar=200)
        p = periodo_da_orbita(xs)
        if r < 1:
            chegou = 'x = 0 (extincao)'
        elif p == 1:
            chegou = 'x = %.6f' % xs[-1]
        else:
            chegou = 'ciclo de periodo %d' % p
        print('   %4.1f   %10.6f   %+7.3f   %-9s   %s'
              % (r, xe, d, prev, chegou))
    print()
    print('   Abaixo de r = 1 o ponto fixo nao trivial nem existe no')
    print('   intervalo [0,1], e a populacao se extingue. Entre 1 e 3 ele e')
    print('   estavel. Em r = 3 a derivada passa por -1, e ai comeca tudo.')
    print()

    print('=' * 72)
    print('2. A CASCATA DE DUPLICACAO E A CONSTANTE DE FEIGENBAUM')
    print('=' * 72)
    print('   Os parametros superestaveis R_n, em que o ciclo de periodo')
    print('   2^n contem x = 1/2, sao obtidos por bisseccao:')
    print()
    print('   n    periodo    R_n              intervalo        razao')
    janelas = [(1.9, 2.1), (3.1, 3.3), (3.49, 3.55), (3.5540, 3.5700),
               (3.5660, 3.5700), (3.56890, 3.56999), (3.569930, 3.569950),
               (3.5699450, 3.5699460)]
    Rs = []
    for n, (a, b) in enumerate(janelas):
        R = superestavel(n, a, b)
        if R is None:
            continue
        Rs.append(R)
        if len(Rs) >= 3:
            d1 = Rs[-2] - Rs[-3]
            d2 = Rs[-1] - Rs[-2]
            print('   %d    %7d    %.12f   %.3e    %10.6f'
                  % (n, 2 ** n, R, d2, d1 / d2))
        else:
            print('   %d    %7d    %.12f' % (n, 2 ** n, R))
    print()
    print('   Valor de Feigenbaum: 4.669201609102990')
    print()
    print('   Conferencias independentes das duas primeiras bifurcacoes')
    print('   (que sao os valores em que o ciclo perde estabilidade, e nao')
    print('   os superestaveis acima):')
    print('     primeira:  r = 3           (exato)')
    print('     segunda:   r = 1 + sqrt(6) = %.12f' % (1 + np.sqrt(6)))
    for r, nome in ((2.999, 'antes de 3'), (3.001, 'depois de 3'),
                    (3.4494, 'antes de 1+sqrt(6)'),
                    (3.4496, 'depois de 1+sqrt(6)')):
        xs = orbita_final(0.3, r, descarte=400000, guardar=200)
        print('     r = %.4f (%-20s): periodo %d'
              % (r, nome, periodo_da_orbita(xs, tol=1e-7)))
    print()
    print('   A constante de Feigenbaum nao depende do mapa: qualquer mapa')
    print('   com um maximo quadratico da o mesmo 4,6692. E o primeiro')
    print('   exemplo de UNIVERSALIDADE que a maioria dos alunos encontra,')
    print('   e e por isso que ela merece o nome de constante.')
    print()

    print('=' * 72)
    print('3. O EXPOENTE DE LYAPUNOV')
    print('=' * 72)
    print('   lambda = media de ln|f\'(x)| ao longo da orbita. Negativo quer')
    print('   dizer que orbitas vizinhas se juntam; positivo, que se afastam')
    print('   exponencialmente.')
    print()
    print('   r         lambda        regime')
    for r in (2.5, 3.2, 3.5, 3.56, 3.569946, 3.7, 3.8284, 3.84, 3.9, 4.0):
        lam = lyapunov(r)
        if lam < -1e-6:
            regime = 'periodico'
        elif abs(lam) < 1e-3:
            regime = 'borda (bifurcacao ou janela)'
        else:
            regime = 'CAOTICO'
        print('   %9.6f   %+10.6f   %s' % (r, lam, regime))
    print()
    print('   Em r = 4 o valor exato e ln 2 = %.12f' % np.log(2))
    print('   medido:                        %.12f' % lyapunov(4.0))
    print()
    print('   Esse e um dos poucos casos em que o expoente sai em forma')
    print('   fechada: em r = 4 o mapa e conjugado a x -> 2x mod 1, que')
    print('   dobra a distancia a cada passo, e dobrar e exp(ln 2).')
    print()

    print('=' * 72)
    print('4. QUANTO TEMPO A PREVISAO DURA')
    print('=' * 72)
    r = 3.9
    lam = lyapunov(r)
    print('   Com r = %.1f, lambda = %.6f.' % (r, lam))
    print()
    print('   Duas orbitas que comecam separadas por 1e-14:')
    print()
    print('   iteracao   separacao medida   1e-14 * exp(lambda n)')
    a = itera(0.300000000000000, r, 60)
    b = itera(0.300000000000010, r, 60)
    for n in (0, 5, 10, 15, 20, 25, 30, 35):
        print('   %8d   %16.3e   %20.3e'
              % (n, abs(a[n] - b[n]), 1e-14 * np.exp(lam * n)))
    print()
    # a taxa medida num par só flutua: lambda é uma MÉDIA ao longo da
    # órbita, e trechos curtos esticam mais ou menos que ela
    taxa_par = np.log(abs(a[35] - b[35]) / abs(a[0] - b[0])) / 35
    somas = []
    rng = np.random.default_rng(7)
    for _ in range(400):
        x0 = rng.uniform(0.05, 0.95)
        u = itera(x0, r, 35)
        w = itera(x0 + 1e-14, r, 35)
        if abs(w[35] - u[35]) > 0:
            somas.append(np.log(abs(w[35] - u[35]) / 1e-14) / 35)
    print('   taxa medida NESTE par de orbitas:        %+.6f' % taxa_par)
    print('   media sobre 400 pares com inicios ao acaso: %+.6f'
          % float(np.mean(somas)))
    print('   expoente de Lyapunov:                    %+.6f' % lam)
    print()
    print('   Um par so nao basta: a taxa dele fica 9 % acima do expoente,')
    print('   porque lambda e uma MEDIA ao longo da orbita e trechos curtos')
    print('   esticam mais ou menos que ela. A media sobre quatrocentos')
    print('   pares converge para o valor certo. Confundir a flutuacao de')
    print('   uma amostra com erro de conta e um engano comum aqui.')
    print()
    n_perda = np.log(0.1 / 1e-14) / lam
    print('   A separacao cresce como previsto ate saturar em 0,1, que e a')
    print('   largura do atrator: dali em diante as duas orbitas nao tem')
    print('   mais relacao nenhuma. Isso acontece em n = %.0f iteracoes.'
          % n_perda)
    print()
    print('   A conta geral vale a pena guardar: para ganhar UMA casa')
    print('   decimal a mais de previsao e preciso melhorar a condicao')
    print('   inicial em um fator 10, e isso compra apenas')
    print('   ln(10)/lambda = %.1f iteracoes a mais.' % (np.log(10) / lam))
    print()

    print('=' * 72)
    print('5. ORDEM DENTRO DO CAOS: A JANELA DE PERIODO 3')
    print('=' * 72)
    inicio = 1 + np.sqrt(8)
    print('   A janela de periodo 3 comeca exatamente em 1 + sqrt(8) = %.12f'
          % inicio)
    print()
    print('   r            periodo   lambda')
    for r in (inicio - 0.001, inicio - 0.0001, inicio + 0.0001,
              inicio + 0.001, 3.83, 3.84, 3.8495, 3.8500):
        xs = orbita_final(0.3, r, descarte=200000, guardar=90)
        p = periodo_da_orbita(xs, tol=1e-6)
        print('   %.6f   %7s   %+10.6f'
              % (r, p if p else 'aperiod.', lyapunov(r)))
    print()
    print('   Antes de 3,828427 a orbita e aperiodica e lambda e positivo;')
    print('   depois dela aparece um ciclo de periodo 3 e lambda fica')
    print('   negativo. A janela tambem tem a sua propria cascata (3, 6,')
    print('   12, ...) e termina em caos de novo, perto de 3,8495.')
    print()
    print('   O teorema de Sarkovskii diz algo mais forte: num mapa')
    print('   continuo do intervalo, a existencia de uma orbita de periodo')
    print('   3 implica a existencia de orbitas de TODOS os periodos. E o')
    print('   titulo do artigo de Li e Yorke de 1975, que introduziu a')
    print('   palavra caos: "Period three implies chaos".')


if __name__ == '__main__':
    main()
