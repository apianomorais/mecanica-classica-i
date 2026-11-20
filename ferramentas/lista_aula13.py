# -*- coding: utf-8 -*-
"""Exercícios propostos do módulo 13."""

LISTA = [
    ('13.1  As duas versões da terceira lei',
     r'''Deduza \(M\ddot{\vet{R}} = \vet{F}^{\text{ext}}\) somando as
     equações de movimento. Depois mostre que a conservação do
     <em>momento angular</em> total exige mais do que a terceira lei na
     forma \(\vet{F}_{ij} = -\vet{F}_{ji}\): exige que as forças internas
     sejam dirigidas ao longo da reta que une os dois corpos. Dê um exemplo
     de força que não satisfaz essa segunda condição.''',
     r'''<p><b>O centro de massa.</b> Somando sobre \(i\):</p>
     <p>\[ \sum_i m_i\ddot{\vet{r}}_i = \sum_i\vet{F}_i^{\text{ext}}
        + \sum_i\sum_{j\neq i}\vet{F}_{ij}. \]</p>
     <p>A soma dupla percorre cada par duas vezes, uma como \(\vet{F}_{ij}\)
     e outra como \(\vet{F}_{ji}\), e os dois se cancelam. O lado esquerdo é
     \(M\ddot{\vet{R}}\) por definição.</p>
     <p><b>O momento angular.</b> Derivando
     \(\vet{L} = \sum_i\vet{r}_i\cruz m_i\dot{\vet{r}}_i\), o termo
     \(\dot{\vet{r}}_i\cruz\dot{\vet{r}}_i\) some e sobra o torque. Para as
     forças internas, agrupando o par \(ij\):</p>
     <p>\[ \vet{r}_i\cruz\vet{F}_{ij} + \vet{r}_j\cruz\vet{F}_{ji}
        = (\vet{r}_i-\vet{r}_j)\cruz\vet{F}_{ij}, \]</p>
     <p>usando apenas \(\vet{F}_{ji} = -\vet{F}_{ij}\). Esse produto
     vetorial só é nulo se \(\vet{F}_{ij}\) for <b>paralelo</b> a
     \(\vet{r}_i-\vet{r}_j\).</p>
     <p><b>Os nomes.</b> A condição \(\vet{F}_{ij} = -\vet{F}_{ji}\) é a
     forma <em>fraca</em> da terceira lei, e basta para o momento linear. A
     forma <em>forte</em> exige também que as forças estejam na linha que
     une os corpos, e é ela que o momento angular pede. Todas as forças
     centrais satisfazem as duas.</p>
     <p><b>O contraexemplo.</b> A força magnética entre duas cargas em
     movimento viola as duas formas. Duas cargas se movendo
     perpendicularmente uma à outra exercem forças que nem são opostas nem
     são colineares, e o momento do par não se conserva. A física não está
     errada: o que falta na conta é o momento carregado pelo próprio campo
     eletromagnético, que é um terceiro participante. Somando ele, a
     conservação volta. Esse é o preço de tratar interações que se propagam
     com velocidade finita como se fossem instantâneas, e é um dos motivos
     pelos quais a mecânica newtoniana não sobrevive à eletrodinâmica
     sem reparos.</p>'''),

    ('13.2  O teorema de König, e a massa reduzida outra vez',
     r'''Escrevendo \(\vet{r}_i = \vet{R}+\vet{r}_i'\), mostre que</p>
     <p>\[ K = \frac{MV^2}{2} + \sum_i\frac{m_iv_i'^2}{2}, \]</p>
     <p>isto é, que os termos cruzados somem. Depois particularize para duas
     partículas e obtenha \(K = MV^2/2 + \mu v_{\text{rel}}^2/2\).''',
     r'''<p><b>A separação.</b> Derivando a decomposição,
     \(\vet{v}_i = \vet{V}+\vet{v}_i'\), e elevando ao quadrado:</p>
     <p>\[ K = \sum_i\frac{m_i}{2}\left(V^2 + 2\vet{V}\cdot\vet{v}_i'
        + v_i'^2\right). \]</p>
     <p>O primeiro termo dá \(MV^2/2\) e o terceiro é a soma pedida. O
     cruzado vale \(\vet{V}\cdot\sum_i m_i\vet{v}_i'\), e essa soma é o
     momento total <em>medido no referencial do centro de massa</em>, que é
     zero por definição. É o único passo da conta, e ele é o que dá sentido
     à decomposição: as duas parcelas não se misturam.</p>
     <p><b>Duas partículas.</b> No referencial do CM,
     \(\vet{v}_1' = (m_2/M)\vet{v}_{\text{rel}}\) e
     \(\vet{v}_2' = -(m_1/M)\vet{v}_{\text{rel}}\), com
     \(\vet{v}_{\text{rel}} = \vet{v}_1-\vet{v}_2\). Somando:</p>
     <p>\[ \frac{m_1}{2}\frac{m_2^2}{M^2}v_{\text{rel}}^2
        + \frac{m_2}{2}\frac{m_1^2}{M^2}v_{\text{rel}}^2
        = \frac{m_1m_2}{2M}v_{\text{rel}}^2
        = \frac{\mu v_{\text{rel}}^2}{2}. \]</p>
     <p><b>Para que serve.</b> Essa é a conta que decide quanta energia uma
     colisão pode dissipar, e ela responde antes de se saber qualquer coisa
     sobre o mecanismo da batida. O que o momento protege é \(MV^2/2\); o
     que está em jogo é \(\mu v_{\text{rel}}^2/2\). A massa reduzida, que
     apareceu no módulo 6 como truque de dois corpos e no 12 como redução do
     problema de Kepler, é a mesma coisa aqui.</p>'''),

    ('13.3  O pêndulo balístico',
     r'''Uma bala de 10 g se aloja num bloco de 2,00 kg pendurado por um fio.
     O conjunto sobe 8,0 cm. Ache a velocidade da bala, calcule a fração da
     energia cinética que se perdeu e explique por que o problema <em>não</em>
     pode ser resolvido por conservação de energia do começo ao fim.''',
     r'''<p><b>As duas fases, e a ordem certa.</b> A colisão é
     instantânea e totalmente inelástica: vale momento, não vale energia. A
     subida é lenta e sem atrito: vale energia, não vale momento (o fio
     exerce força externa). Resolver na ordem errada é o erro clássico
     aqui.</p>
     <p><b>A subida.</b> \(v_{\text{bloco}} = \sqrt{2gh}
     = \sqrt{2(9{,}81)(0{,}080)} = 1{,}253\) m/s.</p>
     <p><b>A colisão.</b> \(mv = (M+m)v_{\text{bloco}}\), então</p>
     <p>\[ v = \frac{2{,}010}{0{,}010}\times 1{,}253
        = \underline{252\ \mathrm{m/s}}. \]</p>
     <p><b>A energia.</b> \(K_i = \tfrac12(0{,}010)(252)^2 = 317\) J contra
     \(K_f = \tfrac12(2{,}010)(1{,}253)^2 = 1{,}58\) J: sobra
     \(0{,}50\ \%\). A fração que resta é exatamente \(m/(M+m)\), e isso
     não é coincidência: pelo exercício anterior, o que sobrevive é
     \(MV^2/2\), e a razão sai em duas linhas.</p>
     <p><b>Por que não dá para usar energia na colisão.</b> Porque 99,5 % da
     energia vai para deformação, calor e som dentro do bloco. Se alguém
     insistir em conservar energia na primeira fase, obtém
     \(v = \sqrt{2gh}\times\sqrt{(M+m)/m} = 17{,}8\) m/s, catorze vezes
     menor que o valor certo.</p>
     <p><b>O que torna o aparelho útil.</b> Justamente essa perda enorme. A
     grandeza medida, \(h\), depende da velocidade da bala de maneira
     linear, e não quadrática, o que torna o instrumento preciso com uma
     régua comum. O pêndulo balístico foi inventado por Benjamin Robins em
     1742 e foi o primeiro meio confiável de medir velocidade de
     projétil.</p>'''),

    ('13.4  Por que o moderador de um reator é leve',
     r'''Mostre que, numa colisão elástica frontal com um alvo parado, a
     energia que resta ao projétil é
     \(E_f/E_i = \left[(A-1)/(A+1)\right]^2\), com \(A = m_2/m_1\). Calcule
     para hidrogênio, carbono e urânio-238, e estime quantas colisões um
     nêutron de 2 MeV precisa para chegar a 0,025 eV em cada um.''',
     r'''<p><b>A fórmula.</b> Da colisão unidimensional com \(e = 1\) e
     \(u_2 = 0\):</p>
     <p>\[ v_1 = \frac{m_1-m_2}{m_1+m_2}u_1
        \quad\Longrightarrow\quad
        \frac{E_f}{E_i} = \left(\frac{1-A}{1+A}\right)^2 \equiv \alpha. \]</p>
     <p><b>Os números</b> (com \(m_1\) o nêutron):</p>
     <p>hidrogênio, \(A = 1\): \(\alpha = 0\), o nêutron <b>para</b>;<br>
     carbono, \(A = 12\): \(\alpha = (11/13)^2 = 0{,}716\);<br>
     urânio, \(A = 238\): \(\alpha = (237/239)^2 = 0{,}983\).</p>
     <p><b>Quantas colisões.</b> Numa batida qualquer, e não frontal, a
     energia final se distribui uniformemente entre \(\alpha E_i\) e
     \(E_i\), e o que é constante em média é o logaritmo:</p>
     <p>\[ \xi = \med{\ln\frac{E_i}{E_f}}
        = 1 + \frac{\alpha\ln\alpha}{1-\alpha}. \]</p>
     <p>O número de colisões é \(\ln(E_0/E_t)/\xi\), com
     \(\ln(2\times10^6/0{,}025) = 18{,}2\):</p>
     <p>hidrogênio, \(\xi = 1\): <b>18</b> colisões;<br>
     carbono, \(\xi = 0{,}158\): <b>115</b> colisões;<br>
     urânio, \(\xi = 0{,}0084\): <b>2170</b> colisões.</p>
     <p><b>A conclusão de projeto.</b> Moderar nêutrons pede núcleos leves,
     e a água comum seria perfeita se não fosse por um detalhe que esta
     conta não vê: o hidrogênio <em>absorve</em> nêutrons com facilidade,
     formando deutério. Daí a água pesada e o grafite, que moderam pior mas
     não comem o nêutron. O reator de Fermi, em 1942, foi de grafite por
     essa razão, e o programa alemão perdeu a guerra do reator em parte por
     ter descartado o grafite com base numa medida de absorção feita com
     material impuro.</p>'''),

    ('13.5  Esferas rígidas, e o que a seção de choque mede',
     r'''Calcule \(d\sigma/d\Omega\) para o espalhamento de uma esfera
     rígida de raio \(R\), mostrando que é isotrópico e que a seção de
     choque total vale \(\pi R^2\). Compare com Rutherford e diga o que a
     forma angular está informando em cada caso.''',
     r'''<p><b>A geometria.</b> A partícula atinge a esfera num ponto em que
     a normal faz ângulo \(\gamma\) com a direção de incidência, e reflete
     especularmente, de modo que \(\theta = \pi - 2\gamma\). O parâmetro de
     impacto é \(b = R\sen\gamma = R\cos(\theta/2)\).</p>
     <p><b>A seção de choque.</b> Com
     \(|db/d\theta| = (R/2)\sen(\theta/2)\):</p>
     <p>\[ \der{\sigma}{\Omega} = \frac{b}{\sen\theta}\left|\der{b}{\theta}\right|
        = \frac{R^2\cos(\theta/2)\sen(\theta/2)}{2\sen\theta}
        = \frac{R^2}{4}, \]</p>
     <p>usando \(\sen\theta = 2\sen(\theta/2)\cos(\theta/2)\). É
     independente de \(\theta\): o espalhamento é <b>isotrópico</b>.
     Integrando sobre os \(4\pi\) esterradianos,
     \(\sigma = \pi R^2\), que é a área da sombra da esfera, como o bom
     senso exige.</p>
     <p><b>A comparação.</b> O contraste com Rutherford é o ponto do
     exercício. Esfera rígida: alcance finito, seção total finita,
     distribuição plana. Coulomb: alcance infinito, seção total divergente,
     distribuição com um pico feroz em \(\theta\) pequeno.</p>
     <p><b>E o que isso informa.</b> A forma angular é uma impressão digital
     do potencial. Um espalhamento isotrópico diz que o alvo tem uma borda
     bem definida; um \(1/\sen^4(\theta/2)\) diz que o potencial é \(1/r\)
     até distâncias muito menores que o alvo. Medir a distribuição angular e
     ler dela o potencial é o que se faz, com a mesma lógica, desde Geiger e
     Marsden até os aceleradores de hoje. Foi assim, aliás, que se descobriu
     que o próton não é pontual: em energia alta a distribuição se afasta da
     de uma carga pontual, e o desvio mede o tamanho dele.</p>'''),

    ('13.6  O ângulo máximo de um projétil pesado',
     r'''Demonstre que, se \(m_1 &gt; m_2\), o ângulo de espalhamento no
     laboratório não pode passar de \(\sen\theta_{\max} = m_2/m_1\). Use o
     argumento geométrico das velocidades, e não a fórmula da tangente.
     Depois explique o que esse resultado tem a ver com 1911.''',
     r'''<p><b>A construção.</b> A velocidade do projétil no laboratório é
     sempre</p>
     <p>\[ \vet{v}_1 = \vet{V} + \vet{v}_1', \]</p>
     <p>com \(\vet{V}\) a velocidade do centro de massa, fixa, e
     \(\vet{v}_1'\) a velocidade no referencial do CM, que na colisão
     elástica <b>mantém o módulo</b> e só gira. Então a ponta de
     \(\vet{v}_1\) percorre uma circunferência de raio
     \(v_1' = u_1m_2/M\), centrada na ponta de \(\vet{V}\), cujo módulo é
     \(V = u_1m_1/M\).</p>
     <p><b>Os dois casos.</b> Se \(v_1' &gt; V\), isto é \(m_2 &gt; m_1\), a
     origem fica <em>dentro</em> da circunferência, e \(\vet{v}_1\) pode
     apontar para qualquer lado: todos os ângulos são possíveis, inclusive
     180°. Se \(v_1' &lt; V\), a origem fica <em>fora</em>, e o vetor só
     alcança os pontos da circunferência vistos da origem: há um ângulo
     máximo, o da tangente.</p>
     <p><b>O ângulo.</b> No triângulo retângulo formado pelo centro, o ponto
     de tangência e a origem, o cateto oposto é o raio e a hipotenusa é a
     distância ao centro:</p>
     <p>\[ \sen\theta_{\max} = \frac{v_1'}{V}
        = \frac{u_1m_2/M}{u_1m_1/M} = \frac{m_2}{m_1}. \]</p>
     <p>Para \(m_1 = m_2\) a origem cai sobre a circunferência e o máximo é
     90°, que é o resultado da seção 4 visto por outro caminho.</p>
     <p><b>E 1911.</b> Partículas alfa (massa 4) voltando para trás numa
     folha de ouro exigem um alvo mais pesado que 4, e portanto não podem
     estar batendo em elétrons, que são dois mil vezes mais leves: contra um
     elétron, a alfa nem sente. O alvo tinha de ser pesado. Pelo
     \(1/\sen^4(\theta/2)\), tinha também de ser concentrado, porque uma
     carga espalhada não produz campo forte o bastante perto do centro. As
     duas exigências juntas, pesado e minúsculo, são o núcleo atômico, e
     ambas saem de contas que cabem nesta página.</p>'''),
]
