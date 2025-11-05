import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np

# Configuração do tabuleiro
TAMANHO = 8
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.set_xlim(-0.5, TAMANHO - 0.5)
ax.set_ylim(-0.5, TAMANHO - 0.5)
ax.set_aspect('equal')
ax.axis('off')

# Cores
cor_casa_branca = '#f0d9b5'
cor_casa_preta = '#b58863'
cor_rainha = '#d32f2f'
cor_rainha_valida = '#1976d2'
cor_conflito = '#ff5252'
cor_exploracao = '#4caf50'
cor_backtrack = '#ff9800'

# Estado do algoritmo
tabuleiro = [-1] * TAMANHO  # -1 significa sem rainha
linha_atual = 0
historico = []  # Para armazenar o histórico de estados
solucao_encontrada = False
texto_info = None
texto_stats = None
rainhas_patches = []  # Lista para armazenar patches das rainhas

def desenhar_tabuleiro():
    """Desenha o tabuleiro de xadrez"""
    for i in range(TAMANHO):
        for j in range(TAMANHO):
            cor = cor_casa_branca if (i + j) % 2 == 0 else cor_casa_preta
            rect = patches.Rectangle((j - 0.5, TAMANHO - 1 - i - 0.5), 1, 1,
                                    linewidth=1, edgecolor='black', facecolor=cor)
            ax.add_patch(rect)

def verificar_conflito(tabuleiro, linha, coluna):
    """Verifica se há conflito ao colocar uma rainha na posição (linha, coluna)"""
    for i in range(linha):
        if tabuleiro[i] == coluna:  # Mesma coluna
            return True
        if abs(tabuleiro[i] - coluna) == abs(i - linha):  # Mesma diagonal
            return True
    return False

def desenhar_rainhas(tabuleiro, linha_atual, destacar_conflito=None, coluna_testando=None):
    """Desenha as rainhas no tabuleiro"""
    # Remove rainhas antigas
    for patch in rainhas_patches:
        patch.remove()
    rainhas_patches.clear()
    
    # Remove textos antigos de rainhas
    textos_para_remover = []
    for text in ax.texts:
        if hasattr(text, '_eh_rainha'):
            textos_para_remover.append(text)
    for text in textos_para_remover:
        text.remove()
    
    # Desenha as rainhas
    for linha in range(TAMANHO):
        if tabuleiro[linha] != -1:
            coluna = tabuleiro[linha]
            x = coluna
            y = TAMANHO - 1 - linha
            
            # Cor depende do estado
            if linha == linha_atual and destacar_conflito and coluna == coluna_testando:
                cor = cor_conflito  # Conflito
            elif linha < linha_atual:
                cor = cor_rainha_valida  # Rainha válida
            else:
                cor = cor_rainha  # Rainha sendo testada
            
            # Desenha a rainha
            circle = patches.Circle((x, y), 0.35, color=cor, ec='black', linewidth=2, zorder=10)
            ax.add_patch(circle)
            rainhas_patches.append(circle)
            
            # Símbolo de rainha
            texto = ax.text(x, y, '♛', ha='center', va='center', fontsize=20, 
                   color='white', fontweight='bold', zorder=11)
            texto._eh_rainha = True
            rainhas_patches.append(texto)
        
        # Mostra posição sendo testada (mesmo sem rainha)
        elif linha == linha_atual and coluna_testando is not None and tabuleiro[linha] == -1:
            x = coluna_testando
            y = TAMANHO - 1 - linha
            # Desenha círculo transparente para indicar teste
            circle = patches.Circle((x, y), 0.35, color=cor_rainha, 
                                   ec='black', linewidth=2, alpha=0.5, zorder=9)
            ax.add_patch(circle)
            rainhas_patches.append(circle)
            texto = ax.text(x, y, '?', ha='center', va='center', fontsize=16, 
                   color='black', fontweight='bold', zorder=10, alpha=0.7)
            texto._eh_rainha = True
            rainhas_patches.append(texto)

def atualizar_info(texto, cor='black'):
    """Atualiza o texto informativo"""
    global texto_info
    if texto_info:
        texto_info.remove()
    texto_info = ax.text(TAMANHO/2 - 0.5, -1.2, texto, 
                        ha='center', va='top', fontsize=14, 
                        fontweight='bold', color=cor,
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8))

def atualizar_stats(iteracao, backtrack_count):
    """Atualiza estatísticas"""
    global texto_stats
    if texto_stats:
        texto_stats.remove()
    stats = f"Iteração: {iteracao} | Backtracks: {backtrack_count}"
    texto_stats = ax.text(TAMANHO/2 - 0.5, TAMANHO + 0.3, stats,
                         ha='center', va='bottom', fontsize=12,
                         bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7))

# Estado da animação
frame_atual = 0
iteracao = 0
backtrack_count = 0
etapas = []
etapa_atual = 0

