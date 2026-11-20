# -*- coding: utf-8 -*-
"""Módulo 3: forças que dependem do tempo, da velocidade e da posição.

A resistência do ar é tratada dos dois lados: analiticamente, nos casos em
que a solução fechada existe, e numericamente, no caso em que ela não
existe. A fronteira entre os dois é o assunto da seção 3.
"""
from molde import escreve, secoes_html
import exercicios
from lista_aula03 import LISTA

S1 = r'''
<p>A segunda lei não é uma fórmula para calcular força. Lida com cuidado, ela
é uma <em>equação diferencial</em>: dada a força, ela determina a aceleração,
que é a segunda derivada da posição, e o que se quer é a posição em função do
tempo. Escrita assim fica claro o que há para fazer:</p>

\[ m\dder{\vet{r}}{t} = \vet{F}\left(\vet{r},\dot{\vet{r}},t\right). \]

<p>O lado direito mostra os três tipos de dependência que este módulo trata.
A força pode depender do <strong>tempo</strong>, como a de um motor que é
ligado e desligado; da <strong>velocidade</strong>, como o arrasto do ar; e da
<strong>posição</strong>, como a de uma mola ou a gravitação.</p>

<div class="bloco def">
<span class="rotulo">O que é resolver</span>
<p>Resolver a equação de movimento é achar \(\vet{r}(t)\) para todo \(t\),
dadas a posição e a velocidade num instante. Essas duas condições iniciais são
necessárias porque a equação é de segunda ordem, e são <em>suficientes</em>:
nada mais sobre o passado do sistema importa. É essa propriedade que faz da
mecânica newtoniana uma teoria determinista.</p>
</div>

<h3>As três ferramentas de integração</h3>

<p><strong>Força só do tempo.</strong> Duas integrações diretas,
\(v(t) = v_0 + \frac1m\int F\,dt\), e nenhuma dificuldade conceitual.</p>

<p><strong>Força só da velocidade.</strong> Separa-se e integra-se:</p>

\[ m\der{v}{t} = F(v)
   \;\Longrightarrow\;
   t = m\int_{v_0}^{v}\frac{dv'}{F(v')}. \]

<p>Repare no que saiu: \(t(v)\), e não \(v(t)\). Para inverter é preciso ter
sorte com a integral, e a seção 3 mostra os casos em que se tem.</p>

<p><strong>Força só da posição.</strong> O truque é multiplicar por \(v\) e
reconhecer a derivada da energia cinética, o que leva à conservação de energia
e a uma quadratura. O módulo 4 faz isso com cuidado.</p>

<p>Resta o caso misto, em que a força depende da velocidade <em>e</em> o
movimento é bidimensional. É onde mora a resistência do ar de verdade, e é
onde a fórmula fechada acaba.</p>
'''

