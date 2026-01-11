"""
Ficheiro principal do projeto de simulação de clínica.
Ponto de entrada da aplicação.
"""

import interface


def main():
    """
    Função principal que inicia a aplicação.
    """
    print("="*60)
    print("Simulação de Clínica - Sistema de Eventos Discretos")
    print("="*60)
    print("\nA iniciar interface gráfica...\n")
    
    try:
        interface.executar_interface()
    except KeyboardInterrupt:
        print("\n\nAplicacao interrompida pelo utilizador.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        raise


if __name__ == "__main__":
    main()

