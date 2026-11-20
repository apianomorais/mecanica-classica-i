# -*- coding: utf-8 -*-
"""Módulo 1: vetores, matrizes e cálculo vetorial."""
from molde import escreve, secoes_html
import exercicios
from lista_aula01 import LISTA

S1 = r'''
<p>Todo mundo chega a esta disciplina sabendo que vetor é "um segmento
orientado, com módulo, direção e sentido". Essa definição serve para desenhar,
e não serve para quase mais nada. Ela não diz o que fazer quando alguém
pergunta se a corrente elétrica é vetor, se a velocidade angular é vetor, ou
se o trio formado por duas coordenadas e uma temperatura é vetor.</p>

<p>A definição que a física usa é outra, e começa com uma pergunta diferente:
o que acontece com os números quando se gira o sistema de coordenadas?</p>

<h3>A rotação, primeiro</h3>

<p>Girar os eixos de um ângulo \(\varphi\) em torno de \(z\) leva as
coordenadas de um ponto de \((x,y,z)\) para</p>

\[ \begin{pmatrix} x' \\ y' \\ z' \end{pmatrix}
   =
   \begin{pmatrix}
     \cos\varphi & \sen\varphi & 0 \\
     -\sen\varphi & \cos\varphi & 0 \\
     0 & 0 & 1
   \end{pmatrix}
   \begin{pmatrix} x \\ y \\ z \end{pmatrix}, \]

<p>ou, em notação compacta, \(x'_i = R_{ij}x_j\), com a soma sobre o índice
repetido subentendida.</p>

<p>A matriz \(R\) tem duas propriedades que a caracterizam:</p>

\[ R^{\mathsf T}R = \mathbb{1}, \qquad \det R = +1. \]

<p>A primeira é a <strong>ortogonalidade</strong>, e é ela que garante que
distâncias não mudem ao girar. A segunda separa as rotações das reflexões:
uma matriz ortogonal com determinante \(-1\) também preserva distâncias, mas
troca a mão direita pela esquerda, e nenhum movimento rígido faz isso.</p>

<div class="bloco def">
<span class="rotulo">A definição de vetor</span>
<p>Um trio de números \((A_1,A_2,A_3)\) é um <strong>vetor</strong> quando,
sob rotação dos eixos, as suas componentes se transformam exatamente como as
coordenadas:</p>
\[ A'_i = R_{ij}A_j. \]
<p>Um único número que não muda sob rotação, \(s' = s\), é um
<strong>escalar</strong>. Nove números com duas leis de transformação,
\(T'_{ij} = R_{ik}R_{jl}T_{kl}\), formam um <strong>tensor</strong> de segunda
ordem, que é o assunto da <a href="https://apianomorais.github.io/mecanica-classica-iii/">Mecânica Clássica III</a>.</p>
</div>

<h3>Por que essa definição, e não a outra</h3>

<p>A exigência parece burocrática, e é a coisa mais útil do módulo. Se os dois
lados de uma equação são vetores, a equação vale em qualquer sistema de
coordenadas girado, sem refazer conta nenhuma. É o que permite escrever
\(\vet{F} = m\vet{a}\) uma vez só e usar em qualquer orientação de eixos. Uma
equação escrita componente por componente, sem essa garantia, pode ser
verdadeira num sistema e falsa no vizinho.</p>

<div class="destaque">
<p><strong>Exemplo trabalhado: um trio que não é vetor.</strong> Tome um ponto
do plano, em \((3, 4, 0)\) metros, e a temperatura ali medida,
\(T = 25\ \mathrm{K}\). Junte os três números no trio \((3, 4, 25)\) e gire os
eixos de 40° em torno de \(x\).</p>

<p><strong>O vetor posição</strong> vai para</p>

\[ (3{,}000;\ 3{,}064;\ 2{,}571)\ \mathrm{m}, \]

<p>com as três componentes ainda em metros e com o módulo intacto, 5,000 m.</p>

<p><strong>O trio</strong>, tratado como se fosse vetor, vai para</p>

\[ (3{,}000;\ -13{,}006;\ 21{,}722), \]

<p>e a segunda componente vale \(4\cos 40^\circ - 25\sen 40^\circ\), isto é,
uma soma de metros com kelvin. O resultado não é grandeza nenhuma.</p>

<p><strong>A moral.</strong> Não existe "a transformação correta do trio",
porque o trio não é um objeto geométrico: é uma lista. O que se transforma é a
posição, que é vetor, e o que fica quieto é a temperatura, que é escalar. Ter
três números não basta.</p>
</div>

<div class="bloco alerta">
<span class="rotulo">E os que quase são vetores</span>
<p>O produto vetorial de dois vetores transforma-se como vetor sob rotação,
mas não troca de sinal sob reflexão, ao contrário de um vetor de verdade. Esses
objetos são chamados de <strong>pseudovetores</strong> ou vetores axiais, e a
lista inclui o torque, o momento angular, a velocidade angular e o campo
magnético. A distinção só aparece quando há reflexão no problema, e é por isso
que ela passa despercebida em quase todo o curso. Em física de partículas, onde
há processos que distinguem esquerda de direita, ela se torna central.</p>
</div>
'''

