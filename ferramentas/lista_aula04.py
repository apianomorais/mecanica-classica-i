# -*- coding: utf-8 -*-
"""Exercícios propostos do módulo 4."""

LISTA = [
    ('4.1  As três integrais, no papel',
     r'''Para a força \(\vet{F} = (-y,\,x)\), calcule à mão o trabalho de
     \((0,0)\) a \((1,1)\) pela reta e pelo caminho em duas pernas, e confirme
     os valores que o programa imprime. Depois mostre que a diferença entre os
     dois é o fluxo do rotacional pela área entre eles, e explique por que
     nenhuma função \(U(x,y)\) pode existir para essa força.''',
     r'''<p><b>Pela reta.</b> Parametrize \(x = s\), \(y = s\), com \(s\) de 0
     a 1, de modo que \(d\vet{r} = (1,1)\,ds\):</p>
     <p>\[ W = \int_0^1 (-s,\,s)\cdot(1,1)\,ds = \int_0^1 (-s + s)\,ds = 0. \]</p>
     <p>O integrando é nulo ponto a ponto: ao longo da diagonal, essa força é
     perpendicular ao deslocamento em todo lugar.</p>
     <p><b>Pelas duas pernas.</b> Na primeira, \(y = 0\) e
     \(d\vet{r} = (dx,0)\), de modo que \(\vet{F}\cdot d\vet{r} = -y\,dx = 0\).
     Na segunda, \(x = 1\) e \(d\vet{r} = (0,dy)\), de modo que
     \(\vet{F}\cdot d\vet{r} = x\,dy = dy\):</p>
     <p>\[ W = 0 + \int_0^1 dy = 1. \]</p>
     <p><b>A diferença e o teorema de Green.</b> O caminho fechado formado pela
     ida em duas pernas e pela volta em linha reta encerra o triângulo de
     vértices \((0,0)\), \((1,0)\) e \((1,1)\), de área \(1/2\). Como
     \(\rot{\vet{F}} = \partial_x(x) - \partial_y(-y) = 2\), constante,</p>
     <p>\[ \oint \vet{F}\cdot d\vet{r} = \iint 2\,dA = 2\cdot\frac12 = 1, \]</p>
     <p>que é exatamente a diferença \(1 - 0\) entre os dois caminhos.</p>
     <p><b>Por que não existe \(U\).</b> Se existisse, teríamos
     \(F_x = -\partial U/\partial x\) e \(F_y = -\partial U/\partial y\). As
     derivadas cruzadas de uma função suave comutam, de modo que seria preciso
     ter \(\partial F_x/\partial y = \partial F_y/\partial x\), isto é,
     \(-1 = +1\). A exigência não é sobre a força ser estranha: é sobre a
     igualdade das derivadas cruzadas, e essa força simplesmente não a
     satisfaz.</p>''' ),

    ('4.2  Prever o erro do Euler antes de rodar',
     r'''No oscilador harmônico \(\ddot{x} = -\omega^2 x\), escreva um passo do
     método de Euler explícito como uma matriz \(2\times2\) agindo em
     \((x,\,v/\omega)\) e mostre que ela multiplica a distância à origem do
     espaço de fase por \(\sqrt{1+\omega^2\Delta t^2}\) a cada passo. Use isso
     para prever a razão \(E_{\text{final}}/E_0\) depois de 200 períodos com
     \(\omega = 1\) e \(\Delta t = 0{,}01\), e compare com o que o programa
     mede.''',
     r'''<p><b>A matriz.</b> Um passo de Euler explícito é
     \(x_{n+1} = x_n + \Delta t\,v_n\) e
     \(v_{n+1} = v_n - \Delta t\,\omega^2 x_n\). Escrevendo
     \(u = v/\omega\) para que as duas coordenadas tenham a mesma dimensão, e
     chamando \(\varepsilon = \omega\Delta t\),</p>
     <p>\[ \begin{pmatrix} x_{n+1} \\ u_{n+1}\end{pmatrix}
        = \begin{pmatrix} 1 & \varepsilon \\ -\varepsilon & 1\end{pmatrix}
          \begin{pmatrix} x_n \\ u_n\end{pmatrix}. \]</p>
     <p><b>O que ela faz.</b> Essa matriz é
     \(\sqrt{1+\varepsilon^2}\) vezes uma matriz de rotação de ângulo
     \(\arctg\varepsilon\). Ela gira o ponto no espaço de fase, que é o que se
     espera, e ao mesmo tempo o afasta da origem pelo fator
     \(\sqrt{1+\varepsilon^2} &gt; 1\). Como
     \(E = \frac{m\omega^2}{2}(x^2 + u^2)\) é proporcional ao quadrado da
     distância à origem, a energia é multiplicada por \(1+\varepsilon^2\) em
     cada passo. O crescimento não depende do sinal de nada nem da fase: é
     geométrico e inevitável.</p>
     <p><b>A previsão.</b> Em 200 períodos há
     \(N = 200\cdot 2\pi/\Delta t = 125\,663\) passos, de modo que</p>
     <p>\[ \frac{E_N}{E_0} = \left(1+\varepsilon^2\right)^{N}
        = \left(1{,}0001\right)^{125663} = 2{,}86551\times10^{5}. \]</p>
     <p>O programa mede \(2{,}86551\times10^{5}\). A previsão e a medida
     coincidem nos <b>nove dígitos</b> impressos, o que diz uma coisa útil
     sobre erro numérico: ele raramente é aleatório. Quase sempre tem fórmula,
     e quando tem, dá para decidir o passo antes de gastar a primeira hora de
     processamento.</p>
     <p><b>Para onde isso aponta.</b> Expandindo,
     \(\left(1+\varepsilon^2\right)^{N} \simeq e^{N\varepsilon^2}
     = e^{\omega^2\Delta t\,t}\): o erro cresce exponencialmente no tempo, com
     taxa proporcional ao passo. Dividir o passo por dez não divide o erro por
     dez; muda o expoente. É por isso que, para integrações longas, mexer no
     passo é remédio fraco e trocar de método é remédio forte.</p>''' ),

    ('4.3  O looping, e o ponto em que o carrinho desgruda',
     r'''Um carrinho é solto do repouso de uma altura \(h\) numa pista lisa que
     termina num <em>looping</em> circular vertical de raio \(R\). Encontre a
     menor altura que permite completar a volta. Depois, soltando-o de
     \(h = 2R\), ache o ponto exato em que ele perde contato com a pista.''',
     r'''<p><b>A condição no topo.</b> No alto do <em>looping</em>, o peso e a
     normal apontam os dois para o centro:</p>
     <p>\[ N + mg = \frac{mv^2}{R}. \]</p>
     <p>A pista empurra, mas não puxa, de modo que \(N \ge 0\). O caso limite é
     \(N = 0\), em que a gravidade sozinha faz o papel de força centrípeta:
     \(v_{\text{topo}}^2 = gR\). Note que o carrinho precisa estar
     <em>andando</em> no topo, e depressa; a intuição de "chegar lá com
     velocidade zero" descreve um carrinho que já caiu antes.</p>
     <p><b>A energia.</b> Pista lisa, só o peso trabalha:</p>
     <p>\[ mgh = mg(2R) + \frac{mv_{\text{topo}}^2}{2}
        = 2mgR + \frac{mgR}{2}
        \quad\Longrightarrow\quad h_{\min} = \frac{5R}{2}. \]</p>
     <p>Com \(R = 3\) m dá \(h = 7{,}5\) m, e o resultado não depende da massa.</p>
     <p><b>Soltando de \(h = 2R\).</b> Aí ele não completa a volta. Seja
     \(\varphi\) o ângulo medido a partir do topo, com o carrinho na altura
     \(y = R + R\cos\varphi\). A componente radial do peso é
     \(mg\cos\varphi\), e a condição de contato é</p>
     <p>\[ mg\cos\varphi - N = \frac{mv^2}{R}, \qquad
        v^2 = 2g\left(h - y\right). \]</p>
     <p>Com \(N = 0\) e \(h = 2R\):</p>
     <p>\[ gR\cos\varphi = 2g\left(2R - R - R\cos\varphi\right)
        \quad\Longrightarrow\quad 3\cos\varphi = 2, \]</p>
     <p>de modo que \(\cos\varphi = 2/3\), \(\varphi = 48{,}2^\circ\) e
     \(y = 5R/3\). Com \(R = 3\) m, ele desgruda a 5,00 m do chão, a dois
     terços do caminho até o topo, e dali em diante descreve uma parábola
     dentro do <em>looping</em>. É o mesmo cálculo que decide se um satélite
     rasante continua em órbita ou cai.</p>''' ),

    ('4.4  Qualquer mínimo é uma mola',
     r'''O potencial de Lennard-Jones entre dois átomos neutros é
     \(U(r) = 4\epsilon\left[(\sigma/r)^{12} - (\sigma/r)^{6}\right]\).
     Encontre a distância de equilíbrio e a profundidade do poço, e obtenha a
     frequência das pequenas oscilações em torno do mínimo. Aplique ao
     argônio, com \(\epsilon/k_B = 120\) K, \(\sigma = 3{,}4\) Å e massa
     atômica 39,95 u, lembrando que num par de átomos iguais a massa que entra
     na conta é a reduzida, \(\mu = m/2\).''',
     r'''<p><b>O mínimo.</b> Derivando e igualando a zero:</p>
     <p>\[ \der{U}{r} = 4\epsilon\left[-\frac{12\sigma^{12}}{r^{13}}
        + \frac{6\sigma^{6}}{r^{7}}\right] = 0
        \quad\Longrightarrow\quad r_0 = 2^{1/6}\sigma = 1{,}1225\,\sigma, \]</p>
     <p>e substituindo, \(U(r_0) = -\epsilon\). A profundidade do poço é o
     próprio \(\epsilon\), que é por isso que ele aparece com esse nome na
     fórmula.</p>
     <p><b>A curvatura.</b> Derivando mais uma vez e avaliando em \(r_0\):</p>
     <p>\[ k = U''(r_0) = \frac{72\,\epsilon}{2^{1/3}\sigma^2}
        = 57{,}1464\,\frac{\epsilon}{\sigma^2}. \]</p>
     <p>Perto do fundo, \(U \simeq -\epsilon + \frac12 k (r-r_0)^2\): uma mola,
     com \(\omega = \sqrt{k/\mu}\). Nada no argumento usou a forma particular
     do Lennard-Jones, e é isso que torna o resultado interessante: todo
     mínimo liso de todo potencial é uma mola para amplitudes pequenas.</p>
     <p><b>No argônio.</b> Com
     \(\epsilon = 120\,k_B = 1{,}657\times10^{-21}\) J,
     \(\sigma = 3{,}4\times10^{-10}\) m e
     \(\mu = 39{,}95\,\mathrm{u}/2 = 3{,}317\times10^{-26}\) kg:</p>
     <p>\[ \omega = \sqrt{\frac{57{,}15\,\epsilon}{\mu\sigma^2}}
        = 4{,}97\times10^{12}\ \mathrm{rad/s},
        \qquad f = 7{,}91\times10^{11}\ \mathrm{Hz}, \]</p>
     <p>o que corresponde a um período de 1,26 ps e a um número de onda de
     26 cm⁻¹, bem dentro do infravermelho distante. É assim que se mede \(k\)
     na prática: não empurrando átomos com uma régua, e sim olhando em que
     frequência eles absorvem.</p>
     <p><b>Um aviso sobre a amplitude.</b> À temperatura ambiente, a energia
     térmica típica \(k_BT\) vale 2,5 vezes a profundidade do poço do argônio.
     O par simplesmente não fica ligado, e é por isso que o argônio é gás. A
     aproximação harmônica descreve o fundo do poço, e dizer em que
     temperatura o fundo do poço importa é outra conversa, que pertence à
     Física Estatística.</p>''' ),

    ('4.5  Velocidade de escape, sem foguete',
     r'''Use a conservação da energia com \(U = -GMm/r\) para obter a
     velocidade de escape de um corpo lançado da superfície de um planeta.
     Calcule para a Terra e para a Lua, e diga até que altura sobe um projétil
     lançado da Terra com metade da velocidade de escape.''',
     r'''<p><b>A conta.</b> Escapar é chegar ao infinito com velocidade nula,
     isto é, ter energia mecânica total igual a zero:</p>
     <p>\[ \frac{mv_e^2}{2} - \frac{GMm}{R} = 0
        \quad\Longrightarrow\quad v_e = \sqrt{\frac{2GM}{R}}. \]</p>
     <p>A massa do projétil sai da conta, e a direção do lançamento não
     aparece: energia é escalar. Um tiro para cima e um tiro na horizontal
     escapam com a mesma rapidez, desde que nenhum dos dois esbarre no
     planeta.</p>
     <p><b>Os números.</b> Terra, com
     \(M = 5{,}972\times10^{24}\) kg e \(R = 6371\) km:
     \(v_e = 11{,}19\) km/s. Lua, com
     \(M = 7{,}342\times10^{22}\) kg e \(R = 1737\) km:
     \(v_e = 2{,}38\) km/s, quase cinco vezes menor. É essa diferença que
     permitiu ao módulo lunar subir com um motor pequeno, e é ela que explica
     por que a Lua não tem atmosfera: as moléculas mais leves atingem
     \(2{,}4\) km/s com facilidade na temperatura do dia lunar.</p>
     <p><b>Com metade da velocidade.</b> Agora a energia é negativa, e o corpo
     volta. No ponto mais alto a velocidade é nula:</p>
     <p>\[ \frac{v_e^2}{8} - \frac{GM}{R} = -\frac{GM}{r_{\max}}
        \quad\Longrightarrow\quad \frac{1}{r_{\max}}
        = \frac{1}{R}-\frac{1}{4R} = \frac{3}{4R}, \]</p>
     <p>de modo que \(r_{\max} = 4R/3\) e a altura é \(R/3 = 2124\) km. Metade
     da velocidade não dá um terço do caminho ao infinito, dá 2124 km: a
     relação entre velocidade e alcance é tudo menos linear, e é ela que torna
     o lançamento espacial um problema difícil.</p>
     <p><b>Cuidado com a leitura.</b> Esses 11,19 km/s não são a velocidade com
     que um foguete viaja. Um foguete acelera durante minutos e nunca chega
     perto disso na baixa atmosfera, onde o arrasto o destruiria. A velocidade
     de escape é a velocidade de um corpo <em>lançado de uma vez</em>, como
     uma bala de canhão, que é exatamente o cenário que Newton desenhou.</p>''' ),

    ('4.6  O atrito que esquenta: dois trabalhos que não se cancelam',
     r'''Um bloco de 2,0 kg está sobre uma prancha de 5,0 kg, que desliza sem
     atrito no chão. Entre o bloco e a prancha, \(\mu_c = 0{,}30\). Uma força
     horizontal de 40 N puxa a prancha. Mostre que os dois escorregam um sobre
     o outro, calcule o trabalho do atrito sobre cada um ao fim de 1,0 s e
     mostre que a soma dos dois não é nula. Diga o que é essa diferença.''',
     r'''<p><b>Escorregam?</b> Se andassem juntos, a aceleração comum seria
     \(a = 40/7 = 5{,}71\ \mathrm{m/s^2}\), e seria preciso que o atrito
     fornecesse \(m_1a = 11{,}4\) N ao bloco. O máximo disponível é
     \(\mu m_1 g = 5{,}88\) N. Não dá: escorregam. (A força mínima para isso é
     \((m_1+m_2)\mu g = 20{,}6\) N.)</p>
     <p><b>As acelerações.</b> Sobre o bloco age apenas o atrito, para a frente,
     que é a reação ao arrasto que ele exerce na prancha:</p>
     <p>\[ a_1 = \mu g = 2{,}942\ \mathrm{m/s^2}, \qquad
        a_2 = \frac{F - \mu m_1 g}{m_2} = 6{,}823\ \mathrm{m/s^2}. \]</p>
     <p><b>Os deslocamentos em 1,0 s.</b>
     \(d_1 = 1{,}471\) m e \(d_2 = 3{,}412\) m, de modo que a prancha escorregou
     \(\Delta = 1{,}941\) m sob o bloco.</p>
     <p><b>Os dois trabalhos.</b> A força de atrito tem o mesmo módulo
     \(f = 5{,}884\) N nos dois corpos, e sentidos opostos, mas os pontos de
     aplicação percorrem distâncias diferentes:</p>
     <p>\[ W_{\text{bloco}} = +f\,d_1 = +8{,}655\ \mathrm{J}, \qquad
        W_{\text{prancha}} = -f\,d_2 = -20{,}074\ \mathrm{J}. \]</p>
     <p>\[ W_{\text{bloco}} + W_{\text{prancha}} = -11{,}418\ \mathrm{J}
        = -f\,\Delta. \]</p>
     <p><b>O que é essa diferença.</b> É o calor gerado na interface, e a
     fórmula \(Q = f\Delta\) é geral: o calor do atrito é a força vezes o
     <em>escorregamento relativo</em>, não vezes o deslocamento de nenhum dos
     dois. Conferindo o balanço: a força externa realizou
     \(F d_2 = 136{,}464\) J, a energia cinética do conjunto ao fim de 1 s é
     \(125{,}046\) J, e a diferença é 11,418 J, o mesmo número.</p>
     <p><b>A lição.</b> Pares de ação e reação sempre têm forças simétricas, e
     nem sempre têm trabalhos simétricos. Os trabalhos só se cancelam quando os
     dois pontos de aplicação têm o mesmo deslocamento, que é o caso do
     contato sem escorregamento. Quando há escorregamento, a soma dos
     trabalhos internos é exatamente a energia que deixa a mecânica e vira
     agitação molecular.</p>''' ),
]
