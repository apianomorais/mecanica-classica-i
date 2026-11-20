# -*- coding: utf-8 -*-
"""Módulo 6: o oscilador harmônico simples.

O argumento do módulo não é que o oscilador seja comum, e sim que ele é
inevitável: todo mínimo liso é uma parábola para amplitudes pequenas, como
o módulo 4 mostrou. Por isso vale gastar um módulo com uma única equação.
"""
from molde import escreve, secoes_html
import exercicios
from lista_aula06 import LISTA

S1 = r'''
<p>Uma disciplina inteira dedica um módulo a uma equação só, e convém dizer
por quê. Não é porque molas sejam importantes. É porque o módulo 4 terminou
mostrando que qualquer mínimo liso de qualquer potencial, expandido em série
em torno do ponto de equilíbrio \(x_0\), vale</p>

\[ U(x) \simeq U(x_0) + \underbrace{U'(x_0)}_{=\,0}(x-x_0)
   + \frac12 U''(x_0)\,(x-x_0)^2 + \ldots \]

<p>O termo linear morre porque \(x_0\) é mínimo, e o primeiro termo que
sobrevive é quadrático. Chamando \(k = U''(x_0)\) e medindo \(x\) a partir do
equilíbrio, a força é \(F = -kx\) e a equação de movimento é</p>

\[ m\ddot{x} = -kx \qquad\Longleftrightarrow\qquad
   \ddot{x} + \omega^2 x = 0, \qquad \omega = \sqrt{\frac{k}{m}}. \]

<p>Isso vale para a mola, para o pêndulo, para o átomo numa rede cristalina,
para a ponte que balança, para o circuito elétrico, para o campo
eletromagnético numa cavidade. Não porque esses sistemas se pareçam, e sim
porque todos têm um mínimo e todos ficam perto dele. Aprender esta equação
uma vez é aprender metade da física.</p>

<div class="destaque">
<p><strong>A receita, em duas perguntas.</strong> Diante de um sistema novo que
oscila, não procure a mola. Pergunte: quem faz o papel de inércia, e quem faz
o papel de rigidez? A resposta é sempre
\(\omega = \sqrt{\text{rigidez}/\text{inércia}}\), e a seção 6 mostra cinco
sistemas sem nenhuma semelhança entre si em que a receita funciona sem
mudança.</p>
</div>
'''

S2 = r'''
<p>A equação é linear, de segunda ordem, com coeficientes constantes, e por
isso tem exatamente duas soluções independentes e duas constantes a
determinar. A maneira direta de escrevê-las:</p>

\[ x(t) = x_0\cos\omega t + \frac{v_0}{\omega}\sen\omega t. \]

<p>As constantes já saíram prontas das condições iniciais: em \(t=0\) a
primeira parcela vale \(x_0\) e tem derivada nula, e a segunda vale zero e tem
derivada \(v_0\). Essa forma é cômoda para começar e péssima para ler, porque
não diz qual é a amplitude do movimento.</p>

<p>A outra forma diz. Usando \(\cos(a-b) = \cos a\cos b + \sen a\sen b\),</p>

\[ x(t) = C\cos\left(\omega t - \varphi\right), \qquad
   C = \sqrt{x_0^2 + \left(\frac{v_0}{\omega}\right)^2}, \qquad
   \tg\varphi = \frac{v_0}{\omega x_0}. \]

<p>Não são duas soluções: é a mesma, com o par de constantes trocado. O
programa confere as duas expressões em cinquenta mil instantes e a maior
diferença é de \(10^{-17}\) m, que é o erro da aritmética da máquina.</p>

<div data-widget="oscilador"></div>

<p>Vale demorar na terceira vista do componente, mas antes na primeira: mexa
em \(x_0\) e em \(v_0\) e repare no que <em>não</em> muda. A amplitude muda, a
fase muda, e o espaçamento entre os máximos fica onde estava. Amplitude e fase
são herança das condições iniciais; o período é propriedade do sistema.</p>
'''

