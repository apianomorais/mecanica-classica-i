# -*- coding: utf-8 -*-
"""Módulo 2: as leis de Newton e os referenciais inerciais."""
from molde import escreve, secoes_html
import exercicios
from lista_aula02 import LISTA

W = 'https://pt.wikipedia.org/wiki/'

S1 = r'''
<p>As três leis estão em toda parte, inclusive na memória de quem chega a esta
disciplina, e é justamente por isso que vale lê-las devagar. A pergunta que
organiza esta seção não é o que cada uma diz, e sim <em>o que cada uma faz</em>:
qual delas afirma um fato sobre o mundo, qual define um conceito, e qual pode
ser testada.</p>

<h3>A primeira lei</h3>

<blockquote>Todo corpo permanece em repouso ou em movimento retilíneo uniforme,
a menos que seja obrigado a mudar esse estado por forças aplicadas sobre
ele.</blockquote>

<p>A leitura preguiçosa diz que a primeira lei é o caso particular da segunda
com \(\vet{F} = 0\). Se fosse só isso, ela não precisaria existir.</p>

<p>O que ela afirma, de fato, é que <strong>existe pelo menos um referencial em
que isso acontece</strong>. Num vagão que freia, um corpo solto acelera para a
frente sem que força alguma atue sobre ele, e a primeira lei é falsa ali. A
primeira lei, portanto, não é uma equação: é a seleção dos referenciais em que
as outras duas podem ser usadas. Esses referenciais são os
<strong>inerciais</strong>.</p>

<div class="bloco def">
<span class="rotulo">A definição que não é circular</span>
<p>Há um incômodo lógico conhecido: referencial inercial é aquele em que vale a
primeira lei, e a primeira lei vale nos referenciais inerciais. A saída é
operacional, e não lógica: procura-se um referencial em que corpos distantes de
tudo se movam em linha reta, e verifica-se que a escolha funciona para todos os
corpos ao mesmo tempo. Se um único referencial serve para a Lua, para um
pêndulo e para um próton, ele não foi escolhido por conveniência.</p>
<p>Na prática, o referencial das estrelas distantes serve muito bem, e a
questão de por que ele serve é profunda o bastante para ter nome próprio:
<a href="%(W)sPrinc%%C3%%ADpio_de_Mach">princípio de Mach</a>.</p>
</div>

<h3>A segunda lei</h3>

\[ \vet{F} = \der{\vet{p}}{t}, \qquad \vet{p} = m\vet{v}. \]

<p>Escrita com o momento, e não como \(\vet{F} = m\vet{a}\), ela cobre também
os casos de massa variável, que o módulo 5 trata com o foguete.</p>

<p>Há aqui uma armadilha filosófica que vale enfrentar. Se força for
<em>definida</em> como \(m\vet{a}\), a segunda lei não afirma nada: é uma
definição disfarçada. O que a salva é que as forças têm leis próprias e
independentes: a gravitação dá \(GMm/r^2\), a mola dá \(-kx\), o arrasto dá
\(-kv^2\). Medindo a força por um caminho e a aceleração por outro, a igualdade
vira uma afirmação testável sobre o mundo, e é testada o tempo todo.</p>

<h3>A terceira lei</h3>

<p>Na <strong>forma fraca</strong>, as forças entre dois corpos são iguais em
módulo e opostas em sentido. Na <strong>forma forte</strong>, elas ainda são
dirigidas ao longo da linha que une os dois.</p>

<p>A forma fraca garante a conservação do momento linear, assunto do módulo 5.
A forma forte é necessária para a conservação do momento angular, e é satisfeita
pela gravitação e pela eletrostática.</p>

<div class="bloco alerta">
<span class="rotulo">Onde a terceira lei falha</span>
<p>A força magnética entre duas cargas em movimento não obedece à terceira lei,
nem na forma fraca. Duas cargas movendo-se perpendicularmente uma à outra
exercem forças que não são opostas, e a soma dos momentos das duas partículas
não se conserva.</p>
<p>A física não quebra: o que falta está guardado no campo eletromagnético, que
também carrega momento. O
<a href="https://apianomorais.github.io/eletromagnetismo/cap08.html">capítulo 8
de Eletromagnetismo</a> faz essa contabilidade, e a conclusão é que a terceira
lei é uma aproximação excelente enquanto a propagação puder ser tratada como
instantânea.</p>
</div>
''' % {'W': W}

