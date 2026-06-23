import os
import glob
import time
from cats_love_boxes import resolver_fase

def carregar_fase_txt(caminho_arquivo):
    """Abre e converte um arquivo estruturado por espaços em matriz de texto."""
    matriz = []
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            elementos = linha.strip().split()
            if elementos:
                matriz.append(elementos)
    return matriz

def executar_bateria_de_testes():
    # Procura recursivamente por arquivos .txt na pasta 'fases'
    pasta_fases = os.path.join('fases', '*.txt')
    arquivos_fases = sorted(glob.glob(pasta_fases))
    
    if not arquivos_fases:
        print("Erro: Nenhuma fase (.txt) encontrada na pasta 'fases/'.")
        print("Por favor, certifique-se de que a pasta existe e contém mapas salvos.")
        return

    print(f"=== Suite Automatizada de Testes MAPF ===")
    print(f"Fases localizadas no diretório: {len(arquivos_fases)}\n")
    
    for caminho in arquivos_fases:
        nome_fase = os.path.basename(caminho)
        print(f"Processando entrada: {nome_fase}")
        
        try:
            matriz = carregar_fase_txt(caminho)
            
            # --- MEDIÇÃO DE TEMPO INÍCIO ---
            tempo_inicio = time.perf_counter()
            resultado = resolver_fase(matriz)
            tempo_fim = time.perf_counter()
            # -------------------------------
            
            tempo_total = tempo_fim - tempo_inicio
            
            print(f"  Resultado obtido: ", end="")
            if resultado == "NAO":
                print("Mundo Sem Solução ❌")
            else:
                print(f"Solucionado de forma ótima! ✔️ ({len(resultado)} passos)")
                print(f"  Movimentos calculados: {resultado}")
            
            # Exibe o tempo gasto com precisão de 4 casas decimais
            print(f"  Tempo de execução: {tempo_total:.4f} segundos")
            
        except Exception as e:
            print(f"  Falha Crítica ao interpretar {nome_fase}: {e}")
            
        print("-" * 60)

if __name__ == "__main__":
    executar_bateria_de_testes()