# -*- coding: utf-8 -*-
"""Oscilações forçadas: três ressonâncias que não coincidem, e a resposta
a uma força qualquer.

O QUE RESOLVE
    1. Confere a solução estacionária (amplitude e fase) contra a integração
       numérica, depois de o transiente morrer.
    2. Mostra, medindo, que os picos da amplitude, da velocidade e da
       potência absorvida acontecem em TRES frequencias diferentes, e que
       apenas duas delas coincidem com omega0.
    3. Mede a largura de banda da curva de potência e verifica que ela vale
       exatamente 2 gama, de onde Q = omega0 / largura.
    4. Acompanha o transiente: batimento quando a força está perto da
       ressonância, e o tempo de estabelecimento, que vale 1/gama e nao
       depende da frequencia da forca.
    5. Resolve a resposta a uma força ARBITRARIA pela integral de
       convolução com a função de Green, e confere contra a integração
       direta da equação.

A FÍSICA
    A equação x'' + 2 gama x' + omega0^2 x = (F0/m) cos(omega t) é linear,
    e por isso a sua solução é a soma do transiente (que decai) com o
    estacionário (que dura). O estacionário oscila na frequência da FORÇA, e
    não na do sistema, e isso é o que torna o problema diferente do módulo 7.
    A linearidade também dá de graça o caso geral: se a resposta a um impulso
    é conhecida, a resposta a qualquer força é uma soma de impulsos.

COMO CONFERIR SE ESTÁ CERTO
    1. A amplitude e a fase estacionárias medidas na integração têm de bater
       com as fórmulas em erro de integrador.
    2. O pico de amplitude tem de estar em sqrt(omega0^2 - 2 gama^2), o de
       velocidade exatamente em omega0, e o de potência exatamente em omega0.
    3. A largura a meia altura da curva de potência tem de dar 2 gama.
    4. A convolução com a função de Green tem de reproduzir a integração
       direta para pulsos que não têm nada de senoidal.

Prof. Apiano Morais - LFCA/URCA - Mecânica Clássica I
"""

import numpy as np


# ====================================================== solução estacionária
def amplitude(w, w0, gama, f0):
    """Amplitude do regime estacionário, com f0 = F0/m."""
    return f0 / np.sqrt((w0 ** 2 - w ** 2) ** 2 + (2 * gama * w) ** 2)


def fase(w, w0, gama):
    """Atraso da resposta em relação à força, entre 0 e pi."""
    return np.arctan2(2 * gama * w, w0 ** 2 - w ** 2)


def potencia_media(w, w0, gama, f0):
    """Potência média absorvida, por unidade de massa.

    P = <F v> = (f0 w A / 2) sen(fase), e usando sen(fase) = 2 gama w A / f0
    sai a forma fechada abaixo, que é uma lorentziana em w.
    """
    A = amplitude(w, w0, gama, f0)
    return gama * (w * A) ** 2


def integra(w0, gama, f0, w, t_fim, dt=1e-4, x0=0.0, v0=0.0):
    """Runge-Kutta de 4a ordem para x'' + 2 gama x' + w0^2 x = f0 cos(w t)."""
    n = int(round(t_fim / dt))
    ts = np.empty(n + 1)
    xs = np.empty(n + 1)
    vs = np.empty(n + 1)
    x, v, t = float(x0), float(v0), 0.0
    ts[0], xs[0], vs[0] = t, x, v
    c, k = 2.0 * gama, w0 * w0

    def a(x, v, t):
        return -c * v - k * x + f0 * np.cos(w * t)

    for i in range(1, n + 1):
        k1x, k1v = v, a(x, v, t)
        k2x, k2v = v + dt * k1v / 2, a(x + dt * k1x / 2, v + dt * k1v / 2,
                                       t + dt / 2)
        k3x, k3v = v + dt * k2v / 2, a(x + dt * k2x / 2, v + dt * k2v / 2,
                                       t + dt / 2)
        k4x, k4v = v + dt * k3v, a(x + dt * k3x, v + dt * k3v, t + dt)
        x += dt * (k1x + 2 * k2x + 2 * k3x + k4x) / 6
        v += dt * (k1v + 2 * k2v + 2 * k3v + k4v) / 6
        t += dt
        ts[i], xs[i], vs[i] = t, x, v
    return ts, xs, vs


