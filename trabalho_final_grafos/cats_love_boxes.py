import collections

# Símbolos do tabuleiro
LIVRE = '0'
PAREDE = 'W'
FOLHAS = 'L'
BURACO = 'B'

def resolver_fase(matriz_inicial):
    R = len(matriz_inicial)
    C = len(matriz_inicial[0])
    
    gatos_ini = {}
    caixas_ini_dit = {}  
    objetivos = set()
    status_vertices_ini = {}
    
    tabuleiro_base = []
    for r in range(R):
        linha = []
        for c in range(C):
            celula = matriz_inicial[r][c]
            pos = (r, c)
            
            # Divide a célula por '_' caso haja uma sobreposição (ex: 'C1_L')
            partes = celula.split('_')
            chao_base = LIVRE
            
            for val in partes:
                if val.startswith('G'):   # Gato (G1, G2, etc.)
                    gatos_ini[val] = pos
                elif val.startswith('C'): # Caixa (C1, C2, etc.)
                    caixas_ini_dit[pos] = val
                elif val.startswith('O'): # Qualquer objetivo (O1, O2, ..., O14, etc.)
                    objetivos.add(pos)
                elif val in [FOLHAS, BURACO]:
                    status_vertices_ini[pos] = val
                elif val == PAREDE:
                    chao_base = PAREDE
                    
            linha.append(chao_base)
        tabuleiro_base.append(linha)
        
    chaves_gatos = sorted(gatos_ini.keys())
    gatos_estado = tuple(gatos_ini[g] for g in chaves_gatos)
    
    caixas_estado = tuple(sorted(caixas_ini_dit.items()))
    status_estado = frozenset(status_vertices_ini.items())
    
    estado_inicial = (gatos_estado, caixas_estado, status_estado)
    
    fila = collections.deque([(estado_inicial, [])])
    visitados = {estado_inicial}
    
    MOVS = [(-1, 0, 'Cima'), (1, 0, 'Baixo'), (0, -1, 'Esquerda'), (0, 1, 'Direita')]
    
    while fila:
        estado_atual, caminho = fila.popleft()
        g_pos, c_tuple, s_dict_froz = estado_atual
        
        c_dict = dict(c_tuple)
        s_dict = dict(s_dict_froz)
        
        # Condição de Vitória Dinâmica: Todos os objetivos mapeados (não importa quantos)
        # devem conter alguma caixa sobre eles.
        if objetivos and all(obj in c_dict for obj in objetivos):
            return caminho
            
        for idx_gato in range(len(chaves_gatos)):
            g_id = chaves_gatos[idx_gato]  # 'G1', 'G2', etc.
            g_atual = g_pos[idx_gato]
            outros_gatos = [g_pos[i] for i in range(len(chaves_gatos)) if i != idx_gato]
            
            for dr, dc, dir_nome in MOVS:
                nr, nc = g_atual[0] + dr, g_atual[1] + dc
                prox_g = (nr, nc)
                
                if not (0 <= nr < R and 0 <= nc < C) or tabuleiro_base[nr][nc] == PAREDE:
                    continue
                if prox_g in outros_gatos:
                    continue
                if s_dict.get(prox_g) == BURACO:
                    continue
                    
                if prox_g in c_dict:
                    tipo_caixa = c_dict[prox_g]  
                    
                    # Mantém a restrição física de peso (G1 não move caixas com prefixo/tipo C2)
                    if g_id == 'G1' and tipo_caixa.startswith('C2'):
                        continue
                        
                    cr, cc = prox_g[0] + dr, prox_g[1] + dc
                    prox_c = (cr, cc)
                    
                    if not (0 <= cr < R and 0 <= cc < C) or tabuleiro_base[cr][cc] == PAREDE:
                        continue
                    if prox_c in outros_gatos or prox_c in c_dict:
                        continue
                        
                    novo_s_dict = s_dict.copy()
                    novo_c_dict = c_dict.copy()
                    
                    del novo_c_dict[prox_g]
                    
                    if s_dict.get(prox_c) == BURACO:
                        novo_s_dict[prox_c] = LIVRE
                    else:
                        novo_c_dict[prox_c] = tipo_caixa
                        
                    if g_id == 'G2' and s_dict.get(g_atual) == FOLHAS:
                        novo_s_dict[g_atual] = BURACO
                        
                    novos_g_pos = list(g_pos)
                    novos_g_pos[idx_gato] = prox_g
                    
                    prox_estado = (tuple(novos_g_pos), tuple(sorted(novo_c_dict.items())), frozenset(novo_s_dict.items()))
                    if prox_estado not in visitados:
                        visitados.add(prox_estado)
                        fila.append((prox_estado, caminho + [f"{g_id}:{dir_nome}"]))
                        
                else:
                    novo_s_dict = s_dict.copy()
                    if g_id == 'G2' and s_dict.get(g_atual) == FOLHAS:
                        novo_s_dict[g_atual] = BURACO
                        
                    novos_g_pos = list(g_pos)
                    novos_g_pos[idx_gato] = prox_g
                    
                    prox_estado = (tuple(novos_g_pos), tuple(sorted(c_dict.items())), frozenset(novo_s_dict.items()))
                    if prox_estado not in visitados:
                        visitados.add(prox_estado)
                        fila.append((prox_estado, caminho + [f"{g_id}:{dir_nome}"]))
                        
    return "NAO"