S3 = r'''
<p>Que o período não dependa da amplitude é tão familiar que passa por óbvio,
e não é. Dobrar a amplitude dobra a distância a percorrer, o que sozinho
aumentaria o tempo. Mas dobrar a amplitude também dobra a força em cada ponto,
porque \(F = -kx\), e portanto dobra a velocidade típica. Os dois efeitos se
cancelam <strong>exatamente</strong>, e o cancelamento exato é privilégio da
força linear.</p>

<p>O programa testa isso soltando o mesmo oscilador de amplitudes que variam
por um fator mil:</p>

<div class="saida">
amplitude (m)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;periodo medido (s)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0,01&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>2,094395102</b><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0,50&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>2,094395102</b><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;10,00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>2,094395102</b>
</div>

<p>Nove casas iguais. Foi esse fato, observado por
<a href="https://pt.wikipedia.org/wiki/Galileu_Galilei">Galileu</a> em
lustres de igreja e verificado por ele com o próprio pulso, que tornou
possível o relógio de pêndulo de
<a href="https://pt.wikipedia.org/wiki/Christiaan_Huygens">Huygens</a>, e com
ele a navegação moderna. Um relógio precisa de um fenômeno cujo ritmo não
dependa de quão forte se bate nele.</p>

<div class="destaque">
<p><strong>Mas Galileu estava errado, e Huygens percebeu.</strong> O pêndulo
<em>não</em> é isócrono: ele apenas é quase isócrono para ângulos pequenos, e
a seção 5 mede o quanto. Huygens resolveu o problema de verdade em 1659,
mostrando que a curva exatamente isócrona não é o círculo e sim a
<strong>cicloide</strong>, e construiu relógios com guias cicloidais para
forçar o fio a descrevê-la. Na prática o atrito das guias estragava mais do
que a correção ganhava, e a solução que venceu foi outra: manter a amplitude
pequena e constante.</p>
</div>
'''

S4 = r'''
<p>Com \(x = C\cos(\omega t - \varphi)\), a velocidade é
\(v = -C\omega\sen(\omega t - \varphi)\), de modo que</p>

\[ U = \frac12 kx^2 = \frac{kC^2}{2}\cos^2(\omega t - \varphi), \qquad
   T = \frac{mv^2}{2} = \frac{kC^2}{2}\sen^2(\omega t - \varphi), \]

<p>usando \(m\omega^2 = k\). A soma é \(kC^2/2\) em qualquer instante, que é a
energia total: a conservação aparece aqui como a identidade trigonométrica
mais conhecida de todas. E como \(\med{\cos^2} = \med{\sen^2} = 1/2\) ao longo
de um ciclo,</p>

\[ \med{T} = \med{U} = \frac{E}{2}. \]

<p>A energia passa a metade do tempo em cada forma. O programa mede as duas
médias integrando ao longo de um período e acha 0,140625000 para cada uma,
contra \(E/2 = 0{,}140625000\).</p>

<p>Esse resultado é um caso particular do <strong>teorema do virial</strong>, e
ele tem consequências muito além da mecânica. É dele que vem, na Física
Estatística, a conclusão de que cada grau de liberdade quadrático leva
\(\frac12 k_BT\) de energia em média, e daí os calores específicos dos gases e
dos sólidos.</p>

<h3>A elipse, e a área que ela encerra</h3>

<p>No espaço de fase, eliminando o tempo entre \(x\) e \(v\):</p>

\[ \frac{x^2}{C^2} + \frac{v^2}{C^2\omega^2} = 1, \]

<p>uma elipse. O movimento percorre essa elipse para sempre, no sentido
horário, e a conservação da energia é exatamente a afirmação de que ele não
sai dela. A área encerrada vale \(\pi C^2\) no plano \((x, v/\omega)\), que é
\(2\pi E/\omega^2\), e o programa confirma os dois números até a nona casa.</p>

<p>Essa área tem nome, <strong>ação</strong>, e uma propriedade notável: se a
mola for enrijecida muito devagar, a energia muda e a área não. É um invariante
adiabático, e foi exatamente essa quantidade que Bohr quantizou em 1913, muito
antes de existir mecânica quântica. O módulo 12 a reencontra nas órbitas.</p>
'''

