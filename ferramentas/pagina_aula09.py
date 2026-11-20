# -*- coding: utf-8 -*-
"""Módulo 9: além do linear.

Muda a pergunta do curso: em vez de "qual é x(t)", passa-se a perguntar "que
tipos de movimento existem". O instrumento é o plano de fase, e a técnica é a
linearização em torno dos pontos fixos. Termina no ciclo-limite, que é um tipo
de movimento que sistema linear nenhum produz.
"""
from molde import escreve, secoes_html
import exercicios
from lista_aula09 import LISTA

S1 = r'''
<p>Os módulos 6, 7 e 8 resolveram tudo o que apareceu, e isso foi possível por
um motivo só: as equações eram lineares. Some duas soluções e você tem outra
solução; multiplique por dois e continua valendo. Toda a maquinaria (a
superposição, a função de Green, as senoides) depende dessa propriedade.</p>

<p>A maioria das equações da física não a tem. O pêndulo de verdade já não
tinha, desde o módulo 6:</p>

\[ \ddot\theta = -\frac{g}{L}\sen\theta. \]

<p>Não existe fórmula elementar para \(\theta(t)\), e no entanto sabemos muita
coisa sobre esse movimento. Sabemos que ele é periódico, que o período cresce
com a amplitude, que diverge em 180°. Nada disso veio de resolver a equação.
Veio de olhar a energia, que é outro jeito de olhar.</p>

<p>Este módulo sistematiza esse outro jeito. A mudança é de pergunta:</p>

<div class="bloco def">
<p class="rotulo">A troca de pergunta</p>
<p>Em vez de <em>qual é \(x(t)\) para esta condição inicial</em>, pergunta-se
<em>que tipos de movimento este sistema admite, e qual condição inicial leva a
qual</em>. A primeira pergunta quer uma fórmula; a segunda quer um
<strong>mapa</strong>.</p>
</div>

<h3>O plano de fase</h3>

<p>Escreva a equação de segunda ordem como duas de primeira:</p>

\[ \dot\theta = \omega, \qquad \dot\omega = -\frac{g}{L}\sen\theta. \]

<p>Agora o estado do sistema é um <em>ponto</em> \((\theta,\omega)\) num plano,
e as duas equações dizem, em cada ponto desse plano, para onde o estado se
move. Isso é um campo de velocidades, e o movimento é uma curva que segue o
campo. Duas propriedades valem destacar antes de qualquer conta:</p>

<ul>
<li>Por cada ponto passa <strong>uma única</strong> trajetória. Se duas se
cruzassem, o estado no cruzamento teria duas continuações, e a equação não
permite isso. Trajetórias nunca se cruzam, e é essa regra que organiza o
desenho inteiro.</li>
<li>O tempo some do desenho. A figura mostra a <em>forma</em> de cada
movimento, não o ritmo. Saber onde a trajetória vai devagar exige olhar o
campo, e não a curva.</li>
</ul>

<div data-widget="retratos"></div>

<p>A primeira vista é o retrato do pêndulo inteiro. Tudo o que o módulo 6
gastou páginas dizendo está ali, de uma vez: as órbitas fechadas de amplitude
pequena, as órbitas de rotação lá em cima, e a curva que separa as duas
famílias. E aparece uma coisa nova, que a fórmula do período não mostrava.</p>
'''

