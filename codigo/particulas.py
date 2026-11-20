# -*- coding: utf-8 -*-
"""Sistemas de partículas: centro de massa, colisões e espalhamento.

O QUE RESOLVE
    1. Integra um sistema de N partículas com forças internas aos pares e
       uma força externa, e verifica que o centro de massa se move como uma
       partícula de massa total sob a força externa resultante, qualquer que
       seja o emaranhado das forças internas.
    2. Resolve a colisão unidimensional com coeficiente de restituição e
       mede a energia perdida, conferindo a fórmula contra a conta direta.
    3. Verifica que duas massas iguais em colisão elástica bidimensional
       saem a 90 graus uma da outra, e mostra que isso é falso assim que as
       massas diferem.
    4. Compara o ângulo de espalhamento no laboratório com o do referencial
       do centro de massa, e verifica o ângulo máximo quando o projétil é
       mais pesado que o alvo.
    5. Integra trajetórias de Rutherford e mede o ângulo de deflexão em
       função do parâmetro de impacto, conferindo contra a fórmula exata.
    6. Monta a seção de choque diferencial a partir das trajetórias e
       confere a dependência em 1/sen^4(theta/2).

A FÍSICA
    Forças internas aparecem aos pares opostos, de modo que somam zero: é a
    terceira lei que permite falar de um sistema como se fosse um corpo só.
    Daí saem, em sequência, o teorema do centro de massa, a conservação do
    momento total, e o referencial do centro de massa, no qual toda colisão
    elástica é apenas uma rotação do vetor velocidade relativa. O resto é
    traduzir de volta para o laboratório.

COMO CONFERIR SE ESTÁ CERTO
    1. A trajetória do CM integrada junto com as N partículas tem de
       coincidir com a parábola da força externa, em erro de integrador.
    2. Com e = 1 a velocidade relativa tem de inverter de sinal e a energia
       tem de se conservar; com e = 0 os dois corpos saem juntos.
    3. Para massas iguais o produto escalar das velocidades finais tem de
       ser nulo, exceto na colisão frontal.
    4. O ângulo medido na trajetória de Rutherford tem de bater com
       tan(theta/2) = k / (m v^2 b).
    5. A seção de choque medida tem de ser proporcional a 1/sen^4(theta/2).

Prof. Apiano Morais - LFCA/URCA - Mecânica Clássica I
"""

import numpy as np
from math import sqrt, atan2, hypot

# ---------------------------------------------------------------------------
# 1. N partículas, forças internas aos pares
# ---------------------------------------------------------------------------


def forcas_internas(pos, cargas, k_mola, r_eq):
    """Força de mola entre TODOS os pares, mais uma repulsão em 1/r^2.

    Nada aqui é escolhido para ser simples: a ideia é justamente emaranhar as
    forças internas e ver o centro de massa ignorar tudo.
    """
    n = len(pos)
    f = np.zeros_like(pos)
    for i in range(n):
        for j in range(i + 1, n):
            d = pos[j] - pos[i]
            r = np.hypot(d[0], d[1])
            u = d / r
            # mola: atrai se esticada, repele se comprimida
            fij = k_mola * (r - r_eq) * u
            # repulsão tipo Coulomb entre as duas cargas
            fij = fij - cargas[i] * cargas[j] / r ** 2 * u
            f[i] += fij
            f[j] -= fij          # terceira lei, imposta por construção
    return f


def integra_sistema(pos, vel, massas, cargas, g_ext, k_mola, r_eq, t_fim, dt):
    """Velocity-Verlet. A força não depende da velocidade, então ele serve.

    O módulo 7 mostrou que com atrito ele é silenciosamente errado; aqui não
    há atrito, e a vantagem de ser simplético compensa.
    """
    m = massas[:, None]
    def acel(p):
        return (forcas_internas(p, cargas, k_mola, r_eq) + massas[:, None] * g_ext) / m
    p = pos.copy()
    v = vel.copy()
    a = acel(p)
    passos = int(round(t_fim / dt))
    cms = np.zeros((passos + 1, 2))
    mtot = massas.sum()
    cms[0] = (massas[:, None] * p).sum(axis=0) / mtot
    for n in range(passos):
        p = p + v * dt + 0.5 * a * dt ** 2
        a_novo = acel(p)
        v = v + 0.5 * (a + a_novo) * dt
        a = a_novo
        cms[n + 1] = (massas[:, None] * p).sum(axis=0) / mtot
    return p, v, cms