S5 = r'''
<p>O pêndulo simples é o exemplo que todo mundo usa e quase ninguém resolve. A
equação exata, para um fio ideal de comprimento \(L\), vem do torque:</p>

\[ \ddot\theta = -\frac{g}{L}\sen\theta. \]

<p>Isso <strong>não</strong> é um oscilador harmônico. Vira um quando se troca
\(\sen\theta\) por \(\theta\), o que é legítimo para \(\theta\) pequeno e
produz \(T_0 = 2\pi\sqrt{L/g}\), famosamente independente da massa e da
amplitude. A pergunta honesta é quanto custa essa troca.</p>

<p>Da conservação da energia sai o período exato, por quadratura, com a mesma
técnica do módulo 4:</p>

\[ T = 4\sqrt{\frac{L}{2g}}\int_0^{\theta_0}
   \frac{d\theta}{\sqrt{\cos\theta - \cos\theta_0}}
   = 4\sqrt{\frac{L}{g}}\;K\!\left(\sen\frac{\theta_0}{2}\right), \]

<p>em que \(K\) é a
<a href="https://pt.wikipedia.org/wiki/Integral_el%C3%ADptica">integral
elíptica completa de primeira espécie</a>, que não se escreve com funções
elementares. A substituição \(\sen(\theta/2) = \sen(\theta_0/2)\sen u\)
cancela a divergência do integrando no ponto de retorno, e a regra do ponto
médio faz o resto:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>\(\theta_0\)</th><th>\(T\) exato (s)</th><th>\(T/T_0\)</th>
<th>erro de usar \(T_0\)</th><th>série até \(\theta^4\)</th></tr></thead>
<tbody>
<tr><td>5°</td><td>2,007365</td><td>1,00048</td><td>0,05 %</td>
<td>\(1\times10^{-8}\) %</td></tr>
<tr><td>10°</td><td>2,010236</td><td>1,00191</td><td>0,19 %</td>
<td>\(7\times10^{-7}\) %</td></tr>
<tr><td>20°</td><td>2,021796</td><td>1,00767</td><td>0,77 %</td>
<td>\(4\times10^{-5}\) %</td></tr>
<tr><td>45°</td><td>2,086612</td><td>1,03997</td><td>4,0 %</td>
<td>0,006 %</td></tr>
<tr><td>90°</td><td>2,368246</td><td>1,18034</td><td>18 %</td><td>0,37 %</td></tr>
<tr><td>179°</td><td>7,827133</td><td>3,90107</td><td>290 %</td><td>50 %</td></tr>
</tbody>
</table>
</div>

<p>A tabela responde a pergunta prática. Em 10°, o erro de 0,19 % é menor que
a incerteza de um cronômetro de mão disparado a olho, e por isso o pêndulo é
um bom instrumento de laboratório para medir \(g\). Em 20° ele já atrapalha, e
o exercício 6.3 mostra que ignorá-lo faz \(g\) sair 1,5 % baixo, o que é mais
do que o erro de qualquer régua.</p>

<p>Para conferir que a quadratura está certa, o programa calcula os mesmos
períodos de outro jeito, integrando \(\ddot\theta = -(g/L)\sen\theta\) passo a
passo. Os dois caminhos concordam em \(2\times10^{-11}\) s.</p>

<p>Na última linha o período quase quadruplica, e ele diverge quando
\(\theta_0 \to 180^\circ\). Um pêndulo colocado exatamente em pé não cai
nunca: é um equilíbrio instável, e o tempo infinito para sair dele é o mesmo
tempo infinito da separatriz do poço duplo do módulo 4. Harmônico e não linear
não são dois mundos; são o mesmo sistema em amplitudes diferentes, e o
módulo 9 segue daqui.</p>
'''

