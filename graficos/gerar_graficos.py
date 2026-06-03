import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append("../parte1_otimizacao_continua")

from funcao import *

funcoes = [
    ("Quadratica", funcao_quadratica, -100, 100),
    ("Gaussiana",  funcao_gaussiana, -2, 5),
    ("Ackley",     funcao_ackley, -8, 8),
    ("Rastrigin",  funcao_rastrigin, -5.12, 5.12),
    ("Mista",      funcao_mista, -10, 10),
    ("Seno",       funcao_seno, -1, 3),
]

for nome, f, x_min, x_max in funcoes:
    x1 = np.linspace(x_min, x_max, 80)
    x2 = np.linspace(x_min, x_max, 80)
    X1, X2 = np.meshgrid(x1, x2)
    Z = f(X1, X2)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X1, X2, Z, cmap="viridis", edgecolor="none")
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_zlabel("f(x1, x2)")
    ax.set_title(f"{nome}")
    plt.tight_layout()
    plt.savefig(f"{nome.lower()}.png", dpi=150)
    plt.close()
    print(f"OK: graficos/{nome.lower()}.png")