S2 = r'''
<p>A curva vinho da primeira vista é a <strong>separatriz</strong>, e ela está
exatamente em \(e = 2\), a energia do alto. Não é uma órbita como as outras:
é a fronteira entre dois comportamentos qualitativamente diferentes.</p>

<p>O programa testa isso com duas condições iniciais que diferem em
\(2\times10^{-6}\) na velocidade:</p>

<div class="saida">
theta0   omega0      energia     o que acontece em 40 s<br>
&nbsp;0,00   1,999999   1,999998   <b>libracao</b><br>
&nbsp;0,00   2,000001   2,000002   <b>ROTACAO, 2,50 voltas</b>
</div>

<p>Uma volta e meia de diferença no destino, a partir de dois milionésimos de
diferença no começo. E não há nada de caótico aqui: a dinâmica é perfeitamente
previsível, e a conta que separa os dois casos é \(e &lt; 2\) ou \(e &gt; 2\),
que qualquer um faz. Mas já aparece o ingrediente que o módulo 10 vai
explorar: <strong>a dependência sensível das condições iniciais</strong>.</p>

<div class="bloco alerta">
<p class="rotulo">Sensibilidade não é caos</p>
<p>Essa confusão é comum e vale desarmar agora. Perto de qualquer separatriz,
condições vizinhas se separam, e isso acontece em sistemas integráveis
perfeitamente mansos, como o pêndulo. O que caracteriza o caos, como o módulo
10 vai precisar, é a separação exponencial <em>típica</em>, em quase todo
lugar, e não apenas sobre uma curva de medida nula.</p>
</div>

<h3>O que acontece com atrito</h3>

<p>Ponha \(-2\gamma\omega\) na equação e mexa no deslizante do componente. As
curvas deixam de se fechar, e toda trajetória termina parada num dos mínimos.
A separatriz, que era uma curva fechada, some, e no lugar dela fica a
fronteira entre <strong>bacias de atração</strong>.</p>

<p>O programa mede essas fronteiras soltando o pêndulo do fundo com
velocidades crescentes e perguntando em qual mínimo ele para:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>fronteira, em \(\omega_0\)</th><th>mínimo antes</th>
<th>mínimo depois</th><th>largura da faixa</th></tr></thead>
<tbody>
<tr><td>entre 2,60 e 2,65</td><td>\(0\)</td><td>\(2\pi\)</td><td>2,65</td></tr>
<tr><td>entre 4,30 e 4,35</td><td>\(2\pi\)</td><td>\(4\pi\)</td><td>1,70</td></tr>
<tr><td>entre 6,15 e 6,20</td><td>\(4\pi\)</td><td>\(6\pi\)</td><td>1,85</td></tr>
<tr><td>entre 8,00 e 8,05</td><td>\(6\pi\)</td><td>\(8\pi\)</td><td>1,85</td></tr>
</tbody>
</table>
</div>

<p>Vale registrar uma expectativa que a medida desmentiu. Era razoável esperar
faixas cada vez mais estreitas, já que cruzar mais barreiras custa mais energia
e \(\omega\) cresce com a raiz da energia. Medindo, a primeira faixa é larga,
2,65, e as seguintes ficam entre 1,70 e 1,85: praticamente constantes. A
expectativa era razoável e estava errada, e é por isso que se mede.</p>
'''

