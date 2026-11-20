# -*- coding: utf-8 -*-
"""Módulo 4: trabalho, energia e forças conservativas.

O fio do módulo é a equivalência entre quatro afirmações que o aluno costuma
decorar separadas: trabalho independente do caminho, trabalho nulo em
caminho fechado, existência de U, rotacional nulo. O programa verifica as
quatro na mesma força.
"""
from molde import escreve, secoes_html
import exercicios
from lista_aula04 import LISTA

S1 = r'''
<p>Integrar a segunda lei no tempo, como fizemos no módulo 3, dá a trajetória
inteira, e é a resposta mais completa que existe. O preço é que ela só sai
passo a passo, e há perguntas que não precisam dela. Com que velocidade o
bloco chega ao fim do plano? Até onde sobe o carrinho? A montanha-russa fecha
o <em>looping</em>? Nenhuma dessas pergunta <em>quando</em>, e é essa a brecha
que o conceito de trabalho explora.</p>

<p>O trabalho de uma força ao longo de um deslocamento é a integral de linha</p>

\[ W_{a\to b} = \int_{a}^{b} \vet{F}\cdot d\vet{r}, \]

<p>em que \(d\vet{r}\) é o deslocamento infinitesimal <strong>ao longo do
caminho percorrido</strong>. O produto escalar já diz uma parte da física:
a componente da força perpendicular ao movimento não realiza trabalho nenhum.
É por isso que a normal de um plano, a tração de um pêndulo e a força
magnética sobre uma carga ficam todas de fora da conta de energia, por mais
intensas que sejam.</p>

<h3>O teorema do trabalho e da energia cinética</h3>

<p>Tome a segunda lei e multiplique escalarmente por \(d\vet{r} = \vet{v}\,dt\):</p>

\[ \vet{F}\cdot d\vet{r} = m\der{\vet{v}}{t}\cdot\vet{v}\,dt
   = \frac{m}{2}\der{(\vet{v}\cdot\vet{v})}{t}\,dt
   = d\!\left(\frac{mv^2}{2}\right). \]

<p>Integrando dos dois lados entre dois instantes:</p>

\[ W_{a\to b} = T_b - T_a, \qquad T = \frac{mv^2}{2}. \]

<p>Esse resultado vale para <strong>qualquer</strong> força: elástica,
gravitacional, de atrito, de arrasto, de contato. Não é preciso que a força
seja conservativa, nem que se conheça energia potencial nenhuma. É apenas a
segunda lei reescrita, e é por isso que ele é o ponto de partida e não a
conclusão.</p>

<div class="destaque">
<p><strong>O que o teorema não resolve.</strong> Ele troca a integral no tempo
por uma integral no espaço, e essa integral ainda depende do caminho que o
corpo percorreu. Para calcular \(W\) é preciso saber a trajetória, que é
justamente o que se queria evitar. A saída vem na próxima seção, e só para
algumas forças.</p>
</div>
'''