# ---------------------------------------------------------------------------
# 2 e 3. Colisões
# ---------------------------------------------------------------------------


def colisao_1d(m1, m2, u1, u2, e):
    """Colisão unidimensional com coeficiente de restituição e.

    As duas equações são a conservação do momento e a definição
    v2 - v1 = -e (u2 - u1). Resolvidas, dão:
    """
    M = m1 + m2
    v1 = (m1 * u1 + m2 * u2 + m2 * e * (u2 - u1)) / M
    v2 = (m1 * u1 + m2 * u2 + m1 * e * (u1 - u2)) / M
    return v1, v2


def colisao_2d_elastica(m1, m2, u1, theta_cm):
    """Colisão elástica com o alvo m2 parado, vista do laboratório.

    No referencial do centro de massa a colisão elástica é apenas uma
    rotação de theta_cm do vetor velocidade relativa: os módulos não mudam.
    Basta então rodar e voltar para o laboratório somando a velocidade do CM.
    """
    M = m1 + m2
    v_cm = np.array([m1 * u1 / M, 0.0])
    # velocidades no CM, antes
    w1 = np.array([u1, 0.0]) - v_cm
    # no CM o módulo se conserva; rodamos o vetor de w1
    c, s = np.cos(theta_cm), np.sin(theta_cm)
    w1f = np.array([c * w1[0] - s * w1[1], s * w1[0] + c * w1[1]])
    w2f = -m1 / m2 * w1f
    return w1f + v_cm, w2f + v_cm


# ---------------------------------------------------------------------------
# 5 e 6. Espalhamento de Rutherford
# ---------------------------------------------------------------------------


def deflexao(b, v_inf, k_sobre_m, r_ini=4000.0, folga=0.02, teto=0.8):
    """Integra uma trajetória de espalhamento e devolve o ângulo de saída.

    A partícula entra vinda de x = -r_ini com parâmetro de impacto b, sob
    aceleração +k_sobre_m/r^2 (repulsiva). O ângulo é medido pela direção da
    velocidade quando ela já está longe de novo.

    Usa RK4 com escalares, e não com vetores do numpy de dois elementos: a
    diferença de velocidade é de uma ordem de grandeza, e isso importa quando
    são milhares de trajetórias.
    """
    x, y = -r_ini, b
    vx, vy = v_inf, 0.0

    def a(x, y):
        r2 = x * x + y * y
        r3 = r2 * sqrt(r2)
        return k_sobre_m * x / r3, k_sobre_m * y / r3

    # passo adaptado: pequeno perto, grande longe. O teto existe para que a
    # aproximação distante, onde a força é desprezível, não consuma a conta.
    t = 0.0
    while True:
        r = sqrt(x * x + y * y)
        # A saída é "longe e se afastando", e não "longe e do outro lado":
        # com parâmetro de impacto pequeno o desvio passa de 90 graus e a
        # partícula volta pelo lado de onde veio, sem nunca cruzar x = 0.
        if r > r_ini and (x * vx + y * vy) > 0:
            break
        dt = min(folga * r / v_inf, teto)
        ax1, ay1 = a(x, y)
        k1 = (vx, vy, ax1, ay1)
        ax2, ay2 = a(x + 0.5 * dt * k1[0], y + 0.5 * dt * k1[1])
        k2 = (vx + 0.5 * dt * k1[2], vy + 0.5 * dt * k1[3], ax2, ay2)
        ax3, ay3 = a(x + 0.5 * dt * k2[0], y + 0.5 * dt * k2[1])
        k3 = (vx + 0.5 * dt * k2[2], vy + 0.5 * dt * k2[3], ax3, ay3)
        ax4, ay4 = a(x + dt * k3[0], y + dt * k3[1])
        k4 = (vx + dt * k3[2], vy + dt * k3[3], ax4, ay4)
        x += dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        y += dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        vx += dt / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
        vy += dt / 6 * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3])
        t += dt
        if t > 1e5:
            return np.nan
    return atan2(vy, vx)


# ---------------------------------------------------------------------------