S2 = r'''
<p>Antes de integrar, vale saber quanta força o ar faz. Para um corpo que se
move num fluido, há dois regimes.</p>

<p><strong>Arrasto linear</strong>, \(F = -bv\), vale quando o escoamento é
<a href="https://pt.wikipedia.org/wiki/Escoamento_laminar">laminar</a>, isto é, para objetos pequenos ou velocidades baixas. É o caso de uma
gota de névoa, de uma bolinha caindo em óleo ou de uma partícula de poeira no
ar. O <a href="https://pt.wikipedia.org/wiki/N%C3%BAmero_de_Reynolds">número de Reynolds</a> é pequeno, e a viscosidade domina.</p>

<p><strong>Arrasto quadrático</strong>, \(F = -\frac12\rho C_DAv^2\), vale
quando o escoamento é turbulento, que é o caso de quase tudo que interessa no
ar: uma bola, um ciclista, um carro, um paraquedista. A força vem da inércia do
ar empurrado para os lados, e não da viscosidade.</p>

<p>Por comodidade, escrevemos a aceleração do arrasto quadrático como</p>

\[ \vet{a}_{\text{arr}} = -k\left|\vet{v}\right|\vet{v},
   \qquad k = \frac{\rho C_DA}{2m}, \]

<p>com \(k\) medido em inverso de metro, e a do arrasto linear como</p>

\[ \vet{a}_{\text{arr}} = -\frac{\vet{v}}{\tau},
   \qquad \tau = \frac{m}{b}, \]

<p>com \(\tau\) em segundos. Nos dois casos o arrasto aponta contra a
velocidade, e é essa exigência que vai acoplar as componentes no caso
quadrático.</p>

<h3>Velocidade terminal</h3>

<p>Para a queda vertical há um resultado simples e útil nos dois regimes.
Quando o arrasto iguala o peso, a aceleração zera e a velocidade para de
crescer:</p>

\[ v_t = g\tau \quad\text{(linear)},
   \qquad
   v_t = \sqrt{\frac{g}{k}} \quad\text{(quadrático)}. \]

<p>Com \(k = 0{,}004\ \mathrm{m^{-1}}\), que é o valor usado no simulador e no
programa deste módulo, isso dá \(v_t = 49{,}5\ \mathrm{m/s}\), ou 178 km/h, da
ordem do que se mede num paraquedista de bruços, cerca de 54 m/s. Uma bola de
tênis, bem mais leve para o seu tamanho, tem \(k\) quatro vezes maior e cai a
23 m/s; uma gota de chuva de 2 mm tem \(k = 0{,}21\ \mathrm{m^{-1}}\) e desce a
apenas 6,8 m/s, que é a razão de a chuva não machucar. O exercício 3.1 monta
essa tabela.</p>

<div class="bloco alerta">
<span class="rotulo">Onde o acoplamento mora</span>
<p>Sem ar, o movimento horizontal e o vertical são independentes, e é isso que
permite tratar cada um por vez. Com arrasto <em>linear</em> eles continuam
independentes, porque a força horizontal só menciona \(v_x\) e a vertical só
menciona \(v_y\). Com arrasto <em>quadrático</em>,
\(\left|\vet{v}\right| = \sqrt{v_x^2+v_y^2}\) aparece nas duas equações, de
modo que o que acontece na vertical muda a desaceleração horizontal e
vice-versa.</p>
<p>Guarde essa distinção: ela é exatamente a fronteira entre o que a próxima
seção resolve no papel e o que só se resolve no computador.</p>
</div>
'''

