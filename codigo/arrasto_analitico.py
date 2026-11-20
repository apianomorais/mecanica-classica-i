# -*- coding: utf-8 -*-
"""Resistência do ar: o que se resolve no papel, e a conferência numérica.

O QUE RESOLVE
    Reúne as soluções FECHADAS da queda e do lançamento com arrasto, nos
    casos em que elas existem, e compara cada uma com a integração
    numérica do mesmo problema:

    1. arrasto linear em uma dimensão: v(t) e y(t) por exponenciais;
    2. arrasto linear em duas dimensões: x(t) e y(t), ainda exatos,
       porque as componentes continuam desacopladas;
    3. arrasto quadrático na subida: v(t) por tangente;
    4. arrasto quadrático na queda: v(t) por tangente hiperbólica;
    5. arrasto quadrático em duas dimensões: NÃO tem solução fechada, e o
       programa mostra por que a tentativa de separar falha.

A FÍSICA
    A fronteira entre o que se resolve e o que não se resolve não é de
    dificuldade, e sim de ESTRUTURA. Com arrasto linear, a força é uma
    função linear de cada componente da velocidade, e o sistema se separa
    em duas equações independentes, cada uma com solução exponencial. Com
    arrasto quadrático, aparece |v| = sqrt(vx^2 + vy^2), que mistura as
    componentes: em uma dimensão isso é inofensivo, porque |v| = |v|, mas
    em duas dimensões acopla tudo e nenhuma função elementar dá conta.

COMO CONFERIR SE ESTÁ CERTO
    1. Cada solução fechada tem de coincidir com o RK4 em 1e-10 ou
       melhor. Se não coincidir, uma das duas está errada.
    2. O erro do Euler contra a solução EXATA tem de cair como Delta t,
       e esse é o teste mais limpo da ordem do método, porque aqui a
       referência não tem erro nenhum.
    3. Os limites têm de fechar: com k -> 0 as fórmulas com arrasto
       precisam devolver a cinemática de sempre.

Prof. Apiano Morais - LFCA/URCA - Mecânica Clássica I
"""

import numpy as np

G = 9.81


# ===================================================== soluções fechadas
def linear_1d(t, v0, tau):
    """Arrasto linear, uma dimensão: v(t) e y(t) exatos.

    m dv/dt = -mg - m v/tau  =>  v(t) = (v0 + vt) e^{-t/tau} - vt
    """
    vt = G * tau
    v = (v0 + vt) * np.exp(-t / tau) - vt
    y = (v0 + vt) * tau * (1 - np.exp(-t / tau)) - vt * t
    return v, y


def linear_2d(t, vx0, vy0, tau):
    """Arrasto linear, duas dimensões: ainda exato, porque separa."""
    vt = G * tau
    x = vx0 * tau * (1 - np.exp(-t / tau))
    y = (vy0 + vt) * tau * (1 - np.exp(-t / tau)) - vt * t
    vx = vx0 * np.exp(-t / tau)
    vy = (vy0 + vt) * np.exp(-t / tau) - vt
    return x, y, vx, vy


def quadratico_subida(t, v0, k):
    """Arrasto quadrático subindo: v(t) = vt tan(theta0 - g t/vt)."""
    vt = np.sqrt(G / k)
    th0 = np.arctan(v0 / vt)
    return vt * np.tan(th0 - G * t / vt)


def quadratico_subida_marcos(v0, k):
    """Tempo de subida e altura máxima, em fórmula fechada."""
    vt = np.sqrt(G / k)
    t_sub = vt / G * np.arctan(v0 / vt)
    h_max = vt ** 2 / (2 * G) * np.log(1 + v0 ** 2 / vt ** 2)
    return t_sub, h_max


def quadratico_queda(t, k):
    """Arrasto quadrático caindo do repouso: v(t) = vt tanh(g t/vt)."""
    vt = np.sqrt(G / k)
    return vt * np.tanh(G * t / vt), vt ** 2 / G * np.log(np.cosh(G * t / vt))


