# -*- coding: utf-8 -*-
"""Retratos de fase: pontos fixos, separatrizes, bacias e ciclos-limite.

O QUE RESOLVE
    1. Desenha (em números) o retrato de fase do pêndulo e identifica os dois
       tipos de movimento, libração e rotação, separados pela separatriz.
    2. Classifica os pontos fixos pela matriz jacobiana, comparando os
       autovalores analíticos com os calculados por diferenças finitas.
    3. Verifica que uma trajetória lançada perto de uma sela sai ao longo da
       direção do autovetor instável, que é o que a linearização promete.
    4. Mapeia as bacias de atração do pêndulo amortecido: em qual dos
       mínimos o pêndulo para, dado o chute inicial.
    5. Mostra que o oscilador de van der Pol tem um ciclo-limite ÚNICO e
       atrator, ao qual trajetórias de dentro e de fora convergem, e mede a
       amplitude e o período nos dois limites.

A FÍSICA
    Sem solução fechada, ainda se pode saber tudo o que importa olhando o
    plano (posição, velocidade). As equações dizem, em cada ponto, para onde
    a trajetória vai; os pontos onde ela não vai a lugar nenhum são os pontos
    fixos, e o comportamento perto deles é decidido por uma matriz 2x2. É
    uma mudança de atitude: em vez de perguntar "qual é x(t)", pergunta-se
    "que tipos de movimento existem".

COMO CONFERIR SE ESTÁ CERTO
    1. Os autovalores da jacobiana calculada por diferenças finitas têm de
       bater com os analíticos em todos os pontos fixos.
    2. A separatriz do pêndulo tem de estar exatamente em E = 2 m g L, e
       trajetórias logo abaixo e logo acima têm de fazer coisas diferentes.
    3. A direção de saída de uma sela tem de coincidir com o autovetor
       instável, em erro de integrador.
    4. No ciclo-limite de van der Pol, trajetórias de dentro e de fora têm
       de convergir para a MESMA curva; a amplitude tem de tender a 2 quando
       mu tende a zero, e o período dividido por mu tem de tender a
       3 - 2 ln 2 = 1,6137 quando mu é grande.

Prof. Apiano Morais - LFCA/URCA - Mecânica Clássica I
"""

import numpy as np

G = 9.80665


# ============================================================ o pêndulo
def campo_pendulo(th, om, g_sobre_l=1.0, gama=0.0):
    """O campo de velocidades no plano de fase: (d theta/dt, d omega/dt)."""
    return om, -g_sobre_l * np.sin(th) - 2 * gama * om


def integra(campo, estado, t_fim, dt=1e-4, parar=None):
    """Runge-Kutta de 4a ordem para um sistema de duas equações."""
    n = int(round(t_fim / dt))
    x, y = float(estado[0]), float(estado[1])
    saida = np.empty((n + 1, 2))
    saida[0] = (x, y)
    for i in range(1, n + 1):
        k1 = campo(x, y)
        k2 = campo(x + dt * k1[0] / 2, y + dt * k1[1] / 2)
        k3 = campo(x + dt * k2[0] / 2, y + dt * k2[1] / 2)
        k4 = campo(x + dt * k3[0], y + dt * k3[1])
        x += dt * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
        y += dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
        saida[i] = (x, y)
        if parar is not None and parar(x, y):
            return saida[:i + 1]
    return saida


def jacobiana(campo, x, y, h=1e-6):
    """Matriz das derivadas do campo, por diferenças centradas."""
    fx1, fy1 = campo(x + h, y)
    fx2, fy2 = campo(x - h, y)
    fx3, fy3 = campo(x, y + h)
    fx4, fy4 = campo(x, y - h)
    return np.array([[(fx1 - fx2) / (2 * h), (fx3 - fx4) / (2 * h)],
                     [(fy1 - fy2) / (2 * h), (fy3 - fy4) / (2 * h)]])