S2 = r'''
<p>Na segunda lei, a massa aparece como medida da resistência à aceleração. Na
lei da gravitação, ela aparece como medida da intensidade da atração. Não há
nenhuma razão óbvia para que sejam o mesmo número.</p>

\[ m_{\text{inercial}}\vet{a} = \vet{F},
   \qquad
   \vet{F}_{\text{grav}} = m_{\text{grav}}\,\vet{g}. \]

<p>Se as duas fossem diferentes, corpos de materiais diferentes cairiam com
acelerações diferentes, porque</p>

\[ \vet{a} = \frac{m_{\text{grav}}}{m_{\text{inercial}}}\,\vet{g}. \]

<p>A experiência diz que não caem, e diz isso com uma precisão espantosa.</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>experimento</th><th>quando</th>
<th>limite para \(\left|m_g/m_i - 1\right|\)</th></tr></thead>
<tbody>
<tr><td>Galileu, planos inclinados</td><td>1600</td><td>\(10^{-2}\)</td></tr>
<tr><td>Newton, pêndulos de materiais diferentes</td><td>1686</td>
    <td>\(10^{-3}\)</td></tr>
<tr><td><a href="%(W)sLor%%C3%%A1nd_E%%C3%%B6tv%%C3%%B6s">Eötvös</a>, balança de
    torção</td><td>1909</td><td>\(5\times10^{-9}\)</td></tr>
<tr><td>Dicke e Braginsky</td><td>1964 e 1972</td><td>\(10^{-12}\)</td></tr>
<tr><td>MICROSCOPE, em órbita</td><td>2022</td><td>\(10^{-15}\)</td></tr>
</tbody>
</table>
</div>

<div class="bloco fisica">
<span class="rotulo">O que Einstein fez com isso</span>
<p>Um fato experimental verificado em quinze casas decimais merece ser elevado
a princípio. Einstein fez exatamente isso: se as duas massas são iguais em toda
parte, então nenhuma experiência local distingue estar num campo gravitacional
uniforme de estar num referencial acelerado. É o
<a href="%(W)sPrinc%%C3%%ADpio_da_equival%%C3%%AAncia">princípio da
equivalência</a>, e dele saiu a relatividade geral.</p>
<p>Repare no caminho: a igualdade entre as duas massas é, na mecânica
newtoniana, uma coincidência sem explicação. Na relatividade geral ela deixa de
ser coincidência, porque não há força gravitacional nenhuma, apenas movimento
livre num espaço-tempo curvo. Uma teoria explica o que a outra apenas
constata.</p>
</div>
''' % {'W': W}

S3 = r'''
<p>Nenhum laboratório na Terra é inercial, e vale saber o tamanho do erro que
se comete ao fingir que é. São três efeitos, e o programa do módulo mede os
três.</p>

<h3>A rotação diária</h3>

<p>Com \(\omega = 7{,}292\times10^{-5}\ \mathrm{rad/s}\) e
\(R = 6{,}378\times10^{6}\ \mathrm{m}\), a aceleração centrípeta no equador
vale</p>

\[ \omega^2R = 0{,}0339\ \mathrm{m/s^2}, \]

<p>isto é, <strong>0,35 %</strong> de \(g\). É por isso que a gravidade medida
varia com a latitude, e o efeito é do tamanho de uma balança de banheiro
perceber.</p>

<div class="destaque">
<p><strong>Exemplo trabalhado: a balança que viaja.</strong> A fórmula
internacional da gravidade, que inclui a rotação e o achatamento da Terra,
dá</p>

\[ g(3{,}72^\circ\mathrm{S}) = 9{,}78054\ \mathrm{m/s^2}
   \quad\text{(Fortaleza)}, \]
\[ g(60{,}17^\circ\mathrm{N}) = 9{,}81931\ \mathrm{m/s^2}
   \quad\text{(Helsinque)}. \]

<p>Uma balança calibrada em Fortaleza e levada a Helsinque marca, para um corpo
de 70 kg,</p>

\[ \Delta m = 70\left(\frac{9{,}81931}{9{,}78054}-1\right)
   = 0{,}277\ \mathrm{kg}, \]

<p>quase 280 gramas a mais. A massa não mudou; o que mudou foi o peso, e a
balança mede peso.</p>

<p><strong>E quanto disso é rotação?</strong> O programa separa as duas causas.
O modelo de uma linha, só com a força centrífuga, reproduz
<strong>65 %</strong> da variação medida entre o equador e o polo, com a
dependência correta em \(\cos^2\) da latitude. O terço restante é o achatamento:
o raio equatorial é 21 km maior que o polar, e só isso já muda \(g\) em
0,018 m/s².</p>
</div>

<h3>A deflexão de Coriolis</h3>

<p>Num referencial girante aparece, além da centrífuga, uma força que depende da
velocidade:</p>

\[ \vet{F}_{\text{Coriolis}} = -2m\,\vet{\omega}\cruz\vet{v}. \]

<p>Um corpo solto de uma torre cai desviado para <em>leste</em>, porque no alto
ele tem velocidade tangencial maior que a do solo. A conta de primeira ordem
dá</p>

\[ d = \frac{1}{3}\,\omega g t^3\cos\lambda,
   \qquad t = \sqrt{\frac{2h}{g}}. \]

<p>Para 100 m de queda no Crato, isso dá <strong>2,2 cm</strong>, e o programa
confirma integrando as equações completas no referencial girante, sem
aproximação. De 300 m, o desvio passa de 11 cm.</p>

<h3>O pêndulo de Foucault</h3>

<p>O plano de oscilação de um pêndulo longo gira com
\(\omega\sen\lambda\), de modo que o período de precessão é</p>

\[ T_{\text{prec}} = \frac{23{,}93\ \mathrm{h}}{\sen\lambda}. \]

<div class="tabela-rolavel">
<table>
<thead><tr><th>lugar</th><th>latitude</th><th>período</th></tr></thead>
<tbody>
<tr><td>Polo</td><td>90°</td><td>23,9 h</td></tr>
<tr><td>Paris, onde Foucault fez em 1851</td><td>48,85°</td><td>31,8 h</td></tr>
<tr><td>São Paulo</td><td>23,55° S</td><td>59,9 h</td></tr>
<tr><td>Crato</td><td>7,23° S</td><td>190,2 h, quase 8 dias</td></tr>
<tr><td>Equador</td><td>0°</td><td>não gira</td></tr>
</tbody>
</table>
</div>

<p>Perto do equador a demonstração é desconfortável, e é essa a razão de não
haver um pêndulo de Foucault em toda praça do Nordeste.</p>

<div class="bloco def">
<span class="rotulo">Quando a Terra pode ser tratada como inercial</span>
<p>Os três efeitos têm tamanhos muito diferentes do caso para caso, e o critério
é comparar o tempo do experimento com o dia sideral. Experimento que dura
segundos, como uma queda de laboratório ou uma colisão de carrinhos, não sente
nada. Experimento que dura horas, como um pêndulo longo, sente. E movimento que
dura dias e percorre milhares de quilômetros, como uma massa de ar, é
<em>dominado</em> pela Coriolis: é ela que organiza os ciclones.</p>
</div>
'''

