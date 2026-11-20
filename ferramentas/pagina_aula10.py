# -*- coding: utf-8 -*-
"""Módulo 10: caos determinístico.

Fecha a unidade de não linear. Fica com o lado dissipativo e introdutório
(mapa logístico, cascata, Feigenbaum, Lyapunov, atratores); o caso
hamiltoniano, com toros, seções de Poincaré e KAM, é a unidade final de
Mecânica Clássica III.
"""
from molde import escreve, secoes_html
import exercicios
from lista_aula10 import LISTA

S1 = r'''
<p>O módulo 9 terminou com um resultado que fecha uma porta. Pelo teorema de
Poincaré-Bendixson, uma trajetória presa numa região limitada do
<strong>plano</strong>, sem ponto fixo pela frente, tem de convergir para uma
órbita fechada. Não existe terceira opção. Como trajetórias não podem se
cruzar, não há espaço no plano para uma curva se embolar indefinidamente sem
se repetir.</p>

<div class="bloco def">
<p class="rotulo">Do que o caos precisa</p>
<p>Para haver caos num sistema de equações diferenciais autônomas são
necessárias <strong>não linearidade</strong> e pelo menos
<strong>três dimensões</strong> no espaço de fase. Nem uma nem outra é
suficiente sozinha.</p>
</div>

<p>Três dimensões aparecem com mais facilidade do que parece. Um oscilador
forçado, como o do módulo 8, tem duas variáveis de estado, \(x\) e
\(\dot{x}\), mais a fase da força, que avança sozinha: são três. É por isso
que o pêndulo amortecido e forçado pode ser caótico enquanto o pêndulo
livre, por maior que seja a amplitude, nunca é.</p>

<p>Há outro caminho, mais barato ainda, e é o deste módulo: desistir do tempo
contínuo. Num <strong>mapa</strong>, o estado pula de um valor para o
seguinte, e a proibição de cruzamento não se aplica, porque não há curva
contínua ligando os pontos. Uma única variável basta.</p>

\[ x_{n+1} = r\,x_n\left(1-x_n\right). \]

<p>Esse é o <strong>mapa logístico</strong>, e ele tem uma linha de conta por
iteração. Foi popularizado em 1976 por
<a href="https://pt.wikipedia.org/wiki/Robert_May,_Bar%C3%A3o_May_de_Oxford">Robert
May</a>, num artigo com o subtítulo certo: equações muito simples podem ter
dinâmica muito complicada. Lido como modelo, \(x\) é uma população
normalizada e o termo \((1-x)\) é a saturação por falta de recursos.</p>
'''

S2 = r'''
<p>A primeira vista do componente é a <strong>teia</strong>, que é o mapa
feito à mão: suba até a parábola para calcular \(x_{n+1}\), ande até a
diagonal para transformar essa saída na entrada seguinte, repita.</p>

<div data-widget="caos"></div>

<p>Os pontos fixos são os cruzamentos da parábola com a diagonal:
\(x^* = 0\) e \(x^* = 1 - 1/r\). A estabilidade é decidida pela inclinação da
parábola ali, pelo mesmo tipo de argumento do módulo 9, agora na versão
discreta:</p>

\[ \left|f'(x^*)\right| &lt; 1 \quad\Longrightarrow\quad \text{estável},
   \qquad f'(x^*) = r\left(1-2x^*\right) = 2-r. \]

<p>O programa confere a previsão contra a iteração:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>\(r\)</th><th>\(x^*=1-1/r\)</th><th>\(f'(x^*)\)</th>
<th>previsão</th><th>para onde a órbita vai</th></tr></thead>
<tbody>
<tr><td>0,8</td><td>\(-0{,}25\)</td><td>\(+1{,}20\)</td><td>instável</td>
<td>\(x = 0\), extinção</td></tr>
<tr><td>1,5</td><td>0,333333</td><td>\(+0{,}50\)</td><td>estável</td>
<td>\(x = 0{,}333333\)</td></tr>
<tr><td>2,9</td><td>0,655172</td><td>\(-0{,}90\)</td><td>estável</td>
<td>\(x = 0{,}655172\)</td></tr>
<tr><td>3,2</td><td>0,687500</td><td>\(-1{,}20\)</td><td>instável</td>
<td>ciclo de período 2</td></tr>
</tbody>
</table>
</div>

<p>Em \(r = 3\) a derivada passa por \(-1\), e aí começa tudo. A perda de
estabilidade por \(f' = -1\) tem nome, <strong>bifurcação de duplicação de
período</strong>, e o que nasce dela é um ciclo de período 2. O ponto fixo não
some: ele continua existindo, agora instável, e a teia simplesmente deixa de
convergir para ele.</p>

<p>Repare na primeira linha da tabela. Com \(r &lt; 1\) o ponto fixo não
trivial é negativo, isto é, não está no intervalo que interessa, e a
população se extingue. É um lembrete de que achar a raiz de uma equação não é
o mesmo que achar uma solução do problema.</p>
'''

