# -*- coding: utf-8 -*-
"""Trabalho, energia e o que distingue uma força conservativa.

O QUE RESOLVE
    1. Calcula o trabalho de uma força ao longo de caminhos diferentes entre
       os mesmos dois pontos, e mostra em números o que significa o trabalho
       não depender do caminho.
    2. Testa se uma força é conservativa pelo rotacional, calculado por
       diferenças finitas, e confere contra o teste do caminho fechado.
    3. Lê o movimento inteiro no gráfico de U(x): pontos de retorno,
       regiões proibidas e o período da oscilação por quadratura, conferido
       contra a integração da equação de movimento.
    4. Mede a deriva da energia de quatro integradores ao longo de duzentos
       períodos, que é onde o Euler-Cromer finalmente mostra a que veio.

A FÍSICA
    Uma força é conservativa quando o trabalho entre dois pontos não depende
    do caminho, o que é a mesma coisa que o trabalho ser nulo em qualquer
    caminho fechado, o que é a mesma coisa que existir uma energia potencial
    U com F = -grad U, o que é a mesma coisa que o rotacional ser nulo. As
    quatro afirmações são equivalentes, e o programa verifica as quatro na
    mesma força para que a equivalência deixe de ser uma frase decorada.

COMO CONFERIR SE ESTÁ CERTO
    1. Para a força conservativa, os dois caminhos têm de dar o mesmo
       trabalho, igual a -(U_final - U_inicial), em erro de quadratura.
    2. Para a força não conservativa, os dois caminhos têm de discordar, e a
       diferença tem de ser igual ao fluxo do rotacional pela área entre
       eles, que é o teorema de Green.
    3. O período por quadratura tem de bater com o período medido na
       integração numérica em cinco casas.
    4. No oscilador harmônico, o Euler ganha energia, o Euler-Cromer e o
       Verlet oscilam em torno do valor certo sem deriva, e o RK4 perde
       energia devagar. Essa é a diferença entre ordem e simplecticidade.

Prof. Apiano Morais - LFCA/URCA - Mecânica Clássica I
"""

import numpy as np

# ===================================================== 1. trabalho e caminho

def forca_conservativa(x, y):
    """F = (y^2, 2xy), que vem de U = -x y^2."""
    return np.array([y ** 2, 2 * x * y])


def potencial(x, y):
    return -x * y ** 2


def forca_rotacional(x, y):
    """F = (-y, x), o exemplo mais limpo de força com rotacional."""
    return np.array([-y, x])


def trabalho(campo, caminho, n=200000):
    """Integral de linha de F . dr ao longo de um caminho parametrizado.

    O caminho é uma função de s em [0, 1] que devolve o ponto (x, y). A
    derivada é calculada por diferença centrada, e a integral pela regra
    do trapézio, que basta de sobra para a precisão que queremos aqui.
    """
    s = np.linspace(0.0, 1.0, n + 1)
    pts = np.array([caminho(si) for si in s])
    dr = np.gradient(pts, s, axis=0)
    integrando = np.array([np.dot(campo(p[0], p[1]), d) for p, d in zip(pts, dr)])
    return np.trapezoid(integrando, s)


def reta(a, b):
    a, b = np.array(a, float), np.array(b, float)
    return lambda s: a + s * (b - a)


def duas_pernas(a, b):
    """Primeiro anda em x, depois em y."""
    a, b = np.array(a, float), np.array(b, float)
    def c(s):
        if s < 0.5:
            return np.array([a[0] + 2 * s * (b[0] - a[0]), a[1]])
        return np.array([b[0], a[1] + (2 * s - 1) * (b[1] - a[1])])
    return c


def arco(a, b):
    """Um arco de senoide entre os dois pontos, só para ser um terceiro."""
    a, b = np.array(a, float), np.array(b, float)
    def c(s):
        p = a + s * (b - a)
        n = np.array([-(b - a)[1], (b - a)[0]])
        return p + 0.35 * np.sin(np.pi * s) * n
    return c


# ========================================================== 2. o rotacional

def rotacional(campo, x, y, h=1e-5):
    """Componente z de rot F, por diferença centrada."""
    fx_mais = campo(x, y + h)[0]
    fx_menos = campo(x, y - h)[0]
    fy_mais = campo(x + h, y)[1]
    fy_menos = campo(x - h, y)[1]
    return (fy_mais - fy_menos) / (2 * h) - (fx_mais - fx_menos) / (2 * h)


