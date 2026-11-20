# -*- coding: utf-8 -*-
"""Módulo 11: gravitação.

Fica com o teorema das cascas (provado por integração), o teste da Lua, as
marés e a medida de G. A formulação de campo com a lei de Gauss, a equação de
Poisson e os multipolos é a unidade de gravitação de Mecânica Clássica III, e
a página aponta para lá em vez de repetir.
"""
from molde import escreve, secoes_html
import exercicios
from lista_aula11 import LISTA

S1 = r'''
<p>A lei da gravitação universal cabe numa linha:</p>

\[ \vet{F} = -\frac{GMm}{r^2}\,\vers{r}. \]

<p>O que não cabe numa linha é o que foi preciso para escrevê-la, nem o que
decorre dela. Vale separar as duas coisas.</p>

<h3>De onde veio o expoente 2</h3>

<p>Ele não foi adivinhado. Tome a terceira lei de Kepler, que era um fato
observado desde 1619: \(T^2 \propto a^3\). Para uma órbita circular, a força
centrípeta é</p>

\[ F = \frac{mv^2}{r} = \frac{m}{r}\left(\frac{2\pi r}{T}\right)^2
     = \frac{4\pi^2mr}{T^2}. \]

<p>Substituindo \(T^2 = ka^3 = kr^3\):</p>

\[ F = \frac{4\pi^2 m}{k\,r^2}. \]

<p>O expoente 2 <em>sai</em> da terceira lei de Kepler, e não é hipótese. O
que Newton acrescentou foi a universalidade: que a mesma lei vale para a maçã,
e que a constante \(4\pi^2/k\) é proporcional à massa do corpo central, de modo
que a força é simétrica nas duas massas.</p>

<h3>O teste da Lua</h3>

<p>A afirmação de que é a <em>mesma</em> força precisa de teste. Se for, a
aceleração da Lua tem de ser \(g\) reduzida pelo inverso do quadrado:</p>

\[ a_{\text{Lua}} \stackrel{?}{=} g\left(\frac{R_T}{d}\right)^2. \]

<p>O programa faz a conta com os valores modernos:</p>

<div class="saida">
g (R_T/d)^2 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= 2,693837e-03 m/s²<br>
4 pi^2 d / T^2 (medida) = 2,723330e-03 m/s²<br>
razao &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= <b>1,0109</b>
</div>

<p>Um por cento de diferença. A tentação é dizer "concorda bem" e seguir
adiante; a atitude certa é perguntar de onde vem o 1 %, porque os dados têm
seis algarismos e o erro é mil vezes maior que eles.</p>

<p>Faltam dois termos. Primeiro, o \(g\) medido inclui a rotação da Terra e o
achatamento, como o módulo 2 mostrou; o \(g\) puramente gravitacional é
\(GM/R^2 = 9{,}8203\) m/s², contra 9,80665 medido. Segundo, a Lua não orbita a
Terra: as duas orbitam o centro de massa comum, de modo que a aceleração
<em>relativa</em> obedece a \(G(M+m)/d^2\), e não \(GM/d^2\). Refazendo:</p>

<div class="saida">
G (M + m) / d^2 = 2,730751e-03 m/s²<br>
4 pi^2 d / T^2 &nbsp;= 2,723330e-03 m/s²<br>
razao &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= <b>0,99728</b>
</div>

<p>Sobram dois décimos de por cento, que é a diferença entre o semieixo maior e
a distância média usada aqui. A lição vale para o curso inteiro: quando uma
conta de física erra 1 %, quase sempre falta um termo, e não precisão.</p>
'''