S3 = r'''
<p>O ciclo de período 2 também perde estabilidade, pelo mesmo mecanismo, e dá
lugar a um de período 4, depois 8, 16. Os intervalos entre bifurcações
sucessivas encolhem depressa, e a sequência <em>se acumula</em> num valor
finito, \(r_\infty = 3{,}569946\). Depois dele, caos.</p>

<p>Medir os pontos de bifurcação diretamente é desconfortável, porque ali o
ciclo é marginalmente estável e a convergência é lentíssima. O programa usa um
truque padrão: mede os parâmetros <strong>superestáveis</strong> \(R_n\), em
que o ciclo de período \(2^n\) contém \(x = 1/2\). Como \(f'(1/2) = 0\), a
derivada do ciclo inteiro se anula ali, e o \(R_n\) é raiz simples de uma
equação bem posta, achável por bissecção. Eles estão no meio de cada janela e
convergem para a mesma constante:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>\(n\)</th><th>período</th><th>\(R_n\)</th>
<th>intervalo</th><th>razão</th></tr></thead>
<tbody>
<tr><td>0</td><td>1</td><td>2,000000000000</td><td></td><td></td></tr>
<tr><td>1</td><td>2</td><td>3,236067977500</td><td></td><td></td></tr>
<tr><td>2</td><td>4</td><td>3,498561699328</td><td>\(2{,}6\times10^{-1}\)</td>
<td>4,708943</td></tr>
<tr><td>3</td><td>8</td><td>3,554640862769</td><td>\(5{,}6\times10^{-2}\)</td>
<td>4,680771</td></tr>
<tr><td>4</td><td>16</td><td>3,566667379856</td><td>\(1{,}2\times10^{-2}\)</td>
<td>4,662960</td></tr>
<tr><td>5</td><td>32</td><td>3,569243531637</td><td>\(2{,}6\times10^{-3}\)</td>
<td>4,668404</td></tr>
</tbody>
</table>
</div>

<p>A razão converge para</p>

\[ \delta = 4{,}669201609\ldots \]

<p>que é a <strong>constante de Feigenbaum</strong>. Repare que
\(R_1 = 3{,}2360679775\) é exatamente \(1+\sqrt5\), e vale conferir isso à
mão: a conta cabe em cinco linhas.</p>

<div class="bloco fisica">
<p class="rotulo">Por que isso é uma constante, e não um resultado</p>
<p>O número 4,6692 <strong>não depende do mapa</strong>. Qualquer mapa
unidimensional com um máximo quadrático (o seno, \(r\sen\pi x\), o mapa da
tenda arredondado, incontáveis outros) produz a mesma cascata com a mesma
razão. Mitchell Feigenbaum descobriu isso em 1975 numa calculadora de mão, e
a explicação é uma teoria de renormalização: perto da acumulação, o mapa
iterado duas vezes, reescalado, <em>é</em> o mapa original. Para a maioria
dos alunos este é o primeiro encontro com <strong>universalidade</strong>, e é
um bom lugar para encontrá-la, porque aqui ela pode ser medida numa tarde.</p>
</div>

<p>A segunda vista do componente é o <strong>diagrama de bifurcação</strong>,
com janelas de ampliação. Vale percorrê-las na ordem: o diagrama inteiro, a
cascata, um pedaço da cascata, a janela de período 3. A terceira ampliação
mostra o ponto principal, que é o diagrama se parecer consigo mesmo em toda
escala.</p>
'''

