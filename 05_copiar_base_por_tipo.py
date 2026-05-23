"""
Script para copiar documentos da base organizada e classificá-los por tipo.
Estrutura de origem: 3-BASE_ORGANIZADA/[PROCESSO]/[INSTANCIA]/[TIPO_DOC]/[arquivo.pdf]
Estrutura de destino: 4-BASE_POR_TIPO/[TIPO_DOC]/[arquivo.pdf]
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

def copiar_base_por_tipo():
    """
    Copia todos os documentos da base organizada para a base por tipo.
    Organiza os documentos apenas pela categoria (Acórdão, Decisão, Sentença, Voto, etc.)
    """
    pasta_projeto = os.path.dirname(os.path.abspath(__file__))
    pasta_base_organizada = os.path.join(pasta_projeto, "3-BASE_ORGANIZADA")
    pasta_destino = os.path.join(pasta_projeto, "4-BASE_POR_TIPO")
    
    print("=" * 60)
    print("COPIANDO DOCUMENTOS POR TIPO DE DOCUMENTO")
    print("=" * 60)
    print(f"\nPasta origem: {pasta_base_organizada}")
    print(f"Pasta destino: {pasta_destino}\n")
    
    if not os.path.exists(pasta_base_organizada):
        print(f"Erro: Pasta {pasta_base_organizada} não encontrada!")
        return
    
    # Criar pasta de destino se não existir
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Dicionário para contar arquivos por tipo
    contagem_por_tipo = defaultdict(int)
    total_arquivos = 0
    arquivos_duplicados = 0
    
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
                
                # Criar pasta de destino para este tipo
                pasta_destino_tipo = os.path.join(pasta_destino, tipo_doc)
                os.makedirs(pasta_destino_tipo, exist_ok=True)
                
                # Copiar todos os arquivos deste tipo
                for arquivo in os.listdir(caminho_tipo):
                    caminho_origem = os.path.join(caminho_tipo, arquivo)
                    
                    if not os.path.isfile(caminho_origem):
                        continue
                    
                    caminho_destino_arquivo = os.path.join(pasta_destino_tipo, arquivo)
                    
                    # Verificar se arquivo já existe no destino
                    if os.path.exists(caminho_destino_arquivo):
                        print(f"⚠️  Arquivo duplicado: {arquivo} (será sobrescrito)")
                        arquivos_duplicados += 1
                    
                    try:
                        shutil.copy2(caminho_origem, caminho_destino_arquivo)
                        contagem_por_tipo[tipo_doc] += 1
                        total_arquivos += 1
                        print(f"✓ Copiado: {tipo_doc}/{arquivo}")
                    except Exception as e:
                        print(f"✗ Erro ao copiar {arquivo}: {e}")
    
    # Exibir resumo
    print("\n" + "=" * 60)
    print("RESUMO DA OPERAÇÃO")
    print("=" * 60)
    print(f"Total de arquivos copiados: {total_arquivos}")
    print(f"Arquivos duplicados encontrados: {arquivos_duplicados}")
    print(f"\nBreakdown por tipo de documento:")
    
    for tipo, quantidade in sorted(contagem_por_tipo.items()):
        print(f"  {tipo}: {quantidade} documentos")
    
    print("\n✓ Processo concluído com sucesso!")
    print(f"Documentos organizados em: {pasta_destino}\n")

if __name__ == "__main__":
    copiar_base_por_tipo()
