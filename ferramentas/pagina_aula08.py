# -*- coding: utf-8 -*-
"""Módulo 8: oscilações forçadas, ressonância e a resposta a uma força qualquer.

Dois pontos em que o módulo discorda do senso comum: "a frequência de
ressonância" não é uma só, e a ponte de Tacoma não caiu por ressonância.
E um ponto que fecha a unidade: a função de Green resolve o caso geral.
"""
from molde import escreve, secoes_html
import exercicios
from lista_aula08 import LISTA

S1 = r'''
<p>Os módulos 6 e 7 descreveram osciladores entregues a si mesmos. Agora
chega alguém de fora e empurra, periodicamente:</p>

\[ \ddot{x} + 2\gamma\dot{x} + \omega_0^2 x = \frac{F_0}{m}\cos\omega t. \]

<p>A equação continua linear, e é dessa única propriedade que decorre tudo o
que vem a seguir. A solução geral de uma equação linear não homogênea é a
solução geral da homogênea mais <em>uma</em> solução particular:</p>

\[ x(t) = \underbrace{x_{\text{tr}}(t)}_{\text{morre como }e^{-\gamma t}}
        + \underbrace{x_{\text{est}}(t)}_{\text{dura}}. \]

<p>O primeiro termo é o transiente, e é exatamente o problema do módulo 7,
intacto: ele oscila em \(\omega_1\) e não sabe nada sobre a força. O segundo
é o estacionário, e oscila na frequência da <strong>força</strong>, não na do
sistema. Essa é a diferença que organiza o módulo inteiro.</p>

<p>Procurando o estacionário na forma \(x = A\cos(\omega t - \varphi)\),
substituindo e separando os termos em seno e cosseno, sai</p>

\[ A(\omega) = \frac{F_0/m}
   {\sqrt{\left(\omega_0^2-\omega^2\right)^2 + \left(2\gamma\omega\right)^2}},
   \qquad
   \tg\varphi = \frac{2\gamma\omega}{\omega_0^2-\omega^2}. \]

<p>O programa mede \(A\) e \(\varphi\) na integração numérica, depois de
esperar dez constantes de tempo para o transiente morrer, e ajusta a senoide
por mínimos quadrados. As fórmulas e a medida concordam em \(10^{-6}\).</p>

<h3>A fase, que diz mais que a amplitude</h3>

<p>Vale olhar a fase antes da amplitude, porque ela é mais informativa e
menos lembrada:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>regime</th><th>\(\varphi\)</th><th>o que o corpo faz</th></tr></thead>
<tbody>
<tr><td>\(\omega \ll \omega_0\)</td><td>\(\to 0\)</td>
<td>acompanha a força, em fase; a mola manda</td></tr>
<tr><td>\(\omega = \omega_0\)</td><td>exatamente \(\pi/2\)</td>
<td>atrasado um quarto de ciclo; a força empurra sempre a favor da
velocidade</td></tr>
<tr><td>\(\omega \gg \omega_0\)</td><td>\(\to \pi\)</td>
<td>em oposição à força; a inércia manda</td></tr>
</tbody>
</table>
</div>

<p>A passagem de 0 a \(\pi\) acontece numa faixa de largura \(2\gamma\) em
torno de \(\omega_0\), e é tanto mais brusca quanto menor o amortecimento. O
valor \(\pi/2\) em \(\omega_0\) não é aproximação: é exato, em qualquer
\(\gamma\), e é ele que explica por que a potência absorvida tem máximo ali,
como a seção seguinte mostra.</p>
'''

