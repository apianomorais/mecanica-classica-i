# -*- coding: utf-8 -*-
"""Momento linear, impulso e o foguete de massa variável.

O QUE RESOLVE
    1. Verifica o teorema do impulso para uma força que varia no tempo, e
       mostra que a força média que importa é a média no TEMPO e não a média
       na distância.
    2. Deduz a equação de Tsiolkovsky integrando a equação do foguete e
       confere o resultado contra a integração numérica passo a passo.
    3. Mede o que a gravidade cobra durante a queima, que é a diferença
       entre o delta-v ideal e o delta-v que sobra.
    4. Compara um foguete de um estágio com um de dois estágios de mesma
       massa total e mesma fração estrutural, e mede quanto o estagiamento
       rende.
    5. Mostra onde a conta ingênua de massa variável dá errado: a corrente
       que cai sobre a mesa e o vagão que recolhe areia.

A FÍSICA
    A segunda lei na forma F = ma vale para massa constante. A forma geral
    é F = dp/dt, e quando a massa do corpo muda é preciso dizer o que entra
    e o que sai, e com que velocidade. O foguete expele massa com velocidade
    v_e relativa a ele, e daí sai a equação do foguete. Trocar as duas
    formas uma pela outra é o erro clássico do assunto, e ele aparece na
    seção 5.

COMO CONFERIR SE ESTÁ CERTO
    1. O impulso calculado pela integral da força tem de dar a variação de
       momento medida na integração, em 1e-12.
    2. O delta-v de Tsiolkovsky tem de coincidir com a integração numérica
       da equação do foguete em erro de integrador.
    3. Com gravidade constante, a diferença entre o delta-v ideal e o
       obtido tem de valer exatamente g vezes o tempo de queima.
    4. No limite de carga útil nula, os dois estágios têm de render o dobro
       do logaritmo de um estágio só.

Prof. Apiano Morais - LFCA/URCA - Mecânica Clássica I
"""

import numpy as np

G0 = 9.80665


# ====================================================== 1. impulso e momento
def forca(t, T=0.012, F0=2400.0):
    """Um chute: força que sobe e desce em sen^2 durante T segundos."""
    return np.where((t >= 0) & (t <= T), F0 * np.sin(np.pi * t / T) ** 2, 0.0)


def impulso_analitico(T=0.012, F0=2400.0):
    """int sen^2 = T/2, de modo que J = F0 T / 2."""
    return F0 * T / 2


def integra_chute(m=0.43, T=0.012, F0=2400.0, n=400000):
    """Integra m dv/dt = F(t) e devolve (v_final, deslocamento no contato).

    O deslocamento que interessa é o percorrido ENQUANTO o pé toca a
    bola, e não o da janela de integração: depois que a força acaba a
    bola continua andando, e somar esse trecho infla o número.
    """
    dt = T / n
    v, x, t = 0.0, 0.0, 0.0
    for _ in range(n):
        a = float(forca(t + dt / 2, T, F0)) / m        # ponto médio
        v += dt * a
        x += dt * v
        t += dt
    return v, x, t


# ======================================================== 2. o foguete ideal
def tsiolkovsky(ve, m0, mf):
    return ve * np.log(m0 / mf)


def integra_foguete(ve, m0, mf, taxa, g=0.0, dt=1e-5):
    """Integra m dv/dt = ve |dm/dt| - m g, com dm/dt = -taxa constante.

    Devolve (v_final, tempo de queima). A massa entra na conta a cada
    passo, e é isso que torna o problema diferente de uma força constante.
    """
    v, m, t = 0.0, m0, 0.0
    while m > mf:
        passo = min(dt, (m - mf) / taxa)
        if passo <= 0:
            break
        # a massa no meio do passo: com a massa do começo, o erro do
        # integrador apareceria na quarta casa e estragaria a comparação
        # com Tsiolkovsky, que é o ponto do exercício
        a = ve * taxa / (m - taxa * passo / 2) - g
        v += passo * a
        m -= passo * taxa
        t += passo
    return v, t