def mede_estacionario(w0, gama, f0, w, ciclos_espera=None):
    """Amplitude e fase medidas depois de o transiente morrer.

    Espera dez constantes de tempo 1/gama, e então ajusta a cos(wt) +
    b sen(wt) por mínimos quadrados sobre alguns ciclos inteiros: ajustar
    é muito mais preciso que procurar o máximo ponto a ponto.
    """
    T = 2 * np.pi / w
    espera = 10.0 / gama if ciclos_espera is None else ciclos_espera * T
    t_fim = espera + 20 * T
    ts, xs, _ = integra(w0, gama, f0, w, t_fim)
    m = ts >= espera
    t, x = ts[m], xs[m]
    M = np.column_stack([np.cos(w * t), np.sin(w * t)])
    (a, b), *_ = np.linalg.lstsq(M, x, rcond=None)
    # x = a cos + b sen = A cos(wt - fase), com A = hypot e tg fase = b/a
    return np.hypot(a, b), np.arctan2(b, a)


# ============================================= 5. resposta a força qualquer
def green(t, w0, gama):
    """Resposta a um impulso unitário de momento aplicado em t = 0.

    É a solução de x'' + 2 gama x' + w0^2 x = delta(t), que equivale a
    soltar o oscilador do repouso com velocidade 1. Vale zero para t < 0,
    e é essa anulação que garante a causalidade.
    """
    w1 = np.sqrt(w0 ** 2 - gama ** 2)
    return np.where(t < 0, 0.0, np.exp(-gama * t) * np.sin(w1 * t) / w1)


def por_convolucao(forca, w0, gama, ts):
    """x(t) = integral de G(t - s) f(s) ds.

    Escrita como soma dupla, essa integral custa n^2 operações, e com os
    150 mil pontos usados aqui isso são 2e10 multiplicações: horas. Mas
    ela é exatamente uma convolução discreta, e o numpy a calcula de uma
    vez, em C. O resultado é o mesmo; o que muda é esperar segundos em
    vez de horas.

    O fator dt converte a soma em integral. O erro é de primeira ordem
    nas bordas, por ser soma simples e não trapézio, e some com dt.
    """
    dt = ts[1] - ts[0]
    f = np.array([forca(t) for t in ts])
    g = green(ts, w0, gama)
    return np.convolve(g, f)[:len(ts)] * dt


def integra_forca(forca, w0, gama, t_fim, dt=1e-4):
    """A mesma resposta, integrando a equação diretamente.

    A força é chamada como função de um número, e não de um arranjo: num
    laço de trezentos mil passos, criar um arranjo de um elemento a cada
    chamada custa mais que todo o resto da conta junto.
    """
    n = int(round(t_fim / dt))
    ts = np.linspace(0.0, t_fim, n + 1)
    xs = np.empty(n + 1)
    x, v, t = 0.0, 0.0, 0.0
    xs[0] = x
    c, k = 2.0 * gama, w0 * w0

    def a(x, v, t):
        return -c * v - k * x + forca(t)

    for i in range(1, n + 1):
        k1x, k1v = v, a(x, v, t)
        k2x, k2v = v + dt * k1v / 2, a(x + dt * k1x / 2, v + dt * k1v / 2,
                                       t + dt / 2)
        k3x, k3v = v + dt * k2v / 2, a(x + dt * k2x / 2, v + dt * k2v / 2,
                                       t + dt / 2)
        k4x, k4v = v + dt * k3v, a(x + dt * k3x, v + dt * k3v, t + dt)
        x += dt * (k1x + 2 * k2x + 2 * k3x + k4x) / 6
        v += dt * (k1v + 2 * k2v + 2 * k3v + k4v) / 6
        t += dt
        xs[i] = x
    return ts, xs


