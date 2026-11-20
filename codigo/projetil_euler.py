# -*- coding: utf-8 -*-
"""Lançamento de projétil com arrasto, pelo método de Euler.

O QUE RESOLVE
    Integra o sistema de QUATRO equações de primeira ordem

        dx/dt  = vx
        dy/dt  = vy
        dvx/dt = -k |v| vx
        dvy/dt = -g - k |v| vy

    pelo método de Euler, pelo de Euler-Cromer e pelo Runge-Kutta de
    quarta ordem, e compara os três.

A FÍSICA
    Com arrasto quadrático não existe solução em fórmula fechada: a
    trajetória deixa de ser parábola, perde a simetria entre subida e
    descida, e o alcance cai. Isso não impede nada. A equação de movimento
    é uma equação diferencial, e qualquer equação diferencial pode ser
    integrada passo a passo, desde que se saiba o estado inicial.

    O ponto central do módulo está na palavra SISTEMA. Uma equação de
    segunda ordem vira duas de primeira; duas dimensões dobram a conta; e
    o método é exatamente o mesmo, aplicado a um vetor de estado em vez
    de a um número. Trocar quatro equações por quarenta não muda uma
    linha do método.

COMO CONFERIR SE ESTÁ CERTO
    1. Com k = 0, o alcance tem de convergir para v0^2 sen(2 theta)/g,
       que é o caso com solução conhecida.
    2. O erro de Euler tem de cair como Delta t (expoente 1) e o do RK4
       como (Delta t)^4 (expoente 4). Os expoentes são medidos, não
       supostos.
    3. A velocidade terminal medida na queda longa tem de bater com
       sqrt(g/k), que vem de igualar peso e arrasto.
    4. Euler-Cromer custa o mesmo que Euler e tambem e de primeira ordem.
       Aqui ele erra MAIS, e isso nao e defeito do programa: a vantagem
       dele aparece em problemas oscilatorios, em que conserva energia,
       e nao em acuracia bruta num voo balistico.

Prof. Apiano Morais - LFCA/URCA - Mecânica Clássica I
"""

import numpy as np

G = 9.81


def derivada(u, k):
    """f(u) para o estado u = [x, y, vx, vy]."""
    x, y, vx, vy = u
    v = np.hypot(vx, vy)
    return np.array([vx, vy, -k * v * vx, -G - k * v * vy])


def passo_euler(u, dt, k):
    return u + dt * derivada(u, k)


def passo_cromer(u, dt, k):
    """Atualiza as velocidades primeiro e usa as NOVAS nas posições."""
    d = derivada(u, k)
    vx = u[2] + dt * d[2]
    vy = u[3] + dt * d[3]
    return np.array([u[0] + dt * vx, u[1] + dt * vy, vx, vy])


def passo_rk4(u, dt, k):
    a = derivada(u, k)
    b = derivada(u + dt / 2 * a, k)
    c = derivada(u + dt / 2 * b, k)
    d = derivada(u + dt * c, k)
    return u + dt / 6 * (a + 2 * b + 2 * c + d)


METODOS = {'euler': passo_euler, 'cromer': passo_cromer, 'rk4': passo_rk4}


def voo(v0, ang, k, dt, metodo='euler', lim=20_000_000):
    """Integra até o projétil voltar ao chão e devolve o alcance.

    O alcance é interpolado entre os dois últimos pontos, para que o
    resultado não dependa de onde por acaso caiu o último passo. Sem
    isso, o erro medido seria dominado por esse detalhe e o expoente de
    convergência sairia errado.
    """
    th = np.radians(ang)
    u = np.array([0.0, 0.0, v0 * np.cos(th), v0 * np.sin(th)])
    avanca = METODOS[metodo]
    n = 0
    while n < lim:
        ant = u
        u = avanca(u, dt, k)
        n += 1
        if u[1] < 0.0:
            return pouso(ant, u, dt), n
    raise RuntimeError('não voltou ao chão')


def hermite(f0, d0, f1, d1, dt, s):
    """Interpolação cúbica de Hermite, que usa valor E derivada nas pontas."""
    s2, s3 = s * s, s * s * s
    return ((2 * s3 - 3 * s2 + 1) * f0
            + (s3 - 2 * s2 + s) * dt * d0
            + (-2 * s3 + 3 * s2) * f1
            + (s3 - s2) * dt * d1)


def pouso(ant, dep, dt):
    """Onde a trajetória cruza y = 0, entre os dois últimos estados.

    A tentação é interpolar y linearmente, e isso ARRUÍNA a medida: a
    interpolação linear erra em (Delta t)^2, de modo que o erro do RK4
    passa a cair como (Delta t)^2 em vez de (Delta t)^4, e o método
    parece pior do que é. Como o integrador fornece as velocidades, que
    são as derivadas de x e de y, a interpolação de Hermite sai de graça
    e erra em (Delta t)^4, que é o que o método merece.
    """
    a, b = 0.0, 1.0
    for _ in range(80):
        m = 0.5 * (a + b)
        if hermite(ant[1], ant[3], dep[1], dep[3], dt, m) > 0.0:
            a = m
        else:
            b = m
    s = 0.5 * (a + b)
    return hermite(ant[0], ant[2], dep[0], dep[2], dt, s)


