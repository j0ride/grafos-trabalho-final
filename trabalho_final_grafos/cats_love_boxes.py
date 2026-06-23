import collections

# Símbolos do tabuleiro
LIVRE = '0'
PAREDE = 'W'
FOLHAS = 'L'
BURACO = 'B'

def resolver_fase(matriz_inicial):
    R = len(matriz_inicial)
    C = len(matriz_inicial[0])
    
    # Extrair posições iniciais e limpar o tabuleiro base
    gatos_ini = {}
    caixas_ini = {}
    objetivos = set()
    status_vertices_ini = {}
    
    tabuleiro_base = []
    for r in range(R):
        linha = []
        for c in range(C):
            val = matriz_inicial[r][c]
            pos = (r, c)
            
            if val in ['G1', 'G2']:
                gatos_ini[val] = pos
                linha.append(LIVRE)
            elif val in ['C1', 'C2']:
                caixas_ini[val] = pos
                linha.append(LIVRE)
            elif val in ['O1', 'O2']:
                objetivos.add(pos)
                linha.append(LIVRE)
            elif val in [FOLHAS, BURACO]:
                status_vertices_ini[pos] = val
                linha.append(LIVRE)  # O status dinâmico é controlado via dicionário
            else:
                linha.append(val)
        tabuleiro_base.append(linha)
        
    chaves_caixas = sorted(caixas_ini.keys())
    chaves_gatos = sorted(gatos_ini.keys())
    
    gatos_estado = tuple(gatos_ini[g] for g in chaves_gatos)
    caixas_estado = tuple(caixas_ini[c] for c in chaves_caixas)
    status_estado = frozenset(status_vertices_ini.items())
    
    estado_inicial = (gatos_estado, caixas_estado, status_estado)
    
    fila = collections.deque([(estado_inicial, [])])
    visitados = {estado_inicial}
    
    # Movimentos ortogonais possíveis
    MOVS = [(-1, 0, 'Cima'), (1, 0, 'Baixo'), (0, -1, 'Esquerda'), (0, 1, 'Direita')]
    
    while fila:
        estado_atual, caminho = fila.popleft()
        g_pos, c_pos, s_dict_froz = estado_atual
        s_dict = dict(s_dict_froz)
        
        # Condição de Vitória: Todas as caixas estão posicionadas nos objetivos
        if all(pos in objetivos for pos in c_pos):
            return caminho
            
        # Exploração de movimentos para cada gato
        for idx_gato in range(len(chaves_gatos)):
            g_atual = g_pos[idx_gato]
            outros_gatos = [g_pos[i] for i in range(len(chaves_gatos)) if i != idx_gato]
            
            for dr, dc, dir_nome in MOVS:
                nr, nc = g_atual[0] + dr, g_atual[1] + dc
                prox_g = (nr, nc)
                
                # 1. Verificar limites da matriz e barreiras físicas
                if not (0 <= nr < R and 0 <= nc < C) or tabuleiro_base[nr][nc] == PAREDE:
                    continue
                # 2. Impedir colisões / conflito de vértice com outros gatos
                if prox_g in outros_gatos:
                    continue
                # 3. Impedir pisar em buracos abertos ativos
                if s_dict.get(prox_g) == BURACO:
                    continue
                    
                # Checar se há uma caixa na célula de destino
                caixa_na_frente_idx = None
                for idx_c, pos_c in enumerate(c_pos):
                    if pos_c == prox_g:
                        caixa_na_frente_idx = idx_c
                        break
                        
                if sorted(caixas_ini.keys()) and caixa_na_frente_idx is not None:
                    # Mecânica de Empurrar a Caixa
                    cr, cc = prox_g[0] + dr, prox_g[1] + dc
                    prox_c = (cr, cc)
                    
                    # Checar limites da nova posição da caixa e se bateu na parede
                    if not (0 <= cr < R and 0 <= cc < C) or tabuleiro_base[cr][cc] == PAREDE:
                        continue
                    if prox_c in outros_gatos or prox_c in c_pos:
                        continue
                        
                    novo_s_dict = s_dict.copy()
                    caixas_restantes = list(c_pos)
                    
                    if s_dict.get(prox_c) == BURACO:
                        # Caixa é sacrificada para selar o buraco (Passagem liberada)
                        caixas_restantes.pop(caixa_na_frente_idx)
                        novo_s_dict[prox_c] = LIVRE
                    else:
                        caixas_restantes[caixa_na_frente_idx] = prox_c
                        
                    # Se o gato pesado (G2) desocupa um vértice com folhas, vira Buraco irreversível
                    if chaves_gatos[idx_gato] == 'G2' and s_dict.get(g_atual) == FOLHAS:
                        novo_s_dict[g_atual] = BURACO
                        
                    novos_g_pos = list(g_pos)
                    novos_g_pos[idx_gato] = prox_g
                    
                    prox_estado = (tuple(novos_g_pos), tuple(caixas_restantes), frozenset(novo_s_dict.items()))
                    if prox_estado not in visitados:
                        visitados.add(prox_estado)
                        fila.append((prox_estado, caminho + [f"{chaves_gatos[idx_gato]}:{dir_nome}"]))
                else:
                    # Ação de Movimento Simples do Gato
                    novo_s_dict = s_dict.copy()
                    if chaves_gatos[idx_gato] == 'G2' and s_dict.get(g_atual) == FOLHAS:
                        novo_s_dict[g_atual] = BURACO
                        
                    novos_g_pos = list(g_pos)
                    novos_g_pos[idx_gato] = prox_g
                    
                    prox_estado = (tuple(novos_g_pos), c_pos, frozenset(novo_s_dict.items()))
                    if prox_estado not in visitados:
                        visitados.add(prox_estado)
                        fila.append((prox_estado, caminho + [f"{chaves_gatos[idx_gato]}:{dir_nome}"]))
                        
    return "NAO"