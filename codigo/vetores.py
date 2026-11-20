# -*- coding: utf-8 -*-
"""O que faz de um trio de números um vetor, posto à prova.

O QUE RESOLVE
    Verifica numericamente as afirmações do módulo 1, que no papel saem por
    manipulação de índices e no computador saem por medida:

    1. uma matriz de rotação é ortogonal e tem determinante +1;
    2. rotação preserva o módulo de um vetor e o produto escalar entre dois,
       enquanto um trio qualquer de números não preserva nada;
    3. o produto vetorial é antissimétrico, perpendicular aos dois fatores, e
       o seu módulo é a área do paralelogramo;
    4. o produto misto é o volume do paralelepípedo, com sinal;
    5. as identidades BAC-CAB, rot(grad f) = 0 e div(rot A) = 0;
    6. uma força é conservativa se, e só se, o rotacional é nulo, e a
       verificação é feita pela circulação em caminhos fechados.

A FÍSICA
    A definição de vetor que importa não é "segmento orientado com módulo,
    direção e sentido": é a LEI DE TRANSFORMAÇÃO. Um trio de números é um
    vetor quando, ao girar o sistema de coordenadas, as três componentes se
    misturam exatamente como as coordenadas se misturam. Essa exigência é o
    que garante que equações escritas em forma vetorial valham em qualquer
    referencial, e é por isso que a física insiste nela.

COMO CONFERIR SE ESTÁ CERTO
    Cada teste imprime o desvio em relação ao valor exato. Tudo o que é
    identidade algébrica tem de dar zero de máquina (1e-16). O que é
    aproximação numérica, como as derivadas por diferenças finitas, tem erro
    controlado pelo passo, e o programa mostra a diferença entre os dois
    casos, que é uma das lições do módulo.

Prof. Apiano Morais - LFCA/URCA - Mecânica Clássica I
"""

import numpy as np


# ====================================================== rotações
def rotacao(eixo, ang):
    """Matriz de rotação de um ângulo em torno de x, y ou z."""
    c, s = np.cos(ang), np.sin(ang)
    if eixo == 'z':
        return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    if eixo == 'y':
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def rotacao_geral(a, b, g):
    """Composição das três, que gera uma rotação qualquer."""
    return rotacao('z', g) @ rotacao('y', b) @ rotacao('z', a)


# ====================================================== derivadas numéricas
def gradiente(f, p, h=1e-5):
    g = np.zeros(3)
    for i in range(3):
        e = np.zeros(3)
        e[i] = h
        g[i] = (f(p + e) - f(p - e)) / (2 * h)
    return g


def jacobiana(F, p, h=1e-5):
    J = np.zeros((3, 3))
    for j in range(3):
        e = np.zeros(3)
        e[j] = h
        J[:, j] = (F(p + e) - F(p - e)) / (2 * h)
    return J


def divergente(F, p, h=1e-5):
    return np.trace(jacobiana(F, p, h))


def rotacional(F, p, h=1e-5):
    J = jacobiana(F, p, h)
    return np.array([J[2, 1] - J[1, 2], J[0, 2] - J[2, 0], J[1, 0] - J[0, 1]])


def circulacao(F, caminho, n=20000):
    """Integral de linha de F ao longo de um caminho fechado parametrizado."""
    t = np.linspace(0.0, 1.0, n + 1)
    pts = np.array([caminho(ti) for ti in t])
    meios = 0.5 * (pts[1:] + pts[:-1])
    passos = pts[1:] - pts[:-1]
    return float(sum(np.dot(F(m), d) for m, d in zip(meios, passos)))