# =========================================================== integradores
def rk4_1d(f, y0, T, n):
    y, dt = float(y0), T / n
    for _ in range(n):
        a = f(y)
        b = f(y + dt / 2 * a)
        c = f(y + dt / 2 * b)
        d = f(y + dt * c)
        y += dt / 6 * (a + 2 * b + 2 * c + d)
    return y


def euler_1d(f, y0, T, n):
    y, dt = float(y0), T / n
    for _ in range(n):
        y += dt * f(y)
    return y


def rk4_sistema(f, u0, T, n):
    u, dt = np.array(u0, float), T / n
    for _ in range(n):
        a = f(u)
        b = f(u + dt / 2 * a)
        c = f(u + dt / 2 * b)
        d = f(u + dt * c)
        u = u + dt / 6 * (a + 2 * b + 2 * c + d)
    return u


def main():
    print('=' * 68)
    print('1. ARRASTO LINEAR EM UMA DIMENSAO')
    print('=' * 68)
    tau, v0, T = 3.0, 20.0, 2.0
    vt = G * tau
    print('   tau = %.1f s, velocidade terminal vt = g tau = %.2f m/s' % (tau, vt))
    v_ex, y_ex = linear_1d(T, v0, tau)
    f = lambda v: -G - v / tau
    v_rk = rk4_1d(f, v0, T, 200000)
    print('   v(%.0f s):  fechada %.10f    RK4 %.10f    dif %.1e'
          % (T, v_ex, v_rk, abs(v_ex - v_rk)))
    print()
    print('   erro do Euler contra a solucao EXATA (sem referencia numerica):')
    print('   dt (s)        v numerico        erro        razao')
    ant = None
    for n in (200, 2000, 20000, 200000):
        dt = T / n
        e = abs(euler_1d(f, v0, T, n) - v_ex)
        r = '   -' if ant is None else '%6.2f' % (ant / e)
        print('   %9.6f     %12.8f    %9.3e   %s' % (dt, euler_1d(f, v0, T, n), e, r))
        ant = e
    print('   A razao tende a 10 ao dividir o passo por 10: ordem 1, medida')
    print('   contra a verdade e nao contra outra aproximacao.')
    print()

    print('=' * 68)
    print('2. ARRASTO LINEAR EM DUAS DIMENSOES: ainda exato')
    print('=' * 68)
    vx0, vy0, T = 35.0, 35.0, 4.0
    x_ex, y_ex, vx_ex, vy_ex = linear_2d(T, vx0, vy0, tau)
    g2 = lambda u: np.array([u[2], u[3], -u[2] / tau, -G - u[3] / tau])
    u = rk4_sistema(g2, [0, 0, vx0, vy0], T, 400000)
    print('   t = %.0f s' % T)
    print('   x:  fechada %.8f   RK4 %.8f   dif %.1e'
          % (x_ex, u[0], abs(x_ex - u[0])))
    print('   y:  fechada %.8f   RK4 %.8f   dif %.1e'
          % (y_ex, u[1], abs(y_ex - u[1])))
    print()
    print('   Por que separa: a forca e -b*vx na horizontal e -mg - b*vy na')
    print('   vertical. Nenhuma das duas menciona a outra componente, de modo')
    print('   que sao duas equacoes independentes de primeira ordem.')
    print()
    print('   A assintota vertical: x nunca passa de vx0*tau = %.3f m,' % (vx0 * tau))
    print('   por mais que se espere. O projetil cai na vertical no fim.')
    print()

    print('=' * 68)
    print('3. ARRASTO QUADRATICO EM UMA DIMENSAO')
    print('=' * 68)
    k = 0.004
    vtq = np.sqrt(G / k)
    print('   k = %.4f /m, vt = sqrt(g/k) = %.4f m/s' % (k, vtq))
    print()
    print('   SUBIDA, v(t) = vt tan(theta0 - g t / vt):')
    v0, T = 40.0, 2.0
    v_ex = quadratico_subida(T, v0, k)
    fq = lambda v: -G - k * abs(v) * v
    v_rk = rk4_1d(fq, v0, T, 200000)
    print('     v(%.0f s):  fechada %.10f   RK4 %.10f   dif %.1e'
          % (T, v_ex, v_rk, abs(v_ex - v_rk)))
    t_sub, h_max = quadratico_subida_marcos(v0, k)
    print('     tempo de subida = %.6f s,  altura maxima = %.6f m'
          % (t_sub, h_max))
    print('     (sem ar seriam %.6f s e %.6f m)'
          % (v0 / G, v0 ** 2 / (2 * G)))
    print()
    print('   QUEDA do repouso, v(t) = vt tanh(g t / vt):')
    T = 5.0
    v_ex, y_ex = quadratico_queda(T, k)
    v_rk = rk4_1d(fq, 0.0, T, 200000)
    print('     v(%.0f s):  fechada %.10f   RK4 %.10f   dif %.1e'
          % (T, v_ex, abs(v_rk), abs(v_ex - abs(v_rk))))
    print()
    print('   Repare na simetria quebrada: subindo, gravidade e arrasto')
    print('   somam-se, e a tangente leva a velocidade a zero em tempo')
    print('   FINITO; caindo, eles se opoem, e a tangente hiperbolica so')
    print('   alcanca vt no infinito.')
    print()

    print('=' * 68)
    print('4. ARRASTO QUADRATICO EM DUAS DIMENSOES: sem solucao fechada')
    print('=' * 68)
    print('   As equacoes sao')
    print('     dvx/dt = -k sqrt(vx^2+vy^2) vx')
    print('     dvy/dt = -g - k sqrt(vx^2+vy^2) vy')
    print('   e a raiz quadrada amarra as duas. Para ver que a separacao')
    print('   falha, basta comparar o movimento horizontal real com o que')
    print('   se obteria tratando cada componente por si:')
    print()
    kq = 0.004
    fsys = lambda u: np.array([u[2], u[3],
                               -kq * np.hypot(u[2], u[3]) * u[2],
                               -G - kq * np.hypot(u[2], u[3]) * u[3]])
    fsep = lambda u: np.array([u[2], u[3],
                               -kq * abs(u[2]) * u[2],
                               -G - kq * abs(u[3]) * u[3]])
    T = 3.0
    a = rk4_sistema(fsys, [0, 0, 35.0, 35.0], T, 200000)
    b = rk4_sistema(fsep, [0, 0, 35.0, 35.0], T, 200000)
    print('   t = %.0f s     acoplado      "separado"     diferenca' % T)
    print('   x (m)       %9.4f     %9.4f     %8.4f' % (a[0], b[0], abs(a[0] - b[0])))
    print('   y (m)       %9.4f     %9.4f     %8.4f' % (a[1], b[1], abs(a[1] - b[1])))
    print()
    print('   Metros de diferenca em tres segundos. Separar nao e uma')
    print('   aproximacao ruim: e outra fisica.')
    print()

    print('=' * 68)
    print('5. OS LIMITES FECHAM')
    print('=' * 68)
    print('   Com arrasto indo a zero, as formulas tem de devolver a')
    print('   cinematica de sempre (queda livre, v = v0 - g t):')
    print('   tau (s)      v(2 s) pela formula linear     v = v0 - g t')
    for tau_t in (10.0, 100.0, 1000.0, 1e5):
        v, _ = linear_1d(2.0, 20.0, tau_t)
        print('   %9.0f    %18.8f    %14.8f' % (tau_t, v, 20.0 - G * 2.0))
    print()
    print('   k (1/m)      altura maxima quadratica       v0^2/2g')
    for kk in (1e-2, 1e-4, 1e-6, 1e-9):
        _, h = quadratico_subida_marcos(40.0, kk)
        print('   %9.0e    %18.6f    %14.6f' % (kk, h, 40.0 ** 2 / (2 * G)))


if __name__ == '__main__':
    main()