S3 = r'''
<p>Boa parte do que se diz sobre resistência do ar em sala é que "não tem
solução analítica". Isso é falso na maioria dos casos e verdadeiro no caso que
mais interessa, e vale separar os dois com precisão.</p>

<h3>Arrasto linear, uma dimensão</h3>

<p>A equação da queda é</p>

\[ \der{v}{t} = -g - \frac{v}{\tau}, \]

<p>que é linear e separável. Agrupando,</p>

\[ \der{v}{t} = -\frac{v + v_t}{\tau},
   \qquad v_t = g\tau, \]

<p>e integrando de \(v_0\) a \(v\),</p>

\[ \boxed{\;v(t) = \left(v_0+v_t\right)e^{-t/\tau} - v_t,\;} \]

\[ y(t) = \left(v_0+v_t\right)\tau\left(1-e^{-t/\tau}\right) - v_tt. \]

<p>A leitura é direta: a velocidade tende exponencialmente a \(-v_t\), com
constante de tempo \(\tau\), e qualquer memória da velocidade inicial some em
alguns \(\tau\). Depois de \(3\tau\) a velocidade já está a 5 % da terminal.</p>

<h3>Arrasto linear, duas dimensões: ainda exato</h3>

<p>Com arrasto linear, as duas equações são</p>

\[ \der{v_x}{t} = -\frac{v_x}{\tau},
   \qquad
   \der{v_y}{t} = -g - \frac{v_y}{\tau}, \]

<p>e nenhuma delas menciona a outra componente. São dois problemas de uma
dimensão, resolvidos separadamente, e o resultado é exato:</p>

\[ x(t) = v_{x0}\tau\left(1-e^{-t/\tau}\right),
   \qquad
   y(t) = \left(v_{y0}+v_t\right)\tau\left(1-e^{-t/\tau}\right) - v_tt. \]

<div class="bloco fisica">
<span class="rotulo">A assíntota vertical</span>
<p>Repare no que a primeira fórmula diz quando \(t\to\infty\):</p>
\[ x_\infty = v_{x0}\tau. \]
<p>O alcance horizontal é <em>limitado</em>, por mais tempo que o projétil
fique no ar. Com \(v_{x0} = 35\ \mathrm{m/s}\) e \(\tau = 3\ \mathrm{s}\), ele
nunca passa de 105 m na horizontal, e a trajetória termina caindo na vertical.
Essa assíntota não existe sem arrasto, e é a assinatura mais visível da
resistência do ar numa trajetória.</p>
</div>

<h3>Arrasto quadrático, uma dimensão</h3>

<p>Aqui o módulo da velocidade é o próprio \(|v|\), de modo que não há
acoplamento, e a equação continua separável. O sinal do arrasto depende do
sentido do movimento, e por isso a subida e a descida dão funções
diferentes.</p>

<p><strong>Subindo</strong>, gravidade e arrasto apontam os dois para baixo:</p>

\[ \der{v}{t} = -g - kv^2
   \;\Longrightarrow\;
   v(t) = v_t\tan\!\left(\theta_0 - \frac{gt}{v_t}\right),
   \qquad \theta_0 = \arctan\frac{v_0}{v_t}. \]

<p>Dessa solução saem dois resultados fechados e muito úteis:</p>

\[ t_{\text{subida}} = \frac{v_t}{g}\arctan\frac{v_0}{v_t},
   \qquad
   h_{\max} = \frac{v_t^2}{2g}\ln\!\left(1+\frac{v_0^2}{v_t^2}\right). \]

<p><strong>Caindo</strong> a partir do repouso, os dois se opõem:</p>

\[ \der{v}{t} = -g + kv^2
   \;\Longrightarrow\;
   v(t) = v_t\tanh\frac{gt}{v_t},
   \qquad
   y(t) = \frac{v_t^2}{g}\ln\cosh\frac{gt}{v_t}. \]

<div class="destaque">
<p><strong>Exemplo trabalhado: subir custa menos tempo do que descer.</strong>
Uma bola é atirada para cima com \(v_0 = 40\ \mathrm{m/s}\), com
\(k = 0{,}004\ \mathrm{m^{-1}}\), de modo que \(v_t = 49{,}52\ \mathrm{m/s}\).
As fórmulas acima dão</p>

\[ t_{\text{subida}} = \frac{49{,}52}{9{,}81}
   \arctan\frac{40}{49{,}52} = 3{,}430\ \mathrm{s}, \]

\[ h_{\max} = \frac{49{,}52^2}{2\times9{,}81}
   \ln\!\left(1+\frac{40^2}{49{,}52^2}\right) = 62{,}78\ \mathrm{m}. \]

<p>Sem ar, os mesmos 40 m/s dariam 4,077 s e 81,55 m. O ar tira
<strong>23 %</strong> da altura e encurta a subida em 16 %.</p>

<p><strong>E a descida?</strong> Caindo dos 62,78 m, a bola chega ao chão com
menos velocidade do que saiu, e leva <em>mais</em> tempo do que levou para
subir. A razão é a mesma nos dois casos: na subida o arrasto trabalha a favor
da gravidade e tudo acontece mais depressa; na descida ele trabalha contra, e
tudo acontece mais devagar. A simetria entre subida e descida, que todo mundo
aprende no ensino médio, é uma consequência da ausência de ar, e não um fato
geral.</p>
</div>

<h3>Arrasto quadrático, duas dimensões: a fronteira</h3>

<p>Agora o acoplamento aparece:</p>

\[ \der{v_x}{t} = -k\sqrt{v_x^2+v_y^2}\;v_x,
   \qquad
   \der{v_y}{t} = -g - k\sqrt{v_x^2+v_y^2}\;v_y. \]

<p>A raiz quadrada amarra as duas equações, e não existe solução em funções
elementares. Não é falta de esforço: é uma propriedade do sistema.</p>

<p>A tentação natural é tratar cada componente como se fosse um problema
unidimensional, usando \(|v_x|v_x\) e \(|v_y|v_y\) separadamente. Vale medir o
estrago. O programa <code>arrasto_analitico.py</code> integra os dois sistemas
com \(v_{x0}=v_{y0}=35\ \mathrm{m/s}\) e \(k = 0{,}004\ \mathrm{m^{-1}}\):</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>em \(t = 3\) s</th><th>acoplado (correto)</th>
<th>"separado"</th><th>diferença</th></tr></thead>
<tbody>
<tr><td>\(x\)</td><td>84,53 m</td><td>87,66 m</td><td>3,13 m</td></tr>
<tr><td>\(y\)</td><td>45,56 m</td><td>50,59 m</td><td>5,03 m</td></tr>
</tbody>
</table>
</div>

<p>Metros de diferença em três segundos. Separar não é uma aproximação ruim: é
outra física.</p>

<div class="bloco def">
<span class="rotulo">O mapa do que se resolve</span>
<div class="tabela-rolavel">
<table>
<thead><tr><th></th><th>uma dimensão</th><th>duas dimensões</th></tr></thead>
<tbody>
<tr><td><strong>linear</strong></td>
    <td>exponencial</td>
    <td>exponencial, exato</td></tr>
<tr><td><strong>quadrático</strong></td>
    <td>tangente e tangente hiperbólica</td>
    <td><strong>sem solução fechada</strong></td></tr>
</tbody>
</table>
</div>
<p>Só uma casa das quatro resiste, e é justamente a do caso realista: bola,
projétil, atleta, qualquer coisa que voe no ar. É por ela que existe o resto
deste módulo.</p>
</div>
'''

