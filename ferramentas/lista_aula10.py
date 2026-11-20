# -*- coding: utf-8 -*-
"""Exercícios propostos do módulo 10."""

LISTA = [
    ('10.1  Os pontos fixos, e por que r = 3',
     r'''Encontre os pontos fixos do mapa logístico, mostre que
     \(f'(x^*) = 2-r\) no ponto fixo não trivial e obtenha o intervalo de
     \(r\) em que ele é estável. Explique por que a instabilidade aparece com
     \(f' = -1\) e não com \(f' = +1\).''',
     r'''<p><b>Os pontos fixos.</b> \(x^* = rx^*(1-x^*)\) dá
     \(x^*\left[1-r(1-x^*)\right] = 0\), de onde</p>
     <p>\[ x^* = 0 \qquad\text{e}\qquad x^* = 1-\frac{1}{r}. \]</p>
     <p>O segundo só está em \([0,1]\) se \(r \ge 1\): abaixo disso a
     população se extingue, e o ponto fixo não trivial é negativo, isto é,
     não descreve nada.</p>
     <p><b>A derivada.</b> \(f'(x) = r(1-2x)\), de modo que</p>
     <p>\[ f'(x^*) = r\left[1-2\left(1-\frac1r\right)\right]
        = r\left(\frac2r - 1\right) = 2-r. \]</p>
     <p>Note que a conta não depende de \(x^*\) explicitamente: a inclinação
     no ponto fixo é função só de \(r\). Isso é particularidade da
     parábola.</p>
     <p><b>O intervalo.</b> \(\left|2-r\right| &lt; 1\) dá
     \(1 &lt; r &lt; 3\). Em \(r = 1\) a derivada vale \(+1\) e em \(r = 3\)
     vale \(-1\), que são os dois jeitos de perder estabilidade.</p>
     <p><b>Os dois jeitos, e por que são diferentes.</b> Escreva
     \(x_n = x^* + \delta_n\). Linearizando, \(\delta_{n+1} = f'\delta_n\),
     de modo que \(\delta_n = (f')^n\delta_0\):</p>
     <ul>
     <li>\(f' \to +1\): a perturbação cresce <em>sem trocar de sinal</em>. O
     ponto fixo colide com outro ponto fixo e os dois trocam de
     estabilidade. É o que acontece em \(r = 1\), onde \(x^*=0\) e
     \(x^*=1-1/r\) se cruzam, e chama-se bifurcação transcrítica.</li>
     <li>\(f' \to -1\): a perturbação cresce <em>alternando de sinal</em>, e
     a órbita passa a pular de um lado para o outro do ponto fixo. Essa
     alternância é um ciclo de período 2 nascendo, e é por isso que esta é a
     bifurcação de duplicação de período. Um mapa só duplica período por
     \(-1\), nunca por \(+1\).</li>
     </ul>''' ),

    ('10.2  O ciclo de período 2 e o valor 1 + √6',
     r'''Resolve \(f(f(x)) = x\), elimine os pontos fixos do mapa simples e
     obtenha os dois pontos do ciclo de período 2. Mostre que a estabilidade
     do ciclo é governada por \(-r^2+2r+4\) e deduza que ele perde
     estabilidade em \(r = 1+\sqrt6\).''',
     r'''<p><b>Os pontos do ciclo.</b> Qualquer ponto fixo de \(f\) também é
     ponto fixo de \(f\circ f\), de modo que \(x\) e \(x-(1-1/r)\) dividem o
     polinômio \(f(f(x))-x\). Feita a divisão, sobra</p>
     <p>\[ r^2x^2 - r(r+1)x + (r+1) = 0
        \quad\Longrightarrow\quad
        x_{\pm} = \frac{r+1 \pm \sqrt{(r-3)(r+1)}}{2r}. \]</p>
     <p>O discriminante é negativo para \(r &lt; 3\): o ciclo de período 2
     <b>não existe</b> abaixo de 3, e nasce exatamente onde o ponto fixo perde
     estabilidade. Em \(r = 3\) as duas raízes coincidem em \(x = 2/3\), que é
     o próprio ponto fixo.</p>
     <p><b>A estabilidade.</b> Pela regra da cadeia,</p>
     <p>\[ \left(f\circ f\right)'(x_\pm) = f'(x_+)\,f'(x_-)
        = r^2\left(1-2x_+\right)\left(1-2x_-\right), \]</p>
     <p>e repare que o produto é o <em>mesmo</em> nos dois pontos: um ciclo é
     estável ou instável por inteiro, nunca pela metade. Usando
     \(x_++x_- = (r+1)/r\) e \(x_+x_- = (r+1)/r^2\):</p>
     <p>\[ \left(1-2x_+\right)\left(1-2x_-\right)
        = 1 - \frac{2(r+1)}{r} + \frac{4(r+1)}{r^2}, \]</p>
     <p>\[ \left(f\circ f\right)' = r^2 - 2r(r+1) + 4(r+1)
        = -r^2+2r+4. \]</p>
     <p><b>Os dois extremos.</b> Em \(r = 3\) isso vale \(+1\), confirmando o
     nascimento marginal. A perda de estabilidade acontece quando passa por
     \(-1\):</p>
     <p>\[ -r^2+2r+4 = -1 \quad\Longrightarrow\quad r^2-2r-5 = 0
        \quad\Longrightarrow\quad r = 1+\sqrt6 = 3{,}449490. \]</p>
     <p>O programa confirma por iteração: em \(r = 3{,}4494\) o período é 2 e
     em \(r = 3{,}4496\) já é 4.</p>
     <p><b>O que vem depois.</b> O mesmo cálculo para o ciclo de período 4
     exigiria um polinômio de grau 16, e a partir daí não há forma fechada.
     Essa é a razão prática de a cascata inteira ser estudada numericamente, e
     de os dois primeiros valores (3 e \(1+\sqrt6\)) serem os únicos que
     aparecem com raiz quadrada nos livros.</p>''' ),

    ('10.3  O primeiro parâmetro superestável, à mão',
     r'''O programa usa os parâmetros em que \(x = 1/2\) pertence ao ciclo.
     Mostre que, para o ciclo de período 2, esse parâmetro é
     \(R_1 = 1+\sqrt5\), e explique por que esses parâmetros são melhores que
     os pontos de bifurcação para medir a constante de Feigenbaum.''',
     r'''<p><b>A condição.</b> Se \(x=1/2\) está num ciclo de período 2, então
     \(f(f(1/2)) = 1/2\). Com \(f(1/2) = r/4\):</p>
     <p>\[ r\cdot\frac{r}{4}\left(1-\frac{r}{4}\right) = \frac12
        \quad\Longrightarrow\quad
        r^2\left(4-r\right) = 8
        \quad\Longrightarrow\quad
        r^3 - 4r^2 + 8 = 0. \]</p>
     <p><b>A fatoração.</b> \(r = 2\) é raiz, por inspeção
     (\(8-16+8=0\)), e corresponde ao caso de período 1, em que \(x=1/2\) é o
     próprio ponto fixo. Dividindo:</p>
     <p>\[ r^3-4r^2+8 = (r-2)\left(r^2-2r-4\right), \]</p>
     <p>e a raiz positiva do fator quadrático é</p>
     <p>\[ R_1 = 1+\sqrt5 = 3{,}2360679775, \]</p>
     <p>exatamente o valor que a bissecção encontra. (A outra raiz,
     \(1-\sqrt5\), é negativa e não interessa.)</p>
     <p><b>Por que superestável.</b> Como \(f'(1/2) = 0\), a derivada do ciclo
     inteiro, que é o produto das derivadas nos seus pontos, também se anula.
     Perturbações morrem mais rápido que exponencialmente: a convergência é
     quadrática. Daí o nome.</p>
     <p><b>Por que servem melhor.</b> Três motivos práticos:</p>
     <ul>
     <li>Nos pontos de <em>bifurcação</em> a derivada do ciclo vale
     \(\pm1\), de modo que a convergência é lentíssima e a medida numérica
     fica imprecisa. Nos superestáveis ela é a mais rápida possível.</li>
     <li>Os \(R_n\) são raízes <em>simples</em> de
     \(f^{2^n}(1/2) = 1/2\), uma equação bem posta, achável por bissecção com
     todas as casas. Os pontos de bifurcação são raízes de uma condição de
     tangência, numericamente pior.</li>
     <li>Os \(R_n\) ficam no meio de cada janela, e a razão
     \(\left(R_{n-1}-R_{n-2}\right)/\left(R_n-R_{n-1}\right)\) converge para a
     <em>mesma</em> \(\delta\), porque a constante descreve a geometria da
     cascata, e não um ponto particular dela.</li>
     </ul>
     <p>Essa escolha é um exemplo de uma coisa que vale além deste módulo:
     quando uma medida numérica fica ruim, às vezes a solução não é melhorar o
     método e sim medir outra coisa, que dê a mesma resposta.</p>''' ),

    ('10.4  λ = ln 2 em r = 4, sem medir',
     r'''Mostre que a substituição \(x_n = \sen^2\left(\pi\theta_n\right)\)
     transforma o mapa logístico com \(r = 4\) no mapa de dobramento
     \(\theta_{n+1} = 2\theta_n \bmod 1\). Conclua que \(\lambda = \ln 2\) e
     explique por que o expoente não muda numa mudança de variável.''',
     r'''<p><b>A conjugação.</b> Com \(x = \sen^2(\pi\theta)\) e \(r = 4\):</p>
     <p>\[ x_{n+1} = 4\sen^2(\pi\theta_n)\left[1-\sen^2(\pi\theta_n)\right]
        = 4\sen^2(\pi\theta_n)\cos^2(\pi\theta_n), \]</p>
     <p>e usando \(2\sen\alpha\cos\alpha = \sen2\alpha\),</p>
     <p>\[ x_{n+1} = \sen^2\left(2\pi\theta_n\right)
        = \sen^2\left[\pi\left(2\theta_n\right)\right]. \]</p>
     <p>Isto é, \(\theta_{n+1} = 2\theta_n\), módulo 1 porque
     \(\sen^2(\pi\theta)\) tem período 1 em \(\theta\).</p>
     <p><b>O expoente do mapa de dobramento.</b> Ali a derivada é 2 em todo
     ponto, de modo que a média de \(\ln|f'|\) é trivialmente \(\ln 2\). Duas
     condições iniciais vizinhas têm a distância <em>exatamente</em> dobrada a
     cada passo, até que a operação módulo as separe de vez.</p>
     <p><b>Por que vale para o logístico.</b> O expoente de Lyapunov é
     invariante sob mudanças de variável suaves e invertíveis. Se
     \(x = h(\theta)\), a distância entre órbitas vizinhas em \(x\) é
     \(\left|h'\right|\) vezes a distância em \(\theta\), e esse fator
     aparece uma vez no começo e uma vez no fim do cálculo da média: na média
     de \(\ln\), ele contribui com
     \(\left[\ln|h'(\theta_N)| - \ln|h'(\theta_0)|\right]/N\), que vai a zero.
     O esticamento acumulado é o mesmo; só a régua mudou.</p>
     <p>\[ \lambda_{\text{logístico}}(r=4) = \ln 2 = 0{,}693147\ldots \]</p>
     <p>contra 0,693153 medido com duzentas mil iterações.</p>
     <p><b>Um bônus.</b> A conjugação também explica <em>por que</em> o mapa
     é caótico em \(r=4\): no dobramento, escrever \(\theta\) em binário
     mostra que iterar é apenas deslocar a vírgula uma casa para a direita. O
     futuro da órbita é lido nos dígitos que já estavam lá, cada vez mais
     à direita. Uma incerteza na décima casa binária vira incerteza de ordem
     1 depois de dez iterações, e é isso o caos: não criação de informação, e
     sim revelação de informação que estava em dígitos que ninguém mediu.</p>''' ),

    ('10.5  Quanto tempo a previsão dura, com números',
     r'''Um sistema tem \(\lambda = 0{,}50\) por iteração e um atrator de
     largura 1. Começando com incerteza \(10^{-6}\), quantas iterações a
     previsão dura? E se a incerteza cair para \(10^{-12}\)? Quanto custaria
     dobrar o horizonte de previsão?''',
     r'''<p><b>A conta.</b> A previsão acaba quando
     \(d_0e^{\lambda n} \simeq L\), com \(L\) a largura do atrator:</p>
     <p>\[ n_{\max} = \frac{1}{\lambda}\ln\frac{L}{d_0}. \]</p>
     <p><b>Os dois casos.</b></p>
     <p>\[ n_{\max} = \frac{\ln 10^{6}}{0{,}5} = 27{,}6
        \qquad\text{e}\qquad
        n_{\max} = \frac{\ln 10^{12}}{0{,}5} = 55{,}3. \]</p>
     <p>Um milhão de vezes mais precisão <b>dobrou</b> o horizonte. É esse o
     recado: o horizonte cresce com o <em>logaritmo</em> da precisão.</p>
     <p><b>Dobrar de novo.</b> De 55 para 110 iterações exigiria
     \(d_0 = 10^{-24}\), o que está abaixo da precisão dupla de máquina
     (\(10^{-16}\)) e, em qualquer medida física, abaixo do comprimento de
     Planck comparado a um metro. Em sistemas caóticos, o horizonte de
     previsão é praticamente um teto.</p>
     <p><b>Em números do mundo.</b> Para a atmosfera, estimativas dão
     \(\lambda \sim 1/(1{,}5\ \text{dia})\). Com incerteza inicial de
     \(10^{-3}\) do tamanho típico das estruturas,
     \(n_{\max} \simeq 1{,}5\ln(10^3) = 10\) dias. Melhorar a rede de medidas
     em mil vezes, que é um esforço gigantesco, levaria isso para 20 dias, e
     não para dez mil. É por isso que a previsão do tempo melhorou muito em
     <em>qualidade</em> nos últimos quarenta anos e quase nada em
     <em>alcance</em>.</p>
     <p><b>O que não decorre disso.</b> Que previsão nenhuma é possível. O
     <em>clima</em> (a estatística do atrator: média, variância, frequência de
     extremos) é perfeitamente previsível, e não depende de saber onde a
     órbita está. Confundir a imprevisibilidade da trajetória com
     imprevisibilidade da estatística é o erro mais comum que se comete com a
     palavra caos fora da física.</p>''' ),

    ('10.6  A mesma cascata, agora num pêndulo',
     r'''O pêndulo amortecido e forçado,
     \(\ddot\theta + 2\gamma\dot\theta + \sen\theta = A\cos\omega t\), tem as
     três dimensões necessárias. Explique quais são, descreva como amostrá-lo
     para obter um mapa, e proponha o procedimento numérico para encontrar
     nele a cascata de duplicação e medir \(\delta\).''',
     r'''<p><b>As três dimensões.</b> O estado instantâneo precisa de
     \(\theta\) e \(\dot\theta\), e a equação <em>não</em> é autônoma, porque
     \(t\) aparece do lado direito. O remédio padrão é promover a fase da
     força a variável:</p>
     <p>\[ \dot\theta = \omega_\theta, \qquad
        \dot\omega_\theta = -2\gamma\omega_\theta - \sen\theta + A\cos\phi,
        \qquad \dot\phi = \omega. \]</p>
     <p>Três equações, autônomas, e portanto espaço de fase tridimensional
     (com \(\phi\) periódico, isto é, um cilindro). O pêndulo <em>livre</em>
     tem só duas, e é por isso que ele nunca é caótico, por maior que seja a
     amplitude.</p>
     <p><b>Como virar mapa.</b> Registre \((\theta,\dot\theta)\) uma vez por
     período da força, sempre na mesma fase: em
     \(t_n = 2\pi n/\omega\). O fluxo contínuo em três dimensões vira um mapa
     bidimensional, e tudo o que este módulo discute passa a valer. (É a
     mesma construção que, no caso <em>conservativo</em>, produz as seções de
     Poincaré da unidade final de Mecânica Clássica III; aqui o sistema é
     dissipativo e o resultado é um atrator, não um toro.)</p>
     <p><b>O procedimento.</b></p>
     <ul>
     <li>Fixe \(\gamma\) e \(\omega\), e use \(A\) como parâmetro de
     controle, no papel do \(r\).</li>
     <li>Para cada \(A\), integre por Runge-Kutta, descarte alguns milhares de
     períodos de transiente e registre \(\theta\) amostrado uma vez por
     período, por mais algumas centenas.</li>
     <li>Desenhe esses valores contra \(A\): é o diagrama de bifurcação, com a
     mesma leitura (um ponto, dois pontos, nuvem).</li>
     <li>Localize os \(A_n\) em que o período dobra e meça
     \(\left(A_{n-1}-A_{n-2}\right)/\left(A_n-A_{n-1}\right)\).</li>
     </ul>
     <p><b>O que se espera encontrar.</b> A razão converge para os mesmos
     \(4{,}6692\). Esse é o ponto do exercício: a constante de Feigenbaum não
     é uma propriedade de parábolas, e sim de como sistemas dissipativos
     perdem estabilidade. Um pêndulo de metal e um mapa de uma linha pertencem
     à mesma classe de universalidade, e isso é verificável numa tarde.</p>
     <p><b>Dois cuidados numéricos.</b> O transiente aqui é muito mais longo
     que no mapa, e cortá-lo curto demais produz um diagrama borrado que
     parece caos sem ser. E a amostragem tem de ser na <em>mesma</em> fase da
     força sempre: usar o passo do integrador, que não divide o período
     exatamente, introduz um batimento lento que também parece
     estrutura.</p>''' ),
]
