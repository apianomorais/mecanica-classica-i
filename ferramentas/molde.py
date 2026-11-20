# -*- coding: utf-8 -*-
"""Molde das páginas de Mecânica Clássica I (DF005).

A única fonte de verdade é a lista MODULOS abaixo: o menu do topo, as setas de
navegação e os cartões da página inicial saem toda dela. Módulo ainda não
escrito aparece no menu sem link, para o aluno saber que existe no plano da
disciplina, e nunca produz link quebrado.

Uso típico, a partir da raiz do site:

    python3 ferramentas/pagina_index.py
    python3 ferramentas/pagina_aula01.py
    ...

A marcação reproduz a das disciplinas irmãs (Mecânica Clássica II e III), de
modo que o mesmo estilo.css serve para as três.

Prof. Apiano Morais - LFCA/URCA
"""
import datetime
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
VERSAO = datetime.datetime.now().strftime('%Y%m%d%H%M')

# (arquivo, número, título do módulo, título curto para as setas, unidade)
MODULOS = [
    ('aula01.html', 1, 'Vetores, matrizes e cálculo vetorial',
     'Vetores e cálculo vetorial', 'Ferramentas'),
    ('aula02.html', 2, 'As leis de Newton e os referenciais inerciais',
     'As leis de Newton', 'Mecânica newtoniana'),
    ('aula03.html', 3, 'Forças que dependem do tempo, da velocidade e da posição',
     'Forças e arrasto', 'Mecânica newtoniana'),
    ('aula04.html', 4, 'Trabalho, energia e forças conservativas',
     'Trabalho e energia', 'Mecânica newtoniana'),
    ('aula05.html', 5, 'Momento linear, impulso e o movimento de foguetes',
     'Momento e foguetes', 'Mecânica newtoniana'),
    ('aula06.html', 6, 'O oscilador harmônico simples',
     'Oscilador harmônico', 'Oscilações'),
    ('aula07.html', 7, 'Oscilações amortecidas',
     'Oscilações amortecidas', 'Oscilações'),
    ('aula08.html', 8, 'Oscilações forçadas, ressonância e a resposta a uma força qualquer',
     'Oscilações forçadas', 'Oscilações'),
    ('aula09.html', 9, 'Além do linear: pêndulo, espaço de fase e retratos de fase',
     'Além do linear', 'Não linear e caos'),
    ('aula10.html', 10, 'Caos determinístico: mapa logístico, Lyapunov e atratores',
     'Caos determinístico', 'Não linear e caos'),
    ('aula11.html', 11, 'Gravitação: campo, potencial, cascas e marés',
     'Gravitação', 'Gravitação e forças centrais'),
    ('aula12.html', 12, 'Forças centrais: o problema de dois corpos e as órbitas de Kepler',
     'Forças centrais', 'Gravitação e forças centrais'),
    ('aula13.html', 13, 'Sistemas de partículas: centro de massa, colisões e espalhamento',
     'Sistemas de partículas', 'Gravitação e forças centrais'),
]

# abreviações das unidades, para o menu do topo não estourar a largura
CURTO = {
    'Ferramentas': 'Ferramentas',
    'Mecânica newtoniana': 'Newton',
    'Oscilações': 'Oscilações',
    'Não linear e caos': 'Caos',
    'Gravitação e forças centrais': 'Gravitação',
}

SERVICO = [
    ('formulario.html', 'Formulário'),
    ('codigo.html', 'Código'),
]


def existe(arquivo):
    return (RAIZ / arquivo).exists()


def menu(atual):
    """Menu do topo: Início, os módulos por unidade e as páginas de serviço."""
    partes = ['<a href="index.html"%s>Início</a>'
              % (' class="ativo"' if atual == 'index.html' else '')]
    unidade = None
    for arq, num, titulo, _curto, uni in MODULOS:
        if uni != unidade:
            unidade = uni
            partes.append('<span class="grupo">%s</span>' % CURTO.get(uni, uni))
        rotulo = 'Módulo %d: %s' % (num, titulo)
        if existe(arq):
            classe = 'num ativo' if arq == atual else 'num'
            partes.append('<a href="%s" class="%s" title="%s">%d</a>'
                          % (arq, classe, rotulo, num))
        else:
            partes.append('<span class="num pendente" title="%s · em preparação">'
                          '%d</span>' % (rotulo, num))
    for arq, nome in SERVICO:
        if existe(arq):
            classe = ' class="ativo"' if arq == atual else ''
            partes.append('<a href="%s"%s>%s</a>' % (arq, classe, nome))
    return '\n      ' + '\n      '.join(partes) + '\n    '


