import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

# Configuração da figura
fig, ax = plt.subplots(1, 1, figsize=(14, 12))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

# Cores
cor_exploracao = '#22c55e'  # Verde
cor_backtrack = '#ef4444'   # Vermelho
cor_novo_galho = '#3b82f6'  # Azul
cor_neutro = '#6b7280'      # Cinza
cor_beco = '#fee2e2'        # Vermelho claro
cor_solucao = '#dcfce7'     # Verde claro
cor_no_ativo = '#dbeafe'    # Azul claro

# Posições dos nós
# Nível 0 (raiz)
raiz = (5, 11)

# Nível 1
a1 = (3, 9)
a2 = (5, 9)
a3 = (7, 9)

# Nível 2 (a partir de A2)
b1 = (4, 7)
b2 = (5, 7)
b3 = (6, 7)

# Nível 3 (a partir de B1)
c1 = (3.5, 5)
c2 = (4, 5)
c3 = (4.5, 5)

# Nível 4 (a partir de C2)
d1 = (3.5, 3)
d2 = (4, 3)
d3 = (4.5, 3)

# Desenhar arestas neutras primeiro
# Nível 0 → 1
ax.plot([raiz[0], a1[0]], [raiz[1], a1[1]], color=cor_neutro, linewidth=2, zorder=1)
ax.plot([raiz[0], a3[0]], [raiz[1], a3[1]], color=cor_neutro, linewidth=2, zorder=1)

# Nível 1 → 2 (a partir de A2)
ax.plot([a2[0], b2[0]], [a2[1], b2[1]], color=cor_neutro, linewidth=2, zorder=1)
ax.plot([a2[0], b3[0]], [a2[1], b3[1]], color=cor_neutro, linewidth=2, zorder=1)

# Nível 2 → 3 (a partir de B1)
ax.plot([b1[0], c2[0]], [b1[1], c2[1]], color=cor_neutro, linewidth=2, zorder=1)
ax.plot([b1[0], c3[0]], [b1[1], c3[1]], color=cor_neutro, linewidth=2, zorder=1)

# Nível 3 → 4 (a partir de C2)
ax.plot([c2[0], d1[0]], [c2[1], d1[1]], color=cor_neutro, linewidth=2, zorder=1)
ax.plot([c2[0], d3[0]], [c2[1], d3[1]], color=cor_neutro, linewidth=2, zorder=1)

# Desenhar caminho de exploração (verde)
ax.plot([raiz[0], a2[0]], [raiz[1], a2[1]], color=cor_exploracao, linewidth=4, zorder=2)
ax.plot([a2[0], b1[0]], [a2[1], b1[1]], color=cor_exploracao, linewidth=4, zorder=2)
ax.plot([b1[0], c1[0]], [b1[1], c1[1]], color=cor_exploracao, linewidth=4, zorder=2)

# Desenhar backtrack (seta pontilhada vermelha)
arrow_backtrack = FancyArrowPatch(
    (c1[0], c1[1] - 0.3),
    (b1[0], b1[1] + 0.2),
    arrowstyle='->',
    color=cor_backtrack,
    linewidth=3,
    linestyle='--',
    zorder=3,
    mutation_scale=20
)
ax.add_patch(arrow_backtrack)

# Desenhar novo galho após backtrack (azul)
ax.plot([b1[0], c2[0]], [b1[1], c2[1]], color=cor_novo_galho, linewidth=4, zorder=2)
ax.plot([c2[0], d2[0]], [c2[1], d2[1]], color=cor_novo_galho, linewidth=4, zorder=2)

# Desenhar nós
# Nó raiz
circle_raiz = Circle(raiz, 0.3, color='white', ec='#374151', linewidth=3, zorder=4)
ax.add_patch(circle_raiz)
ax.text(raiz[0], raiz[1], 'Início', ha='center', va='center', fontsize=12, fontweight='bold', zorder=5)

# Nível 1
circle_a1 = Circle(a1, 0.25, color='white', ec='#374151', linewidth=2, zorder=4)
ax.add_patch(circle_a1)
ax.text(a1[0], a1[1], 'A1', ha='center', va='center', fontsize=11, zorder=5)

circle_a2 = Circle(a2, 0.25, color=cor_no_ativo, ec=cor_novo_galho, linewidth=3, zorder=4)
ax.add_patch(circle_a2)
ax.text(a2[0], a2[1], 'A2', ha='center', va='center', fontsize=11, zorder=5)

circle_a3 = Circle(a3, 0.25, color='white', ec='#374151', linewidth=2, zorder=4)
ax.add_patch(circle_a3)
ax.text(a3[0], a3[1], 'A3', ha='center', va='center', fontsize=11, zorder=5)

# Nível 2
circle_b1 = Circle(b1, 0.25, color=cor_no_ativo, ec=cor_novo_galho, linewidth=3, zorder=4)
ax.add_patch(circle_b1)
ax.text(b1[0], b1[1], 'B1', ha='center', va='center', fontsize=11, zorder=5)

circle_b2 = Circle(b2, 0.25, color='white', ec='#374151', linewidth=2, zorder=4)
ax.add_patch(circle_b2)
ax.text(b2[0], b2[1], 'B2', ha='center', va='center', fontsize=11, zorder=5)

circle_b3 = Circle(b3, 0.25, color='white', ec='#374151', linewidth=2, zorder=4)
ax.add_patch(circle_b3)
ax.text(b3[0], b3[1], 'B3', ha='center', va='center', fontsize=11, zorder=5)

