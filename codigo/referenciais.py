# -*- coding: utf-8 -*-
"""Referenciais inerciais, e o quanto a Terra não é um deles.

O QUE RESOLVE
    1. Resolve um bloco num plano inclinado com atrito pelo diagrama de corpo
       livre e confere o resultado contra a conservação de energia.
    2. Simula o mesmo movimento visto de um referencial acelerado e mostra
       que a segunda lei só volta a funcionar com a força de inércia.
    3. Mede o quanto a Terra deixa de ser inercial: a variação de g com a
       latitude pela rotação, e o desvio para leste de um corpo que cai.
    4. Calcula o período de precessão de um pêndulo de Foucault em várias
       latitudes, inclusive a do Crato.

A FÍSICA
    A primeira lei não é um caso particular da segunda: ela AFIRMA que
    existem referenciais em que a segunda lei vale, e esses são os
    inerciais. Isso tem consequência prática, porque nenhum laboratório na
    Terra é um deles. O programa mede o tamanho do erro que se comete ao
    tratar a Terra como inercial, e o resultado é tranquilizador para quase
    tudo e decisivo para algumas coisas.

COMO CONFERIR SE ESTÁ CERTO
    1. A aceleração do bloco pelo diagrama tem de bater com a obtida da
       energia, em 1e-12.
    2. No referencial acelerado, a trajetória calculada com a força de
       inércia tem de coincidir com a transformação da trajetória inercial,
       em erro de integrador.
    3. A g calculada com a correção centrífuga tem de reproduzir os valores
       medidos de 9,780 no equador e 9,832 no polo dentro de 0,1 %.
    4. O desvio para leste tem de bater com a fórmula d = (1/3) omega g t^3
       cos(lat), que é a solução de primeira ordem em omega.

Prof. Apiano Morais - LFCA/URCA - Mecânica Clássica I
"""

import numpy as np

G = 9.80665                 # gravidade padrão, m/s^2
OMEGA = 7.292115e-5         # rotação da Terra, rad/s
R_TERRA = 6.371e6           # raio médio, m
R_EQUADOR = 6.378137e6      # raio equatorial, m


# ============================================ 1. plano inclinado com atrito
def plano_inclinado(theta_graus, mu):
    """Aceleração de um bloco que desce, pelo diagrama de corpo livre.

    Projetando na direção do movimento e na normal:
        N = m g cos(theta)
        m a = m g sen(theta) - mu N
    de onde a = g (sen theta - mu cos theta), independente da massa.
    """
    th = np.radians(theta_graus)
    return G * (np.sin(th) - mu * np.cos(th))


def pela_energia(theta_graus, mu, d):
    """A mesma aceleração, obtida do teorema trabalho-energia.

    Descendo uma distância d ao longo do plano, o peso realiza
    m g d sen(theta) e o atrito realiza -mu m g d cos(theta). Igualando
    ao ganho de energia cinética, m v^2 / 2, e usando v^2 = 2 a d.
    """
    th = np.radians(theta_graus)
    trabalho_por_massa = G * d * (np.sin(th) - mu * np.cos(th))
    v2 = 2 * trabalho_por_massa
    return v2 / (2 * d)


# ====================================== 2. o mesmo movimento, outro referencial
def trajetoria_inercial(a_quadro, T, n=200000):
    """Partícula livre, sem força nenhuma, vista do referencial inercial."""
    dt = T / n
    x, v = 0.0, 1.0
    for _ in range(n):
        x += dt * v                      # nenhuma força: v é constante
    return x, v


def trajetoria_no_acelerado(a_quadro, T, n=200000, com_inercia=True):
    """A mesma partícula, vista de um quadro que acelera com a_quadro.

    No quadro acelerado, x' = x - a t^2 / 2, de modo que a partícula
    PARECE acelerada para trás. A segunda lei só continua valendo se
    acrescentarmos a força de inércia -m a_quadro.
    """
    dt = T / n
    x, v = 0.0, 1.0
    for _ in range(n):
        a = -a_quadro if com_inercia else 0.0
        v += dt * a
        x += dt * v
    return x, v