def navegacao(atual):
    """Setas anterior e próximo, pulando o que ainda não existe."""
    seq = ['index.html'] + [m[0] for m in MODULOS if existe(m[0])]
    seq += [a for a, _ in SERVICO if existe(a)]
    if atual not in seq:
        return ''
    i = seq.index(atual)
    partes = []

    def rotulo(arq):
        for a, num, titulo, curto, _uni in MODULOS:
            if a == arq:
                return '%d. %s' % (num, curto)
        for a, nome in SERVICO:
            if a == arq:
                return nome
        return 'Início'

    if i > 0:
        ant = seq[i - 1]
        texto = 'Voltar' if ant == 'index.html' else 'Módulo anterior'
        partes.append('<a href="%s"><small>%s</small>← %s</a>'
                      % (ant, texto, rotulo(ant)))
    if i < len(seq) - 1:
        pro = seq[i + 1]
        partes.append('<a class="prox" href="%s"><small>Próximo</small>%s →</a>'
                      % (pro, rotulo(pro)))
    if not partes:
        return ''
    return ('<nav class="nav-aulas">\n    %s\n  </nav>'
            % '\n    '.join(partes))


CABECA = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} | Mecânica Clássica I</title>
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="stylesheet" href="assets/css/estilo.css?v={versao}">
<script src="assets/js/comum.js?v={versao}"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>

<header class="topo">
  <div class="topo-interno">
    <a class="marca" href="index.html">Mecânica Clássica I <span>· LFCA/URCA</span></a>
    <nav class="menu">{menu}</nav>
  </div>
</header>

<div class="envoltorio">
{lateral}
<main class="conteudo">

{chapeu}  <h1>{h1}</h1>
{subtitulo}
{corpo}

  {nav}

</main>
</div>

<footer class="rodape">
  <img class="logo-rodape" src="assets/img/logo-lfca.png" alt="LFCA | URCA">
  <p><strong>Prof. Apiano Morais</strong> · <a href="mailto:apiano.morais@urca.br">apiano.morais@urca.br</a><br>
  Laboratório de Física Computacional Aplicada (LFCA) · Universidade Regional do Cariri</p>
  <!--PORTAL--><p><small><a href="https://apianomorais.github.io/">Todas as disciplinas e a pesquisa em apianomorais.github.io</a></small></p><!--/PORTAL-->
</footer>

<script src="assets/js/widgets.js?v={versao}"></script>
</body>
</html>
'''


def secoes_html(secoes):
    """Numera as seções e põe as âncoras s1, s2, ... que a lateral usa."""
    partes = []
    for i, (titulo, corpo) in enumerate(secoes, 1):
        partes.append('  <h2 id="s%d">%d. %s</h2>\n%s' % (i, i, titulo, corpo))
    return '\n'.join(partes)


def escreve(arquivo, corpo, secoes=None, chapeu=None, titulo=None,
            subtitulo=None, titulo_proprio=False):
    dados = [m for m in MODULOS if m[0] == arquivo]
    if dados:
        _a, num, tit, _curto, uni = dados[0]
        titulo = titulo or tit
        chapeu = chapeu if chapeu is not None else 'Módulo %d · %s' % (num, uni)
    else:
        titulo = titulo or arquivo
        chapeu = chapeu or ''

    lateral = ''
    if secoes:
        itens = '\n'.join(
            '    <li><a href="#s%d">%d. %s</a></li>' % (j + 1, j + 1, t)
            for j, t in enumerate(secoes))
        lateral = ('\n<aside class="lateral">\n  <h4>Neste módulo</h4>\n'
                   '  <ol>\n%s\n  </ol>\n</aside>\n' % itens)

    pag = CABECA.format(
        titulo=titulo, h1=titulo, versao=VERSAO, menu=menu(arquivo),
        lateral=lateral,
        chapeu='  <p class="chapeu">%s</p>\n' % chapeu if chapeu else '',
        subtitulo='  <p class="subtitulo">%s</p>' % subtitulo if subtitulo else '',
        corpo=corpo, nav=navegacao(arquivo))
    if titulo_proprio:
        pag = pag.replace('  <h1>%s</h1>\n' % titulo, '', 1)
    (RAIZ / arquivo).write_text(pag, encoding='utf-8')
    print('%s escrito (%d caracteres)' % (arquivo, len(pag)))