def main():
    w0, gama, f0 = 4.0, 0.2, 1.0

    print('=' * 72)
    print('1. O ESTACIONARIO, CONFERIDO CONTRA A INTEGRACAO')
    print('=' * 72)
    print('   omega0 = %.1f rad/s, gama = %.2f, f0 = F0/m = %.1f'
          % (w0, gama, f0))
    print()
    print('   omega   A formula    A medida     dif      fase formula  medida')
    for w in (1.0, 3.0, 3.99, 4.0, 4.5, 8.0):
        Af, ff = amplitude(w, w0, gama, f0), fase(w, w0, gama)
        Am, fm = mede_estacionario(w0, gama, f0, w)
        print('   %5.2f   %9.5f   %9.5f   %.1e   %9.4f   %9.4f'
              % (w, Af, Am, abs(Af - Am), ff, fm))
    print()
    print('   Repare na fase: ela vale quase zero bem abaixo da ressonancia')
    print('   (o corpo acompanha a forca), exatamente pi/2 em omega0 e quase')
    print('   pi bem acima (o corpo anda em oposicao). A passagem de 0 a pi')
    print('   acontece numa faixa de largura 2 gama em torno de omega0, e e')
    print('   tanto mais brusca quanto menor o amortecimento.')
    print()

    print('=' * 72)
    print('2. TRES RESSONANCIAS QUE NAO COINCIDEM')
    print('=' * 72)
    print('   Busca fina do maximo de cada curva, para varios gamas:')
    print()
    print('   gama    pico de A      previsto       pico de v    pico de P')
    for g in (0.1, 0.4, 1.0, 2.0, 2.8, 3.0):
        ws = np.linspace(0.1, 8.0, 400001)
        A = amplitude(ws, w0, g, f0)
        V = ws * A
        P = g * V ** 2
        wA = ws[np.argmax(A)]
        wV = ws[np.argmax(V)]
        wP = ws[np.argmax(P)]
        if w0 ** 2 > 2 * g ** 2:
            print('   %5.2f   %9.5f   %12.5f   %11.5f  %10.5f'
                  % (g, wA, np.sqrt(w0 ** 2 - 2 * g ** 2), wV, wP))
        else:
            print('   %5.2f   %9.5f   %12s   %11.5f  %10.5f'
                  % (g, wA, 'nao ha pico', wV, wP))
    print()
    print('   A amplitude tem pico em sqrt(omega0^2 - 2 gama^2), que e MENOR')
    print('   que omega0 e some de vez quando gama passa de omega0/sqrt(2) =')
    print('   %.4f. Acima disso a amplitude so decresce, e o maximo cai'
          % (w0 / np.sqrt(2)))
    print('   na borda da busca: e a ultima linha da tabela.')
    print('   A velocidade e a potencia tem pico exatamente em omega0, em')
    print('   qualquer amortecimento. Sao tres ressonancias diferentes, e a')
    print('   pergunta "qual e a frequencia de ressonancia" so tem resposta')
    print('   depois de dizer ressonancia DE QUE.')
    print()

    print('=' * 72)
    print('3. A LARGURA DA CURVA DE POTENCIA DA O Q')
    print('=' * 72)
    print('   gama    w_baixo    w_alto     largura    2 gama     Q medido   w0/2gama')
    for g in (0.05, 0.1, 0.4, 1.0):
        ws = np.linspace(0.01, 12.0, 2000001)
        P = potencia_media(ws, w0, g, f0)
        meio = P.max() / 2
        dentro = np.where(P >= meio)[0]
        wb, wa = ws[dentro[0]], ws[dentro[-1]]
        largura = wa - wb
        print('   %5.2f   %8.5f   %8.5f   %9.5f   %8.5f   %8.4f   %8.4f'
              % (g, wb, wa, largura, 2 * g, w0 / largura, w0 / (2 * g)))
    print()
    print('   A largura a meia altura vale 2 gama exatamente, em qualquer')
    print('   amortecimento, e nao apenas quando ele e fraco. E por isso que')
    print('   a maneira padrao de medir Q num laboratorio e varrer a')
    print('   frequencia e dividir omega0 pela largura: nao e preciso')
    print('   desligar nada nem cronometrar decaimento.')
    print()

    print('=' * 72)
    print('4. O TRANSIENTE, E O BATIMENTO')
    print('=' * 72)
    g = 0.05
    for w in (3.6, 3.95):
        ts, xs, _ = integra(w0, g, f0, w, 260.0, dt=2e-4)
        env = np.abs(xs)
        # amplitude final, pela formula
        Af = amplitude(w, w0, g, f0)
        # instante a partir do qual |x| nunca mais sai de 2 % do estacionario
        pico_local = []
        for i in range(1, len(xs) - 1):
            if xs[i] > xs[i - 1] and xs[i] >= xs[i + 1]:
                pico_local.append((ts[i], xs[i]))
        fora = [t for t, a in pico_local if abs(a - Af) > 0.02 * Af]
        t_est = fora[-1] if fora else 0.0
        bat = 2 * np.pi / abs(w0 - w)
        print('   omega = %.2f  (|w0-w| = %.2f)' % (w, abs(w0 - w)))
        print('     amplitude estacionaria        = %.5f' % Af)
        print('     maior amplitude do transiente = %.5f' % max(a for _, a in pico_local))
        print('     periodo de batimento previsto = %.2f s' % bat)
        print('     tempo ate estabilizar (2 %%)   = %.1f s = %.2f / gama'
              % (t_est, t_est * g))
        print()
    print('   O transiente ULTRAPASSA o estacionario: 68 % acima dele no')
    print('   primeiro caso e 7 % no segundo. A soma de duas senoides de')
    print('   frequencias parecidas produz batimento, e o primeiro maximo')
    print('   do batimento chega perto do DOBRO do estacionario quando o')
    print('   amortecimento tende a zero. Quem dimensiona estrutura pelo')
    print('   regime permanente subestima o pico, e o fator pode chegar a 2.')
    print()
    print('   E o tempo de estabelecimento quase nao depende de quao perto')
    print('   da ressonancia se esta: deu 3,6 e 3,7 vezes 1/gama nos dois')
    print('   casos, para frequencias bem diferentes. A razao e que quem')
    print('   morre e o TRANSIENTE, que e o problema do modulo 7 e nao sabe')
    print('   nada sobre a forca. Cair a 2 % de uma exponencial leva')
    print('   ln(1/0,02) = %.2f constantes de tempo, e e disso que se trata.'
          % np.log(50))
    print()

    print('=' * 72)
    print('5. A RESPOSTA A UMA FORCA QUALQUER')
    print('=' * 72)
    print('   A funcao de Green G(t) = exp(-gama t) sen(w1 t) / w1 e a')
    print('   resposta a um impulso. Como a equacao e linear, a resposta a')
    print('   qualquer forca e a soma das respostas aos impulsos que a')
    print('   compoem: x(t) = integral de G(t-s) f(s) ds.')
    print()
    g = 0.3
    dt = 2e-4
    t_fim = 20.0
    ts = np.arange(0.0, t_fim + dt / 2, dt)

    def pulso(t):
        """Pulso retangular entre t = 1 e t = 2. Nada senoidal."""
        return 1.0 if 1.0 <= t <= 2.0 else 0.0

    def dente(t):
        """Dente de serra de período 2, que tem descontinuidades."""
        return (t % 2.0) - 1.0 if t >= 0 else 0.0

    def martelo(t):
        """Três marteladas gaussianas estreitas, em tempos quaisquer."""
        s = 0.03
        return sum(np.exp(-((t - t0) / s) ** 2) for t0 in (2.0, 5.5, 6.2))

    print('   forca                 dif com dt      com dt/2      razao')
    for nome, f in (('pulso retangular', pulso), ('dente de serra', dente),
                    ('tres marteladas', martelo)):
        difs = []
        for passo in (dt, dt / 2):
            tt = np.arange(0.0, t_fim + passo / 2, passo)
            xc = por_convolucao(f, w0, g, tt)
            _, xd = integra_forca(f, w0, g, t_fim, dt=passo)
            difs.append(np.max(np.abs(xc - xd)))
        print('   %-20s  %.2e      %.2e     %5.2f'
              % (nome, difs[0], difs[1], difs[0] / difs[1]))
    print()
    print('   Tres forcas sem nenhuma relacao com senoides, e a convolucao')
    print('   reproduz a integracao direta. As razoes dizem de que tamanho')
    print('   e a diferenca que sobra: 2 para as duas forcas com salto, isto')
    print('   e, erro de PRIMEIRA ordem no passo, e 4 para as marteladas,')
    print('   que sao suaves, isto e, SEGUNDA ordem. A soma usada aqui e a')
    print('   regra do retangulo, que e de primeira ordem quando o')
    print('   integrando tem descontinuidade e ganha uma ordem quando nao')
    print('   tem. Nao ha discordancia entre os dois metodos: ha o erro de')
    print('   quadratura de um deles, e ele some com o passo.')
    print()
    print('   Isso e o principio da superposicao funcionando: resolver UMA')
    print('   vez, para o impulso, resolve para sempre, para qualquer forca.')
    print()
    print('   Essa ideia nao fica na mecanica. A funcao de Green e a mesma')
    print('   ferramenta que resolve circuitos, propagacao de ondas, difusao')
    print('   de calor e, com outro nome, o propagador da teoria quantica de')
    print('   campos. O oscilador amortecido e o exemplo mais barato dela.')


if __name__ == '__main__':
    main()