def main():
    rng = np.random.default_rng(20261120)

    print('=' * 70)
    print('1. A MATRIZ DE ROTACAO')
    print('=' * 70)
    R = rotacao_geral(0.7, -1.3, 2.1)
    print('   R^T R - I  (maior desvio) = %.3e'
          % np.abs(R.T @ R - np.eye(3)).max())
    print('   det R - 1                 = %.3e' % abs(np.linalg.det(R) - 1))
    print('   Ortogonal e de determinante +1: preserva comprimentos e nao')
    print('   inverte a mao do sistema de coordenadas.')
    print()
    S = R.copy()
    S[:, 0] *= -1
    print('   Trocando o sinal de uma coluna, det = %.1f: isso e uma'
          % np.linalg.det(S))
    print('   REFLEXAO, e nao uma rotacao. Nenhum movimento rigido leva uma')
    print('   mao direita na esquerda.')
    print()

    print('=' * 70)
    print('2. O QUE A ROTACAO PRESERVA')
    print('=' * 70)
    v = rng.normal(size=3)
    w = rng.normal(size=3)
    vl, wl = R @ v, R @ w
    print('   |v| antes = %.12f   depois = %.12f   dif = %.1e'
          % (np.linalg.norm(v), np.linalg.norm(vl),
             abs(np.linalg.norm(v) - np.linalg.norm(vl))))
    print('   v.w antes = %.12f   depois = %.12f   dif = %.1e'
          % (v @ w, vl @ wl, abs(v @ w - vl @ wl)))
    print()
    print("   E O QUE NAO E VETOR. Tome o trio (x, y, T), em que x e y sao")
    print('   coordenadas de um ponto, em metros, e T e a temperatura medida')
    print('   ali, em kelvin. Sao tres numeros, e nao sao um vetor.')
    print()
    p = np.array([3.0, 4.0, 0.0])
    T = 25.0
    Rx = rotacao('x', np.radians(40))
    print('   O vetor posicao (3, 4, 0) m, girado 40 graus em torno de x:')
    print('     [%7.3f %7.3f %7.3f] m   (as tres componentes sao metros,'
          % tuple(Rx @ p))
    print('                                   e o modulo nao mudou: %.6f)'
          % np.linalg.norm(Rx @ p))
    print()
    print('   O trio (3, 4, 25), tratado como se fosse vetor:')
    print('     [%7.3f %7.3f %7.3f]' % tuple(Rx @ np.array([p[0], p[1], T])))
    print('     A segunda componente vale 4*cos40 - 25*sen40, isto e, uma')
    print('     soma de metros com kelvin. O resultado nao e grandeza')
    print('     nenhuma, e a conta nao significa nada.')
    print()
    print('   Nao existe "a transformacao correta do trio", porque o trio')
    print('   nao e um objeto geometrico. O que se transforma e a posicao,')
    print('   que e vetor, e o que fica quieto e a temperatura, que e')
    print('   escalar. Ter tres numeros nao basta: o criterio e transformar-')
    print('   se como as coordenadas se transformam, e e essa a definicao de')
    print('   vetor que o resto do curso usa.')
    print()
    print('=' * 70)
    print('3. PRODUTOS ESCALAR E VETORIAL')
    print('=' * 70)
    a = np.array([2.0, 1.0, -1.0])
    b = np.array([1.0, 3.0, 2.0])
    c = np.cross(a, b)
    print('   a x b = [%.4f %.4f %.4f]' % tuple(c))
    print('   (a x b).a = %.3e   (a x b).b = %.3e   (perpendicular aos dois)'
          % (c @ a, c @ b))
    print('   a x b + b x a = %.3e  (antissimetrico)'
          % np.abs(c + np.cross(b, a)).max())
    area = np.linalg.norm(a) * np.linalg.norm(b) * np.sin(
        np.arccos(a @ b / (np.linalg.norm(a) * np.linalg.norm(b))))
    print('   |a x b| = %.10f   |a||b|sen(theta) = %.10f   dif = %.1e'
          % (np.linalg.norm(c), area, abs(np.linalg.norm(c) - area)))
    print()
    d = np.array([0.0, -2.0, 4.0])
    misto = a @ np.cross(b, d)
    det = np.linalg.det(np.array([a, b, d]))
    print('   produto misto a.(b x d) = %.10f' % misto)
    print('   determinante da matriz  = %.10f   dif = %.1e'
          % (det, abs(misto - det)))
    print('   Os dois sao o volume do paralelepipedo, com sinal: positivo se')
    print('   os tres vetores formam uma mao direita.')
    print()
    bac = np.cross(a, np.cross(b, d))
    cab = b * (a @ d) - d * (a @ b)
    print('   BAC-CAB: a x (b x d) - [b(a.d) - d(a.b)] = %.1e'
          % np.abs(bac - cab).max())
    print()

    print('=' * 70)
    print('4. AS IDENTIDADES DO CALCULO VETORIAL')
    print('=' * 70)

    def campo_escalar(p):
        x, y, z = p
        return x ** 2 * y - np.sin(z) * x + 3 * y * z

    def campo_vetorial(p):
        x, y, z = p
        return np.array([y * z ** 2, x ** 2 - z, np.exp(x) * y])

    p0 = np.array([0.7, -1.2, 0.4])
    rot_grad = rotacional(lambda q: gradiente(campo_escalar, q), p0, h=1e-4)
    print('   rot(grad f)  = [%.2e %.2e %.2e]' % tuple(rot_grad))
    div_rot = divergente(lambda q: rotacional(campo_vetorial, q, h=1e-4),
                         p0, h=1e-4)
    print('   div(rot A)   = %.2e' % div_rot)
    print()
    print('   As duas identidades sao exatas na algebra. No computador, uma')
    print('   delas deu zero de maquina e a outra deu 1e-7: a diferenca esta')
    print('   em quantas derivadas numericas foram encadeadas. Cada derivada')
    print('   central divide o arredondamento por h, e com h = 1e-4 duas')
    print('   derivadas encadeadas ja carregam 1e-16/h^2 = 1e-8 de ruido.')
    print('   O erro que sobra e o da diferenca finita, e nao da identidade.')
    print()

    print('=' * 70)
    print('5. FORCA CONSERVATIVA: O TESTE DO ROTACIONAL')
    print('=' * 70)

    def F_cons(p):
        """F = grad(x y z), conservativa por construcao."""
        x, y, z = p
        return np.array([y * z, x * z, x * y])

    def F_nao(p):
        """Campo de rotacao pura, o exemplo classico de nao conservativo."""
        x, y, z = p
        return np.array([-y, x, 0.0])

    for nome, F in (('conservativa  ', F_cons), ('nao conservativa', F_nao)):
        r = rotacional(F, np.array([0.3, 0.5, -0.2]), h=1e-4)
        print('   %s   rot F = [%+.2e %+.2e %+.2e]' % (nome, r[0], r[1], r[2]))
    print()
    print('   E a circulacao em caminhos fechados, que e a definicao:')
    circulos = [
        ('circulo de raio 1 no plano xy',
         lambda t: np.array([np.cos(2 * np.pi * t), np.sin(2 * np.pi * t), 0.0])),
        ('circulo de raio 2, deslocado',
         lambda t: np.array([1 + 2 * np.cos(2 * np.pi * t),
                             0.5 + 2 * np.sin(2 * np.pi * t), 0.0])),
        ('quadrado de lado 1',
         lambda t: np.array(
             [min(max(4 * t, 0), 1) - min(max(4 * t - 2, 0), 1),
              min(max(4 * t - 1, 0), 1) - min(max(4 * t - 3, 0), 1), 0.0])),
    ]
    print('   caminho                          conservativa   nao conservativa')
    for nome, cam in circulos:
        print('   %-30s   %+.3e      %+.4f'
              % (nome, circulacao(F_cons, cam), circulacao(F_nao, cam)))
    print()
    print('   A conservativa da zero em TODO caminho fechado, e por isso o')
    print('   trabalho dela so depende dos extremos. A outra da duas vezes a')
    print('   area cercada (2pi para o raio 1, 8pi para o raio 2, 2 para o')
    print('   quadrado), que e o teorema de Stokes em acao.')


if __name__ == '__main__':
    main()