S2 = r'''
<p>Pegue a força \(\vet{F} = (y^2,\,2xy)\) e calcule o trabalho de \((0,0)\) a
\((1,1)\) por três caminhos diferentes: a reta, o caminho em duas pernas (todo
o \(x\) primeiro, depois todo o \(y\)) e um arco. O programa faz as três
integrais:</p>

<div class="saida">
Forca CONSERVATIVA  F = (y^2, 2xy),  vinda de U = -x y^2<br>
&nbsp;&nbsp;reta&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;W = <b>+1,0000000000</b><br>
&nbsp;&nbsp;duas pernas&nbsp;&nbsp;&nbsp;&nbsp;W = <b>+1,0000000000</b><br>
&nbsp;&nbsp;arco&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;W = <b>+1,0000000000</b>
</div>

<p>Agora troque a força por \(\vet{F} = (-y,\,x)\), que não é um bicho exótico:
é a força que gira, o campo de velocidades de um corpo rígido. Os mesmos três
caminhos, entre os mesmos dois pontos:</p>

<div class="saida">
Forca com ROTACIONAL  F = (-y, x)<br>
&nbsp;&nbsp;reta&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;W = <b>+0,0000000000</b><br>
&nbsp;&nbsp;duas pernas&nbsp;&nbsp;&nbsp;&nbsp;W = <b>+1,0000000000</b><br>
&nbsp;&nbsp;arco&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;W = <b>&minus;0,8912676813</b>
</div>

<p>Três respostas diferentes para a mesma pergunta, e nenhuma delas está
errada. Mudou o caminho, mudou o trabalho. Perguntar quanto vale \(W\) entre
dois pontos, para essa força, é uma pergunta malformulada: falta dizer por
onde.</p>

<p>As forças para as quais a pergunta <em>está</em> bem formulada ganharam
nome: são as <strong>forças conservativas</strong>. E sobre elas há quatro
afirmações que são a mesma afirmação, escrita de quatro maneiras:</p>

<div class="cartoes">
  <div class="cartao">
    <span class="numero">1</span>
    <h3>O caminho não importa</h3>
    <p>\(W_{a\to b}\) é o mesmo por qualquer caminho que ligue \(a\) a \(b\).</p>
  </div>
  <div class="cartao">
    <span class="numero">2</span>
    <h3>O circuito fechado dá zero</h3>
    <p>\(\oint \vet{F}\cdot d\vet{r} = 0\) em qualquer curva fechada.</p>
  </div>
  <div class="cartao">
    <span class="numero">3</span>
    <h3>Existe um potencial</h3>
    <p>Existe \(U(\vet{r})\) tal que \(\vet{F} = -\nabla U\).</p>
  </div>
  <div class="cartao">
    <span class="numero">4</span>
    <h3>O rotacional é nulo</h3>
    <p>\(\rot{\vet{F}} = 0\) em toda a região.</p>
  </div>
</div>

<p>A ida de 1 para 2 é imediata: um caminho fechado é a ida por um caminho e a
volta por outro, e se os dois trabalhos de ida são iguais, a soma com a volta
invertida dá zero. A ida de 2 para 3 é a construção de \(U\): fixe um ponto
\(O\) e defina \(U(\vet{r}) = -\int_{O}^{\vet{r}}\vet{F}\cdot d\vet{r}\); a
definição só faz sentido porque 2 garante que a escolha do caminho não muda o
resultado. A ida de 3 para 4 é o cálculo vetorial do módulo 1, já que
\(\rot{(\nabla U)} = 0\) sempre. E a volta de 4 para 2 é o
<a href="https://pt.wikipedia.org/wiki/Teorema_de_Green">teorema de Green</a>,
ou o de Stokes em três dimensões.</p>

<p>O programa verifica as quatro na mesma força. O rotacional de
\((y^2,2xy)\), calculado por diferenças finitas em três pontos quaisquer, dá
\(10^{-11}\), que é o erro da diferença finita; o de \((-y,x)\) dá exatamente
2 em todos eles. E o trabalho numa volta fechada de raio 1:</p>

<div class="saida">
conservativa:&nbsp;&nbsp;&nbsp;W = <b>&minus;2,220e&minus;16</b><br>
com rotacional: W = <b>+6,283185</b>&nbsp;&nbsp;&nbsp;contra 2 pi = 6,283185
</div>

<p>Repare no \(2\pi\): é o rotacional, 2, vezes a área do círculo, \(\pi\). O
teste local e o teste global carregam a mesma informação, e o teorema de Green
é o cambista entre os dois.</p>

<div class="destaque">
<p><strong>A letra miúda do passo 4 para o 2.</strong> O teorema de Green exige
que a região onde a força está definida não tenha buracos. Num plano com um
ponto removido, a força \(\vet{F} = (-y,\,x)/(x^2+y^2)\) tem rotacional nulo
em todo lugar onde está definida, e ainda assim dá \(2\pi\) numa volta em
torno da origem. É o mesmo ponto geométrico que aparece no
<a href="https://pt.wikipedia.org/wiki/Efeito_Aharonov-Bohm">efeito
Aharonov-Bohm</a>, e por isso o critério 4 é condição suficiente apenas em
regiões simplesmente conexas.</p>
</div>
'''

