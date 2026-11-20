# -*- coding: utf-8 -*-
"""Gravitação: o teorema das cascas, o teste da Lua e as marés.

O QUE RESOLVE
    1. Verifica o teorema das cascas por integração direta sobre a esfera:
       campo nulo dentro, e campo de massa pontual fora.
    2. Calcula o campo e o potencial dentro e fora de uma esfera maciça, e
       confere contra as formas fechadas.
    3. Refaz o teste que convenceu Newton: comparar a aceleração da Lua com
       a aceleração de uma maçã, usando o inverso do quadrado.
    4. Calcula a força de maré como diferença de campo, mostra por que há
       DUAS marés por dia e obtém a altura da maré de equilíbrio.
    5. Compara a maré lunar com a solar e calcula o limite de Roche.

A FÍSICA
    A lei do inverso do quadrado é simples; as suas consequências não são. O
    teorema das cascas é o que permite tratar planetas como pontos, e Newton
    atrasou a publicação dos Principia por anos até conseguir prová-lo. As
    marés vêm da DIFERENÇA do campo entre um lado e o outro do corpo, e por
    isso caem com o CUBO da distância, e não com o quadrado: é a primeira vez
    no curso em que o que importa é a derivada do campo, e não ele.

COMO CONFERIR SE ESTÁ CERTO
    1. O campo dentro da casca tem de ser nulo em erro de quadratura, em
       vários pontos, inclusive bem perto da superfície.
    2. O campo fora da casca tem de ser GM/r^2 com a massa inteira no centro.
    3. A aceleração da Lua prevista pelo inverso do quadrado tem de bater com
       a medida pela órbita, uma vez corrigida a massa reduzida.
    4. A altura da maré de equilíbrio tem de dar os 36 cm conhecidos, e a
       razão entre a maré lunar e a solar tem de dar 2,2.

Prof. Apiano Morais - LFCA/URCA - Mecânica Clássica I
"""

import numpy as np

G = 6.67430e-11
G_PADRAO = 9.80665

M_TERRA = 5.9722e24
R_TERRA = 6.371e6
M_LUA = 7.342e22
R_LUA = 1.7374e6
D_LUA = 3.84399e8
T_LUA = 27.321661 * 86400.0        # mês sideral, em segundos
M_SOL = 1.98847e30
D_SOL = 1.495979e11


# ================================================== 1. o teorema das cascas
def campo_da_casca(r, R=1.0, M=1.0, n=20000):
    """Campo de uma casca esférica fina, por integração direta.

    Um anel de meio-ângulo theta contribui com dM = (M/2) sen(theta) dtheta,
    e por simetria só a componente ao longo do eixo sobrevive. A distância
    do ponto ao anel é s = sqrt(r^2 + R^2 - 2 r R cos theta), e o cosseno
    do ângulo entre a direção do anel e o eixo vale (r - R cos theta)/s.

    Este é o cálculo que Newton fez geometricamente, e que o atrasou por
    anos: ele não tinha o cálculo integral publicado para usar.
    """
    th = (np.arange(n) + 0.5) * np.pi / n          # ponto médio
    dM = 0.5 * M * np.sin(th) * (np.pi / n)
    s2 = r * r + R * R - 2 * r * R * np.cos(th)
    s = np.sqrt(s2)
    componente = (r - R * np.cos(th)) / s
    return -G * np.sum(dM * componente / s2)       # negativo = para dentro


def campo_esfera_macica(r, R=1.0, M=1.0, n=2000):
    """Campo de uma esfera maciça, somando cascas."""
    bordas = np.linspace(0.0, R, n + 1)
    meios = 0.5 * (bordas[1:] + bordas[:-1])
    dV = (4.0 / 3.0) * np.pi * (bordas[1:] ** 3 - bordas[:-1] ** 3)
    dM = M * dV / ((4.0 / 3.0) * np.pi * R ** 3)
    total = 0.0
    for Rc, m in zip(meios, dM):
        if r > Rc:
            total += -G * m / r ** 2               # casca interna: ponto
        # casca externa: contribuição nula, pelo teorema
    return total


