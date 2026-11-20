# -*- coding: utf-8 -*-
"""Exercícios propostos do módulo 12."""

LISTA = [
    ('12.1  A redução a um corpo é exata',
     r'''Dois corpos de massas \(m_1\) e \(m_2\) interagem apenas entre si,
     por uma força central \(f(r)\) que depende só da separação. Mostre que a
     separação relativa \(\vet{r} = \vet{r}_2-\vet{r}_1\) obedece
     \(\mu\ddot{\vet{r}} = f(r)\vers{r}\), com \(\mu = m_1m_2/(m_1+m_2)\), e
     que a energia total do par, descontada a do centro de massa, é a de uma
     única partícula de massa \(\mu\). Depois diga em que ponto a aproximação
     \(m_2 \ll m_1\) é usada.''',
     r'''<p><b>A equação.</b> As duas equações de movimento são</p>
     <p>\[ m_1\ddot{\vet{r}}_1 = +f(r)\vers{r}, \qquad
          m_2\ddot{\vet{r}}_2 = -f(r)\vers{r}, \]</p>
     <p>com o sinal invertido pela terceira lei (tomando \(f &lt; 0\) para
     atração e \(\vers{r}\) apontando de 1 para 2). Dividindo cada uma pela
     respectiva massa e subtraindo:</p>
     <p>\[ \ddot{\vet{r}} = \ddot{\vet{r}}_2-\ddot{\vet{r}}_1
        = -f(r)\left(\frac{1}{m_2}+\frac{1}{m_1}\right)\vers{r}
        = -\frac{f(r)}{\mu}\vers{r}, \]</p>
     <p>porque \(1/m_1+1/m_2 = 1/\mu\) é a própria definição de massa
     reduzida. A separação se comporta como uma partícula de massa \(\mu\)
     sujeita à força original.</p>
     <p><b>A energia.</b> Escreva as posições em relação ao centro de massa,
     \(\vet{r}_1 = \vet{R}-(m_2/M)\vet{r}\) e
     \(\vet{r}_2 = \vet{R}+(m_1/M)\vet{r}\), com \(M = m_1+m_2\). Derivando e
     somando as duas energias cinéticas, os termos cruzados em
     \(\dot{\vet{R}}\cdot\dot{\vet{r}}\) se cancelam, e sobra</p>
     <p>\[ T = \frac{M\dot{R}^2}{2} + \frac{\mu\dot{r}^2}{2}. \]</p>
     <p>O primeiro termo é a translação do par como um todo, que é constante
     porque não há força externa. O segundo, somado a \(U(r)\), é exatamente a
     energia de uma partícula de massa \(\mu\).</p>
     <p><b>Onde entra a aproximação.</b> Em nenhum lugar. A redução é uma
     identidade algébrica, válida para quaisquer massas, inclusive iguais. A
     aproximação \(m_2 \ll m_1\) só aparece depois, quando se troca \(\mu\) por
     \(m_2\) e \(M\) por \(m_1\) para dizer que o corpo leve orbita o pesado
     parado. Essa segunda troca <em>é</em> aproximada, e é ela que falha no
     teste da Lua do módulo 11 e nos binários do exercício 12.5.</p>
     <p><b>Um detalhe que se perde.</b> A partícula fictícia de massa \(\mu\)
     não está em lugar nenhum: a trajetória que ela descreve é a da
     <em>separação</em>. Os dois corpos reais percorrem elipses semelhantes a
     essa, de semieixos \(a\,m_2/M\) e \(a\,m_1/M\), em torno do centro de
     massa comum, sempre em lados opostos. Para massas iguais, cada um
     descreve uma elipse de metade do tamanho.</p>'''),

    ('12.2  Quais potenciais admitem órbita circular estável',
     r'''Para \(U(r) = -k/r^n\) com \(k &gt; 0\), encontre o raio da órbita
     circular de momento angular \(L\), mostre que ela só é estável se
     \(n &lt; 2\), e calcule a frequência de pequenas oscilações radiais em
     torno dela. Compare essa frequência com a do movimento angular e explique
     o que a razão entre as duas tem a ver com o fechamento da órbita.''',
     r'''<p><b>O raio.</b> O potencial efetivo é
     \(U_{\text{ef}} = L^2/2mr^2 - k/r^n\), e a órbita circular está no
     extremo:</p>
     <p>\[ \der{U_{\text{ef}}}{r} = -\frac{L^2}{mr^3} + \frac{nk}{r^{n+1}} = 0
        \quad\Longrightarrow\quad
        \frac{L^2}{m} = n\,k\,r_0^{\,n-2}. \]</p>
     <p>Para \(n = 1\) isso dá o resultado familiar \(r_0 = L^2/mk\), que é o
     parâmetro \(p\) da seção 3 da aula.</p>
     <p><b>A estabilidade.</b> Derivando outra vez e usando a relação acima
     para eliminar \(L^2/m\):</p>
     <p>\[ \dder{U_{\text{ef}}}{r}\bigg|_{r_0}
        = \frac{3L^2}{mr_0^4} - \frac{n(n+1)k}{r_0^{\,n+2}}
        = \frac{nk}{r_0^{\,n+2}}\left(3-n-1\right)
        = \frac{nk\,(2-n)}{r_0^{\,n+2}}. \]</p>
     <p>Isso é positivo, e portanto o extremo é mínimo, se e somente se
     \(n &lt; 2\). Em termos da força, \(F \propto r^{-(n+1)}\), a condição é
     que o expoente da força seja menor que 3.</p>
     <p><b>O que acontece em \(n \geq 2\).</b> A barreira centrífuga cai como
     \(r^{-2}\); se a atração cai mais rápido que isso, ela vence a barreira
     perto da origem e o potencial efetivo despenca para \(-\infty\). Não há
     mínimo, e a órbita circular que existe é de máximo: qualquer perturbação
     faz a partícula cair no centro ou escapar. Órbitas ligadas estáveis
     exigem \(n &lt; 2\), que é o primeiro filtro de Bertrand.</p>
     <p><b>As duas frequências.</b> A oscilação radial em torno do mínimo tem
     \(\omega_r^2 = U_{\text{ef}}''(r_0)/m = nk(2-n)/mr_0^{\,n+2}\),
     enquanto o movimento angular tem
     \(\omega_\varphi^2 = L^2/m^2r_0^4 = nk/mr_0^{\,n+2}\). Dividindo:</p>
     <p>\[ \frac{\omega_r}{\omega_\varphi} = \sqrt{2-n}. \]</p>
     <p><b>E o fechamento.</b> A órbita quase circular fecha se, no tempo de
     uma oscilação radial completa (do periastro ao periastro), o ângulo
     percorrido for uma fração racional de \(2\pi\); isto é, se
     \(\sqrt{2-n}\) for racional. Dois casos saltam aos olhos: \(n = 1\), a
     gravitação, dá razão 1, e a órbita fecha depois de exatamente uma volta;
     \(n = -2\), a mola \(U \propto r^2\), dá razão 2, e a elipse fecha depois
     de meia volta, com o centro de força no <em>centro</em> da elipse e não no
     foco.</p>
     <p>Outros expoentes também fecham órbitas quase circulares, bastando que
     \(2-n\) seja o quadrado de um racional:
     \(n = -1/4\), por exemplo, dá razão \(3/2\), e a órbita se fecha depois de
     duas voltas. O que o teorema de Bertrand acrescenta, e que
     esta conta de pequenas oscilações não vê, é que nesses outros casos o
     fechamento se perde quando a órbita deixa de ser quase circular. Só
     \(n = 1\) e \(n = -2\) fecham para <em>toda</em> amplitude.</p>'''),

    ('12.3  A equação vis-viva, e por que o periastro é rápido',
     r'''A partir de \(E = -k/2a\) para a órbita elíptica, obtenha a velocidade
     em função do raio,
     \(v^2 = GM\left(2/r - 1/a\right)\). Aplique-a aos raios extremos e mostre
     que \(r_pv_p = r_av_a\). Verifique com a órbita que o programa integra:
     \(r_p = 1{,}000\) UA com \(v_p = 30{,}104\) km/s, e \(r_a = 3{,}5714\) UA
     com \(v_a = 8{,}429\) km/s.''',
     r'''<p><b>A dedução.</b> A energia total vale
     \(E = mv^2/2 - k/r\), e para a elipse \(E = -k/2a\) (o que se obtém
     avaliando a energia no periastro e usando \(e^2 = 1+2EL^2/mk^2\), ou mais
     rápido somando as energias nos dois extremos). Igualando:</p>
     <p>\[ \frac{mv^2}{2} = \frac{k}{r} - \frac{k}{2a}
        \quad\Longrightarrow\quad
        v^2 = \frac{2k}{m}\left(\frac1r - \frac{1}{2a}\right)
            = GM\left(\frac2r - \frac1a\right), \]</p>
     <p>usando \(k/m = GM\) com \(M\) a massa total. O nome <em>vis viva</em>
     é de Leibniz, e a relação é o cavalo de batalha de toda a mecânica
     orbital prática.</p>
     <p><b>Nos extremos.</b> Com \(r_p = a(1-e)\) e \(r_a = a(1+e)\):</p>
     <p>\[ v_p^2 = \frac{GM}{a}\,\frac{1+e}{1-e}, \qquad
          v_a^2 = \frac{GM}{a}\,\frac{1-e}{1+e}
          \quad\Longrightarrow\quad
          \frac{v_p}{v_a} = \frac{1+e}{1-e} = \frac{r_a}{r_p}. \]</p>
     <p>Ou seja \(r_pv_p = r_av_a\), que é a conservação do momento angular
     nos pontos em que a velocidade é inteiramente transversal. A lei das
     áreas, nos dois extremos, se reduz a esta igualdade.</p>
     <p><b>Os números.</b> \(r_a/r_p = 3{,}5714\) e
     \(v_p/v_a = 30{,}104/8{,}429 = 3{,}5722\), com a diferença na quarta casa
     vindo do arredondamento dos valores impressos. A excentricidade sai de
     qualquer um dos dois:
     \(e = (r_a-r_p)/(r_a+r_p) = 2{,}5714/4{,}5714 = 0{,}5625\), que é
     exatamente o valor da tabela da seção 3 para \(v_0 = 1{,}25\,v_{\text{circ}}\).</p>
     <p><b>A leitura física.</b> O planeta é rápido perto e lento longe, na
     proporção inversa exata da distância. Isso não é um fato sobre
     gravitação: é momento angular. A mesma conta se aplica a um patinador que
     recolhe os braços, com a diferença de que o patinador faz trabalho e o
     planeta troca energia cinética por potencial, mantendo a soma fixa.</p>'''),

    ('12.4  A transferência de Hohmann para Marte',
     r'''Uma sonda em órbita circular de 1 UA deve chegar a uma órbita
     circular de 1,5237 UA. A manobra mais econômica em dois impulsos é a
     elipse de Hohmann, tangente às duas órbitas. Calcule os dois \(\Delta v\),
     o total, e o tempo de viagem. Use
     \(GM_\odot = 1{,}32712\times10^{20}\) m³/s².''',
     r'''<p><b>A geometria.</b> A elipse de transferência tem periastro em
     \(r_1\) e apoastro em \(r_2\), de modo que</p>
     <p>\[ a_t = \frac{r_1+r_2}{2} = 1{,}2618\ \text{UA}
        = 1{,}8877\times10^{11}\ \mathrm{m}, \qquad
        e_t = \frac{r_2-r_1}{r_2+r_1} = 0{,}2075. \]</p>
     <p><b>O primeiro impulso.</b> A velocidade circular em 1 UA é
     \(v_1 = \sqrt{GM/r_1} = 29{,}785\) km/s. A velocidade de periastro da
     elipse, pela vis-viva do exercício anterior, é</p>
     <p>\[ v_p = \sqrt{GM\left(\frac{2}{r_1}-\frac{1}{a_t}\right)}
        = 32{,}729\ \mathrm{km/s}
        \quad\Longrightarrow\quad
        \Delta v_1 = 2{,}945\ \mathrm{km/s}. \]</p>
     <p><b>O segundo.</b> No apoastro a sonda tem
     \(v_a = \sqrt{GM(2/r_2-1/a_t)} = 21{,}481\) km/s, e precisa de
     \(v_2 = \sqrt{GM/r_2} = 24{,}129\) km/s para circularizar:</p>
     <p>\[ \Delta v_2 = 2{,}649\ \mathrm{km/s}, \qquad
          \Delta v_{\text{total}} = 5{,}594\ \mathrm{km/s}. \]</p>
     <p><b>O tempo.</b> A viagem é meia volta na elipse de transferência:</p>
     <p>\[ \frac{T_t}{2} = \pi\sqrt{\frac{a_t^3}{GM}}
        = 2{,}237\times10^7\ \mathrm{s} = 258{,}9\ \text{dias}. \]</p>
     <p><b>O que é curioso aqui.</b> Os dois impulsos <em>aumentam</em> a
     velocidade, e no entanto a sonda chega a Marte mais lenta do que saiu da
     Terra: 24,1 contra 29,8 km/s. A energia total cresceu nas duas queimas, e
     o que cresceu foi a energia potencial. Órbitas mais altas são mais
     energéticas e mais lentas ao mesmo tempo, o que é a leitura orbital do
     \(E = -k/2a\): subir custa energia e reduz a velocidade.</p>
     <p><b>Uma complicação real.</b> O cálculo acima dá o \(\Delta v\) em
     relação ao Sol. Uma sonda que parte da Terra tem de escapar do poço
     terrestre primeiro, e aí se usa a manobra oberthiana: queimar perto da
     Terra, onde a velocidade é alta, aproveita a energia cinética já
     existente e custa muito menos \(\Delta v\) do que a mesma mudança feita
     longe. Marte também tem de estar no lugar certo na chegada, o que limita
     os lançamentos a janelas de 26 meses.</p>'''),

    ('12.5  Pesar Sirius, e o preço de esquecer a massa total',
     r'''Sirius é um binário de período 50,1 anos e semieixo relativo
     19,8 UA. Obtenha a massa total do sistema em massas solares. Depois
     calcule que período a terceira lei de Kepler na forma original
     (\(T^2 = a^3\), com \(T\) em anos e \(a\) em UA) preveria para esse
     semieixo, e comente o tamanho do erro.''',
     r'''<p><b>A massa.</b> Em unidades de ano, UA e massa solar, a terceira
     lei fica \(T^2 = a^3/M\) com \(M = m_1+m_2\) em massas solares, porque
     essas unidades foram escolhidas para que a constante valha 1 no caso
     Sol-Terra. Então</p>
     <p>\[ M = \frac{a^3}{T^2} = \frac{19{,}8^3}{50{,}1^2}
        = \frac{7762}{2510} = 3{,}09\ M_\odot. \]</p>
     <p>Os valores catalogados são 2,06 e 1,02 massas solares, somando 3,08.
     A conta de uma linha acerta em três casas.</p>
     <p><b>O erro de usar \(M = 1\).</b> A lei original prevê
     \(T = \sqrt{a^3} = \sqrt{7762} = 88{,}1\) anos, contra 50,1 observados:
     um erro de <b>76 %</b>. Não é um detalhe de quarta casa. A razão é a raiz
     da massa total: \(\sqrt{3{,}09} = 1{,}76\).</p>
     <p><b>Por que funciona no sistema solar.</b> Lá a massa total do par
     Sol-planeta é 1,000955 massas solares no pior caso, que é Júpiter, e a
     correção no período é de meio milésimo. Kepler não tinha precisão para
     ver isso, e teve a sorte de o Sol dominar. Num binário de massas
     comparáveis, a lei na forma original simplesmente não serve, e é
     justamente por isso que binários são a principal fonte de massas
     estelares medidas: a terceira lei, na forma correta, é uma balança.</p>
     <p><b>O que falta para separar as duas massas.</b> A terceira lei dá
     apenas a soma. Para obter \(m_1\) e \(m_2\) separadamente é preciso medir
     as duas elipses em torno do centro de massa e usar
     \(m_1a_1 = m_2a_2\), isto é, observar qual das estrelas descreve a
     elipse menor. Foi assim que a companheira de Sirius, prevista por Bessel
     em 1844 a partir do bamboleio da estrela principal, ganhou uma massa
     antes mesmo de ser vista.</p>'''),

    (r'12.6  A precessão produzida por uma perturbação em \(1/r^3\)',
     r'''Acrescente ao potencial de Kepler um termo
     \(\delta U = -\beta/r^3\). Mostre que, em primeira ordem em \(\beta\), o
     periastro avança \(\Delta\varphi = 6\pi\beta/L^2p\) por órbita, com
     \(p = L^2/mk\). Depois use o termo da relatividade geral,
     \(\beta = GML^2/mc^2\), para recuperar a fórmula de Mercúrio.''',
     r'''<p><b>A equação da órbita perturbada.</b> A conta geral, feita na
     seção 3 da aula para \(U = -k/r\), vale para qualquer potencial se
     escrita como</p>
     <p>\[ \dder{u}{\varphi} + u = -\frac{m}{L^2u^2}\,F(1/u), \]</p>
     <p>com \(F = -dU/dr\). Para \(U = -k/r - \beta/r^3\), a força é
     \(F = -k/r^2 - 3\beta/r^4 = -ku^2-3\beta u^4\), de modo que</p>
     <p>\[ \dder{u}{\varphi} + u = \frac{mk}{L^2} + \frac{3m\beta}{L^2}u^2. \]</p>
     <p><b>A linearização.</b> Escreva \(u = u_0+\delta u\) com
     \(u_0 = 1/p = mk/L^2\) o valor circular, e mantenha só a primeira ordem
     em \(\delta u\). O termo \(u^2 \to u_0^2+2u_0\delta u\), e o pedaço
     proporcional a \(\delta u\) passa para o lado esquerdo:</p>
     <p>\[ \dder{\delta u}{\varphi}
        + \left(1 - \frac{6m\beta u_0}{L^2}\right)\delta u
        = \text{constante}. \]</p>
     <p>É o oscilador do módulo 6, com frequência angular (em \(\varphi\))</p>
     <p>\[ \omega = \sqrt{1-\frac{6m\beta}{L^2p}}
        \approx 1 - \frac{3m\beta}{L^2p}. \]</p>
     <p><b>O avanço.</b> O periastro se repete quando
     \(\omega\varphi\) avança \(2\pi\), isto é, a cada
     \(\varphi = 2\pi/\omega &gt; 2\pi\). O excesso sobre uma volta é</p>
     <p>\[ \Delta\varphi = \frac{2\pi}{\omega}-2\pi
        \approx 2\pi\,\frac{3m\beta}{L^2p}
        = \frac{6\pi\beta}{L^2p} \]</p>
     <p>por órbita, com \(m\) absorvido ao se usar \(L\) por unidade de massa,
     como o programa faz. Repare no sinal: \(\beta &gt; 0\) deixa
     \(\omega &lt; 1\), o periastro demora mais que uma volta para voltar, e o
     avanço é no sentido do movimento. Com \(\beta &lt; 0\) a roseta gira ao
     contrário.</p>
     <p><b>Mercúrio.</b> Substituindo \(\beta = GML^2/mc^2\) e
     \(p = a(1-e^2)\):</p>
     <p>\[ \Delta\varphi = \frac{6\pi}{L^2}\cdot\frac{GML^2}{c^2}
        \cdot\frac{1}{a(1-e^2)}
        = \frac{6\pi GM}{c^2a\left(1-e^2\right)}, \]</p>
     <p>que é a fórmula da seção 4 e dá 42,98 segundos de arco por século.
     O \(L^2\) se cancela, e por isso o avanço depende apenas da geometria da
     órbita e da massa central, e não do momento angular do planeta.</p>
     <p><b>Um aviso honesto.</b> Esta dedução chega ao número certo partindo de
     um potencial newtoniano com um termo extra, mas não é a dedução
     relativística. Na relatividade geral o termo em \(1/r^3\) aparece na
     equação da órbita, e não no potencial, e a passagem de uma para a outra
     envolve trocar o tempo próprio pelo coordenado. A coincidência é real e
     útil, e é assim que o cálculo é apresentado em quase todo lugar, mas
     chamar \(-GML^2/mc^2r^3\) de "o potencial da relatividade geral" é um
     abuso de linguagem.</p>'''),
]
