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
        
        for doc in documentos:
            codigo = doc.get("codigo", "")
            categoria = doc.get("categoria", "")
            
            if not codigo:
                continue
                
            # O arquivo original tem o nome igual ao código + .pdf
            nome_arquivo = f"{codigo}.pdf"
            caminho_origem = os.path.join(pasta_base_bruta, nome_arquivo)
            
            if os.path.exists(caminho_origem):
                # Criar a estrutura de pastas no destino
                # ORGANIZADOR_PASTAS / DESTINO / Nº PROCESSO / INSTÂNCIA / CATEGORIA
                caminho_destino_pasta = os.path.join(pasta_destino_base, n_processo, instancia, categoria)
                os.makedirs(caminho_destino_pasta, exist_ok=True)
                
                caminho_destino_arquivo = os.path.join(caminho_destino_pasta, nome_arquivo)
                
                # Mover o arquivo
                try:
                    shutil.move(caminho_origem, caminho_destino_arquivo)
                    arquivos_movidos += 1
                    print(f"Movido: {nome_arquivo} -> {caminho_destino_pasta}")
                except Exception as e:
                    print(f"Erro ao mover {nome_arquivo}: {e}")
            else:
                arquivos_nao_encontrados.append(nome_arquivo)
                
    print(f"\nResumo:")
    print(f"Arquivos movidos com sucesso: {arquivos_movidos}")
    print(f"Arquivos não encontrados na base bruta: {len(arquivos_nao_encontrados)}")
    if arquivos_nao_encontrados:
        print("Alguns arquivos não encontrados:", arquivos_nao_encontrados[:10])

if __name__ == "__main__":
    pasta_projeto = r"c:\Users\Ed\Documents\1-Documentos\1-EDIVALDO\2-Meus_Projetos\Organizador_Pastas"
    
    json_path = os.path.join(pasta_projeto, "2-BASE_PRE_PROCESSADA_IMAGENS", "estrutura_final.json")
    pasta_base_bruta = os.path.join(pasta_projeto, "1-BASE_BRUTA_TOTAL")
    
    # Criaremos uma pasta DESTINO para a base limpa e organizada
    pasta_destino_base = os.path.join(pasta_projeto, "3-BASE_ORGANIZADA")
    
    organizar_arquivos(json_path, pasta_base_bruta, pasta_destino_base)
