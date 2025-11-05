import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.animation import FuncAnimation
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
raiz = (5, 11)
a1 = (3, 9)
a2 = (5, 9)
a3 = (7, 9)
b1 = (4, 7)
b2 = (5, 7)
b3 = (6, 7)
c1 = (3.5, 5)
c2 = (4, 5)
c3 = (4.5, 5)
d1 = (3.5, 3)
d2 = (4, 3)
d3 = (4.5, 3)

# Listas para armazenar elementos animados
linhas_exploracao = []
linhas_backtrack = []
linhas_novo_galho = []
circulos_ativos = []
textos_info = []

# Título
titulo = ax.text(5, 11.8, 'Árvore de Busca - Backtracking', 
                 ha='center', va='bottom', fontsize=16, fontweight='bold', color='#1f2937')

# Função para desenhar a estrutura base da árvore
def desenhar_estrutura_base():
    # Arestas neutras
    ax.plot([raiz[0], a1[0]], [raiz[1], a1[1]], color=cor_neutro, linewidth=2, alpha=0.3, zorder=1)
    ax.plot([raiz[0], a3[0]], [raiz[1], a3[1]], color=cor_neutro, linewidth=2, alpha=0.3, zorder=1)
    ax.plot([a2[0], b2[0]], [a2[1], b2[1]], color=cor_neutro, linewidth=2, alpha=0.3, zorder=1)
    ax.plot([a2[0], b3[0]], [a2[1], b3[1]], color=cor_neutro, linewidth=2, alpha=0.3, zorder=1)
    ax.plot([b1[0], c2[0]], [b1[1], c2[1]], color=cor_neutro, linewidth=2, alpha=0.3, zorder=1)
    ax.plot([b1[0], c3[0]], [b1[1], c3[1]], color=cor_neutro, linewidth=2, alpha=0.3, zorder=1)
    ax.plot([c2[0], d1[0]], [c2[1], d1[1]], color=cor_neutro, linewidth=2, alpha=0.3, zorder=1)
    ax.plot([c2[0], d3[0]], [c2[1], d3[1]], color=cor_neutro, linewidth=2, alpha=0.3, zorder=1)
    
    # Todos os nós (inicialmente desativados)
    nos = [
        (raiz, 'Início', 'white', '#374151', 3),
        (a1, 'A1', 'white', '#374151', 2),
        (a2, 'A2', 'white', '#374151', 2),
        (a3, 'A3', 'white', '#374151', 2),
        (b1, 'B1', 'white', '#374151', 2),
        (b2, 'B2', 'white', '#374151', 2),
        (b3, 'B3', 'white', '#374151', 2),
        (c1, 'C1', 'white', '#374151', 2),
        (c2, 'C2', 'white', '#374151', 2),
        (c3, 'C3', 'white', '#374151', 2),
        (d1, 'D1', 'white', '#374151', 2),
        (d2, 'D2', 'white', '#374151', 2),
        (d3, 'D3', 'white', '#374151', 2),
    ]
    
    for pos, label, cor, borda, lw in nos:
        circle = Circle(pos, 0.25, color=cor, ec=borda, linewidth=lw, zorder=4)
        ax.add_patch(circle)
        if label == 'C1':
            text = ax.text(pos[0], pos[1], 'X', ha='center', va='center', 
                          fontsize=14, fontweight='bold', color='#ef4444', zorder=5, alpha=0.3)
        elif label == 'D2':
            text = ax.text(pos[0], pos[1], '✓', ha='center', va='center', 
                          fontsize=18, color='#22c55e', fontweight='bold', zorder=5, alpha=0.3)
        else:
            text = ax.text(pos[0], pos[1], label, ha='center', va='center', 
                          fontsize=11, zorder=5, alpha=0.3)
    
    # Legenda
    legenda_x = 1.5
    legenda_y = 8.5
    legenda_altura = 3
    
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
    
    ax.plot([legenda_x, legenda_x + 0.4], [legenda_y + legenda_altura - 0.9, legenda_y + legenda_altura - 0.9], 
            color=cor_exploracao, linewidth=4)
    ax.text(legenda_x + 0.5, legenda_y + legenda_altura - 0.9, 'Exploração', 
            ha='left', va='center', fontsize=10, color='#374151')
    
    ax.plot([legenda_x, legenda_x + 0.4], [legenda_y + legenda_altura - 1.3, legenda_y + legenda_altura - 1.3], 
            color=cor_backtrack, linewidth=3, linestyle='--')
    ax.text(legenda_x + 0.5, legenda_y + legenda_altura - 1.3, 'Backtrack', 
            ha='left', va='center', fontsize=10, color='#374151')
    
    ax.plot([legenda_x, legenda_x + 0.4], [legenda_y + legenda_altura - 1.7, legenda_y + legenda_altura - 1.7], 
            color=cor_novo_galho, linewidth=4)
    ax.text(legenda_x + 0.5, legenda_y + legenda_altura - 1.7, 'Novo galho', 
            ha='left', va='center', fontsize=10, color='#374151')
    
    circle_legenda_beco = Circle((legenda_x + 0.2, legenda_y + legenda_altura - 2.1), 0.15, 
                                 color=cor_beco, ec=cor_backtrack, linewidth=2)
    ax.add_patch(circle_legenda_beco)
    ax.text(legenda_x + 0.2, legenda_y + legenda_altura - 2.1, 'X', ha='center', va='center', 
            fontsize=10, fontweight='bold', color=cor_backtrack)
    ax.text(legenda_x + 0.5, legenda_y + legenda_altura - 2.1, 'Beco sem saída', 
            ha='left', va='center', fontsize=10, color='#374151')
    
    circle_legenda_sol = Circle((legenda_x + 0.2, legenda_y + legenda_altura - 2.5), 0.15, 
                                color=cor_solucao, ec=cor_exploracao, linewidth=2)
    ax.add_patch(circle_legenda_sol)
    ax.text(legenda_x + 0.2, legenda_y + legenda_altura - 2.5, '✓', ha='center', va='center', 
            fontsize=12, color=cor_exploracao, fontweight='bold')
    ax.text(legenda_x + 0.5, legenda_y + legenda_altura - 2.5, 'Solução encontrada', 
            ha='left', va='center', fontsize=10, color='#374151')