S4 = r'''
<p>Toda a parte prática deste módulo cabe num procedimento de quatro passos,
que parece burocrático até o dia em que o problema fica complicado.</p>

<div class="bloco def">
<span class="rotulo">O método</span>
<ol>
<li><strong>Escolha o corpo.</strong> Um de cada vez, e desenhe só ele, solto
de tudo.</li>
<li><strong>Desenhe as forças que agem <em>sobre</em> ele</strong>, e apenas
essas. Força que o corpo faz em outro não entra no diagrama dele.</li>
<li><strong>Escolha os eixos</strong>, de preferência com um deles na direção
do movimento ou da aceleração esperada.</li>
<li><strong>Escreva \(\vet{F} = m\vet{a}\) componente a componente</strong>, e
só então resolva.</li>
</ol>
</div>

<div class="destaque">
<p><strong>Exemplo trabalhado: o bloco no plano inclinado.</strong> Um bloco de
massa \(m\) desce um plano de inclinação \(\theta\), com coeficiente de atrito
cinético \(\mu\).</p>

<p><strong>Passo 2.</strong> Três forças agem sobre o bloco: o peso
\(m\vet{g}\), a normal \(\vet{N}\) e o atrito \(\vet{f}\), contrário ao
movimento.</p>

<p><strong>Passo 3.</strong> Eixos ao longo do plano e perpendicular a ele, e
não horizontal e vertical. É a escolha que faz a aceleração ter uma componente
só.</p>

<p><strong>Passo 4.</strong> Perpendicular ao plano não há aceleração:</p>

\[ N - mg\cos\theta = 0 \;\Longrightarrow\; N = mg\cos\theta. \]

<p>Ao longo do plano,</p>

\[ mg\sen\theta - \mu N = ma
   \;\Longrightarrow\;
   \boxed{\;a = g\left(\sen\theta - \mu\cos\theta\right).\;} \]

<p><strong>Três leituras.</strong> A massa sumiu, de modo que todos os blocos
descem igual, qualquer que seja o material (desde que \(\mu\) seja o mesmo). A
aceleração zera quando \(\tg\theta = \mu\), o que dá um jeito prático de medir
coeficiente de atrito: incline até escorregar e meça o ângulo. E para
\(\tg\theta \lt \mu\) a fórmula dá número negativo, o que não significa que o
bloco sobe: significa que ele fica parado, segurado pelo atrito estático, que é
outra força com outra lei.</p>

<p><strong>A conferência.</strong> O programa resolve o mesmo problema pelo
teorema trabalho-energia, sem diagrama nenhum, e os dois resultados coincidem
em \(10^{-16}\) nos quatro casos testados. Diagrama de corpo livre e balanço de
energia são a mesma física escrita de duas maneiras.</p>
</div>

<h3>E quando o referencial acelera</h3>

<p>Dentro de um vagão que acelera com \(\vet{A}\), a segunda lei deixa de valer
na forma de sempre. Ela volta a valer com um termo a mais:</p>

\[ m\vet{a}' = \vet{F} - m\vet{A}, \]

<p>em que \(\vet{a}'\) é a aceleração medida dentro do vagão. O termo
\(-m\vet{A}\) é a <strong>força de inércia</strong>, e ela tem uma propriedade
que delata a sua natureza: é proporcional à massa do corpo, exatamente como a
gravidade. Daí o princípio da equivalência da seção 2.</p>

<p>O programa mede o estrago de esquecê-la: uma partícula livre com
\(v_0 = 1\) m/s, num vagão que acelera a 3 m/s², é vista 4,0 m <em>atrás</em>
de onde partiu depois de dois segundos. Quem usa a segunda lei sem o termo de
inércia prevê \(+2{,}0\) m, errando <strong>6 metros</strong>, que é exatamente
\(\frac12AT^2\).</p>

<p>O componente abaixo mostra as duas descrições do mesmo movimento. Repare que
a bola nunca é tocada por nada: o que muda de um painel para o outro é apenas
quem está parado na tela.</p>

<div data-widget="referenciais"></div>

<p>Vale olhar o caso \(A = 0\), que é o referencial inercial de volta: os dois
painéis ficam idênticos e a seta vinho desaparece. A força de inércia não é
uma força da natureza, e sim o preço de insistir em usar \(\vet{F} = m\vet{a}\)
onde ela não vale.</p>
'''

