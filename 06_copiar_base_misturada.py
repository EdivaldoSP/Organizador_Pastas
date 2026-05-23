"""
Script para copiar todos os documentos da base organizada para uma pasta misturada.
Estrutura de origem: 3-BASE_ORGANIZADA/[PROCESSO]/[INSTANCIA]/[TIPO_DOC]/[arquivo.pdf]
Estrutura de destino: 5-BASE_BRUTA_MISTURADA/[arquivo.pdf]

Similar à pasta 1-BASE_BRUTA_TOTAL, mas com os documentos já processados.
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

def copiar_base_misturada():
    """
    Copia todos os documentos da base organizada para uma pasta misturada.
    Todos os arquivos ficam na raiz da pasta de destino.
    """
    pasta_projeto = os.path.dirname(os.path.abspath(__file__))
    pasta_base_organizada = os.path.join(pasta_projeto, "3-BASE_ORGANIZADA")
    pasta_destino = os.path.join(pasta_projeto, "5-BASE_BRUTA_MISTURADA")
    
    print("=" * 60)
    print("CRIANDO BASE BRUTA MISTURADA (DESORGANIZADA)")
    print("=" * 60)
    print(f"\nPasta origem: {pasta_base_organizada}")
    print(f"Pasta destino: {pasta_destino}\n")
    
    if not os.path.exists(pasta_base_organizada):
        print(f"Erro: Pasta {pasta_base_organizada} não encontrada!")
        return
    
    # Criar pasta de destino se não existir
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Contadores
    total_arquivos = 0
    arquivos_duplicados = 0
    arquivos_pulados = 0
    
    # Percorrer todas as pastas de processo
    for processo in os.listdir(pasta_base_organizada):
        caminho_processo = os.path.join(pasta_base_organizada, processo)
        
        if not os.path.isdir(caminho_processo):
            continue
        
        # Percorrer todas as instâncias do processo
        for instancia in os.listdir(caminho_processo):
            caminho_instancia = os.path.join(caminho_processo, instancia)
            
            if not os.path.isdir(caminho_instancia):
                continue
            
            # Percorrer todos os tipos de documento (Acórdão, Decisão, etc.)
            for tipo_doc in os.listdir(caminho_instancia):
                caminho_tipo = os.path.join(caminho_instancia, tipo_doc)
                
                if not os.path.isdir(caminho_tipo):
                    continue
                
                # Copiar todos os arquivos
                for arquivo in os.listdir(caminho_tipo):
                    caminho_origem = os.path.join(caminho_tipo, arquivo)
                    
                    if not os.path.isfile(caminho_origem):
                        continue
                    
                    caminho_destino_arquivo = os.path.join(pasta_destino, arquivo)
                    
                    # Verificar se arquivo já existe no destino
                    if os.path.exists(caminho_destino_arquivo):
                        # Adicionar sufixo para não sobrescrever
                        nome_base, extensao = os.path.splitext(arquivo)
                        nome_novo = f"{nome_base}_{processo}{extensao}"
                        caminho_destino_arquivo = os.path.join(pasta_destino, nome_novo)
                        print(f"⚠️  Arquivo duplicado: {arquivo} → {nome_novo}")
                        arquivos_duplicados += 1
                    
                    try:
                        shutil.copy2(caminho_origem, caminho_destino_arquivo)
                        total_arquivos += 1
                        print(f"✓ Copiado: {arquivo}")
                    except Exception as e:
                        print(f"✗ Erro ao copiar {arquivo}: {e}")
                        arquivos_pulados += 1
    
    # Exibir resumo
    print("\n" + "=" * 60)
    print("RESUMO DA OPERAÇÃO")
    print("=" * 60)
    print(f"Total de arquivos copiados: {total_arquivos}")
    print(f"Arquivos duplicados (renomeados): {arquivos_duplicados}")
    print(f"Arquivos com erro: {arquivos_pulados}")
    print(f"\n✓ Base bruta misturada criada em: {pasta_destino}")
    print(f"  Total de arquivos na pasta: {len(os.listdir(pasta_destino))}\n")

if __name__ == "__main__":
    copiar_base_misturada()
