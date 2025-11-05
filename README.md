# Diagrama Visual de Backtracking

Este projeto contém um diagrama visual que ilustra o conceito de backtracking usando uma árvore de busca.

## Como executar o código Python

### 1. Instalar as dependências

Primeiro, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

Ou instale manualmente:

```bash
pip install matplotlib numpy
```

### 2. Executar o script

#### Versão Estática (sem animação)
Execute o script Python:

```bash
python diagrama_backtracking.py
```

O diagrama será exibido em uma janela gráfica automaticamente.

#### Versão Animada (com movimento)
Execute o script Python animado:

```bash
python diagrama_backtracking_animado.py
```

A animação mostrará as fases do backtracking em sequência:
- **Fase 1**: Início da busca
- **Fase 2**: Explorando nó A2
- **Fase 3**: Explorando nó B1
- **Fase 4**: Beco sem saída encontrado!
- **Fase 5**: Backtrack - voltando para B1
- **Fase 6**: Tentando novo caminho (C2)
- **Fase 7**: Solução encontrada! ✓

A animação se repete automaticamente.

#### Problema das 8 Rainhas Animado
Execute o problema clássico das 8 rainhas:

```bash
python problema_8_rainhas_animado.py
```

Esta animação mostra:
- **Tentativas**: Quando o algoritmo tenta colocar uma rainha em uma posição
- **Conflitos**: Quando uma rainha não pode ser colocada (ataque detectado)
- **Colocação bem-sucedida**: Quando uma rainha é colocada com sucesso
- **Backtrack**: Quando o algoritmo volta para tentar uma posição diferente
- **Solução**: Quando todas as 8 rainhas são colocadas sem conflitos

A animação mostra em tempo real:
- Rainhas válidas (azul)
- Rainha sendo testada (vermelha)
- Conflitos detectados (vermelho brilhante)
- Estatísticas de iterações e backtracks

## Elementos do Diagrama

- **Nó Raiz (Início)**: Representa o estado inicial do problema
- **Caminho Verde**: Mostra a exploração do algoritmo
- **Nó com X vermelho**: Representa um beco sem saída (solução parcial inválida)
- **Seta Vermelha Pontilhada**: Indica o backtrack (retrocesso ao nó pai)
- **Linha Azul**: Mostra o novo galho escolhido após o backtrack
- **Nó com ✓ verde**: Representa uma solução válida encontrada

## Arquivos

- `diagrama_backtracking.py` - Script Python para gerar o diagrama estático
- `diagrama_backtracking_animado.py` - Script Python para gerar o diagrama animado (com movimento)
- `problema_8_rainhas_animado.py` - Animação do problema clássico das 8 rainhas usando backtracking
- `diagrama_backtracking.svg` - Versão SVG do diagrama
- `visualizar_diagrama.html` - Versão HTML para visualização no navegador
- `requirements.txt` - Dependências do projeto