def campo_esfera_formula(r, R=1.0, M=1.0):
    if r >= R:
        return -G * M / r ** 2
    return -G * M * r / R ** 3


def potencial_esfera_formula(r, R=1.0, M=1.0):
    if r >= R:
        return -G * M / r
    return -G * M * (3 * R * R - r * r) / (2 * R ** 3)


# ======================================================== 4. e 5. as marés
def mare_diferencial(m, d, R):
    """Aceleração de maré na superfície, ao longo da linha dos centros.

    No referencial do centro do corpo, o que sobra é a diferença entre o
    campo local e o campo no centro. Ao longo da linha dos centros, em
    primeira ordem em R/d, ela vale 2 G m R / d^3, e aponta PARA FORA nos
    dois lados: daí as duas marés.
    """
    return 2 * G * m * R / d ** 3


def mare_exata(m, d, R, lado):
    """A mesma diferença, sem aproximar, nos dois lados do corpo."""
    if lado == 'perto':
        return G * m / (d - R) ** 2 - G * m / d ** 2
    return G * m / d ** 2 - G * m / (d + R) ** 2


def altura_mare(m, d, R=R_TERRA, g=G_PADRAO):
    """Altura da maré de equilíbrio no ponto sublunar.

    O potencial de maré vale -(G m R^2 / d^3) P2(cos), e a superfície do
    oceano acompanha uma equipotencial, de modo que o desnível é esse
    potencial dividido por g.
    """
    return G * m * R ** 2 / (g * d ** 3)


def limite_roche_fluido(R_prim, rho_prim, rho_sat):
    return 2.44 * R_prim * (rho_prim / rho_sat) ** (1.0 / 3.0)


def limite_roche_rigido(R_prim, rho_prim, rho_sat):
    return R_prim * (2 * rho_prim / rho_sat) ** (1.0 / 3.0)


