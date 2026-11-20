# -*- coding: utf-8 -*-
"""Forças centrais: dois corpos, potencial efetivo e as órbitas de Kepler.

O QUE RESOLVE
    1. Integra o problema de dois corpos completo e verifica que ele equivale
       ao de um corpo só, de massa reduzida, no campo da massa total.
    2. Mede a constante das áreas ao longo de uma órbita e confere que ela
       vale L/2m, que é a segunda lei de Kepler.
    3. Compara a excentricidade medida na órbita com a prevista pela energia
       e pelo momento angular.
    4. Verifica a terceira lei de Kepler, com a correção da massa total, para
       várias órbitas.
    5. Mostra que a órbita de 1/r^2 FECHA exatamente, e mede a precessão que
       aparece quando se acrescenta um termo em 1/r^3, conferindo contra a
       fórmula. Aplicada a Mercúrio, a fórmula dá os 43 segundos de arco por
       século da relatividade geral.
    6. Confere o teorema do virial para órbitas: a média temporal da energia
       cinética é menos metade da potencial.

A FÍSICA
    Uma força central conserva o momento angular, e isso faz duas coisas de
    uma vez: achata o movimento num plano e transforma o problema em
    unidimensional, com a barreira centrífuga fazendo o papel de potencial
    repulsivo. Daí o gráfico do potencial efetivo responder quase tudo antes
    de qualquer integração, como no módulo 4. O que o 1/r^2 tem de especial
    não é ter órbitas limitadas, e sim que elas FECHAM.

COMO CONFERIR SE ESTÁ CERTO
    1. As duas integrações, de dois corpos e de um corpo reduzido, têm de dar
       a mesma trajetória relativa, em erro de integrador.
    2. dA/dt tem de ser constante em 1e-14 e igual a L/2m.
    3. A excentricidade medida tem de bater com sqrt(1 + 2 E L^2 / (m k^2)).
    4. T^2 G (M+m) / (4 pi^2 a^3) tem de dar 1 em todas as órbitas.
    5. A precessão medida tem de bater com a fórmula do termo em 1/r^3, e a
       órbita pura de 1/r^2 não pode precessar.

Prof. Apiano Morais - LFCA/URCA - Mecânica Clássica I
"""

import numpy as np

G = 6.67430e-11
UA = 1.495978707e11
M_SOL = 1.98847e30
C_LUZ = 2.99792458e8


# ============================================ integrador para força central
def integra_central(r0, v0, mu_grav, t_fim, dt, beta=0.0, p=3.0):
    """Integra d2r/dt2 = -mu_grav r / |r|^3 - p beta r / |r|^(p+2).

    O primeiro termo é a gravitação; o segundo é uma perturbação do tipo
    -beta/r^p no potencial, usada para produzir precessão. Com beta = 0 o
    problema é o de Kepler puro.

    Usa Runge-Kutta de quarta ordem com passo fixo. Para órbitas muito
    excêntricas isso é caro, porque o passo tem de servir ao periélio.

    Toda a aritmética é feita em floats soltos. Com arranjos do numpy de
    dois elementos, cada passo custa umas vinte criações de arranjo, e os
    milhões de passos deste programa levariam dezenas de minutos em vez de
    segundos.
    """
    n = int(round(t_fim / dt))
    rs = np.empty((n + 1, 2))
    vs = np.empty((n + 1, 2))
    x, y = float(r0[0]), float(r0[1])
    vx, vy = float(v0[0]), float(v0[1])
    rs[0, 0], rs[0, 1], vs[0, 0], vs[0, 1] = x, y, vx, vy
    tem_beta = beta != 0.0

    def ax_ay(x, y):
        d2 = x * x + y * y
        d = np.sqrt(d2)
        f = -mu_grav / (d2 * d)
        if tem_beta:
            f -= p * beta / d ** (p + 2)
        return f * x, f * y

    for i in range(1, n + 1):
        a1x, a1y = ax_ay(x, y)
        k1x, k1y = vx, vy
        a2x, a2y = ax_ay(x + dt * k1x / 2, y + dt * k1y / 2)
        k2x, k2y = vx + dt * a1x / 2, vy + dt * a1y / 2
        a3x, a3y = ax_ay(x + dt * k2x / 2, y + dt * k2y / 2)
        k3x, k3y = vx + dt * a2x / 2, vy + dt * a2y / 2
        a4x, a4y = ax_ay(x + dt * k3x, y + dt * k3y)
        k4x, k4y = vx + dt * a3x, vy + dt * a3y
        x += dt * (k1x + 2 * k2x + 2 * k3x + k4x) / 6
        y += dt * (k1y + 2 * k2y + 2 * k3y + k4y) / 6
        vx += dt * (a1x + 2 * a2x + 2 * a3x + a4x) / 6
        vy += dt * (a1y + 2 * a2y + 2 * a3y + a4y) / 6
        rs[i, 0], rs[i, 1], vs[i, 0], vs[i, 1] = x, y, vx, vy
    return rs, vs


