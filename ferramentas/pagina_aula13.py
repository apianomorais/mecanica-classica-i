# -*- coding: utf-8 -*-
"""Módulo 13: sistemas de partículas, colisões e espalhamento.

Fecha o curso. A terceira lei, que apareceu no módulo 2 como enunciado,
volta aqui como ferramenta: é ela que permite tratar um sistema inteiro
como se fosse um ponto.
"""
from molde import escreve, secoes_html
import exercicios
from lista_aula13 import LISTA

S1 = r'''
<p>Até aqui, quase tudo foi uma partícula só, ou duas. Um sistema de
\(N\) partículas parece outro problema, com \(N\) equações acopladas e
nenhuma esperança de solução. E é mesmo, em geral. Mas algumas perguntas
sobre o sistema inteiro têm resposta sem que se resolva nada.</p>

<p>Some as \(N\) equações de movimento. Cada partícula sofre forças de
todas as outras, mais uma força externa:</p>

\[ m_i\ddot{\vet{r}}_i = \vet{F}_i^{\text{ext}}
   + \sum_{j \neq i}\vet{F}_{ij}. \]

<p>Na soma sobre \(i\), o termo \(\vet{F}_{ij}\) aparece junto com
\(\vet{F}_{ji}\), e pela terceira lei os dois se cancelam. <em>Todas</em>
as forças internas somem, aos pares, por mais complicadas que sejam.
Definindo a posição do centro de massa,</p>

<div class="bloco def">
<p class="rotulo">O teorema do centro de massa</p>
\[ \vet{R} = \frac{1}{M}\sum_i m_i\vet{r}_i, \qquad M = \sum_i m_i
   \quad\Longrightarrow\quad
   M\ddot{\vet{R}} = \vet{F}^{\text{ext}}_{\text{total}}. \]
<p>O centro de massa se move como uma única partícula de massa \(M\) sob a
resultante das forças externas. Nada do que acontece dentro do sistema
interfere nisso.</p>
</div>

<div data-widget="particulas"></div>

<p>O programa testa isso com seis partículas ligadas por molas entre todos
os pares, mais uma repulsão em \(1/r^2\), caindo num campo de gravidade.
As trajetórias individuais são um emaranhado. O centro de massa percorre
19 m numa parábola, e se afasta da parábola prevista em
\(3\times10^{-14}\) m.</p>

<div class="bloco alerta">
<p class="rotulo">Quando refinar o passo piora</p>
<p>Esse desvio <strong>cresce</strong> quando o passo de integração
diminui: \(3\times10^{-14}\) com \(dt = 2\times10^{-4}\) e
\(2\times10^{-13}\) com \(dt = 5\times10^{-5}\). É o contrário do que
acontece em todo o resto do curso, e não é defeito. O teorema do centro de
massa é exato: não há erro de truncamento a reduzir, e o que resta é
arredondamento, que se acumula com o número de passos. Quando uma conta já
está certa até a última casa, refiná-la só a piora.</p>
</div>

<p>Sem força externa, \(\ddot{\vet{R}} = 0\), e o momento total
\(\vet{P} = M\dot{\vet{R}}\) se conserva. Essa é a lei de conservação mais
geral da mecânica newtoniana, e ela não depende de o sistema ser rígido,
elástico, dissipativo, ou coisa alguma. Depende só da terceira lei.</p>
'''