S2 = r'''
<p>Pergunte a alguém qual é a frequência de ressonância de um oscilador
amortecido e a resposta virá: \(\omega_0\). A resposta está certa pela metade,
e saber qual metade é o conteúdo desta seção.</p>

<p>A amplitude do <em>deslocamento</em> tem máximo onde o denominador de
\(A(\omega)\) é mínimo. Derivando:</p>

\[ \omega_A = \sqrt{\omega_0^2 - 2\gamma^2}, \]

<p>que é <strong>menor</strong> que \(\omega_0\), e que deixa de existir
quando \(\gamma &gt; \omega_0/\sqrt{2}\): a partir daí a curva só decresce, e
não há ressonância de amplitude nenhuma.</p>

<p>A amplitude da <em>velocidade</em> é \(\omega A(\omega)\), e o seu máximo
está exatamente em \(\omega_0\), em qualquer amortecimento. E a
<em>potência média absorvida</em>, que é o que de fato se transfere da força
para o oscilador,</p>

\[ \med{P} = \med{F\dot{x}} = \gamma\left[\omega A(\omega)\right]^2 m, \]

<p>tem máximo exatamente em \(\omega_0\) também. O programa faz a busca fina
dos três máximos:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>\(\gamma\)</th><th>pico de \(x\)</th>
<th>\(\sqrt{\omega_0^2-2\gamma^2}\)</th><th>pico de \(v\)</th>
<th>pico de \(P\)</th></tr></thead>
<tbody>
<tr><td>0,10</td><td>3,99750</td><td>3,99750</td><td>3,99999</td><td>3,99999</td></tr>
<tr><td>0,40</td><td>3,95980</td><td>3,95980</td><td>3,99999</td><td>3,99999</td></tr>
<tr><td>1,00</td><td>3,74166</td><td>3,74166</td><td>3,99999</td><td>3,99999</td></tr>
<tr><td>2,00</td><td>2,82842</td><td>2,82843</td><td>3,99999</td><td>3,99999</td></tr>
<tr><td>2,80</td><td>0,56569</td><td>0,56569</td><td>3,99999</td><td>3,99999</td></tr>
<tr><td>3,00</td><td>0,10000</td><td>não há pico</td><td>3,99999</td><td>3,99999</td></tr>
</tbody>
</table>
</div>

<p>Os 3,99999 das duas últimas colunas são o ponto da grade mais próximo de
4: a busca varre 400 mil frequências entre 0,1 e 8, de modo que o espaçamento
é \(2\times10^{-5}\). E o 0,10000 da última linha é a borda da busca, porque
ali a curva já não tem máximo nenhum: ela só decresce.</p>

<p>São três ressonâncias, em duas frequências diferentes, e a pergunta "qual é
a frequência de ressonância" só tem resposta depois de dizer ressonância
<em>de quê</em>. A distinção não é escolástica: quem projeta para a estrutura
não quebrar olha o pico do deslocamento, e quem projeta para transferir
energia, como uma antena, um forno de micro-ondas ou um sintonizador, olha o
da potência.</p>

<div data-widget="forcado"></div>

<h3>A largura da curva, e o Q de laboratório</h3>

<p>A curva de potência é uma lorentziana, e a sua largura a meia altura tem
forma fechada: os pontos de meia potência estão em</p>

\[ \omega_{\pm} = \sqrt{\omega_0^2+\gamma^2} \pm \gamma
   \qquad\Longrightarrow\qquad
   \Delta\omega = \omega_+ - \omega_- = 2\gamma. \]

<p>A largura vale \(2\gamma\) <strong>exatamente</strong>, em qualquer
amortecimento, e não apenas no limite de \(Q\) alto. O programa confirma em
cinco casas. Daí a definição operacional</p>

\[ Q = \frac{\omega_0}{\Delta\omega}, \]

<p>que é como \(Q\) se mede num laboratório de verdade: varre-se a frequência
e divide-se. Não é preciso desligar nada, nem cronometrar decaimento, nem
conhecer \(m\), \(k\) ou \(b\). Compare com o módulo 7, onde \(Q\) saiu de
picos sucessivos: são medidas independentes da mesma grandeza, e a
concordância entre elas é um teste do modelo.</p>
'''