# ===================================================== 3. e 4. estagiamento
def um_estagio(ve, m_total, carga, eps):
    """Delta-v de um estágio só.

    eps é a fração estrutural: a massa de tanques e motores dividida pela
    massa do estágio inteiro (estrutura mais propelente). O que sobra, em
    cima da carga útil, é propelente.
    """
    m_estagio = m_total - carga
    m_estrutura = eps * m_estagio
    m_final = carga + m_estrutura
    return ve * np.log(m_total / m_final)


def n_estagios_identicos(ve, m_total, carga, eps, n):
    """Delta-v de n estágios idênticos, em forma fechada.

    Quando todos os estágios têm a mesma fração estrutural e o mesmo ve, o
    ótimo é reparti-los de modo que cada um multiplique a massa pela mesma
    razão r = (m_total/carga)^(1/n). O estágio i parte de M_i e termina em
    M_{i+1} + eps (M_i - M_{i+1}), de onde

        delta-v por estágio = ve ln[ r / (1 + eps (r - 1)) ].

    Para n = 1 isso se reduz exatamente a um_estagio(), e para n = 2 tem de
    coincidir com o melhor valor da busca numérica, que é o teste feito no
    main().
    """
    r = (m_total / carga) ** (1.0 / n)
    return n * ve * np.log(r / (1 + eps * (r - 1)))


def dois_estagios(ve, m_total, carga, eps, fracao):
    """Dois estágios em série, com a mesma fração estrutural.

    'fracao' é a parte da massa de foguete (sem a carga) que fica no
    primeiro estágio. O segundo estágio inteiro, com a carga dentro, é a
    carga útil do primeiro.
    """
    m_foguete = m_total - carga
    m1 = fracao * m_foguete
    m2 = (1 - fracao) * m_foguete
    # primeiro estágio: empurra tudo
    final1 = m_total - (1 - eps) * m1
    dv1 = ve * np.log(m_total / final1)
    # segundo: já largou o primeiro inteiro
    inicio2 = carga + m2
    final2 = carga + eps * m2
    dv2 = ve * np.log(inicio2 / final2)
    return dv1 + dv2, dv1, dv2


# ============================================ 5. massa variável mal contada
def corrente_na_mesa(L=1.0, mu=1.0, n=200001):
    """Força sobre a mesa enquanto a corrente cai, por dois caminhos.

    O caminho curto: a mesa sustenta o peso do que já parou, mu g x, e
    ainda absorve o momento do que chega, mu v^2 = 2 mu g x, de modo que
    a força vale 3 mu g x.

    O caminho honesto, que é o que o programa usa para CONFERIR: aplicar
    F = dp/dt à corrente inteira, de massa fixa mu L. As forças externas
    sobre ela são o peso total e a normal da mesa, de modo que

        mu L g - N = dp/dt,     com p = mu (L - x) v,

    já que só o pedaço que ainda cai tem momento. Derivando p
    numericamente a partir da queda livre e isolando N, sai um número que
    não usou em lugar algum a fórmula que se quer verificar.
    """
    t_fim = np.sqrt(2 * L / G0)
    t = np.linspace(0, t_fim, n)
    x = np.minimum(0.5 * G0 * t ** 2, L)
    v = G0 * t
    p = mu * (L - x) * v                      # momento do trecho que cai
    dpdt = np.gradient(p, t)
    N = mu * L * G0 - dpdt                    # pela segunda lei
    return x, N, 3 * mu * G0 * x



# ============================================ 6. gravidade que varia com h
R_TERRA = 6.371e6          # raio médio da Terra, m
MU_TERRA = 3.986004418e14  # GM da Terra, m^3/s^2
G_SUP = MU_TERRA / R_TERRA ** 2

