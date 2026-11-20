# -*- coding: utf-8 -*-
"""Página inicial de Mecânica Clássica I (DF005)."""
from molde import MODULOS, escreve, existe
import sites

# (número do módulo, descrição, etiquetas)
DESCRICOES = {
    1: ('Soma, produto escalar e vetorial, a matriz de rotação e o que faz de '
        'um trio de números um vetor. Gradiente, divergente e rotacional, e o '
        'teorema que diz quando uma força vem de um potencial.',
        ['Rotação e transformação', 'Gradiente', 'Campo conservativo']),
    2: ('As três leis lidas com cuidado, o que cada uma afirma e o que cada '
        'uma define. Referencial inercial, massa inercial e a diferença entre '
        'uma lei e uma convenção.',
        ['O que a primeira lei define', 'Diagrama de corpo livre', 'Inercial']),
    3: ('A equação de movimento como equação diferencial. Força constante, '
        'força que depende do tempo, arrasto linear e quadrático, velocidade '
        'terminal e a queda que não é a da fórmula do ensino médio.',
        ['Arrasto', 'Velocidade terminal', 'Integração numérica']),
    4: ('Trabalho, energia cinética e o teorema que liga os dois. Quando a '
        'força é conservativa, o potencial existe, e o gráfico de \\(U(x)\\) '
        'conta a história inteira do movimento sem resolver equação nenhuma.',
        ['Teorema trabalho-energia', 'Potencial', 'Pontos de retorno']),
    5: ('Impulso, conservação do momento e a razão de ela ser mais funda que '
        'a conservação da energia. A equação do foguete, deduzida da massa '
        'variável, e o que ela diz sobre viagens espaciais.',
        ['Impulso', 'Equação do foguete', 'Massa variável']),
    6: ('O movimento que aparece em toda parte, porque todo mínimo de '
        'potencial é uma parábola de perto. Solução, espaço de fase, energia '
        'e os sistemas que obedecem à mesma equação.',
        ['Aproximação harmônica', 'Espaço de fase', 'Analogias']),
    7: ('Atrito linear e os três regimes: subamortecido, crítico e '
        'superamortecido. Fator de qualidade, decremento logarítmico, e por '
        'que o amortecimento crítico é o que se quer numa porta e num '
        'amortecedor.',
        ['Três regimes', 'Fator Q', 'Amortecimento crítico']),
    8: ('Regime transiente e regime permanente, curva de ressonância, largura '
        'de banda e defasagem. Depois, a força qualquer: resposta a impulso, '
        'superposição e a série de Fourier como ferramenta de engenheiro.',
        ['Ressonância', 'Defasagem', 'Fourier']),
    9: ('O que acontece quando a aproximação harmônica não serve. Pêndulo '
        'completo, período que depende da amplitude, retratos de fase, pontos '
        'de sela e separatrizes.',
        ['Pêndulo completo', 'Retrato de fase', 'Separatriz']),
    10: ('Determinismo não é previsibilidade. Mapa logístico, duplicação de '
         'período e a constante de Feigenbaum, expoente de Lyapunov, o '
         'oscilador de Duffing e o atrator estranho.',
         ['Mapa logístico', 'Feigenbaum', 'Lyapunov']),
    11: ('A lei do inverso do quadrado, o campo e o potencial gravitacionais, '
         'o teorema das cascas provado de duas maneiras, e as marés como '
         'efeito de gradiente e não de atração.',
         ['Teorema das cascas', 'Potencial', 'Marés']),
    12: ('Redução a um corpo com massa reduzida, as duas constantes de '
         'movimento, o potencial efetivo e a classificação das órbitas. As '
         'três leis de Kepler deduzidas, e não postuladas.',
         ['Massa reduzida', 'Potencial efetivo', 'Kepler deduzido']),
    13: ('Centro de massa de um sistema qualquer, as três conservações, '
         'colisões elásticas e inelásticas, e o espalhamento visto do '
         'laboratório e do centro de massa.',
         ['Centro de massa', 'Colisões', 'Espalhamento']),
}