S5 = r'''
<div class="cartoes">
  <a class="cartao" href="codigo/referenciais.py">
    <span class="numero">Programa</span>
    <h3>referenciais.py</h3>
    <p>Resolve o plano inclinado pelos dois caminhos, compara os dois
    referenciais, mede a variação de g com a latitude, integra a deflexão de
    Coriolis e calcula o pêndulo de Foucault em cinco lugares.</p>
  </a>
</div>

<p><strong>O que ele imprime, e o que conferir.</strong></p>

<ul>
<li>A aceleração no plano inclinado, pelo diagrama e pela energia, coincide em
\(10^{-16}\) nos quatro casos.</li>
<li>No referencial acelerado, a trajetória calculada com a força de inércia
reproduz a transformação \(x - \frac12At^2\) em \(3\times10^{-5}\) m, que é o
erro do integrador e não da física; sem a força de inércia, o erro é de
6 metros.</li>
<li>O modelo centrífugo explica <strong>65 %</strong> da variação de \(g\) entre
o equador e o polo, com a razão constante em todas as latitudes, o que mostra
que a dependência angular está certa e falta apenas um fator.</li>
<li>O desvio para leste calculado pela fórmula de primeira ordem e o obtido
integrando as equações completas coincidem em todos os casos.</li>
</ul>

<div class="bloco ex">
<span class="rotulo">Um detalhe do método numérico</span>
<p>A integração da queda no referencial girante usa passo de \(10^{-4}\) s e
para quando o corpo cruza o chão, sem interpolar. Isso basta aqui porque o
desvio é lido em centímetros e o erro de um passo é micrométrico. No módulo 3,
em que o alcance é a grandeza medida, essa mesma economia arruinaria a medida
da ordem do método, e lá foi preciso interpolar com cuidado. O rigor que um
cálculo exige depende do que se vai fazer com o resultado.</p>
</div>
'''

SECOES = [
    ('As três leis, lidas devagar', S1),
    ('As duas massas, e por que são iguais', S2),
    ('Quanto a Terra não é inercial', S3),
    ('Diagramas de corpo livre', S4),
    ('No Spyder', S5),
]

SECOES.append(('Exercícios propostos', exercicios.bloco(LISTA)))


def main():
    titulos = [t for t, _ in SECOES]
    escreve('aula02.html', secoes_html(SECOES), secoes=titulos,
            subtitulo='A primeira lei não é um caso particular da segunda: ela '
                      'escolhe os referenciais em que a segunda pode ser usada. '
                      'Este módulo lê as três leis com cuidado, mede o quanto a '
                      'Terra não é um desses referenciais, e monta o método que '
                      'resolve problemas de força pelo resto do curso.')


if __name__ == '__main__':
    main()