S4 = r'''
<p>O método numérico mais simples que existe nasce de uma ideia de uma linha:
se eu sei onde estou e sei a derivada, sei aproximadamente onde estarei daqui a
pouco.</p>

<p>Para uma equação de primeira ordem \(\dot y = f(y,t)\), isso se escreve</p>

\[ y_{n+1} = y_n + \Delta t\,f(y_n,t_n), \]

<p>que é o <strong><a href="https://pt.wikipedia.org/wiki/M%C3%A9todo_de_Euler">método de Euler</a></strong>, publicado por <a href="https://pt.wikipedia.org/wiki/Leonhard_Euler">Leonhard Euler</a> em 1768. Geometricamente, ele troca a curva
verdadeira pela reta tangente a ela no ponto em que estamos, e anda sobre essa
reta durante \(\Delta t\). Como a curva entorta dentro do passo e a tangente
não, cada passo deixa um resto, e os restos se acumulam.</p>

<h3>O que fazer com uma equação de segunda ordem</h3>

<p>A equação de movimento é de segunda ordem, e o método acima é para
primeira. A ponte é um truque que vale a pena guardar para o resto do curso:
toda equação de ordem \(n\) vira um <em>sistema</em> de \(n\) equações de
primeira ordem, bastando dar nome às derivadas.</p>

<p>Para o projétil em duas dimensões, chame de estado o vetor de quatro
números</p>

\[ \vet{u} = \left(x,\;y,\;v_x,\;v_y\right), \]

<p>e escreva a derivada de cada um deles:</p>

\[ \der{}{t}
   \begin{pmatrix} x \\ y \\ v_x \\ v_y \end{pmatrix}
   =
   \begin{pmatrix}
     v_x \\
     v_y \\
     -k\left|\vet{v}\right|v_x \\
     -g - k\left|\vet{v}\right|v_y
   \end{pmatrix},
   \qquad \left|\vet{v}\right| = \sqrt{v_x^2+v_y^2}. \]

<p>São quatro equações, todas de primeira ordem, todas acopladas. E o passo de
Euler é o mesmo de antes, aplicado ao vetor inteiro:</p>

\[ \vet{u}_{n+1} = \vet{u}_n + \Delta t\,\vet{f}\!\left(\vet{u}_n\right). \]

<div class="bloco def">
<span class="rotulo">A ideia que mais rende neste curso</span>
<p>Nada no passo de Euler sabe que são quatro equações. Trocar quatro por
quarenta, ou por quatro mil, não muda uma linha do método: muda o tamanho do
vetor. É por isso que o mesmo programa de dez linhas resolve o projétil deste
módulo, o oscilador do módulo 7, o pêndulo do módulo 9 e o problema de dois
corpos do módulo 12.</p>
</div>

<h3>Em Python, honestamente</h3>

<p>A tradução do sistema para código é quase literal, e é esse o ponto:</p>

<pre><code>def derivada(u, k):
    x, y, vx, vy = u
    v = np.hypot(vx, vy)
    return np.array([vx, vy, -k*v*vx, -g - k*v*vy])

def passo_euler(u, dt, k):
    return u + dt * derivada(u, k)</code></pre>

<p>Repare que <code>passo_euler</code> não menciona projétil, arrasto nem
gravidade. Ele recebe um vetor e uma função, e devolve o vetor seguinte. É
genérico porque o método é genérico.</p>

<div class="bloco alerta">
<span class="rotulo">Uma armadilha de ordem</span>
<p>As quatro linhas são atualizadas <em>juntas</em>, todas a partir dos valores
antigos. Quem escreve o código em quatro linhas separadas, e usa na linha do
\(x\) o \(v_x\) que acabou de calcular, não está mais fazendo Euler: está
fazendo <strong>Euler-Cromer</strong>, que é outro método. Não é erro, e em
problemas oscilatórios chega a ser melhor, mas é preciso saber qual dos dois se
está usando.</p>
</div>

<h3>O melhor teste possível</h3>

<p>A seção 3 deu quatro soluções exatas, e elas servem para algo além de
beleza: servem para <em>auditar</em> o integrador. Rodando o método numérico
num caso de solução conhecida, o erro medido não depende de nenhuma outra
aproximação. O programa faz isso com o arrasto linear, e o resultado é
limpo:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>\(\Delta t\) (s)</th><th>\(v\) numérico (m/s)</th>
<th>erro contra o exato</th><th>razão</th></tr></thead>
<tbody>
<tr><td>0,01</td><td>-4,08003691</td><td>2,825×10⁻²</td><td></td></tr>
<tr><td>0,001</td><td>-4,05461208</td><td>2,820×10⁻³</td><td>10,02</td></tr>
<tr><td>0,0001</td><td>-4,05207379</td><td>2,820×10⁻⁴</td><td>10,00</td></tr>
<tr><td>0,00001</td><td>-4,05182000</td><td>2,820×10⁻⁵</td><td>10,00</td></tr>
</tbody>
</table>
</div>

<p>Dividir o passo por dez divide o erro por dez, exatamente. Essa é a
definição de método de primeira ordem, medida contra a verdade e não contra
outra aproximação. Só depois de passar nesse teste é que faz sentido soltar o
programa no caso quadrático bidimensional, em que não há com que comparar.</p>
'''