S2 = r'''
<p>Escrever \(GMm/r^2\) para a Terra e a Lua esconde uma pergunta
incômoda: \(r\) medido a partir de onde? A Terra tem 6400 km de raio, e os
pedaços dela estão a distâncias diferentes da Lua. A resposta é o
<strong>teorema das cascas</strong>, e ele é o motivo de Newton ter adiado os
<em>Principia</em> por anos.</p>

<div class="bloco def">
<p class="rotulo">Teorema das cascas</p>
<p>Uma casca esférica de massa uniforme atrai um ponto <strong>externo</strong>
como se toda a sua massa estivesse concentrada no centro, e não exerce força
alguma sobre um ponto <strong>interno</strong>, em qualquer posição dentro
dela.</p>
</div>

<div data-widget="gravidade"></div>

<p>O lado externo é cômodo; o interno é surpreendente. Dentro da casca, o campo
é <em>exatamente</em> nulo em toda parte, e não apenas no centro. O programa
verifica isso somando anéis, sem usar teorema nenhum:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>\(r/R\)</th><th>campo calculado</th>
<th>o que um ponto daria</th></tr></thead>
<tbody>
<tr><td>0,300</td><td>\(5\times10^{-20}\)</td><td>\(7\times10^{-10}\)</td></tr>
<tr><td>0,950</td><td>\(1\times10^{-17}\)</td><td>\(7\times10^{-11}\)</td></tr>
<tr><td>0,999</td><td>\(3\times10^{-14}\)</td><td>\(7\times10^{-11}\)</td></tr>
</tbody>
</table>
</div>

<p>O argumento geométrico é mais bonito que a conta. Fique num ponto qualquer
dentro da casca e olhe em duas direções opostas, dentro de um cone estreito. O
pedaço de casca próximo está perto e atrai mais, por \(1/s^2\); mas ele é
pequeno, e a área interceptada pelo cone cresce com \(s^2\). Os dois efeitos se
cancelam <strong>exatamente</strong>, em qualquer direção que se olhe. Esse
cancelamento é uma propriedade do expoente 2: com \(1/r^{2{,}001}\) ele
falharia, e é por isso que medir o campo dentro de uma casca é um dos testes
mais sensíveis da lei.</p>

<h3>Dentro de uma esfera maciça</h3>

<p>Uma esfera maciça é uma pilha de cascas. Num ponto a distância \(r\) do
centro, as cascas externas não fazem nada e as internas agem como um ponto
central, de modo que só conta a massa \(M(r) = M r^3/R^3\):</p>

\[ g(r) = \frac{GM(r)}{r^2} = \frac{GMr}{R^3} \qquad (r &lt; R). \]

<p>O campo cresce <strong>linearmente</strong> com \(r\) dentro da esfera, o
que é a lei de Hooke disfarçada. Um corpo largado num túnel que atravessasse a
Terra pelo centro faria um movimento harmônico simples, com</p>

\[ T = 2\pi\sqrt{\frac{R^3}{GM}} = 84{,}35\ \text{minutos}, \]

<p>que é <em>o mesmo</em> período de um satélite rasante. Não é coincidência:
as duas contas têm o mesmo \(GM/R^3\), e o satélite rasante é a projeção do
movimento no túnel vista de fora.</p>

<div class="bloco fisica">
<p class="rotulo">Onde este módulo para, e onde continua</p>
<p>A formulação de campo (o fluxo, a lei de Gauss, a equação de Poisson
\(\nabla^2\Phi = 4\pi G\rho\) e a expansão em multipolos para corpos sem
simetria) é a unidade de gravitação de <strong>Mecânica Clássica III</strong>,
junto com a autogravidade e a equação de Lane-Emden. Aqui o teorema das cascas
foi provado por integração direta, que é como Newton o fez e é o que basta para
tudo o que vem a seguir.</p>
</div>
'''

