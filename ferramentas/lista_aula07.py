# -*- coding: utf-8 -*-
"""Exercícios propostos do módulo 7."""

LISTA = [
    ('7.1  Identificar o regime e escrever a solução',
     r'''Um bloco de 250 g preso a uma mola de 16 N/m move-se num meio que
     exerce \(-b\dot{x}\) com \(b = 2{,}0\) N·s/m. Diga em que regime está,
     escreva \(x(t)\) para o bloco solto do repouso a 5,0 cm, e calcule o
     período, o fator de qualidade e o tamanho do primeiro repique.''',
     r'''<p><b>Os dois parâmetros.</b></p>
     <p>\[ \omega_0 = \sqrt{\frac{k}{m}} = \sqrt{\frac{16}{0{,}25}}
        = 8{,}00\ \mathrm{rad/s}, \qquad
        \gamma = \frac{b}{2m} = \frac{2{,}0}{0{,}50}
        = 4{,}00\ \mathrm{rad/s}. \]</p>
     <p>Como \(\gamma &lt; \omega_0\), o regime é <b>subamortecido</b>, com
     \(\gamma/\omega_0 = 0{,}5\). O amortecimento é forte: o sistema oscila,
     mas pouco.</p>
     <p><b>A frequência e o período.</b></p>
     <p>\[ \omega_1 = \sqrt{\omega_0^2-\gamma^2} = \sqrt{64-16}
        = 6{,}928\ \mathrm{rad/s}, \qquad T_1 = 0{,}9069\ \mathrm{s}, \]</p>
     <p>contra \(T_0 = 0{,}7854\) s do oscilador sem amortecimento: 15 % mais
     devagar.</p>
     <p><b>A solução.</b> Com \(x_0 = 0{,}050\) m e \(v_0 = 0\), a forma
     compacta é \(x = Ce^{-\gamma t}\cos(\omega_1 t - \varphi)\) com</p>
     <p>\[ C = x_0\frac{\omega_0}{\omega_1} = 0{,}05774\ \mathrm{m},
        \qquad \varphi = \arctg\frac{\gamma}{\omega_1} = 30{,}0^\circ. \]</p>
     <p>\[ x(t) = 0{,}05774\,e^{-4t}\cos\left(6{,}928\,t - 0{,}5236\right)
        \ \mathrm{m}. \]</p>
     <p>Note que \(C &gt; x_0\): a amplitude da senoide de dentro é maior que
     o deslocamento inicial, porque em \(t=0\) a exponencial ainda vale 1 e o
     cosseno não está no máximo. O corpo nunca chega a 5,77 cm.</p>
     <p><b>Qualidade e repique.</b> \(Q = \omega_0/2\gamma = 1{,}00\), o que já
     avisa que quase não haverá oscilação visível. De fato, o primeiro repique
     acontece em \(t = \pi/\omega_1 = 0{,}453\) s, em
     \(x = -0{,}94\) cm: menos de um quinto do deslocamento inicial. De um
     pico ao seguinte a amplitude é dividida por
     \(e^{\gamma T_1} = 37{,}6\).</p>''' ),

    ('7.2  Medir o amortecimento com uma régua',
     r'''Um registro de oscilação mostra picos sucessivos de 12,00 cm,
     10,33 cm, 8,89 cm e 7,65 cm, espaçados de 2,00 s. A massa é 500 g.
     Obtenha o decremento logarítmico, \(\gamma\), \(Q\), a constante \(b\), o
     tempo para a amplitude cair a \(1/e\) e a fração de energia perdida por
     ciclo. Depois diga quanto \(\omega_0\) difere de \(\omega_1\).''',
     r'''<p><b>O decremento.</b> A razão entre picos vizinhos é constante, o
     que já confirma que o amortecimento é viscoso:</p>
     <p>\[ \frac{12{,}00}{10{,}33} = \frac{10{,}33}{8{,}89}
        = \frac{8{,}89}{7{,}65} = 1{,}162
        \quad\Longrightarrow\quad \delta = \ln 1{,}162 = 0{,}150. \]</p>
     <p><b>As grandezas derivadas.</b></p>
     <p>\[ \gamma = \frac{\delta}{T_1} = \frac{0{,}150}{2{,}00}
        = 0{,}0750\ \mathrm{s^{-1}}, \qquad
        Q = \frac{\pi}{\delta} = 20{,}9, \]</p>
     <p>\[ b = 2m\gamma = 0{,}0750\ \mathrm{N\,s/m}, \qquad
        \tau = \frac{1}{\gamma} = 13{,}3\ \mathrm{s} = 6{,}7\ \text{ciclos}. \]</p>
     <p>A regra de bolso confere: a amplitude cai a \(1/e\) em \(Q/\pi\)
     ciclos, e \(20{,}9/\pi = 6{,}7\).</p>
     <p><b>A energia.</b> Ela cai com o quadrado da amplitude, de modo que por
     ciclo resta \(e^{-2\delta}\):</p>
     <p>\[ \frac{|\Delta E|}{E} = 1 - e^{-2\times0{,}150} = 25{,}9\ \%. \]</p>
     <p>Cuidado com o atalho: \(2\pi/Q = 30{,}0\) %, que erra em 16 % por
     linearizar a exponencial. É a mesma discrepância da seção 3, aqui com
     \(Q\) pequeno o bastante para ela doer.</p>
     <p><b>\(\omega_0\) contra \(\omega_1\).</b></p>
     <p>\[ \omega_1 = \frac{2\pi}{2{,}00} = 3{,}1416\ \mathrm{rad/s}, \qquad
        \omega_0 = \sqrt{\omega_1^2+\gamma^2} = 3{,}14249\ \mathrm{rad/s}. \]</p>
     <p>Diferem em \(9\times10^{-4}\) rad/s, ou 0,03 %. Com \(Q = 21\), medir
     \(\omega_1\) e chamar de \(\omega_0\) é inofensivo, e o exercício 7.1
     mostra o caso oposto. A correção é de segunda ordem em
     \(\gamma/\omega_0\), e por isso some tão depressa.</p>''' ),

    ('7.3  De onde vem o t solto do caso crítico',
     r'''No amortecimento crítico a equação característica tem raiz dupla
     \(r = -\gamma\), e \(e^{-\gamma t}\) é apenas <em>uma</em> solução.
     Mostre que \((A+Bt)e^{-\gamma t}\) resolve a equação, e explique de duas
     maneiras por que a segunda solução tem de ser essa: tomando o limite do
     caso subamortecido e por redução de ordem.''',
     r'''<p><b>Verificação direta.</b> Com \(x = te^{-\gamma t}\):</p>
     <p>\[ \dot{x} = (1-\gamma t)e^{-\gamma t}, \qquad
        \ddot{x} = (\gamma^2 t - 2\gamma)e^{-\gamma t}. \]</p>
     <p>Substituindo em \(\ddot{x} + 2\gamma\dot{x} + \gamma^2 x\), já que
     \(\omega_0 = \gamma\) no caso crítico:</p>
     <p>\[ \left[(\gamma^2t - 2\gamma) + 2\gamma(1-\gamma t)
        + \gamma^2 t\right]e^{-\gamma t}
        = \left[\gamma^2t - 2\gamma + 2\gamma - 2\gamma^2t
        + \gamma^2t\right]e^{-\gamma t} = 0. \]</p>
     <p>Resolve mesmo, e nada no cálculo explica <em>por quê</em>.</p>
     <p><b>Pelo limite.</b> No caso subamortecido,</p>
     <p>\[ x = e^{-\gamma t}\left(A\cos\omega_1 t
        + B\sen\omega_1 t\right). \]</p>
     <p>Faça \(\omega_1 \to 0\) mantendo \(B\omega_1 = \beta\) fixo. O
     cosseno tende a 1 e \(B\sen\omega_1 t = \beta\,
     \frac{\sen\omega_1t}{\omega_1} \to \beta t\). O \(t\) aparece como o
     limite de um seno cuja frequência vai a zero mas cuja amplitude cresce na
     mesma proporção: a oscilação que sobrou é o primeiro quarto dela,
     esticado até virar reta. A mesma coisa acontece no superamortecido,
     vindo do outro lado com senos hiperbólicos.</p>
     <p><b>Por redução de ordem.</b> Sabendo uma solução \(x_1\), procure a
     segunda na forma \(x = u(t)x_1\). Substituindo na equação, os termos em
     \(u\) cancelam (porque \(x_1\) já é solução) e sobra, para a raiz dupla,
     \(\ddot{u} = 0\), cuja solução geral é \(u = A + Bt\). O \(t\) não é
     truque de livro: é o que resta quando a equação para \(u\) degenera.</p>
     <p><b>O que isso significa fisicamente.</b> O termo \(Bt\) permite que o
     sistema crítico ainda <em>ultrapasse</em> o equilíbrio uma vez, se for
     lançado em direção a ele com velocidade suficiente. Solto do repouso, ele
     não ultrapassa nunca: a condição \(v_0 = 0\) faz \(B = \gamma x_0\), que
     tem o sinal errado para produzir cruzamento. Vale conferir isso no
     programa antes de acreditar.</p>''' ),

    ('7.4  Projetar o amortecedor de um instrumento',
     r'''O ponteiro de um instrumento tem \(\omega_0 = 20\) rad/s e precisa se
     acomodar dentro de 1 % da leitura final o mais rápido possível. Encontre
     o amortecimento ótimo, compare com o crítico e explique por que a
     resposta muda se a exigência passar para 0,01 %.''',
     r'''<p><b>A regra.</b> O ótimo é onde o primeiro repique tem exatamente o
     tamanho da tolerância:</p>
     <p>\[ \exp\!\left(\frac{-\pi z}{\sqrt{1-z^2}}\right) = \text{tol},
        \qquad
        \Lambda = \frac{-\ln(\text{tol})}{\pi},
        \qquad z = \sqrt{\frac{\Lambda^2}{1+\Lambda^2}}. \]</p>
     <p><b>Para 1 %.</b> \(\Lambda = 4{,}605/\pi = 1{,}466\), de onde
     \(z = 0{,}826\) e \(\gamma = 16{,}5\) rad/s. O programa mede o ótimo em
     0,83, e o crítico demora <b>57 % a mais</b> para a mesma tolerância.</p>
     <p><b>Para 0,01 %.</b> \(\Lambda = 2{,}932\), \(z = 0{,}946\),
     \(\gamma = 18{,}9\) rad/s, e a vantagem sobre o crítico cai para 36 %. A
     exigência mais apertada empurra o projeto para perto do crítico, porque
     o repique permitido encolheu.</p>
     <p><b>Por que a resposta depende da tolerância.</b> Porque o tempo de
     acomodação não é uma função suave de \(z\): ele dá <em>saltos</em>.
     Enquanto o primeiro repique couber na faixa, o relógio para ali; quando
     ele não cabe, é preciso esperar o repique seguinte, um semiciclo inteiro
     depois. O ótimo fica exatamente no limiar entre as duas situações, e por
     isso é definido pela tolerância e não pelo sistema.</p>
     <p><b>A moral.</b> "Amortecimento crítico" não é um objetivo de projeto, é
     um ponto matemático. O objetivo é o tempo de acomodação, e ele depende do
     que se aceita como "acomodado". Instrumentos analógicos e servomecanismos
     são de fato projetados em \(z\) entre 0,6 e 0,8, e não em 1,0, por esse
     motivo.</p>''' ),

    ('7.5  Atrito seco: a amplitude cai em linha reta',
     r'''Um bloco de 500 g preso a uma mola de 20 N/m desliza sobre uma mesa
     com \(\mu_c = 0{,}05\), e é solto de 15 cm. Mostre que a amplitude cai de
     \(2\mu mg/k\) a cada <em>meio</em> ciclo, que o período não muda, e
     encontre onde e quando o bloco para.''',
     r'''<p><b>A equação.</b> A força de atrito tem módulo constante e muda de
     sinal com a velocidade:</p>
     <p>\[ m\ddot{x} = -kx - \mu m g\,\mathrm{sinal}(\dot{x}). \]</p>
     <p>Em cada semiciclo o sinal é fixo, de modo que o movimento é um
     oscilador harmônico comum <em>deslocado</em>: o centro de oscilação sai
     de zero para \(\mp\mu mg/k\). Daí duas consequências imediatas.</p>
     <p><b>O período não muda.</b> Deslocar o centro não altera a equação
     homogênea, e portanto \(\omega = \omega_0 = \sqrt{k/m} = 6{,}325\) rad/s
     em todos os semiciclos. É a diferença mais visível em relação ao arrasto
     viscoso, que atrasa a oscilação. A simulação dá meio período de
     0,49673 s em todos eles, contra \(\pi/\omega_0 = 0{,}49673\) s.</p>
     <p><b>A amplitude cai em progressão aritmética.</b> Em cada semiciclo o
     corpo descreve meia volta em torno do centro deslocado, de modo que a
     amplitude medida a partir do zero verdadeiro perde duas vezes o
     deslocamento do centro:</p>
     <p>\[ \Delta A = \frac{2\mu mg}{k}
        = \frac{2\times0{,}05\times0{,}5\times9{,}81}{20}
        = 2{,}45\ \mathrm{cm}. \]</p>
     <p>Os picos previstos são 15,00, 12,55, 10,10, 7,64, 5,19, 2,74 e
     0,29 cm, e a simulação reproduz exatamente esses valores. Compare com o
     caso viscoso, em que eles cairiam em progressão <em>geométrica</em>: é
     uma assinatura experimental que distingue os dois tipos de perda sem
     precisar de instrumento nenhum.</p>
     <p><b>Onde para.</b> Existe uma zona morta: se o corpo chega ao repouso
     com \(|x| \le \mu mg/k = 1{,}23\) cm, a mola não vence o atrito estático e
     ele fica. A simulação para em \(x = +0{,}29\) cm depois de
     <b>2,98 s</b> e seis reversões, isto é, o bloco morre fora do
     equilíbrio.</p>
     <p><b>Por que isso importa.</b> O oscilador viscoso leva tempo infinito
     para parar e para no lugar certo; o de atrito seco para em tempo finito e
     no lugar errado. Um instrumento de ponteiro com atrito seco no eixo tem
     erro de leitura irredutível do tamanho da zona morta, e nenhuma
     calibração o corrige: por isso instrumentos bons usam amortecimento
     viscoso ou eletromagnético, e não atrito mecânico.</p>''' ),

    ('7.6  A suspensão de um carro, com números',
     r'''Um quarto de automóvel tem 400 kg sobre a roda, e a suspensão é
     projetada para frequência natural de 1,0 Hz. Encontre \(k\), a flecha
     estática e a constante \(b\) para \(z = 0{,}7\). Depois explique o
     resultado desconcertante da medição: para uma tolerância de 2 %, o
     projeto em \(z = 0{,}7\) acomoda em 0,95 s e o crítico em 0,93 s, mas
     \(z = 0{,}78\) acomoda em 0,57 s.''',
     r'''<p><b>Os números do projeto.</b> Com \(f_0 = 1{,}0\) Hz,
     \(\omega_0 = 6{,}283\) rad/s:</p>
     <p>\[ k = m\omega_0^2 = 400\times39{,}48
        = 15{,}8\ \mathrm{kN/m}, \qquad
        b = 2zm\omega_0 = 3519\ \mathrm{N\,s/m}. \]</p>
     <p>A flecha estática é um jeito rápido de conferir:</p>
     <p>\[ \delta_{\text{est}} = \frac{mg}{k} = \frac{g}{\omega_0^2}
        = 24{,}8\ \mathrm{cm}, \]</p>
     <p>que não depende da massa e é da ordem do curso real de uma suspensão.
     Repare que escolher a frequência natural <em>é</em> escolher a flecha:
     \(f_0 = \frac{1}{2\pi}\sqrt{g/\delta_{\text{est}}}\). Carros de passeio
     ficam em torno de 1 Hz, e carros de corrida, com flecha de 3 cm, em
     torno de 3 Hz, o que explica o desconforto.</p>
     <p><b>O resultado desconcertante.</b> Ele é consequência do salto
     discutido no exercício 7.4. O primeiro repique vale</p>
     <p>\[ \exp\!\left(\frac{-\pi z}{\sqrt{1-z^2}}\right)
        = \begin{cases}
        4{,}6\ \% & \text{para } z = 0{,}70,\\
        2{,}0\ \% & \text{para } z = 0{,}78.
        \end{cases} \]</p>
     <p>Com \(z = 0{,}70\), o repique de 4,6 % <b>estoura</b> a faixa de 2 %,
     de modo que o cronômetro só para no repique seguinte, meio período
     depois: daí os 0,95 s. Com \(z = 0{,}78\), o repique cabe raspando, e o
     relógio para já na primeira passagem: 0,57 s. O crítico, sem repique
     nenhum, chega aos 2 % por decaimento puro, em 0,93 s.</p>
     <p><b>A leitura correta.</b> O tempo de acomodação não é função suave do
     amortecimento, e perto do limiar um ajuste de 10 % em \(b\) pode cortar o
     tempo pela metade ou dobrá-lo. É por isso que suspensão se ajusta em
     bancada e não em planilha.</p>
     <p><b>Uma honestidade final.</b> O modelo de um grau de liberdade ignora
     a massa da roda e a rigidez do pneu, que formam um segundo oscilador em
     torno de 10 Hz. A suspensão real é projetada para amortecer os dois, e o
     compromisso entre conforto (a massa de cima) e aderência (a roda) é o que
     torna o problema interessante. O módulo 8 dá a ferramenta que falta aqui:
     a resposta a uma excitação contínua, que é o que a estrada é.</p>''' ),
]