S3 = r'''
<p>Para uma força conservativa, o trabalho entre dois pontos é a diferença de
uma função que só depende da posição:</p>

\[ W_{a\to b} = -\left[U(b) - U(a)\right] = U(a) - U(b). \]

<p>Juntando com o teorema do trabalho e da energia cinética, que vale sempre:</p>

\[ T_b - T_a = U(a) - U(b) \quad\Longrightarrow\quad
   T_a + U(a) = T_b + U(b) \equiv E. \]

<p>A conservação da energia mecânica não é um princípio novo que se acrescenta
a Newton. Ela é uma <strong>primeira integral</strong> da equação de
movimento: uma combinação de posição e velocidade cuja derivada no tempo é
nula, obtida integrando a segunda lei uma vez. Daí a utilidade prática: ela
troca uma equação diferencial de segunda ordem por uma de primeira ordem, e
muitas vezes isso basta para responder o que se perguntou.</p>

<p>O sinal de menos na definição de \(U\) é convenção, mas é uma convenção com
motivo: ela faz a energia potencial crescer quando se empurra o corpo contra a
força, de modo que \(U\) mede o quanto se <em>investiu</em> no sistema. Com
ela, a força sai do potencial por</p>

\[ \vet{F} = -\nabla U, \qquad\text{e em uma dimensão}\qquad F = -\der{U}{x}. \]

<p>A energia potencial é definida a menos de uma constante, porque só
diferenças aparecem na física. Mudar o nível zero muda \(U\) e \(E\) juntos,
sem mexer em força nenhuma. Os três casos de sempre:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>Força</th><th>Expressão</th><th>Energia potencial</th>
<th>Zero usual</th></tr></thead>
<tbody>
<tr><td>Peso, perto do chão</td><td>\(-mg\vers{y}\)</td><td>\(mgy\)</td>
<td>o chão</td></tr>
<tr><td>Mola, lei de Hooke</td><td>\(-kx\)</td><td>\(\frac12kx^2\)</td>
<td>a mola relaxada</td></tr>
<tr><td>Gravitação</td><td>\(-\dfrac{GMm}{r^2}\vers{r}\)</td>
<td>\(-\dfrac{GMm}{r}\)</td><td>o infinito</td></tr>
</tbody>
</table>
</div>

<p>Na terceira linha o zero no infinito não é escolha estética: é a única que
torna \(U\) finita em todo ponto e ainda deixa a forma simples. O sinal
negativo que sobra diz que é preciso <em>fornecer</em> energia para afastar os
dois corpos, e é desse negativo que sai a ideia de energia de ligação, que
reaparece do átomo ao sistema solar.</p>
'''