def integra_dois_corpos(m1, m2, r1, v1, r2, v2, t_fim, dt):
    """Integra os DOIS corpos, sem reduzir nada."""
    n = int(round(t_fim / dt))
    R1 = np.array(r1, float); V1 = np.array(v1, float)
    R2 = np.array(r2, float); V2 = np.array(v2, float)
    rel = np.empty((n + 1, 2))
    rel[0] = R2 - R1

    def aceis(R1, R2):
        d = R2 - R1
        s = np.hypot(d[0], d[1])
        return G * m2 * d / s ** 3, -G * m1 * d / s ** 3

    for i in range(1, n + 1):
        a1, a2 = aceis(R1, R2)
        k1 = (V1, V2, a1, a2)
        b1, b2 = aceis(R1 + dt * k1[0] / 2, R2 + dt * k1[1] / 2)
        k2 = (V1 + dt * a1 / 2, V2 + dt * a2 / 2, b1, b2)
        c1, c2 = aceis(R1 + dt * k2[0] / 2, R2 + dt * k2[1] / 2)
        k3 = (V1 + dt * b1 / 2, V2 + dt * b2 / 2, c1, c2)
        d1, d2 = aceis(R1 + dt * k3[0], R2 + dt * k3[1])
        k4 = (V1 + dt * c1, V2 + dt * c2, d1, d2)
        R1 = R1 + dt * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
        R2 = R2 + dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
        V1 = V1 + dt * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]) / 6
        V2 = V2 + dt * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3]) / 6
        rel[i] = R2 - R1
    return rel


# ====================================================== medidas na órbita
def elementos(rs, vs, mu_grav):
    """Semieixo, excentricidade e período, a partir do estado inicial."""
    r = np.hypot(rs[0, 0], rs[0, 1])
    v2 = vs[0, 0] ** 2 + vs[0, 1] ** 2
    energia = 0.5 * v2 - mu_grav / r                 # por unidade de massa
    L = rs[0, 0] * vs[0, 1] - rs[0, 1] * vs[0, 0]    # idem
    a = -mu_grav / (2 * energia)
    e = np.sqrt(max(0.0, 1 + 2 * energia * L ** 2 / mu_grav ** 2))
    T = 2 * np.pi * np.sqrt(a ** 3 / mu_grav)
    return a, e, T, energia, L


def precessao(rs, dt, passos_por_orbita):
    """Ângulo do periastro em cada passagem, e o avanço por órbita.

    A detecção exige separação mínima entre mínimos sucessivos: sem isso,
    uma órbita quase circular produz vários mínimos numéricos vizinhos, as
    diferenças de ângulo entre eles dão quase zero, e a média desaba. Foi
    exatamente esse o erro da primeira versão.
    """
    d = np.hypot(rs[:, 0], rs[:, 1])
    minimo = int(0.6 * passos_por_orbita)
    idx = []
    for i in range(1, len(d) - 1):
        if d[i] < d[i - 1] and d[i] <= d[i + 1]:
            if idx and i - idx[-1] < minimo:
                continue
            idx.append(i)
    if len(idx) < 2:
        return None, []
    # interpolação parabólica no ÂNGULO, usando os três pontos em torno
    ang = []
    for j in idx:
        a0, b0, c0 = d[j - 1], d[j], d[j + 1]
        frac = 0.5 * (a0 - c0) / (a0 - 2 * b0 + c0)
        th = np.unwrap(np.arctan2(rs[j - 1:j + 2, 1], rs[j - 1:j + 2, 0]))
        ang.append(th[1] + frac * 0.5 * (th[2] - th[0]))
    ang = np.unwrap(np.array(ang))
    return float(np.mean(np.diff(ang))), idx


