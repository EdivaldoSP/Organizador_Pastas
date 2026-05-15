import os
import glob
import json

def categorizar_arquivos(base_dir):
    print("Iniciando categorização...")
    
    search_pattern = os.path.join(base_dir, "**", "documentos.json")
    arquivos_json = glob.glob(search_pattern, recursive=True)
    
    estrutura_final = []
    
    for json_path in arquivos_json:
        # A pasta pai do JSON é a instância (se houver) e o avô é o Nº do Processo
        pasta_instancia = os.path.dirname(json_path)
        nome_instancia = os.path.basename(pasta_instancia)
        
        pasta_processo = os.path.dirname(pasta_instancia)
        n_processo = os.path.basename(pasta_processo)
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                dados_documentos = json.load(f)
        except Exception as e:
            print(f"Erro ao ler {json_path}: {e}")
            continue
        
        processo_info = {
            "processo": n_processo,
            "instancia": nome_instancia,
            "documentos": []
        }
        
        for doc in dados_documentos:
            codigo = doc.get("codigo", "")
            classificacao = doc.get("classificacao", "")
            
            # Normalizar a classificação se necessário
            classif_lower = classificacao.lower()
            categoria_final = "Outros"
            
            if "sentença" in classif_lower or "sentenca" in classif_lower:
                categoria_final = "Sentença"
            elif "decisão" in classif_lower or "decisao" in classif_lower:
                categoria_final = "Decisão"
            elif "voto" in classif_lower:
                categoria_final = "Voto"
            elif "acórdão" in classif_lower or "acordao" in classif_lower:
                categoria_final = "Acórdão"
            elif classificacao:
                categoria_final = classificacao.strip() # Se tiver uma classe específica na tabela
                
            processo_info["documentos"].append({
                "codigo": codigo,
                "categoria": categoria_final,
                "classificacao_original": classificacao
            })
            
        estrutura_final.append(processo_info)
        
    output_path = os.path.join(base_dir, "estrutura_final.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(estrutura_final, f, ensure_ascii=False, indent=4)
        
    print(f"Estrutura final salva em: {output_path}")

if __name__ == "__main__":
    base_dir = r"c:\Users\Ed\Documents\1-Documentos\1-EDIVALDO\2-Meus_Projetos\Organizador_Pastas\2-BASE_PRE_PROCESSADA_IMAGENS"
    categorizar_arquivos(base_dir)