def circuito(campo, raio=1.0, centro=(0.5, 0.5), n=400000):
    """Trabalho ao longo de uma circunferência percorrida uma vez."""
    th = np.linspace(0.0, 2 * np.pi, n + 1)
    x = centro[0] + raio * np.cos(th)
    y = centro[1] + raio * np.sin(th)
    dx, dy = -raio * np.sin(th), raio * np.cos(th)
    f = np.array([campo(xi, yi) for xi, yi in zip(x, y)])
    return np.trapezoid(f[:, 0] * dx + f[:, 1] * dy, th)


# ================================================ 3. ler o movimento em U(x)

A_POCO, U0 = 1.0, 1.0
MASSA = 1.0


def U(x):
    """Poço duplo, o exemplo mais barato de potencial que não é parábola.

    U(x) = U0 [ (x/a)^4 - 2 (x/a)^2 ], com mínimos em x = +-a, valendo
    -U0, e uma barreira em x = 0, valendo zero.
    """
    u = x / A_POCO
    return U0 * (u ** 4 - 2 * u ** 2)


def dU(x):
    u = x / A_POCO
    return U0 * (4 * u ** 3 - 4 * u) / A_POCO


def pontos_de_retorno(E):
    """Onde U(x) = E, no poço da direita, para -U0 < E < 0.

    Resolvendo a biquadrada: u^2 = 1 +- sqrt(1 + E/U0).
    """
    if not (-U0 < E < 0):
        raise ValueError('esta rotina só trata o poço da direita')
    r = np.sqrt(1 + E / U0)
    return A_POCO * np.sqrt(1 - r), A_POCO * np.sqrt(1 + r)


def periodo_por_quadratura(E, n=200000):
    """T = int dx sqrt(2m / (E - U)), de um ponto de retorno ao outro.

    A ida e a volta levam o mesmo tempo, de modo que o período é duas
    vezes a integral de dx/v, e o dois cancela com o meio que vem de
    v = sqrt(2(E-U)/m). Quem põe um 2 a mais na frente acha o dobro do
    período, que foi o que aconteceu aqui na primeira tentativa.

    O integrando diverge nos pontos de retorno, mas a divergência é
    integrável. A substituição x = (b+a)/2 + (b-a)/2 sen(th) a cancela
    exatamente quando os dois pontos de retorno são simples, que é o caso
    aqui. Mesmo assim, usamos a regra do ponto médio: ela nunca avalia o
    integrando nos extremos, onde o arredondamento pode fazer E - U dar
    negativo por 1e-17 e produzir um número absurdo.
    """
    a, b = pontos_de_retorno(E)
    meio, semi = (a + b) / 2, (b - a) / 2
    passo = np.pi / n
    th = -np.pi / 2 + passo * (np.arange(n) + 0.5)
    x = meio + semi * np.sin(th)
    integrando = np.sqrt(2 * MASSA / (E - U(x))) * semi * np.cos(th)
    return float(np.sum(integrando) * passo)


def periodo_por_integracao(E, dt=1e-6):
    """O mesmo período, medido soltando a partícula do ponto de retorno.

    Solto em repouso no ponto de retorno interno, a partícula vai até o
    externo e volta. O período é duas vezes o tempo de ida, e o instante
    da chegada sai por interpolação em v, que cruza zero linearmente.
    """
    a, _ = pontos_de_retorno(E)
    x, v = a, 0.0
    t = 0.0
    v_ant, t_ant = v, t
    # velocity-Verlet, para o tempo medido não depender do integrador
    acc = -dU(x) / MASSA
    while True:
        x_novo = x + v * dt + 0.5 * acc * dt * dt
        acc_novo = -dU(x_novo) / MASSA
        v_novo = v + 0.5 * (acc + acc_novo) * dt
        t += dt
        if t > 2 * dt and v_novo <= 0 < v:      # chegou ao retorno externo
            frac = v / (v - v_novo)
            return 2 * (t - dt + frac * dt)
        v_ant, t_ant = v, t
        x, v, acc = x_novo, v_novo, acc_novo
        if t > 1e4:
            raise RuntimeError('não voltou')