def classifica(autovalores):
    """Nome do ponto fixo, a partir dos autovalores da jacobiana."""
    a, b = autovalores
    if abs(a.imag) > 1e-9:
        if abs(a.real) < 1e-9:
            return 'centro'
        return 'foco estável' if a.real < 0 else 'foco instável'
    if a.real * b.real < 0:
        return 'sela'
    if a.real < 0:
        return 'nó estável'
    return 'nó instável'


# ====================================================== van der Pol
def campo_vdp(x, y, mu=1.0):
    """x'' - mu (1 - x^2) x' + x = 0, escrita como duas de primeira ordem.

    O termo de amortecimento muda de sinal: é NEGATIVO para |x| < 1, isto
    é, bombeia energia perto da origem, e positivo para |x| > 1, isto é,
    dissipa longe dela. Entre os dois regimes sobra uma órbita fechada.
    """
    return y, mu * (1 - x * x) * y - x


def amplitude_e_periodo(mu, inicial=(0.1, 0.0), t_fim=None, dt=None):
    """Amplitude e período do ciclo-limite, medidos depois do transiente."""
    if t_fim is None:
        t_fim = max(200.0, 60.0 * mu)
    if dt is None:
        dt = min(1e-3, 1e-3 / max(1.0, mu))
    traj = integra(lambda x, y: campo_vdp(x, y, mu), inicial, t_fim, dt)
    # usa só o último terço, quando o transiente já morreu
    corte = 2 * len(traj) // 3
    x = traj[corte:, 0]
    amp = max(x.max(), -x.min())
    # período pelos cruzamentos de zero no sentido crescente
    zeros = []
    for i in range(len(x) - 1):
        if x[i] < 0 <= x[i + 1]:
            f = -x[i] / (x[i + 1] - x[i])
            zeros.append((corte + i + f) * dt)
    if len(zeros) < 3:
        return amp, float('nan')
    return amp, float(np.mean(np.diff(zeros)))


