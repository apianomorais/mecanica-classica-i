# -*- coding: utf-8 -*-
"""Módulo 5: momento linear, impulso e o movimento de foguetes.

O eixo do módulo é que F = dp/dt é a forma original e F = ma é o caso
particular de massa constante. Tudo o que o módulo tem de difícil, do
foguete à corrente que cai, mora nessa distinção.
"""
from molde import escreve, secoes_html
import exercicios
from lista_aula05 import LISTA

S1 = r'''
<p>Newton não escreveu \(\vet{F} = m\vet{a}\). O que está nos
<em>Principia</em> é que a força é a taxa de variação da
<em>quantidade de movimento</em>, que hoje chamamos de momento linear:</p>

\[ \vet{p} = m\vet{v}, \qquad \vet{F} = \der{\vet{p}}{t}. \]

<p>Quando a massa não muda, a derivada passa por ela e sai
\(\vet{F} = m\vet{a}\), que é a forma usada em tudo o que fizemos até o
módulo 4. A diferença parece pedante até o primeiro problema de massa
variável, e aí ela decide tudo.</p>

<p>Há um motivo mais fundo para começar pelo momento. Tome dois corpos que
interagem apenas entre si. Pela terceira lei, \(\vet{F}_{12} = -\vet{F}_{21}\),
de modo que</p>

\[ \der{}{t}\left(\vet{p}_1 + \vet{p}_2\right)
   = \vet{F}_{12} + \vet{F}_{21} = 0. \]

<p>O momento total de um sistema isolado é constante, e a conta não pediu
nada sobre a natureza da força: nem que seja conservativa, nem que se conheça
sua forma, nem que o choque seja elástico. Basta que as forças internas venham
em pares opostos. É por isso que a conservação do momento sobrevive a colisões
em que a energia mecânica não se conserva, e é por isso que ela resolve
problemas que a energia não resolve.</p>

<div class="destaque">
<p><strong>De onde vem, de verdade.</strong> A conservação do momento é mais
profunda que a terceira lei, que, como vimos no módulo 2, falha entre cargas
em movimento. O teorema de
<a href="https://pt.wikipedia.org/wiki/Emmy_Noether">Emmy Noether</a> mostra
que ela decorre de uma simetria: as leis da física são as mesmas aqui e dois
metros adiante. Homogeneidade do espaço dá momento conservado, do mesmo jeito
que homogeneidade do tempo dá energia conservada. Essa é a razão de essas duas
leis sobreviverem intactas à relatividade e à mecânica quântica, enquanto
\(\vet{F} = m\vet{a}\) não sobrevive a nenhuma das duas.</p>
</div>
'''

S2 = r'''
<p>Integrando \(\vet{F} = d\vet{p}/dt\) no tempo:</p>

\[ \vet{J} = \int_{t_a}^{t_b}\vet{F}\,dt = \vet{p}_b - \vet{p}_a. \]

<p>Esse é o teorema do impulso, e ele é ao tempo o que o teorema do trabalho
e da energia é ao espaço. Os dois saem da mesma equação integrada em variáveis
diferentes, e respondem perguntas diferentes.</p>

<p>O programa chuta uma bola de futebol com uma força que sobe e desce em
\(\sen^2\) durante 12 ms, com 2400 N de pico:</p>

<div class="saida">
impulso J = F0 T / 2 = <b>14,400000 N s</b><br>
momento final m v&nbsp;&nbsp;&nbsp;&nbsp;= <b>14,400000 kg m/s</b><br>
diferenca&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= 8e&minus;11<br>
velocidade de saida&nbsp;&nbsp;= <b>33,5 m/s = 121 km/h</b>
</div>

<p>Repare no que determina a velocidade de saída: a <strong>média da força no
tempo</strong>, 1200 N, metade do pico. A média na distância daria outro
número e responderia outra pergunta, a da energia. Quem quer chutar mais forte
não precisa de mais força de pico, precisa de mais impulso, que é força vezes
tempo de contato. É por isso que a técnica de acompanhar a bola com o pé
funciona.</p>

<h3>O mesmo teorema, lido ao contrário</h3>

<p>Numa parada, \(\Delta p\) está dado: é a quantidade de movimento que se
tinha e que precisa acabar. O que se pode escolher é o tempo. Como
\(\bar{F} = \Delta p/\Delta t\), estender o tempo é a única maneira de reduzir
a força. Uma pessoa de 75 kg a 50 km/h carrega \(J = 1050\) N·s, e tudo o que
muda de um caso para o outro é o denominador:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>Como a parada acontece</th><th>\(\Delta t\)</th>
<th>força média</th><th>em unidades de peso</th></tr></thead>
<tbody>
<tr><td>contra uma superfície rígida</td><td>2 ms</td><td>525 kN</td>
<td>714 \(g\)</td></tr>
<tr><td>contra um airbag</td><td>50 ms</td><td>21 kN</td><td>29 \(g\)</td></tr>
<tr><td>com a zona de deformação do carro</td><td>300 ms</td><td>3,5 kN</td>
<td>4,8 \(g\)</td></tr>
</tbody>
</table>
</div>

<p>O airbag não absorve energia nem amortece no sentido vago da palavra: ele
<strong>compra tempo</strong>. Quinze vezes mais tempo, quinze vezes menos
força. É o mesmo princípio do joelho que dobra ao cair, do capacete, da luva de
<em>baseball</em> que recua no momento de pegar a bola, e da embalagem que
protege o que está dentro.</p>
'''