S3 = r'''
<p>O estacionário é o que sobra; o transiente é o que acontece primeiro. E há
uma armadilha de projeto escondida aí.</p>

<p>Quando \(\omega\) está perto de \(\omega_0\), o transiente e o estacionário
têm frequências parecidas, e a soma de duas senoides de frequências parecidas
produz <strong>batimento</strong>, com período \(2\pi/|\omega_0-\omega|\).
Durante os primeiros batimentos, a amplitude pode ultrapassar bastante a do
regime permanente:</p>

<div class="saida">
omega = 3,60&nbsp;&nbsp;&nbsp;estacionaria <b>0,32666</b>&nbsp;&nbsp;&nbsp;pico do transiente <b>0,54923</b>&nbsp;&nbsp;(+68 %)<br>
omega = 3,95&nbsp;&nbsp;&nbsp;estacionaria <b>1,78449</b>&nbsp;&nbsp;&nbsp;pico do transiente <b>1,90651</b>&nbsp;&nbsp;(+7 %)
</div>

<p>E o excesso cresce quando o amortecimento diminui. Medindo em
\(\omega = 3{,}95\) com \(\gamma\) cada vez menor, a razão entre o pico e o
estacionário vai a 1,07, depois 1,55, depois 1,88: no limite
\(\gamma \to 0\) ela tende a <strong>2</strong>.</p>

<div class="destaque">
<p><strong>A armadilha.</strong> Quem dimensiona uma estrutura pela resposta
de regime permanente pode errar por um fator 2. O primeiro minuto de uma
máquina ligando é mais perigoso que a hora seguinte inteira, e é por isso que
turbinas e motores grandes são acelerados <em>depressa</em> através das
frequências críticas, em vez de devagar: o que machuca é passar tempo
perto.</p>
</div>

<p>Já o tempo até estabilizar é teimoso: deu \(3{,}6/\gamma\) e
\(3{,}7/\gamma\) nos dois casos, com frequências de força bem diferentes. A
razão é que quem precisa morrer é o transiente, que é o problema do módulo 7 e
não sabe nada sobre a força. Cair a 2 % de uma exponencial leva
\(\ln(1/0{,}02) = 3{,}9\) constantes de tempo, e é disso que se trata.</p>

<div class="destaque">
<p><strong>A ponte de Tacoma não caiu por ressonância.</strong> A fotografia da
ponte se contorcendo, em 1940, ilustra o capítulo de ressonância de quase todo
livro de física básica, e a atribuição é incorreta. Não havia força externa
periódica: o vento soprava de modo aproximadamente constante. O que houve foi
<em>flutter</em> aeroelástico, uma instabilidade autoexcitada em que o próprio
movimento da estrutura modula a força do ar, criando amortecimento
<strong>negativo</strong>. A diferença é de fundo: na ressonância a amplitude
satura em \(F_0/2m\gamma\omega_0\), e no flutter ela cresce exponencialmente
até a ruína, sem precisar de frequência externa nenhuma. A correção está em
K. Y. Billah e R. H. Scanlan,
<a href="https://doi.org/10.1119/1.16590"><em>Resonance, Tacoma Narrows bridge
failure, and undergraduate physics textbooks</em></a>, Am. J. Phys.
<strong>59</strong>, 118 (1991).</p>
</div>
'''

S4 = r'''
<p>Até aqui a força foi uma senoide, o que é cômodo e pouco realista. Um
terremoto não é senoidal, nem uma martelada, nem uma rajada de vento, nem um
buraco na estrada. A pergunta geral é: dada uma força qualquer \(f(t)\), qual
é \(x(t)\)?</p>

<p>A linearidade responde de graça, e a resposta é uma das ideias mais
reaproveitadas da física. Comece resolvendo um caso só: a resposta a um
<strong>impulso</strong> aplicado em \(t = 0\), que é o mesmo que soltar o
oscilador em repouso com velocidade unitária. Essa é a
<strong>função de Green</strong>:</p>

\[ G(t) = \begin{cases}
   \dfrac{e^{-\gamma t}\sen\omega_1 t}{\omega_1}, & t \ge 0,\\[6pt]
   0, & t &lt; 0. \end{cases} \]

<p>Agora olhe uma força qualquer como uma fila de impulsos, um em cada
instante \(s\), de tamanho \(f(s)\,ds\). Cada um produz a sua resposta,
deslocada no tempo, e como a equação é linear as respostas simplesmente se
somam:</p>

\[ x(t) = \int_{-\infty}^{t} G(t-s)\,f(s)\,ds. \]

<p>Isso resolve o problema <em>inteiro</em>, para sempre, sem nunca mais
resolver equação diferencial nenhuma. O programa testa com três forças que não
têm nada de senoidal, comparando a convolução com a integração direta da
equação:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>força</th><th>diferença com \(\Delta t\)</th>
<th>com \(\Delta t/2\)</th><th>razão</th><th>ordem</th></tr></thead>
<tbody>
<tr><td>pulso retangular</td><td>\(2{,}98\times10^{-5}\)</td>
<td>\(1{,}49\times10^{-5}\)</td><td>2,00</td><td>primeira</td></tr>
<tr><td>dente de serra</td><td>\(6{,}04\times10^{-5}\)</td>
<td>\(3{,}01\times10^{-5}\)</td><td>2,00</td><td>primeira</td></tr>
<tr><td>três marteladas</td><td>\(3{,}33\times10^{-9}\)</td>
<td>\(8{,}33\times10^{-10}\)</td><td>4,00</td><td>segunda</td></tr>
</tbody>
</table>
</div>

<p>A diferença que sobra não é discordância entre os dois métodos: é o erro de
quadratura da soma usada na convolução, e ele some com o passo. A razão entre
as colunas diz de que ordem: 2 quando a força tem salto, 4 quando ela é suave.
Reconhecer a ordem do próprio erro é o que separa uma verificação de uma
coincidência.</p>

<h3>Causalidade, memória e o resto da física</h3>

<p>Repare no limite superior da integral. A resposta em \(t\) depende apenas
da força <em>antes</em> de \(t\), porque \(G\) é nula para argumento negativo.
É a causalidade escrita como propriedade de uma função, e é por isso que ela
é imposta à mão na definição.</p>

<p>E repare no \(e^{-\gamma t}\): o peso de uma força antiga decai, de modo que
o oscilador tem <strong>memória</strong> de cerca de \(1/\gamma\). O que
aconteceu muito antes disso já não importa, e é essa perda de memória que
torna o regime permanente possível.</p>

<p>A ideia não fica na mecânica. A função de Green é a mesma ferramenta que
resolve circuitos elétricos, propagação de ondas, difusão de calor, campos
eletromagnéticos de fontes arbitrárias e, com outro nome, o propagador da
teoria quântica de campos. Em todos esses casos a receita é a mesma: resolva
para o impulso e some. O oscilador amortecido é o exemplo mais barato que
existe dela, e por isso vale a pena entendê-lo aqui, onde a conta cabe numa
linha.</p>
'''

