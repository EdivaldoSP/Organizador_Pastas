import subprocess
import sys
import os

def main():
    # Caminho do executável Python atual
    python_exe = sys.executable
    
    # Configurar o encoding para não dar erro no print do EasyOCR no Windows
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    scripts = [
        "01_extracao_imagens.py",
        "02_categorizacao.py",
        "03_organizador_arquivos.py"
    ]

    print("========================================")
    print("INICIANDO ORGANIZADOR DE PASTAS")
    print("========================================")

    for i, script in enumerate(scripts, 1):
        print(f"\n[{i}/{len(scripts)}] Executando {script}...")
        
        # Executa o script usando o Python correto
        result = subprocess.run([python_exe, script], env=env)
        
        if result.returncode != 0:
            print(f"\nErro ao executar a etapa {i} ({script}). Processo abortado.")
            sys.exit(1)

    print("\n========================================")
    print("PROCESSO FINALIZADO COM SUCESSO!")
    print("========================================")

if __name__ == "__main__":
    main()