S3 = r'''
<p>Aqui o cuidado com o sistema deixa de ser filosofia. A tentação é escrever
\(\vet{F} = m(t)\vet{a}\) para o foguete, com a massa diminuindo, e isso está
errado. O erro não é de conta: é de pergunta. A segunda lei vale para um
sistema fixo de partículas, e o foguete sozinho não é um sistema fixo, porque
está jogando pedaços de si para trás.</p>

<p>O jeito certo é tomar como sistema <strong>o foguete mais o gás que ele
está prestes a expelir</strong>, que é um sistema de massa constante, e
comparar dois instantes. No instante \(t\), massa \(m\) com velocidade \(v\).
No instante \(t + dt\), massa \(m + dm\) (com \(dm &lt; 0\)) a \(v + dv\), mais
a massa \(-dm\) expelida, que sai com velocidade \(v - v_e\) vista do solo, já
que \(v_e\) é medida em relação ao foguete:</p>

\[ p(t) = mv, \qquad
   p(t+dt) = (m+dm)(v+dv) + (-dm)\left(v - v_e\right). \]

<p>A diferença, descartando o produto \(dm\,dv\), que é de segunda ordem:</p>

\[ dp = m\,dv + v_e\,dm. \]

<p>Sem forças externas, \(dp = 0\), e sobra a equação do foguete:</p>

\[ m\der{v}{t} = -v_e\der{m}{t}. \]

<p>O lado direito é positivo, porque \(dm/dt &lt; 0\): é o
<strong>empuxo</strong>, e ele vale a velocidade de exaustão vezes a vazão de
massa. Repare que nada aqui precisa de ar para empurrar. O foguete acelera
porque joga massa para trás, e isso funciona igualmente bem no vácuo, o que
custou a <a href="https://pt.wikipedia.org/wiki/Robert_Goddard">Robert
Goddard</a> um editorial de jornal, em 1920, explicando-lhe que ele não
entendia o ensino médio. O <em>New York Times</em> publicou a retratação em
1969, com a Apolo 11 a caminho da Lua.</p>

<h3>A integração, e o logaritmo</h3>

<p>Separando as variáveis e integrando entre o início e o fim da queima:</p>

\[ \int_{v_0}^{v_f} dv = -v_e\int_{m_0}^{m_f}\frac{dm}{m}
   \quad\Longrightarrow\quad
   \Delta v = v_e\ln\frac{m_0}{m_f}. \]

<p>É a equação de
<a href="https://pt.wikipedia.org/wiki/Konstantin_Tsiolkovsky">Tsiolkovsky</a>,
escrita em 1903 por um professor de matemática surdo de província, e ela
continua sendo a restrição que decide todo projeto de foguete. O programa
confere a dedução contra a integração numérica passo a passo:</p>

<div class="saida">
Tsiolkovsky&nbsp;&nbsp;ve ln(m0/mf) = <b>4734,966338 m/s</b><br>
integracao numerica&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= <b>4734,966337 m/s</b>
</div>

<p>O que a fórmula diz é brutal. O \(\Delta v\) cresce com o
<strong>logaritmo</strong> da razão de massas, de modo que dobrar a velocidade
final exige elevar ao quadrado a razão: de 10 para 100. Com querosene e
oxigênio líquido, \(v_e \simeq 2942\) m/s, a órbita baixa pede cerca de
9400 m/s contando as perdas, o que dá uma razão de massas de 24 para 1. Isto
é: 96 % da máquina que sai do chão precisa ser combustível, e todo o resto
(tanques, motores, estrutura, carga) tem de caber nos 4 % restantes.</p>
'''

