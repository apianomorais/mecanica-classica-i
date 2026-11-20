# -*- coding: utf-8 -*-
"""Módulo 12: forças centrais e as órbitas de Kepler.

Este é o lugar da dedução newtoniana completa. Mecânica Clássica II revisita
o mesmo problema em poucas linhas, como demonstração da economia do
formalismo lagrangiano, e aponta para cá.
"""
from molde import escreve, secoes_html
import exercicios
from lista_aula12 import LISTA

S1 = r'''
<p>Uma força é <strong>central</strong> quando aponta sempre para um ponto
fixo e depende só da distância a ele:</p>

\[ \vet{F} = f(r)\,\vers{r}. \]

<p>A gravitação é o caso que interessa aqui, mas quase nada do que vem a
seguir usa a forma de \(f\). O que faz o trabalho é a <strong>simetria</strong>,
e vale separar o que decorre dela do que decorre do inverso do quadrado.</p>

<h3>O que a simetria dá de graça</h3>

<p>O torque em relação ao centro é \(\vet{\tau} = \vet{r}\cruz\vet{F}\), e os
dois vetores são paralelos: o torque é nulo, e o momento angular se conserva.
Daí saem duas consequências imediatas.</p>

<p><strong>O movimento é plano.</strong> Como \(\vet{L} = \vet{r}\cruz m\vet{v}\)
é constante e \(\vet{r}\) é perpendicular a ele por construção, a posição fica
para sempre no plano perpendicular a \(\vet{L}\). O problema de três dimensões
vira um de duas antes de qualquer conta.</p>

<p><strong>A lei das áreas.</strong> Em coordenadas polares no plano, a área
varrida num tempo \(dt\) é \(dA = \frac12 r^2 d\varphi\), de modo que</p>

\[ \der{A}{t} = \frac{r^2\dot\varphi}{2} = \frac{L}{2m} = \text{constante}. \]

<p>Essa é a segunda lei de Kepler, e repare no que ela <em>não</em> usa:
nada sobre gravitação. Ela vale para qualquer força central, inclusive uma
mola. Kepler descobriu em 1609, a partir de dados de Marte, uma consequência
de simetria.</p>

<h3>O problema de dois corpos vira o de um</h3>

<p>Falta um cuidado que o módulo 11 já cobrou: o Sol também se move. Com dois
corpos interagindo apenas entre si, subtraia as duas equações de movimento:</p>

\[ \ddot{\vet{r}} = \ddot{\vet{r}}_2 - \ddot{\vet{r}}_1
   = -\frac{G(m_1+m_2)}{r^2}\vers{r}. \]

<p>A separação relativa obedece à equação de <em>um</em> corpo no campo da
massa <strong>total</strong>. Equivalentemente, escrevendo em termos da massa
reduzida \(\mu = m_1m_2/(m_1+m_2)\), do módulo 6, o problema se reduz a uma
partícula de massa \(\mu\) no campo de \(m_1+m_2\).</p>

<p>O programa integra os dois corpos sem reduzir nada, com massas de
\(10^{30}\) e \(3\times10^{29}\) kg, e compara a trajetória relativa com a do
problema reduzido: a maior diferença é de \(10^{-12}\) da separação, que é
erro de integrador. A redução é exata, e não uma aproximação de massa
pequena.</p>
'''

S2 = r'''
<p>A conservação de \(L\) faz mais do que achatar o movimento: ela elimina o
ângulo da conta de energia. Com \(\dot\varphi = L/mr^2\),</p>

\[ E = \frac{m}{2}\left(\dot{r}^2 + r^2\dot\varphi^2\right) + U(r)
    = \frac{m\dot{r}^2}{2}
    + \underbrace{\frac{L^2}{2mr^2} + U(r)}_{U_{\text{ef}}(r)}. \]

<div class="bloco def">
<p class="rotulo">Potencial efetivo</p>
<p>O problema de duas coordenadas virou um de <strong>uma</strong>, formalmente
idêntico ao do módulo 4: uma partícula num potencial unidimensional
\(U_{\text{ef}}\). O termo novo, \(L^2/2mr^2\), é a <strong>barreira
centrífuga</strong>: repulsiva, divergente na origem, e é ela que impede uma
partícula com \(L \neq 0\) de cair no centro, por mais atraída que seja.</p>
</div>

<div data-widget="orbitas"></div>

<p>E aí o gráfico responde quase tudo <em>antes</em> de integrar, exatamente
como no módulo 4. Onde \(E &lt; U_{\text{ef}}\) o movimento é proibido; os
cruzamentos são os pontos de retorno; o mínimo da curva é a órbita circular.
Para o potencial de Kepler, \(U = -k/r\), a classificação sai completa:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>energia</th><th>pontos de retorno</th><th>órbita</th>
<th>excentricidade</th></tr></thead>
<tbody>
<tr><td>\(E = U_{\text{ef,mín}}\)</td><td>um só raio</td><td>circular</td>
<td>\(e = 0\)</td></tr>
<tr><td>\(U_{\text{ef,mín}} &lt; E &lt; 0\)</td><td>dois</td><td>elíptica</td>
<td>\(0 &lt; e &lt; 1\)</td></tr>
<tr><td>\(E = 0\)</td><td>um</td><td>parabólica</td><td>\(e = 1\)</td></tr>
<tr><td>\(E &gt; 0\)</td><td>um</td><td>hiperbólica</td><td>\(e &gt; 1\)</td></tr>
</tbody>
</table>
</div>

<p>A fronteira \(E = 0\) é a velocidade de escape do módulo 5, aqui vista de
outro ângulo: ela separa órbitas fechadas de abertas.</p>
'''

