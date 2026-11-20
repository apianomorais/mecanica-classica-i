# -*- coding: utf-8 -*-
"""Exercícios propostos do módulo 6."""

LISTA = [
    ('6.1  Das condições iniciais à amplitude e à fase',
     r'''Um bloco de 300 g preso a uma mola de 2,5 N/m é puxado 3,0 cm e solto
     com velocidade de 12 cm/s <em>para dentro</em> (isto é, em direção ao
     equilíbrio). Encontre \(\omega\), o período, a amplitude, a fase e a
     energia total. Depois diga em que instante ele passa pela primeira vez
     pela posição de equilíbrio.''',
     r'''<p><b>A frequência.</b></p>
     <p>\[ \omega = \sqrt{\frac{k}{m}} = \sqrt{\frac{2{,}5}{0{,}300}}
        = 2{,}887\ \mathrm{rad/s}, \qquad
        T = \frac{2\pi}{\omega} = 2{,}177\ \mathrm{s}. \]</p>
     <p>Repare que a frequência não depende de nada do que foi feito com o
     bloco: ela estava decidida antes de alguém tocar nele.</p>
     <p><b>A amplitude.</b> Com \(x_0 = +0{,}030\) m e
     \(v_0 = -0{,}12\) m/s (negativo, porque aponta para o equilíbrio):</p>
     <p>\[ C = \sqrt{x_0^2 + \left(\frac{v_0}{\omega}\right)^2}
        = \sqrt{0{,}030^2 + 0{,}04157^2} = 5{,}13\ \mathrm{cm}. \]</p>
     <p>A amplitude é maior que a distância em que ele foi solto, e tem de ser:
     ele foi solto <em>com</em> velocidade, e não do repouso. Se tivesse sido
     solto parado, a amplitude seria os 3,0 cm.</p>
     <p><b>A fase.</b></p>
     <p>\[ \tg\varphi = \frac{v_0}{\omega x_0} = \frac{-0{,}12}{0{,}0866}
        = -1{,}386 \quad\Longrightarrow\quad \varphi = -54{,}2^\circ
        = -0{,}946\ \mathrm{rad}. \]</p>
     <p>O sinal negativo diz que o máximo já passou: a partícula está
     <em>depois</em> do pico, a caminho do equilíbrio, que é exatamente o que
     o enunciado descreve.</p>
     <p><b>A energia.</b></p>
     <p>\[ E = \frac12 kC^2 = \frac12 \times 2{,}5 \times (0{,}0513)^2
        = 3{,}29\ \mathrm{mJ}. \]</p>
     <p>Conferindo pelo outro caminho:
     \(\frac12 k x_0^2 + \frac12 m v_0^2
     = 1{,}125 + 2{,}16 = 3{,}29\) mJ. Os dois batem, como têm de bater.</p>
     <p><b>Quando cruza o equilíbrio.</b> \(x = 0\) quando
     \(\cos(\omega t - \varphi) = 0\), isto é,
     \(\omega t - \varphi = \pi/2\) (o primeiro valor positivo de \(t\)):</p>
     <p>\[ t = \frac{\pi/2 + \varphi}{\omega}
        = \frac{1{,}5708 - 0{,}946}{2{,}887} = 0{,}216\ \mathrm{s}. \]</p>
     <p>Menos de um décimo do período, o que faz sentido: ele já estava
     indo nessa direção.</p>''' ),

    ('6.2  As duas médias, feitas no papel',
     r'''Mostre, integrando diretamente ao longo de um período, que
     \(\med{T} = \med{U} = E/2\) para o oscilador harmônico. Depois verifique
     que o resultado <em>não</em> vale para o pêndulo em amplitude grande, e
     diga qual das duas médias fica maior nesse caso.''',
     r'''<p><b>As integrais.</b> Com \(x = C\cos(\omega t - \varphi)\),</p>
     <p>\[ \med{U} = \frac{1}{T}\int_0^T \frac{kC^2}{2}
        \cos^2(\omega t - \varphi)\,dt. \]</p>
     <p>Use \(\cos^2\alpha = \frac{1+\cos 2\alpha}{2}\). O termo com
     \(\cos 2\alpha\) integra a zero ao longo de um período inteiro, porque
     completa dois ciclos, e sobra</p>
     <p>\[ \med{U} = \frac{kC^2}{2}\cdot\frac12 = \frac{E}{2}. \]</p>
     <p>Para \(\med{T}\) o cálculo é idêntico, com
     \(\sen^2\alpha = \frac{1-\cos 2\alpha}{2}\), e dá o mesmo \(E/2\).
     Note que nem foi preciso saber a fase: ela só desloca o intervalo de
     integração de uma função periódica, o que não muda a média.</p>
     <p><b>Por que o resultado é especial.</b> O teorema do virial diz que,
     para \(U \propto x^n\), as médias se relacionam por
     \(2\med{T} = n\med{U}\). O caso \(n = 2\) é o único em que elas são
     iguais. Para a gravitação, \(n = -1\), e sai \(2\med{T} = -\med{U}\),
     que é a relação usada para pesar galáxias.</p>
     <p><b>No pêndulo de amplitude grande.</b> Agora
     \(U = mgL(1-\cos\theta)\), que cresce mais devagar que a parábola
     \(\frac12 mgL\theta^2\): o potencial é mais "largo" que o harmônico.
     A partícula passa mais tempo perto dos pontos de retorno, onde
     \(T = 0\) e \(U\) é máxima, e portanto <b>\(\med{U}\) fica maior que
     \(\med{T}\)</b>.</p>
     <p>Isso é o mesmo fato, visto de outro ângulo, que o aumento do período
     com a amplitude: o pêndulo demora porque a força restauradora
     \(\sen\theta\) é mais fraca que \(\theta\) nos extremos, e é essa fraqueza
     que também desequilibra as médias. Uma afirmação dessas não deve ser
     aceita de graça: adapte o programa para integrar as duas médias no
     pêndulo e confira o sinal da diferença em 90°.</p>''' ),

    ('6.3  Medir g com um pêndulo, e o erro que ninguém vê',
     r'''Um estudante mede \(T\) para um pêndulo de exatamente 1,000 m e usa
     \(g = 4\pi^2L/T^2\). Calcule o \(g\) que ele obtém se soltar o pêndulo de
     5°, de 10° e de 20°, usando os períodos exatos da tabela da seção 5.
     Proponha uma correção e verifique o que sobra de erro.''',
     r'''<p><b>Os três resultados.</b> Com \(g = 4\pi^2 L/T^2\):</p>
     <div class="tabela-rolavel">
     <table>
     <thead><tr><th>\(\theta_0\)</th><th>\(T\) exato (s)</th>
     <th>\(g\) obtido</th><th>erro</th></tr></thead>
     <tbody>
     <tr><td>5°</td><td>2,007365</td><td>9,7973</td><td>\(-0{,}10\) %</td></tr>
     <tr><td>10°</td><td>2,010236</td><td>9,7694</td><td>\(-0{,}38\) %</td></tr>
     <tr><td>20°</td><td>2,021796</td><td>9,6579</td><td>\(-1{,}52\) %</td></tr>
     </tbody>
     </table>
     </div>
     <p>O erro é sempre <b>para baixo</b>, e isso é importante: não é ruído,
     é viés. Repetir a medida mil vezes e tirar a média não melhora nada,
     porque o erro não é aleatório. Soltar de 20° e medir com um cronômetro de
     0,01 s dá um \(g\) com três casas de precisão aparente e uma casa de
     exatidão real.</p>
     <p><b>A correção.</b> Como \(T = T_0(1 + \theta_0^2/16 + \ldots)\), basta
     inverter:</p>
     <p>\[ g_{\text{corrigido}} = \frac{4\pi^2L}{T^2}
        \left(1 + \frac{\theta_0^2}{16}\right)^2. \]</p>
     <p>Aplicando aos três casos, sobra \(4\times10^{-7}\),
     \(7\times10^{-6}\) e \(1\times10^{-4}\) de erro relativo. Em 20°, uma
     correção de duas linhas transforma 1,5 % de erro em 0,01 %, que é melhor
     do que qualquer cronômetro de mão consegue medir.</p>
     <p><b>A lição experimental.</b> Nem todo erro aparece na repetição. O
     desvio padrão de um conjunto de medidas mede o acaso, e não mede o viés
     do modelo usado para interpretá-las. Quem confunde precisão com exatidão
     publica três casas erradas com grande confiança.</p>''' ),

    ('6.4  A boia que é um pêndulo disfarçado',
     r'''Um cilindro de seção \(A\) e densidade \(\rho_c\) flutua em água de
     densidade \(\rho\), com uma altura \(h\) submersa no equilíbrio. Mostre
     que, afundado um pouco e solto, ele oscila harmonicamente com
     \(\omega = \sqrt{g/h}\). Explique por que a resposta não depende de
     \(\rho_c\), de \(A\) nem da altura total do cilindro, e calcule o período
     para \(h = 12\) cm.''',
     r'''<p><b>O equilíbrio.</b> O empuxo sustenta o peso:</p>
     <p>\[ \rho g A h = m g \quad\Longrightarrow\quad m = \rho A h. \]</p>
     <p>Essa igualdade é a chave de tudo o que vem a seguir, e é bom guardá-la
     antes de prosseguir: a massa do cilindro é a massa do líquido que ele
     desloca.</p>
     <p><b>Deslocado de \(y\) para baixo.</b> O volume submerso aumenta de
     \(Ay\), e o empuxo extra é uma força restauradora:</p>
     <p>\[ F = -\rho g A y, \]</p>
     <p>que é a lei de Hooke com \(k = \rho g A\). Então</p>
     <p>\[ \omega = \sqrt{\frac{k}{m}} = \sqrt{\frac{\rho g A}{\rho A h}}
        = \sqrt{\frac{g}{h}}. \]</p>
     <p><b>Por que tudo cancela.</b> Porque a mesma quantidade \(\rho A\)
     aparece na rigidez e na inércia. Um cilindro mais largo tem mais empuxo
     por centímetro afundado, e exatamente na mesma proporção tem mais massa.
     Um cilindro mais denso afunda mais, e isso aumenta \(h\) na medida certa.
     Sobra apenas a altura submersa.</p>
     <p><b>O número.</b> Com \(h = 0{,}12\) m:</p>
     <p>\[ \omega = \sqrt{9{,}80665/0{,}12} = 9{,}04\ \mathrm{rad/s},
        \qquad T = 0{,}695\ \mathrm{s}. \]</p>
     <p>É o mesmo período de um pêndulo simples de 12 cm, e a coincidência não
     é coincidência: as duas contas chegam em \(\omega^2 = g/\ell\) porque as
     duas têm a gravidade como única fonte de rigidez, e nos dois casos a
     inércia é proporcional ao mesmo comprimento.</p>
     <p><b>A letra miúda.</b> Esse resultado ignora que a água em volta também
     precisa ser acelerada (a chamada massa adicionada) e que o movimento gera
     ondas que levam energia embora. Na prática a boia oscila um pouco mais
     devagar e amortece depressa, o que é assunto do módulo 7.</p>''' ),

    ('6.5  A molécula, e a massa que não é de nenhum átomo',
     r'''Dois átomos de massas \(m_1\) e \(m_2\) ligados por uma mola de
     constante \(k\) oscilam ao longo da linha que os une, com o centro de
     massa parado. Mostre que a separação \(s = x_2 - x_1 - s_0\) obedece à
     equação do oscilador harmônico com a massa reduzida
     \(\mu = m_1m_2/(m_1+m_2)\). Aplique ao monóxido de carbono, cujo espectro
     mostra absorção em 2143 cm⁻¹, para obter \(k\), e diga quanto se erraria
     usando a massa de um átomo só.''',
     r'''<p><b>As duas equações.</b> A mola puxa os dois átomos com forças
     opostas, proporcionais ao esticamento \(s\):</p>
     <p>\[ m_1\ddot{x}_1 = +ks, \qquad m_2\ddot{x}_2 = -ks. \]</p>
     <p>Divida cada uma pela respectiva massa e subtraia:</p>
     <p>\[ \ddot{x}_2 - \ddot{x}_1 = -ks\left(\frac{1}{m_2}+\frac{1}{m_1}\right)
        \quad\Longrightarrow\quad
        \ddot{s} = -\frac{k}{\mu}s, \qquad
        \frac{1}{\mu} = \frac{1}{m_1}+\frac{1}{m_2}. \]</p>
     <p>O problema de dois corpos virou o de um corpo só, de massa \(\mu\),
     preso a uma parede. É o mesmo truque que o módulo 12 usa para reduzir o
     problema de dois corpos gravitacional, e vale a pena reconhecê-lo aqui,
     onde é barato.</p>
     <p><b>A massa reduzida do CO.</b> Com \(m_1 = 12{,}000\) u e
     \(m_2 = 15{,}995\) u:</p>
     <p>\[ \mu = \frac{12{,}000\times15{,}995}{27{,}995}
        = 6{,}856\ \mathrm{u} = 1{,}1385\times10^{-26}\ \mathrm{kg}. \]</p>
     <p>Ela é menor que a menor das duas massas, sempre, e é essa a razão de
     chamá-la reduzida.</p>
     <p><b>A constante elástica.</b> O número de onda de 2143 cm⁻¹ é uma
     frequência disfarçada: \(\omega = 2\pi c\tilde\nu\), com \(c\) em cm/s,</p>
     <p>\[ \omega = 2\pi \times 2{,}998\times10^{10} \times 2143
        = 4{,}037\times10^{14}\ \mathrm{rad/s}, \]</p>
     <p>\[ k = \mu\omega^2 = 1{,}1385\times10^{-26}\times
        \left(4{,}037\times10^{14}\right)^2 = 1855\ \mathrm{N/m}. \]</p>
     <p>Para comparar: uma mola de academia tem algumas centenas de N/m, e
     esta ligação química é mais rígida que isso, numa escala de 0,1 nm.</p>
     <p><b>O erro de usar a massa errada.</b> Com 12 u no lugar de \(\mu\),
     sairia \(k = 3247\) N/m, <b>75 % maior</b>. O erro não está em nenhuma
     conta: está em supor que um dos átomos fica parado, quando os dois se
     movem. Como \(\mu\) é sempre menor que qualquer das massas, esse engano
     sempre superestima a rigidez.</p>
     <p><b>Um aviso.</b> Esses 1855 N/m valem para a aproximação harmônica. A
     curva de energia de uma ligação real é assimétrica (lembre do
     Lennard-Jones do módulo 4: a parede repulsiva é muito mais íngreme que a
     cauda atrativa), e a anarmonicidade empurra o valor tabelado para perto de
     1900 N/m. A diferença de 2 % é justamente o que a espectroscopia mede
     olhando o segundo harmônico.</p>''' ),

    ('6.6  Huygens, a cicloide e a correção de quarta ordem',
     r'''Obtenha a correção \(T \simeq T_0(1+\theta_0^2/16)\) expandindo
     \(\sen\theta\) até a ordem cúbica. Depois explique, sem fazer a conta,
     por que a cicloide de Huygens é exatamente isócrona, e por que isso não
     contradiz nada do que foi dito sobre o pêndulo circular.''',
     r'''<p><b>A expansão.</b> Com
     \(\sen\theta \simeq \theta - \theta^3/6\), a equação vira</p>
     <p>\[ \ddot\theta + \omega_0^2\theta
        \left(1 - \frac{\theta^2}{6}\right) = 0,
        \qquad \omega_0^2 = \frac{g}{L}. \]</p>
     <p>O termo cúbico enfraquece a força restauradora, e já se pode prever o
     sinal do efeito antes de qualquer conta: força menor, oscilação mais
     lenta, período maior. Tratando o termo como pequeno e exigindo que a
     solução não acumule erro de fase (o método de Lindstedt-Poincaré, que o
     módulo 9 retoma), sai</p>
     <p>\[ \omega \simeq \omega_0\left(1 - \frac{\theta_0^2}{16}\right)
        \quad\Longrightarrow\quad
        T \simeq T_0\left(1 + \frac{\theta_0^2}{16}\right). \]</p>
     <p>Em 20°, \(\theta_0 = 0{,}349\) rad e a correção vale 0,76 %, contra
     0,767 % do cálculo exato. Uma correção de um termo já captura quase todo
     o erro.</p>
     <p><b>A cicloide.</b> Huygens percebeu que o problema não era o pêndulo e
     sim a <em>curva</em>. Numa trajetória qualquer, o que importa é como a
     força restauradora varia com a distância percorrida ao longo da curva,
     medida pelo comprimento de arco \(s\). O período é rigorosamente
     independente da amplitude se, e somente se, a força for
     <em>exatamente</em> proporcional a \(s\):</p>
     <p>\[ \der{^2s}{t^2} = -\omega^2 s. \]</p>
     <p>No círculo, a força vale \(-mg\sen\theta\) enquanto o arco vale
     \(s = L\theta\): proporcional a \(\sen\theta\), não a \(\theta\), e daí
     todo o desvio. A cicloide é a curva em que a componente da gravidade ao
     longo do arco sai proporcional ao próprio arco, e por isso ela é
     <b>exatamente</b> isócrona, em qualquer amplitude.</p>
     <p><b>Por que não há contradição.</b> O isocronismo nunca foi propriedade
     da gravidade nem da oscilação: é propriedade da <em>força linear</em>. O
     pêndulo circular é quase isócrono porque \(\sen\theta \simeq \theta\)
     para \(\theta\) pequeno, e a cicloide é exatamente isócrona porque nela a
     linearidade é exata. As duas afirmações dizem a mesma coisa.</p>
     <p><b>E por que ninguém usa.</b> Huygens construiu relógios com guias
     cicloidais em 1673. O atrito do fio contra as guias introduzia mais erro
     do que a correção eliminava, e a solução que prevaleceu foi manter a
     amplitude pequena e constante, com um escapamento que repõe exatamente a
     energia perdida. É uma lição que vale além dos relógios: a solução
     teoricamente perfeita perdeu para a que convivia melhor com o atrito.</p>''' ),
]