desenhar_estrutura_base()

def atualizar_no(pos, label, cor, borda, lw=3):
    """Atualiza ou cria um nó"""
    # Remove círculo antigo se existir
    for circle in circulos_ativos[:]:
        if hasattr(circle, '_pos') and circle._pos == pos:
            circle.remove()
            circulos_ativos.remove(circle)
            break
    
    # Remove texto antigo
    textos_para_remover = []
    for text in ax.texts:
        if hasattr(text, '_pos') and text._pos == pos:
            textos_para_remover.append(text)
    for text in textos_para_remover:
        text.remove()
    
    # Cria novo círculo
    circle = Circle(pos, 0.25, color=cor, ec=borda, linewidth=lw, zorder=4)
    circle._pos = pos
    ax.add_patch(circle)
    circulos_ativos.append(circle)
    
    # Cria novo texto
    if label == 'X':
        text = ax.text(pos[0], pos[1], 'X', ha='center', va='center', 
                      fontsize=14, fontweight='bold', color=cor_backtrack, zorder=5)
    elif label == '✓':
        text = ax.text(pos[0], pos[1], '✓', ha='center', va='center', 
                      fontsize=18, color=cor_exploracao, fontweight='bold', zorder=5)
    else:
        text = ax.text(pos[0], pos[1], label, ha='center', va='center', 
                      fontsize=11, zorder=5)
    text._pos = pos

# Ativar nó raiz inicialmente
atualizar_no(raiz, 'Início', 'white', '#374151', 3)

