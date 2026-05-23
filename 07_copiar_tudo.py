"""
Script para executar os dois scripts de cópia:
1. Copiar e organizar por tipo de documento (05_copiar_base_por_tipo.py)
2. Copiar e criar base bruta misturada (06_copiar_base_misturada.py)
"""

import subprocess
import sys
import os

def main():
    # Caminho do executável Python atual
    python_exe = sys.executable
    
    # Configurar o encoding para não dar erro no Windows
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    scripts = [
        "05_copiar_base_por_tipo.py",
        "06_copiar_base_misturada.py"
    ]

    print("\n" + "=" * 60)
    print("COPIANDO DOCUMENTOS DA BASE ORGANIZADA")
    print("=" * 60 + "\n")

    for i, script in enumerate(scripts, 1):
        print(f"\n[{i}/{len(scripts)}] Executando {script}...\n")
        
        # Executa o script usando o Python correto
        result = subprocess.run([python_exe, script], env=env)
        
        if result.returncode != 0:
            print(f"\nErro ao executar a etapa {i} ({script}). Processo abortado.")
            sys.exit(1)

    print("\n" + "=" * 60)
    print("TODAS AS CÓPIAS FORAM FINALIZADAS COM SUCESSO!")
    print("=" * 60)
    print("\nPastas criadas:")
    print("  • 4-BASE_POR_TIPO/ - Documentos organizados por tipo")
    print("  • 5-BASE_BRUTA_MISTURADA/ - Documentos em pasta única (misturados)")
    print()

if __name__ == "__main__":
    main()
