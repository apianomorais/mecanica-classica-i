# -*- coding: utf-8 -*-
"""Módulo 7: oscilações amortecidas.

O módulo tem um ponto polêmico de propósito: a afirmação, repetida em quase
todo livro, de que o amortecimento crítico é o mais rápido para voltar ao
repouso. Medindo, ela é falsa, e o enunciado correto tem uma letra miúda.
"""
from molde import escreve, secoes_html
import exercicios
from lista_aula07 import LISTA

S1 = r'''
<p>O oscilador do módulo 6 nunca para, e isso não existe. Qualquer oscilador
real perde energia: para o ar, para o atrito interno do material, para o
suporte, para o som que emite. O modelo mais simples dessa perda é a força de
arrasto linear do módulo 3, \(-b\dot{x}\), e com ela a equação fica</p>

\[ m\ddot{x} = -kx - b\dot{x} \qquad\Longleftrightarrow\qquad
   \ddot{x} + 2\gamma\dot{x} + \omega_0^2 x = 0, \]

<p>com \(\gamma = b/2m\) e \(\omega_0 = \sqrt{k/m}\). O fator 2 na definição
de \(\gamma\) é convenção, e é escolhido justamente para deixar as fórmulas
que virão sem fatores 2 espalhados.</p>

<p>Procurando soluções da forma \(x = e^{rt}\), que é o chute padrão para
equações lineares de coeficientes constantes, sai a equação característica</p>

\[ r^2 + 2\gamma r + \omega_0^2 = 0
   \qquad\Longrightarrow\qquad
   r = -\gamma \pm \sqrt{\gamma^2 - \omega_0^2}. \]

<p>Tudo o que acontece neste módulo está no sinal do que está dentro da raiz.
São três casos, e eles não se parecem nem um pouco:</p>

<div class="cartoes">
  <div class="cartao">
    <span class="numero">γ &lt; ω₀</span>
    <h3>Subamortecido</h3>
    <p>Raízes complexas. \(x = Ce^{-\gamma t}\cos(\omega_1 t - \varphi)\), com
    \(\omega_1 = \sqrt{\omega_0^2-\gamma^2}\). Oscila, com amplitude
    minguando.</p>
  </div>
  <div class="cartao">
    <span class="numero">γ = ω₀</span>
    <h3>Crítico</h3>
    <p>Raiz dupla. \(x = (A + Bt)e^{-\gamma t}\). O \(t\) solto aparece
    porque uma raiz dupla só fornece uma solução, e faltava a segunda.</p>
  </div>
  <div class="cartao">
    <span class="numero">γ &gt; ω₀</span>
    <h3>Superamortecido</h3>
    <p>Duas raízes reais negativas. \(x = C_1e^{r_1t} + C_2e^{r_2t}\). Não
    oscila: volta devagar, arrastado.</p>
  </div>
</div>

<p>O programa confere as três fórmulas contra a integração numérica da mesma
equação, e a maior diferença é de \(10^{-13}\) m. Vale reparar no que isso
significa: o integrador não sabe em que regime está, nem consulta o sinal de
\(\gamma^2-\omega_0^2\). Ele resolve a mesma equação nos três casos e encontra
a mesma curva que a fórmula correspondente. As três formas são uma só.</p>

<div class="destaque">
<p><strong>Um aviso numérico.</strong> O método de Verlet, que serviu tão bem
nos módulos 4 e 6, <em>não serve aqui</em>. Ele supõe que a aceleração dependa
apenas da posição, e a força de arrasto depende da velocidade. Usá-lo assim
mesmo produz um amortecimento errado, sem erro visível, sem aviso, sem
divergência: apenas um número plausível. O programa usa Runge-Kutta de quarta
ordem, que não faz essa suposição.</p>
</div>
'''