S4 = r'''
<p>"Caótico" precisa de definição quantitativa, e a definição é esta. Tome
duas órbitas separadas por \(d_0\) e acompanhe a separação. Num sistema
caótico ela cresce exponencialmente,</p>

\[ d_n \simeq d_0\,e^{\lambda n}, \]

<p>e \(\lambda\) é o <strong>expoente de Lyapunov</strong>. Para um mapa ele
sai de uma média:</p>

\[ \lambda = \lim_{N\to\infty}\frac{1}{N}
   \sum_{n=0}^{N-1}\ln\left|f'(x_n)\right|, \]

<p>que é a taxa média de esticamento ao longo da órbita. O sinal é o que
importa: \(\lambda &lt; 0\) significa que órbitas vizinhas se juntam, e o
sistema esquece a condição inicial; \(\lambda &gt; 0\) significa que ele a
amplifica.</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>\(r\)</th><th>\(\lambda\)</th><th>regime</th></tr></thead>
<tbody>
<tr><td>2,500000</td><td>\(-0{,}693147\)</td><td>periódico</td></tr>
<tr><td>3,500000</td><td>\(-0{,}872507\)</td><td>periódico (ciclo 4)</td></tr>
<tr><td>3,569946</td><td>\(+0{,}000986\)</td><td>a acumulação: \(\lambda=0\)</td></tr>
<tr><td>3,700000</td><td>\(+0{,}354775\)</td><td>caótico</td></tr>
<tr><td>3,840000</td><td>\(-0{,}044410\)</td><td>janela de período 3</td></tr>
<tr><td>3,900000</td><td>\(+0{,}495505\)</td><td>caótico</td></tr>
<tr><td>4,000000</td><td>\(+0{,}693153\)</td><td>caótico</td></tr>
</tbody>
</table>
</div>

<p>A última linha é um dos poucos casos em que o expoente sai em forma
fechada. Em \(r = 4\) o mapa é conjugado a \(x \mapsto 2x \bmod 1\), que dobra
a distância a cada passo, de modo que</p>

\[ \lambda(4) = \ln 2 = 0{,}693147\ldots \]

<p>e a medida numérica dá 0,693153, com a diferença vindo do número finito de
iterações. Note também que \(\lambda(2{,}5)\) deu exatamente \(-\ln 2\), por
um motivo completamente diferente: ali a órbita é o ponto fixo, e
\(|f'| = 1/2\).</p>

<h3>Quanto tempo a previsão dura</h3>

<p>A terceira vista do componente traz a consequência prática, que é o que o
caos custa. Oito pares de órbitas começam separados por \(10^{-14}\), que é a
precisão de um número de máquina, e a escala vertical é logarítmica, de modo
que crescimento exponencial vira reta.</p>

<p>As curvas sobem com a inclinação dada por \(\lambda\) até
<strong>saturar</strong> na largura do atrator. Dali em diante as duas órbitas
não têm mais relação nenhuma: a previsão acabou. Com \(r = 3{,}9\) e
\(\lambda = 0{,}4955\), isso leva 60 iterações.</p>

<div class="bloco alerta">
<p class="rotulo">A troca que não compensa</p>
<p>Para prever mais longe é preciso medir melhor o começo. Quanto melhor?
Ganhar <strong>uma casa decimal</strong> na condição inicial compra apenas
\(\ln 10/\lambda = 4{,}6\) iterações a mais de previsão. Medir dez vezes
melhor não prevê dez vezes mais longe: prevê um pouquinho mais longe, e o
custo da medida cresce muito mais depressa que o ganho. É essa troca ruim, e
não a falta de computador, que limita a previsão do tempo a cerca de duas
semanas.</p>
</div>

<p>Um cuidado de medida, que o programa documenta. A taxa observada num
<em>único</em> par de órbitas fica 9 % acima do expoente, porque \(\lambda\) é
uma média ao longo da órbita e trechos curtos esticam mais ou menos que ela. A
média sobre quatrocentos pares com inícios ao acaso dá 0,4929 contra
\(\lambda = 0{,}4955\). Confundir a flutuação de uma amostra com erro de conta
é um engano comum aqui.</p>
'''