def cartoes():
    linhas = []
    unidade = None
    for arq, num, titulo, _curto, uni in MODULOS:
        if uni != unidade:
            if unidade is not None:
                linhas.append('  </div>\n')
            unidade = uni
            linhas.append('  <h3 class="unidade">%s</h3>\n' % uni)
            linhas.append('  <div class="cartoes">\n')
        desc, etiquetas = DESCRICOES[num]
        eti = '\n'.join('        <span class="etiqueta">%s</span>' % e
                        for e in etiquetas)
        corpo = ('''      <span class="numero">Módulo %d</span>
      <h3>%s</h3>
      <p>%s</p>
      <div class="etiquetas">
%s
      </div>''' % (num, titulo, desc, eti))
        if existe(arq):
            linhas.append('    <a class="cartao" href="%s">\n%s\n    </a>\n'
                          % (arq, corpo))
        else:
            linhas.append('    <div class="cartao pendente">\n%s\n'
                          '      <p class="aviso">Em preparação</p>\n'
                          '    </div>\n' % corpo)
    linhas.append('  </div>\n')
    return ''.join(linhas)


ABERTURA = r'''
  <p>Na noite de 23 de setembro de 1846, o astrônomo Johann Gottfried Galle
  apontou o telescópio do Observatório de Berlim para um pedaço de céu que
  ninguém tinha motivo para examinar. Ele seguia uma carta recebida naquele
  mesmo dia, vinda de Paris, assinada por Urbain Le Verrier, e a carta não
  trazia uma observação: trazia uma previsão. Em menos de uma hora, Galle e o
  estudante Heinrich d'Arrest encontraram um objeto que não constava das
  cartas celestes, a menos de um grau da posição anunciada.</p>

  <p>O que Le Verrier tinha feito nos meses anteriores não envolveu telescópio
  nenhum. Urano não andava exatamente onde deveria, e as discrepâncias eram
  minúsculas, da ordem de um minuto de arco. Ele supôs que houvesse um planeta
  ainda desconhecido puxando Urano, escreveu as equações de movimento com a lei
  da gravitação, e resolveu o problema ao contrário: dada a perturbação, onde
  está quem a causa? A resposta foi um ponto no céu, e o ponto estava certo.</p>

  <p>Essa é a demonstração mais espetacular de uma ideia que esta disciplina
  desenvolve do começo ao fim: conhecidas as forças e o estado inicial, o futuro
  está determinado, e pode ser calculado. É uma ideia com pouco mais de trezentos
  anos, e mudou o que se entende por explicar alguma coisa.</p>

  <p>Há um segundo capítulo nessa história, e ele também cabe aqui. Em 1889, o
  rei Óscar II da Suécia ofereceu um prêmio a quem demonstrasse que o Sistema
  Solar é estável. Henri Poincaré ganhou, e depois, revisando as provas já
  impressas do seu próprio trabalho, encontrou um erro. Ao consertá-lo,
  descobriu o contrário do que pensara ter provado: há órbitas tão
  emaranhadas que nenhuma fórmula as descreve, e diferenças mínimas nas
  condições iniciais crescem sem limite. O determinismo continuava de pé; a
  previsibilidade, não.</p>

  <p>Entre esses dois resultados cabe o curso inteiro. Os cinco primeiros
  módulos montam a máquina de Newton com cuidado, os quatro seguintes a aplicam
  ao movimento mais comum da natureza, que é a oscilação, o décimo mostra onde a
  máquina deixa de ser previsível, e os três últimos voltam ao céu para deduzir
  as leis de Kepler em vez de decorá-las.</p>

  <hr class="linha">
'''