S2 = r'''
<p>Há duas maneiras de multiplicar vetores, e cada uma responde a uma pergunta
geométrica diferente.</p>

<h3>O produto escalar: quanto um avança na direção do outro</h3>

\[ \vet{a}\cdot\vet{b} = a_ib_i = ab\cos\theta. \]

<p>O resultado é um escalar, no sentido técnico da seção 1: o mesmo número em
qualquer sistema girado. Ele zera quando os vetores são perpendiculares, e é
máximo quando são paralelos.</p>

<p>No curso, ele aparece no trabalho, \(W = \vet{F}\cdot\vet{d}\), onde mede
exatamente a parte da força que acompanha o deslocamento, e na energia
cinética, \(T = \frac12m\,\vet{v}\cdot\vet{v}\).</p>

<h3>O produto vetorial: a área que os dois cercam</h3>

\[ \vet{a}\cruz\vet{b} = \varepsilon_{ijk}a_jb_k\vers{e}_i
   = \begin{vmatrix}
       \vers{x} & \vers{y} & \vers{z} \\
       a_1 & a_2 & a_3 \\
       b_1 & b_2 & b_3
     \end{vmatrix}, \]

<p>O símbolo \(\varepsilon_{ijk}\) é o <a href="https://pt.wikipedia.org/wiki/S%C3%ADmbolo_de_Levi-Civita">símbolo de Levi-Civita</a>, que vale \(+1\) para índices em ordem cíclica, \(-1\) para a ordem trocada e zero quando há índice repetido.</p>

<p>com módulo \(ab\sen\theta\), que é a área do paralelogramo formado pelos
dois, e direção perpendicular ao plano deles. Ele zera quando os vetores são
paralelos, isto é, exatamente onde o escalar é máximo.</p>

<p>No curso, ele aparece no torque, \(\vet{\tau} = \vet{r}\cruz\vet{F}\), e no
momento angular, \(\vet{L} = \vet{r}\cruz\vet{p}\), os dois assuntos do módulo
13 e de toda a Mecânica Clássica II.</p>

<h3>Os produtos triplos</h3>

<p><strong>O misto</strong>, \(\vet{a}\cdot\left(\vet{b}\cruz\vet{c}\right)\),
é o volume do paralelepípedo construído sobre os três, com sinal positivo se
eles formam uma mão direita. Ele é igual ao determinante da matriz que tem os
três como linhas, e por isso não muda sob permutação cíclica.</p>

<p><strong>O duplo vetorial</strong> obedece à identidade mais útil da
disciplina, conhecida pelo apelido BAC-CAB:</p>

\[ \vet{a}\cruz\left(\vet{b}\cruz\vet{c}\right)
   = \vet{b}\left(\vet{a}\cdot\vet{c}\right)
   - \vet{c}\left(\vet{a}\cdot\vet{b}\right). \]

<div class="bloco fisica">
<span class="rotulo">Onde o BAC-CAB paga o aluguel</span>
<p>A aceleração centrípeta de um ponto que gira com velocidade angular
\(\vet{\omega}\) é \(\vet{\omega}\cruz\left(\vet{\omega}\cruz\vet{r}\right)\).
Aplicando a identidade,</p>
\[ \vet{\omega}\cruz\left(\vet{\omega}\cruz\vet{r}\right)
   = \vet{\omega}\left(\vet{\omega}\cdot\vet{r}\right) - \omega^2\vet{r}, \]
<p>e, para \(\vet{r}\) perpendicular ao eixo, sobra \(-\omega^2\vet{r}\): o
resultado aponta para dentro e tem módulo \(\omega^2r\), que é a fórmula
decorada no ensino médio, agora deduzida. O exercício 1.4 faz a conta
completa.</p>
</div>
'''