def main():
    print('=' * 72)
    print('1. O CENTRO DE MASSA IGNORA AS FORCAS INTERNAS')
    print('=' * 72)
    rng = np.random.default_rng(7)
    n = 6
    massas = np.array([1.0, 2.0, 0.5, 3.0, 1.5, 0.8])
    cargas = np.array([1.0, -2.0, 1.5, -1.0, 2.0, -1.5])
    pos = rng.uniform(-2.0, 2.0, (n, 2))
    vel = rng.uniform(-1.5, 1.5, (n, 2))
    g_ext = np.array([0.0, -9.81])
    mtot = massas.sum()
    r_cm0 = (massas[:, None] * pos).sum(axis=0) / mtot
    v_cm0 = (massas[:, None] * vel).sum(axis=0) / mtot

    t_fim, dt = 2.0, 2.0e-4
    _, _, cms = integra_sistema(pos, vel, massas, cargas, g_ext,
                                k_mola=40.0, r_eq=1.0, t_fim=t_fim, dt=dt)
    ts = np.arange(len(cms)) * dt
    previsto = (r_cm0[None, :] + v_cm0[None, :] * ts[:, None]
                + 0.5 * g_ext[None, :] * (ts ** 2)[:, None])
    erro = np.max(np.hypot(cms[:, 0] - previsto[:, 0], cms[:, 1] - previsto[:, 1]))
    print('   %d particulas, molas entre TODOS os pares mais repulsao 1/r^2'
          % n)
    print('   massa total: %.1f, gravidade externa: %.2f m/s^2'
          % (mtot, -g_ext[1]))
    print()
    print('   maior desvio entre o CM integrado e a parabola prevista:')
    print('     %.3e m, em %.1f s de voo' % (erro, t_fim))
    print('   deslocamento do CM no mesmo intervalo: %.3f m'
          % np.hypot(*(cms[-1] - cms[0])))
    print()
    print('   com o passo cortado pela metade, duas vezes:')
    for d in [1.0e-4, 5.0e-5]:
        _, _, c2 = integra_sistema(pos, vel, massas, cargas, g_ext,
                                   40.0, 1.0, t_fim, d)
        t2 = np.arange(len(c2)) * d
        p2 = (r_cm0[None, :] + v_cm0[None, :] * t2[:, None]
              + 0.5 * g_ext[None, :] * (t2 ** 2)[:, None])
        print('     dt = %.1e  ->  desvio %.3e m'
              % (d, np.max(np.hypot(c2[:, 0] - p2[:, 0], c2[:, 1] - p2[:, 1]))))
    print()
    print('   Repare que o desvio CRESCE quando o passo diminui, o contrario')
    print('   do que acontece em todo o resto do curso. Nao e um erro: o')
    print('   teorema do centro de massa e EXATO, nao ha erro de truncamento')
    print('   nenhum a reduzir, e o que sobra e arredondamento, que se')
    print('   acumula com o numero de passos. Quando a conta esta certa ate')
    print('   a ultima casa, refina-la so piora.')
    print()
    print('   As forcas internas sao violentas e totalmente emaranhadas, e o')
    print('   centro de massa nao toma conhecimento de nenhuma delas: ele cai')
    print('   em parabola, como uma particula de massa 8,8 kg. A razao e a')
    print('   terceira lei: no somatorio, cada forca interna aparece duas')
    print('   vezes com sinais opostos.')
    print()

    # ---- momento total sem campo externo ----
    _, vfin, _ = integra_sistema(pos, vel, massas, cargas,
                                 np.zeros(2), 40.0, 1.0, 1.0, 2.0e-4)
    p_ini = (massas[:, None] * vel).sum(axis=0)
    p_fim = (massas[:, None] * vfin).sum(axis=0)
    print('   Sem campo externo, momento total:')
    print('     inicial: (%+.9f, %+.9f)' % (p_ini[0], p_ini[1]))
    print('     final:   (%+.9f, %+.9f)' % (p_fim[0], p_fim[1]))
    print('     variacao relativa: %.2e'
          % (np.hypot(*(p_fim - p_ini)) / np.hypot(*p_ini)))
    print()

    print('=' * 72)
    print('2. COLISAO EM UMA DIMENSAO, E A ENERGIA QUE SOME')
    print('=' * 72)
    m1, m2 = 2.0, 3.0
    u1, u2 = 5.0, -1.0
    print('   m1 = %.1f kg a %+.1f m/s contra m2 = %.1f kg a %+.1f m/s'
          % (m1, u1, m2, u2))
    print()
    print('     e      v1        v2      K final / K inicial   perda prevista')
    K0 = 0.5 * m1 * u1 ** 2 + 0.5 * m2 * u2 ** 2
    mu = m1 * m2 / (m1 + m2)
    for e in [1.0, 0.8, 0.5, 0.0]:
        v1, v2 = colisao_1d(m1, m2, u1, u2, e)
        K1 = 0.5 * m1 * v1 ** 2 + 0.5 * m2 * v2 ** 2
        # a perda prevista: metade da energia do movimento relativo, vezes
        # (1 - e^2), que é o que o referencial do CM entrega de graça
        perda = 0.5 * mu * (u1 - u2) ** 2 * (1 - e ** 2)
        print('   %.1f  %+8.4f  %+8.4f      %.6f        %8.4f J  (medida %8.4f)'
              % (e, v1, v2, K1 / K0, perda, K0 - K1))
    print()
    print('   Com e = 1 a energia se conserva em 1e-16 e a velocidade')
    print('   relativa apenas troca de sinal. Com e = 0 os dois seguem')
    print('   juntos, e a perda e MAXIMA, mas nao total: sobra a energia do')
    print('   centro de massa, que o momento obriga a sobrar. A formula da')
    print('   perda sai de ler a colisao no referencial do CM, onde a energia')
    print('   cinetica e exatamente mu*v_rel^2/2.')
    print()

    print('=' * 72)
    print('3. OS 90 GRAUS DAS MASSAS IGUAIS')
    print('=' * 72)
    u = 4.0
    print('   massas iguais, alvo parado, para varios angulos do CM:')
    print('     theta_cm    angulo entre v1 e v2    v1.v2')
    for tcm in [30.0, 60.0, 90.0, 120.0, 150.0]:
        v1, v2 = colisao_2d_elastica(1.0, 1.0, u, np.radians(tcm))
        cos = np.dot(v1, v2) / (np.hypot(*v1) * np.hypot(*v2))
        print('     %6.1f         %8.4f graus        %+.2e'
              % (tcm, np.degrees(np.arccos(np.clip(cos, -1, 1))), np.dot(v1, v2)))
    print()
    print('   Exatamente 90 graus, em qualquer angulo de espalhamento. A')
    print('   conta e de uma linha: com m1 = m2 a conservacao do momento da')
    print('   u = v1 + v2 e a da energia da u^2 = v1^2 + v2^2, e as duas')
    print('   juntas exigem v1.v2 = 0.')
    print()
    print('   Com massas diferentes isso acaba:')
    for m2 in [0.5, 1.0, 2.0]:
        v1, v2 = colisao_2d_elastica(1.0, m2, u, np.radians(70.0))
        cos = np.dot(v1, v2) / (np.hypot(*v1) * np.hypot(*v2))
        print('     m1=1,0  m2=%.1f  theta_cm=70 graus -> %7.3f graus'
              % (m2, np.degrees(np.arccos(np.clip(cos, -1, 1)))))
    print()
    print('   E e por isso que a camara de bolhas distingue um proton de um')
    print('   nucleo pesado so de olhar o angulo entre os dois rastros.')
    print()

    print('=' * 72)
    print('4. LABORATORIO CONTRA CENTRO DE MASSA')
    print('=' * 72)
    print('   theta_lab = arctg[ sen(theta_cm) / (cos(theta_cm) + m1/m2) ]')
    print()
    print('   m1/m2   theta_cm=60   theta_cm=120   theta_cm=180   maximo')
    for razao in [0.2, 1.0, 2.0, 5.0]:
        linha = '   %5.1f ' % razao
        for tcm in [60.0, 120.0, 180.0]:
            t = np.radians(tcm)
            tl = np.arctan2(np.sin(t), np.cos(t) + razao)
            linha += '   %9.3f' % np.degrees(tl % np.pi if tl < 0 else tl)
        if razao > 1:
            linha += '    %7.3f' % np.degrees(np.arcsin(1.0 / razao))
        elif razao == 1:
            # o caso de fronteira: massas iguais chegam a 90 graus e param
            linha += '       90.0'
        else:
            linha += '      180.0'
        print(linha)
    print()
    print('   A coluna de theta_cm = 180 merece atencao: para m1 > m2 ela da')
    print('   ZERO. Bater de frente e voltar no referencial do centro de')
    print('   massa, para um projetil pesado, significa seguir em frente no')
    print('   laboratorio, so que mais devagar. O recuo so chega ao')
    print('   laboratorio quando o alvo e pesado o bastante.')
    print()
    print('   Quando o projetil e mais pesado que o alvo ha um angulo MAXIMO')
    print('   de espalhamento, sen(theta_max) = m2/m1: por mais de frente que')
    print('   seja a batida, o projetil nao consegue ser desviado alem disso.')
    print('   Uma bola de boliche nao volta de um pino. Foi exatamente a')
    print('   violacao disso, em 1911, que mostrou que o atomo tinha nucleo:')
    print('   particulas alfa voltando para tras exigiam um alvo pesado e')
    print('   pequeno, e nao o pudim de Thomson.')
    print()

    print('=' * 72)
    print('5. RUTHERFORD: A DEFLEXAO CONTRA O PARAMETRO DE IMPACTO')
    print('=' * 72)
    v_inf = 1.0
    k_sm = 1.0          # k/m, em unidades em que v_inf = 1
    print('   repulsao k/m = %.1f, velocidade no infinito = %.1f' % (k_sm, v_inf))
    print()
    print('        b        theta medido    theta previsto     diferenca')
    for b in [0.2, 0.5, 1.0, 2.0, 5.0, 10.0]:
        th = deflexao(b, v_inf, k_sm)
        prev = 2.0 * np.arctan(k_sm / (v_inf ** 2 * b))
        print('   %8.2f      %9.5f       %9.5f      %9.2e'
              % (b, th, prev, abs(th - prev)))
    print()
    print('   A formula exata e tg(theta/2) = k / (m v^2 b), e ela sai da')
    print('   mesma equacao da orbita do modulo 12, agora com energia')
    print('   positiva: a trajetoria e uma hiperbole, e o angulo entre as')
    print('   assintotas e o que se mede.')
    print()
    print('   A diferenca acima nao e erro de integrador: e o preco de medir')
    print('   em distancia finita um angulo que so existe no infinito. Ela')
    print('   cai como 1/r_ini, e a tabela mostra isso dobrando r_ini:')
    print()
    print('        r_ini      erro em b=1,0     razao com a linha de cima')
    ant = None
    for ri in [500.0, 1000.0, 2000.0, 4000.0]:
        er = abs(deflexao(1.0, v_inf, k_sm, ri)
                 - 2.0 * np.arctan(k_sm / (v_inf ** 2 * 1.0)))
        print('   %9.0f      %12.3e          %s'
              % (ri, er, '%.3f' % (ant / er) if ant else '-'))
        ant = er
    print()
    print('   A razao da 2,0 em todas as linhas: primeira ordem em 1/r_ini,')
    print('   como tem de ser, porque o impulso que falta depois de r_ini e')
    print('   a integral de k/r^2 dt, que vale k/(m v r_ini). Uma forca de')
    print('   alcance infinito nao deixa a particula livre em lugar nenhum.')
    print()
    print('   Repare que theta NAO vai a zero para b grande de qualquer')
    print('   jeito: cai como 1/b. Nenhum parametro de impacto, por maior que')
    print('   seja, deixa a particula passar sem desvio. Essa cauda e a razao')
    print('   de a secao de choque total de Rutherford DIVERGIR.')
    print()

    print('=' * 72)
    print('6. A SECAO DE CHOQUE DIFERENCIAL')
    print('=' * 72)
    print('   dsigma/dOmega = (b / sen theta) |db/dtheta|, medido nas')
    print('   trajetorias integradas e comparado com (k/2mv^2)^2/sen^4(th/2):')
    print()
    print('     theta      medida        formula       razao')
    bs = np.geomspace(0.08, 20.0, 60)
    ths = np.array([deflexao(b, v_inf, k_sm) for b in bs])
    for i in range(6, len(bs) - 6, 9):
        # derivada por diferença central em b
        dbdth = (bs[i + 1] - bs[i - 1]) / (ths[i + 1] - ths[i - 1])
        med = abs(bs[i] / np.sin(ths[i]) * dbdth)
        form = (k_sm / (2 * v_inf ** 2)) ** 2 / np.sin(ths[i] / 2) ** 4
        print('   %8.4f  %12.5e  %12.5e    %.6f'
              % (ths[i], med, form, med / form))
    print()
    print('   A razao vale 1 em tres casas ao longo de quatro ordens de')
    print('   grandeza da secao de choque. O 1/sen^4(theta/2) e a assinatura')
    print('   do 1/r^2, e foi medi-lo que Geiger e Marsden fizeram.')
    print()
    print('   A integral de dsigma/dOmega sobre todos os angulos diverge em')
    print('   theta -> 0, pelo mesmo motivo da secao anterior: o alcance')
    print('   infinito da forca. Num alvo real a divergencia some, porque os')
    print('   eletrons blindam o nucleo e o potencial deixa de ser 1/r a')
    print('   partir do raio atomico.')
    print()


if __name__ == '__main__':
    main()