def main():
    print('=' * 72)
    print('1. O RETRATO DE FASE DO PENDULO')
    print('=' * 72)
    print('   Com g/L = 1, a energia por unidade de m L^2 vale')
    print('     e = omega^2 / 2 + (1 - cos theta),')
    print('   que vale 0 no fundo e 2 no alto. A separatriz e e = 2.')
    print()
    campo = lambda th, om: campo_pendulo(th, om, 1.0, 0.0)
    print('   theta0   omega0     energia    o que acontece em 40 s')
    for th0, om0 in ((0.5, 0.0), (3.0, 0.0), (0.0, 1.9),
                     (0.0, 1.999999), (0.0, 2.000001), (0.0, 2.5)):
        e = om0 ** 2 / 2 + (1 - np.cos(th0))
        tr = integra(campo, (th0, om0), 40.0, dt=2e-4)
        voltas = (tr[-1, 0] - tr[0, 0]) / (2 * np.pi)
        tipo = 'ROTACAO, %.2f voltas' % voltas if abs(voltas) > 0.5 else 'libracao'
        print('   %6.2f   %8.6f   %9.6f   %s' % (th0, om0, e, tipo))
    print()
    print('   A fronteira entre os dois tipos de movimento e exatamente')
    print('   e = 2: as duas linhas do meio diferem em 2e-6 na velocidade')
    print('   inicial e fazem coisas qualitativamente diferentes. Em cima')
    print('   da separatriz o pendulo leva tempo INFINITO para chegar ao')
    print('   alto, que e o mesmo resultado do modulo 6.')
    print()

    print('=' * 72)
    print('2. OS PONTOS FIXOS, E O QUE A MATRIZ 2x2 DECIDE')
    print('=' * 72)
    print('   Nos pontos fixos o campo se anula: omega = 0 e sen(theta) = 0.')
    print('   Perto deles a dinamica e decidida pelos autovalores da')
    print('   jacobiana, que a rotina calcula por diferencas finitas.')
    print()
    for gama, nome in ((0.0, 'pendulo sem atrito'), (0.3, 'pendulo com atrito')):
        campo = lambda th, om: campo_pendulo(th, om, 1.0, gama)
        print('   %s (gama = %.1f)' % (nome, gama))
        print('     ponto fixo      autovalores                 tipo')
        for th in (0.0, np.pi):
            J = jacobiana(campo, th, 0.0)
            vals = np.linalg.eigvals(J)
            if abs(vals[0].imag) > 1e-9:
                desc = '%+.4f +- %.4fi' % (vals[0].real, abs(vals[0].imag))
            else:
                desc = '%+.4f e %+.4f' % (vals[0].real, vals[1].real)
            print('     theta = %-7s %-26s %s'
                  % ('0' if th == 0 else 'pi', desc, classifica(vals)))
        # conferência contra os autovalores analíticos
        ana0 = np.roots([1, 2 * gama, 1.0])
        anapi = np.roots([1, 2 * gama, -1.0])
        J0 = np.linalg.eigvals(jacobiana(campo, 0.0, 0.0))
        Jpi = np.linalg.eigvals(jacobiana(campo, np.pi, 0.0))
        d0 = np.max(np.abs(np.sort_complex(ana0) - np.sort_complex(J0)))
        dpi = np.max(np.abs(np.sort_complex(anapi) - np.sort_complex(Jpi)))
        print('     diferenca para os autovalores analiticos: %.1e e %.1e'
              % (d0, dpi))
        print()
    print('   Sem atrito, o fundo e um CENTRO: autovalores imaginarios puros,')
    print('   o pendulo orbita e nunca para. Com atrito vira FOCO ESTAVEL, e')
    print('   a orbita vira espiral. O alto e SELA nos dois casos, e e por')
    print('   isso que o equilibrio instavel nao depende de atrito: ele e')
    print('   instavel por geometria, nao por dissipacao.')
    print()

    print('=' * 72)
    print('3. SAINDO DE UMA SELA PELA DIRECAO PREVISTA')
    print('=' * 72)
    campo = lambda th, om: campo_pendulo(th, om, 1.0, 0.3)
    J = jacobiana(campo, np.pi, 0.0)
    vals, vecs = np.linalg.eig(J)
    i_inst = int(np.argmax(vals.real))
    v = vecs[:, i_inst].real
    v = v / np.linalg.norm(v)
    print('   Sela em theta = pi. Autovalor instavel: %+.6f' % vals[i_inst].real)
    print('   Autovetor instavel (normalizado): (%+.6f, %+.6f)' % (v[0], v[1]))
    print()
    print('   Deslocamento inicial   direcao da trajetoria     angulo (graus)')
    for eps in (1e-3, 1e-4, 1e-5, 1e-6):
        # empurrado numa direcao QUALQUER, perpendicular ao autovetor
        perp = np.array([-v[1], v[0]])
        ini = np.array([np.pi, 0.0]) + eps * perp
        tr = integra(campo, ini, 12.0, dt=1e-4)
        d = tr[-1] - np.array([np.pi, 0.0])
        d = d / np.linalg.norm(d)
        ang = np.degrees(np.arccos(np.clip(abs(np.dot(d, v)), -1, 1)))
        print('   %18.0e   (%+.6f, %+.6f)   %10.4f' % (eps, d[0], d[1], ang))
    print()
    print('   O chute inicial foi PERPENDICULAR ao autovetor instavel, e')
    print('   mesmo assim a trajetoria sai alinhada com ele: o angulo vai a')
    print('   zero quando o deslocamento inicial diminui. A sela esquece a')
    print('   direcao de entrada e impoe a sua. E isso que torna a')
    print('   linearizacao util mesmo longe do ponto fixo.')
    print()

    print('=' * 72)
    print('4. BACIAS DE ATRACAO DO PENDULO AMORTECIDO')
    print('=' * 72)
    gama = 0.15
    campo = lambda th, om: campo_pendulo(th, om, 1.0, gama)
    print('   Pendulo amortecido (gama = %.2f) solto de theta = 0 com' % gama)
    print('   velocidades crescentes. Em qual minimo ele para?')
    print()
    print('   omega0    minimo final    voltas completas')
    anterior = None
    trocas = []
    for om0 in np.arange(1.0, 6.01, 0.05):
        tr = integra(campo, (0.0, om0), 200.0, dt=1e-3)
        k = int(round(tr[-1, 0] / (2 * np.pi)))
        if anterior is not None and k != anterior:
            trocas.append((om0, anterior, k))
        anterior = k
        if abs(om0 - round(om0 * 2) / 2) < 1e-9:     # imprime de meio em meio
            print('   %6.2f    theta = %4d pi    %d' % (om0, 2 * k, k))
    print()
    print('   As trocas de bacia acontecem em:')
    for om0, a, b in trocas:
        print('     entre omega0 = %.2f e %.2f, o pendulo passa do minimo'
              % (om0 - 0.05, om0))
        print('     %d pi para o minimo %d pi' % (2 * a, 2 * b))
    print()
    print('   Repare que as faixas ficam mais estreitas quando a velocidade')
    print('   cresce. Perto de uma fronteira, uma diferenca minima no chute')
    print('   leva o pendulo a parar uma volta inteira adiante: a dinamica e')
    print('   previsivel (nao ha caos aqui), mas a DEPENDENCIA do resultado')
    print('   final com a condicao inicial ja e desconfortavel. O modulo 10')
    print('   mostra o que acontece quando essa sensibilidade deixa de ser')
    print('   so uma questao de fronteiras.')
    print()

    print('=' * 72)
    print('5. O CICLO-LIMITE DE VAN DER POL')
    print('=' * 72)
    print('   x\'\' - mu (1 - x^2) x\' + x = 0. O amortecimento e NEGATIVO')
    print('   perto da origem e positivo longe dela, de modo que nem o')
    print('   repouso nem a amplitude grande sobrevivem.')
    print()
    print('   Convergencia de dentro e de fora para a MESMA curva:')
    print('   mu     amplitude de dentro   de fora     diferenca')
    for mu in (0.1, 1.0, 4.0):
        a_in, _ = amplitude_e_periodo(mu, (0.05, 0.0))
        a_out, _ = amplitude_e_periodo(mu, (4.0, 0.0))
        print('   %4.1f   %17.9f   %9.9f   %.1e'
              % (mu, a_in, a_out, abs(a_in - a_out)))
    print()
    print('   Nao e coincidencia nem escolha de condicao inicial: o ciclo e')
    print('   unico e atrai todo mundo (menos a origem, que e ponto fixo).')
    print('   Isso e uma OSCILACAO AUTOSSUSTENTADA: a amplitude nao vem das')
    print('   condicoes iniciais, como no modulo 6, e sim do proprio sistema.')
    print()
    print('   Limite de mu pequeno: a amplitude tende a 2')
    print('   mu        amplitude     periodo    2 pi')
    for mu in (0.5, 0.2, 0.05, 0.01):
        a, T = amplitude_e_periodo(mu)
        print('   %5.2f   %11.6f   %9.6f   %.6f' % (mu, a, T, 2 * np.pi))
    print()
    print('   Limite de mu grande: o periodo cresce como (3 - 2 ln 2) mu')
    print('   mu        periodo      T / mu      3 - 2 ln 2')
    alvo = 3 - 2 * np.log(2)
    for mu in (5.0, 10.0, 20.0, 40.0):
        a, T = amplitude_e_periodo(mu, (2.0, 0.0))
        print('   %5.1f   %11.5f   %9.6f   %10.6f' % (mu, T, T / mu, alvo))
    print()
    print('   Com mu grande o movimento deixa de ser senoidal: sao cargas')
    print('   lentas seguidas de descargas rapidas, o que se chama oscilacao')
    print('   de RELAXACAO. Van der Pol encontrou isso em 1920 estudando')
    print('   circuitos de valvula, e a mesma equacao descreve o batimento')
    print('   cardiaco, o disparo de neuronios e o som da palheta de um')
    print('   clarinete. O amortecimento negativo e o mesmo do flutter do')
    print('   modulo 8: a diferenca e que aqui a nao linearidade o segura.')


if __name__ == '__main__':
    main()