S2 = r'''
<p>No regime subamortecido, a frequência não é \(\omega_0\):</p>

\[ \omega_1 = \omega_0\sqrt{1 - \left(\frac{\gamma}{\omega_0}\right)^2}. \]

<p>O amortecimento <strong>atrasa</strong> a oscilação, e o programa mede isso
nos cruzamentos de zero:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>\(\gamma\)</th><th>\(\omega_1\) medido</th>
<th>\(\sqrt{\omega_0^2-\gamma^2}\)</th><th>diferença</th>
<th>\(T/T_0\)</th></tr></thead>
<tbody>
<tr><td>0,20</td><td>3,99499687</td><td>3,99499687</td>
<td>\(4\times10^{-11}\)</td><td>1,0013</td></tr>
<tr><td>0,80</td><td>3,91918359</td><td>3,91918359</td>
<td>\(3\times10^{-11}\)</td><td>1,0206</td></tr>
<tr><td>2,00</td><td>3,46410161</td><td>3,46410162</td>
<td>\(2\times10^{-10}\)</td><td>1,1547</td></tr>
<tr><td>3,80</td><td>1,24899960</td><td>1,24899960</td>
<td>\(1\times10^{-10}\)</td><td>3,2026</td></tr>
</tbody>
</table>
</div>

<p>Com \(\gamma = 3{,}8\), que é 95 % de \(\omega_0\), o período fica 3,2
vezes maior. É um efeito grande, e tem consequência prática: um pêndulo dentro
de óleo não serve para medir tempo, e um relógio cujo mecanismo esteja sujo
atrasa, não adianta.</p>

<div data-widget="amortecido"></div>

<p>Repare na primeira vista que, para \(\gamma\) pequeno, a curva quase não se
distingue da senoide do módulo 6 nos primeiros ciclos. O amortecimento fraco
é invisível no curto prazo e decisivo no longo: é exatamente o caso do
oscilador de alto \(Q\), de que trata a seção seguinte.</p>
'''

S3 = r'''
<p>Entre um pico e o seguinte, a amplitude é dividida sempre pelo mesmo fator
\(e^{\gamma T_1}\). O logaritmo dessa razão chama-se
<strong>decremento logarítmico</strong>:</p>

\[ \delta = \ln\frac{x_n}{x_{n+1}} = \gamma T_1 = \frac{2\pi\gamma}{\omega_1}. \]

<p>Ele é a maneira prática de medir amortecimento: bastam uma régua e dois
picos de um registro, sem precisar conhecer \(m\), \(k\) ou \(b\).</p>

<p>Daí se define o <strong>fator de qualidade</strong> \(Q\), que mede quantos
ciclos o oscilador sustenta antes de perder a energia. E aqui o módulo precisa
dizer uma coisa que os livros costumam esconder: existem três definições de
\(Q\), elas são tratadas como se fossem a mesma, e <em>não são</em>.</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>definição</th><th>fórmula</th><th>vale exatamente</th></tr></thead>
<tbody>
<tr><td>pela razão massa-amortecimento</td><td>\(\omega_0/2\gamma\)</td>
<td>por definição</td></tr>
<tr><td>pelo decremento logarítmico</td><td>\(\pi/\delta\)</td>
<td>\(\omega_1/2\gamma\)</td></tr>
<tr><td>pela energia perdida por ciclo</td>
<td>\(2\pi E/\left|\Delta E\right|\)</td>
<td>\(2\pi/\left(1-e^{-2\pi/Q}\right)\)</td></tr>
</tbody>
</table>
</div>

<p>O programa mede as três e verifica as diferenças em forma fechada. A
primeira discrepância é exatamente o fator \(\omega_1/\omega_0\):</p>

<div class="saida">
gama&nbsp;&nbsp;&nbsp;Q_formula&nbsp;&nbsp;&nbsp;Q_picos&nbsp;&nbsp;&nbsp;razao medida&nbsp;&nbsp;&nbsp;sqrt(1-(g/w0)^2)<br>
&nbsp;0,40&nbsp;&nbsp;&nbsp;&nbsp;5,00000&nbsp;&nbsp;&nbsp;4,97494&nbsp;&nbsp;&nbsp;<b>0,99498744</b>&nbsp;&nbsp;&nbsp;<b>0,99498744</b><br>
&nbsp;2,00&nbsp;&nbsp;&nbsp;&nbsp;1,00000&nbsp;&nbsp;&nbsp;0,86603&nbsp;&nbsp;&nbsp;<b>0,86602540</b>&nbsp;&nbsp;&nbsp;<b>0,86602540</b><br>
&nbsp;3,00&nbsp;&nbsp;&nbsp;&nbsp;0,66667&nbsp;&nbsp;&nbsp;0,44096&nbsp;&nbsp;&nbsp;<b>0,66143783</b>&nbsp;&nbsp;&nbsp;<b>0,66143783</b>
</div>

<p>A segunda é mais interessante, porque sobrevive mesmo com amortecimento
fraco. A energia decai como \(e^{-2\gamma t}\), de modo que a fração perdida
num ciclo vale \(1 - e^{-2\pi/Q}\), e não \(2\pi/Q\): a segunda expressão é a
primeira linearizada. O erro relativo é de cerca de \(\pi/Q\), o que significa
<strong>3 % mesmo num oscilador com \(Q = 100\)</strong>, que já é pouco
amortecido. O programa confirma a previsão fechada em todas as casas.</p>

<p>Nada disso é erro numérico nem preciosismo. São três grandezas diferentes
com o mesmo nome, e qual delas um experimento mede depende de como ele é
feito. Quem compara um \(Q\) medido por decaimento com um \(Q\) tabelado por
largura de banda precisa saber disso.</p>

<div class="destaque">
<p><strong>A regra de bolso que funciona.</strong> A amplitude cai a \(1/e\) em
\(\tau = 1/\gamma = Q/(\pi f_0)\), isto é, em cerca de \(Q/\pi\) ciclos. Uma
corda de violão com \(Q = 1000\) em 330 Hz leva 0,96 s para cair a \(1/e\), e
o som fica audível por alguns segundos depois. Um cristal de quartzo de
relógio, com \(Q \simeq 10^5\) em 32 768 Hz, leva quase um segundo também, só
que em 32 mil ciclos em vez de 320.</p>
</div>
'''

