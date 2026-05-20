import os
from collections import defaultdict
from pathlib import Path

def gerar_estatisticas_base_organizada():
    """
    Gera estatísticas da base de documentos organizada.
    Mostra: total de documentos, por processo e por tipo.
    """
    
    pasta_projeto = os.path.dirname(os.path.abspath(__file__))
    pasta_base_organizada = os.path.join(pasta_projeto, "3-BASE_ORGANIZADA")
    
    if not os.path.exists(pasta_base_organizada):
        print(f"Erro: Pasta {pasta_base_organizada} não encontrada.")
        return
    
    # Inicializar contadores
    total_documentos = 0
    documentos_por_processo = defaultdict(int)
    documentos_por_tipo = defaultdict(int)
    documentos_por_processo_tipo = defaultdict(lambda: defaultdict(int))
    
    # Tipos válidos de documentos
    tipos_validos = {"Acórdão", "Decisão", "Sentença", "Voto"}
    
    # Percorrer a estrutura de pastas
    for processo_nome in os.listdir(pasta_base_organizada):
        caminho_processo = os.path.join(pasta_base_organizada, processo_nome)
        
        if not os.path.isdir(caminho_processo):
            continue
        
        # Percorrer as instâncias (pastas dentro de cada processo)
        for instancia_nome in os.listdir(caminho_processo):
            caminho_instancia = os.path.join(caminho_processo, instancia_nome)
            
            if not os.path.isdir(caminho_instancia):
                continue
            
            # Percorrer os tipos de documento
            for tipo_nome in os.listdir(caminho_instancia):
                caminho_tipo = os.path.join(caminho_instancia, tipo_nome)
                
                if not os.path.isdir(caminho_tipo):
                    continue
                
                # Contar PDFs nesta pasta
                arquivos_pdf = [f for f in os.listdir(caminho_tipo) if f.endswith('.pdf')]
                quantidade = len(arquivos_pdf)
                
                if quantidade > 0:
                    total_documentos += quantidade
                    documentos_por_processo[processo_nome] += quantidade
                    documentos_por_tipo[tipo_nome] += quantidade
                    documentos_por_processo_tipo[processo_nome][tipo_nome] += quantidade
    
    # Exibir estatísticas
    print("\n" + "="*70)
    print("ESTATÍSTICAS DA BASE ORGANIZADA")
    print("="*70)
    
    print(f"\n📊 TOTAL DE DOCUMENTOS: {total_documentos:,}")
    
    print(f"\n📁 TOTAL DE PROCESSOS: {len(documentos_por_processo)}")
    
    print("\n" + "-"*70)
    print("DOCUMENTOS POR TIPO")
    print("-"*70)
    
    for tipo in sorted(documentos_por_tipo.keys()):
        quantidade = documentos_por_tipo[tipo]
        percentual = (quantidade / total_documentos * 100) if total_documentos > 0 else 0
        print(f"  {tipo:<20} {quantidade:>10,} documentos ({percentual:>5.1f}%)")
    
    print("\n" + "-"*70)
    print("TOP 20 PROCESSOS COM MAIS DOCUMENTOS")
    print("-"*70)
    
    processos_ordenados = sorted(
        documentos_por_processo.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    for idx, (processo, quantidade) in enumerate(processos_ordenados[:20], 1):
        percentual = (quantidade / total_documentos * 100) if total_documentos > 0 else 0
        print(f"  {idx:>2}. {processo:<35} {quantidade:>8,} docs ({percentual:>5.1f}%)")
    
    print("\n" + "-"*70)
    print("DISTRIBUIÇÃO POR TIPO E PROCESSO (Top 10)")
    print("-"*70)
    
    for idx, (processo, quantidade) in enumerate(processos_ordenados[:10], 1):
        print(f"\n  {idx}. {processo} ({quantidade} documentos)")
        tipos_deste_processo = documentos_por_processo_tipo[processo]
        for tipo in sorted(tipos_deste_processo.keys()):
            qtd_tipo = tipos_deste_processo[tipo]
            percentual = (qtd_tipo / quantidade * 100) if quantidade > 0 else 0
            print(f"     • {tipo:<15} {qtd_tipo:>5,} ({percentual:>5.1f}%)")
    
    print("\n" + "="*70)
    print("RESUMO GERAL")
    print("="*70)
    print(f"  Total de Documentos:     {total_documentos:,}")
    print(f"  Total de Processos:      {len(documentos_por_processo)}")
    print(f"  Média por Processo:      {total_documentos/len(documentos_por_processo):.1f}")
    print(f"  Tipos de Documentos:     {len(documentos_por_tipo)}")
    
    if total_documentos > 0:
        print(f"  Tipo Mais Frequente:     {max(documentos_por_tipo, key=documentos_por_tipo.get)}")
        print(f"  Tipo Menos Frequente:    {min(documentos_por_tipo, key=documentos_por_tipo.get)}")
    
    print("="*70 + "\n")

if __name__ == "__main__":
    gerar_estatisticas_base_organizada()