S3 = r'''
<p>Para a forma da órbita, e não apenas para a sua classificação, é preciso
integrar. A conta tem um truque, e o truque vale ser entendido porque
reaparece em outros problemas.</p>

<p>Primeiro, troque a variável independente de \(t\) para \(\varphi\), usando
a conservação de \(L\):</p>

\[ \der{r}{t} = \der{r}{\varphi}\dot\varphi
   = \frac{L}{mr^2}\der{r}{\varphi}. \]

<p>Substituindo na energia aparece uma equação com \(r^{-4}\), que é feia.
A troca \(u = 1/r\) arruma tudo, porque
\(dr/d\varphi = -u^{-2}\,du/d\varphi\):</p>

\[ \left(\der{u}{\varphi}\right)^2 = \frac{2mE}{L^2}
   + \frac{2mk}{L^2}u - u^2. \]

<p>Derivando em \(\varphi\) e dividindo por \(2\,du/d\varphi\):</p>

<div class="bloco def">
<p class="rotulo">A equação da órbita</p>
\[ \dder{u}{\varphi} + u = \frac{mk}{L^2}. \]
<p>É o oscilador harmônico do módulo 6, com \(\varphi\) no lugar do tempo e um
termo de fonte constante. A órbita de Kepler e a mola são o mesmo problema
matemático, em variáveis diferentes.</p>
</div>

<p>A solução geral é \(u = mk/L^2 + A\cos(\varphi-\varphi_0)\). Escolhendo os
eixos de modo que \(\varphi_0 = 0\) e definindo \(e = AL^2/mk\):</p>

\[ r(\varphi) = \frac{p}{1+e\cos\varphi}, \qquad
   p = \frac{L^2}{mk}, \qquad
   e = \sqrt{1 + \frac{2EL^2}{mk^2}}. \]

<p>Essa é a equação de uma <strong>cônica com foco na origem</strong>, e é a
primeira lei de Kepler, agora com a classificação por energia que a tabela
anterior antecipou. A excentricidade depende só de \(E\) e \(L\): não é
preciso desenhar a órbita para saber o formato dela.</p>

<p>O programa confere isso comparando a excentricidade prevista com a medida
na órbita integrada, pela razão entre os raios extremos:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>\(v_0/v_{\text{circ}}\)</th><th>\(e\) pela energia</th>
<th>\(e\) pela geometria</th><th>diferença</th></tr></thead>
<tbody>
<tr><td>1,00</td><td>0,000000000</td><td>0,000000000</td><td>\(5\times10^{-15}\)</td></tr>
<tr><td>1,10</td><td>0,210000000</td><td>0,210000000</td><td>\(2\times10^{-15}\)</td></tr>
<tr><td>1,25</td><td>0,562500000</td><td>0,562500000</td><td>\(1\times10^{-14}\)</td></tr>
<tr><td>1,40</td><td>0,960000000</td><td>0,959999997</td><td>\(3\times10^{-9}\)</td></tr>
</tbody>
</table>
</div>

<h3>A terceira lei</h3>

<p>Integrando a lei das áreas sobre um período inteiro, e usando que a área da
elipse é \(\pi ab\) com \(b = a\sqrt{1-e^2}\):</p>

\[ T = \frac{2\pi ab}{L/m} \quad\Longrightarrow\quad
   T^2 = \frac{4\pi^2a^3}{G(m_1+m_2)}. \]

<p>O programa verifica em quatro órbitas de semieixos diferentes: a razão
\(T^2G(m_1+m_2)/4\pi^2a^3\) dá 1,000000000000 em todas.</p>

<div class="bloco alerta">
<p class="rotulo">A constante de Kepler não é constante</p>
<p>Na forma que Kepler escreveu, \(T^2/a^3\) é a mesma para todos os planetas.
Pela dedução, ela depende de \(m_1+m_2\), e portanto difere de um planeta para
outro. A lei de Kepler funciona porque o Sol tem mil vezes a massa de Júpiter,
que é o maior dos planetas: o erro é de um milésimo. Levar a lei a sério até a
quarta casa, num sistema binário com massas comparáveis, dá errado.</p>
</div>
'''