S2 = r'''
<p>Há um referencial em que tudo fica mais simples, e vale a pena mudar
para ele antes de qualquer conta de colisão: o que viaja com o centro de
massa. Nele, por construção, o momento total é zero.</p>

<p>Para duas partículas, escreva as velocidades como a do centro de massa
mais o resto. A energia cinética se separa em duas parcelas que não se
misturam:</p>

<div class="bloco def">
<p class="rotulo">A energia cinética se parte em duas</p>
\[ K = \underbrace{\frac{MV^2}{2}}_{\text{do centro de massa}}
     + \underbrace{\frac{\mu v_{\text{rel}}^2}{2}}_{\text{do movimento relativo}},
  \qquad \mu = \frac{m_1m_2}{m_1+m_2}. \]
<p>Os termos cruzados se cancelam, e a massa reduzida do módulo 6 reaparece
aqui sem ter sido convidada.</p>
</div>

<p>Essa separação decide, sozinha, quanta energia uma colisão pode
dissipar. A primeira parcela é intocável: o momento total se conserva, logo
\(V\) não muda, logo \(MV^2/2\) não muda. Só a segunda parcela está
disponível. Mesmo numa batida em que os dois corpos saem grudados, sobra
\(MV^2/2\), e sobra porque a conservação do momento obriga.</p>

<p>No referencial do centro de massa isso fica visível: os dois momentos
são sempre opostos, antes e depois, e a colisão elástica é apenas uma
<strong>reflexão</strong> do vetor velocidade relativa, que mantém o módulo
e muda a direção. O problema de duas incógnitas vira um problema de um
ângulo.</p>
'''

S3 = r'''
<p>Na colisão unidimensional, a conservação do momento dá uma equação e
faltam duas incógnitas. A segunda equação é empírica, e se escreve com o
<strong>coeficiente de restituição</strong>:</p>

\[ v_2 - v_1 = -e\,(u_2-u_1), \qquad 0 \leq e \leq 1. \]

<p>A velocidade relativa inverte de sinal e encolhe por um fator \(e\).
Com \(e = 1\) ela só inverte, e a colisão é elástica; com \(e = 0\) os dois
corpos saem juntos. Resolvendo as duas equações:</p>

\[ v_1 = \frac{m_1u_1+m_2u_2 + m_2e\,(u_2-u_1)}{M}, \qquad
   v_2 = \frac{m_1u_1+m_2u_2 + m_1e\,(u_1-u_2)}{M}. \]

<p>E a energia perdida sai da seção anterior sem esforço nenhum: a colisão
retira do movimento relativo a fração \(1-e^2\), e o centro de massa não é
tocado.</p>

\[ \Delta K = \frac{\mu\,v_{\text{rel}}^2}{2}\left(1-e^2\right). \]

<p>O programa confere isso com \(m_1 = 2\) kg a \(+5\) m/s contra
\(m_2 = 3\) kg a \(-1\) m/s:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>\(e\)</th><th>\(v_1\)</th><th>\(v_2\)</th>
<th>\(K_f/K_i\)</th><th>perda prevista</th><th>perda medida</th></tr></thead>
<tbody>
<tr><td>1,0</td><td>−2,20</td><td>+3,80</td><td>1,000000</td>
<td>0,0 J</td><td>0,0 J</td></tr>
<tr><td>0,8</td><td>−1,48</td><td>+3,32</td><td>0,706566</td>
<td>7,776 J</td><td>7,776 J</td></tr>
<tr><td>0,5</td><td>−0,40</td><td>+2,60</td><td>0,388679</td>
<td>16,200 J</td><td>16,200 J</td></tr>
<tr><td>0,0</td><td>+1,40</td><td>+1,40</td><td>0,184906</td>
<td>21,600 J</td><td>21,600 J</td></tr>
</tbody>
</table>
</div>

<p>Na última linha os dois saem com a mesma velocidade, que é a do centro
de massa, e ainda assim 18,5 % da energia inicial sobrevive. Essa é a
parcela que o momento protege.</p>

<div class="bloco fisica">
<p class="rotulo">O que o \(e\) esconde</p>
<p>O coeficiente de restituição não é uma propriedade do material, por mais
que as tabelas o apresentem assim. Ele depende da velocidade do impacto, da
geometria dos corpos, da temperatura, e cai quando a batida é mais forte,
porque a deformação plástica aumenta. Usá-lo é admitir que não se vai olhar
para dentro da colisão: é um parâmetro de ignorância, útil e honesto,
contanto que não se finja que é constante.</p>
</div>
'''