S3 = r'''
<p>A Lua imprime a você uma aceleração de \(3{,}3\times10^{-5}\) m/s², que é
três milionésimos de \(g\): sobre uma pessoa de 70 kg, 2,3 mN, o peso de um
quarto de grama. Ainda assim a Lua move oceanos. A explicação é que o que move o oceano não é o campo
da Lua, e sim a <strong>diferença</strong> entre o campo em cada ponto e o
campo no centro da Terra.</p>

<p>A Terra inteira está em queda livre em direção à Lua. No referencial do
centro da Terra, que é portanto acelerado, aparece a força de inércia do módulo
2, uniforme e igual a menos o campo no centro. O que sobra é</p>

\[ \vet{a}_{\text{maré}}(\vet{r})
   = \vet{g}_{\text{Lua}}(\vet{r}) - \vet{g}_{\text{Lua}}(0), \]

<p>e isso é desenhado na segunda vista do componente. Ao longo da linha dos
centros, expandindo em \(R/d\):</p>

\[ a_{\text{maré}} \simeq \frac{2GmR}{d^3}. \]

<div class="bloco alerta">
<p class="rotulo">Duas marés, não uma</p>
<p>O erro mais comum é imaginar que a Lua "puxa a água para si", o que daria
<em>uma</em> maré alta por dia. O desenho mostra o contrário: os dois lados
abaulam para fora. O lado próximo é puxado <strong>mais</strong> que o centro e
se adianta; o lado oposto é puxado <strong>menos</strong> que o centro e fica
para trás. Como a Terra gira por baixo dos dois abaulamentos, cada ponto passa
por dois máximos a cada volta.</p>
</div>

<p>O programa calcula a diferença sem aproximar, nos dois lados:</p>

<div class="saida">
lado voltado para a Lua:&nbsp;&nbsp;+1,127233e-06 m/s² &nbsp;(para a Lua)<br>
lado oposto:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+1,072549e-06 m/s² &nbsp;(para longe da Lua)<br>
aproximacao 2 G m R / d^3: 1,099287e-06 m/s²
</div>

<p>Os dois lados diferem em 5,1 %, e essa assimetria é real: vem dos termos de
ordem superior em \(R/d\), que a aproximação despreza. A aproximação cai
exatamente no meio dos dois, como deve.</p>

<h3>A potência três, e por que a Lua ganha do Sol</h3>

<p>Repare na mudança de expoente. O campo cai com \(d^2\); a maré, que é a
<em>derivada</em> do campo, cai com \(d^3\). É a primeira vez no curso em que o
que importa não é o campo, e sim como ele varia no espaço.</p>

<p>Essa potência decide a competição entre a Lua e o Sol. O Sol puxa a Terra
<strong>178 vezes mais forte</strong> que a Lua. Mas a maré vai como
\(m/d^3\), e a Lua está 390 vezes mais perto:</p>

\[ \frac{\text{maré lunar}}{\text{maré solar}}
   = \frac{m_L}{m_S}\left(\frac{d_S}{d_L}\right)^3 = 2{,}18. \]

<p>A terceira vista do componente compõe as duas ao longo de um mês. Os dois
abaulamentos se somam na sizígia (Lua nova e cheia), dando as marés de água
viva, e se subtraem na quadratura, dando as águas mortas. A razão entre as duas
é 2,70, e o período da modulação é <em>meio</em> mês, porque Lua nova e Lua
cheia produzem exatamente a mesma maré.</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>maré de equilíbrio</th><th>altura no ponto sublunar</th>
<th>amplitude total</th></tr></thead>
<tbody>
<tr><td>lunar</td><td>0,357 m</td><td>0,536 m</td></tr>
<tr><td>solar</td><td>0,164 m</td><td>0,246 m</td></tr>
<tr><td>sizígia</td><td></td><td>0,782 m</td></tr>
<tr><td>quadratura</td><td></td><td>0,290 m</td></tr>
</tbody>
</table>
</div>

<p>Esses números são da <strong>maré de equilíbrio</strong>, que supõe um
oceano global respondendo instantaneamente. O oceano real tem continentes,
inércia e ressonâncias de bacia, e por isso as marés medidas na costa chegam a
metros. Os 16 m da baía de Fundy são uma ressonância da bacia, com período
próprio perto de 12 h, excitada por uma maré de equilíbrio de meio metro: é o
módulo 8 em escala geográfica, com \(Q\) alto.</p>
'''