S4 = r'''
<p>Há uma propriedade das órbitas de Kepler tão familiar que passa
despercebida: <strong>elas fecham</strong>. Depois de uma volta, o planeta
volta exatamente ao mesmo ponto, com a mesma velocidade, e repete o percurso
para sempre.</p>

<p>Isso é excepcional, e o programa mede o quanto: com o potencial
\(-k/r\) puro, o avanço do periastro ao longo de seis órbitas é de
\(10^{-13}\) radianos, que é erro de integrador.</p>

<div class="bloco fisica">
<p class="rotulo">Teorema de Bertrand</p>
<p>Entre todas as leis de potência \(U \propto r^n\), apenas <strong>duas</strong>
produzem órbitas fechadas para <em>todas</em> as condições iniciais limitadas:
a gravitação, \(n = -1\), e a mola, \(n = 2\). Qualquer outra lei, e qualquer
perturbação de uma destas, abre a órbita numa roseta. A regularidade que Kepler
observou não é típica da natureza: é um acidente privilegiado do inverso do
quadrado.</p>
</div>

<p>Isso tem uma consequência prática enorme: a órbita que não fecha
<strong>denuncia</strong> que falta algo no potencial. É um instrumento, e foi
usado como tal.</p>

<p>Acrescente ao potencial um termo \(-\beta/r^3\) e a equação da órbita ganha
um termo linear em \(u\), o que muda a frequência angular do oscilador em
\(\varphi\). Em primeira ordem, o periastro avança</p>

\[ \Delta\varphi = \frac{6\pi\beta}{L^2p} \quad\text{por órbita}. \]

<p>O programa mede o avanço na órbita integrada e compara:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>\(\beta\)</th><th>avanço medido (rad)</th>
<th>previsto (rad)</th><th>razão</th></tr></thead>
<tbody>
<tr><td>\(3\times10^{39}\)</td><td>0,01024131</td><td>0,01019645</td><td>1,004</td></tr>
<tr><td>\(1\times10^{40}\)</td><td>0,03449220</td><td>0,03398817</td><td>1,015</td></tr>
<tr><td>\(3\times10^{40}\)</td><td>0,10665120</td><td>0,10196450</td><td>1,046</td></tr>
<tr><td>\(1\times10^{41}\)</td><td>0,39893000</td><td>0,33988170</td><td>1,174</td></tr>
</tbody>
</table>
</div>

<p>A razão vai a 1 quando a perturbação diminui, que é o comportamento certo
de uma fórmula de primeira ordem. Com perturbação grande ela subestima, e o
desvio é previsível, não é erro.</p>

<h3>Mercúrio</h3>

<p>O caso que interessa é exatamente esse. A relatividade geral acrescenta ao
potencial newtoniano um termo em \(1/r^3\),</p>

\[ U_{\text{RG}} = -\frac{GML^2}{c^2r^3}, \]

<p>e com ele o periastro avança</p>

\[ \Delta\varphi = \frac{6\pi GM}{c^2a\left(1-e^2\right)}\ \text{por órbita}. \]

<p>Para Mercúrio (\(a = 5{,}7909\times10^{10}\) m, \(e = 0{,}20563\),
\(T = 87{,}9691\) dias), isso dá \(5{,}019\times10^{-7}\) rad por órbita, ou
0,10352 segundos de arco; com 415,20 órbitas por século,</p>

\[ \boxed{42{,}98\ \text{segundos de arco por século}} \]

<p>contra 43,0 observados, depois de descontadas as perturbações dos outros
planetas (que são bem maiores, cerca de 530″/século, e explicam o resto do
avanço total de 574″). Foi a primeira confirmação da relatividade geral, em
1915, e é um número que a mecânica newtoniana não consegue produzir de jeito
nenhum.</p>

<p>Vale notar o que estava em jogo. Le Verrier, que havia descoberto Netuno
pelo mesmo método (uma órbita que não fechava como devia), propôs um planeta
interior, Vulcano, para explicar Mercúrio. Nunca foi encontrado. Dessa vez a
anomalia não era um corpo faltando, e sim a teoria.</p>
'''