S4 = r'''
<p>A dedução acima ignorou a gravidade. Com ela, a equação fica</p>

\[ m\der{v}{t} = -v_e\der{m}{t} - mg, \]

<p>e o termo novo integra trivialmente, porque não depende da massa:</p>

\[ \Delta v = v_e\ln\frac{m_0}{m_f} - g\,t_q. \]

<p>A perda vale exatamente \(g\) vezes o tempo de queima, e o programa
confirma isso em todas as taxas testadas. Daí uma conclusão que surpreende:
<strong>queimar depressa rende mais</strong>. O mesmo propelente, gasto em
metade do tempo, entrega metade da perda.</p>

<div data-widget="foguete"></div>

<p>O limite para queimar depressa não é da física. É que o empuxo é constante
enquanto a massa só diminui, de modo que a aceleração cresce durante toda a
queima. Com a taxa mais alta do programa, ela terminaria em 48 \(g\), o que
desmontaria o veículo e mataria a tripulação. É por isso que os motores da
Saturno V eram desligados em sequência perto do fim do primeiro estágio, e não
por falta de combustível.</p>

<p>No outro extremo há um piso, que a terceira coluna do widget mostra. Se o
empuxo não vence o peso, o foguete não decola: ele fica na plataforma gastando
propelente, e a equação continua valendo, só que descrevendo um veículo
parado. A razão empuxo/peso na partida precisa passar de 1, e na prática fica
entre 1,2 e 1,5, porque empuxo demais também custa motor.</p>
'''

S5 = r'''
<p>Um estágio só tem um teto, e ele é fácil de ver. Chame de
\(\epsilon\) a <strong>fração estrutural</strong>: a massa de tanques, motores
e estrutura dividida pela massa do estágio cheio. Mesmo com carga útil
<em>nula</em>, o foguete termina a queima carregando \(\epsilon m_0\), de modo
que</p>

\[ \Delta v_{\max} = v_e\ln\frac{1}{\epsilon}. \]

<p>Com \(\epsilon = 0{,}10\), que já é bom, e querosene, isso dá 6774 m/s. Os
9400 m/s da órbita baixa estão fora de alcance, e não por pouco. Nenhum
foguete de um estágio só jamais colocou carga em órbita, e a razão não é
falta de engenharia: é essa linha.</p>

<p>A saída é parar de carregar tanque vazio. Com \(n\) estágios de mesma
fração estrutural e mesmo \(v_e\), o melhor arranjo é o de estágios
idênticos, cada um multiplicando a massa pela mesma razão
\(r = \left(m_0/m_{\text{carga}}\right)^{1/n}\), e o resultado é</p>

\[ \Delta v = n\,v_e\ln\frac{r}{1 + \epsilon\left(r-1\right)}. \]

<p>Vale a pena desconfiar dessa fórmula fechada. O programa calcula o caso de
dois estágios de outro jeito, varrendo todas as divisões possíveis de massa
entre eles e ficando com a melhor, e compara:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>carga útil</th><th>1 estágio</th><th>2 estágios (busca)</th>
<th>3 estágios</th><th>ganho de 1 para 2</th></tr></thead>
<tbody>
<tr><td>5000 kg</td><td>4886</td><td>5622</td><td>5810</td><td>+15,1 %</td></tr>
<tr><td>2000 kg</td><td>5870</td><td>7490</td><td>7917</td><td>+27,6 %</td></tr>
<tr><td>1000 kg</td><td>6287</td><td>8718</td><td>9411</td><td>+38,7 %</td></tr>
<tr><td>500 kg</td><td>6521</td><td>9772</td><td>10808</td><td>+49,9 %</td></tr>
<tr><td>200 kg</td><td>6670</td><td>10897</td><td>12491</td><td>+63,4 %</td></tr>
</tbody>
</table>
</div>

<p>A busca numérica e a forma fechada discordam em 0,002 m/s na pior das cinco
linhas, o que é erro de varredura. São dois caminhos independentes para o
mesmo número.</p>

<p>Leia a terceira linha com atenção: com 1000 kg de carga, três estágios dão
9411 m/s, que passa de raspão dos 9400 necessários. Está tudo ali, o
desconforto inteiro do negócio: 50 toneladas na plataforma para pôr uma
tonelada em órbita, e ainda assim por margem de 11 m/s.</p>

<p>Repare também que o ganho do estagiamento <em>cresce</em> quando a carga
útil encolhe. O motivo é direto: o que o estagiamento evita é carregar tanque
vazio, e quanto maior a parte da massa final que é tanque vazio, mais há a
ganhar em jogá-lo fora.</p>
'''

