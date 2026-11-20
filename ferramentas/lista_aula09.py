# -*- coding: utf-8 -*-
"""Exercícios propostos do módulo 9."""

LISTA = [
    ('9.1  O poço duplo no plano de fase',
     r'''O oscilador de Duffing \(\ddot{x} + \gamma\dot{x} - x + x^3 = 0\) é o
     poço duplo do módulo 4 com atrito. Escreva-o como um sistema de primeira
     ordem, encontre os três pontos fixos e classifique cada um pela
     jacobiana, para \(\gamma = 0\) e para \(\gamma = 0{,}5\).''',
     r'''<p><b>O sistema.</b> Com \(y = \dot{x}\):</p>
     <p>\[ \dot{x} = y, \qquad \dot{y} = x - x^3 - \gamma y. \]</p>
     <p><b>Os pontos fixos.</b> \(y = 0\) e \(x - x^3 = x(1-x^2) = 0\), de onde
     \(x = 0\) e \(x = \pm1\). São o máximo da barreira e os dois mínimos do
     poço duplo, exatamente como no módulo 4.</p>
     <p><b>A jacobiana.</b></p>
     <p>\[ J = \begin{pmatrix} 0 & 1 \\ 1-3x^2 & -\gamma\end{pmatrix},
        \qquad
        \lambda^2 + \gamma\lambda - \left(1-3x_0^2\right) = 0. \]</p>
     <p><b>Na origem</b>, \(1-3x_0^2 = 1\) e
     \(\lambda = \left(-\gamma \pm \sqrt{\gamma^2+4}\right)/2\). A raiz é maior
     que \(\gamma\), de modo que os dois autovalores são reais e de sinais
     opostos: <b>sela</b>, com ou sem atrito. O máximo da barreira é instável
     por geometria.</p>
     <p><b>Nos mínimos</b>, \(1-3x_0^2 = -2\) e
     \(\lambda = \left(-\gamma \pm \sqrt{\gamma^2-8}\right)/2\):</p>
     <ul>
     <li>\(\gamma = 0\): \(\lambda = \pm i\sqrt2\), imaginários puros,
     <b>centros</b>. O corpo orbita o fundo para sempre, com frequência
     \(\sqrt2\), que é a mesma \(\sqrt{U''}\) do módulo 4 (ali \(U'' = 8\)
     porque a escala do potencial era outra; a estrutura é a mesma).</li>
     <li>\(\gamma = 0{,}5\): \(\gamma^2 - 8 &lt; 0\), de modo que
     \(\lambda = -0{,}25 \pm 1{,}39i\), <b>focos estáveis</b>.</li>
     </ul>
     <p><b>O desenho que resulta.</b> Duas espirais convergentes, separadas por
     uma sela, e a fronteira entre as duas bacias é a variedade estável da
     sela. É o mesmo arranjo do pêndulo amortecido, com dois poços em vez de
     infinitos, e é por isso que os dois retratos se parecem tanto.</p>
     <p><b>Um aviso de notação.</b> O sinal de \(-x\) é essencial. Com
     \(+x\) em vez de \(-x\) o potencial seria um poço único endurecido, a
     origem seria um centro e não haveria sela nenhuma. Duffing endurecido e
     Duffing com poço duplo são dois sistemas diferentes com o mesmo
     nome.</p>''' ),

    ('9.2  A separatriz em forma fechada',
     r'''Obtenha a equação da separatriz do pêndulo no plano \((\theta,\omega)\)
     a partir da conservação da energia, e mostre que, sobre ela, o pêndulo se
     aproxima do alto exponencialmente, com taxa igual ao autovalor instável da
     sela.''',
     r'''<p><b>A curva.</b> A energia por unidade de \(mL^2\) é</p>
     <p>\[ e = \frac{\omega^2}{2} + \frac{g}{L}\left(1-\cos\theta\right), \]</p>
     <p>e a separatriz é a curva de energia igual à do alto,
     \(e = 2g/L\). Igualando e usando
     \(1+\cos\theta = 2\cos^2(\theta/2)\):</p>
     <p>\[ \omega^2 = \frac{2g}{L}\left(1+\cos\theta\right)
        \quad\Longrightarrow\quad
        \omega = \pm 2\sqrt{\frac{g}{L}}\,\cos\frac{\theta}{2}. \]</p>
     <p>São dois arcos de cosseno que se encontram nas selas, em
     \(\theta = \pm\pi\), onde \(\omega = 0\). É a curva vinho do
     componente.</p>
     <p><b>A aproximação do alto.</b> Chame \(\varphi = \pi-\theta\) a distância
     angular até o alto. Para \(\varphi\) pequeno,
     \(\cos(\theta/2) = \sen(\varphi/2) \simeq \varphi/2\), de modo que</p>
     <p>\[ \dot\varphi = -\omega \simeq -\sqrt{\frac{g}{L}}\;\varphi
        \quad\Longrightarrow\quad
        \varphi(t) \propto e^{-\sqrt{g/L}\;t}. \]</p>
     <p>O pêndulo se aproxima do alto exponencialmente e <b>nunca chega</b>:
     tempo infinito, que é o mesmo resultado que o módulo 6 obteve pela
     divergência do período.</p>
     <p><b>A conexão que interessa.</b> A taxa \(\sqrt{g/L}\) é exatamente o
     autovalor da sela, \(\lambda = \pm\sqrt{g/L}\) para \(\gamma=0\). Não é
     coincidência: a separatriz <em>é</em> a variedade estável da sela, e a
     linearização em torno dela descreve justamente a aproximação final. O
     cálculo global e o local dão o mesmo número, porque descrevem a mesma
     curva em regiões diferentes.</p>
     <p><b>Com atrito.</b> A energia deixa de se conservar e essa curva deixa
     de ser trajetória. A variedade estável da sela continua existindo, agora
     como fronteira entre bacias, mas já não tem forma fechada: é preciso
     integrar para trás no tempo a partir da sela, que é o que o componente
     faz.</p>''' ),

    ('9.3  Por que trajetórias não se cruzam, e o que isso proíbe',
     r'''Explique por que duas trajetórias distintas nunca se cruzam no plano
     de fase. Use isso para mostrar que uma trajetória fechada tem de encerrar
     pelo menos um ponto fixo, e conclua que um sistema de duas equações sem
     ponto fixo nenhum não pode ter oscilação.''',
     r'''<p><b>Por que não se cruzam.</b> O campo
     \((\dot{x},\dot{y}) = (f,g)\) associa a cada ponto do plano
     <em>uma</em> velocidade. Se duas trajetórias passassem pelo mesmo ponto,
     o estado ali teria duas continuações futuras diferentes, e portanto duas
     velocidades. O teorema de existência e unicidade para equações
     diferenciais proíbe isso, desde que \(f\) e \(g\) sejam suaves.</p>
     <p><b>Um cuidado.</b> Essa regra vale no plano de fase, e não no gráfico de
     \(x(t)\), onde curvas se cruzam o tempo todo. Dois movimentos podem passar
     pela mesma <em>posição</em> em instantes diferentes; o que não podem é
     passar pelo mesmo <em>estado</em>, posição e velocidade juntas.</p>
     <p><b>A consequência topológica.</b> Suponha uma trajetória fechada
     \(C\). Ela divide o plano em dentro e fora, e nenhuma trajetória pode
     atravessá-la, pela regra acima. Então o interior de \(C\) é uma região
     invariante: quem começa dentro fica dentro para sempre. Um resultado de
     ponto fixo (o de Brouwer, na versão que se aplica a campos de vetores)
     garante que um campo contínuo numa região fechada e limitada, que não
     aponta para fora pela borda, tem de se anular em algum ponto dela.</p>
     <p>Logo <b>toda órbita fechada encerra ao menos um ponto fixo</b>.</p>
     <p><b>A conclusão útil.</b> Um sistema de duas equações autônomas sem
     ponto fixo algum não pode ter nenhuma oscilação, periódica ou de
     ciclo-limite. Antes de procurar um ciclo, procure os pontos fixos: se não
     houver nenhum, não há o que procurar.</p>
     <p><b>E a recíproca, que é mais forte.</b> O teorema de
     Poincaré-Bendixson diz que, numa região limitada do <em>plano</em> em que
     a trajetória fique presa e não haja ponto fixo, ela tem de convergir para
     uma órbita fechada. É esse teorema que garante a existência do
     ciclo-limite de van der Pol, e é também ele que explica por que o caos
     precisa de pelo menos três dimensões: no plano não há espaço para a
     trajetória se embolar sem se cruzar. Esse é o argumento que abre o
     módulo 10.</p>''' ),

    ('9.4  Classificar sem calcular autovalor nenhum',
     r'''Mostre que o traço e o determinante da jacobiana bastam para
     classificar um ponto fixo em duas dimensões, e construa o mapa dos casos
     no plano \((\operatorname{tr}J, \det J)\). Aplique ao pêndulo com atrito
     nos dois pontos fixos.''',
     r'''<p><b>A ideia.</b> Para uma matriz \(2\times2\), a equação
     característica é</p>
     <p>\[ \lambda^2 - \tau\lambda + \Delta = 0,
        \qquad \tau = \operatorname{tr}J, \quad \Delta = \det J, \]</p>
     <p>de onde \(\lambda_{\pm} = \left(\tau \pm
     \sqrt{\tau^2-4\Delta}\right)/2\). Tudo o que importa está em \(\tau\) e
     \(\Delta\), e não é preciso resolver nada.</p>
     <p><b>O mapa.</b></p>
     <div class="tabela-rolavel">
     <table>
     <thead><tr><th>região</th><th>tipo</th></tr></thead>
     <tbody>
     <tr><td>\(\Delta &lt; 0\)</td><td>sela (sempre, qualquer \(\tau\))</td></tr>
     <tr><td>\(\Delta &gt; 0\), \(\tau^2 &gt; 4\Delta\), \(\tau &lt; 0\)</td>
     <td>nó estável</td></tr>
     <tr><td>\(\Delta &gt; 0\), \(\tau^2 &gt; 4\Delta\), \(\tau &gt; 0\)</td>
     <td>nó instável</td></tr>
     <tr><td>\(\Delta &gt; 0\), \(\tau^2 &lt; 4\Delta\), \(\tau &lt; 0\)</td>
     <td>foco estável</td></tr>
     <tr><td>\(\Delta &gt; 0\), \(\tau^2 &lt; 4\Delta\), \(\tau &gt; 0\)</td>
     <td>foco instável</td></tr>
     <tr><td>\(\Delta &gt; 0\), \(\tau = 0\)</td><td>centro</td></tr>
     </tbody>
     </table>
     </div>
     <p>A parábola \(\tau^2 = 4\Delta\) separa nós de focos, e o eixo
     \(\Delta = 0\) separa selas de tudo o mais. Note a leitura direta:
     \(\Delta = \lambda_+\lambda_-\), de modo que \(\Delta &lt; 0\) obriga
     sinais opostos; e \(\tau = \lambda_++\lambda_-\) decide a estabilidade
     quando os dois têm o mesmo sinal.</p>
     <p><b>No pêndulo com atrito.</b> Com
     \(J = \begin{pmatrix}0 & 1\\ -\cos\theta_0 & -2\gamma\end{pmatrix}\),
     sai \(\tau = -2\gamma\) e \(\Delta = \cos\theta_0\), sempre.</p>
     <ul>
     <li><b>Fundo</b>, \(\cos\theta_0 = +1\): \(\Delta = 1 &gt; 0\). Com
     \(\gamma = 0\), \(\tau = 0\): centro. Com \(0&lt;\gamma&lt;1\),
     \(\tau^2 = 4\gamma^2 &lt; 4\): foco estável. Com \(\gamma &gt; 1\): nó
     estável, que é o superamortecido do módulo 7.</li>
     <li><b>Alto</b>, \(\cos\theta_0 = -1\): \(\Delta = -1 &lt; 0\) sempre.
     Sela, para qualquer atrito, sem nenhuma conta.</li>
     </ul>
     <p><b>Por que vale a pena.</b> Em sistemas com muitos parâmetros, procurar
     onde \(\Delta\) ou \(\tau\) mudam de sinal localiza as
     <b>bifurcações</b>, que são os valores em que o retrato de fase muda de
     tipo. O módulo 10 é feito disso.</p>''' ),

    ('9.5  A amplitude 2 do ciclo-limite, por energia',
     r'''Para \(\mu\) pequeno, a órbita de van der Pol é quase
     \(x = A\cos t\). Use o balanço de energia ao longo de um ciclo para
     mostrar que \(A = 2\), e explique por que esse número não depende de
     \(\mu\).''',
     r'''<p><b>A energia.</b> Defina \(E = \left(x^2+\dot{x}^2\right)/2\), que é
     a energia do oscilador harmônico de fundo. Derivando e usando a
     equação:</p>
     <p>\[ \der{E}{t} = x\dot{x} + \dot{x}\ddot{x}
        = \dot{x}\left(x + \ddot{x}\right)
        = \mu\left(1-x^2\right)\dot{x}^2. \]</p>
     <p>O sinal confirma a leitura: a energia cresce enquanto \(|x| &lt; 1\) e
     diminui quando \(|x| &gt; 1\).</p>
     <p><b>A condição de ciclo.</b> Numa órbita fechada, a energia volta ao
     valor inicial depois de uma volta:</p>
     <p>\[ \Delta E = \mu\oint\left(1-x^2\right)\dot{x}^2\,dt = 0. \]</p>
     <p><b>A conta.</b> Com \(x = A\cos t\) e \(\dot{x} = -A\sen t\), ao longo
     de um período \(2\pi\):</p>
     <p>\[ \oint \dot{x}^2dt = A^2\pi, \qquad
        \oint x^2\dot{x}^2dt = A^4\oint\cos^2t\,\sen^2t\,dt
        = \frac{A^4\pi}{4}, \]</p>
     <p>usando \(\med{\sen^2} = 1/2\) e
     \(\med{\cos^2\sen^2} = 1/8\). Então</p>
     <p>\[ A^2\pi - \frac{A^4\pi}{4} = 0
        \quad\Longrightarrow\quad A^2\left(1-\frac{A^2}{4}\right) = 0
        \quad\Longrightarrow\quad A = 2. \]</p>
     <p><b>Por que \(\mu\) sumiu.</b> Porque ele multiplica a equação inteira:
     a condição é que a integral se anule, e um fator global não muda onde uma
     coisa se anula. O \(\mu\) controla a <em>rapidez</em> com que o ciclo é
     atingido, e não <em>onde</em> ele está. A outra raiz, \(A = 0\), é a
     origem, que é ponto fixo instável.</p>
     <p><b>O alcance e o limite do argumento.</b> Ele supôs que a órbita é
     senoidal, o que só vale para \(\mu\) pequeno. O programa mede 2,000001
     com \(\mu = 0{,}01\) e 2,0225 com \(\mu = 4\): a previsão se degrada
     devagar, e a forma da órbita se degrada muito mais depressa que a
     amplitude. Esse é o primeiro exemplo no curso de um
     <b>método perturbativo</b>: supor a resposta, impor uma condição de
     consistência e extrair um número.</p>''' ),

    ('9.6  Onde a classificação não se aplica',
     r'''O oscilador com atrito seco do módulo 7 obedece a
     \(\ddot{x} = -\omega_0^2x - \mu g\,\mathrm{sinal}(\dot{x})\). Encontre o
     conjunto dos pontos fixos e mostre que a técnica da jacobiana não se
     aplica a ele. Diga o que se perde e o que ainda se pode afirmar.''',
     r'''<p><b>Os pontos fixos.</b> Precisa-se de \(\dot{x} = 0\) e
     \(\ddot{x} = 0\). Com \(\dot{x} = 0\) a força de atrito não tem sinal
     definido: ela é estática, e pode assumir qualquer valor até
     \(\mu_e m g\). O bloco fica parado sempre que a mola não vencer o atrito
     estático, isto é, sempre que</p>
     <p>\[ \left|x\right| \le \frac{\mu m g}{k} = \frac{\mu g}{\omega_0^2}. \]</p>
     <p>Os pontos fixos não formam um ponto: formam um <b>segmento</b> inteiro
     sobre o eixo \(\dot{x} = 0\), a zona morta do módulo 7. Com os números de
     lá (\(\mu = 0{,}05\), \(m = 0{,}5\) kg, \(k = 20\) N/m), o segmento tem
     \(\pm1{,}23\) cm.</p>
     <p><b>Por que a jacobiana não serve.</b> Por dois motivos
     independentes:</p>
     <ul>
     <li>O campo <b>não é diferenciável</b> em \(\dot{x} = 0\): a função sinal
     salta. Não existe matriz de derivadas ali, e o método parte de uma
     expansão em série que não existe.</li>
     <li>Os pontos fixos <b>não são isolados</b>. A classificação pressupõe um
     ponto fixo isolado, com uma vizinhança em que ele é o único. Aqui todo
     ponto do segmento tem outros pontos fixos arbitrariamente perto.</li>
     </ul>
     <p><b>O que se perde.</b> As categorias do módulo (sela, nó, foco, centro)
     simplesmente não se aplicam, e perguntas como "o ponto fixo é estável?"
     precisam ser reformuladas: estável no sentido de que o bloco fica onde
     parou, sim; no sentido de que ele volta ao equilíbrio da mola, não, porque
     ele para fora dele.</p>
     <p><b>O que ainda se pode afirmar.</b> Quase tudo, com as ferramentas
     deste módulo aplicadas <em>por partes</em>. Em cada semiciclo o sinal de
     \(\dot{x}\) é fixo, e ali o sistema é um oscilador harmônico comum, com
     centro deslocado para \(\mp\mu g/\omega_0^2\). O retrato de fase é feito
     de semicírculos alternados, centrados em dois pontos diferentes, que se
     emendam no eixo \(\dot{x} = 0\): uma espiral feita de arcos de
     circunferência, e não de exponenciais. Daí sai, geometricamente, a queda
     <em>aritmética</em> da amplitude que o módulo 7 mediu.</p>
     <p><b>A moral.</b> O retrato de fase continua sendo o instrumento certo; o
     que falha é a linearização, que é apenas uma das técnicas para
     construí-lo. Convém não confundir a ferramenta com o método.</p>''' ),
]