S4 = r'''
<p>Em duas dimensões, a conservação do momento dá duas equações e as
incógnitas são quatro. Falta uma informação, que é o parâmetro de impacto,
ou equivalentemente o ângulo de espalhamento no referencial do centro de
massa. Fixado esse ângulo, tudo o mais se determina.</p>

<p>Um caso vale ser memorizado. Duas massas <strong>iguais</strong>, uma
delas parada, em colisão elástica. A conservação do momento dá
\(\vet{u} = \vet{v}_1+\vet{v}_2\) e a da energia dá
\(u^2 = v_1^2+v_2^2\). Elevando a primeira ao quadrado e comparando:</p>

\[ \vet{v}_1\cdot\vet{v}_2 = 0. \]

<div class="destaque">
<p>Massas iguais, colisão elástica, alvo parado: os dois saem em ângulo
reto, qualquer que seja o quanto a batida foi de raspão.</p>
</div>

<p>O programa verifica para cinco ângulos de espalhamento diferentes, e o
produto escalar dá \(10^{-16}\) em todos. Com massas diferentes o ângulo
deixa de ser reto imediatamente: \(76{,}9°\) com um alvo de metade da massa
e \(103{,}1°\) com um alvo do dobro, para a mesma batida. Uma fotografia de
câmara de bolhas, com dois rastros a 90°, está dizendo que as duas
partículas têm a mesma massa.</p>

<h3>Laboratório e centro de massa</h3>

<p>Traduzir o ângulo de um referencial para o outro é somar a velocidade do
centro de massa, o que dá</p>

\[ \tg\theta_{\text{lab}} =
   \frac{\sen\theta_{\text{cm}}}{\cos\theta_{\text{cm}} + m_1/m_2}. \]

<div class="tabela-rolavel">
<table>
<thead><tr><th>\(m_1/m_2\)</th><th>\(\theta_{\text{cm}}=60°\)</th>
<th>\(120°\)</th><th>\(180°\)</th><th>\(\theta_{\text{lab}}\) máximo</th></tr></thead>
<tbody>
<tr><td>0,2</td><td>51,05°</td><td>109,11°</td><td>180,00°</td><td>180°</td></tr>
<tr><td>1,0</td><td>30,00°</td><td>60,00°</td><td>90,00°</td><td>90°</td></tr>
<tr><td>2,0</td><td>19,11°</td><td>30,00°</td><td>0,00°</td><td>30,00°</td></tr>
<tr><td>5,0</td><td>8,95°</td><td>10,89°</td><td>0,00°</td><td>11,54°</td></tr>
</tbody>
</table>
</div>

<p>A coluna de \(180°\) merece ser lida devagar. Para um projétil mais
pesado que o alvo ela dá <strong>zero</strong>: bater de frente e voltar no
referencial do centro de massa significa, no laboratório, seguir em frente,
só que mais devagar. O recuo só chega ao laboratório quando o alvo é
pesado o bastante.</p>

<p>E há um teto. Quando \(m_1 &gt; m_2\), o denominador nunca troca de
sinal, e o ângulo de laboratório não passa de</p>

\[ \sen\theta_{\max} = \frac{m_2}{m_1}. \]

<p>Uma bola de boliche não volta de um pino, por mais perfeita que seja a
pontaria. Guarde isso para a seção seguinte.</p>
'''