S5 = r'''
<p>Uma última verificação, que amarra este módulo ao 6. O teorema do virial,
para \(U \propto r^n\), dá \(2\med{T} = n\med{U}\). Com \(n = -1\):</p>

\[ 2\med{T} = -\med{U} \quad\Longrightarrow\quad
   E = \med{T}+\med{U} = -\med{T} = \frac{\med{U}}{2}. \]

<p>O programa integra uma órbita inteira e mede:</p>

<div class="saida">
media de T:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+1,268770e+08 J/kg<br>
media de U:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&minus;2,537507e+08 J/kg<br>
razao &lt;T&gt; / (&minus;&lt;U&gt;/2):&nbsp;<b>1,000013</b>
</div>

<div class="bloco alerta">
<p class="rotulo">Um erro que não dá sintoma</p>
<p>A primeira versão deste cálculo deu 0,963 em vez de 1, e o motivo ficou
registrado no código: a integração usava o período de <em>outra</em> órbita,
calculada na seção anterior com excentricidade diferente, de modo que a média
era tomada sobre uma fração de volta. O resultado não diverge, não dá erro, não
parece absurdo: dá 0,963. Médias sobre períodos só valem sobre períodos
inteiros, e conferir um teorema conhecido é a maneira mais barata de descobrir
que se integrou a coisa errada.</p>
</div>

<p>A relação \(2\med{T} = -\med{U}\) é mais útil do que parece. Aplicada a um
aglomerado de galáxias, ela permite estimar a massa total a partir da dispersão
de velocidades, que é observável. Foi assim que Fritz Zwicky, em 1933, mediu o
aglomerado de Coma e encontrou uma massa muito maior que a da matéria
luminosa: a primeira evidência de matéria escura veio do teorema do virial,
aplicado a órbitas.</p>
'''

S6 = r'''
<div class="cartoes">
  <a class="cartao" href="codigo/orbitas.py">
    <span class="numero">Programa</span>
    <h3>orbitas.py</h3>
    <p>Integra os dois corpos e compara com o problema reduzido, mede a lei
    das áreas, confere a excentricidade e a terceira lei, mede a precessão
    com e sem perturbação, e verifica o virial.</p>
  </a>
</div>

<p><strong>O que ele imprime, e o que conferir.</strong></p>

<ul>
<li>A trajetória relativa dos dois corpos e a do problema reduzido diferem em
\(10^{-12}\) da separação.</li>
<li>\(dA/dt\) vale \(L/2\) e o resíduo cai por quatro quando o passo cai por
dois, porque é a área do triângulo de corda, e não física.</li>
<li>A excentricidade pela energia e pela geometria coincidem em
\(10^{-14}\).</li>
<li>\(T^2G(m_1+m_2)/4\pi^2a^3\) dá 1 em doze casas, em quatro órbitas.</li>
<li>Sem perturbação a órbita fecha em \(10^{-13}\) rad; com \(-\beta/r^3\), a
razão entre o avanço medido e o previsto vai a 1,004 quando \(\beta\)
diminui.</li>
<li>O virial dá 1,000013.</li>
</ul>

<div class="bloco ex">
<p><strong>Para mexer.</strong> Troque o expoente da força de 2 para 2,1 e meça
a precessão: ela aparece imediatamente, e esse é o teste mais sensível do
expoente que existe em astronomia. Depois implemente a transferência de Hohmann
do exercício 12.4 e compare o \(\Delta v\) com a soma dos dois impulsos
calculados à mão. Por fim, resolva a equação de Kepler
\(M = E - e\sen E\) por Newton-Raphson e use-a para marcar a posição do planeta
em intervalos iguais de tempo, o que torna a lei das áreas visível no
desenho.</p>
</div>
'''

SECOES = [
    ('O que a simetria dá de graça', S1),
    ('O potencial efetivo, e a classificação das órbitas', S2),
    ('A equação da órbita, e as três leis', S3),
    ('Fechar é excepcional, e Mercúrio', S4),
    ('O virial em órbita, e a matéria escura', S5),
    ('No Spyder', S6),
]

SECOES.append(('Exercícios propostos', exercicios.bloco(LISTA)))


def main():
    titulos = [t for t, _ in SECOES]
    escreve('aula12.html', secoes_html(SECOES), secoes=titulos,
            subtitulo='Uma força central conserva o momento angular, e com '
                      'isso achata o movimento num plano e o reduz a uma '
                      'dimensão. O gráfico do potencial efetivo classifica as '
                      'órbitas antes de qualquer integração, e o que o inverso '
                      'do quadrado tem de especial é que elas fecham.')


if __name__ == '__main__':
    main()
