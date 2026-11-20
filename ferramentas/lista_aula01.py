# -*- coding: utf-8 -*-
"""Exercícios propostos do módulo 1."""

LISTA = [
    ('1.1  A rotação preserva o produto escalar',
     r'''Mostre, usando apenas \(R^{\mathsf T}R = \mathbb{1}\), que a rotação
     preserva o produto escalar de dois vetores quaisquer, e conclua daí que
     preserva módulos e ângulos. Depois explique por que uma matriz ortogonal
     com \(\det R = -1\) também preserva o produto escalar e, ainda assim, não
     é uma rotação.''',
     r'''<p><b>A conta.</b> Com \(a'_i = R_{ij}a_j\) e \(b'_i = R_{ik}b_k\),</p>
     <p>\[ \vet{a}'\cdot\vet{b}' = a'_ib'_i = R_{ij}a_jR_{ik}b_k
        = \left(R^{\mathsf T}R\right)_{jk}a_jb_k
        = \delta_{jk}a_jb_k = \vet{a}\cdot\vet{b}. \]</p>
     <p><b>As consequências.</b> Tomando \(\vet{b} = \vet{a}\), o módulo não
     muda. E como \(\cos\theta = \vet{a}\cdot\vet{b}/ab\) tem numerador e
     denominador invariantes, o ângulo também não muda. Rotação é
     exatamente isso: a transformação que preserva a geometria.</p>
     <p><b>A reflexão.</b> A demonstração acima usou apenas a ortogonalidade,
     e não o determinante, de modo que vale igualmente para
     \(\det R = -1\). O que a reflexão estraga não é comprimento nem ângulo, e
     sim a <em>orientação</em>: ela leva uma mão direita numa esquerda. Para
     ver isso, basta aplicar a reflexão a três vetores com produto misto
     positivo e notar que o produto misto fica negativo.</p>
     <p><b>Por que isso importa.</b> O conjunto das matrizes ortogonais com
     determinante \(+1\) é um grupo, chamado <a href="https://pt.wikipedia.org/wiki/Grupo_ortogonal">\(SO(3)\)</a>, e é ele que descreve
     os movimentos rígidos possíveis de um corpo. A reflexão não está nele
     porque nenhum corpo real consegue atravessar o espelho.</p>''' ),

    ('1.2  Três números que não são vetor',
     r'''Dê dois exemplos de trios de números que não formam vetor e justifique
     em cada caso. Depois responda: a velocidade angular \(\vet{\omega}\) é
     vetor? E um ângulo de rotação finito?''',
     r'''<p><b>Exemplo 1: duas coordenadas e uma temperatura.</b> O trio
     \((x, y, T)\) tem três números, mas sob rotação dos eixos as duas
     primeiras componentes se misturam e a terceira não tem como acompanhar,
     porque \(T\) não é componente de nada. Tratar o trio como vetor produz
     somas de metros com kelvin.</p>
     <p><b>Exemplo 2: as três notas de um aluno em três provas.</b> O trio
     \((n_1, n_2, n_3)\) é uma lista perfeitamente legítima, e nada nela se
     transforma sob rotação de eixos, porque não há eixos. A soma das notas é
     útil; o "módulo" \(\sqrt{n_1^2+n_2^2+n_3^2}\) não significa coisa
     alguma.</p>
     <p><b>A velocidade angular</b> é vetor, e isso não é óbvio. Velocidades
     angulares somam-se como vetores, obedecem à lei de transformação e têm
     direção bem definida. Tecnicamente ela é um <em>pseudovetor</em>, isto é,
     comporta-se como vetor sob rotação mas não troca de sinal sob reflexão. A
     Mecânica Clássica II dedica um módulo inteiro a esse ponto.</p>
     <p><b>O ângulo de rotação finito não é vetor</b>, e a prova é
     experimental: gire um livro 90° em torno de \(x\) e depois 90° em torno de
     \(y\); depois refaça na ordem inversa. O livro termina em orientações
     diferentes. Como a soma de vetores é comutativa e a composição de rotações
     finitas não é, rotações finitas não podem ser vetores. Rotações
     <em>infinitesimais</em>, por outro lado, comutam até primeira ordem, e é
     por isso que \(\vet{\omega} = d\vet{\theta}/dt\) é vetor.</p>''' ),

    ('1.3  Uma conta completa com os dois produtos',
     r'''Dados \(\vet{a} = (2,1,-1)\), \(\vet{b} = (1,3,2)\) e
     \(\vet{c} = (0,-2,4)\), calcule \(\vet{a}\cdot\vet{b}\),
     \(\vet{a}\cruz\vet{b}\), o ângulo entre \(\vet{a}\) e \(\vet{b}\), a área
     do paralelogramo que eles formam e o volume do paralelepípedo dos três.
     Verifique que \(\vet{a}\cruz\vet{b}\) é perpendicular aos dois.''',
     r'''<p><b>Produto escalar.</b></p>
     <p>\[ \vet{a}\cdot\vet{b} = 2(1) + 1(3) + (-1)(2) = 3. \]</p>
     <p><b>Produto vetorial.</b> Pelo determinante,</p>
     <p>\[ \vet{a}\cruz\vet{b}
        = \left(1\cdot2-(-1)\cdot3\right)\vers{x}
        - \left(2\cdot2-(-1)\cdot1\right)\vers{y}
        + \left(2\cdot3-1\cdot1\right)\vers{z}
        = (5,\,-5,\,5). \]</p>
     <p><b>Perpendicularidade.</b>
     \((5,-5,5)\cdot(2,1,-1) = 10-5-5 = 0\) e
     \((5,-5,5)\cdot(1,3,2) = 5-15+10 = 0\). Confere.</p>
     <p><b>Ângulo.</b> Com \(a = \sqrt6 = 2{,}449\) e
     \(b = \sqrt{14} = 3{,}742\),</p>
     <p>\[ \cos\theta = \frac{3}{\sqrt6\sqrt{14}} = 0{,}3273
        \;\Longrightarrow\;
        \theta = 70{,}9^\circ. \]</p>
     <p><b>Área.</b> \(\left|\vet{a}\cruz\vet{b}\right| = \sqrt{75} =
     8{,}660\), e a conferência pelo seno:
     \(ab\sen\theta = 9{,}165\times0{,}9449 = 8{,}660\).</p>
     <p><b>Volume.</b></p>
     <p>\[ \vet{a}\cdot\left(\vet{b}\cruz\vet{c}\right)
        = \begin{vmatrix} 2 & 1 & -1 \\ 1 & 3 & 2 \\ 0 & -2 & 4\end{vmatrix}
        = 30. \]</p>
     <p>Positivo, de modo que os três formam uma mão direita, nessa ordem.</p>
     <p><b>Fecha com o programa.</b> O <code>vetores.py</code> confere todos
     esses números, inclusive a igualdade entre o produto misto e o
     determinante, em \(10^{-15}\).</p>''' ),

    ('1.4  A aceleração centrípeta deduzida',
     r'''Um ponto gira com velocidade angular \(\vet{\omega}\) constante em
     torno de um eixo que passa pela origem. A sua aceleração é
     \(\vet{a} = \vet{\omega}\cruz\left(\vet{\omega}\cruz\vet{r}\right)\).
     Use a identidade BAC-CAB para mostrar que, quando \(\vet{r}\) é
     perpendicular ao eixo, isso dá o resultado conhecido do ensino médio. E
     quando \(\vet{r}\) não é perpendicular?''',
     r'''<p><b>Aplicando a identidade</b> com \(\vet{a}\to\vet{\omega}\),
     \(\vet{b}\to\vet{\omega}\) e \(\vet{c}\to\vet{r}\):</p>
     <p>\[ \vet{\omega}\cruz\left(\vet{\omega}\cruz\vet{r}\right)
        = \vet{\omega}\left(\vet{\omega}\cdot\vet{r}\right)
        - \vet{r}\left(\vet{\omega}\cdot\vet{\omega}\right)
        = \vet{\omega}\left(\vet{\omega}\cdot\vet{r}\right) - \omega^2\vet{r}. \]</p>
     <p><b>Caso perpendicular.</b> Se \(\vet{r}\perp\vet{\omega}\), o primeiro
     termo some e</p>
     <p>\[ \vet{a} = -\omega^2\vet{r}, \]</p>
     <p>com módulo \(\omega^2r = v^2/r\), apontando para o eixo. É a
     aceleração centrípeta, agora deduzida em vez de decorada.</p>
     <p><b>Caso geral.</b> Decomponha
     \(\vet{r} = \vet{r}_\parallel + \vet{r}_\perp\) em relação ao eixo. O
     termo \(\vet{\omega}\left(\vet{\omega}\cdot\vet{r}\right)\) vale
     \(\omega^2\vet{r}_\parallel\), de modo que</p>
     <p>\[ \vet{a} = \omega^2\vet{r}_\parallel - \omega^2\vet{r}
        = -\omega^2\vet{r}_\perp. \]</p>
     <p>A aceleração continua apontando para o <em>eixo</em>, e não para a
     origem, e o seu módulo é \(\omega^2\) vezes a distância ao eixo. É o
     resultado correto, e é o que faz sentido: um ponto perto do polo de uma
     esfera girante tem aceleração pequena, por mais longe do centro que
     esteja.</p>
     <p><b>Onde isso volta.</b> A aceleração centrífuga aparente, nos
     referenciais em rotação da Mecânica Clássica II, é exatamente o negativo
     desse termo.</p>''' ),

    ('1.5  Do potencial gravitacional para a lei de Newton',
     r'''A energia potencial gravitacional entre duas massas é
     \(U(r) = -GMm/r\), com \(r = \left|\vet{r}\right|\). Calcule
     \(\vet{F} = -\nabla U\) e verifique que o resultado é a lei da gravitação.
     Use que \(\nabla r = \vers{r}\).''',
     r'''<p><b>Primeiro, o gradiente de \(r\).</b> Com
     \(r = \sqrt{x^2+y^2+z^2}\),</p>
     <p>\[ \pder{r}{x} = \frac{x}{r}
        \;\Longrightarrow\;
        \nabla r = \frac{\vet{r}}{r} = \vers{r}. \]</p>
     <p><b>Agora a força.</b> Pela regra da cadeia, como \(U\) só depende de
     \(r\),</p>
     <p>\[ \nabla U = \der{U}{r}\nabla r
        = \frac{GMm}{r^2}\vers{r}, \]</p>
     <p>de onde</p>
     <p>\[ \vet{F} = -\nabla U = -\frac{GMm}{r^2}\vers{r}. \]</p>
     <p>O sinal negativo diz que a força aponta para a origem, isto é, é
     atrativa, e o módulo vai com o inverso do quadrado. É a lei da
     gravitação.</p>
     <p><b>A verificação do rotacional.</b> Qualquer campo da forma
     \(f(r)\vers{r}\) tem rotacional nulo, porque é gradiente de alguma coisa.
     Isso garante que a gravitação é conservativa, que existe energia
     potencial, e que o trabalho entre dois pontos não depende do caminho.
     Todo o módulo 12, com as órbitas de Kepler, se apoia nisso.</p>
     <p><b>Repare na economia.</b> A informação toda estava numa única função
     escalar \(U(r)\). O gradiente extraiu dela as três componentes da força. É
     por essa economia que a mecânica avançada, na Mecânica Clássica II, abandona
     as forças e trabalha com funções escalares.</p>''' ),

    ('1.6  Conservativa ou não, por dois caminhos',
     r'''Considere \(\vet{F}_1 = (yz,\,xz,\,xy)\) e
     \(\vet{F}_2 = (-y,\,x,\,0)\). Calcule o rotacional de cada uma. Para a
     que não for conservativa, calcule a circulação num círculo de raio \(R\)
     centrado na origem e verifique o teorema de Stokes. Para a outra, ache a
     energia potencial.''',
     r'''<p><b>Os rotacionais.</b> Para \(\vet{F}_1\),</p>
     <p>\[ \left(\rot{\vet{F}_1}\right)_z
        = \pder{(xz)}{x} - \pder{(yz)}{y} = z - z = 0, \]</p>
     <p>e o mesmo acontece nas outras duas componentes: \(\rot{\vet{F}_1} =
     0\). Para \(\vet{F}_2\),</p>
     <p>\[ \rot{\vet{F}_2} = \left(1-(-1)\right)\vers{z} = 2\vers{z} \neq 0. \]</p>
     <p><b>O potencial de \(\vet{F}_1\).</b> Procurando \(U\) com
     \(\vet{F}_1 = -\nabla U\), a primeira componente dá
     \(\partial U/\partial x = -yz\), isto é, \(U = -xyz + g(y,z)\). As outras
     duas componentes mostram que \(g\) é constante, de modo que</p>
     <p>\[ U = -xyz + \text{const}. \]</p>
     <p><b>A circulação de \(\vet{F}_2\).</b> No círculo de raio \(R\),
     parametrizado por \(\vet{r} = R(\cos\phi,\sen\phi,0)\), tem-se
     \(\vet{F}_2 = R(-\sen\phi,\cos\phi,0)\) e
     \(d\vet{\ell} = R(-\sen\phi,\cos\phi,0)d\phi\), de modo que
     \(\vet{F}_2\cdot d\vet{\ell} = R^2d\phi\) e</p>
     <p>\[ \oint\vet{F}_2\cdot d\vet{\ell} = 2\pi R^2. \]</p>
     <p><b>Stokes confere:</b> a integral do rotacional sobre o disco é
     \(2\vers{z}\cdot\vers{z}\times\pi R^2 = 2\pi R^2\). Igual.</p>
     <p>Com \(R = 1\) isso dá 6,2832 e com \(R = 2\) dá 25,133, que são
     exatamente os números que o programa do módulo imprime, inclusive para um
     círculo deslocado da origem, porque o rotacional é constante e só a área
     importa.</p>
     <p><b>A moral.</b> Dois testes, duas respostas, mesma conclusão. O do
     rotacional é local e barato; o da circulação é global e é a definição.
     Quando os dois discordam, há um buraco na região, e aí a topologia entra
     na física, o que acontece de fato no <a href="https://pt.wikipedia.org/wiki/Efeito_Aharonov-Bohm">efeito Aharonov-Bohm</a> e nos vórtices
     de um superfluido.</p>''' ),
]
