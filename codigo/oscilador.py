# -*- coding: utf-8 -*-
"""O oscilador harmônico simples, e os seus limites.

O QUE RESOLVE
    1. Mostra que a soma de um seno e um cosseno de mesma frequência é um
       único seno com outra amplitude e outra fase, e confere isso em todos
       os instantes.
    2. Verifica o isocronismo: o período do oscilador harmônico não depende
       da amplitude, em nenhuma ordem.
    3. Mede as médias temporais da energia cinética e da potencial ao longo
       de um ciclo, e a área da elipse no espaço de fase.
    4. Calcula o período exato do pêndulo simples, por quadratura, e compara
       com a aproximação de ângulo pequeno e com a correção de quarta ordem.
    5. Mostra que sistemas sem nenhuma semelhança (pêndulo físico, líquido
       num tubo em U, boia, molécula) obedecem à mesma equação, com
       frequências dadas pela mesma receita.

A FÍSICA
    O oscilador harmônico merece um módulo inteiro não por ser comum, e sim
    por ser INEVITÁVEL: todo mínimo liso de todo potencial é uma parábola
    para amplitudes pequenas, como o módulo 4 mostrou. A equação é a mesma
    sempre, e o trabalho de modelar um sistema novo se reduz a identificar
    quem faz o papel de massa e quem faz o papel de constante elástica.

COMO CONFERIR SE ESTÁ CERTO
    1. A soma A cos(wt) + B sen(wt) e a forma C cos(wt - fase) têm de
       coincidir em 1e-15 em todos os instantes testados.
    2. O período medido na integração não pode mudar com a amplitude, em
       nenhuma casa que o integrador resolva.
    3. As médias de T e de U num ciclo têm de dar E/2 cada uma, e a área da
       elipse no espaço de fase tem de valer 2 pi E / omega.
    4. O período do pêndulo por quadratura tem de bater com a série
       T0 (1 + theta^2/16 + 11 theta^4/3072) para ângulos pequenos, e tem de
       divergir quando theta tende a 180 graus.

Prof. Apiano Morais - LFCA/URCA - Mecânica Clássica I
"""

import numpy as np

G = 9.80665


# ============================================== 1. as duas formas da solução
def forma_soma(t, A, B, w):
    return A * np.cos(w * t) + B * np.sin(w * t)


def forma_amplitude(t, A, B, w):
    """A mesma função, escrita como C cos(wt - fase)."""
    C = np.hypot(A, B)
    fase = np.arctan2(B, A)
    return C * np.cos(w * t - fase)


# ================================================ 2. e 3. o oscilador exato
def integra_oscilador(w, x0, v0, n_periodos=1, n=2000000):
    """Velocity-Verlet, que conserva energia e não distorce o período.

    Devolve o período medido, as médias temporais de T e de U e a área
    varrida no espaço de fase (x, v/w), que é a integral de x dv/w.
    """
    T_esperado = 2 * np.pi / w
    dt = n_periodos * T_esperado / n
    x, v = x0, v0
    a = -w * w * x
    soma_T, soma_U, area = 0.0, 0.0, 0.0
    t_cruz = None
    x_ant, v_ant, t = x, v, 0.0
    for i in range(n):
        x_novo = x + v * dt + 0.5 * a * dt * dt
        a_novo = -w * w * x_novo
        v_novo = v + 0.5 * (a + a_novo) * dt
        # médias pela regra do trapézio
        soma_T += 0.5 * (0.5 * v ** 2 + 0.5 * v_novo ** 2) * dt
        soma_U += 0.5 * (0.5 * w * w * x ** 2 + 0.5 * w * w * x_novo ** 2) * dt
        # área no plano (x, u) com u = v/w, pela regra do trapézio
        area += 0.5 * (x + x_novo) * (v_novo - v) / w
        t += dt
        # Um período é o retorno ao MESMO estado, e não apenas a v = 0.
        # Partindo do repouso em x0, a velocidade zera em T/2 (no outro
        # ponto de retorno) e de novo em T. Só o segundo cruzamento tem o
        # mesmo sentido do início, de positivo para negativo, e é ele que
        # fecha o período: medir pelo primeiro dá metade.
        if t_cruz is None and i > 2 and v_ant > 0 >= v_novo:
            frac = v_ant / (v_ant - v_novo)
            t_cruz = t - dt + frac * dt
        x_ant, v_ant = x, v_novo
        x, v, a = x_novo, v_novo, a_novo
    duracao = n_periodos * T_esperado
    return t_cruz, soma_T / duracao, soma_U / duracao, abs(area)