# Fases da animação
fases = [
    {'tipo': 'info', 'texto': 'Fase 1: Início da busca', 'frame': 0},
    {'tipo': 'exploracao', 'de': raiz, 'para': a2, 'frame': 20},
    {'tipo': 'ativar_no', 'pos': a2, 'label': 'A2', 'cor': cor_no_ativo, 'borda': cor_novo_galho, 'frame': 30},
    {'tipo': 'info', 'texto': 'Fase 2: Explorando nó A2', 'frame': 35},
    {'tipo': 'exploracao', 'de': a2, 'para': b1, 'frame': 50},
    {'tipo': 'ativar_no', 'pos': b1, 'label': 'B1', 'cor': cor_no_ativo, 'borda': cor_novo_galho, 'frame': 60},
    {'tipo': 'info', 'texto': 'Fase 3: Explorando nó B1', 'frame': 65},
    {'tipo': 'exploracao', 'de': b1, 'para': c1, 'frame': 80},
    {'tipo': 'ativar_no', 'pos': c1, 'label': 'X', 'cor': cor_beco, 'borda': cor_backtrack, 'frame': 90},
    {'tipo': 'info', 'texto': 'Fase 4: Beco sem saída encontrado!', 'frame': 95},
    {'tipo': 'backtrack', 'de': c1, 'para': b1, 'frame': 110},
    {'tipo': 'desativar_no', 'pos': c1, 'frame': 125},
    {'tipo': 'info', 'texto': 'Fase 5: Backtrack - voltando para B1', 'frame': 130},
    {'tipo': 'novo_galho', 'de': b1, 'para': c2, 'frame': 145},
    {'tipo': 'ativar_no', 'pos': c2, 'label': 'C2', 'cor': cor_no_ativo, 'borda': cor_novo_galho, 'frame': 155},
    {'tipo': 'info', 'texto': 'Fase 6: Tentando novo caminho (C2)', 'frame': 160},
    {'tipo': 'novo_galho', 'de': c2, 'para': d2, 'frame': 175},
    {'tipo': 'ativar_no', 'pos': d2, 'label': '✓', 'cor': cor_solucao, 'borda': cor_exploracao, 'frame': 185},
    {'tipo': 'info', 'texto': 'Fase 7: Solução encontrada! ✓', 'frame': 190},
]

# Preparar estrutura para animação
frame_atual = 0
max_frames = 250

def animar(frame):
    global frame_atual
    
    # Processar fases baseado no frame atual
    for fase in fases:
        if fase['frame'] == frame:
            if fase['tipo'] == 'exploracao':
                linha = ax.plot([fase['de'][0], fase['para'][0]], 
                               [fase['de'][1], fase['para'][1]], 
                               color=cor_exploracao, linewidth=4, zorder=2)[0]
                linhas_exploracao.append(linha)
            
            elif fase['tipo'] == 'backtrack':
                arrow = FancyArrowPatch(
                    (fase['de'][0], fase['de'][1] - 0.3),
                    (fase['para'][0], fase['para'][1] + 0.2),
                    arrowstyle='->',
                    color=cor_backtrack,
                    linewidth=3,
                    linestyle='--',
                    zorder=3,
                    mutation_scale=20
                )
                ax.add_patch(arrow)
                linhas_backtrack.append(arrow)
            
            elif fase['tipo'] == 'novo_galho':
                linha = ax.plot([fase['de'][0], fase['para'][0]], 
                               [fase['de'][1], fase['para'][1]], 
                               color=cor_novo_galho, linewidth=4, zorder=2)[0]
                linhas_novo_galho.append(linha)
            
            elif fase['tipo'] == 'ativar_no':
                atualizar_no(fase['pos'], fase['label'], fase['cor'], fase['borda'])
            
            elif fase['tipo'] == 'desativar_no':
                for circle in circulos_ativos[:]:
                    if hasattr(circle, '_pos') and circle._pos == fase['pos']:
                        circle.set_alpha(0.3)
                        circle.set_edgecolor('#6b7280')
                        circle.set_linewidth(2)
                        break
            
            elif fase['tipo'] == 'info':
                # Remove texto anterior
                for text in textos_info:
                    text.remove()
                textos_info.clear()
                
                # Adiciona novo texto
                texto = ax.text(5, 0.5, fase['texto'], 
                               ha='center', va='bottom', 
                               fontsize=14, fontweight='bold', 
                               color='#1f2937',
                               bbox=dict(boxstyle='round,pad=0.5', 
                                       facecolor='yellow', alpha=0.8),
                               zorder=10)
                textos_info.append(texto)
    
    return []

# Criar animação
anim = FuncAnimation(fig, animar, frames=max_frames, interval=100, 
                     repeat=True, blit=False)

plt.tight_layout()
plt.show()