S5 = r'''
<p>O widget integra o sistema das quatro equações com o passo que você
escolher, e desenha por cima a solução exata sempre que ela existir. Vale mexer
nele antes de ler o resto.</p>

<div data-widget="projetil"></div>

<p><strong>Comece pelo arrasto linear.</strong> Nesse modo, o widget conhece a
resposta certa: a curva fina é a solução fechada da seção 3, e a curva em
bronze é o que o Euler produz. Aumente o passo e veja as duas se separarem;
diminua e veja encostarem. O erro mostrado é medido contra o exato, e não
contra outra aproximação.</p>

<p><strong>Depois passe para o quadrático.</strong> A curva exata desaparece,
porque ela não existe, e no lugar dela entra uma referência numérica fina. É a
situação real de quem trabalha com isso: a verdade não está disponível, e o
máximo que se consegue é uma aproximação boa o bastante para servir de
régua.</p>

<p>Três coisas aparecem nas três vistas, e as três são o conteúdo deste
módulo.</p>

<p><strong>Na primeira</strong>, a trajetória com arrasto não é parábola: a
subida é mais longa que a descida e a queda é mais íngreme. Com os valores
iniciais, o alcance cai de 255 m para 149 m, isto é, o ar leva 41 % do
alcance.</p>

<p><strong>Na segunda</strong>, cada passo é uma seta reta, tangente à
trajetória no ponto de partida. Fica visível por que o erro existe e por que
ele diminui com o passo.</p>

<p><strong>Na terceira</strong>, o erro do alcance é posto contra \(\Delta t\)
em escala logarítmica nos dois eixos, de modo que uma lei de potência vira uma
reta e o expoente vira a inclinação. Euler dá inclinação 1; o <a href="https://pt.wikipedia.org/wiki/M%C3%A9todo_de_Runge-Kutta">Runge-Kutta de
quarta ordem</a>, que faz quatro avaliações da derivada por passo, dá 4.</p>

<div class="bloco def">
<span class="rotulo">O que significa ser de primeira ordem</span>
<p>Para ganhar um algarismo decimal de precisão, Euler precisa de
<em>dez vezes</em> mais passos. O RK4 precisa de menos de duas vezes
(\(10^{1/4} = 1{,}78\)). É por isso que ninguém usa Euler em produção, e é por
isso que todo mundo aprende Euler primeiro: ele é a ideia, e o resto é
refinamento dela.</p>
</div>
'''