S6 = r'''
<p>A receita \(\omega = \sqrt{\text{rigidez}/\text{inércia}}\) é mais útil do
que parece, porque dispensa recomeçar do zero a cada sistema. O programa
aplica a mesma receita a cinco sistemas que não têm nada em comum:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>sistema</th><th>\(\omega^2\)</th><th>\(\omega\) (rad/s)</th>
<th>\(T\) (s)</th></tr></thead>
<tbody>
<tr><td>mola de 2,5 N/m com 300 g</td><td>\(k/m\)</td><td>2,887</td>
<td>2,177</td></tr>
<tr><td>pêndulo simples de 1,00 m</td><td>\(g/L\)</td><td>3,132</td>
<td>2,006</td></tr>
<tr><td>barra de 1,00 m presa numa ponta</td><td>\(3g/2L\)</td><td>3,835</td>
<td>1,638</td></tr>
<tr><td>água num tubo em U, coluna de 40 cm</td><td>\(2g/L\)</td><td>7,002</td>
<td>0,897</td></tr>
<tr><td>boia cilíndrica, 12 cm submersos</td><td>\(g/h\)</td><td>9,040</td>
<td>0,695</td></tr>
</tbody>
</table>
</div>

<p>Duas linhas merecem comentário. A barra uniforme presa numa ponta oscila
mais rápido que o pêndulo simples de mesmo comprimento, e não mais devagar
como a intuição sugere: a massa distribuída fica, em média, mais perto do eixo,
e o pêndulo simples equivalente tem \(2L/3 = 0{,}667\) m. E a boia tem
frequência que não depende da densidade do material nem do raio do cilindro,
apenas da altura submersa: ela é um pêndulo de comprimento \(h\) disfarçado.</p>

<p>O exercício 6.5 faz o mesmo com uma molécula, onde a inércia que entra na
conta não é a massa de nenhum dos dois átomos e sim a massa reduzida. Errar
isso custa 75 % na constante elástica.</p>
'''

S7 = r'''
<div class="cartoes">
  <a class="cartao" href="codigo/oscilador.py">
    <span class="numero">Programa</span>
    <h3>oscilador.py</h3>
    <p>Confere as duas formas da solução, mede o período para amplitudes que
    variam por mil, calcula as médias de energia e a área da elipse, resolve o
    pêndulo exato por quadratura e aplica a receita a cinco sistemas.</p>
  </a>
</div>

<p><strong>O que ele imprime, e o que conferir.</strong></p>

<ul>
<li>As formas \(A\cos\omega t + B\sen\omega t\) e \(C\cos(\omega t-\varphi)\)
coincidem em \(10^{-17}\) m ao longo de cinquenta mil instantes.</li>
<li>O período medido é o mesmo nas nove casas para amplitudes de 1 cm a
10 m.</li>
<li>As médias de \(T\) e de \(U\) num ciclo dão \(E/2\) cada uma, e a área da
elipse dá \(2\pi E/\omega^2\), as duas na nona casa.</li>
<li>O período do pêndulo por quadratura e por integração direta da equação de
movimento concordam em \(2\times10^{-11}\) s.</li>
<li>A série \(1 + \theta^2/16 + 11\theta^4/3072\) acompanha a integral
elíptica até uns 60° e desiste depois.</li>
</ul>

<div class="bloco ex">
<p><strong>Para mexer.</strong> Dois tropeços estão guardados no código, com
comentário: medir o período pelo primeiro zero da velocidade dá metade do
valor certo, e contar o tempo do pêndulo até o fundo dá um quarto do período,
não metade. Apague os comentários, refaça as contas erradas e veja o tamanho
do estrago: são erros que não produzem nenhum sintoma visível, apenas um
número plausível e errado pela metade. Depois acrescente um sexto sistema à
tabela da seção 6, por exemplo uma bola rolando sem deslizar dentro de uma
calota de raio \(R\), e confira se a frequência que você deduziu bate com a
integração numérica.</p>
</div>
'''

SECOES = [
    ('Por que um módulo inteiro para uma equação', S1),
    ('A solução, e as duas constantes que sempre são duas', S2),
    ('Isocronismo, e o que ele tem de particular', S3),
    ('A energia que vai e volta, e a área que não muda', S4),
    ('O pêndulo de verdade, sem aproximação', S5),
    ('A mesma equação em cinco sistemas', S6),
    ('No Spyder', S7),
]

SECOES.append(('Exercícios propostos', exercicios.bloco(LISTA)))


def main():
    titulos = [t for t, _ in SECOES]
    escreve('aula06.html', secoes_html(SECOES), secoes=titulos,
            subtitulo='O oscilador harmônico não merece um módulo por ser '
                      'comum, e sim por ser inevitável: todo mínimo liso é uma '
                      'parábola para amplitudes pequenas. Aqui a equação é '
                      'resolvida, o isocronismo é medido, e o pêndulo de '
                      'verdade mostra onde a aproximação acaba.')


if __name__ == '__main__':
    main()