S3 = r'''
<p>As três vistas do simulador tratam os três pontos deste módulo que nenhuma
fórmula resolve sozinha.</p>

<div data-widget="vetores"></div>

<p>Na primeira, gire os eixos e repare no que acontece: a seta verde não se
mexe, os números mudam, e o módulo não muda nunca. É a seção 1 inteira numa
figura.</p>

<p>Na segunda, leve o ângulo de 0° a 90° e compare os dois produtos. Onde um é
máximo o outro é nulo, e a área sombreada é literalmente o módulo do produto
vetorial.</p>

<p>Na terceira, mova o ponto pela paisagem e confira duas afirmações: o
gradiente é sempre perpendicular à curva de nível, e ele aponta para a
<em>subida</em>, de modo que a força, \(\vet{F} = -\nabla U\), aponta para o
fundo do poço.</p>
'''

S4 = r'''
<p>A segunda metade do módulo troca vetores constantes por <em>campos</em>:
funções que atribuem um número ou um vetor a cada ponto do espaço. A
temperatura numa sala é um campo escalar; a velocidade do ar na mesma sala é
um campo vetorial. Há três derivadas que interessam, e vale entender o que cada
uma mede antes de decorar a fórmula.</p>

<h3>Gradiente: para onde cresce</h3>

\[ \nabla f = \pder{f}{x}\vers{x} + \pder{f}{y}\vers{y}
   + \pder{f}{z}\vers{z}. \]

<p>O gradiente de um campo escalar é um campo vetorial que aponta na direção
de crescimento mais rápido, com módulo igual à taxa de crescimento nessa
direção. Duas consequências imediatas: ele é perpendicular às superfícies de
nível, e ele se anula onde \(f\) tem máximo, mínimo ou sela.</p>

<p>A variação de \(f\) ao andar um deslocamento \(d\vet{\ell}\) é</p>

\[ df = \nabla f\cdot d\vet{\ell}, \]

<p>e essa única equação contém tudo o que há para saber sobre o gradiente.</p>

<h3>Divergente: o quanto brota</h3>

\[ \divg{\vet{A}} = \pder{A_x}{x} + \pder{A_y}{y} + \pder{A_z}{z}. \]

<p>O divergente mede o fluxo que sai de um volume pequeno, por unidade de
volume. Onde ele é positivo há fonte; onde é negativo há sorvedouro; onde é
nulo, tudo o que entra sai. Num fluido incompressível,
\(\divg{\vet{v}} = 0\) em toda parte, e o módulo 2 de Fenômenos de Transporte
vive dessa equação.</p>

<h3>Rotacional: o quanto gira</h3>

\[ \rot{\vet{A}} =
   \begin{vmatrix}
     \vers{x} & \vers{y} & \vers{z} \\
     \partial_x & \partial_y & \partial_z \\
     A_x & A_y & A_z
   \end{vmatrix}. \]

<p>O rotacional mede a circulação em torno de um laço pequeno, por unidade de
área. A imagem clássica é a de uma rodinha de pás mergulhada no campo: se ela
gira, o rotacional não é nulo, e o eixo de giro dá a direção.</p>

<div class="bloco def">
<span class="rotulo">Duas identidades que valem sempre</span>
\[ \rot{\left(\nabla f\right)} = 0,
   \qquad
   \divg{\left(\rot{\vet{A}}\right)} = 0. \]
<p>A primeira diz que gradiente não gira; a segunda, que rotacional não brota.
As duas saem de as derivadas parciais comutarem, e são verificadas
numericamente pelo programa do módulo. Elas são a razão de, no
eletromagnetismo, existirem potenciais: \(\divg{\vet{B}} = 0\) permite escrever
\(\vet{B} = \rot{\vet{A}}\), e \(\rot{\vet{E}} = 0\), na eletrostática, permite
escrever \(\vet{E} = -\nabla V\).</p>
</div>
'''