S5 = r'''
<p>Depois da acumulação o diagrama não é caos uniforme: há <strong>janelas de
ordem</strong> espalhadas por toda parte, e a mais larga é a de período 3, que
começa exatamente em</p>

\[ r = 1+\sqrt8 = 3{,}828427\ldots \]

<p>O programa atravessa esse valor e mede dos dois lados:</p>

<div class="saida">
r = 3,828327&nbsp;&nbsp;&nbsp;aperiodica&nbsp;&nbsp;&nbsp;lambda = <b>+0,208864</b><br>
r = 3,828527&nbsp;&nbsp;&nbsp;periodo <b>3</b>&nbsp;&nbsp;&nbsp;lambda = <b>&minus;0,060942</b>
</div>

<p>Dois décimos de milésimo de diferença em \(r\), e o sistema passa de
caótico a periódico. Dentro da janela há uma cascata própria (3, 6, 12,
&hellip;) que termina em caos de novo, perto de 3,8495, e dentro dela outras
janelas, indefinidamente.</p>

<div class="bloco fisica">
<p class="rotulo">Período três implica caos</p>
<p>O teorema de Sarkovskii, de 1964, diz algo surpreendentemente forte: num
mapa contínuo do intervalo em si mesmo, a existência de uma órbita de período
3 implica a existência de órbitas de <strong>todos</strong> os períodos. Li e
Yorke redescobriram o resultado em 1975 num artigo cujo título,
<em>Period three implies chaos</em>, introduziu a palavra na literatura
matemática. Quando a janela de período 3 aparece, os outros ciclos todos
também estão lá; são apenas instáveis, e por isso não se veem.</p>
</div>

<h3>E a mecânica?</h3>

<p>O mapa logístico não é um sistema mecânico, e é justo perguntar o que ele
tem a ver com este curso. Duas coisas.</p>

<p>Primeiro, a cascata de duplicação e a constante \(\delta\) aparecem
<em>iguais</em> no pêndulo amortecido e forçado, que é mecânico e tem as três
dimensões necessárias. A universalidade de Feigenbaum não é uma propriedade de
parábolas: é uma propriedade de como sistemas dissipativos perdem
estabilidade, e o exercício 10.6 pede para encontrá-la ali.</p>

<p>Segundo, mapas aparecem naturalmente em mecânica quando se amostra um
sistema contínuo uma vez por período: é o que se faz com um oscilador forçado,
tomando \((x,\dot{x})\) a cada ciclo da força. O fluxo contínuo em três
dimensões vira um mapa em duas, e o módulo inteiro passa a valer. O lado
<em>conservativo</em> dessa construção, com toros invariantes e o teorema KAM,
é a unidade final de <strong>Mecânica Clássica III</strong>, onde ela tem o
espaço que merece.</p>
'''

S6 = r'''
<div class="cartoes">
  <a class="cartao" href="codigo/caos.py">
    <span class="numero">Programa</span>
    <h3>caos.py</h3>
    <p>Decide estabilidade por \(|f'|&lt;1\), localiza as bifurcações pelos
    parâmetros superestáveis, mede Feigenbaum e o expoente de Lyapunov, e
    mostra a separação exponencial de duas órbitas vizinhas.</p>
  </a>
</div>

<p><strong>O que ele imprime, e o que conferir.</strong></p>

<ul>
<li>A previsão de \(|f'| &lt; 1\) bate com o que a iteração faz, nos cinco
casos.</li>
<li>As bifurcações estão em \(r = 3\) e \(r = 1+\sqrt6 = 3{,}449490\),
conferidas por iteração dos dois lados.</li>
<li>A razão entre intervalos sucessivos vai a 4,6684 na quinta duplicação,
contra \(\delta = 4{,}669202\).</li>
<li>\(\lambda(4) = 0{,}693153\) contra \(\ln2 = 0{,}693147\).</li>
<li>A média da taxa de separação sobre 400 pares dá 0,4929 contra
\(\lambda = 0{,}4955\), ao passo que um par isolado erra 9 %.</li>
<li>A janela de período 3 começa entre 3,828327 e 3,828527, contendo
\(1+\sqrt8\).</li>
</ul>

<div class="bloco ex">
<p><strong>Para mexer.</strong> Troque \(rx(1-x)\) por \(r\sen(\pi x)\) e
refaça a medida de Feigenbaum: os \(R_n\) serão outros, e a razão será a
mesma 4,6692. É a maneira mais barata de ver universalidade com as próprias
mãos. Depois tente \(x \mapsto r x(1-x^2)\), cujo máximo também é quadrático,
e por fim um mapa com máximo <em>quártico</em>, que dá outra constante: a
universalidade tem classes, e a classe é fixada pela ordem do máximo.</p>
</div>
'''

SECOES = [
    ('Do que o caos precisa, e como baratear', S1),
    ('A teia, os pontos fixos e a primeira duplicação', S2),
    ('A cascata e a constante de Feigenbaum', S3),
    ('O expoente de Lyapunov, e o preço da previsão', S4),
    ('Ordem dentro do caos, e a volta à mecânica', S5),
    ('No Spyder', S6),
]

SECOES.append(('Exercícios propostos', exercicios.bloco(LISTA)))


def main():
    titulos = [t for t, _ in SECOES]
    escreve('aula10.html', secoes_html(SECOES), secoes=titulos,
            subtitulo='Caos não é desordem nem ruído: é sensibilidade '
                      'exponencial às condições iniciais num sistema '
                      'inteiramente determinístico. Uma linha de conta por '
                      'iteração basta para produzi-lo, e para medir quanto '
                      'tempo uma previsão dura.')


if __name__ == '__main__':
    main()