S4 = r'''
<p>Em uma dimensão, com \(E\) fixo, a conservação da energia vira</p>

\[ \frac{m}{2}\left(\der{x}{t}\right)^2 = E - U(x). \]

<p>O lado esquerdo não pode ser negativo. Essa única observação já dá quase
tudo o que se quer saber sobre o movimento, <strong>sem resolver equação
alguma</strong>, apenas olhando o gráfico de \(U\) com uma reta horizontal na
altura \(E\):</p>

<ul>
<li>Onde \(U(x) &gt; E\), o movimento é <strong>proibido</strong>. O corpo
nunca chega ali.</li>
<li>Onde \(U(x) = E\), a velocidade é nula: são os <strong>pontos de
retorno</strong>. O corpo chega, para e volta.</li>
<li>Entre dois pontos de retorno, o movimento é <strong>oscilatório</strong>,
confinado, e se repete indefinidamente.</li>
<li>Nos mínimos de \(U\), a força é nula e o equilíbrio é
<strong>estável</strong>, porque qualquer deslocamento gera força de volta.
Nos máximos, a força também é nula, e o equilíbrio é
<strong>instável</strong>.</li>
<li>A velocidade é máxima onde \(U\) é mínima, e o corpo anda devagar perto dos
pontos de retorno. É por isso que a maior parte do tempo de uma oscilação é
gasta perto dos extremos.</li>
</ul>

<p>O componente abaixo é esse gráfico, para o poço duplo
\(U(x) = x^4 - 2x^2\). Mova a energia e veja o que muda.</p>

<div data-widget="energia"></div>

<p>Dois regimes aparecem. Com \(E &lt; 0\) o corpo fica preso em um dos dois
poços, e qual deles depende só de onde começou: a barreira em \(x = 0\) é
intransponível. Com \(E &gt; 0\) os dois poços se juntam num único movimento,
que varre os dois lados. A transição em \(E = 0\) é brusca, e o período diverge
exatamente ali, porque o corpo passa cada vez mais devagar pelo topo da
barreira, onde a força é nula.</p>

<h3>O período sai do gráfico</h3>

<p>O gráfico de \(U\) dá mais do que a descrição qualitativa: dá o período, em
número. Isolando a velocidade e separando as variáveis,</p>

\[ \der{x}{t} = \sqrt{\frac{2\left[E - U(x)\right]}{m}}
   \quad\Longrightarrow\quad
   T = \int_{x_1}^{x_2}\sqrt{\frac{2m}{E - U(x)}}\;dx, \]

<p>com \(x_1\) e \(x_2\) os dois pontos de retorno. O integrando diverge nos
extremos, mas a divergência é integrável, e uma troca de variável
\(x = \frac{x_1+x_2}{2} + \frac{x_2-x_1}{2}\sen\theta\) a cancela por
completo. O resultado é uma integral sobre a <strong>posição</strong>, não
sobre o tempo: o período sai sem que se tenha resolvido a equação de
movimento.</p>

<p>Vale a pena medir se isso é verdade mesmo. O programa calcula o período
dos dois jeitos, pela quadratura acima e integrando a equação de movimento até
o corpo voltar:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>\(E\)</th><th>retorno interno</th><th>retorno externo</th>
<th>\(T\) por quadratura</th><th>\(T\) integrado</th><th>diferença</th></tr></thead>
<tbody>
<tr><td>\(-0{,}90\)</td><td>0,82691</td><td>1,14727</td><td>2,265540924</td>
<td>2,265540924</td><td>\(6\times10^{-11}\)</td></tr>
<tr><td>\(-0{,}75\)</td><td>0,70711</td><td>1,22474</td><td>2,342840168</td>
<td>2,342840168</td><td>\(1\times10^{-10}\)</td></tr>
<tr><td>\(-0{,}50\)</td><td>0,54120</td><td>1,30656</td><td>2,518927047</td>
<td>2,518927047</td><td>\(8\times10^{-12}\)</td></tr>
<tr><td>\(-0{,}25\)</td><td>0,36603</td><td>1,36603</td><td>2,831474417</td>
<td>2,831474417</td><td>\(4\times10^{-12}\)</td></tr>
<tr><td>\(-0{,}10\)</td><td>0,22653</td><td>1,39595</td><td>3,261573298</td>
<td>3,261573298</td><td>\(2\times10^{-11}\)</td></tr>
</tbody>
</table>
</div>

<p>Nove casas em comum entre dois cálculos que não têm nada em comum. E repare
na coluna do período: ele <em>cresce</em> com a energia. Isso é o oposto do que
acontece no oscilador harmônico, em que o período não depende da amplitude, e
é o primeiro sintoma da não linearidade, que volta no módulo 9.</p>

<p>No fundo do poço, porém, o harmônico é recuperado. Expandindo \(U\) em torno
do mínimo em \(x = 1\),</p>

\[ U(x) \simeq U(1) + \frac12 U''(1)\,(x-1)^2, \qquad U''(1) = 8, \]

<p>que é uma mola de constante \(k = U''(1)\), com período
\(2\pi/\sqrt{U''/m} = 2{,}221441\). É para esse número que a coluna da
quadratura caminha quando \(E\) se aproxima do fundo, \(-1\), e a tabela
mostra justamente isso. Qualquer mínimo de qualquer potencial é um oscilador
harmônico para amplitudes pequenas, e é por isso que o módulo 6 gasta um
módulo inteiro com uma única equação.</p>
'''