S5 = r'''
<div class="cartoes">
  <a class="cartao" href="codigo/forcado.py">
    <span class="numero">Programa</span>
    <h3>forcado.py</h3>
    <p>Mede amplitude e fase do estacionário, localiza os três picos de
    ressonância, mede a largura da curva de potência, acompanha o batimento
    do transiente e resolve a resposta a três forças quaisquer por
    convolução.</p>
  </a>
</div>

<p><strong>O que ele imprime, e o que conferir.</strong></p>

<ul>
<li>Amplitude e fase medidas na integração batem com as fórmulas em
\(10^{-6}\), em seis frequências.</li>
<li>O pico do deslocamento cai em \(\sqrt{\omega_0^2-2\gamma^2}\) nos cinco
amortecimentos em que ele existe, e some no sexto.</li>
<li>Os picos da velocidade e da potência ficam em \(\omega_0\) com cinco casas,
em qualquer \(\gamma\).</li>
<li>A largura a meia altura da curva de potência dá \(2\gamma\) em cinco
casas.</li>
<li>A convolução reproduz a integração direta, com erro de primeira ordem para
forças com salto e de segunda para forças suaves.</li>
</ul>

<div class="bloco ex">
<p><strong>Para mexer.</strong> Troque a força senoidal por uma onda quadrada
de mesma frequência e compare a resposta com a soma das respostas aos
harmônicos ímpares, que é a série de Fourier da onda quadrada: o resultado
deve coincidir, e é a demonstração de que resolver para senoides também
resolve o caso geral, por outro caminho. Depois diminua \(\gamma\) e verifique
que o fator de ultrapassagem do transiente tende a 2.</p>
</div>
'''

SECOES = [
    ('A força externa, e as duas partes da resposta', S1),
    ('Três ressonâncias que não coincidem', S2),
    ('O transiente, o batimento e a armadilha de projeto', S3),
    ('A resposta a uma força qualquer', S4),
    ('No Spyder', S5),
]

SECOES.append(('Exercícios propostos', exercicios.bloco(LISTA)))


def main():
    titulos = [t for t, _ in SECOES]
    escreve('aula08.html', secoes_html(SECOES), secoes=titulos,
            subtitulo='Empurrar o oscilador periodicamente produz três '
                      'ressonâncias em frequências diferentes, e um transiente '
                      'que pode ultrapassar o regime permanente ao dobro. E '
                      'resolver o caso do impulso resolve, de uma vez, o caso '
                      'de qualquer força.')


if __name__ == '__main__':
    main()