# ============================================ 4. energia e integradores

OMEGA = 1.0


def energia_harmonico(x, v):
    return 0.5 * MASSA * v ** 2 + 0.5 * MASSA * OMEGA ** 2 * x ** 2


def integrar(metodo, x0, v0, dt, passos):
    """Energia final e o maior desvio relativo, no começo e no fim.

    Medir o desvio nos primeiros vinte períodos e nos últimos vinte
    separa as duas coisas que se confundem: um método simplético faz a
    energia OSCILAR com amplitude fixa, e um método dissipativo faz a
    energia DERIVAR. Só a segunda cresce com o tempo.
    """
    x, v = x0, v0
    e0 = energia_harmonico(x, v)
    pior = 0.0
    por_periodo = 2 * np.pi / dt
    inicio = int(20 * por_periodo)
    comeco_do_fim = passos - inicio
    pior_cedo, pior_tarde = 0.0, 0.0
    for passo in range(passos):
        if metodo == 'euler':
            a = -OMEGA ** 2 * x
            x, v = x + dt * v, v + dt * a
        elif metodo == 'cromer':
            a = -OMEGA ** 2 * x
            v = v + dt * a
            x = x + dt * v
        elif metodo == 'verlet':
            a = -OMEGA ** 2 * x
            x = x + dt * v + 0.5 * dt * dt * a
            a2 = -OMEGA ** 2 * x
            v = v + 0.5 * dt * (a + a2)
        elif metodo == 'rk4':
            def f(s):
                return np.array([s[1], -OMEGA ** 2 * s[0]])
            s = np.array([x, v])
            k1 = f(s)
            k2 = f(s + dt * k1 / 2)
            k3 = f(s + dt * k2 / 2)
            k4 = f(s + dt * k3)
            s = s + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
            x, v = s[0], s[1]
        e = energia_harmonico(x, v)
        d = abs(e - e0) / e0
        pior = max(pior, d)
        if passo < inicio:
            pior_cedo = max(pior_cedo, d)
        elif passo >= comeco_do_fim:
            pior_tarde = max(pior_tarde, d)
    return energia_harmonico(x, v) / e0, pior, pior_cedo, pior_tarde