# Nível 3
circle_c1 = Circle(c1, 0.25, color=cor_beco, ec=cor_backtrack, linewidth=3, zorder=4)
ax.add_patch(circle_c1)
ax.text(c1[0], c1[1], 'X', ha='center', va='center', fontsize=14, fontweight='bold', color=cor_backtrack, zorder=5)

circle_c2 = Circle(c2, 0.25, color='white', ec='#374151', linewidth=2, zorder=4)
ax.add_patch(circle_c2)
ax.text(c2[0], c2[1], 'C2', ha='center', va='center', fontsize=11, zorder=5)

circle_c3 = Circle(c3, 0.25, color='white', ec='#374151', linewidth=2, zorder=4)
ax.add_patch(circle_c3)
ax.text(c3[0], c3[1], 'C3', ha='center', va='center', fontsize=11, zorder=5)

# Nível 4
circle_d1 = Circle(d1, 0.25, color='white', ec='#374151', linewidth=2, zorder=4)
ax.add_patch(circle_d1)
ax.text(d1[0], d1[1], 'D1', ha='center', va='center', fontsize=11, zorder=5)

circle_d2 = Circle(d2, 0.25, color=cor_solucao, ec=cor_exploracao, linewidth=3, zorder=4)
ax.add_patch(circle_d2)
ax.text(d2[0], d2[1], '✓', ha='center', va='center', fontsize=18, color=cor_exploracao, fontweight='bold', zorder=5)

circle_d3 = Circle(d3, 0.25, color='white', ec='#374151', linewidth=2, zorder=4)
ax.add_patch(circle_d3)
ax.text(d3[0], d3[1], 'D3', ha='center', va='center', fontsize=11, zorder=5)

# Anotações
ax.text(raiz[0], raiz[1] + 0.6, 'Árvore de Busca - Backtracking', 
        ha='center', va='bottom', fontsize=16, fontweight='bold', color='#1f2937')

ax.text(3.5, 8, 'Exploração', ha='center', va='center', 
        fontsize=11, fontweight='bold', color=cor_exploracao, 
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

ax.text(2.5, 6, 'Backtrack', ha='center', va='center', 
        fontsize=11, fontweight='bold', color=cor_backtrack,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

ax.text(4.5, 6, 'Novo Galho', ha='center', va='center', 
        fontsize=11, fontweight='bold', color=cor_novo_galho,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

# Legenda
legenda_x = 1.5
legenda_y = 8.5
legenda_altura = 3

# Caixa da legenda
legenda_box = FancyBboxPatch(
    (legenda_x - 0.3, legenda_y - 0.3),
    2.6,
    legenda_altura,
    boxstyle="round,pad=0.2",
    facecolor='#f9fafb',
    edgecolor='#d1d5db',
    linewidth=2,
    zorder=3
)
ax.add_patch(legenda_box)

ax.text(legenda_x, legenda_y + legenda_altura - 0.5, 'Legenda:', 
        ha='left', va='top', fontsize=13, fontweight='bold', color='#374151')

# Linha de exploração
ax.plot([legenda_x, legenda_x + 0.4], [legenda_y + legenda_altura - 0.9, legenda_y + legenda_altura - 0.9], 
        color=cor_exploracao, linewidth=4)
ax.text(legenda_x + 0.5, legenda_y + legenda_altura - 0.9, 'Exploração (caminho atual)', 
        ha='left', va='center', fontsize=10, color='#374151')

# Linha de backtrack
ax.plot([legenda_x, legenda_x + 0.4], [legenda_y + legenda_altura - 1.3, legenda_y + legenda_altura - 1.3], 
        color=cor_backtrack, linewidth=3, linestyle='--')
ax.text(legenda_x + 0.5, legenda_y + legenda_altura - 1.3, 'Backtrack (retrocesso)', 
        ha='left', va='center', fontsize=10, color='#374151')

# Linha de novo galho
ax.plot([legenda_x, legenda_x + 0.4], [legenda_y + legenda_altura - 1.7, legenda_y + legenda_altura - 1.7], 
        color=cor_novo_galho, linewidth=4)
ax.text(legenda_x + 0.5, legenda_y + legenda_altura - 1.7, 'Novo galho (após backtrack)', 
        ha='left', va='center', fontsize=10, color='#374151')

# Beco sem saída
circle_legenda_beco = Circle((legenda_x + 0.2, legenda_y + legenda_altura - 2.1), 0.15, 
                             color=cor_beco, ec=cor_backtrack, linewidth=2)
ax.add_patch(circle_legenda_beco)
ax.text(legenda_x + 0.2, legenda_y + legenda_altura - 2.1, 'X', ha='center', va='center', 
        fontsize=10, fontweight='bold', color=cor_backtrack)
ax.text(legenda_x + 0.5, legenda_y + legenda_altura - 2.1, 'Beco sem saída', 
        ha='left', va='center', fontsize=10, color='#374151')

# Solução encontrada
circle_legenda_sol = Circle((legenda_x + 0.2, legenda_y + legenda_altura - 2.5), 0.15, 
                            color=cor_solucao, ec=cor_exploracao, linewidth=2)
ax.add_patch(circle_legenda_sol)
ax.text(legenda_x + 0.2, legenda_y + legenda_altura - 2.5, '✓', ha='center', va='center', 
        fontsize=12, color=cor_exploracao, fontweight='bold')
ax.text(legenda_x + 0.5, legenda_y + legenda_altura - 2.5, 'Solução encontrada', 
        ha='left', va='center', fontsize=10, color='#374151')

plt.tight_layout()
plt.show()