# ============================================ 3. a Terra não é inercial
def g_efetiva(lat_graus):
    """g medida, descontando a aceleração centrípeta da rotação.

    A componente da aceleração centrífuga ao longo da vertical local vale
    omega^2 R cos^2(lat). Este é o efeito da ROTAÇÃO apenas; o achatamento
    da Terra responde por uma parcela comparável, e por isso o resultado
    fica perto, e não igual, ao valor medido.
    """
    lat = np.radians(lat_graus)
    return G - OMEGA ** 2 * R_EQUADOR * np.cos(lat) ** 2


def desvio_leste(h, lat_graus):
    """Desvio para leste de um corpo solto de altura h, em primeira ordem."""
    lat = np.radians(lat_graus)
    t = np.sqrt(2 * h / G)
    return OMEGA * G * t ** 3 * np.cos(lat) / 3.0, t


def desvio_leste_numerico(h, lat_graus, dt=1e-4):
    """O mesmo desvio, integrando as equações no referencial girante.

    a = g - 2 omega x v, com omega apontando para o norte celeste. Em
    coordenadas locais (leste, norte, cima), omega = omega (0, cos lat,
    sen lat).
    """
    lat = np.radians(lat_graus)
    w = OMEGA * np.array([0.0, np.cos(lat), np.sin(lat)])
    r = np.array([0.0, 0.0, h])
    v = np.zeros(3)
    g = np.array([0.0, 0.0, -G])
    while r[2] > 0:
        a = g - 2 * np.cross(w, v)
        v = v + dt * a
        r = r + dt * v
    return r[0]


def foucault(lat_graus):
    """Período de precessão do plano de oscilação, em horas."""
    s = np.sin(np.radians(abs(lat_graus)))
    return float('inf') if s == 0 else 23.9344696 / s