# ========================================== 4. o pêndulo, sem aproximação
def periodo_pendulo_quadratura(theta0, L=1.0, n=400000):
    """Período exato do pêndulo simples, pela mesma quadratura do módulo 4.

    Da conservação da energia, (L theta')^2 / 2 = g L (cos theta - cos th0),
    de modo que

        T = 4 sqrt(L / 2g) int_0^th0 dth / sqrt(cos th - cos th0).

    O integrando diverge em th0, e a substituição sen(th/2) = sen(th0/2)
    sen(u) cancela a divergência exatamente, deixando a integral elíptica
    completa de primeira espécie. Usamos a regra do ponto médio, que nunca
    avalia nos extremos.
    """
    k = np.sin(theta0 / 2)
    passo = (np.pi / 2) / n
    u = passo * (np.arange(n) + 0.5)
    integrando = 1.0 / np.sqrt(1 - (k * np.sin(u)) ** 2)
    K = float(np.sum(integrando) * passo)
    return 4 * np.sqrt(L / G) * K


def periodo_pendulo_serie(theta0, L=1.0, ordem=4):
    """T0 (1 + th^2/16 + 11 th^4/3072 + ...)."""
    T0 = 2 * np.pi * np.sqrt(L / G)
    s = 1 + theta0 ** 2 / 16
    if ordem >= 4:
        s += 11 * theta0 ** 4 / 3072
    return T0 * s


def periodo_pendulo_integrado(theta0, L=1.0, dt=1e-6):
    """O mesmo período, integrando theta'' = -(g/L) sen(theta)."""
    th, om = theta0, 0.0
    a = -(G / L) * np.sin(th)
    t = 0.0
    while True:
        th_novo = th + om * dt + 0.5 * a * dt * dt
        a_novo = -(G / L) * np.sin(th_novo)
        om_novo = om + 0.5 * (a + a_novo) * dt
        t += dt
        # Solto do repouso em theta0, o pêndulo leva um QUARTO do período
        # para chegar ao fundo, e não metade: o período é quatro vezes
        # esse tempo. Confundir os dois dá metade do valor certo.
        if t > 2 * dt and th_novo <= 0 < th:
            frac = th / (th - th_novo)
            return 4 * (t - dt + frac * dt)
        th, om, a = th_novo, om_novo, a_novo
        if t > 1e3:
            raise RuntimeError('não voltou')


# ================================ 5. a mesma equação em sistemas diferentes
def frequencias():
    """Cinco sistemas, a mesma receita: omega = sqrt(rigidez / inércia)."""
    saida = []

    # mola, 2,5 N/m e 300 g
    k, m = 2.5, 0.300
    saida.append(('mola de 2,5 N/m com 300 g', np.sqrt(k / m),
                  'k / m'))

    # pêndulo simples de 1 m
    saida.append(('pêndulo simples de 1,00 m', np.sqrt(G / 1.0),
                  'g / L'))

    # pêndulo físico: barra uniforme de 1 m presa numa ponta
    # I = mL^2/3, torque restaurador = m g (L/2) theta
    L = 1.0
    saida.append(('barra de 1,00 m presa na ponta',
                  np.sqrt((G * L / 2) / (L * L / 3)), '3g / 2L'))

    # líquido num tubo em U, coluna total de 40 cm
    Lcol = 0.40
    saida.append(('água num tubo em U, 40 cm', np.sqrt(2 * G / Lcol),
                  '2g / L'))

    # boia cilíndrica de 12 cm de altura submersa
    h = 0.12
    saida.append(('boia cilíndrica, 12 cm submersos', np.sqrt(G / h),
                  'g / h'))

    return saida