PLANO = r'''
  <div class="bloco def">
    <span class="rotulo">Identificação</span>
    <p><strong>Curso:</strong> Bacharelado em Física<br>
    <strong>Disciplina:</strong> Mecânica Clássica I (DF005), obrigatória<br>
    <strong>Carga horária:</strong> 60 h teóricas, 4 h semanais, 4 créditos<br>
    <strong>Segue:</strong> Mecânica Clássica II (DF006), que tem esta como
    pré-requisito</p>
  </div>

  <p><strong>Ementa.</strong> Revisão de cálculo vetorial. Mecânica newtoniana
  de uma partícula: leis de Newton, equações de movimento, trabalho, energia,
  momento linear e sistemas de massa variável. Oscilações livres, amortecidas e
  forçadas. Oscilações não lineares e introdução ao caos determinístico.
  Gravitação. Movimento sob forças centrais e o problema de dois corpos.
  Dinâmica de sistemas de partículas e colisões.</p>

  <p><strong>Objetivos.</strong> Formular e resolver equações de movimento para
  sistemas de uma e de várias partículas, analiticamente onde houver solução
  fechada e numericamente onde não houver. Reconhecer o oscilador harmônico
  como aproximação universal perto de um mínimo de potencial e saber quando ela
  falha. Deduzir as leis de Kepler a partir da lei da gravitação. Distinguir
  determinismo de previsibilidade.</p>

  <p><strong>Avaliação.</strong> Três provas escritas e uma lista de problemas
  computacionais, em que cada estudante resolve numericamente um problema sem
  solução fechada e confere o resultado contra um caso limite conhecido.</p>

  <div class="bloco alerta">
    <span class="rotulo">Sobre os programas</span>
    <p>Boa parte do que esta disciplina pede não tem solução em fórmula fechada:
    a queda com arrasto quadrático, o pêndulo de amplitude grande, o oscilador
    forçado não linear, a órbita perturbada. Cada módulo que precisa disso traz
    um programa em Python, comentado, que roda no Spyder sem configuração, e
    que sempre inclui uma maneira de conferir se o resultado está certo: um
    caso limite com solução conhecida, uma quantidade que tem de se conservar,
    ou a ordem de convergência esperada.</p>
  </div>
'''

BIBLIOGRAFIA = r'''
  <p><strong>Bibliografia básica</strong></p>
  <ul>
    <li>THORNTON, S. T.; MARION, J. B. <em>Classical Dynamics of Particles and
    Systems</em>. 5. ed. Cengage Learning, 2003. A referência de ordem desta
    disciplina: os capítulos 1 a 5, 8 e 9.</li>
    <li>TAYLOR, J. R. <em>Classical Mechanics</em>. University Science Books,
    2005. Mais conversado, excelente nos capítulos de oscilações e de caos.</li>
    <li>SYMON, K. R. <em>Mecânica</em>. 3. ed. Rio de Janeiro: Campus, 1982.
    Clássico em português, forte em sistemas de partículas.</li>
  </ul>

  <p><strong>Complementar</strong></p>
  <ul>
    <li>STROGATZ, S. H. <em>Nonlinear Dynamics and Chaos</em>. 2. ed. Westview,
    2015. Para os módulos 9 e 10, é a melhor porta de entrada que existe.</li>
    <li>KIBBLE, T. W. B.; BERKSHIRE, F. H. <em>Classical Mechanics</em>. 5. ed.
    Imperial College Press, 2004.</li>
  </ul>

  <div class="bloco def">
    <span class="rotulo">Disciplinas vizinhas</span>
    <p>O que vem depois, em
    <a href="https://apianomorais.github.io/mecanica-classica-ii/">Mecânica
    Clássica II</a> (DF006), é corpo rígido, referenciais em rotação, cálculo
    variacional e os formalismos de Lagrange e de Hamilton. O espaço de fase
    que aparece aqui nos módulos 6 e 9 é o mesmo que reaparece lá no teorema de
    Liouville, e depois em
    <a href="https://apianomorais.github.io/fisica-estatistica/">Física
    Estatística</a> como ponto de partida.</p>
  </div>
'''


def main():
    corpo = []
    corpo.append('  <h2 id="s1">1. Duas noites e uma ideia</h2>\n' + ABERTURA)
    corpo.append('  <h2 id="s2">2. Os módulos</h2>\n' + cartoes())
    corpo.append('  <h2 id="s3">3. O plano de ensino</h2>\n' + PLANO)
    corpo.append('  <h2 id="s4">4. Bibliografia</h2>\n' + BIBLIOGRAFIA)
    corpo.append('  <h2 id="s5">5. Outros sites</h2>\n'
                 + sites.bloco(aqui='mecanica-classica-i', titulo=False))
    escreve('index.html', '\n'.join(corpo),
            secoes=['Duas noites e uma ideia', 'Os módulos',
                    'O plano de ensino', 'Bibliografia', 'Outros sites'],
            titulo='Mecânica Clássica I',
            chapeu='DF005 · Bacharelado em Física · LFCA/URCA',
            subtitulo='Material interativo da disciplina. Das leis de Newton '
                      'às órbitas de Kepler, passando pelas oscilações e pelo '
                      'ponto em que o determinismo deixa de ser previsão.')


if __name__ == '__main__':
    main()
