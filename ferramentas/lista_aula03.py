# -*- coding: utf-8 -*-
"""Exercícios propostos do módulo 3."""

LISTA = [
    ('3.1  A tabela das velocidades terminais',
     r'''Calcule \(k = \rho C_DA/2m\) e a velocidade terminal
     \(v_t = \sqrt{g/k}\) para uma bola de tênis (57 g, 6,7 cm,
     \(C_D = 0{,}50\)), uma bola de golfe (45,9 g, 4,27 cm, \(C_D = 0{,}25\)
     pelas covinhas), uma bola de futebol (430 g, 22 cm, \(C_D = 0{,}25\)) e
     uma gota de chuva de 2 mm de diâmetro (\(C_D = 0{,}47\)). Use
     \(\rho = 1{,}2\ \mathrm{kg/m^3}\). Depois explique por que a gota, que é a
     mais leve de todas, é a que tem o maior \(k\).''',
     r'''<div class="tabela-rolavel">
     <table>
     <thead><tr><th>objeto</th><th>\(k\) (m⁻¹)</th><th>\(v_t\) (m/s)</th>
     <th>km/h</th></tr></thead>
     <tbody>
     <tr><td>bola de tênis</td><td>0,0186</td><td>23,0</td><td>83</td></tr>
     <tr><td>bola de golfe</td><td>0,0047</td><td>45,8</td><td>165</td></tr>
     <tr><td>bola de futebol</td><td>0,0133</td><td>27,2</td><td>98</td></tr>
     <tr><td>gota de 2 mm</td><td>0,2114</td><td>6,8</td><td>25</td></tr>
     </tbody>
     </table>
     </div>
     <p><b>Por que a gota ganha.</b> O que importa não é a massa, e sim a razão
     entre área e massa. A área vai com \(d^2\) e a massa com \(d^3\), de modo
     que</p>
     <p>\[ k = \frac{\rho C_DA}{2m} \propto \frac{d^2}{d^3} = \frac{1}{d}. \]</p>
     <p>Objeto pequeno tem \(k\) grande. É a mesma razão pela qual um inseto
     cai de qualquer altura sem se machucar e um elefante não, e pela qual a
     poeira fica suspensa no ar enquanto a pedra não fica.</p>
     <p><b>E a chuva.</b> Os 6,8 m/s da gota são a razão de a chuva ser
     inofensiva. Sem ar, caindo de uma nuvem a 2 km, ela chegaria a
     \(\sqrt{2gh} = 198\ \mathrm{m/s}\), e cada gota seria um projétil.</p>''' ),

    ('3.2  Três passos de Euler na mão',
     r'''Uma pedra é lançada verticalmente para cima com
     \(v_0 = 20\ \mathrm{m/s}\), sujeita a \(g = 9{,}81\ \mathrm{m/s^2}\) e a
     arrasto \(a_{\text{arr}} = -k|v|v\) com \(k = 0{,}01\ \mathrm{m^{-1}}\).
     Dê três passos de Euler com \(\Delta t = 0{,}5\ \mathrm{s}\), montando a
     tabela de \(y\) e \(v\). Compare a altura obtida com a do caso sem
     arrasto.''',
     r'''<p><b>O sistema</b> tem duas equações:</p>
     <p>\[ \der{y}{t} = v, \qquad \der{v}{t} = -g - k|v|v. \]</p>
     <p><b>Os passos</b>, sempre com os valores antigos do lado direito:</p>
     <div class="tabela-rolavel">
     <table>
     <thead><tr><th>\(n\)</th><th>\(t\) (s)</th><th>\(y\) (m)</th>
     <th>\(v\) (m/s)</th><th>\(dv/dt\) (m/s²)</th></tr></thead>
     <tbody>
     <tr><td>0</td><td>0,0</td><td>0,00</td><td>20,00</td><td>-13,81</td></tr>
     <tr><td>1</td><td>0,5</td><td>10,00</td><td>13,09</td><td>-11,52</td></tr>
     <tr><td>2</td><td>1,0</td><td>16,55</td><td>7,33</td><td>-10,35</td></tr>
     <tr><td>3</td><td>1,5</td><td>20,21</td><td>2,16</td><td>-9,86</td></tr>
     </tbody>
     </table>
     </div>
     <p>A primeira linha sai assim: \(dv/dt = -9{,}81 - 0{,}01\times20\times20
     = -13{,}81\); daí \(y_1 = 0 + 0{,}5\times20 = 10{,}00\) e
     \(v_1 = 20 - 0{,}5\times13{,}81 = 13{,}09\).</p>
     <p><b>Comparação.</b> Sem arrasto, a altura máxima seria
     \(v_0^2/2g = 20{,}39\ \mathrm{m}\), atingida em 2,04 s. Com arrasto, a
     integração fina dá <b>17,10 m</b>: o ar tira 16 % da altura. E a tabela
     acima, feita com \(\Delta t = 0{,}5\) s, chega a <b>21,29 m</b>, isto é,
     erra 24 % e para o lado errado, dando mais altura do que o caso
     <em>sem</em> ar nenhum.</p>
     <p><b>A lição.</b> Esse é o ponto do exercício. Um passo grande não
     apenas erra: erra tanto que inverte a conclusão física, sugerindo que o ar
     <em>ajuda</em> a subir. A tabela feita à mão serve para entender o método,
     e nunca para produzir número confiável. É exatamente o que a terceira vista do widget
     mostra: dividir o passo por dez divide o erro por dez.</p>''' ),

    ('3.3  Por que o ângulo ótimo deixa de ser 45°',
     r'''Sem arrasto, o alcance máximo acontece a 45°. Rode o programa do
     módulo e verifique que, com arrasto, o ângulo ótimo cai. Explique o
     mecanismo físico, sem fórmula.''',
     r'''<p><b>O que o programa dá:</b></p>
     <div class="tabela-rolavel">
     <table>
     <thead><tr><th>\(k\) (m⁻¹)</th><th>ângulo ótimo</th>
     <th>alcance (m)</th></tr></thead>
     <tbody>
     <tr><td>0</td><td>45°</td><td>254,8</td></tr>
     <tr><td>0,001</td><td>44°</td><td>213,9</td></tr>
     <tr><td>0,004</td><td>41°</td><td>150,2</td></tr>
     <tr><td>0,010</td><td>38°</td><td>99,5</td></tr>
     <tr><td>0,020</td><td>35°</td><td>66,8</td></tr>
     </tbody>
     </table>
     </div>
     <p><b>O mecanismo.</b> Sem ar, o alcance é o produto da velocidade
     horizontal pelo tempo de voo, e 45° é o meio-termo exato entre os dois:
     subir mais aumenta o tempo e diminui a velocidade horizontal, na mesma
     proporção.</p>
     <p>Com ar, o tempo de voo deixa de ser gratuito. Cada segundo no ar é um
     segundo em que o arrasto come velocidade, e a trajetória alta, que
     demora mais, paga mais caro. O equilíbrio se desloca para lançamentos mais
     rasos, que trocam tempo de voo por velocidade preservada.</p>
     <p><b>Onde isso aparece.</b> Lançadores de peso usam cerca de 42°, e não
     45°, e parte da diferença é arrasto (a outra parte é que a mão não larga o
     peso no chão, e sim a dois metros de altura, o que também baixa o ângulo
     ótimo). Em balística de longo alcance, com velocidades muito maiores, o
     efeito é enorme.</p>''' ),

    ('3.4  Arrasto linear, e o limite de estabilidade de Euler',
     r'''Para arrasto <em>linear</em>, a queda vertical obedece a
     \(\dot v = -(v - v_t)/\tau\), com solução exata
     \(v(t) = v_t\left(1-e^{-t/\tau}\right)\) partindo do repouso. Mostre que o
     método de Euler aplicado a essa equação só é estável se
     \(\Delta t \lt 2\tau\), e diga o que acontece acima disso.''',
     r'''<p><b>O passo de Euler</b> para essa equação é</p>
     <p>\[ v_{n+1} = v_n + \Delta t\left(-\frac{v_n-v_t}{\tau}\right)
        = v_t + \left(1-\frac{\Delta t}{\tau}\right)\left(v_n-v_t\right). \]</p>
     <p>Chamando de \(e_n = v_n - v_t\) o afastamento do valor final,</p>
     <p>\[ e_{n+1} = \left(1-\frac{\Delta t}{\tau}\right)e_n
        \;\Longrightarrow\;
        e_n = \left(1-\frac{\Delta t}{\tau}\right)^{n}e_0. \]</p>
     <p><b>A condição.</b> O erro só encolhe se o fator for menor que 1 em
     módulo:</p>
     <p>\[ \left|1-\frac{\Delta t}{\tau}\right| \lt 1
        \;\Longleftrightarrow\;
        0 \lt \Delta t \lt 2\tau. \]</p>
     <p><b>O que acontece acima.</b> Para \(\Delta t = 2\tau\) o fator vale
     \(-1\) e a solução fica oscilando entre dois valores para sempre, sem
     convergir. Acima disso o fator é menor que \(-1\) e a solução
     <em>explode</em>, alternando de sinal e crescendo sem limite. Com
     \(\tau = 5\) s e \(\Delta t = 12\) s, quarenta passos levam a velocidade a
     \(-3{,}5\times10^{7}\) m/s, o que é absurdo em todos os sentidos.</p>
     <p><b>A lição.</b> Instabilidade não é falta de precisão: é o método
     produzindo lixo com aparência de número. E repare que o resultado não
     depende de quanto se quer de precisão, e sim do tempo característico do
     problema. Todo sistema com um tempo curto escondido, como uma mola muito
     rígida, impõe um passo curto a métodos explícitos, mesmo que o movimento
     interessante seja lento. É o que se chama de problema rígido, e é por isso
     que existem métodos implícitos.</p>''' ),

    ('3.5  Quanto custa cada algarismo',
     r'''Pelo widget, com os valores iniciais, Euler com
     \(\Delta t = 0{,}2\) s erra cerca de 2,4 m no alcance de 149 m. Estime
     quantos passos Euler precisa para errar menos de 1 cm, e quantos o RK4
     precisa. Compare o custo em avaliações da derivada.''',
     r'''<p><b>Euler.</b> O erro é proporcional a \(\Delta t\), de modo que
     para cair de 2,4 m a 0,01 m é preciso dividir o passo por 240:</p>
     <p>\[ \Delta t = \frac{0{,}2}{240} = 8{,}3\times10^{-4}\ \mathrm{s}. \]</p>
     <p>Com um voo de cerca de 7 s, isso dá <b>8400 passos</b>, e como Euler faz
     uma avaliação da derivada por passo, <b>8400 avaliações</b>.</p>
     <p><b>RK4.</b> O erro do RK4 com \(\Delta t = 0{,}2\) s é de
     \(2{,}0\times10^{-5}\) m, pela tabela do programa, portanto já está
     <em>mil vezes</em> melhor que o alvo. Mesmo com \(\Delta t = 0{,}2\) s
     bastam 35 passos, isto é, <b>140 avaliações</b>, porque o RK4 faz quatro
     por passo.</p>
     <p><b>A conta final.</b> 8400 contra 140: o RK4 é sessenta vezes mais
     barato para a mesma precisão, apesar de custar quatro vezes mais por
     passo. A vantagem cresce com a precisão exigida, porque os expoentes são
     diferentes.</p>
     <p><b>Então por que aprender Euler?</b> Porque o RK4 é Euler aplicado
     quatro vezes com pesos escolhidos, e quem não entendeu a ideia de andar na
     direção da derivada não entende o refinamento. E porque, para muitos
     problemas de sala, Euler com passo pequeno resolve, e o tempo do aluno é
     mais caro que o do computador.</p>''' ),

    ('3.6  Um sistema maior, sem mudar o método',
     r'''Escreva o vetor de estado e a função derivada para <em>dois</em>
     projéteis que não interagem, lançados ao mesmo tempo com ângulos
     diferentes. Quantas equações são? O que muda no passo de Euler? Depois
     repita para \(N\) projéteis.''',
     r'''<p><b>Dois projéteis.</b> O estado é</p>
     <p>\[ \vet{u} = \left(x_1,y_1,v_{x1},v_{y1},
        x_2,y_2,v_{x2},v_{y2}\right), \]</p>
     <p>com oito componentes, e a derivada é a mesma receita repetida duas
     vezes:</p>
     <p><code>return np.array([vx1, vy1, -k*v1*vx1, -g-k*v1*vy1,<br>
     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
     vx2, vy2, -k*v2*vx2, -g-k*v2*vy2])</code></p>
     <p><b>O que muda no passo de Euler:</b> nada. A linha
     <code>u + dt*derivada(u, k)</code> continua idêntica, porque ela opera
     sobre o vetor inteiro e não sabe quantas componentes ele tem.</p>
     <p><b>Para \(N\) projéteis</b> são \(4N\) equações, e o código mais limpo
     guarda o estado como um arranjo de forma \((N,4)\), ou como quatro
     arranjos de tamanho \(N\). O método segue o mesmo.</p>
     <p><b>Por que isso importa.</b> É essa indiferença ao tamanho que torna o
     método utilizável no resto do curso e fora dele. Com \(N\) partículas que
     <em>interagem</em>, a única mudança está na função derivada, que passa a
     somar as forças de todos sobre todos; o integrador não muda. Simulações de
     dinâmica molecular com milhões de partículas e simulações de galáxias com
     bilhões usam exatamente essa estrutura, com integradores melhores que
     Euler, mas com a mesma arquitetura.</p>''' ),
]
