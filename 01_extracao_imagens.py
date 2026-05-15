import os
import glob
import json
import pandas as pd
import easyocr

def extrair_dados_imagem(image_path, reader):
    print(f"Processando: {image_path}")
    
    # Extrai texto usando easyocr
    # detail=0 retorna apenas os textos.
    resultados = reader.readtext(image_path, detail=0)
    
    dados = []
    
    i = 0
    while i < len(resultados):
        texto = resultados[i].strip()
        
        # Verifica se é um número que representa o código do documento (ex: 105013043)
        if texto.isdigit() and len(texto) >= 6:
            codigo = texto
            classificacao = "Indefinida"
            
            # A classificação geralmente vem na próxima linha
            if i + 1 < len(resultados):
                prox = resultados[i+1].strip()
                # Valida para não pegar datas ou outros números
                if not prox.isdigit() and "/" not in prox:
                    classificacao = prox
                    
            dados.append({"codigo": codigo, "classificacao": classificacao})
            
        i += 1
        
    return dados

def processar_pasta_imagens(base_dir):
    reader = easyocr.Reader(['pt'])
    
    # Procura por todas as imagens dentro da estrutura
    # ORGANIZADOR DE PASTAS / 2-BASE_PRE_PROCESSADA_IMAGENS / Nº PROCESSO / INSTÂNCIA / *.png|jpg
    
    search_pattern = os.path.join(base_dir, "**", "*.png")
    imagens = glob.glob(search_pattern, recursive=True)
    
    search_pattern_jpg = os.path.join(base_dir, "**", "*.jpg")
    imagens.extend(glob.glob(search_pattern_jpg, recursive=True))
    
    for img_path in imagens:
        pasta_destino = os.path.dirname(img_path)
        
        dados = extrair_dados_imagem(img_path, reader)
        
        if dados:
            # 1. Salvar JSON
            json_path = os.path.join(pasta_destino, "documentos.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)
            print(f"Salvo: {json_path}")
            
            # 2. Salvar Excel
            df = pd.DataFrame(dados)
            excel_path = os.path.join(pasta_destino, "tabela_documentos.xlsx")
            df.to_excel(excel_path, index=False)
            print(f"Salvo: {excel_path}")

if __name__ == "__main__":
    base_dir = r"c:\Users\Ed\Documents\1-Documentos\1-EDIVALDO\2-Meus_Projetos\Organizador_Pastas\2-BASE_PRE_PROCESSADA_IMAGENS"
    processar_pasta_imagens(base_dir)