def main():
    print('=' * 70)
    print('1. PLANO INCLINADO: DIAGRAMA CONTRA ENERGIA')
    print('=' * 70)
    print('   theta    mu      a pelo diagrama    a pela energia      dif')
    for th, mu in ((30, 0.0), (30, 0.2), (45, 0.35), (15, 0.3)):
        a1 = plano_inclinado(th, mu)
        a2 = pela_energia(th, mu, 2.5)
        print('   %5d°  %.2f    %12.8f     %12.8f    %.1e'
              % (th, mu, a1, a2, abs(a1 - a2)))
    print()
    print('   Os dois caminhos tem de dar o mesmo numero, e dao: o diagrama')
    print('   de corpo livre e o teorema trabalho-energia sao a mesma fisica')
    print('   escrita de duas maneiras. Repare que a massa sumiu dos dois.')
    print()
    th_lim = np.degrees(np.arctan(0.35))
    print('   Angulo em que o bloco comeca a deslizar com mu = 0,35:')
    print('     theta = arctan(mu) = %.3f graus' % th_lim)
    print('     (abaixo disso a aceleracao daria negativa, o que significa')
    print('      apenas que o bloco fica parado: o atrito estatico segura)')
    print()

    print('=' * 70)
    print('2. O MESMO MOVIMENTO EM DOIS REFERENCIAIS')
    print('=' * 70)
    aq, T = 3.0, 2.0
    xi, vi = trajetoria_inercial(aq, T)
    xc, vc = trajetoria_no_acelerado(aq, T, com_inercia=True)
    xs, vs = trajetoria_no_acelerado(aq, T, com_inercia=False)
    esperado = xi - 0.5 * aq * T ** 2
    print('   Particula LIVRE, v0 = 1 m/s, quadro acelerando a %.1f m/s^2' % aq)
    print('   no referencial inercial:        x = %+.6f m' % xi)
    print('   no acelerado, com inercia:      x = %+.6f m' % xc)
    print('   transformacao x - a t^2 / 2:    x = %+.6f m' % esperado)
    print('   diferenca:                      %.2e m' % abs(xc - esperado))
    print()
    print('   no acelerado, SEM a forca de inercia: x = %+.6f m' % xs)
    print('   erro cometido:                        %.3f m' % abs(xs - esperado))
    print()
    print('   Sem a forca de inercia, a conta erra em metade de a t^2, que em')
    print('   dois segundos ja da 6 metros. A primeira lei nao e decorativa:')
    print('   ela diz em quais referenciais a segunda pode ser usada.')
    print()

    print('=' * 70)
    print('3. QUANTO A TERRA NAO E INERCIAL')
    print('=' * 70)
    print('   aceleracao centrifuga no equador = %.5f m/s^2 (%.2f %% de g)'
          % (OMEGA ** 2 * R_EQUADOR, 100 * OMEGA ** 2 * R_EQUADOR / G))
    print()
    medidos = {0: 9.7803, 15: 9.7838, 30: 9.7932, 45: 9.8062,
               60: 9.8192, 90: 9.8322}
    print('   Comparar valores absolutos seria injusto, porque o modelo de uma')
    print('   linha nao sabe que a Terra e achatada. O que ele preve e a')
    print('   VARIACAO com a latitude, e e isso que a tabela compara:')
    print()
    print('   latitude    modelo (g - g_polo)    medido (g - g_polo)   razao')
    for lat in (0, 15, 30, 45, 60):
        dm = g_efetiva(lat) - g_efetiva(90)
        dr = medidos[lat] - medidos[90]
        print('   %6d°        %+10.5f            %+10.5f        %5.2f'
              % (lat, dm, dr, dm / dr))
    print()
    print('   O modelo explica cerca de dois tercos da variacao medida, com o')
    print('   comportamento certo em cos^2(lat). O terco que falta e o')
    print('   achatamento da Terra: o raio no equador e 21 km maior que no')
    print('   polo, e so isso ja muda g em 0,018 m/s^2.')
    print()
    # a fórmula internacional da gravidade, que já inclui o achatamento
    def g_normal(lat):
        p = np.radians(lat)
        return 9.780327 * (1 + 0.0053024 * np.sin(p) ** 2
                           - 0.0000058 * np.sin(2 * p) ** 2)
    gf, gh = g_normal(-3.72), g_normal(60.17)
    m = 70.0
    print('   Repare no tamanho do efeito. Pela formula internacional da')
    print('   gravidade, que ja inclui o achatamento:')
    print('     Fortaleza (3,72° S):  g = %.5f m/s^2' % gf)
    print('     Helsinque (60,17° N): g = %.5f m/s^2' % gh)
    print('   Uma balanca calibrada em Fortaleza, levada a Helsinque, marca')
    print('   %.0f g a mais num corpo de %.0f kg.' % (1000 * m * (gh / gf - 1), m))
    print()

    print('=' * 70)
    print('4. O DESVIO PARA LESTE DE UM CORPO QUE CAI')
    print('=' * 70)
    print('   altura   latitude   formula (cm)   integrado (cm)    tempo (s)')
    for h, lat in ((100, 0), (100, -7.23), (100, 45), (300, -7.23)):
        d, t = desvio_leste(h, lat)
        dn = desvio_leste_numerico(h, lat)
        print('   %5d m   %7.2f°   %10.3f     %10.3f      %7.3f'
              % (h, lat, 100 * d, 100 * dn, t))
    print()
    print('   Cem metros de queda no Crato desviam 2,2 cm para leste. E')
    print('   pequeno, e e mensuravel: foi assim que Hooke e depois Guglielmini')
    print('   tentaram provar a rotacao da Terra, no seculo XVII.')
    print()

    print('=' * 70)
    print('5. PENDULO DE FOUCAULT')
    print('=' * 70)
    print('   O plano de oscilacao gira com omega sen(lat).')
    print('   lugar                 latitude    periodo de precessao')
    lugares = [('Polo Norte', 90.0), ('Paris (Pantheon)', 48.85),
               ('Sao Paulo', -23.55), ('Crato, CE', -7.23),
               ('Equador', 0.0)]
    for nome, lat in lugares:
        p = foucault(lat)
        if np.isinf(p):
            print('   %-20s  %7.2f°    nao gira' % (nome, lat))
        else:
            print('   %-20s  %7.2f°    %7.1f h  = %5.2f dias'
                  % (nome, lat, p, p / 24))
    print()
    print('   No Crato, o pendulo levaria quase oito dias para dar uma volta')
    print('   completa, o que torna a demonstracao desconfortavel. Em Paris,')
    print('   onde Foucault a fez em 1851, bastam 32 horas.')


if __name__ == '__main__':
    main()