S4 = r'''
<p>Chegamos ao ponto em que este módulo discorda da bibliografia. Quase todo
livro de mecânica afirma, sem qualificação, que o amortecimento crítico é o
que leva o sistema de volta ao repouso mais depressa. É o tipo de frase que se
repete por décadas sem que ninguém meça.</p>

<p>Medindo, ela é falsa. O programa desloca o oscilador de 1 m, solta, e
cronometra quanto tempo ele leva para entrar e permanecer dentro de 2 % do
repouso:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>\(\gamma/\omega_0\)</th><th>regime</th>
<th>tempo de acomodação (s)</th></tr></thead>
<tbody>
<tr><td>0,30</td><td>subamortecido</td><td>2,8075</td></tr>
<tr><td>0,60</td><td>subamortecido</td><td>1,4857</td></tr>
<tr><td><strong>0,78</strong></td><td>subamortecido</td>
<td><strong>0,9011</strong></td></tr>
<tr><td>0,90</td><td>subamortecido</td><td>1,1748</td></tr>
<tr><td>1,00</td><td>crítico</td><td>1,4584</td></tr>
<tr><td>1,10</td><td>superamortecido</td><td>1,7304</td></tr>
<tr><td>1,50</td><td>superamortecido</td><td>2,6636</td></tr>
<tr><td>3,00</td><td>superamortecido</td><td>5,7437</td></tr>
</tbody>
</table>
</div>

<p>O mínimo está em 0,78, e o crítico demora <strong>62 % a mais</strong>. A
diferença não é sutil nem é artefato de medida.</p>

<p>O enunciado correto tem uma letra miúda que costuma ser omitida: o crítico
é o mais rápido <em>entre os que não ultrapassam o repouso</em>. Se um pequeno
repique couber dentro da tolerância exigida, vale a pena deixá-lo acontecer,
porque o sistema chega lá antes.</p>

<h3>A regra de projeto, em forma fechada</h3>

<p>Isso dá um critério exato, e não uma recomendação vaga. Escrevendo
\(z = \gamma/\omega_0\), o primeiro repique de um sistema subamortecido solto
do repouso vale</p>

\[ \text{repique} = \exp\!\left(-\frac{\pi z}{\sqrt{1-z^2}}\right), \]

<p>e o ótimo é onde esse repique tem exatamente o tamanho da tolerância.
Igualando e resolvendo para \(z\), com \(\Lambda = -\ln(\text{tol})/\pi\):</p>

\[ z_{\text{ótimo}} = \sqrt{\frac{\Lambda^2}{1+\Lambda^2}}. \]

<p>O programa compara essa previsão com a busca numérica:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>tolerância</th><th>ótimo medido</th><th>ótimo previsto</th>
<th>crítico demora</th></tr></thead>
<tbody>
<tr><td>5 %</td><td>0,70</td><td>0,690</td><td>+64 %</td></tr>
<tr><td>2 %</td><td>0,78</td><td>0,780</td><td>+62 %</td></tr>
<tr><td>1 %</td><td>0,83</td><td>0,826</td><td>+57 %</td></tr>
<tr><td>0,2 %</td><td>0,90</td><td>0,892</td><td>+46 %</td></tr>
<tr><td>0,01 %</td><td>0,95</td><td>0,946</td><td>+36 %</td></tr>
</tbody>
</table>
</div>

<p>A fórmula acerta o ótimo medido em todos os casos, e a tabela mostra o
caminho de volta: quanto mais apertada a tolerância, mais o ótimo se aproxima
do crítico. No limite de tolerância zero, o livro volta a ter razão, e é
exatamente esse limite que ele está descrevendo sem dizer.</p>

<p>É por isso que a suspensão de um automóvel é projetada em torno de
\(z \simeq 0{,}7\), e não em 1,0: ninguém exige que o carro volte ao repouso
com precisão infinita, exige que ele pare de balançar antes do próximo buraco.
Amortecedor gasto, com \(z\) baixo, faz o carro quicar; amortecedor duro
demais, com \(z\) alto, transmite cada buraco à carroceria, porque não tem
tempo de ceder.</p>
'''

