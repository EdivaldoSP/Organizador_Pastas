import os
import json
import shutil

def organizar_arquivos(json_path, pasta_base_bruta, pasta_destino_base):
    print("Iniciando organização dos arquivos...")
    
    if not os.path.exists(json_path):
        print(f"Erro: Arquivo {json_path} não encontrado.")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        estrutura = json.load(f)
        
    arquivos_movidos = 0
    arquivos_nao_encontrados = []
    
    for processo_info in estrutura:
        n_processo = processo_info.get("processo", "")
        instancia = processo_info.get("instancia", "")
        documentos = processo_info.get("documentos", [])
        
        movidos_neste_processo = 0
        faltantes_neste_processo = []
        
        for doc in documentos:
            codigo = doc.get("codigo", "")
            categoria = doc.get("categoria", "")
            
            if not codigo:
                continue
                
            # O arquivo original tem o nome igual ao código + .pdf
            nome_arquivo = f"{codigo}.pdf"
            caminho_origem = os.path.join(pasta_base_bruta, nome_arquivo)
            
            # Criar a estrutura de pastas no destino
            # ORGANIZADOR_PASTAS / DESTINO / Nº PROCESSO / INSTÂNCIA / CATEGORIA
            caminho_destino_pasta = os.path.join(pasta_destino_base, n_processo, instancia, categoria)
            caminho_destino_arquivo = os.path.join(caminho_destino_pasta, nome_arquivo)

            if os.path.exists(caminho_origem):
                os.makedirs(caminho_destino_pasta, exist_ok=True)
                
                # Mover o arquivo
                try:
                    shutil.move(caminho_origem, caminho_destino_arquivo)
                    arquivos_movidos += 1
                    movidos_neste_processo += 1
                    print(f"Movido: {nome_arquivo} -> {caminho_destino_pasta}")
                except Exception as e:
                    print(f"Erro ao mover {nome_arquivo}: {e}")
            else:
                faltantes_neste_processo.append(f"Processo {n_processo}: {nome_arquivo}")

        # Heurística para não checar na pasta de destino (pois fica lento):
        # Consideramos que o processo "do momento" é aquele em que estamos movendo arquivos agora.
        # Se movemos pelo menos 1 arquivo desse processo, mas faltaram outros, nós avisamos.
        # Se nenhum arquivo foi movido (0), assumimos que é um processo antigo que já foi 
        # todo organizado no passado, então ignoramos e não poluímos a tela.
        if movidos_neste_processo > 0 and len(faltantes_neste_processo) > 0:
            arquivos_nao_encontrados.extend(faltantes_neste_processo)
                
    print(f"\nResumo:")
    print(f"Arquivos movidos com sucesso: {arquivos_movidos}")
    print(f"Arquivos não encontrados na base bruta: {len(arquivos_nao_encontrados)}")
    if arquivos_nao_encontrados:
        print("Alguns arquivos não encontrados:", arquivos_nao_encontrados[:10])

if __name__ == "__main__":
    pasta_projeto = os.path.dirname(os.path.abspath(__file__))
    
    json_path = os.path.join(pasta_projeto, "2-BASE_PRE_PROCESSADA_IMAGENS", "estrutura_final.json")
    pasta_base_bruta = os.path.join(pasta_projeto, "1-BASE_BRUTA_TOTAL")
    
    # Criaremos uma pasta DESTINO para a base limpa e organizada
    pasta_destino_base = os.path.join(pasta_projeto, "3-BASE_ORGANIZADA")
    
    organizar_arquivos(json_path, pasta_base_bruta, pasta_destino_base)