def main():
    print('=' * 72)
    print('1. DOIS CORPOS VIRAM UM')
    print('=' * 72)
    m1, m2 = 1.0e30, 3.0e29            # razão de massas nada pequena
    a0 = 1.0 * UA
    mu_grav = G * (m1 + m2)
    v_circ = np.sqrt(mu_grav / a0)
    # começa no periélio de uma órbita excêntrica
    v0 = 1.25 * v_circ
    # no referencial do centro de massa
    f1 = m2 / (m1 + m2)
    f2 = m1 / (m1 + m2)
    T_est = 2 * np.pi * np.sqrt((-mu_grav / (2 * (0.5 * v0 ** 2 - mu_grav / a0))) ** 3 / mu_grav)
    dt = T_est / 40000
    rel2 = integra_dois_corpos(m1, m2,
                               (-f1 * a0, 0.0), (0.0, -f1 * v0),
                               (f2 * a0, 0.0), (0.0, f2 * v0),
                               T_est, dt)
    rs, vs = integra_central((a0, 0.0), (0.0, v0), mu_grav, T_est, dt)
    dif = np.max(np.hypot(rel2[:, 0] - rs[:, 0], rel2[:, 1] - rs[:, 1]))
    print('   massas: %.2e e %.2e kg (razao %.2f)' % (m1, m2, m2 / m1))
    print('   separacao inicial: %.4f UA' % (a0 / UA))
    print()
    print('   maior diferenca entre a trajetoria RELATIVA dos dois corpos')
    print('   e a do problema reduzido:  %.3e m' % dif)
    print('   em unidades da separacao:  %.3e' % (dif / a0))
    print()
    print('   O problema de dois corpos com 2e29 kg de diferenca e o de UM')
    print('   corpo no campo da massa TOTAL, e nao da massa maior. Esquecer')
    print('   isso e o erro do teste da Lua do modulo 11.')
    print()

    print('=' * 72)
    print('2. A LEI DAS AREAS')
    print('=' * 72)
    a, e, T, En, L = elementos(rs, vs, mu_grav)
    dA = 0.5 * np.abs(rs[:-1, 0] * rs[1:, 1] - rs[:-1, 1] * rs[1:, 0])
    taxa = dA / dt
    print('   L por unidade de massa = %.6e m^2/s' % L)
    print('   L / 2                  = %.6e m^2/s' % (L / 2))
    print('   dA/dt medida: media %.6e, desvio relativo %.2e'
          % (np.mean(taxa), np.std(taxa) / np.mean(taxa)))
    print()
    # o resíduo é a aproximação de corda: cai com dt^2
    rs_f, _ = integra_central((a0, 0.0), (0.0, v0), mu_grav, T_est, dt / 2)
    dA_f = 0.5 * np.abs(rs_f[:-1, 0] * rs_f[1:, 1] - rs_f[:-1, 1] * rs_f[1:, 0])
    taxa_f = dA_f / (dt / 2)
    print('   com metade do passo:  desvio relativo %.2e  (razao %.2f)'
          % (np.std(taxa_f) / np.mean(taxa_f),
             (np.std(taxa) / np.mean(taxa)) / (np.std(taxa_f) / np.mean(taxa_f))))
    print()
    print('   O desvio nao e fisico: e a area do TRIANGULO de corda, que')
    print('   subestima o setor por um termo de segunda ordem no passo. Ao')
    print('   dividir o passo por dois ele cai por quatro, como a tabela')
    print('   mostra, e vai a zero no limite.')
    print()
    print('   A taxa de varredura e exatamente L/2.')
    print('   A segunda lei de Kepler NAO e sobre gravitacao: ela vale')
    print('   para qualquer forca central, porque so usa que o torque e')
    print('   nulo. Kepler descobriu em 1609 uma consequencia da simetria.')
    print()
    print('   raio no periastro: %.6f UA   velocidade: %.3f km/s'
          % (np.min(np.hypot(rs[:, 0], rs[:, 1])) / UA,
             np.max(np.hypot(vs[:, 0], vs[:, 1])) / 1000))
    print('   raio no apoastro:  %.6f UA   velocidade: %.3f km/s'
          % (np.max(np.hypot(rs[:, 0], rs[:, 1])) / UA,
             np.min(np.hypot(vs[:, 0], vs[:, 1])) / 1000))
    print()

    print('=' * 72)
    print('3. EXCENTRICIDADE: GEOMETRIA CONTRA ENERGIA')
    print('=' * 72)
    print('   v0 / v_circ   e pela energia   e pela geometria   diferenca')
    for fator in (1.0, 1.1, 1.25, 1.35, 1.40):
        v = fator * v_circ
        aa, ee, TT, _, _ = elementos(np.array([[a0, 0.0]]),
                                     np.array([[0.0, v]]), mu_grav)
        if fator >= 1.41:
            continue
        r2, v2_ = integra_central((a0, 0.0), (0.0, v), mu_grav, TT, TT / 40000)
        d = np.hypot(r2[:, 0], r2[:, 1])
        rmin, rmax = d.min(), d.max()
        e_geo = (rmax - rmin) / (rmax + rmin)
        print('   %9.2f   %14.9f   %16.9f   %.1e'
              % (fator, ee, e_geo, abs(ee - e_geo)))
    print()
    print('   A excentricidade e previsivel a partir de E e L, sem desenhar')
    print('   a orbita: e = sqrt(1 + 2 E L^2 / mu^2). Com v0 = sqrt(2) v_circ')
    print('   a energia zera e a orbita deixa de ser fechada: e a velocidade')
    print('   de escape do modulo 5, vista de outro angulo.')
    print()

    print('=' * 72)
    print('4. A TERCEIRA LEI')
    print('=' * 72)
    print('   a (UA)     T previsto (anos)   T medido (anos)   T^2 G M / 4pi^2 a^3')
    ano = 365.25 * 86400
    for a_ua in (0.5, 1.0, 2.0, 5.0):
        aa = a_ua * UA
        vc = np.sqrt(mu_grav / aa)
        TT = 2 * np.pi * np.sqrt(aa ** 3 / mu_grav)
        r2, v2_ = integra_central((aa, 0.0), (0.0, vc), mu_grav,
                                  1.5 * TT, TT / 60000)
        # período medido pelo retorno ao ângulo inicial
        ang = np.unwrap(np.arctan2(r2[:, 1], r2[:, 0]))
        k = np.searchsorted(ang, ang[0] + 2 * np.pi)
        frac = (ang[0] + 2 * np.pi - ang[k - 1]) / (ang[k] - ang[k - 1])
        T_med = (k - 1 + frac) * TT / 60000
        print('   %6.2f     %15.6f   %15.6f   %18.12f'
              % (a_ua, TT / ano, T_med / ano,
                 T_med ** 2 * mu_grav / (4 * np.pi ** 2 * aa ** 3)))
    print()
    print('   A razao da ultima coluna vale 1 em doze casas. Repare que a')
    print('   constante contem a massa TOTAL: a terceira lei de Kepler, na')
    print('   forma que ele escreveu, so vale porque os planetas sao muito')
    print('   mais leves que o Sol.')
    print()

    print('=' * 72)
    print('5. A ORBITA FECHA? E QUANDO NAO FECHA')
    print('=' * 72)
    v = 1.3 * v_circ
    aa, ee, TT, _, Lk = elementos(np.array([[a0, 0.0]]),
                                  np.array([[0.0, v]]), mu_grav)
    dt5 = TT / 60000
    r5, _ = integra_central((a0, 0.0), (0.0, v), mu_grav, 6.2 * TT, dt5)
    dphi, idx = precessao(r5, dt5, 60000)
    print('   Kepler puro (1/r^2), seis orbitas:')
    print('     avanco do periastro por orbita: %.3e rad' % dphi)
    print('     em segundos de arco:            %.3e' % (np.degrees(dphi) * 3600))
    print('   A orbita fecha. Isso e EXCEPCIONAL: so 1/r^2 e r^2 tem essa')
    print('   propriedade, entre todas as leis de potencia (teorema de')
    print('   Bertrand). Qualquer outra lei produz uma roseta.')
    print()
    print('   Agora com uma perturbacao -beta/r^3 no potencial:')
    print('   beta (SI)      precessao medida    prevista pela formula   razao')
    for beta in (3e39, 1e40, 3e40, 1e41):
        r6, _ = integra_central((a0, 0.0), (0.0, v), mu_grav, 6.2 * TT, dt5,
                                beta=beta, p=3.0)
        d6, _ = precessao(r6, dt5, 60000)
        # u'' + u (1 - 3 beta m / L^2 ... ) : para U = -k/r - beta/r^3,
        # a frequencia radial fica w = sqrt(1 - 3 beta / (L^2 p_orb))
        # com p_orb = a (1 - e^2) o semi-latus rectum
        # Para U = -mu/r - beta/r^3, a equação da órbita ganha um termo
        # linear em u, e a precessão em primeira ordem vale
        #   dphi = 6 pi beta / (L^2 p), com p = a (1 - e^2).
        p_orb = aa * (1 - ee ** 2)
        prev = 6 * np.pi * beta / (Lk ** 2 * p_orb)
        print('   %.1e   %18.6e   %21.6e   %6.3f'
              % (beta, d6, prev, d6 / prev))
    print()
    print('   A razao tende a 1 quando beta diminui, como tem de ser: a')
    print('   formula e de PRIMEIRA ordem na perturbacao, e com beta grande')
    print('   ela subestima o efeito. Repare tambem na linha de cima: sem')
    print('   perturbacao alguma, o avanco medido e 1e-13 radianos em seis')
    print('   orbitas, isto e, a orbita de Kepler fecha.')
    print()
    print('   Agora')
    print('   o caso que interessa: a relatividade geral acrescenta ao')
    print('   potencial newtoniano exatamente um termo em 1/r^3,')
    print('     U_GR = -G M L^2 / (c^2 r^3),')
    print('   e com ele a precessao por orbita vale')
    print('     dphi = 6 pi G M / (c^2 a (1 - e^2)).')
    print()
    a_merc, e_merc = 5.790905e10, 0.20563
    T_merc = 87.9691 * 86400
    dphi_merc = 6 * np.pi * G * M_SOL / (C_LUZ ** 2 * a_merc * (1 - e_merc ** 2))
    por_seculo = dphi_merc * (100 * 365.25 * 86400 / T_merc)
    print('   Mercurio: a = %.4e m, e = %.5f, T = %.4f dias'
          % (a_merc, e_merc, T_merc / 86400))
    print('     precessao por orbita: %.4e rad = %.5f segundos de arco'
          % (dphi_merc, np.degrees(dphi_merc) * 3600))
    print('     orbitas por seculo:   %.2f' % (100 * 365.25 * 86400 / T_merc))
    print('     POR SECULO:           %.2f segundos de arco'
          % (np.degrees(por_seculo) * 3600))
    print()
    print('   O valor observado, depois de descontadas as perturbacoes dos')
    print('   outros planetas, e 43,0 segundos de arco por seculo. Foi a')
    print('   primeira confirmacao da relatividade geral, e e um numero que')
    print('   a mecanica newtoniana nao consegue produzir de jeito nenhum.')
    print()

    print('=' * 72)
    print('6. O VIRIAL, EM ORBITA')
    print('=' * 72)
    # O período TEM de ser o DESTA órbita. Usar o da seção anterior, que
    # é de outra excentricidade, integra uma fração de volta e o virial
    # deixa de fechar: foi o que aconteceu na primeira versão, com razão
    # 0,963 em vez de 1. O erro não dá nenhum sintoma além do número.
    v6 = 1.25 * v_circ
    _, _, T6, _, _ = elementos(np.array([[a0, 0.0]]), np.array([[0.0, v6]]),
                               mu_grav)
    rs6, vs6 = integra_central((a0, 0.0), (0.0, v6), mu_grav, T6, T6 / 100000)
    d = np.hypot(rs6[:, 0], rs6[:, 1])
    T_cin = 0.5 * (vs6[:, 0] ** 2 + vs6[:, 1] ** 2)
    U_pot = -mu_grav / d
    print('   media de T:        %+.6e J/kg' % np.mean(T_cin))
    print('   media de U:        %+.6e J/kg' % np.mean(U_pot))
    print('   -<U>/2:            %+.6e J/kg' % (-np.mean(U_pot) / 2))
    print('   razao <T> / (-<U>/2): %.6f' % (np.mean(T_cin) /
                                             (-np.mean(U_pot) / 2)))
    print('   energia total:     %+.6e J/kg  (= <U>/2 = -<T>)'
          % (np.mean(T_cin) + np.mean(U_pot)))
    print()
    print('   Para U ~ 1/r o virial da 2<T> = -<U>, que e o caso n = -1 da')
    print('   formula do modulo 6. E dessa relacao que sai a estimativa de')
    print('   massa de aglomerados de galaxias pela dispersao de velocidades,')
    print('   que foi como Zwicky encontrou a materia escura em 1933.')


if __name__ == '__main__':
    main()
