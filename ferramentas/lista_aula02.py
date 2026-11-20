# -*- coding: utf-8 -*-
"""Exercícios propostos do módulo 2."""

LISTA = [
    ('2.1  Por que a primeira lei precisa existir',
     r'''Mostre, com um exemplo concreto, que a primeira lei não é o caso
     particular da segunda com \(\vet{F} = 0\). Depois responda: como alguém
     dentro de uma caixa fechada pode descobrir se o seu referencial é
     inercial?''',
     r'''<p><b>O exemplo.</b> Um vagão freia a \(2\ \mathrm{m/s^2}\), e sobre o
     piso liso há uma bola. Para quem está na plataforma, a bola segue em linha
     reta com velocidade constante: nenhuma força horizontal age sobre ela, e
     ela não acelera. Para quem está dentro do vagão, a mesma bola
     <em>acelera</em> para a frente a \(2\ \mathrm{m/s^2}\), sem que exista
     agente algum que a empurre.</p>
     <p>Se a primeira lei fosse apenas \(\vet{F} = 0 \Rightarrow \vet{a} = 0\),
     ela seria simplesmente <b>falsa</b> dentro do vagão. O que ela afirma, na
     verdade, é que existem referenciais em que a implicação vale, e esses são
     os inerciais. Ela não é um caso particular: é a condição de validade dos
     outros dois.</p>
     <p><b>O teste dentro da caixa.</b> Solte corpos de massas e materiais
     diferentes, longe de tudo, e veja se todos permanecem em repouso. Se
     algum acelerar sem agente identificável, o referencial não é inercial.</p>
     <p><b>A ressalva de Einstein.</b> Esse teste não distingue um referencial
     acelerado de um campo gravitacional uniforme, porque nos dois casos todos
     os corpos aceleram igual. Para distinguir, é preciso uma caixa grande o
     bastante para notar que as linhas de campo de uma massa real
     <em>convergem</em>: dois corpos soltos lado a lado se aproximam um pouco.
     Esse efeito de maré é o que a relatividade geral chama de curvatura, e é
     a única assinatura local de gravidade de verdade.</p>''' ),

    ('2.2  Se as duas massas fossem diferentes',
     r'''Suponha que, para dois materiais, a razão \(m_g/m_i\) diferisse de
     \(\eta = 10^{-12}\). Calcule a diferença de tempo de queda de uma altura
     de 10 m e a separação entre os dois corpos ao chegarem ao chão. Comente
     por que os experimentos de precisão não usam queda livre.''',
     r'''<p><b>As acelerações</b> diferem pela mesma fração:
     \(\Delta a / a = \eta\).</p>
     <p><b>A diferença de tempo.</b> De \(h = \frac12at^2\) vem
     \(t = \sqrt{2h/a}\), de modo que</p>
     <p>\[ \frac{\Delta t}{t} = -\frac{1}{2}\frac{\Delta a}{a}
        \;\Longrightarrow\;
        \Delta t = \frac{\eta t}{2}
        = \frac{10^{-12}\times1{,}428}{2}
        = 7{,}1\times10^{-13}\ \mathrm{s}. \]</p>
     <p><b>A separação</b> no instante da chegada:</p>
     <p>\[ \Delta h = \frac{1}{2}\eta g t^2 = 1{,}0\times10^{-11}\ \mathrm{m}, \]</p>
     <p>isto é, um centésimo do diâmetro de um átomo.</p>
     <p><b>Por que não se usa queda livre.</b> Medir \(10^{-11}\) m numa queda
     de 1,4 s é impossível. A saída dos experimentos de precisão é trocar a
     medida de uma diferença pequena por uma medida de <em>nulo</em>: a balança
     de torção de Eötvös compara duas massas penduradas, e o que se mede é se o
     fio torce ou não. Um aparelho de nulo não precisa de escala calibrada,
     apenas de estabilidade, e por isso ganha várias ordens de grandeza.</p>
     <p>A mesma ideia reaparece em toda a física experimental: a ponte de
     Wheatstone, o interferômetro de Michelson e o LIGO são todos aparelhos de
     nulo.</p>''' ),

    ('2.3  Dois blocos, um plano e um fio',
     r'''Um bloco de \(m_1 = 2{,}0\ \mathrm{kg}\) está num plano inclinado de
     30°, com \(\mu = 0{,}20\), ligado por um fio que passa por uma polia ideal
     a um bloco de \(m_2 = 1{,}5\ \mathrm{kg}\) pendurado. Verifique se o
     sistema se move, e, se mover, calcule a aceleração e a tração.''',
     r'''<p><b>Primeiro, decidir se move.</b> Compare o que puxa com o que
     segura, usando \(g = 9{,}80665\ \mathrm{m/s^2}\):</p>
     <div class="tabela-rolavel">
     <table>
     <thead><tr><th>agente</th><th>valor</th></tr></thead>
     <tbody>
     <tr><td>peso de \(m_2\), puxando</td><td>\(m_2g = 14{,}71\) N</td></tr>
     <tr><td>componente do peso de \(m_1\), segurando</td>
         <td>\(m_1g\sen30^\circ = 9{,}81\) N</td></tr>
     <tr><td>atrito máximo</td>
         <td>\(\mu m_1g\cos30^\circ = 3{,}40\) N</td></tr>
     </tbody>
     </table>
     </div>
     <p>Como \(14{,}71 \gt 9{,}81 + 3{,}40 = 13{,}21\), o sistema se move, com
     \(m_2\) descendo.</p>
     <p><b>Os dois diagramas.</b> Para \(m_2\), tomando positivo para baixo:</p>
     <p>\[ m_2g - T = m_2a. \]</p>
     <p>Para \(m_1\), positivo subindo o plano:</p>
     <p>\[ T - m_1g\sen\theta - \mu m_1g\cos\theta = m_1a. \]</p>
     <p><b>Somando</b>, a tração se cancela, que é a razão de somar:</p>
     <p>\[ a = \frac{m_2g - m_1g\sen\theta - \mu m_1g\cos\theta}{m_1+m_2}
        = \frac{1{,}508}{3{,}5} = 0{,}430\ \mathrm{m/s^2}. \]</p>
     <p><b>A tração</b> sai de qualquer uma das duas:</p>
     <p>\[ T = m_2\left(g-a\right) = 1{,}5\times9{,}376
        = 14{,}06\ \mathrm{N}. \]</p>
     <p><b>Confira pelo outro lado:</b> \(T - 9{,}81 - 3{,}40 = 0{,}861\), e
     \(m_1a = 2{,}0\times0{,}430 = 0{,}861\). Fecha.</p>
     <p><b>Uma observação sobre a tração.</b> Ela é menor que \(m_2g\), e tem de
     ser: se fosse igual, \(m_2\) não aceleraria. E é maior que a força
     necessária para segurar \(m_1\) parado, porque além de segurar ela
     acelera. Tração não é "o peso do que está pendurado", e esse é o erro mais
     comum do capítulo.</p>''' ),

    ('2.4  Para que lado desvia',
     r'''Um corpo é solto do alto de uma torre de 100 m. Calcule o desvio de
     Coriolis no Crato (7,23° S) e em Paris (48,85° N), e diga para que lado
     ele desvia em cada caso. Depois estime o desvio lateral de um projétil de
     artilharia com alcance de 40 km e velocidade de 800 m/s, a 30° de
     latitude.''',
     r'''<p><b>A queda.</b> Com \(t = \sqrt{2h/g} = 4{,}52\) s e</p>
     <p>\[ d = \frac{1}{3}\omega gt^3\cos\lambda, \]</p>
     <p>obtém-se <b>2,18 cm</b> no Crato e <b>1,55 cm</b> em Paris. Em
     <em>ambos</em> o desvio é para <b>leste</b>, e o hemisfério não importa
     aqui: o que importa é que o alto da torre tem velocidade tangencial maior
     que a base, por estar mais longe do eixo, e o corpo leva essa vantagem
     consigo.</p>
     <p>Repare que o desvio vai com \(\cos\lambda\), e não com \(\sen\lambda\):
     é máximo no equador e nulo nos polos, ao contrário do pêndulo de
     Foucault.</p>
     <p><b>O projétil.</b> Para movimento horizontal, a componente que desvia
     vai com \(\sen\lambda\), e a estimativa é</p>
     <p>\[ d \approx \omega v t\sen\lambda
        = 7{,}29\times10^{-5}\times800\times50\times0{,}50
        = 1{,}5\ \mathrm{m}. \]</p>
     <p>Para a direita no hemisfério norte, para a esquerda no sul.</p>
     <p><b>Por que isso é famoso.</b> Um metro e meio em 40 km é 0,004 % de
     erro, e ainda assim é a diferença entre acertar e errar um alvo. As tabelas
     de tiro da artilharia naval da Primeira Guerra já traziam a correção, e
     conta-se que os ingleses, nas Malvinas em 1914, erraram os primeiros tiros
     por usarem tabelas calculadas para o hemisfério norte, com o sinal
     trocado.</p>''' ),

    ('2.5  O pêndulo que não cabe no Cariri',
     r'''Calcule o período de precessão de um pêndulo de Foucault no Crato
     (7,23° S) e em Paris (48,85° N). Quanto tempo é preciso esperar, no Crato,
     para ver o plano girar um grau? Comente a viabilidade da demonstração.''',
     r'''<p><b>A fórmula.</b> O plano precessa com \(\Omega =
     \omega\sen\lambda\), de modo que</p>
     <p>\[ T_{\text{prec}} = \frac{T_{\text{sideral}}}{\sen\lambda}
        = \frac{23{,}934\ \mathrm{h}}{\sen\lambda}. \]</p>
     <p><b>Os números.</b> No Crato, \(\sen7{,}23^\circ = 0{,}1259\), de modo
     que</p>
     <p>\[ T_{\text{prec}} = \frac{23{,}934}{0{,}1259}
        = 190{,}2\ \mathrm{h} = 7{,}9\ \mathrm{dias}. \]</p>
     <p>Em Paris, \(\sen48{,}85^\circ = 0{,}7530\) e o período é de
     <b>31,8 h</b>.</p>
     <p><b>Um grau no Crato</b> leva \(190{,}2/360 = 0{,}528\) h, isto é,
     <b>32 minutos</b>. Para uma aula de duas horas, o plano gira menos de
     quatro graus.</p>
     <p><b>A viabilidade.</b> Quatro graus é mensurável, mas exige um pêndulo
     bom: fio longo, massa pesada, suspensão que não imponha direção
     preferencial, e proteção contra corrente de ar. O maior inimigo não é a
     lentidão, e sim a <em>elipse</em>: qualquer assimetria no lançamento faz o
     pêndulo descrever uma elipse que precessa sozinha, por um efeito puramente
     dinâmico, e esse falso sinal pode ser maior que o verdadeiro. Foucault
     resolvia isso prendendo a massa com um fio e queimando o fio, para que o
     lançamento não tivesse componente lateral nenhuma.</p>''' ),

    ('2.6  Quando a terceira lei falha',
     r'''Duas cargas iguais movem-se, num certo instante, com velocidades
     perpendiculares entre si: a primeira ao longo de \(\vers{x}\) e a segunda,
     colocada sobre o eixo \(x\) à frente dela, ao longo de \(\vers{y}\).
     Argumente que as forças magnéticas entre elas não obedecem à terceira lei,
     e diga o que salva a conservação do momento.''',
     r'''<p><b>O campo da primeira sobre a segunda.</b> Uma carga movendo-se ao
     longo de \(\vers{x}\) produz, num ponto à frente dela sobre o próprio eixo
     \(x\), um campo magnético <b>nulo</b>, porque \(\vet{B} \propto
     \vet{v}\cruz\vers{r}\) e aqui \(\vet{v}\) é paralelo a \(\vers{r}\). Logo
     a segunda carga não sofre força magnética alguma.</p>
     <p><b>O campo da segunda sobre a primeira.</b> A segunda carga move-se ao
     longo de \(\vers{y}\), e o vetor que a liga à primeira é \(-\vers{x}\).
     Agora \(\vet{v}\cruz\vers{r} \neq 0\), de modo que existe campo na posição
     da primeira carga, e existe força sobre ela.</p>
     <p><b>A conclusão.</b> Uma sente força e a outra não. Não há como isso ser
     "igual e oposto": a terceira lei falha na forma fraca, e com ela falharia a
     conservação do momento do par de partículas.</p>
     <p><b>O que salva.</b> O campo eletromagnético também carrega momento, com
     densidade \(\vet{g} = \varepsilon_0\vet{E}\cruz\vet{B}\). Somando o momento
     das partículas com o do campo, o total se conserva exatamente. O
     <a href="https://apianomorais.github.io/eletromagnetismo/cap08.html">capítulo
     8 de Eletromagnetismo</a> faz essa conta, e mostra inclusive que existe
     momento angular guardado em arranjos completamente estáticos.</p>
     <p><b>A moral para este curso.</b> A terceira lei é uma excelente
     aproximação sempre que a propagação puder ser tratada como instantânea,
     isto é, sempre que o tempo que a luz leva para cruzar o sistema for
     desprezível. Para dois blocos e um fio, isso é sempre. Para duas cargas
     relativísticas, nunca.</p>''' ),
]
