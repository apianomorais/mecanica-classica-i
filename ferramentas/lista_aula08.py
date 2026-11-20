# -*- coding: utf-8 -*-
"""Exercícios propostos do módulo 8."""

LISTA = [
    ('8.1  Um oscilador forçado, com números',
     r'''Uma massa de 500 g numa mola de 50 N/m sofre arrasto com
     \(b = 0{,}50\) N·s/m e é forçada por \(F_0 = 2{,}0\) N. Calcule
     \(\omega_0\), \(\gamma\) e \(Q\); a amplitude em frequência muito baixa,
     em \(\omega_0\) e no pico; e a potência média absorvida na
     ressonância.''',
     r'''<p><b>Os parâmetros.</b></p>
     <p>\[ \omega_0 = \sqrt{\frac{50}{0{,}5}} = 10{,}0\ \mathrm{rad/s},
        \qquad \gamma = \frac{b}{2m} = 0{,}50\ \mathrm{rad/s},
        \qquad Q = \frac{\omega_0}{2\gamma} = 10{,}0. \]</p>
     <p><b>As três amplitudes.</b> Em frequência muito baixa a mola sozinha
     responde, e a amplitude é a deformação estática:</p>
     <p>\[ A(0) = \frac{F_0}{m\omega_0^2} = \frac{F_0}{k}
        = 4{,}00\ \mathrm{cm}. \]</p>
     <p>Em \(\omega = \omega_0\) o primeiro termo do denominador se anula e
     sobra só o amortecimento:</p>
     <p>\[ A(\omega_0) = \frac{F_0}{2m\gamma\omega_0} = 40{,}0\ \mathrm{cm}
        = Q\,A(0). \]</p>
     <p>Essa igualdade é geral e merece ser guardada: <b>em \(\omega_0\) a
     amplitude é \(Q\) vezes a estática</b>. É a leitura física de \(Q\) que
     mais serve na prática, e ela diz por que um \(Q\) alto é perigoso quando
     não é desejado.</p>
     <p>No pico verdadeiro, \(\omega_A = \sqrt{100-0{,}5} = 9{,}975\) rad/s, a
     amplitude é 40,05 cm: apenas <b>0,125 %</b> maior que em \(\omega_0\).
     Com \(Q = 10\) a distinção entre as duas ressonâncias já é invisível em
     laboratório, e é por isso que ela some dos livros. Ela volta a importar
     quando \(Q\) é da ordem de 1.</p>
     <p><b>A potência.</b> Na ressonância,</p>
     <p>\[ \med{P} = \frac{F_0^2}{4m\gamma} = \frac{4{,}0}{4\times0{,}5\times0{,}5}
        = 4{,}0\ \mathrm{W}. \]</p>
     <p>Repare no que isso significa: a potência absorvida em regime
     permanente é exatamente a potência <em>dissipada</em> pelo arrasto, porque
     a energia média do oscilador não muda. A força externa não está
     acumulando energia no sistema; está pagando a conta do atrito.</p>''' ),

    ('8.2  Onde cada coisa tem pico',
     r'''Mostre que a amplitude do deslocamento tem máximo em
     \(\omega_A = \sqrt{\omega_0^2-2\gamma^2}\), que a amplitude da velocidade
     tem máximo exatamente em \(\omega_0\), e que o mesmo vale para a potência
     média. Diga o que acontece quando \(\gamma &gt; \omega_0/\sqrt2\).''',
     r'''<p><b>O deslocamento.</b> Maximizar \(A\) é minimizar o radicando</p>
     <p>\[ D(\omega) = \left(\omega_0^2-\omega^2\right)^2
        + 4\gamma^2\omega^2. \]</p>
     <p>Derivando em relação a \(\omega^2\), que é mais limpo que em
     \(\omega\):</p>
     <p>\[ \der{D}{(\omega^2)} = -2\left(\omega_0^2-\omega^2\right)
        + 4\gamma^2 = 0
        \quad\Longrightarrow\quad
        \omega_A^2 = \omega_0^2 - 2\gamma^2. \]</p>
     <p><b>A velocidade.</b> A amplitude da velocidade é \(\omega A\), de modo
     que maximizá-la é minimizar \(D/\omega^2\):</p>
     <p>\[ \frac{D}{\omega^2}
        = \left(\frac{\omega_0^2}{\omega}-\omega\right)^2 + 4\gamma^2. \]</p>
     <p>O segundo termo é constante, e o primeiro é um quadrado que
     <em>se anula</em> quando \(\omega = \omega_0\). Não é preciso derivar
     nada: um quadrado atinge o mínimo possível quando pode ser zerado. O
     amortecimento não entra, e é por isso que esse pico não se move.</p>
     <p><b>A potência.</b> \(\med{P} = m\gamma(\omega A)^2\) é uma função
     crescente de \(\omega A\), de modo que ela tem máximo exatamente onde a
     velocidade tem: em \(\omega_0\). Faz sentido físico, e o sentido está na
     fase: em \(\omega_0\) a fase vale \(\pi/2\), o que põe a velocidade
     <em>em fase</em> com a força, e \(\med{F v}\) é máxima quando os dois
     andam juntos.</p>
     <p><b>Quando o pico some.</b> Se \(\gamma &gt; \omega_0/\sqrt2\), então
     \(\omega_A^2 &lt; 0\) e não há solução real: a curva de amplitude passa a
     decrescer monotonicamente desde \(\omega = 0\). Note que isso acontece
     <em>antes</em> do amortecimento crítico, em
     \(\gamma = \omega_0/\sqrt2 \simeq 0{,}707\,\omega_0\). Existe, portanto,
     uma faixa de amortecimento em que o sistema ainda oscila livremente mas
     já não tem ressonância de amplitude.</p>''' ),

    ('8.3  A largura vale 2γ, e não aproximadamente',
     r'''Encontre as frequências de meia potência resolvendo
     \(\med{P}(\omega) = \med{P}_{\max}/2\) e mostre que a largura é
     exatamente \(2\gamma\), sem aproximação. Verifique com os números do
     exercício 8.1.''',
     r'''<p><b>A condição.</b> Com
     \(\med{P} \propto \omega^2A^2 = \omega^2(F_0/m)^2/D(\omega)\) e
     \(\med{P}_{\max} = (F_0/m)^2/4\gamma^2\) em \(\omega_0\), a condição de
     meia potência é</p>
     <p>\[ \frac{\omega^2}{\left(\omega_0^2-\omega^2\right)^2+4\gamma^2\omega^2}
        = \frac{1}{8\gamma^2}
        \quad\Longrightarrow\quad
        \left(\omega_0^2-\omega^2\right)^2 = 4\gamma^2\omega^2. \]</p>
     <p>Tirando a raiz dos dois lados, com os dois sinais:</p>
     <p>\[ \omega_0^2-\omega^2 = \pm 2\gamma\omega
        \quad\Longrightarrow\quad
        \omega^2 \pm 2\gamma\omega - \omega_0^2 = 0. \]</p>
     <p><b>As raízes.</b> Ficando apenas com as positivas,</p>
     <p>\[ \omega_{\pm} = \sqrt{\omega_0^2+\gamma^2} \pm \gamma, \]</p>
     <p>e a diferença é</p>
     <p>\[ \Delta\omega = \omega_+-\omega_- = 2\gamma, \]</p>
     <p>porque a raiz, que é a parte complicada, é a <em>mesma</em> nas duas e
     se cancela na subtração. O resultado é exato: não houve nenhuma
     aproximação de \(Q\) alto em lugar nenhum.</p>
     <p><b>Com os números de 8.1.</b> \(\sqrt{100+0{,}25} = 10{,}0125\), de
     onde \(\omega_- = 9{,}5125\) e \(\omega_+ = 10{,}5125\) rad/s, com
     largura 1,0000 rad/s \(= 2\gamma\). E
     \(Q = \omega_0/\Delta\omega = 10{,}0\), o mesmo valor obtido de
     \(\omega_0/2\gamma\).</p>
     <p><b>Por que importa.</b> Note que o <em>centro</em> da faixa,
     \(\sqrt{\omega_0^2+\gamma^2}\), não é \(\omega_0\) nem o pico da
     amplitude: é uma terceira frequência. O que é exato é a largura, e é por
     isso que a medida de laboratório usa a largura e não o centro.</p>''' ),

    ('8.4  O que a fase tem a dizer sobre a energia',
     r'''Mostre que a potência média absorvida vale
     \(\med{P} = \frac12 F_0 \omega A \sen\varphi\) e use isso para explicar,
     sem derivar nada, por que a transferência de energia é máxima em
     \(\omega_0\) e nula nos dois extremos de frequência.''',
     r'''<p><b>A conta.</b> Com \(F = F_0\cos\omega t\) e
     \(\dot{x} = -\omega A\sen(\omega t-\varphi)\),</p>
     <p>\[ \med{P} = \med{F\dot{x}}
        = -F_0\omega A\med{\cos\omega t\,\sen(\omega t-\varphi)}. \]</p>
     <p>Abrindo o seno da diferença e usando
     \(\med{\cos^2} = \frac12\), \(\med{\sen\cos} = 0\):</p>
     <p>\[ \med{\cos\omega t\,\sen(\omega t-\varphi)}
        = -\frac{\sen\varphi}{2}
        \quad\Longrightarrow\quad
        \med{P} = \frac{F_0\,\omega A\,\sen\varphi}{2}. \]</p>
     <p><b>A leitura.</b> Só a <em>componente da velocidade em fase com a
     força</em> transporta energia em média, e \(\sen\varphi\) é exatamente a
     fração dela. Daí os três regimes saem sem conta nenhuma:</p>
     <ul>
     <li>\(\omega \ll \omega_0\): \(\varphi \to 0\), o deslocamento acompanha a
     força, a velocidade fica 90° adiantada em relação a ela, e
     \(\med{Fv} \to 0\). A força faz trabalho positivo meio ciclo e negativo no
     outro: empurra e devolve, como numa mola ideal.</li>
     <li>\(\omega = \omega_0\): \(\varphi = \pi/2\) exatamente, a velocidade
     fica <em>em fase</em> com a força, e \(\sen\varphi = 1\). Todo empurrão é
     a favor do movimento, o tempo todo. É o que uma criança faz num balanço,
     e o que ela faz é ajustar a fase, não a amplitude.</li>
     <li>\(\omega \gg \omega_0\): \(\varphi \to \pi\), e \(\sen\varphi \to 0\)
     de novo. A inércia domina e a massa mal se move.</li>
     </ul>
     <p><b>Uma consequência de projeto.</b> Em regime permanente, a potência
     absorvida é igual à dissipada, de modo que a conta acima <em>também</em>
     dá o calor gerado. É assim que se calcula o aquecimento de um material
     submetido a um campo oscilante, e é por isso que o forno de micro-ondas
     opera perto de uma ressonância das moléculas de água e não em qualquer
     frequência.</p>''' ),

    ('8.5  A função de Green e o degrau',
     r'''Verifique que \(G(t) = e^{-\gamma t}\sen(\omega_1t)/\omega_1\) para
     \(t\ge0\) é a resposta a um impulso unitário, isto é, que satisfaz a
     equação homogênea com \(G(0)=0\) e \(\dot G(0)=1\). Use a convolução para
     obter a resposta a uma força que liga de repente e permanece,
     \(f(t) = f_0\) para \(t\ge0\), no caso sem amortecimento, e interprete o
     resultado.''',
     r'''<p><b>Por que essas condições iniciais.</b> Integre a equação de
     \(-\epsilon\) a \(+\epsilon\) em torno do impulso. O termo
     \(\ddot{x}\) dá o salto de \(\dot{x}\), os termos em \(\dot{x}\) e \(x\)
     dão contribuição nula no limite por serem finitos, e o impulso unitário dá
     1. Logo a velocidade salta de 0 para 1 e a posição não salta. Um impulso é
     uma martelada: muda o momento, não a posição.</p>
     <p>Com \(G = e^{-\gamma t}\sen(\omega_1t)/\omega_1\) tem-se
     \(G(0)=0\) e</p>
     <p>\[ \dot G = e^{-\gamma t}\left[\cos\omega_1 t
        - \frac{\gamma}{\omega_1}\sen\omega_1 t\right]
        \quad\Longrightarrow\quad \dot G(0) = 1. \]</p>
     <p>E a função é solução da homogênea, porque é exatamente a forma
     subamortecida do módulo 7. As três exigências são atendidas.</p>
     <p><b>O degrau, sem amortecimento.</b> Com \(\gamma = 0\),
     \(\omega_1 = \omega_0\) e \(f(s) = f_0\) para \(s \ge 0\):</p>
     <p>\[ x(t) = \int_0^t \frac{\sen\omega_0(t-s)}{\omega_0}f_0\,ds
        = \frac{f_0}{\omega_0^2}\left(1-\cos\omega_0 t\right). \]</p>
     <p><b>A interpretação.</b> Chamando \(x_{\text{est}} = f_0/\omega_0^2 =
     F_0/k\) a deformação estática, o resultado é</p>
     <p>\[ x(t) = x_{\text{est}}\left(1-\cos\omega_0 t\right), \]</p>
     <p>que oscila entre 0 e <b>duas vezes</b> a deformação estática. Aplicar
     uma carga de repente deforma a estrutura o dobro do que a mesma carga
     deformaria se fosse depositada devagar.</p>
     <p>Esse fator 2 é a versão mais limpa da armadilha da seção 3, e é o
     mesmo que aparece no transiente perto da ressonância. Com amortecimento, a
     oscilação decai e sobra \(x_{\text{est}}\), mas o <em>pico</em> continua
     próximo do dobro se \(Q\) for alto. Engenharia estrutural chama isso de
     fator de amplificação dinâmica, e projeta com ele.</p>''' ),

    ('8.6  Tacoma: ressonância ou outra coisa?',
     r'''A queda da ponte de Tacoma Narrows, em 1940, ilustra o capítulo de
     ressonância de quase todo livro de física básica. Explique por que a
     atribuição é incorreta, e mostre, modelando o efeito do vento como um
     amortecimento <em>negativo</em>, que o crescimento resultante é
     qualitativamente diferente do de uma ressonância.''',
     r'''<p><b>O que falta para ser ressonância.</b> Ressonância exige uma
     força externa <em>periódica</em>, com frequência própria, perto de uma
     frequência natural da estrutura. No dia do colapso o vento soprava de modo
     aproximadamente constante, a cerca de 68 km/h. Não havia frequência
     externa alguma para coincidir com coisa nenhuma.</p>
     <p>A explicação aceita é <em>flutter</em> aeroelástico: o próprio
     movimento de torção do tabuleiro altera o ângulo com que o ar o encontra,
     e o ar devolve uma força que reforça o movimento. A força não é imposta de
     fora com uma frequência sua; ela é <b>criada pelo movimento</b>, e herda a
     frequência dele.</p>
     <p><b>O modelo.</b> Isso se escreve trocando o sinal do termo de
     arrasto:</p>
     <p>\[ \ddot{x} - 2\left|\gamma\right|\dot{x} + \omega_0^2 x = 0
        \quad\Longrightarrow\quad
        x = Ce^{+|\gamma|t}\cos(\omega_1 t - \varphi). \]</p>
     <p>A mesma equação do módulo 7, com \(\gamma &lt; 0\). A amplitude cresce
     <b>exponencialmente</b>, dobrando a cada \(\ln 2/|\gamma|\), sem precisar
     de força externa nenhuma e sem limite superior enquanto o modelo linear
     valer.</p>
     <p><b>A diferença que importa.</b></p>
     <div class="tabela-rolavel">
     <table>
     <thead><tr><th></th><th>ressonância</th><th>flutter</th></tr></thead>
     <tbody>
     <tr><td>origem da frequência</td><td>externa, da força</td>
     <td>interna, da estrutura</td></tr>
     <tr><td>crescimento</td><td>satura em \(F_0/2m\gamma\omega_0\)</td>
     <td>exponencial, sem saturação linear</td></tr>
     <tr><td>efeito de amortecer mais</td><td>reduz o pico</td>
     <td>pode estabilizar completamente</td></tr>
     <tr><td>depende da velocidade do vento</td><td>não</td>
     <td>sim: há uma velocidade crítica</td></tr>
     </tbody>
     </table>
     </div>
     <p>A última linha é a assinatura prática: flutter tem velocidade crítica,
     abaixo da qual simplesmente não acontece. Pontes modernas são testadas em
     túnel de vento exatamente para localizá-la, e o tabuleiro recebe forma
     aerodinâmica e aberturas para empurrá-la para longe.</p>
     <p><b>A fonte.</b> A correção foi publicada por K. Y. Billah e
     R. H. Scanlan em
     <a href="https://doi.org/10.1119/1.16590"><em>Resonance, Tacoma Narrows
     bridge failure, and undergraduate physics textbooks</em></a>, Am. J. Phys.
     <b>59</b>, 118 (1991), e vale a leitura: o artigo rastreia como o erro
     entrou nos livros e por que se perpetuou. É um bom estudo de caso de uma
     coisa que acontece com frequência na física de ensino, que é uma imagem
     boa demais para ser abandonada.</p>''' ),
]