def expoente(dts, erros):
    """Inclinação do ajuste log-log, que é a ordem do método."""
    bons = [(d, e) for d, e in zip(dts, erros) if e > 1e-12]
    if len(bons) < 3:
        return float('nan')
    d = np.log10([b[0] for b in bons])
    e = np.log10([b[1] for b in bons])
    return np.polyfit(d, e, 1)[0]


def main():
    v0, ang = 50.0, 45.0

    # ---------------------------------------- 1. o caso com solução conhecida
    exato = v0 ** 2 * np.sin(2 * np.radians(ang)) / G
    print('1. SEM ARRASTO: o alcance tem de convergir para a formula')
    print('   exato = v0^2 sen(2θ)/g = %.6f m' % exato)
    print('   dt (s)      Euler (m)      erro (m)       passos')
    dts = [0.4, 0.2, 0.1, 0.05, 0.025, 0.0125]
    erros = []
    for dt in dts:
        a, n = voo(v0, ang, 0.0, dt, 'euler')
        erros.append(abs(a - exato))
        print('   %7.4f    %10.6f    %10.3e    %8d' % (dt, a, erros[-1], n))
    print('   expoente medido = %.3f   (esperado 1)' % expoente(dts, erros))
    print()

    # ------------------------------------------------ 2. ordem dos três métodos
    k = 0.004
    ref, _ = voo(v0, ang, k, 1e-5, 'rk4')
    print('2. COM ARRASTO k = %.4f /m: referencia RK4 com dt = 1e-5 s' % k)
    print('   alcance de referencia = %.8f m' % ref)
    print('   (sem arrasto seriam %.3f m: o ar tira %.1f %%)'
          % (exato, 100 * (exato - ref) / exato))
    print()
    print('   dt (s)      erro Euler     erro Cromer    erro RK4')
    dts = [0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625]
    tab = {m: [] for m in METODOS}
    for dt in dts:
        linha = []
        for m in ('euler', 'cromer', 'rk4'):
            a, _ = voo(v0, ang, k, dt, m)
            tab[m].append(abs(a - ref))
            linha.append(abs(a - ref))
        print('   %7.5f    %10.3e    %10.3e    %10.3e'
              % (dt, linha[0], linha[1], linha[2]))
    print()
    for m, nome in (('euler', 'Euler'), ('cromer', 'Euler-Cromer'),
                    ('rk4', 'Runge-Kutta 4')):
        print('   %-14s expoente medido = %.3f' % (nome, expoente(dts, tab[m])))
    print()
    print('   Os tres expoentes sao os esperados: 1, 1 e 4. Repare que')
    print('   Euler-Cromer, apesar de custar o mesmo que Euler e de ser')
    print('   celebrado nos livros, erra MAIS aqui. A fama dele vem de outro')
    print('   lugar: em problemas oscilatorios ele nao deixa a energia')
    print('   crescer sem limite, e e isso, e nao a acuracia por passo, que o')
    print('   torna o metodo certo para orbitas e osciladores.')
    print()

    # ------------------------------------------------- 3. velocidade terminal
    print('3. VELOCIDADE TERMINAL: queda longa a partir do repouso')
    vt = np.sqrt(G / k)
    print('   esperada sqrt(g/k) = %.4f m/s' % vt)
    u = np.array([0.0, 5000.0, 0.0, 0.0])
    dt = 1e-3
    for _ in range(200_000):
        u = passo_rk4(u, dt, k)
        if u[1] <= 0:
            break
    print('   medida ao chegar ao chao = %.4f m/s' % abs(u[3]))
    print('   diferenca relativa = %.2e' % abs(abs(u[3]) / vt - 1))
    print()

    # ------------------------------------------------------ 4. o angulo otimo
    print('4. O ANGULO DE ALCANCE MAXIMO MUDA COM O ARRASTO')
    print('   k (1/m)     angulo otimo    alcance (m)')
    for kk in (0.0, 0.001, 0.004, 0.010, 0.020):
        melhor, amax = None, -1.0
        for ang_t in np.arange(20.0, 60.01, 1.0):
            a, _ = voo(v0, ang_t, kk, 1e-3, 'rk4')
            if a > amax:
                amax, melhor = a, ang_t
        print('   %7.4f     %6.1f°         %8.3f' % (kk, melhor, amax))
    print()
    print('   Sem ar, 45 graus. Com ar, o angulo otimo CAI, porque o tempo de')
    print('   voo longo da trajetoria alta cobra caro em arrasto. Esse')
    print('   resultado nao sai de formula nenhuma: sai de resolver o sistema')
    print('   muitas vezes e comparar.')


if __name__ == '__main__':
    main()