S3 = r'''
<p>Os pontos onde o campo se anula são os <strong>pontos fixos</strong>: o
sistema colocado ali exatamente fica ali para sempre. No pêndulo, \(\omega=0\)
e \(\sen\theta=0\), isto é, o fundo e o alto.</p>

<p>A pergunta útil não é onde eles estão, e sim o que acontece <em>perto</em>
deles. E aqui há um resultado que organiza o assunto inteiro: perto de um ponto
fixo, o campo é aproximadamente linear, e a dinâmica é decidida por uma matriz
\(2\times2\).</p>

<p>Escrevendo o sistema como \(\dot{x} = f(x,y)\), \(\dot{y} = g(x,y)\) e
expandindo em torno de um ponto fixo \((x_0,y_0)\):</p>

\[ \begin{pmatrix}\dot{\delta x}\\ \dot{\delta y}\end{pmatrix}
   \simeq J \begin{pmatrix}\delta x\\ \delta y\end{pmatrix},
   \qquad
   J = \begin{pmatrix}
   \pder{f}{x} & \pder{f}{y}\\[4pt]
   \pder{g}{x} & \pder{g}{y}\end{pmatrix}_{(x_0,y_0)}. \]

<p>Essa é a <strong>matriz jacobiana</strong>, e os seus autovalores
classificam o ponto fixo. Com \(\delta \propto e^{\lambda t}\), o sinal da
parte real diz se a perturbação cresce ou morre, e a parte imaginária diz se
ela gira:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>autovalores</th><th>nome</th><th>o que acontece</th></tr></thead>
<tbody>
<tr><td>reais, sinais opostos</td><td><strong>sela</strong></td>
<td>atrai numa direção, repele na outra</td></tr>
<tr><td>reais, ambos negativos</td><td>nó estável</td>
<td>tudo converge, sem girar</td></tr>
<tr><td>reais, ambos positivos</td><td>nó instável</td><td>tudo diverge</td></tr>
<tr><td>complexos, parte real \(&lt;0\)</td><td>foco estável</td>
<td>espiral para dentro</td></tr>
<tr><td>complexos, parte real \(&gt;0\)</td><td>foco instável</td>
<td>espiral para fora</td></tr>
<tr><td>imaginários puros</td><td><strong>centro</strong></td>
<td>órbitas fechadas; caso delicado</td></tr>
</tbody>
</table>
</div>

<p>Para o pêndulo com atrito, \(J\) sai imediatamente:</p>

\[ J = \begin{pmatrix} 0 & 1 \\ -\cos\theta_0 & -2\gamma\end{pmatrix}. \]

<p>No fundo, \(\cos\theta_0 = 1\) e os autovalores são
\(-\gamma \pm \sqrt{\gamma^2-1}\): centro sem atrito, foco estável com atrito.
No alto, \(\cos\theta_0 = -1\) e eles são \(-\gamma \pm \sqrt{\gamma^2+1}\),
sempre reais e de sinais opostos: <strong>sela em qualquer amortecimento</strong>.
O equilíbrio de cabeça para baixo é instável por geometria, e não por falta de
atrito.</p>

<p>O programa calcula a jacobiana por diferenças finitas, sem usar as fórmulas
acima, e compara os autovalores com os analíticos: a diferença é de
\(10^{-11}\). Vale fazer isso sempre que o campo for complicado demais para
derivar à mão.</p>

<h3>A sela esquece por onde se entrou</h3>

<p>A segunda vista do componente mostra o que acontece perto de cada ponto
fixo. No caso da sela, há um fato que merece ser verificado em vez de
acreditado: <strong>a trajetória sai alinhada com o autovetor instável,
qualquer que tenha sido a direção de entrada</strong>.</p>

<p>O programa empurra o pêndulo a partir do alto numa direção
<em>perpendicular</em> ao autovetor instável, com deslocamentos que variam por
um fator dez mil, e mede a direção de saída quando a trajetória se afasta 0,05
da sela:</p>

<div class="saida">
deslocamento inicial&nbsp;&nbsp;&nbsp;direcao ao sair<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1e-02&nbsp;&nbsp;&nbsp;(+0,802322, +0,596892)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1e-04&nbsp;&nbsp;&nbsp;(+0,802322, +0,596892)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1e-06&nbsp;&nbsp;&nbsp;(+0,802322, +0,596892)<br>
autovetor instavel&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(+0,802293, +0,596931)
</div>

<p>Idênticas nas seis casas. E os \(0{,}003^\circ\) que sobram em relação ao
autovetor não são resto do chute inicial: são a não linearidade no raio onde se
mediu. Medindo a raios cada vez menores:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>raio de medida</th><th>ângulo (graus)</th>
<th>ângulo / raio</th><th>ângulo / raio²</th></tr></thead>
<tbody>
<tr><td>0,200</td><td>0,044323</td><td>0,2216</td><td>1,1081</td></tr>
<tr><td>0,100</td><td>0,011068</td><td>0,1107</td><td>1,1068</td></tr>
<tr><td>0,050</td><td>0,002767</td><td>0,0553</td><td>1,1068</td></tr>
<tr><td>0,020</td><td>0,000443</td><td>0,0221</td><td>1,1064</td></tr>
<tr><td>0,010</td><td>0,000111</td><td>0,0111</td><td>1,1064</td></tr>
</tbody>
</table>
</div>

<p>Repare em qual coluna fica constante: a última. O desvio cai com o
<strong>quadrado</strong> da distância, e não com a distância. Isso diz mais do
que a linearização prometia: a trajetória de saída não apenas tem a direção do
autovetor, ela é <em>tangente</em> a ele.</p>

<p>Repare também no risco de olhar a coluna errada. A do meio também diminui, e
quem se contentasse com ela concluiria que o erro vai a zero sem notar a que
taxa, e perderia o resultado.</p>
'''