S6 = r'''
<div class="cartoes">
  <a class="cartao" href="codigo/arrasto_analitico.py">
    <span class="numero">Programa</span>
    <h3>arrasto_analitico.py</h3>
    <p>Reúne as soluções fechadas da seção 3 e confere cada uma contra a
    integração numérica, incluindo os limites de arrasto pequeno.</p>
  </a>
  <a class="cartao" href="codigo/projetil_euler.py">
    <span class="numero">Programa</span>
    <h3>projetil_euler.py</h3>
    <p>Integra o sistema das quatro equações por Euler, por Euler-Cromer e por
    Runge-Kutta, mede os expoentes de convergência e varre o ângulo de
    lançamento.</p>
  </a>
</div>

<p><strong>O que o primeiro imprime, e o que conferir.</strong></p>

<ul>
<li>Cada solução fechada bate com o RK4 em \(10^{-12}\) ou melhor: a linear em
uma e em duas dimensões, a tangente da subida e a tangente hiperbólica da
queda.</li>
<li>O erro do Euler contra a solução <em>exata</em> cai por um fator
<strong>10,00</strong> a cada divisão do passo por dez.</li>
<li>Tratar as componentes separadamente, no caso quadrático bidimensional, erra
3,13 m em \(x\) e 5,03 m em \(y\) depois de apenas três segundos.</li>
<li>Com \(\tau\to\infty\) e \(k\to0\), as fórmulas com arrasto devolvem a
cinemática de sempre, como têm de devolver.</li>
</ul>

<p><strong>E o segundo.</strong></p>

<ul>
<li>Sem arrasto, o alcance converge para \(v_0^2\sen 2\theta/g = 254{,}842\)
m, com expoente medido <strong>1,000</strong>.</li>
<li>Com \(k = 0{,}004\ \mathrm{m^{-1}}\), os expoentes medidos são
<strong>0,993</strong> para Euler, <strong>1,002</strong> para Euler-Cromer e
<strong>3,928</strong> para o RK4.</li>
<li>O ângulo de alcance máximo cai de 45° sem ar para 41° com
\(k = 0{,}004\) e 35° com \(k = 0{,}020\).</li>
</ul>

<div class="bloco alerta">
<span class="rotulo">Uma lição que custou caro</span>
<p>A primeira versão deste programa media expoente <strong>2,58</strong> para o
RK4, e o método parecia pior do que é. O defeito não estava no integrador, e
sim em como o programa achava o ponto de pouso: interpolando \(y\)
<em>linearmente</em> entre os dois últimos passos. Essa interpolação erra em
\(\left(\Delta t\right)^2\), e o erro dela passou a dominar o erro do
método.</p>
<p>A correção é usar <a href="https://pt.wikipedia.org/wiki/Interpola%C3%A7%C3%A3o_de_Hermite">interpolação de Hermite</a>, que aproveita as velocidades, já
disponíveis, como derivadas nas pontas, e erra em \(\left(\Delta t\right)^4\).
Com ela, o expoente medido subiu para 3,93. A moral vale para qualquer trabalho
numérico: <em>a medida do erro também tem erro</em>, e um detalhe de
pós-processamento pode esconder a qualidade do método.</p>
</div>
'''

SECOES = [
    ('A segunda lei como equação diferencial', S1),
    ('Quanto o ar atrapalha', S2),
    ('O que se resolve no papel', S3),
    ('O método de Euler, e o sistema de quatro equações', S4),
    ('Mexendo no simulador', S5),
    ('No Spyder', S6),
]

SECOES.append(('Exercícios propostos', exercicios.bloco(LISTA)))


def main():
    titulos = [t for t, _ in SECOES]
    escreve('aula03.html', secoes_html(SECOES), secoes=titulos,
            subtitulo='A resistência do ar, dos dois lados. Onde a equação tem '
                      'solução fechada, ela é deduzida e usada; onde não tem, '
                      'e esse é justamente o caso realista, ela é integrada '
                      'passo a passo. A fronteira entre os dois casos é mais '
                      'interessante que qualquer um deles.')


if __name__ == '__main__':
    main()