S4 = r'''
<p>A maré não só levanta água: ela deforma o próprio satélite. Se a maré que o
planeta exerce sobre ele vencer a gravidade que o mantém inteiro, ele se
desmancha. A distância em que isso acontece é o <strong>limite de
Roche</strong>:</p>

\[ d_{\text{Roche}} \simeq 2{,}44\,R_P
   \left(\frac{\rho_P}{\rho_s}\right)^{1/3} \quad\text{(satélite fluido)}, \]

<p>com 2,44 trocado por \(2^{1/3} = 1{,}26\) no caso rígido, que resiste mais
por ter coesão própria. Para o sistema Terra-Lua, o limite fluido fica em 2,9
raios terrestres, e a Lua está a 60: bem longe de qualquer perigo. Os anéis de
Saturno, ao contrário, estão <em>dentro</em> do limite de Roche de Saturno, e é
por isso que são anéis e não uma lua.</p>

<h3>O atrito das marés, e o dia que cresce</h3>

<p>Até aqui a maré foi tratada como estática. Ela não é: a Terra gira sob os
abaulamentos, e o atrito arrasta o abaulamento alguns graus à frente da linha
Terra-Lua. Esse abaulamento adiantado puxa a Lua para a frente na órbita, e a
Lua puxa a Terra para trás na rotação. As consequências são medidas, não
inferidas:</p>

<ul>
<li>A Lua se afasta <strong>3,8 cm por ano</strong>, medidos por
<em>laser ranging</em> nos retrorrefletores deixados pelas missões Apolo.</li>
<li>O dia aumenta cerca de 1,8 ms por século, o que corais fósseis confirmam:
os do Devoniano mostram cerca de 400 dias por ano.</li>
<li>A Lua já perdeu a rotação própria por esse mecanismo, e por isso nos mostra
sempre a mesma face.</li>
</ul>

<p>O momento angular total se conserva: o que a Terra perde de rotação, a Lua
ganha de órbita. É o módulo 5 operando em escala de bilhões de anos.</p>

<h3>Medir G</h3>

<p>Toda a gravitação depende de uma constante que é a pior medida da física.
\(G\) é conhecida com cinco algarismos; a carga do elétron, com dez. A razão é
que a gravidade é fraquíssima: não há como blindar, nem como amplificar, e
qualquer caminhão passando perturba a medida.</p>

<p>Henry Cavendish fez a primeira medida séria em 1798, com uma balança de
torção: duas esferas pequenas numa haste suspensa por um fio, atraídas por duas
esferas grandes. A deflexão é minúscula, e a constante de torção do fio se mede
pelo <em>período</em> de oscilação da haste, que é o módulo 6 trabalhando como
instrumento.</p>

<div class="bloco fisica">
<p class="rotulo">O que Cavendish mediu, e o que ele não mediu</p>
<p>Cavendish nunca falou em \(G\): a constante só foi introduzida décadas
depois. O título do artigo dele é "Experiments to determine the Density of the
Earth", e é isso que ele mediu, 5,48 vezes a densidade da água. O valor atual é
5,514, de modo que ele errou <strong>0,6 %</strong> com equipamento de
madeira e chumbo. Conhecida a densidade média e o raio, \(G\) sai de
\(g = \frac{4}{3}\pi G\rho R\), e é nesse sentido que se diz que Cavendish
"pesou a Terra".</p>
</div>
'''

S5 = r'''
<div class="cartoes">
  <a class="cartao" href="codigo/gravidade.py">
    <span class="numero">Programa</span>
    <h3>gravidade.py</h3>
    <p>Verifica o teorema das cascas por integração direta, calcula o campo
    dentro de uma esfera maciça, refaz o teste da Lua com as duas correções,
    e calcula marés, alturas de equilíbrio e o limite de Roche.</p>
  </a>
</div>

<p><strong>O que ele imprime, e o que conferir.</strong></p>

<ul>
<li>O campo dentro da casca fica dez ordens de grandeza abaixo do que um ponto
daria, em cinco posições, inclusive a um milésimo da superfície.</li>
<li>Fora da casca, o campo reproduz \(-GM/r^2\) em \(10^{-19}\).</li>
<li>O campo dentro da esfera maciça, somando cascas, reproduz \(-GMr/R^3\) em
\(10^{-26}\), e o potencial no centro é exatamente \(3/2\) do da
superfície.</li>
<li>O teste da Lua passa de 1,1 % para 0,27 % de erro com as duas correções.</li>
<li>A maré de equilíbrio dá 0,357 m, a razão lunar/solar dá 2,18, e os dois
lados da Terra diferem em 5,1 %.</li>
</ul>

<div class="bloco ex">
<p><strong>Para mexer.</strong> Troque o expoente 2 por 2,001 na rotina da
casca e meça o campo interno: ele deixa de ser nulo, e o tamanho do resíduo diz
quão sensível é esse teste. Depois calcule a maré que Júpiter exerce sobre a
Terra, e compare com a da Lua: é a maneira mais rápida de responder, com
números, à pergunta sobre a influência dos planetas sobre nós.</p>
</div>
'''

SECOES = [
    ('De onde veio a lei, e o teste da Lua', S1),
    ('O teorema das cascas, e o túnel pela Terra', S2),
    ('Marés: o que importa é a diferença', S3),
    ('Roche, o dia que cresce, e a medida de G', S4),
    ('No Spyder', S5),
]

SECOES.append(('Exercícios propostos', exercicios.bloco(LISTA)))


def main():
    titulos = [t for t, _ in SECOES]
    escreve('aula11.html', secoes_html(SECOES), secoes=titulos,
            subtitulo='A lei cabe numa linha; as consequências não. O teorema '
                      'das cascas é o que permite tratar planetas como pontos, '
                      'e as marés mostram o que acontece quando o que importa '
                      'deixa de ser o campo e passa a ser a sua variação.')


if __name__ == '__main__':
    main()