S5 = r'''
<p>Não existe \(Q\) bom ou ruim: existe \(Q\) adequado ao que se quer. Metade
dos sistemas da lista abaixo foi projetada para perder energia o mais depressa
possível, e a outra metade para não perder:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>sistema</th><th>\(z\) ou \(Q\)</th><th>o que se quer</th></tr></thead>
<tbody>
<tr><td>suspensão de automóvel</td><td>\(z \simeq 0{,}7\)</td>
<td>voltar rápido sem quicar</td></tr>
<tr><td>porta com mola</td><td>\(z \simeq 0{,}7\)</td><td>fechar sem bater</td></tr>
<tr><td>galvanômetro analógico</td><td>\(z \simeq 0{,}7\)</td>
<td>ponteiro parar sem oscilar</td></tr>
<tr><td>corda de violão (mi)</td><td>\(Q \sim 10^3\)</td>
<td>o som tem de durar</td></tr>
<tr><td>diapasão</td><td>\(Q \sim 10^4\)</td><td>referência de frequência</td></tr>
<tr><td>cristal de quartzo</td><td>\(Q \sim 10^5\)</td><td>relógio</td></tr>
</tbody>
</table>
</div>

<p>O amortecimento linear \(-b\dot{x}\) é um modelo, e convém saber onde ele
falha. Ele descreve bem o arrasto viscoso de um fluido em regime laminar, que
é o caso do módulo 3, e descreve razoavelmente a perda interna de muitos
materiais. Não descreve o atrito seco, em que a força tem módulo constante e
só muda de sinal: ali a amplitude decai <em>linearmente</em>, e não
exponencialmente, e o movimento para em tempo finito, num ponto que em geral
não é o equilíbrio. Esse é o exercício 7.5, e ele tem uma assinatura
experimental inconfundível: picos em progressão aritmética em vez de
geométrica.</p>
'''

S6 = r'''
<div class="cartoes">
  <a class="cartao" href="codigo/amortecido.py">
    <span class="numero">Programa</span>
    <h3>amortecido.py</h3>
    <p>Confere as três soluções contra a integração, mede \(\omega_1\) nos
    cruzamentos, compara as três definições de \(Q\) com as previsões
    fechadas e localiza o amortecimento que minimiza o tempo de
    acomodação.</p>
  </a>
</div>

<p><strong>O que ele imprime, e o que conferir.</strong></p>

<ul>
<li>As três fórmulas e a integração numérica concordam em \(10^{-13}\) m nos
quatro casos.</li>
<li>\(\omega_1\) medido nos cruzamentos bate com \(\sqrt{\omega_0^2-\gamma^2}\)
em \(10^{-10}\).</li>
<li>A razão entre \(Q\) pelos picos e \(Q = \omega_0/2\gamma\) reproduz
\(\sqrt{1-(\gamma/\omega_0)^2}\) em oito casas.</li>
<li>A razão entre \(Q\) pela energia e \(Q\) pelos picos reproduz
\((2\pi/Q)/(1-e^{-2\pi/Q})\) em seis casas.</li>
<li>O ótimo medido do tempo de acomodação coincide com
\(z = \sqrt{\Lambda^2/(1+\Lambda^2)}\) nas cinco tolerâncias testadas.</li>
</ul>

<div class="bloco ex">
<p><strong>Para mexer.</strong> Troque o Runge-Kutta pelo Verlet do módulo 6,
tratando \(-2\gamma\dot{x}\) como se fosse força de posição, e meça o
amortecimento que sai: ele estará errado, e o programa não dará erro nenhum.
Depois acrescente atrito seco, \(-\mu mg\,\mathrm{sinal}(\dot{x})\), no lugar
do arrasto linear, e confira que os picos passam a cair em progressão
aritmética e que o corpo para fora do equilíbrio.</p>
</div>
'''

SECOES = [
    ('A equação, e os três regimes', S1),
    ('O amortecimento atrasa o relógio', S2),
    ('Decremento, Q, e três definições que discordam', S3),
    ('O amortecimento crítico não é o mais rápido', S4),
    ('Que amortecimento se quer, e onde o modelo falha', S5),
    ('No Spyder', S6),
]

SECOES.append(('Exercícios propostos', exercicios.bloco(LISTA)))


def main():
    titulos = [t for t, _ in SECOES]
    escreve('aula07.html', secoes_html(SECOES), secoes=titulos,
            subtitulo='Acrescentar arrasto à mola produz três regimes que não '
                      'se parecem e são a mesma solução. E permite medir uma '
                      'afirmação que quase todo livro faz sem qualificação: a '
                      'de que o amortecimento crítico é o mais rápido para '
                      'voltar ao repouso.')


if __name__ == '__main__':
    main()