def resolver_8_rainhas():
    """Resolve o problema das 8 rainhas usando backtracking"""
    global tabuleiro, linha_atual, etapas, iteracao, backtrack_count
    
    # Algoritmo de backtracking
    linha = 0
    coluna = 0
    
    while linha >= 0 and linha < TAMANHO:
        encontrou = False
        
        # Tenta colocar rainha na linha atual
        while coluna < TAMANHO:
            iteracao += 1
            
            # Salva estado antes de tentar
            tab_antes = tabuleiro.copy()
            
            # Mostra tentativa primeiro
            etapas.append({
                'tipo': 'tentar',
                'linha': linha,
                'coluna': coluna,
                'tabuleiro': tab_antes.copy(),
                'iteracao': iteracao
            })
            
            # Verifica se pode colocar rainha
            if not verificar_conflito(tabuleiro, linha, coluna):
                tabuleiro[linha] = coluna
                etapas.append({
                    'tipo': 'colocar',
                    'linha': linha,
                    'coluna': coluna,
                    'tabuleiro': tabuleiro.copy(),
                    'iteracao': iteracao
                })
                encontrou = True
                coluna = 0  # Reseta para próxima linha
                break
            else:
                # Conflito detectado
                etapas.append({
                    'tipo': 'conflito',
                    'linha': linha,
                    'coluna': coluna,
                    'tabuleiro': tab_antes.copy(),
                    'iteracao': iteracao
                })
            
            coluna += 1
        
        if encontrou:
            # Avança para próxima linha
            linha += 1
            if linha == TAMANHO:
                # Solução encontrada!
                etapas.append({
                    'tipo': 'solucao',
                    'tabuleiro': tabuleiro.copy(),
                    'iteracao': iteracao
                })
                break
        else:
            # Backtrack
            backtrack_count += 1
            etapas.append({
                'tipo': 'backtrack',
                'linha': linha,
                'tabuleiro': tabuleiro.copy(),
                'iteracao': iteracao
            })
            
            # Remove rainha da linha atual
            if tabuleiro[linha] != -1:
                coluna_anterior = tabuleiro[linha]
                tabuleiro[linha] = -1
                linha -= 1
                if linha >= 0:
                    coluna = tabuleiro[linha] + 1
                    tabuleiro[linha] = -1
                else:
                    break
            else:
                linha -= 1
                if linha >= 0:
                    coluna = tabuleiro[linha] + 1
                    tabuleiro[linha] = -1

# Preparar animação
desenhar_tabuleiro()

# Resolve o problema e gera etapas
resolver_8_rainhas()

max_frames = len(etapas) * 3  # 3 frames por etapa para animação suave

def animar(frame):
    global etapa_atual, tabuleiro, linha_atual
    
    if etapa_atual >= len(etapas):
        etapa_atual = 0  # Reinicia a animação
        frame = 0
    
    # Determina qual etapa mostrar baseado no frame
    etapa_idx = min(frame // 3, len(etapas) - 1)
    
    if etapa_idx != etapa_atual:
        etapa_atual = etapa_idx
        etapa = etapas[etapa_atual]
        tabuleiro = etapa['tabuleiro'].copy()
        
        # Atualiza visualização
        if etapa['tipo'] == 'tentar':
            linha_atual = etapa['linha']
            atualizar_info(f"Tentando colocar rainha na linha {etapa['linha']+1}, coluna {etapa['coluna']+1}", 'blue')
            desenhar_rainhas(tabuleiro, linha_atual, destacar_conflito=False, coluna_testando=etapa['coluna'])
        
        elif etapa['tipo'] == 'conflito':
            linha_atual = etapa['linha']
            atualizar_info(f"✗ Conflito! Linha {etapa['linha']+1}, coluna {etapa['coluna']+1} não pode ser usada", 'red')
            desenhar_rainhas(tabuleiro, linha_atual, destacar_conflito=True, coluna_testando=etapa['coluna'])
        
        elif etapa['tipo'] == 'colocar':
            linha_atual = etapa['linha']
            atualizar_info(f"✓ Rainha colocada na linha {etapa['linha']+1}, coluna {etapa['coluna']+1}", 'green')
            desenhar_rainhas(tabuleiro, linha_atual, destacar_conflito=False)
        
        elif etapa['tipo'] == 'backtrack':
            linha_atual = etapa['linha']
            atualizar_info(f"⏪ Backtrack! Voltando para linha {etapa['linha']}", 'orange')
            desenhar_rainhas(tabuleiro, linha_atual, destacar_conflito=False)
        
        elif etapa['tipo'] == 'solucao':
            linha_atual = TAMANHO
            atualizar_info("🎉 SOLUÇÃO ENCONTRADA! 🎉", 'green')
            desenhar_rainhas(tabuleiro, linha_atual, destacar_conflito=False)
        
        atualizar_stats(etapa['iteracao'], backtrack_count)

# Criar animação
anim = FuncAnimation(fig, animar, frames=max_frames, interval=500, 
                     repeat=True, blit=False)

plt.title('Problema das 8 Rainhas - Backtracking Animado', 
          fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.show()

print(f"\nSolução encontrada após {iteracao} iterações e {backtrack_count} backtracks!")
print(f"Posições das rainhas (linha, coluna):")
for i, col in enumerate(tabuleiro):
    print(f"  Linha {i+1}: Coluna {col+1}")

