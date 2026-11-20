# -*- coding: utf-8 -*-
"""Módulo 3: forças que dependem do tempo, da velocidade e da posição.

É aqui que entra o método de Euler, porque é aqui que a equação de
movimento deixa de ter solução em fórmula fechada pela primeira vez.
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
<strong>posição</strong>, como a de uma mola ou a gravitação. Cada caso pede um
tratamento, e só os mais simples têm solução que se escreve.</p>

<div class="bloco def">
<span class="rotulo">O que é resolver</span>
<p>Resolver a equação de movimento é achar \(\vet{r}(t)\) para todo \(t\),
dadas a posição e a velocidade num instante. Essas duas condições iniciais são
necessárias porque a equação é de segunda ordem, e são <em>suficientes</em>:
nada mais sobre o passado do sistema importa. É essa propriedade que faz da
mecânica newtoniana uma teoria determinista.</p>
</div>

<h3>Os casos que se resolvem no papel</h3>

<p><strong>Força constante.</strong> Duas integrações e acabou, e o resultado é
a cinemática do ensino médio.</p>

<p><strong>Força só do tempo.</strong> Também duas integrações,
\(v(t) = v_0 + \frac1m\int F\,dt\), e nenhuma dificuldade conceitual.</p>

<p><strong>Força só da velocidade.</strong> Separa-se e integra-se:</p>

\[ m\der{v}{t} = F(v)
   \;\Longrightarrow\;
   t = m\int_{v_0}^{v}\frac{dv'}{F(v')}. \]

<p>Repare no que saiu: \(t(v)\), e não \(v(t)\). Para inverter é preciso ter
sorte com a integral, e com frequência não se tem.</p>

<p><strong>Força só da posição.</strong> O truque é multiplicar por \(v\) e
reconhecer a derivada da energia cinética, o que leva à conservação de energia
e a uma quadratura. O módulo 4 faz isso com cuidado.</p>

<h3>E o caso que não se resolve</h3>

<p>Basta sair um pouco desses moldes para a solução fechada desaparecer. Um
projétil com arrasto é o exemplo mais próximo da experiência de todo mundo: a
força depende da velocidade, as duas componentes do movimento ficam acopladas
pelo módulo da velocidade, e não existe fórmula para a trajetória. Ela existe
no mundo, e é fácil de observar, mas não em termos de funções elementares.</p>

<p>A resposta desta disciplina para esse fato não é desviar do problema, e sim
trocar de ferramenta.</p>
'''

S2 = r'''
<p>Antes de integrar, vale saber quanta força o ar faz. Para um corpo que se
move num fluido, há dois regimes.</p>

<p><strong>Arrasto linear</strong>, \(F = -bv\), vale quando o escoamento é
laminar, isto é, para objetos pequenos ou velocidades baixas. É o caso de uma
gota de névoa ou de uma bolinha caindo em óleo. A conta fica fácil, e é por isso
que os livros gostam dele.</p>

<p><strong>Arrasto quadrático</strong>, \(F = -\frac12\rho C_D A v^2\), vale
quando o escoamento é turbulento, que é o caso de quase tudo que interessa no
ar: uma bola, um ciclista, um carro, um paraquedista. É o caso realista, e é o
que este módulo usa.</p>

<p>Por comodidade, escrevemos a aceleração do arrasto quadrático como</p>

\[ \vet{a}_{\text{arr}} = -k\left|\vet{v}\right|\vet{v},
   \qquad k = \frac{\rho C_D A}{2m}, \]

<p>com \(k\) medido em inverso de metro. O módulo do vetor aparece porque o
arrasto é sempre contrário à velocidade, seja qual for a direção dela, e essa
é exatamente a razão de as duas componentes do movimento ficarem
acopladas.</p>

<div class="bloco alerta">
<span class="rotulo">Onde o acoplamento mora</span>
<p>Sem ar, o movimento horizontal e o vertical são independentes, e é isso que
permite tratar cada um por vez. Com arrasto quadrático,
\(\left|\vet{v}\right| = \sqrt{v_x^2+v_y^2}\) aparece nas <em>duas</em>
equações, de modo que o que acontece na vertical muda a desaceleração
horizontal e vice-versa. Separar deixa de ser possível, e esse é o
motivo técnico de a fórmula fechada não existir.</p>
</div>

<h3>Velocidade terminal</h3>

<p>Para a queda vertical a partir do repouso há um resultado simples e útil.
Quando o arrasto iguala o peso, a aceleração zera e a velocidade para de
crescer:</p>

\[ mg = \frac12\rho C_DAv_t^2
   \;\Longrightarrow\;
   v_t = \sqrt{\frac{g}{k}}. \]

<p>Com \(k = 0{,}004\ \mathrm{m^{-1}}\), que é o valor usado no simulador e no
programa deste módulo, isso dá \(v_t = 49{,}5\ \mathrm{m/s}\), ou 178 km/h, da
ordem do que se mede num paraquedista de bruços, cerca de 54 m/s. Uma bola de
tênis, bem mais leve para o seu tamanho, tem \(k\) quatro vezes maior e cai a
23 m/s; uma gota de chuva de 2 mm tem \(k = 0{,}21\ \mathrm{m^{-1}}\) e desce a
apenas 6,8 m/s, que é a razão de a chuva não machucar. O exercício 3.1 monta
essa tabela, e o programa do módulo confere o valor integrando a queda e
comparando com \(\sqrt{g/k}\).</p>
'''

S3 = r'''
<p>O método numérico mais simples que existe nasce de uma ideia de uma linha:
se eu sei onde estou e sei a derivada, sei aproximadamente onde estarei daqui a
pouco.</p>

<p>Para uma equação de primeira ordem \(\dot y = f(y,t)\), isso se escreve</p>

\[ y_{n+1} = y_n + \Delta t\,f(y_n,t_n), \]

<p>que é o <strong>método de Euler</strong>. Geometricamente, ele troca a curva
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
'''

S4 = r'''
<p>O widget abaixo integra o sistema das quatro equações com o passo que você
escolher. Vale mexer nele antes de ler o resto.</p>

<div data-widget="projetil"></div>

<p>Três coisas aparecem nas três vistas, e as três são o conteúdo deste
módulo.</p>

<p><strong>Na primeira</strong>, a trajetória com arrasto não é parábola: a
subida é mais longa que a descida e a queda é mais íngreme. Com os valores
iniciais do widget, o alcance cai de 255 m para 149 m, isto é, o ar leva
41 % do alcance. Nenhuma fórmula fechada descreve essa curva, e mesmo assim o
computador a produz sem esforço.</p>

<p><strong>Na segunda</strong>, cada passo é uma seta reta, tangente à
trajetória no ponto de partida. Fica visível por que o erro existe e por que
ele diminui com o passo: o pedaço de curva que a reta ignora encolhe quando
\(\Delta t\) encolhe.</p>

<p><strong>Na terceira</strong>, o erro do alcance é posto contra \(\Delta t\)
em escala logarítmica nos dois eixos, de modo que uma lei de potência vira uma
reta e o expoente vira a inclinação. Euler dá inclinação 1; o Runge-Kutta de
quarta ordem, que faz quatro avaliações da derivada por passo, dá 4.</p>

<div class="bloco def">
<span class="rotulo">O que significa ser de primeira ordem</span>
<p>Para ganhar um algarismo decimal de precisão, Euler precisa de
<em>dez vezes</em> mais passos. O RK4 precisa de menos de duas vezes
(\(10^{1/4} = 1{,}78\)). É por isso que ninguém usa Euler em produção, e é por
isso que todo mundo aprende Euler primeiro: ele é a ideia, e o resto é
refinamento dela.</p>
</div>
'''

S5 = r'''
<div class="cartoes">
  <a class="cartao" href="codigo/projetil_euler.py">
    <span class="numero">Programa</span>
    <h3>projetil_euler.py</h3>
    <p>Integra o sistema das quatro equações por Euler, por Euler-Cromer e por
    Runge-Kutta de quarta ordem, mede os expoentes de convergência e varre o
    ângulo de lançamento.</p>
  </a>
</div>

<p><strong>O que ele imprime, e o que conferir.</strong></p>

<ul>
<li>Sem arrasto, o alcance converge para \(v_0^2\sen 2\theta/g = 254{,}842\)
m, e o expoente medido do erro é <strong>1,000</strong>, que é a ordem de
Euler.</li>
<li>Com \(k = 0{,}004\ \mathrm{m^{-1}}\), os expoentes medidos são
<strong>0,993</strong> para Euler, <strong>1,002</strong> para Euler-Cromer e
<strong>3,928</strong> para o RK4.</li>
<li>A velocidade terminal medida bate com \(\sqrt{g/k}\) em
\(2\times10^{-13}\).</li>
<li>O ângulo de alcance máximo cai de 45° sem ar para 41° com
\(k = 0{,}004\) e 35° com \(k = 0{,}020\).</li>
</ul>

<div class="bloco alerta">
<span class="rotulo">Uma lição que custou caro</span>
<p>A primeira versão deste programa media expoente <strong>2,58</strong> para o
RK4, e o método parecia pior do que é. O defeito não estava no integrador, e
sim em como o programa achava o ponto de pouso: interpolando \(y\)
<em>linearmente</em> entre os dois últimos passos. Essa interpolação erra em
\(\left(\Delta t\right)^2\), e o erro dela passou a dominar o erro do método.</p>
<p>A correção é usar interpolação de Hermite, que aproveita as velocidades, já
disponíveis, como derivadas nas pontas, e erra em \(\left(\Delta t\right)^4\).
Com ela, o expoente medido subiu para 3,93. A moral vale para qualquer trabalho
numérico: <em>a medida do erro também tem erro</em>, e um detalhe de
pós-processamento pode esconder a qualidade do método.</p>
</div>
'''

SECOES = [
    ('A segunda lei como equação diferencial', S1),
    ('Quanto o ar atrapalha', S2),
    ('O método de Euler, e o sistema de quatro equações', S3),
    ('Mexendo no simulador', S4),
    ('No Spyder', S5),
]

SECOES.append(('Exercícios propostos', exercicios.bloco(LISTA)))


def main():
    titulos = [t for t, _ in SECOES]
    escreve('aula03.html', secoes_html(SECOES), secoes=titulos,
            subtitulo='A equação de movimento é uma equação diferencial, e a '
                      'maior parte delas não tem solução em fórmula fechada. '
                      'Este módulo troca a busca pela fórmula pela construção '
                      'da solução, passo a passo, e mostra que resolver quatro '
                      'equações acopladas custa o mesmo que resolver uma.')


if __name__ == '__main__':
    main()
