"""
Arquivo principal da aplicação Streamlit BI.
"""
import streamlit as st
import sys
import os

# Adicionar o diretório raiz ao path para importações relativas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers.app_controller import AppController

def main():
    """
    Função principal que inicia a aplicação Streamlit.
    """
    AppController.run()

if __name__ == "__main__":
    main()