def main():
    print('=' * 72)
    print('1. AS DUAS FORMAS DA MESMA SOLUCAO')
    print('=' * 72)
    A, B, w = 0.030, -0.040, 7.5
    t = np.linspace(0, 3, 50001)
    d = np.max(np.abs(forma_soma(t, A, B, w) - forma_amplitude(t, A, B, w)))
    C, fase = np.hypot(A, B), np.arctan2(B, A)
    print('   A cos(wt) + B sen(wt)  com A = %.3f m, B = %.3f m' % (A, B))
    print('   C cos(wt - fase)       com C = sqrt(A^2+B^2) = %.4f m' % C)
    print('                          e fase = arctg(B/A) = %.4f rad = %.1f graus'
          % (fase, np.degrees(fase)))
    print('   maior diferenca entre as duas, em 50 mil instantes: %.1e m' % d)
    print()
    print('   As duas constantes sao sempre duas, porque a equacao e de')
    print('   segunda ordem. Elas podem ser (A, B) ou (C, fase), e a escolha')
    print('   e so de conveniencia: a primeira sai direto das condicoes')
    print('   iniciais, a segunda diz na cara qual e a amplitude.')
    print()

    print('=' * 72)
    print('2. ISOCRONISMO: O PERIODO NAO DEPENDE DA AMPLITUDE')
    print('=' * 72)
    w = 3.0
    print('   omega = %.1f rad/s, periodo esperado = %.9f s'
          % (w, 2 * np.pi / w))
    print('   amplitude (m)     periodo medido (s)    diferenca')
    for x0 in (0.01, 0.1, 0.5, 2.0, 10.0):
        per, _, _, _ = integra_oscilador(w, x0, 0.0, n=400000)
        print('   %11.2f      %18.9f    %.1e'
              % (x0, per, abs(per - 2 * np.pi / w)))
    print()
    print('   Mil vezes a amplitude, o mesmo periodo nas nove casas. Isso e')
    print('   particularidade da PARABOLA, e nao propriedade de oscilacao:')
    print('   o poco duplo do modulo 4 nao tem nada disso, e o pendulo da')
    print('   secao 4 tambem nao.')
    print()

    print('=' * 72)
    print('3. A ENERGIA, EM MEDIA, E METADE DE CADA')
    print('=' * 72)
    w, x0 = 3.0, 0.25
    per, mT, mU, area = integra_oscilador(w, x0, 0.0, n_periodos=1, n=2000000)
    E = 0.5 * w * w * x0 ** 2            # por unidade de massa
    print('   omega = %.1f rad/s, amplitude %.2f m, massa unitaria.' % (w, x0))
    print('   energia total E           = %.9f J/kg' % E)
    print('   media de T num ciclo      = %.9f  (E/2 = %.9f)' % (mT, E / 2))
    print('   media de U num ciclo      = %.9f' % mU)
    print('   soma das duas             = %.9f' % (mT + mU))
    print()
    print('   area da elipse no plano (x, v/omega) = %.9f' % area)
    print('   2 pi E / omega^2                     = %.9f'
          % (2 * np.pi * E / w ** 2))
    print()
    print('   A igualdade das duas medias e o teorema do virial para um')
    print('   potencial quadratico, e ela e a razao de tantas contas de')
    print('   energia media darem kT/2 por grau de liberdade na Fisica')
    print('   Estatistica. A area da elipse e a ACAO, que reaparece no')
    print('   modulo 12 e, com outro nome, na quantizacao de Bohr.')
    print()

    print('=' * 72)
    print('4. O PENDULO: ONDE O HARMONICO DEIXA DE VALER')
    print('=' * 72)
    T0 = 2 * np.pi * np.sqrt(1.0 / G)
    print('   Pendulo de 1,00 m. Aproximacao de angulo pequeno: T0 = %.6f s'
          % T0)
    print()
    print('   theta0    T exato (s)   T/T0      serie 4a ordem   erro da serie')
    for graus in (1, 5, 10, 20, 45, 90, 150, 179):
        th = np.radians(graus)
        Te = periodo_pendulo_quadratura(th)
        Ts = periodo_pendulo_serie(th)
        print('   %5d°    %10.6f   %7.5f    %10.6f      %8.2e'
              % (graus, Te, Te / T0, Ts, abs(Ts - Te) / Te))
    print()
    print('   Em 10 graus o erro de usar T0 e de 0,19 %, que e menos que a')
    print('   incerteza de um cronometro de mao: por isso o pendulo serve')
    print('   para medir g em laboratorio. Em 90 graus ja sao 18 %, e em')
    print('   179 graus o periodo e quase quatro vezes maior, a caminho de')
    print('   divergir: o pendulo parado em pe nunca cai, e esse e o mesmo')
    print('   tempo infinito da separatriz do modulo 4.')
    print()
    # conferência contra a integração direta da equação de movimento
    print('   Conferencia por outro caminho, integrando theta\'\' = -(g/L) sen:')
    print('   theta0    quadratura     integracao     diferenca')
    for graus in (10, 45, 90):
        th = np.radians(graus)
        a1 = periodo_pendulo_quadratura(th)
        a2 = periodo_pendulo_integrado(th)
        print('   %5d°    %11.7f    %11.7f    %.1e'
              % (graus, a1, a2, abs(a1 - a2)))
    print()

    print('=' * 72)
    print('5. A MESMA EQUACAO, CINCO SISTEMAS')
    print('=' * 72)
    print('   sistema                             omega (rad/s)   T (s)   receita')
    for nome, om, receita in frequencias():
        print('   %-35s %8.3f     %7.3f   sqrt(%s)'
              % (nome, om, 2 * np.pi / om, receita))
    print()
    print('   Nenhum desses sistemas se parece com os outros, e todos')
    print('   obedecem a mesma equacao. O trabalho de modelar um sistema')
    print('   novo se reduz a duas perguntas: quem faz o papel de massa, e')
    print('   quem faz o papel de constante elastica. A resposta e sempre')
    print('   omega = sqrt(rigidez / inercia).')
    print()
    print('   Repare na boia: a frequencia nao depende da densidade nem do')
    print('   raio, so da altura submersa. E o mesmo pendulo de comprimento')
    print('   h, o que e uma coincidencia que nao e coincidencia nenhuma.')


if __name__ == '__main__':
    main()