S5 = r'''
<p>Aqui o cálculo vetorial deixa de ser ferramenta e vira física. A pergunta é
antiga: dada uma força, existe uma energia potencial?</p>

<p>Três afirmações são equivalentes, e a equivalência é o resultado central
desta seção:</p>

<div class="bloco def">
<span class="rotulo">As três caras de uma força conservativa</span>
<ol>
<li>O trabalho de \(\vet{F}\) entre dois pontos não depende do caminho;</li>
<li>a circulação \(\oint\vet{F}\cdot d\vet{\ell}\) é nula em todo caminho
fechado;</li>
<li>\(\rot{\vet{F}} = 0\) em toda a região, e então existe \(U\) com
\(\vet{F} = -\nabla U\).</li>
</ol>
</div>

<p>A ponte entre a segunda e a terceira é o <strong><a href="https://en.wikipedia.org/wiki/Sir_George_Stokes,_1st_Baronet">teorema de Stokes</a></strong>,
que troca uma integral de linha por uma de superfície:</p>

\[ \oint_{\partial S}\vet{F}\cdot d\vet{\ell}
   = \int_S\left(\rot{\vet{F}}\right)\cdot d\vet{a}. \]

<div class="destaque">
<p><strong>Exemplo trabalhado: um campo que não é conservativo.</strong> Tome
\(\vet{F} = -y\,\vers{x} + x\,\vers{y}\), que gira em torno da origem.</p>

<p><strong>O rotacional</strong> sai direto do determinante:</p>

\[ \rot{\vet{F}} = \left(\pder{F_y}{x}-\pder{F_x}{y}\right)\vers{z}
   = \left(1-(-1)\right)\vers{z} = 2\vers{z}. \]

<p><strong>A circulação</strong>, calculada pelo programa em três caminhos
fechados diferentes:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>caminho</th><th>área cercada</th>
<th>\(\oint\vet{F}\cdot d\vet{\ell}\)</th><th>razão</th></tr></thead>
<tbody>
<tr><td>círculo de raio 1</td><td>\(\pi\)</td><td>6,2832</td><td>2,000</td></tr>
<tr><td>círculo de raio 2, deslocado</td><td>\(4\pi\)</td><td>25,1327</td>
    <td>2,000</td></tr>
<tr><td>quadrado de lado 1</td><td>1</td><td>2,0000</td><td>2,000</td></tr>
</tbody>
</table>
</div>

<p><strong>A leitura.</strong> A circulação vale sempre duas vezes a área
cercada, e não depende da forma do caminho nem de onde ele está. É exatamente o
que Stokes prevê, porque \(\rot{\vet{F}} = 2\vers{z}\) é constante: a integral
de superfície vira \(2\times\text{área}\).</p>

<p><strong>E o que isso significa fisicamente.</strong> Uma partícula levada
por esse campo ao longo de um círculo volta ao ponto de partida tendo recebido
energia. Não existe \(U\) para ele, e um campo assim não pode ser uma força
fundamental conservativa. Forças de atrito e forças magnéticas sobre correntes
têm esse caráter, e é por isso que elas não entram na conservação de energia
mecânica.</p>
</div>

<p>O módulo 4 retoma esse resultado do outro lado, construindo \(U\) a partir
de \(\vet{F}\) e lendo o movimento inteiro no gráfico de \(U(x)\).</p>
'''