S5 = r'''
<p>Espalhamento é a colisão vista de longe: não se observa o que acontece
no encontro, apenas por onde a partícula entrou e por onde saiu. Foi assim
que o núcleo atômico foi descoberto, e continua sendo assim que se estuda
tudo o que é pequeno demais para ser visto.</p>

<p>Uma partícula de carga positiva vinda do infinito contra um núcleo
também positivo segue uma órbita do módulo 12 com energia positiva: uma
hipérbole. O ângulo de deflexão é o ângulo entre as assíntotas, e a mesma
equação da órbita dá</p>

\[ \tg\frac{\theta}{2} = \frac{k}{m v_\infty^2\,b}, \]

<p>com \(b\) o parâmetro de impacto. O programa integra as trajetórias e
confere:</p>

<div class="tabela-rolavel">
<table>
<thead><tr><th>\(b\)</th><th>\(\theta\) medido</th><th>\(\theta\) previsto</th>
<th>diferença</th></tr></thead>
<tbody>
<tr><td>0,20</td><td>2,74671</td><td>2,74680</td><td>\(9{,}6\times10^{-5}\)</td></tr>
<tr><td>1,00</td><td>1,57055</td><td>1,57080</td><td>\(2{,}5\times10^{-4}\)</td></tr>
<tr><td>5,00</td><td>0,39469</td><td>0,39479</td><td>\(9{,}6\times10^{-5}\)</td></tr>
<tr><td>10,00</td><td>0,19929</td><td>0,19934</td><td>\(5{,}0\times10^{-5}\)</td></tr>
</tbody>
</table>
</div>

<div class="bloco alerta">
<p class="rotulo">A diferença não é erro de integrador</p>
<p>Ela cai exatamente como \(1/r_{\text{ini}}\): dobrando a distância de
onde a partícula parte, o desvio cai pela metade, em todas as linhas. É o
preço de medir em distância finita um ângulo que só existe no infinito. O
impulso que falta receber depois de \(r_{\text{ini}}\) é a integral de
\(k/r^2\,dt\), que vale \(k/mv\,r_{\text{ini}}\). Uma força de alcance
infinito não deixa a partícula livre em lugar nenhum, e isso vai importar
daqui a dois parágrafos.</p>
</div>

<h3>A seção de choque</h3>

<p>Num experimento não se escolhe \(b\): o feixe chega com todos os
parâmetros de impacto, e o que se conta é quantas partículas saem em cada
direção. Partículas que entram num anel de raio \(b\) e espessura \(db\)
saem num anel de ângulo \(\theta\) e espessura \(d\theta\), de modo que</p>

\[ \der{\sigma}{\Omega}
   = \frac{b}{\sen\theta}\left|\der{b}{\theta}\right|. \]

<p>Com \(b = (k/mv^2)\cotg(\theta/2)\), a derivada sai em três linhas e
dá a fórmula de Rutherford:</p>

<div class="bloco def">
<p class="rotulo">A seção de choque de Rutherford</p>
\[ \der{\sigma}{\Omega}
   = \left(\frac{k}{2mv_\infty^2}\right)^2
     \frac{1}{\sen^4(\theta/2)}. \]
</div>

<p>O programa monta a seção de choque numericamente, derivando \(b(\theta)\)
nas trajetórias integradas, e compara: a razão vale 1 em três casas ao
longo de quatro ordens de grandeza da seção de choque, de
\(2{,}6\times10^{-1}\) a \(2{,}0\times10^{3}\).</p>

<p>Repare que a integral dessa expressão sobre todos os ângulos
<strong>diverge</strong> em \(\theta \to 0\). A seção de choque total de
Rutherford é infinita, e o motivo é o do bloco acima: alcance infinito. Num
alvo real a divergência some, porque a partir do raio atômico os elétrons
blindam o núcleo e o potencial deixa de ser \(1/r\).</p>

<div class="bloco fisica">
<p class="rotulo">1911</p>
<p>No átomo de Thomson a carga positiva estava espalhada por todo o volume,
e o campo interno era fraco: nenhuma partícula alfa poderia ser desviada de
mais do que uma fração de grau. Geiger e Marsden encontraram uma em oito
mil voltando para trás. Pela seção 4, voltar para trás exige um alvo mais
pesado que o projétil, e pelo \(1/\sen^4\) exige que o campo continue
crescendo até distâncias muito pequenas: o alvo tinha de ser pesado,
concentrado e minúsculo. Rutherford comparou o resultado a atirar uma
granada numa folha de papel e vê-la ricochetear. A conta que ele fez para
se convencer é, essencialmente, a desta seção.</p>
</div>
'''