# Repare que G_SUP = 9,8201 m/s^2 NAO e o 9,80665 usado ate aqui. A
# diferenca, de 0,14 %, nao e erro de arredondamento: 9,80665 e a gravidade
# padrao, um valor convencionado que ja desconta a rotacao da Terra e vale
# perto da latitude 45, enquanto GM/R^2 e o valor newtoniano puro para uma
# Terra esferica de raio medio. Misturar os dois faz a conferencia por
# energia desta secao discordar da integracao na terceira casa, que foi
# exatamente o que aconteceu na primeira versao deste codigo. Daqui em
# diante tudo vem de GM e R, e so.


def g_altura(h, R=R_TERRA, mu=MU_TERRA):
    """Aceleração da gravidade a uma altura h acima da superfície."""
    return mu / (R + h) ** 2


def integra_subida(ve, m0, mf, tq, dt=0.002, variavel=True, coast=True):
    """Sobe na vertical com empuxo constante e devolve o voo inteiro.

    Integra, com RK4 em (v, h):

        dv/dt = ve * taxa / m - g(h),    dh/dt = v,    dm/dt = -taxa

    com taxa = (m0 - mf) / tq. Depois do fim do propelente segue em queda
    livre até o apogeu, que é onde a velocidade troca de sinal.

    O cuidado que o problema exige está no começo: enquanto o empuxo não
    vence o peso, o foguete fica NA PLATAFORMA. Sem essa trava o
    integrador devolve velocidade negativa e altura negativa, e o
    resultado parece razoável até alguém olhar o sinal. Veja a seção 6 da
    saída: com tempo de queima longo demais o veículo não decola, e o
    programa tem de dizer isso em vez de inventar um voo subterrâneo.

    Devolve um dicionário com o estado no fim da queima, o apogeu e a
    perda gravitacional medida por integração, que é o que se compara com
    g0 * tq.
    """
    taxa = (m0 - mf) / tq
    empuxo = ve * taxa

    def gg(h):
        return g_altura(h) if variavel else G_SUP

    def deriv(t, v, h):
        m = max(m0 - taxa * t, mf)
        a = (empuxo / m if t < tq else 0.0) - gg(h)
        # na plataforma: enquanto o empuxo não vence o peso, nada acontece
        if h <= 0.0 and a <= 0.0:
            return 0.0, 0.0
        return a, v

    t, v, h = 0.0, 0.0, 0.0
    perda = 0.0            # integral de g(h) dt DEPOIS de sair do chao
    decolou = False
    m_decolagem = m0       # massa no instante em que o empuxo vence o peso
    while t < tq - 1e-12:
        passo = min(dt, tq - t)
        k1 = deriv(t, v, h)
        k2 = deriv(t + passo / 2, v + passo * k1[0] / 2, h + passo * k1[1] / 2)
        k3 = deriv(t + passo / 2, v + passo * k2[0] / 2, h + passo * k2[1] / 2)
        k4 = deriv(t + passo, v + passo * k3[0], h + passo * k3[1])
        v += passo / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        h += passo / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        if h > 0.0 and not decolou:
            decolou = True
            m_decolagem = max(m0 - taxa * t, mf)
        if decolou:
            perda += passo * gg(h)
        t += passo
    v_fim, h_fim = v, h

    h_apo = h
    if coast and v > 0:
        while v > 0:
            k1 = (-gg(h), v)
            k2 = (-gg(h + dt * k1[1] / 2), v + dt * k1[0] / 2)
            k3 = (-gg(h + dt * k2[1] / 2), v + dt * k2[0] / 2)
            k4 = (-gg(h + dt * k3[1]), v + dt * k3[0])
            v += dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            h += dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        h_apo = h

    # O propelente queimado antes de sair do chao e perda tambem, e de
    # outra especie: nao e arrasto gravitacional, e combustivel gasto
    # empurrando a plataforma. Vale o delta-v que ele teria dado.
    plataforma = ve * np.log(m0 / m_decolagem)
    return {'v': v_fim, 'h': h_fim, 'perda': perda, 'apogeu': h_apo,
            'decolou': decolou, 'taxa': taxa, 'empuxo': empuxo,
            'plataforma': plataforma, 'm_decolagem': m_decolagem,
            'peso0': m0 * G_SUP}