def main():
    print('=' * 72)
    print('1. O TEOREMA DAS CASCAS, POR INTEGRACAO DIRETA')
    print('=' * 72)
    print('   Casca de raio 1 e massa 1. O campo e calculado somando os')
    print('   aneis, sem usar nenhum teorema.')
    print()
    print('   DENTRO:')
    print('   r         campo calculado     G M / r^2 (se fosse ponto)')
    for r in (0.01, 0.3, 0.7, 0.95, 0.999):
        print('   %7.3f   %+.6e      %.6e'
              % (r, campo_da_casca(r), G / r ** 2))
    print()
    print('   Compare as duas colunas: o campo calculado fica DEZ ORDENS de')
    print('   grandeza abaixo do que haveria se a mesma massa estivesse')
    print('   concentrada num ponto, e o que sobra e erro de quadratura. Ate')
    print('   a um milesimo da superficie, onde a massa mais proxima esta mil')
    print('   vezes mais perto que a do outro lado, sobram tres ordens.')
    print()
    print('   O cancelamento e exato porque a massa de cada cone cresce com o')
    print('   QUADRADO da distancia, na mesma medida em que o campo cai: os')
    print('   dois efeitos se anulam em qualquer direcao que se olhe.')
    print()
    print('   FORA:')
    print('   r         campo calculado     -G M / r^2       diferenca')
    for r in (1.001, 1.5, 3.0, 10.0):
        c = campo_da_casca(r)
        p = -G / r ** 2
        print('   %7.3f   %+.9e   %+.9e   %.1e'
              % (r, c, p, abs(c - p)))
    print()
    print('   Fora, a casca age exatamente como se toda a massa estivesse no')
    print('   centro. E por isso que se pode falar da distancia "ate a Terra"')
    print('   sem dizer ate que parte dela.')
    print()

    print('=' * 72)
    print('2. DENTRO DE UMA ESFERA MACICA')
    print('=' * 72)
    print('   Pelo teorema, so a massa interna ao ponto conta, e ela cresce')
    print('   com r^3: o campo cresce LINEARMENTE com r dentro da esfera.')
    print()
    print('   r/R      campo somando cascas    -G M r / R^3      diferenca')
    for r in (0.2, 0.5, 0.8, 1.0, 1.5):
        c = campo_esfera_macica(r)
        p = campo_esfera_formula(r)
        print('   %5.2f    %+.9e      %+.9e   %.1e' % (r, c, p, abs(c - p)))
    print()
    print('   potencial no centro:     %.6e' % potencial_esfera_formula(0.0))
    print('   potencial na superficie: %.6e' % potencial_esfera_formula(1.0))
    print('   razao:                   %.6f  (deve ser 3/2)'
          % (potencial_esfera_formula(0.0) / potencial_esfera_formula(1.0)))
    print()
    print('   Um corpo largado num tunel pelo centro da Terra faria um')
    print('   oscilador harmonico, porque a forca e proporcional a r:')
    om = np.sqrt(G * M_TERRA / R_TERRA ** 3)
    print('     omega = sqrt(G M / R^3) = %.6e rad/s' % om)
    print('     periodo = %.1f s = %.2f minutos' % (2 * np.pi / om,
                                                    2 * np.pi / om / 60))
    print('   E o mesmo periodo de um satelite rasante, o que nao e')
    print('   coincidencia: as duas contas tem o mesmo G M / R^3.')
    print()

    print('=' * 72)
    print('3. O TESTE DA LUA')
    print('=' * 72)
    print('   A pergunta de Newton: a forca que segura a Lua e a mesma que')
    print('   faz a maca cair? Se for, e se cair com o inverso do quadrado,')
    print('   entao a aceleracao da Lua tem de ser g vezes (R_T/d)^2.')
    print()
    prevista = G_PADRAO * (R_TERRA / D_LUA) ** 2
    medida = 4 * np.pi ** 2 * D_LUA / T_LUA ** 2
    print('   g (R_T/d)^2                     = %.6e m/s^2' % prevista)
    print('   4 pi^2 d / T^2 (medida na orbita) = %.6e m/s^2' % medida)
    print('   razao                           = %.4f' % (medida / prevista))
    print()
    print('   Um por cento de diferenca. Isso NAO e erro de medida, e a')
    print('   conta esta incompleta de dois jeitos:')
    print()
    g_newton = G * M_TERRA / R_TERRA ** 2
    print('   (a) g medido inclui a rotacao da Terra e o achatamento. O g')
    print('       puramente gravitacional vale G M / R^2 = %.6f m/s^2,'
          % g_newton)
    print('       contra %.5f medido.' % G_PADRAO)
    print('   (b) a Lua nao orbita a Terra: as duas orbitam o centro de')
    print('       massa comum. A aceleracao RELATIVA das duas obedece a')
    print('       G(M + m)/d^2, e nao G M / d^2.')
    print()
    prev2 = G * (M_TERRA + M_LUA) / D_LUA ** 2
    print('   Refazendo com as duas correcoes:')
    print('     G (M + m) / d^2 = %.6e m/s^2' % prev2)
    print('     4 pi^2 d / T^2  = %.6e m/s^2' % medida)
    print('     razao           = %.5f' % (medida / prev2))
    print()
    print('   Agora sobram dois decimos de por cento, que e o tamanho da')
    print('   diferenca entre o semieixo maior e a distancia media usada')
    print('   aqui. A licao: quando uma conta de fisica erra 1 %, quase')
    print('   sempre falta um termo, e nao precisao.')
    print()

    print('=' * 72)
    print('4. POR QUE DUAS MARES POR DIA')
    print('=' * 72)
    print('   No referencial do centro da Terra, o que importa e a DIFERENCA')
    print('   entre o campo da Lua em cada ponto e o campo no centro.')
    print()
    perto = mare_exata(M_LUA, D_LUA, R_TERRA, 'perto')
    longe = mare_exata(M_LUA, D_LUA, R_TERRA, 'longe')
    aprox = mare_diferencial(M_LUA, D_LUA, R_TERRA)
    print('   lado voltado para a Lua:  %+.6e m/s^2  (para a Lua)' % perto)
    print('   lado oposto:              %+.6e m/s^2  (para longe da Lua)'
          % longe)
    print('   aproximacao 2 G m R / d^3: %.6e m/s^2' % aprox)
    print()
    print('   Os dois lados sao empurrados PARA FORA do centro da Terra, um')
    print('   em cada sentido, e e por isso que ha duas marés altas por dia e')
    print('   nao uma. O lado proximo e puxado mais que o centro; o lado')
    print('   distante e puxado MENOS que o centro, e portanto fica para tras.')
    print()
    print('   A assimetria entre os dois e de %.2f %%, e vem dos termos de'
          % (100 * (perto - longe) / longe))
    print('   ordem superior em R/d, que a aproximacao despreza.')
    print()
    print('   Repare na potencia: o campo da Lua cai com d^2, mas a maré cai')
    print('   com d^3, porque ela e a DERIVADA do campo. Essa e a razao de a')
    print('   Lua, muito menor que o Sol, mandar nas marés.')
    print()

    print('=' * 72)
    print('5. A ALTURA DA MARE, E O SOL')
    print('=' * 72)
    hl = altura_mare(M_LUA, D_LUA)
    hs = altura_mare(M_SOL, D_SOL)
    print('   mare de equilibrio lunar, no ponto sublunar: %.3f m' % hl)
    print('   mare de equilibrio solar:                    %.3f m' % hs)
    print('   razao lunar/solar: %.3f' % (hl / hs))
    print()
    print('   A amplitude total (de alta a baixa) vale 3/2 da altura acima,')
    print('   porque o potencial de mare varia de +1 a -1/2:')
    print('     lunar: %.3f m        solar: %.3f m' % (1.5 * hl, 1.5 * hs))
    print('     sizigia (soma): %.3f m     quadratura (diferenca): %.3f m'
          % (1.5 * (hl + hs), 1.5 * (hl - hs)))
    print()
    print('   Compare com as mares reais, que chegam a metros. A diferenca')
    print('   nao e erro: a mare de equilibrio supoe um oceano global em')
    print('   equilibrio instantaneo, e o oceano real tem continentes, inercia')
    print('   e ressonancias de bacia. Na baia de Fundy, a mare de 16 m e')
    print('   uma ressonancia da bacia, excitada por uma mare de equilibrio')
    print('   de meio metro: e o modulo 8 em escala geografica.')
    print()
    print('   Razao entre as contribuicoes, se fosse o campo e nao a mare:')
    print('     campo do Sol / campo da Lua = %.1f'
          % ((M_SOL / D_SOL ** 2) / (M_LUA / D_LUA ** 2)))
    print('   O Sol puxa a Terra 178 vezes mais forte que a Lua, e ainda')
    print('   assim faz menos da metade da mare. A potencia tres explica')
    print('   tudo.')
    print()

    print('=' * 72)
    print('6. O LIMITE DE ROCHE')
    print('=' * 72)
    rho_terra = M_TERRA / ((4 / 3) * np.pi * R_TERRA ** 3)
    rho_lua = M_LUA / ((4 / 3) * np.pi * R_LUA ** 3)
    print('   densidade da Terra: %.0f kg/m^3' % rho_terra)
    print('   densidade da Lua:   %.0f kg/m^3' % rho_lua)
    print()
    rig = limite_roche_rigido(R_TERRA, rho_terra, rho_lua)
    flu = limite_roche_fluido(R_TERRA, rho_terra, rho_lua)
    print('   limite de Roche (corpo rigido): %.3e m = %.2f raios terrestres'
          % (rig, rig / R_TERRA))
    print('   limite de Roche (corpo fluido): %.3e m = %.2f raios terrestres'
          % (flu, flu / R_TERRA))
    print('   distancia atual da Lua:         %.3e m = %.2f raios terrestres'
          % (D_LUA, D_LUA / R_TERRA))
    print()
    print('   A Lua esta a 60 raios terrestres, muito alem do limite. Os')
    print('   aneis de Saturno, ao contrario, estao DENTRO do limite de Roche')
    print('   de Saturno, e e por isso que sao aneis e nao uma lua.')


if __name__ == '__main__':
    main()