S6 = r'''
<p>Fica a impressão de que massa variável é assunto de foguete. Não é, e o
contraexemplo mais barato é uma corrente caindo sobre uma mesa.</p>

<p>Uma corrente de densidade linear \(\mu\) é solta do repouso, com a ponta
tocando a mesa. Quando um comprimento \(x\) já se acumulou, qual é a força que
a mesa faz?</p>

<p>A resposta ingênua é o peso do que já caiu, \(\mu g x\). Ela esquece que a
mesa não apenas <em>sustenta</em> os elos parados: ela também
<strong>para</strong> os elos que chegam. O trecho que ainda cai está em queda
livre, de modo que chega com \(v^2 = 2gx\), e num intervalo \(dt\) a mesa
precisa zerar o momento de uma massa \(\mu v\,dt\):</p>

\[ N = \underbrace{\mu g x}_{\text{peso do que parou}}
     + \underbrace{\mu v^2}_{\text{momento que chega}}
     = \mu g x + 2\mu g x = 3\mu g x. \]

<p>Três vezes o peso do que já caiu, durante toda a queda. O programa não
confia nessa conta: ele aplica \(\vet{F} = d\vet{p}/dt\) à corrente
<em>inteira</em>, que tem massa fixa, e isola a normal,</p>

\[ \mu L g - N = \der{p}{t}, \qquad p = \mu\left(L-x\right)v, \]

<p>o que é um caminho inteiramente independente. As duas contas coincidem em
\(3\times10^{-10}\) N ao longo de toda a queda.</p>

<div class="destaque">
<p><strong>A pergunta que sempre funciona.</strong> Diante de qualquer problema
de massa variável, não pergunte qual é a massa agora. Pergunte: qual é o meu
sistema, ele é fixo, e com que velocidade a massa entra ou sai dele? A
corrente e o foguete parecem opostos (um recebe massa parada, o outro expele
massa rápida) e são o mesmo problema com sinais trocados. O vagão que recolhe
areia, do exercício 5.4, é a terceira versão.</p>
</div>
'''

S7 = r'''
<div class="cartoes">
  <a class="cartao" href="codigo/foguete.py">
    <span class="numero">Programa</span>
    <h3>foguete.py</h3>
    <p>Confere o teorema do impulso, deduz e verifica Tsiolkovsky, mede a
    perda por gravidade, compara um estágio com dois e três, e resolve a
    corrente que cai pelo balanço de momento.</p>
  </a>
</div>

<p><strong>O que ele imprime, e o que conferir.</strong></p>

<ul>
<li>O impulso \(F_0T/2\) e o momento final \(mv\) coincidem em
\(8\times10^{-11}\), e a força média no tempo dá exatamente metade do pico.</li>
<li>Tsiolkovsky e a integração numérica da equação do foguete coincidem em
\(10^{-6}\) m/s.</li>
<li>A perda por gravidade é igual a \(g\,t_q\) em todas as cinco taxas, com
todas as casas.</li>
<li>O ótimo de dois estágios obtido por busca e a forma fechada dos estágios
idênticos discordam em 0,002 m/s.</li>
<li>A normal da corrente calculada por \(dp/dt\) e a fórmula \(3\mu g x\)
coincidem em \(3\times10^{-10}\) N.</li>
</ul>

<div class="bloco ex">
<p><strong>Para mexer.</strong> Troque a vazão do foguete por uma que
<em>diminui</em> com o tempo, de modo a manter a aceleração constante em
3 \(g\), e veja o que acontece com o tempo de queima e com a perda por
gravidade. Depois refaça a tabela de estágios com \(\epsilon = 0{,}06\), que é
o que tanques de alumínio-lítio modernos alcançam, e descubra se um estágio só
chega à órbita nesse caso.</p>
</div>
'''

SECOES = [
    ('O momento linear, e por que ele vem antes', S1),
    ('Impulso: a força média que de fato importa', S2),
    ('A equação do foguete, com o sistema certo', S3),
    ('O que a gravidade cobra durante a queima', S4),
    ('Por que todo foguete tem estágios', S5),
    ('Massa variável mal contada: a corrente', S6),
    ('No Spyder', S7),
]

SECOES.append(('Exercícios propostos', exercicios.bloco(LISTA)))


def main():
    titulos = [t for t, _ in SECOES]
    escreve('aula05.html', secoes_html(SECOES), secoes=titulos,
            subtitulo='F = dp/dt é a forma original da segunda lei, e F = ma é '
                      'o caso particular de massa constante. Tudo o que este '
                      'módulo tem de difícil, do foguete à corrente que cai '
                      'sobre a mesa, mora exatamente nessa distinção.')


if __name__ == '__main__':
    main()