S5 = r'''
<p>O atrito e o arrasto do módulo 3 não são conservativos, e agora dá para
dizer isso com precisão em vez de por decreto. O trabalho do atrito cinético
sobre um bloco que percorre um caminho de comprimento \(\ell\) vale</p>

\[ W_{\text{at}} = -\mu N \ell, \]

<p>e \(\ell\) é o comprimento do caminho, não a distância entre os extremos.
Vá de \(a\) até \(b\) e volte: o deslocamento total é zero, e o trabalho do
atrito é \(-2\mu N d\), que não é zero. O critério 2 falha, e com ele os
outros três: não existe função \(U\) cuja diferença dê esse trabalho, porque o
resultado depende de quanto se andou e não de onde se está.</p>

<p>Com forças não conservativas presentes, a conta de energia fica</p>

\[ \left(T_b + U_b\right) - \left(T_a + U_a\right) = W_{\text{nc}}, \]

<p>em que \(W_{\text{nc}}\) é o trabalho das forças que sobraram, tipicamente
negativo. A energia mecânica diminui, e aqui convém ser honesto sobre o que
isso quer dizer. A energia não desapareceu: ela foi para o movimento
desordenado das moléculas das duas superfícies, que é o que se chama calor. Do
ponto de vista microscópico, todas as forças fundamentais são conservativas; a
dissipação é o que resta quando se descreve um sistema de \(10^{23}\) graus de
liberdade com apenas um. Essa frase é o ponto de partida da Física
Estatística, e é por isso que a irreversibilidade não aparece em nenhuma
equação deste curso, embora apareça em toda experiência de laboratório.</p>

<div class="destaque">
<p><strong>Um atalho que costuma sair errado.</strong> No atrito entre dois
corpos que deslizam um sobre o outro, o trabalho da força sobre um deles
<em>não</em> é o simétrico do trabalho sobre o outro, mesmo que as forças
sejam um par de ação e reação. Os dois pontos de aplicação percorrem
distâncias diferentes, e a diferença entre os dois trabalhos é exatamente o
calor gerado na interface. Esse é o exercício 4.6.</p>
</div>
'''

S6 = r'''
<p>O módulo 3 terminou com uma promessa: dizer por que alguém usaria o método
de Euler-Cromer, que tem a mesma ordem do método de Euler e, no lançamento de
projétil, errava mais. A resposta está na energia, e só aparece em integrações
longas.</p>

<p>O programa integra um oscilador harmônico por duzentos períodos, com quatro
métodos e o mesmo passo, e acompanha a energia. Para separar as duas coisas
que se confundem, ele mede o desvio da energia nos vinte primeiros períodos e
nos vinte últimos, em separado:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>Método</th><th>\(E_{\text{final}}/E_0 - 1\)</th>
<th>desvio nos 20 primeiros períodos</th>
<th>nos 20 últimos</th></tr></thead>
<tbody>
<tr><td>Euler</td><td>\(+2{,}9\times10^{5}\)</td><td>\(2{,}5\)</td>
<td>\(2{,}9\times10^{5}\)</td></tr>
<tr><td>Euler-Cromer</td><td>\(+1{,}8\times10^{-5}\)</td>
<td>\(5{,}0\times10^{-3}\)</td><td>\(5{,}0\times10^{-3}\)</td></tr>
<tr><td>Verlet</td><td>\(-8{,}3\times10^{-11}\)</td>
<td>\(2{,}5\times10^{-5}\)</td><td>\(2{,}5\times10^{-5}\)</td></tr>
<tr><td>RK4</td><td>\(-1{,}7\times10^{-9}\)</td>
<td>\(1{,}7\times10^{-10}\)</td><td>\(1{,}7\times10^{-9}\)</td></tr>
</tbody>
</table>
</div>

<p>Leia as duas últimas colunas antes da primeira. No Euler-Cromer e no
<a href="https://pt.wikipedia.org/wiki/Integra%C3%A7%C3%A3o_de_Verlet">Verlet</a>
o desvio é o <strong>mesmo</strong> no começo e no fim: a energia oscila, com
amplitude fixa, e não vai a lugar nenhum. No Euler ele cresce sem limite, de
2,5 para \(3\times10^{5}\). E no RK4 ele cresce também, exatamente dez vezes
de um trecho para o outro, que é a razão dos tempos: a perda é
<strong>linear no tempo</strong>, lenta mas sistemática, e o sinal negativo da
primeira coluna diz para que lado.</p>

<p>Essa é a diferença entre precisão e estrutura. O RK4 é, de longe, o mais
preciso dos quatro: o erro na posição depois de uma volta é milhões de vezes
menor que o dos outros. Mas ele não preserva a área no espaço de fase, e por
isso dissipa, devagar e para sempre. O Euler-Cromer e o Verlet são
<strong>simpléticos</strong>: preservam exatamente essa estrutura, e em troca
mantêm a energia presa numa faixa estreita por quanto tempo for. Quem integra
órbitas planetárias por milhões de anos escolhe o segundo grupo, e aceita o
erro de fase que vem junto.</p>

<div class="destaque">
<p><strong>Por que o Euler ganha energia.</strong> Num passo do método de
Euler explícito aplicado ao oscilador, a amplitude no espaço de fase é
multiplicada por \(\sqrt{1+\omega^2\Delta t^2}\), que é maior que 1 para
qualquer passo. Em \(N\) passos isso dá
\((1+\omega^2\Delta t^2)^{N/2}\), um crescimento exponencial. Com
\(\Delta t = 0{,}01\) e 125 663 passos, o fator previsto é \(e^{6{,}28}\) em
amplitude, ou \(2{,}9\times10^{5}\) em energia, que é exatamente o que a
tabela mostra. O método não erra por descuido: ele erra de um jeito previsível,
e dá para prever o erro antes de rodar.</p>
</div>
'''