def main():
    print('=' * 72)
    print('1. O TRABALHO DEPENDE DO CAMINHO?')
    print('=' * 72)
    a, b = (0.0, 0.0), (1.0, 1.0)
    print('   De (0,0) a (1,1).')
    print()
    print('   Forca CONSERVATIVA  F = (y^2, 2xy),  vinda de U = -x y^2')
    for nome, cam in (('reta', reta(a, b)), ('duas pernas', duas_pernas(a, b)),
                      ('arco', arco(a, b))):
        print('     %-14s W = %+.10f' % (nome, trabalho(forca_conservativa, cam)))
    print('     -(U_b - U_a)     W = %+.10f' % (-(potencial(*b) - potencial(*a))))
    print()
    print('   Forca com ROTACIONAL  F = (-y, x),  que nao vem de potencial algum')
    for nome, cam in (('reta', reta(a, b)), ('duas pernas', duas_pernas(a, b)),
                      ('arco', arco(a, b))):
        print('     %-14s W = %+.10f' % (nome, trabalho(forca_rotacional, cam)))
    print()
    print('   Os tres caminhos concordam na primeira e discordam na segunda.')
    print('   Nao e questao de precisao: a diferenca entre a reta e as duas')
    print('   pernas, %+.6f, e exatamente o dobro da area do triangulo entre'
          % (trabalho(forca_rotacional, duas_pernas(a, b))
             - trabalho(forca_rotacional, reta(a, b))))
    print('   elas, que vale 1/2. Isso e o teorema de Green com rot F = 2.')
    print()

    print('=' * 72)
    print('2. O TESTE DO ROTACIONAL E O TESTE DO CAMINHO FECHADO')
    print('=' * 72)
    print('   ponto        rot F conservativa     rot F rotacional')
    for p in ((0.3, 0.7), (1.0, 1.0), (-0.5, 2.0)):
        print('   (%+.1f,%+.1f)      %+.3e            %+.6f'
              % (p[0], p[1], rotacional(forca_conservativa, *p),
                 rotacional(forca_rotacional, *p)))
    print()
    wc = circuito(forca_conservativa)
    wr = circuito(forca_rotacional)
    print('   Trabalho numa volta fechada de raio 1:')
    print('     conservativa:  W = %+.3e   (zero, a menos de arredondamento)' % wc)
    print('     com rotacional: W = %+.6f   contra 2 pi = %.6f'
          % (wr, 2 * np.pi))
    print()
    print('   Repare que 2 pi e o rotacional, 2, vezes a area do circulo, pi.')
    print('   O teste local e o teste global sao a mesma informacao.')
    print()

    print('=' * 72)
    print('3. LENDO O MOVIMENTO NO GRAFICO DE U(x)')
    print('=' * 72)
    print('   Poco duplo U(x) = (x^4 - 2x^2), com minimos em x = +-1 valendo -1')
    print('   e barreira em x = 0 valendo 0.')
    print()
    print('      E       retorno interno   retorno externo    T quadratura    T integrado')
    for E in (-0.9, -0.75, -0.5, -0.25, -0.1):
        xi, xe = pontos_de_retorno(E)
        tq = periodo_por_quadratura(E)
        ti = periodo_por_integracao(E)
        print('   %+.2f        %8.5f         %8.5f        %10.6f     %10.6f'
              % (E, xi, xe, tq, ti))
    print()
    print('   Os dois caminhos dao o mesmo periodo, e sao coisas bem')
    print('   diferentes: o primeiro e uma integral sobre a POSICAO, tirada do')
    print('   grafico de U sem resolver equacao nenhuma; o segundo anda no')
    print('   tempo resolvendo a equacao de movimento.')
    print()
    om2 = (dU(1.0 + 1e-6) - dU(1.0 - 1e-6)) / (2e-6) / MASSA
    print('   Perto do fundo do poco o movimento vira harmonico. A curvatura')
    print('   ali vale U\'\'(1) = %.4f, de modo que o periodo tende a' % om2)
    print('     T -> 2 pi / sqrt(U\'\'/m) = %.6f' % (2 * np.pi / np.sqrt(om2)))
    print('   e e para esse numero que a coluna da quadratura caminha quando')
    print('   a energia se aproxima do fundo, -1.')
    print()

    print('=' * 72)
    print('4. A ENERGIA SOBREVIVE AO INTEGRADOR?')
    print('=' * 72)
    print('   Oscilador harmonico, omega = 1, x0 = 1, v0 = 0, dt = 0,01,')
    print('   integrado por 200 periodos (%d passos).'
          % int(200 * 2 * np.pi / 0.01))
    print()
    passos = int(200 * 2 * np.pi / 0.01)
    print('   metodo            E_final/E_0 - 1   desvio nos 20      nos 20')
    print('                                        primeiros per.   ultimos per.')
    for met, nome in (('euler', 'Euler'), ('cromer', 'Euler-Cromer'),
                      ('verlet', 'Verlet'), ('rk4', 'RK4')):
        raz, pior, cedo, tarde = integrar(met, 1.0, 0.0, 0.01, passos)
        print('   %-16s  %+14.3e    %10.2e    %10.2e'
              % (nome, raz - 1, cedo, tarde))
    print()
    print('   As duas ultimas colunas separam o que se costuma confundir. No')
    print('   Euler-Cromer e no Verlet o desvio e o MESMO no comeco e no fim:')
    print('   a energia oscila, com amplitude fixa, e nao vai a lugar nenhum.')
    print('   No Euler ele cresce sem parar. No RK4 ele cresce tambem, so que')
    print('   devagar e para baixo: o sinal negativo na primeira coluna diz')
    print('   que o metodo mais preciso dos quatro esta perdendo energia.')
    print()
    print('   Aqui esta o que o modulo 3 prometeu. O Euler e o RK4 nao')
    print('   conservam energia: o primeiro ganha, e sem limite; o segundo')
    print('   perde, devagar, mas perde sempre. O Euler-Cromer e o Verlet')
    print('   mantem a energia oscilando em torno do valor certo, e a oscilacao')
    print('   nao cresce com o tempo. Eles nao sao mais precisos, sao')
    print('   SIMPLECTICOS: preservam a estrutura do espaco de fase, e por isso')
    print('   sao os metodos de quem vai integrar orbitas por milhoes de anos.')


if __name__ == '__main__':
    main()
