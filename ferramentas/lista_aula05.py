# -*- coding: utf-8 -*-
"""Exercícios propostos do módulo 5."""

LISTA = [
    ('5.1  O airbag não absorve energia: ele compra tempo',
     r'''Uma pessoa de 75 kg viaja a 50 km/h. Calcule o impulso que precisa
     ser aplicado para pará-la e, a partir dele, a força média em três
     situações: parada contra uma superfície rígida em 2 ms, contra um airbag
     em 50 ms, e com a zona de deformação do carro trabalhando por 300 ms.
     Explique por que a energia cinética é a mesma nos três casos e ainda
     assim só um deles é sobrevivível.''',
     r'''<p><b>O impulso.</b> \(v = 50/3{,}6 = 13{,}9\) m/s, de modo que</p>
     <p>\[ J = m v = 75 \times 13{,}9 = 1050\ \mathrm{N\,s}. \]</p>
     <p>Esse número não depende de como a parada acontece. É a quantidade de
     movimento que existe e que precisa ser retirada, e nenhum dispositivo a
     diminui.</p>
     <p><b>As três forças.</b> \(\bar{F} = J/\Delta t\):</p>
     <div class="tabela-rolavel">
     <table>
     <thead><tr><th>situação</th><th>\(\Delta t\)</th><th>\(\bar F\)</th>
     <th>em pesos do corpo</th></tr></thead>
     <tbody>
     <tr><td>superfície rígida</td><td>2 ms</td><td>525 kN</td><td>714 \(g\)</td></tr>
     <tr><td>airbag</td><td>50 ms</td><td>21 kN</td><td>29 \(g\)</td></tr>
     <tr><td>zona de deformação</td><td>300 ms</td><td>3,5 kN</td><td>4,8 \(g\)</td></tr>
     </tbody>
     </table>
     </div>
     <p><b>Por que só um sobrevive.</b> O corpo humano não é danificado por
     energia e sim por <em>força por unidade de área</em>: ossos quebram em
     tensão, órgãos se rompem em desaceleração. A tolerância fica na casa de
     algumas dezenas de \(g\) por frações de segundo. Os 714 \(g\) da primeira
     linha são letais; os 4,8 \(g\) da terceira são um susto.</p>
     <p><b>A lição de projeto.</b> Como \(J\) está fixo, a única variável de
     projeto é \(\Delta t\). Airbag, capacete, joelho que dobra ao cair, luva
     que recua ao pegar a bola, embalagem de isopor: todos fazem a mesma
     coisa, que é esticar o tempo da parada. Nenhum deles "absorve o impacto"
     no sentido vago da expressão.</p>
     <p><b>Um detalhe que costuma passar.</b> O airbag também espalha a força
     por uma área muito maior que a do volante, e as duas coisas se somam. A
     pressão cai pelo tempo e pela área ao mesmo tempo.</p>''' ),

    ('5.2  A dedução de Tsiolkovsky, com o sistema certo',
     r'''Deduza a equação do foguete tomando como sistema o foguete
     <em>mais</em> o gás prestes a ser expelido, e explique em uma frase por
     que escrever \(F = m(t)a\) para o foguete sozinho está errado. Depois
     mostre que, no referencial que se move com o foguete num dado instante, o
     empuxo vale \(v_e\,|dm/dt|\).''',
     r'''<p><b>O sistema.</b> Em \(t\), um corpo único de massa \(m\) com
     velocidade \(v\): \(p(t) = mv\). Em \(t+dt\), duas partes: o foguete, com
     massa \(m + dm\) (e \(dm &lt; 0\)) a \(v + dv\), e o gás expelido, de massa
     \(-dm\), que sai a \(v_e\) <em>em relação ao foguete</em>, isto é, a
     \(v - v_e\) em relação ao solo:</p>
     <p>\[ p(t+dt) = (m+dm)(v+dv) + (-dm)(v - v_e). \]</p>
     <p><b>A diferença.</b> Expandindo e cancelando \(mv\):</p>
     <p>\[ dp = m\,dv + v\,dm + dm\,dv - v\,dm + v_e\,dm
            = m\,dv + v_e\,dm, \]</p>
     <p>com \(dm\,dv\) descartado por ser de segunda ordem. Sem forças
     externas, \(dp = 0\) e</p>
     <p>\[ m\,dv = -v_e\,dm \quad\Longrightarrow\quad
        \int_{0}^{\Delta v}dv = -v_e\int_{m_0}^{m_f}\frac{dm}{m}
        \quad\Longrightarrow\quad \Delta v = v_e\ln\frac{m_0}{m_f}. \]</p>
     <p><b>Por que \(F = m(t)a\) está errado.</b> Porque a segunda lei nessa
     forma vale para um conjunto fixo de partículas, e o foguete sozinho não é
     um: ele perde partículas o tempo todo, e o momento que elas levam embora
     não aparece em lugar nenhum da equação. Usar \(m(t)\) ali é contrabandear
     a variação de massa para dentro de uma fórmula que supôs massa
     constante.</p>
     <p><b>O empuxo.</b> Reescrevendo a equação como
     \(m\,dv/dt = -v_e\,dm/dt\), o lado direito é positivo, já que
     \(dm/dt &lt; 0\), e tem dimensão de força:</p>
     <p>\[ E = v_e\left|\der{m}{t}\right|. \]</p>
     <p>Essa é a leitura prática: o empuxo é a velocidade de exaustão vezes a
     vazão de massa. Um motor que expele 400 kg/s a 2942 m/s entrega 1,18 MN,
     esteja no vácuo ou não, encostado numa parede ou não. Não há nada em que
     empurrar, e é justamente esse o ponto.</p>''' ),

    ('5.3  O teto de um estágio só',
     r'''Com \(v_e = 2942\) m/s e fração estrutural \(\epsilon = 0{,}10\),
     mostre que um foguete de um estágio não chega aos 9400 m/s da órbita
     baixa <em>nem com carga útil nula</em>. Depois use a fórmula dos estágios
     idênticos para achar a maior carga útil, em porcentagem da massa total,
     que dois e três estágios conseguem colocar em órbita.''',
     r'''<p><b>O teto.</b> Com carga útil nula, a massa final é a estrutura,
     \(\epsilon m_0\), de modo que</p>
     <p>\[ \Delta v_{\max} = v_e\ln\frac{m_0}{\epsilon m_0}
        = v_e\ln\frac{1}{\epsilon}
        = 2942\ln 10 = 6774\ \mathrm{m/s}. \]</p>
     <p>Faltam 2600 m/s, e não há carga útil negativa. Repare no que esse
     resultado tem de implacável: ele não depende do tamanho do foguete.
     Construir um dez vezes maior não muda nada, porque \(m_0\) cancela. O
     único jeito de levantar essa linha é melhorar \(\epsilon\) ou
     \(v_e\).</p>
     <p><b>Com \(n\) estágios idênticos.</b> Cada um multiplica a massa pela
     mesma razão \(r = (m_0/m_c)^{1/n}\), e</p>
     <p>\[ \Delta v = n\,v_e\ln\frac{r}{1+\epsilon(r-1)}. \]</p>
     <p>Igualando a 9400 m/s e resolvendo numericamente para a fração de carga
     útil \(m_c/m_0\):</p>
     <div class="tabela-rolavel">
     <table>
     <thead><tr><th>estágios</th><th>carga útil máxima</th>
     <th>massa na plataforma por tonelada em órbita</th></tr></thead>
     <tbody>
     <tr><td>1</td><td>nenhuma</td><td>impossível</td></tr>
     <tr><td>2</td><td>1,29 %</td><td>77 t</td></tr>
     <tr><td>3</td><td>2,01 %</td><td>50 t</td></tr>
     </tbody>
     </table>
     </div>
     <p><b>A leitura.</b> Passar de dois para três estágios melhora a carga em
     56 %, mas passar de um para dois é a diferença entre impossível e
     possível. Os ganhos seguintes encolhem: quatro estágios dariam 2,3 %, e o
     ganho já não paga a complexidade de mais um conjunto de motores, junções
     e eventos de separação, cada um dos quais pode falhar.</p>
     <p><b>Por que o foguete reutilizável muda a conversa.</b> Ele não melhora
     nenhum desses números: ao contrário, guardar propelente para o pouso e
     carregar pernas e grades piora \(\epsilon\) e come carga útil. A aposta é
     econômica, e não física: aceitar menos carga por lançamento em troca de
     não jogar fora a máquina.</p>''' ),

    ('5.4  O vagão que recolhe areia',
     r'''Um vagão de 10 000 kg desliza sem atrito a 5,0 m/s sob uma esteira
     que despeja areia parada dentro dele a 50 kg/s. Encontre a velocidade
     depois de 60 s, a força horizontal que seria preciso aplicar para manter
     a velocidade constante, e a energia mecânica perdida. Diga para onde ela
     foi.''',
     r'''<p><b>A velocidade.</b> Nenhuma força horizontal externa age sobre o
     conjunto vagão mais areia, de modo que o momento horizontal se conserva.
     A areia entra com velocidade horizontal nula:</p>
     <p>\[ M v_0 = \left(M + \lambda t\right)v
        \quad\Longrightarrow\quad
        v(t) = \frac{M v_0}{M + \lambda t}. \]</p>
     <p>Com \(t = 60\) s, a massa vai a 13 000 kg e
     \(v = 50000/13000 = 3{,}846\) m/s. A integração numérica passo a passo
     dá 3,846154 m/s, o mesmo número.</p>
     <p><b>A força para manter a velocidade.</b> Se \(v\) é constante,</p>
     <p>\[ F = \der{p}{t} = v\der{m}{t} = \lambda v_0
        = 50 \times 5{,}0 = 250\ \mathrm{N}. \]</p>
     <p>Note que a força não acelera coisa alguma: ela existe apenas para
     acelerar a areia nova, de zero até \(v_0\), e é essa a diferença entre
     \(F = dp/dt\) e \(F = ma\) neste problema.</p>
     <p><b>A energia.</b> Inicial: \(\frac12 \times 10000 \times 25
     = 125{,}0\) kJ. Final: \(\frac12 \times 13000 \times 3{,}846^2
     = 96{,}2\) kJ. Perderam-se <b>28,8 kJ</b>, isto é, 23 % do total.</p>
     <p><b>Para onde ela foi.</b> Para o atrito entre a areia e o piso do
     vagão, enquanto cada punhado é arrastado de zero até a velocidade do
     vagão. A areia chega parada e precisa ser acelerada; o processo é
     exatamente tão dissipativo quanto uma colisão perfeitamente inelástica, e
     é o que é. O momento se conserva e a energia mecânica não, e esse é o
     padrão sempre que massa é incorporada ao sistema sem deslizar livremente
     depois.</p>
     <p><b>Compare com o foguete.</b> Lá a massa <em>sai</em> com velocidade
     alta e a energia mecânica do conjunto <em>aumenta</em>, às custas da
     química do propelente. Aqui a massa <em>entra</em> parada e a energia
     mecânica diminui. São o mesmo problema com o sinal de \(dm\) trocado.</p>''' ),

    ('5.5  A corrente que cai, e os três pesos',
     r'''Uma corrente de densidade linear \(\mu\) é solta do repouso com a
     ponta encostada na mesa. Mostre que, quando um comprimento \(x\) já se
     acumulou, a mesa exerce \(N = 3\mu g x\). Confirme o resultado aplicando
     \(F = dp/dt\) à corrente inteira, e diga quanto vale a força máxima para
     uma corrente de 2,0 m e 1,5 kg/m.''',
     r'''<p><b>O caminho direto.</b> O trecho que ainda cai está em queda
     livre (nada o segura), de modo que, quando \(x\) já caiu,
     \(v^2 = 2gx\). A mesa faz duas coisas ao mesmo tempo:</p>
     <ul>
     <li>sustenta o peso do que já parou: \(\mu g x\);</li>
     <li>zera o momento do que chega. Em \(dt\), uma massa \(\mu v\,dt\) chega
     com velocidade \(v\) e para, o que exige \(dp/dt = \mu v^2\).</li>
     </ul>
     <p>\[ N = \mu g x + \mu v^2 = \mu g x + 2\mu g x = 3\mu g x. \]</p>
     <p><b>A confirmação independente.</b> Aplique a segunda lei à corrente
     inteira, que tem massa fixa \(\mu L\). As forças externas sobre ela são o
     peso total e a normal:</p>
     <p>\[ \mu L g - N = \der{p}{t}, \qquad p = \mu\left(L - x\right)v, \]</p>
     <p>já que só o trecho suspenso tem momento. Derivando, com
     \(\dot{x} = v\) e \(\dot{v} = g\):</p>
     <p>\[ \der{p}{t} = \mu\left[-v^2 + (L-x)g\right]
        = \mu\left[(L-x)g - 2gx\right], \]</p>
     <p>\[ N = \mu L g - \mu(L-x)g + 2\mu g x = \mu g x + 2\mu g x = 3\mu g x. \]</p>
     <p>Os dois caminhos coincidem, e o segundo nunca precisou separar a
     corrente em pedaços. O programa faz essa conta numericamente e acha
     \(3\times10^{-10}\) N de diferença.</p>
     <p><b>O número.</b> Com \(L = 2{,}0\) m e \(\mu = 1{,}5\) kg/m, a força é
     máxima no instante em que o último elo chega:</p>
     <p>\[ N_{\max} = 3 \times 1{,}5 \times 9{,}81 \times 2{,}0
        = 88{,}3\ \mathrm{N}, \]</p>
     <p>contra um peso total de 29,4 N. No fim da queda, a mesa sente
     <b>três vezes</b> o peso da corrente inteira, e um milissegundo depois
     sente apenas o peso. É por isso que uma corrente derrubada faz muito mais
     barulho do que a sua massa sugere.</p>
     <p><b>Um teste de honestidade.</b> Quem escrever \(N = m(t)g\) com
     \(m(t) = \mu x\) acha um terço da resposta. O erro não está na álgebra:
     está em ter esquecido de perguntar com que velocidade a massa chega.</p>''' ),

    ('5.6  O homem que anda no barco',
     r'''Um homem de 80 kg está numa das pontas de um barco de 120 kg e 4,0 m,
     parado em água sem atrito. Ele caminha até a outra ponta. Quanto o barco
     se desloca em relação à água, e quanto o homem se desloca? Depois explique
     por que a resposta não depende de quão depressa ele anda.''',
     r'''<p><b>O argumento.</b> Não há força horizontal externa, e o sistema
     parte do repouso, de modo que o momento total é zero o tempo todo. Mas
     momento nulo é a mesma coisa que centro de massa parado:</p>
     <p>\[ \vet{p}_{\text{total}} = M_{\text{total}}\,\vet{v}_{CM} = 0
        \quad\Longrightarrow\quad \vet{v}_{CM} = 0
        \quad\Longrightarrow\quad x_{CM} = \text{constante}. \]</p>
     <p><b>A conta.</b> Chame de \(d_b\) o deslocamento do barco (para trás) e
     de \(d_h\) o do homem (para a frente), ambos em relação à água. Um anda
     sobre o outro, de modo que \(d_h + d_b = L\). Com o centro de massa
     parado,</p>
     <p>\[ m_h d_h = m_b d_b
        \quad\Longrightarrow\quad
        d_b = \frac{m_h}{m_h + m_b}L
        = \frac{80}{200}\times 4{,}0 = 1{,}6\ \mathrm{m}, \]</p>
     <p>e \(d_h = 2{,}4\) m. O homem caminhou 4,0 m <em>sobre o barco</em> e
     apenas 2,4 m em relação à água.</p>
     <p><b>Por que a velocidade não importa.</b> Porque a conclusão veio de
     uma lei de conservação, que só compara o estado inicial com o final. Se
     ele anda devagar, o barco desliza devagar; se corre, o barco anda
     depressa e por menos tempo. O produto é o mesmo. Ele pode até parar no
     meio do caminho, tomar café e seguir: o resultado final é 1,6 m.</p>
     <p><b>Onde isso aparece de novo.</b> O mesmo argumento diz que um
     astronauta solto, sem nada para jogar, não consegue voltar à nave por
     mais que se contorça, e que o foguete do resto do módulo acelera sem
     empurrar coisa alguma: o centro de massa do conjunto, foguete mais gases,
     segue exatamente onde seguiria. O módulo 13 retoma o centro de massa como
     ferramenta de cálculo, e não apenas de argumento.</p>''' ),
]