S4 = r'''
<p>Falta um tipo de movimento que sistema linear nenhum produz, e que não
aparece no pêndulo. Tome</p>

\[ \ddot{x} - \mu\left(1-x^2\right)\dot{x} + x = 0, \]

<p>que é a equação de <a href="https://pt.wikipedia.org/wiki/Balthasar_van_der_Pol">van
der Pol</a>, de 1920. Comparando com o módulo 7, o coeficiente de
\(\dot{x}\) é um amortecimento, e aqui ele <strong>muda de sinal</strong>:
negativo para \(|x| &lt; 1\), positivo para \(|x| &gt; 1\). Perto da origem o
sistema bombeia energia; longe dela, dissipa.</p>

<p>Nenhum dos dois comportamentos pode continuar indefinidamente. O repouso é
instável, porque qualquer perturbação é amplificada; a amplitude grande também,
porque é freada. Entre os dois sobra uma órbita fechada, e o que a terceira
vista do componente mostra é que essa órbita <strong>atrai todo mundo</strong>:
é um <strong>ciclo-limite</strong>.</p>

<p>O programa larga o sistema de dentro (\(x_0 = 0{,}05\)) e de fora
(\(x_0 = 4\)) e compara as amplitudes finais:</p>

<div class="saida">
mu&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;amplitude de dentro&nbsp;&nbsp;&nbsp;de fora&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;diferenca<br>
0,5&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2,002487930&nbsp;&nbsp;&nbsp;2,002487928&nbsp;&nbsp;&nbsp;2,3e-09<br>
1,0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2,008619861&nbsp;&nbsp;&nbsp;2,008619861&nbsp;&nbsp;&nbsp;3,1e-10<br>
4,0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2,022962497&nbsp;&nbsp;&nbsp;2,022962494&nbsp;&nbsp;&nbsp;3,6e-09
</div>

<div class="bloco def">
<p class="rotulo">Oscilação autossustentada</p>
<p>No módulo 6 a amplitude vinha das condições iniciais, e qualquer valor
servia. Aqui ela é <strong>propriedade do sistema</strong>: perturbe o
oscilador e ele volta ao mesmo ciclo. É por isso que relógios, corações e
neurônios podem funcionar com ritmo próprio, e é por isso que um oscilador
linear nunca serviria para isso.</p>
</div>

<h3>Os dois limites, e uma correção difícil que acerta</h3>

<p>Com \(\mu\) pequeno o ciclo é quase um círculo de raio 2, e o período quase
\(2\pi\). Os dois valores saem de um balanço de energia, que é o exercício 9.5,
e o programa confirma: com \(\mu = 0{,}01\) a amplitude dá 2,000001 e o período
6,283225, contra \(2\pi = 6{,}283185\).</p>

<p>Com \(\mu\) grande o movimento deixa de ser senoidal: são cargas lentas
seguidas de quedas rápidas, e isso se chama <strong>oscilação de
relaxação</strong>. O período cresce proporcionalmente a \(\mu\), com a
constante \(3-2\ln 2 = 1{,}6137\), mas a convergência é lenta e a teoria prevê a
correção seguinte,</p>

\[ T \simeq \left(3-2\ln 2\right)\mu + 3\alpha\,\mu^{-1/3},
   \qquad \alpha = 2{,}33811, \]

<p>em que \(\alpha\) é o primeiro zero da função de Airy. Vale conferir se essa
conta, que é difícil, acerta:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>\(\mu\)</th><th>\(T\) medido</th><th>\(T/\mu\)</th>
<th>só \(3-2\ln2\)</th><th>com a correção de Airy</th></tr></thead>
<tbody>
<tr><td>5</td><td>11,61223</td><td>2,322446</td><td>1,613706</td><td>2,434106</td></tr>
<tr><td>10</td><td>19,07837</td><td>1,907837</td><td>1,613706</td><td>1,939282</td></tr>
<tr><td>20</td><td>34,68232</td><td>1,734116</td><td>1,613706</td><td>1,742911</td></tr>
<tr><td>40</td><td>66,50137</td><td>1,662534</td><td>1,613706</td><td>1,664981</td></tr>
</tbody>
</table>
</div>

<p>Em \(\mu = 40\) a correção reduz o erro de 3 % para 0,15 %. Uma fórmula
assintótica difícil que acerta a segunda casa de uma medida numérica não é
coincidência, e serve de aviso contra a tentação de descartar termos de ordem
alta só porque são feios.</p>

<p>Van der Pol encontrou essa equação estudando circuitos de válvula, e ela
descreve também o batimento cardíaco, o disparo de neurônios e a palheta de um
clarinete. O amortecimento negativo é o mesmo do flutter de Tacoma, do módulo
8; a diferença é que aqui a não linearidade o segura, em vez de deixá-lo
crescer até a ruína.</p>
'''