S6 = r'''
<div class="cartoes">
  <a class="cartao" href="codigo/particulas.py">
    <span class="numero">Programa</span>
    <h3>particulas.py</h3>
    <p>Integra seis partículas com forças internas emaranhadas e segue o
    centro de massa, resolve a colisão com restituição, verifica os 90° das
    massas iguais, traduz entre laboratório e centro de massa, e monta a
    seção de choque de Rutherford a partir das trajetórias.</p>
  </a>
</div>

<p><strong>O que ele imprime, e o que conferir.</strong></p>

<ul>
<li>O centro de massa segue a parábola prevista com desvio de
\(3\times10^{-14}\) m em 19 m de voo, e o desvio cresce quando o passo
diminui, porque só resta arredondamento.</li>
<li>O momento total, sem campo externo, muda de \(8\times10^{-15}\) em
valor relativo.</li>
<li>A perda de energia na colisão bate com \(\mu v_{\text{rel}}^2(1-e^2)/2\)
em todas as casas impressas.</li>
<li>O produto escalar das velocidades finais, para massas iguais, dá
\(10^{-16}\) em qualquer ângulo.</li>
<li>O desvio de Rutherford bate com a fórmula, e a diferença cai como
\(1/r_{\text{ini}}\), com razão 2,000 em cada linha.</li>
<li>A seção de choque medida dá a fórmula em três casas.</li>
</ul>

<div class="bloco ex">
<p><strong>Para mexer.</strong> Troque a repulsão por atração, mudando o
sinal de \(k\), e refaça o leque: o desvio muda de sentido e aparecem
trajetórias que dão a volta. Depois ponha o expoente da força em 2,5 e
meça a seção de choque: o \(1/\sen^4(\theta/2)\) some, e é essa
sensibilidade que faz do espalhamento um instrumento. Por fim, implemente a
colisão de três corpos alinhados, solte-os com um pequeno desencontro e
confirme que o centro de massa continua sem tomar conhecimento.</p>
</div>

<div class="bloco fisica">
<p class="rotulo">Fim do curso, e o que vem depois</p>
<p>O curso começou com \(\vet{F} = m\vet{a}\) e termina usando a terceira
lei para falar de um sistema inteiro sem resolvê-lo. O padrão se repetiu:
quase sempre, o que deu resposta não foi integrar a equação de movimento, e
sim encontrar a quantidade que não muda. Energia no módulo 4, momento
angular no 12, momento total aqui.</p>
<p>Mecânica Clássica II vira esse padrão do avesso. Em vez de procurar as
constantes depois de escrever as forças, parte-se de uma única função
escalar e as constantes aparecem como consequência das simetrias que ela
tem. A órbita de Kepler, que custou uma aula inteira aqui, sai lá em uma
página; o pêndulo duplo, que é impensável com forças de vínculo, fica
tratável. Vale ter este curso perto quando aquele começar: o formalismo
novo só convence quem já sabe quanto trabalho ele está poupando.</p>
</div>
'''

SECOES = [
    ('A terceira lei, e o centro de massa', S1),
    ('O referencial que simplifica tudo', S2),
    ('Colisões, e a energia que o momento protege', S3),
    ('Duas dimensões, e os 90° das massas iguais', S4),
    ('Espalhamento: de Rutherford ao núcleo', S5),
    ('No Spyder', S6),
]

SECOES.append(('Exercícios propostos', exercicios.bloco(LISTA)))


def main():
    titulos = [t for t, _ in SECOES]
    escreve('aula13.html', secoes_html(SECOES), secoes=titulos,
            subtitulo='Somadas as equações de movimento, as forças internas '
                      'se cancelam aos pares e sobra uma única equação para o '
                      'centro de massa. Dela saem a conservação do momento, a '
                      'teoria das colisões e, no limite em que só se observa '
                      'quem entra e quem sai, o espalhamento que revelou o '
                      'núcleo atômico.')


if __name__ == '__main__':
    main()