def apogeu_por_energia(v, h, R=R_TERRA, mu=MU_TERRA):
    """Apogeu do voo livre pela conservação de energia, com U = -mu/r.

    É a conferência independente da integração: a energia específica
    vale v^2/2 - mu/r e no apogeu a velocidade é nula.
    """
    r = R + h
    e = v * v / 2 - mu / r
    if e >= 0:
        return float('inf')          # escapa
    return -mu / e - R


def apogeu_ingenuo(v, h):
    """O mesmo apogeu com mgh, isto é, supondo g constante."""
    return h + v * v / (2 * G_SUP)


def main():
    print('=' * 72)
    print('1. IMPULSO: A FORCA QUE IMPORTA E A MEDIA NO TEMPO')
    print('=' * 72)
    m, T, F0 = 0.43, 0.012, 2400.0
    v, x, _ = integra_chute(m, T, F0)
    J = impulso_analitico(T, F0)
    print('   Bola de futebol de %.2f kg, chute de %.0f N de pico em %.0f ms.'
          % (m, F0, 1000 * T))
    print('   impulso J = F0 T / 2        = %.6f N s' % J)
    print('   momento final m v           = %.6f kg m/s' % (m * v))
    print('   diferenca                   = %.2e' % abs(J - m * v))
    print('   velocidade de saida         = %.3f m/s = %.1f km/h'
          % (v, 3.6 * v))
    print()
    print('   forca de pico               = %.0f N' % F0)
    print('   forca media no tempo        = %.0f N  (= J / T)' % (J / T))
    print('   a bola anda %.1f cm enquanto o pe a toca.' % (100 * x))
    print()
    print('   Repare que a forca media no TEMPO e metade do pico, e e ela')
    print('   que determina a velocidade de saida. A media na DISTANCIA')
    print('   daria outro numero, e responderia outra pergunta: a energia.')
    print()

    print('=' * 72)
    print('2. A EQUACAO DO FOGUETE')
    print('=' * 72)
    ve, m0, mf, taxa = 2942.0, 50000.0, 10000.0, 200.0
    dv_t = tsiolkovsky(ve, m0, mf)
    dv_n, tq = integra_foguete(ve, m0, mf, taxa)
    print('   ve = %.0f m/s (querosene e oxigenio liquido, Isp = 300 s)' % ve)
    print('   massa inicial %.0f kg, final %.0f kg, razao %.1f'
          % (m0, mf, m0 / mf))
    print('   Tsiolkovsky  ve ln(m0/mf) = %.6f m/s' % dv_t)
    print('   integracao numerica       = %.6f m/s' % dv_n)
    print('   diferenca                 = %.2e m/s' % abs(dv_t - dv_n))
    print('   tempo de queima           = %.1f s' % tq)
    print()
    print('   razao de massas   delta-v (m/s)   quantos ve')
    for r in (1.5, 2.0, np.e, 5.0, 10.0, 20.0):
        print('   %12.3f      %10.1f      %7.3f'
              % (r, ve * np.log(r), np.log(r)))
    print()
    print('   O logaritmo e o vilao de toda a engenharia espacial. Para')
    print('   dobrar o delta-v e preciso ELEVAR AO QUADRADO a razao de')
    print('   massas: de 10 para 100. Nao ha engenharia que resolva isso,')
    print('   so quimica melhor, que aumenta ve, ou estagiamento.')
    print()

    print('=' * 72)
    print('3. O QUE A GRAVIDADE COBRA')
    print('=' * 72)
    dv0, tq = integra_foguete(ve, m0, mf, taxa, g=0.0)
    print('   taxa (kg/s)   tempo (s)   delta-v   perda   g*tq   empuxo/peso')
    for taxa_i in (100.0, 200.0, 400.0, 800.0, 1600.0):
        dvg, t_i = integra_foguete(ve, m0, mf, taxa_i, g=G0)
        tw = ve * taxa_i / (m0 * G0)
        print('   %10.0f   %9.2f   %7.1f   %5.1f   %5.1f   %8.2f%s'
              % (taxa_i, t_i, dvg, dv0 - dvg, G0 * t_i, tw,
                 '  (nao decola)' if tw < 1 else ''))
    print()
    print('   A ultima coluna e o aviso: com empuxo menor que o peso o')
    print('   foguete nao sai do chao, e a primeira linha da tabela e um')
    print('   numero sem foguete por tras. A equacao continua valendo, mas')
    print('   descreve um veiculo que fica na plataforma gastando propelente.')
    print()
    print('   A perda e exatamente g vezes o tempo de queima, e por isso')
    print('   queimar depressa e vantajoso: o mesmo propelente rende mais.')
    print('   O limite nao e fisico, e estrutural: a aceleracao no fim da')
    print('   queima com 1600 kg/s passaria de %.0f g.'
          % (ve * 1600.0 / mf / G0))
    print()

    print('=' * 72)
    print('4. POR QUE OS FOGUETES TEM ESTAGIOS')
    print('=' * 72)
    m_total, eps = 50000.0, 0.10
    print('   Massa total %.0f kg, fracao estrutural %.0f %%, ve = %.0f m/s.'
          % (m_total, 100 * eps, ve))
    print()
    print('   carga util   1 estagio   2 estagios   3 estagios   ganho de 1 p/ 2')
    pior_dif = 0.0
    for carga in (5000.0, 2000.0, 1000.0, 500.0, 200.0):
        d1 = um_estagio(ve, m_total, carga, eps)
        melhor = -1.0
        for f in np.linspace(0.4, 0.97, 2000):
            d2, _, _ = dois_estagios(ve, m_total, carga, eps, f)
            melhor = max(melhor, d2)
        d2f = n_estagios_identicos(ve, m_total, carga, eps, 2)
        d3f = n_estagios_identicos(ve, m_total, carga, eps, 3)
        pior_dif = max(pior_dif, abs(melhor - d2f))
        print('   %8.0f kg  %9.0f   %10.0f   %10.0f   %+9.1f %%'
              % (carga, d1, melhor, d3f, 100 * (melhor / d1 - 1)))
    print()
    print('   A coluna de dois estagios saiu de uma BUSCA pela melhor divisao')
    print('   de massa entre eles, e a forma fechada dos estagios identicos')
    print('   da o mesmo numero: a maior diferenca nas cinco linhas e de')
    print('   %.3f m/s. Os dois caminhos sao independentes, e concordam.' % pior_dif)
    print()
    print('   O ganho cresce quando a carga util encolhe, e a razao e')
    print('   simples: o que o estagiamento faz e parar de carregar tanque')
    print('   vazio. Quanto maior a parte da massa final que e tanque vazio,')
    print('   mais ha a ganhar em jogar fora.')
    print()
    teto = ve * np.log(1 / eps)
    print('   Repare no teto de um estagio so: mesmo com carga util ZERO,')
    print('   ele nao passa de ve ln(1/eps) = %.0f m/s, porque a estrutura' % teto)
    print('   sempre fica. Para a orbita baixa sao precisos cerca de 9400')
    print('   m/s contando as perdas, e e por isso que nenhum foguete de um')
    print('   estagio so jamais colocou carga em orbita.')
    print()

    print('=' * 72)
    print('5. ONDE A CONTA INGENUA DA ERRADO')
    print('=' * 72)
    xs, forca_total, previsto = corrente_na_mesa()
    print('   Corrente de 1 kg/m caindo sobre a mesa, solta do repouso.')
    print('   Quando um comprimento x ja caiu, a mesa sustenta:')
    print('     o peso do que esta parado:        mu g x')
    print('     mais o momento do que chega:      mu v^2 = 2 mu g x')
    print('   O programa NAO usa essa formula: ele aplica F = dp/dt a')
    print('   corrente inteira e isola a normal, o que e um caminho')
    print('   independente. As duas colunas abaixo tem de coincidir.')
    print()
    print('   comprimento caido   N por dp/dt   3 mu g x   diferenca')
    for alvo in (0.25, 0.5, 0.75, 0.98):
        i = int(alvo * (len(xs) - 1))
        print('   %13.3f m   %11.4f N  %9.4f N   %.1e'
              % (xs[i], forca_total[i], previsto[i],
                 abs(forca_total[i] - previsto[i])))
    print()
    print('   A mesa sente TRES VEZES o peso do que ja caiu. Quem escrever')
    print('   F = m a com m variavel, sem perguntar com que velocidade a')
    print('   massa chega, perde os outros dois tercos. A pergunta certa e')
    print('   sempre F = dp/dt, com o cuidado de dizer de qual sistema.')

    print()
    print('=' * 72)
    print('6. A GRAVIDADE QUE DIMINUI COM A ALTURA')
    print('=' * 72)
    ve6, m06, mf6 = 3000.0, 1.0e5, 2.0e4
    dv_ideal = tsiolkovsky(ve6, m06, mf6)
    print('   Subida vertical. ve = %.0f m/s, m0 = %.0f t, mf = %.0f t,'
          % (ve6, m06 / 1e3, mf6 / 1e3))
    print('   razao de massas %.1f, delta-v ideal %.1f m/s.'
          % (m06 / mf6, dv_ideal))
    print()
    print('   g na superficie, por GM/R^2:   %.4f m/s^2' % G_SUP)
    print('   gravidade padrao convencionada: %.5f m/s^2' % G0)
    print('   A diferenca de 0,14 por cento nao e arredondamento: a padrao')
    print('   ja desconta a rotacao da Terra e vale perto da latitude 45,')
    print('   enquanto GM/R^2 e o valor newtoniano puro. Misturar as duas')
    print('   fazia a conferencia por energia discordar na terceira casa.')
    print()
    print('   CONFERENCIA 1. Com g fixo, a perda tem de dar g vezes o tempo')
    print('   de queima, que e o resultado da secao 3:')
    print()
    print('      tq      perda medida      G_SUP * tq      diferenca')
    for tq in (30.0, 60.0, 120.0):
        r = integra_subida(ve6, m06, mf6, tq, variavel=False, coast=False)
        print('   %6.0f s   %10.4f m/s   %10.4f m/s   %9.2e'
              % (tq, r['perda'], G_SUP * tq, abs(r['perda'] - G_SUP * tq)))
    print()
    print('   Agora com g(h) = GM/(R+h)^2:')
    print()
    print('      tq   v na queima  altura   perda g(h)  perda g fixo  economia')
    for tq in (30.0, 60.0, 120.0, 180.0, 240.0):
        r = integra_subida(ve6, m06, mf6, tq)
        print('   %6.0f s  %8.1f m/s %7.1f km %9.1f m/s %9.1f m/s   %5.2f %%'
              % (tq, r['v'], r['h'] / 1e3, r['perda'], G_SUP * tq,
                 100 * (1 - r['perda'] / (G_SUP * tq))))
    print()
    print('   A perda e MENOR que g vezes o tempo de queima, porque o')
    print('   foguete passa boa parte dela onde a gravidade ja e mais fraca.')
    print('   A economia vai de 0,45 por cento numa queima de 30 s a 1,3 por')
    print('   cento numa de 180 s, e depois volta a cair, porque a queima')
    print('   lenta nao consegue mais subir. Repare que a economia NAO salva')
    print('   a queima lenta: a perda em si cresce de 293 para 2334 m/s no')
    print('   mesmo intervalo, e engole metade do delta-v ideal.')
    print()
    print('   CONFERENCIA 2. Nas queimas muito lentas o empuxo nao vence o')
    print('   peso e o foguete fica na plataforma, queimando propelente sem')
    print('   sair do lugar, ate a massa cair o bastante. Esse propelente e')
    print('   perda de outra especie, e vale o delta-v que ele teria dado.')
    print('   A soma das tres parcelas tem de reproduzir Tsiolkovsky:')
    print()
    print('      tq    decola em   v final   perda grav   plataforma'
          '     soma      ideal')
    for tq in (240.0, 300.0, 360.0, 480.0):
        r = integra_subida(ve6, m06, mf6, tq)
        soma = r['v'] + r['perda'] + r['plataforma']
        quando = (m06 - r['m_decolagem']) / r['taxa']
        print('   %6.0f s  %7.1f s  %8.1f  %10.1f  %10.1f  %9.2f  %9.2f'
              % (tq, quando, r['v'], r['perda'], r['plataforma'],
                 soma, dv_ideal))
    print()
    print('   As duas ultimas colunas coincidem em seis algarismos. Como a')
    print('   parcela da plataforma e calculada por ve ln(m0/m_decolagem), e')
    print('   nao por subtracao, o fechamento e uma verificacao de verdade.')
    print('   Na queima de 480 s o foguete passa 294 s preso ao chao e')
    print('   desperdica 2025 m/s, quase metade do delta-v ideal, antes de')
    print('   se mover um centimetro.')
    print()
    print('   O APOGEU, POR TRES CAMINHOS. Depois da queima o voo e livre, e')
    print('   a altura maxima sai da integracao, da conservacao de energia')
    print('   com U = -GM/r, ou da formula de colegio v^2/2g:')
    print()
    print('      tq     integrado     por energia      razao     com mgh   erro')
    for tq in (30.0, 60.0, 120.0, 240.0):
        r = integra_subida(ve6, m06, mf6, tq)
        ae = apogeu_por_energia(r['v'], r['h'])
        ai = apogeu_ingenuo(r['v'], r['h'])
        print('   %6.0f s  %9.2f km  %9.2f km  %.8f  %8.2f km  %+5.1f %%'
              % (tq, r['apogeu'] / 1e3, ae / 1e3, r['apogeu'] / ae,
                 ai / 1e3, 100 * (ai / ae - 1)))
    print()
    print('   CONFERENCIA 3. As duas primeiras colunas coincidem em oito')
    print('   casas, e sao caminhos independentes: uma integra a equacao de')
    print('   movimento, a outra so usa que a energia se conserva. A terceira')
    print('   erra de 7 a 17 por cento, sempre para menos, porque mgh supoe')
    print('   que a gravidade continua valendo %.2f la em cima. A 1200 km'
          % G_SUP)
    print('   ela ja caiu para %.2f m/s^2, isto e, %.0f por cento do valor da'
          % (g_altura(1.2e6), 100 * g_altura(1.2e6) / G_SUP))
    print('   superficie.')
    print()
    r_baixo = integra_subida(ve6, 1.0e5, 9.5e4, 3.0)
    ae = apogeu_por_energia(r_baixo['v'], r_baixo['h'])
    ai = apogeu_ingenuo(r_baixo['v'], r_baixo['h'])
    print('   E a formula de colegio nao esta errada, esta fora de faixa. Um')
    print('   foguete com 5 por cento da massa em propelente e 3 s de queima')
    print('   sobe %.2f km por energia e %.2f km com mgh, uma diferenca de'
          % (ae / 1e3, ai / 1e3))
    print('   %.3f por cento. Abaixo de alguns quilometros, g e constante.'
          % (100 * abs(ai / ae - 1)))


if __name__ == '__main__':
    main()