S5 = r'''
<div class="cartoes">
  <a class="cartao" href="codigo/retratos.py">
    <span class="numero">Programa</span>
    <h3>retratos.py</h3>
    <p>Percorre o retrato do pêndulo, classifica os pontos fixos pela
    jacobiana numérica, mede a direção de saída de uma sela, mapeia as bacias
    de atração e verifica o ciclo-limite de van der Pol nos dois limites.</p>
  </a>
</div>

<p><strong>O que ele imprime, e o que conferir.</strong></p>

<ul>
<li>Duas condições iniciais separadas por \(2\times10^{-6}\) na velocidade
fazem coisas qualitativamente diferentes, uma de cada lado da separatriz.</li>
<li>Os autovalores da jacobiana por diferenças finitas batem com os analíticos
em \(10^{-11}\), nos quatro casos.</li>
<li>A direção de saída da sela é idêntica em seis casas para chutes iniciais
que diferem por um fator \(10^4\), e o desvio em relação ao autovetor cai com o
<em>quadrado</em> do raio de medida.</li>
<li>As amplitudes do ciclo-limite partindo de dentro e de fora coincidem em
\(10^{-9}\).</li>
<li>O período de relaxação, dividido por \(\mu\), acompanha a correção de Airy
até a segunda casa.</li>
</ul>

<div class="bloco ex">
<p><strong>Para mexer.</strong> Troque o pêndulo pelo oscilador de Duffing,
\(\ddot{x} + \gamma\dot{x} - x + x^3 = 0\), que tem <em>três</em> pontos fixos,
e classifique os três pela jacobiana numérica. Depois desenhe a fronteira entre
as bacias dos dois mínimos e compare com a do pêndulo: as duas são variedades
estáveis de uma sela, e é por isso que se parecem. Por fim, acrescente uma
força periódica ao Duffing e guarde o resultado: ele é o assunto do módulo
10.</p>
</div>
'''

SECOES = [
    ('Quando não há fórmula, ainda há mapa', S1),
    ('A separatriz, e a sensibilidade que ainda não é caos', S2),
    ('Pontos fixos: o que uma matriz 2×2 decide', S3),
    ('O ciclo-limite, que nenhum sistema linear tem', S4),
    ('No Spyder', S5),
]

SECOES.append(('Exercícios propostos', exercicios.bloco(LISTA)))


def main():
    titulos = [t for t, _ in SECOES]
    escreve('aula09.html', secoes_html(SECOES), secoes=titulos,
            subtitulo='Sem fórmula fechada ainda se sabe tudo o que importa, '
                      'olhando o plano (posição, velocidade). Os pontos fixos '
                      'organizam o desenho, uma matriz 2×2 classifica cada um, '
                      'e aparece um tipo de movimento que sistema linear '
                      'nenhum produz: o ciclo-limite.')


if __name__ == '__main__':
    main()