S7 = r'''
<div class="cartoes">
  <a class="cartao" href="codigo/energia.py">
    <span class="numero">Programa</span>
    <h3>energia.py</h3>
    <p>Calcula o trabalho por três caminhos, testa o rotacional e o circuito
    fechado, lê o movimento no gráfico de \(U\) com o período por quadratura e
    mede a deriva de energia de quatro integradores.</p>
  </a>
</div>

<p><strong>O que ele imprime, e o que conferir.</strong></p>

<ul>
<li>Os três caminhos dão o mesmo trabalho para a força conservativa, e esse
valor coincide com \(-\Delta U\) em dez casas.</li>
<li>Para a força com rotacional, a diferença entre o caminho reto e o de duas
pernas vale exatamente 1, que é o rotacional, 2, vezes a área do triângulo
entre os dois caminhos, \(1/2\). O teorema de Green em números.</li>
<li>O trabalho numa volta fechada de raio 1 dá \(10^{-16}\) para a
conservativa e \(2\pi\) para a outra, com seis casas certas.</li>
<li>O período por quadratura e o período integrado coincidem em
\(10^{-10}\) nos cinco valores de energia.</li>
<li>O desvio de energia do Euler-Cromer e do Verlet é idêntico nos vinte
primeiros e nos vinte últimos períodos; o do RK4 cresce por um fator dez, que
é a razão dos tempos.</li>
</ul>

<div class="bloco ex">
<p><strong>Para mexer.</strong> Troque o poço duplo por
\(U(x) = -U_0\,\mathrm{sech}^2(x/a)\), que é um poço só, e veja o período
divergir quando \(E \to 0^-\) pelo mesmo motivo de sempre: o corpo leva um
tempo infinito para chegar ao ponto de retorno quando ele coincide com um
máximo de \(U\). Depois mude o passo da seção 4 de \(0{,}01\) para \(0{,}05\) e
confira se a previsão \((1+\omega^2\Delta t^2)^{N/2}\) continua acertando o
erro do Euler.</p>
</div>
'''

SECOES = [
    ('Trabalho, e a pergunta que ele responde', S1),
    ('Quatro maneiras de dizer a mesma coisa', S2),
    ('A energia potencial e a primeira integral', S3),
    ('Lendo o movimento inteiro no gráfico de U', S4),
    ('O atrito, e a energia que não some', S5),
    ('A energia sobrevive ao integrador?', S6),
    ('No Spyder', S7),
]

SECOES.append(('Exercícios propostos', exercicios.bloco(LISTA)))


def main():
    titulos = [t for t, _ in SECOES]
    escreve('aula04.html', secoes_html(SECOES), secoes=titulos,
            subtitulo='O trabalho de uma força depende do caminho, e as forças '
                      'para as quais ele não depende ganharam nome. Daí sai a '
                      'energia potencial, e com ela a possibilidade de ler o '
                      'movimento inteiro no gráfico de U sem resolver equação '
                      'nenhuma.')


if __name__ == '__main__':
    main()
