# -*- coding: utf-8 -*-
"""Exercícios propostos do módulo 11."""

LISTA = [
    ('11.1  Pesar a Terra com a órbita da Lua',
     r'''Mostre que a lei do inverso do quadrado implica a terceira lei de
     Kepler na forma \(T^2 = 4\pi^2a^3/G(M+m)\), e use a órbita da Lua
     (\(a = 384\,399\) km, \(T = 27{,}321661\) dias) para obter a massa da
     Terra. Compare com o valor aceito e explique a diferença.''',
     r'''<p><b>A dedução.</b> Para órbita circular, a atração fornece a força
     centrípeta da aceleração <em>relativa</em> dos dois corpos, que é
     \(G(M+m)/a^2\) (veja o módulo 5 sobre massa reduzida, e o exercício 12.1
     para o caso geral):</p>
     <p>\[ \frac{G(M+m)}{a^2} = \omega^2 a = \frac{4\pi^2a}{T^2}
        \quad\Longrightarrow\quad
        T^2 = \frac{4\pi^2a^3}{G(M+m)}. \]</p>
     <p>A constante de proporcionalidade não é universal: ela depende da massa
     total do par. É por isso que a terceira lei de Kepler, aplicada aos
     planetas, dá a massa do Sol, e aplicada às luas de Júpiter dá a massa de
     Júpiter.</p>
     <p><b>O número.</b> Com \(T = 2{,}360591\times10^6\) s:</p>
     <p>\[ M + m = \frac{4\pi^2a^3}{GT^2} = 6{,}030\times10^{24}\ \mathrm{kg}, \]</p>
     <p>contra \(6{,}046\times10^{24}\) aceito para Terra mais Lua: <b>0,27 %</b>
     de diferença.</p>
     <p><b>De onde vem a diferença.</b> Não é da medida: é do modelo. A órbita
     da Lua não é circular (\(e = 0{,}055\)), de modo que o \(a\) que entra na
     fórmula é o semieixo maior, e o valor usado aqui é a distância
     <em>média</em>, que não é a mesma coisa. Além disso o Sol perturba a
     órbita lunar de modo nada desprezível, a ponto de o mês sideral e o mês
     anomalístico diferirem em horas.</p>
     <p><b>O que isso ilustra.</b> Com dados de seis algarismos e uma conta de
     uma linha, chega-se à massa da Terra com três algarismos certos. Não é
     pouco: antes de Cavendish, ninguém sabia nem a ordem de grandeza. Mas
     insistir na quarta casa exige trocar de modelo, e não de régua.</p>''' ),

    ('11.2  O teorema das cascas pelo argumento dos cones',
     r'''Prove, sem integrar, que o campo dentro de uma casca esférica é nulo.
     Use dois cones opostos a partir de um ponto interno qualquer e mostre que
     as contribuições se cancelam. Depois explique o que aconteceria se a lei
     fosse \(1/r^{2+\epsilon}\).''',
     r'''<p><b>A construção.</b> Tome um ponto \(P\) qualquer dentro da casca e
     um cone duplo estreito, de ângulo sólido \(d\Omega\), com vértice em
     \(P\). Ele recorta dois pedaços da casca, a distâncias \(s_1\) e
     \(s_2\).</p>
     <p><b>As duas áreas.</b> Um cone de ângulo sólido \(d\Omega\) recorta, a
     distância \(s\), uma área \(dA = s^2\,d\Omega/\cos\alpha\), em que
     \(\alpha\) é a inclinação da superfície em relação ao plano perpendicular
     ao eixo do cone. Por simetria da esfera, essa inclinação é
     <em>a mesma</em> nos dois pedaços: a corda que liga os dois faz ângulos
     iguais com a superfície nas duas pontas.</p>
     <p><b>O cancelamento.</b> Com densidade superficial \(\sigma\), as massas
     são \(dm_i = \sigma s_i^2 d\Omega/\cos\alpha\), e os campos:</p>
     <p>\[ \frac{G\,dm_1}{s_1^2}
        = \frac{G\sigma\,d\Omega}{\cos\alpha}
        = \frac{G\,dm_2}{s_2^2}. \]</p>
     <p>As distâncias <b>somem</b>. Os dois campos têm o mesmo módulo e
     sentidos opostos, e se cancelam. Como o ponto \(P\) e a direção do cone
     eram quaisquer, e como toda a casca é coberta por esses pares, o campo
     total é nulo em qualquer ponto interno.</p>
     <p><b>Por que o expoente 2 é essencial.</b> O cancelamento acontece
     porque a massa cresce com \(s^2\) exatamente na mesma medida em que o
     campo cai com \(1/s^2\). Com \(1/s^{2+\epsilon}\), o campo de cada pedaço
     seria \(G\sigma\,d\Omega\,s^{-\epsilon}/\cos\alpha\), e o pedaço
     <em>próximo</em> venceria. Sobraria um campo residual apontando para a
     parede mais perto, proporcional a \(\epsilon\) em primeira ordem.</p>
     <p><b>A consequência experimental.</b> Isso faz do interior de uma casca
     um dos lugares mais sensíveis para testar a lei. O mesmo argumento vale
     palavra por palavra para a lei de Coulomb, e é exatamente assim que os
     melhores limites sobre o expoente elétrico foram obtidos: medindo campo
     dentro de condutores ocos, desde Cavendish e Maxwell. Para a gravidade os
     limites são muito piores, porque a força é fraca demais.</p>''' ),

    ('11.3  O túnel pela Terra, e um túnel torto',
     r'''Mostre que um corpo largado num túnel que atravessa a Terra pelo
     centro faz um movimento harmônico simples e calcule o período. Depois
     mostre o resultado notável: um túnel reto <em>qualquer</em>, mesmo sem
     passar pelo centro, dá o mesmo período.''',
     r'''<p><b>Pelo centro.</b> Dentro da esfera maciça, pelo teorema das
     cascas, só a massa interna conta:</p>
     <p>\[ F = -\frac{GM(r)m}{r^2} = -\frac{GMm}{R^3}r = -kr, \]</p>
     <p>que é a lei de Hooke com \(k = GMm/R^3\). Logo</p>
     <p>\[ T = 2\pi\sqrt{\frac{m}{k}} = 2\pi\sqrt{\frac{R^3}{GM}}
        = 5061\ \mathrm{s} = 84{,}35\ \text{minutos}. \]</p>
     <p>A viagem de um lado ao outro leva metade disso, 42 min, e não depende
     da massa do viajante.</p>
     <p><b>O túnel torto.</b> Seja um túnel reto cuja menor distância ao centro
     é \(b\), e seja \(x\) a posição ao longo do túnel, medida do ponto mais
     próximo do centro. A distância ao centro é \(r = \sqrt{b^2+x^2}\), e a
     força gravitacional tem módulo \(GMm r/R^3\), apontando para o centro. A
     componente ao longo do túnel é essa força vezes \(x/r\):</p>
     <p>\[ F_x = -\frac{GMm}{R^3}\,r\,\frac{x}{r} = -\frac{GMm}{R^3}\,x. \]</p>
     <p>O \(r\) <b>cancela</b>, e sobra exatamente a mesma constante elástica.
     O período é o mesmo 84,35 min para qualquer túnel reto, passando pelo
     centro ou não, longo ou curto.</p>
     <p><b>Por que isso é especial.</b> Esse cancelamento só acontece porque o
     campo interno é <em>linear</em> em \(r\), o que por sua vez só acontece
     porque a densidade é uniforme e a lei é a do inverso do quadrado. Numa
     Terra com núcleo denso (que é o caso real) ele falha, e o período depende
     do túnel. O número real, com o modelo PREM de densidade, fica perto de
     38 min para o túnel pelo centro, e não 42.</p>
     <p><b>O parentesco com o satélite.</b> O período de um satélite rasante é
     \(2\pi\sqrt{R^3/GM}\), o mesmo número. A razão é que o movimento no túnel
     é a <em>projeção</em> do movimento circular rasante sobre o diâmetro, e a
     projeção de um movimento circular uniforme é um harmônico simples de mesmo
     período.</p>''' ),

    ('11.4  Júpiter, o obstetra e as marés',
     r'''Obtenha \(a_{\text{maré}} \simeq 2GmR/d^3\) expandindo a diferença de
     campos em \(R/d\). Use a fórmula para comparar a maré que Júpiter exerce
     sobre a Terra com a da Lua, e a maré que a Lua exerce sobre um recém
     nascido com a do obstetra que o segura.''',
     r'''<p><b>A expansão.</b> Ao longo da linha dos centros, no lado próximo,
     a diferença entre o campo a distância \(d-R\) e a distância \(d\) é</p>
     <p>\[ \frac{Gm}{(d-R)^2} - \frac{Gm}{d^2}
        = \frac{Gm}{d^2}\left[\left(1-\frac{R}{d}\right)^{-2} - 1\right]. \]</p>
     <p>Com \(R \ll d\), \((1-x)^{-2} \simeq 1+2x\):</p>
     <p>\[ a_{\text{maré}} \simeq \frac{2GmR}{d^3}. \]</p>
     <p>No lado distante a mesma conta dá o mesmo módulo, com o sinal trocado
     em relação ao centro: os dois lados abaulam para fora.</p>
     <p><b>Júpiter contra a Lua.</b> A razão é</p>
     <p>\[ \frac{m_J}{m_L}\left(\frac{d_L}{d_J}\right)^3
        = \frac{1{,}898\times10^{27}}{7{,}342\times10^{22}}
          \left(\frac{3{,}844\times10^{8}}{6{,}29\times10^{11}}\right)^3
        = 5{,}9\times10^{-6}. \]</p>
     <p>Júpiter, na melhor oposição possível, produz sobre a Terra uma maré
     <b>seis milionésimos</b> da lunar, isto é, uns dois micrômetros de água.
     A conta vale para os outros planetas, com resultados ainda menores.</p>
     <p><b>A Lua contra o obstetra.</b> Agora o corpo que sofre a maré é um
     bebê, com \(R \simeq 0{,}10\) m:</p>
     <p>\[ a_{\text{Lua}} = \frac{2Gm_L(0{,}10)}{d_L^3}
        = 1{,}7\times10^{-14}\ \mathrm{m/s^2}, \]</p>
     <p>\[ a_{\text{obstetra}} = \frac{2G(70\ \mathrm{kg})(0{,}10)}{(1\ \mathrm{m})^3}
        = 9{,}3\times10^{-10}\ \mathrm{m/s^2}. \]</p>
     <p>O obstetra a um metro exerce sobre o recém-nascido uma força de maré
     <b>54 mil vezes maior</b> que a da Lua. Quem leva a sério a influência
     gravitacional dos astros sobre pessoas precisa, para ser coerente,
     levar muito mais a sério a influência de quem está no mesmo
     quarto.</p>
     <p><b>Por que a Lua move oceanos, então.</b> Porque o oceano tem 12 mil km
     de extensão, e não 10 cm: a maré é proporcional a \(R\). E porque a maré
     age de modo <em>coerente</em> e periódico sobre a bacia inteira, por
     bilhões de ciclos, o que permite ressonância. Força pequena e persistente,
     na frequência certa, é o assunto do módulo 8.</p>''' ),

    ('11.5  A balança de Cavendish, com números',
     r'''Uma balança de torção tem duas esferas de 0,73 kg nas pontas de uma
     haste de 1,86 m, suspensa por um fio, e o período de oscilação torsional é
     420 s. Duas esferas de 158 kg são aproximadas a 22,5 cm dos centros das
     pequenas. Calcule a deflexão de equilíbrio e mostre como \(G\) sai dessas
     medidas. Por que o período entra na conta?''',
     r'''<p><b>Por que o período.</b> A constante de torção \(\kappa\) do fio é
     pequena demais para ser medida aplicando torques conhecidos. Mas ela
     determina o período das oscilações livres da haste, pelo módulo 6:</p>
     <p>\[ T_0 = 2\pi\sqrt{\frac{I}{\kappa}}
        \quad\Longrightarrow\quad
        \kappa = \frac{4\pi^2I}{T_0^2}. \]</p>
     <p>Cronometrar sete minutos é fácil; medir \(10^{-4}\) N·m/rad
     diretamente, não. O oscilador funciona aqui como <em>instrumento</em>, e
     essa é a ideia central do experimento.</p>
     <p><b>Os números.</b> Com \(L = 0{,}93\) m de braço,</p>
     <p>\[ I = 2mL^2 = 1{,}263\ \mathrm{kg\,m^2},
        \qquad \kappa = \frac{4\pi^2(1{,}263)}{420^2}
        = 2{,}83\times10^{-4}\ \mathrm{N\,m/rad}. \]</p>
     <p>A força sobre cada esfera pequena e o torque total:</p>
     <p>\[ F = \frac{GMm}{b^2} = 1{,}52\times10^{-7}\ \mathrm{N},
        \qquad \tau = 2FL = 2{,}83\times10^{-7}\ \mathrm{N\,m}, \]</p>
     <p>\[ \theta = \frac{\tau}{\kappa} = 1{,}00\times10^{-3}\ \mathrm{rad}
        = 0{,}057^\circ, \]</p>
     <p>o que desloca cada esfera em <b>0,93 mm</b>. Essa é a medida inteira:
     menos de um milímetro, com duas toneladas de chumbo e um fio de
     torção.</p>
     <p><b>Isolando \(G\).</b> Juntando tudo,</p>
     <p>\[ G = \frac{2\pi^2 I\,b^2\,\theta}{T_0^2\,M\,m\,L}, \]</p>
     <p>e substituindo os números acima devolve \(6{,}674\times10^{-11}\), como
     tem de ser: a fórmula é apenas a conta anterior reorganizada.</p>
     <p><b>O que Cavendish realmente publicou.</b> O artigo se chama
     "Experiments to determine the Density of the Earth", e o resultado é
     5,48 vezes a densidade da água, contra 5,514 aceito hoje: erro de
     <b>0,6 %</b>. A constante \(G\) nem existia como conceito; ela foi
     introduzida décadas depois. Conhecida a densidade média e o raio, \(G\)
     sai de \(g = \frac43\pi G\rho R\), e é nesse sentido que se diz que
     Cavendish pesou a Terra.</p>
     <p><b>Por que \(G\) continua mal medida.</b> Hoje \(G\) é conhecida com
     cinco algarismos, e a carga do elétron com dez. A gravidade não pode ser
     blindada nem amplificada, e qualquer massa que se mexa nas redondezas
     entra na medida. Medidas independentes de alta qualidade ainda discordam
     entre si por mais do que as barras de erro de cada uma, o que é um
     problema em aberto.</p>''' ),

    ('11.6  A Lua se afasta, e o dia cresce',
     r'''O atrito das marés adianta o abaulamento em relação à linha
     Terra-Lua. Explique por que isso afasta a Lua e freia a Terra. Depois use
     o recuo medido, 3,8 cm por ano, e a conservação do momento angular para
     prever o aumento do dia, e compare com o observado.''',
     r'''<p><b>Por que o abaulamento se adianta.</b> A Terra gira em 24 h e a
     Lua leva 27 dias para dar a volta, de modo que a rotação arrasta o
     abaulamento <em>para a frente</em> da linha Terra-Lua. O atrito impede que
     ele se realinhe instantaneamente, e o resultado é um bojo adiantado alguns
     graus.</p>
     <p><b>As duas consequências.</b> Esse bojo adiantado está mais perto da
     Lua de um lado que do outro, e portanto puxa a Lua <em>para a frente</em>
     na órbita: torque positivo, que aumenta o momento angular orbital e afasta
     a Lua. Pela terceira lei, a Lua puxa o bojo para trás, freando a rotação
     da Terra. Momento angular sai da rotação e entra na órbita, e o total se
     conserva.</p>
     <p><b>A conta.</b> O momento angular orbital é
     \(L_{\text{orb}} = m\sqrt{G(M+m)a}\), de modo que</p>
     <p>\[ \der{L_{\text{orb}}}{t}
        = \frac{m}{2}\sqrt{\frac{G(M+m)}{a}}\;\der{a}{t}
        = 1{,}43\times10^{24}\ \mathrm{J\,s\ por\ ano} \]</p>
     <p>com \(da/dt = 3{,}8\) cm/ano. Esse momento angular sai da rotação
     terrestre, com \(I = 0{,}3307\,MR^2 = 8{,}02\times10^{37}\)
     kg·m² (o coeficiente é menor que \(2/5\) porque a Terra tem o núcleo
     denso):</p>
     <p>\[ \der{\omega}{t} = -\frac{1}{I}\der{L_{\text{orb}}}{t}
        = -1{,}78\times10^{-14}\ \mathrm{rad/s\ por\ ano}, \]</p>
     <p>\[ \der{T_{\text{dia}}}{t} = -\frac{2\pi}{\omega^2}\der{\omega}{t}
        = 2{,}1\ \mathrm{ms\ por\ século}. \]</p>
     <p><b>A comparação.</b> O aumento do dia efetivamente observado, pelos
     registros de eclipses antigos, é de cerca de <b>1,8 ms por século</b>. A
     previsão acima dá 2,1, e a diferença não é erro de conta: a Terra também
     está <em>acelerando</em> a rotação por outro motivo, o reajuste do manto
     depois do degelo da última era glacial, que aproxima massa do eixo e
     diminui \(I\). Os dois efeitos se subtraem.</p>
     <p><b>O registro fóssil.</b> Corais do Devoniano, há 380 milhões de anos,
     mostram cerca de 400 bandas de crescimento diário por banda anual: o ano
     tinha o mesmo comprimento e o dia era mais curto, com umas 22 h.
     Extrapolar 1,8 ms/século para 380 milhões de anos dá a mesma ordem, e
     essa é uma das confirmações mais bonitas que a mecânica celeste tem,
     porque vem da paleontologia.</p>
     <p><b>Onde isso termina.</b> O processo só para quando o dia igualar o
     mês, com a Terra mostrando sempre a mesma face à Lua, o que levaria
     dezenas de bilhões de anos (mais do que a vida restante do Sol). A Lua já
     chegou lá, e é por isso que nos mostra sempre a mesma face. Plutão e
     Caronte completaram os dois lados do processo.</p>''' ),
]