S6 = r'''
<div class="cartoes">
  <a class="cartao" href="codigo/vetores.py">
    <span class="numero">Programa</span>
    <h3>vetores.py</h3>
    <p>Põe à prova, por medida, tudo o que este módulo afirma: a ortogonalidade
    da rotação, a invariância do módulo e do produto escalar, a geometria dos
    dois produtos, as identidades do cálculo vetorial e o teste da força
    conservativa.</p>
  </a>
</div>

<p><strong>O que ele imprime, e o que conferir.</strong></p>

<ul>
<li>\(R^{\mathsf T}R - \mathbb{1}\) e \(\det R - 1\) dão zero de máquina, e
trocar o sinal de uma coluna leva o determinante a \(-1\), que é a assinatura
de uma reflexão.</li>
<li>Rotação preserva \(|\vet{v}|\) e \(\vet{a}\cdot\vet{b}\) em \(10^{-16}\),
enquanto o trio com a temperatura produz uma componente que soma metros com
kelvin.</li>
<li>\(\left|\vet{a}\cruz\vet{b}\right| = ab\sen\theta\) e o produto misto
coincide com o determinante, os dois em \(10^{-15}\).</li>
<li>A identidade BAC-CAB fecha <em>exatamente</em>, em zero de máquina, porque
ali não há derivada nenhuma.</li>
<li>\(\rot{\left(\nabla f\right)}\) e \(\divg{\left(\rot{\vet{A}}\right)}\)
dão zero até o erro das diferenças finitas, e não zero de máquina.</li>
<li>A circulação do campo giratório dá duas vezes a área em todos os caminhos
testados.</li>
</ul>

<div class="bloco alerta">
<span class="rotulo">Uma distinção que vale para o curso inteiro</span>
<p>Repare na diferença entre os dois tipos de zero. O BAC-CAB sai em
\(10^{-16}\), porque é identidade algébrica e o computador só faz somas e
multiplicações. Já \(\rot{\left(\nabla f\right)}\) sai em \(10^{-7}\), porque
ali há duas derivadas numéricas encadeadas, e cada diferença central divide o
arredondamento pelo passo. Com \(h = 10^{-4}\), duas derivadas carregam
\(10^{-16}/h^2 = 10^{-8}\) de ruído.</p>
<p>Quem não souber distinguir esses dois zeros vai passar a vida achando que
encontrou um erro quando encontrou apenas aritmética de ponto flutuante. E,
pior, vai deixar passar erros de verdade escondidos atrás de um
"\(10^{-7}\) é praticamente zero".</p>
</div>
'''

SECOES = [
    ('O que faz de um trio de números um vetor', S1),
    ('Os dois produtos, e o que eles medem', S2),
    ('Mexendo com vetores', S3),
    ('Campos e as três derivadas', S4),
    ('O teste da força conservativa', S5),
    ('No Spyder', S6),
]

SECOES.append(('Exercícios propostos', exercicios.bloco(LISTA)))


def main():
    titulos = [t for t, _ in SECOES]
    escreve('aula01.html', secoes_html(SECOES), secoes=titulos,
            subtitulo='A definição de vetor que a física usa não é a do '
                      'segmento orientado: é a lei de transformação. Deste '
                      'módulo saem as ferramentas que o curso inteiro usa, e '
                      'uma delas, o teste do rotacional, decide se existe '
                      'energia potencial.')


if __name__ == '__main__':
    main()
