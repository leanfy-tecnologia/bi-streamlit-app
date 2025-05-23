"""
Controlador principal da aplicação Streamlit BI.
Gerencia o fluxo de navegação e controle de sessão.
"""
import streamlit as st
import os
from views.login_view import render_login_page
from views.upload_view import render_upload_page
from views.dashboard_view import render_dashboard_page
from utils.auth import is_authenticated, logout

class AppController:
    """
    Controlador principal da aplicação.
    Gerencia o fluxo de navegação e controle de sessão.
    """
    
    @staticmethod
    def initialize_session():
        """
        Inicializa a sessão do Streamlit com valores padrão.
        """
        # Configurar o título da página
        st.set_page_config(
            page_title="Sistema de BI",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Inicializar variáveis de sessão se não existirem
        if "page" not in st.session_state:
            st.session_state.page = "login"
        
        if "user_data" not in st.session_state:
            st.session_state.user_data = None
        
        if "dataframes" not in st.session_state:
            st.session_state.dataframes = {}
    
    @staticmethod
    def render_navigation():
        """
        Renderiza informações básicas e botão de logout na barra lateral.
        """
        if is_authenticated():
            st.sidebar.title("Leanfy - BI ")
            st.sidebar.write("Bem-vindo")
            
            # Botão de logout
            if st.sidebar.button("Logout"):
                logout()
                st.session_state.page = "login"
                st.rerun()
    
    @staticmethod
    def render_current_page():
        """
        Renderiza a página atual com base na seleção do usuário.
        """
        # Verificar autenticação para páginas protegidas
        if st.session_state.page != "login" and not is_authenticated():
            st.session_state.page = "login"
            st.rerun()
            return
        
        # Renderizar a página selecionada
        if st.session_state.page == "login":
            is_logged_in = render_login_page()
            if is_logged_in:
                st.session_state.page = "upload"
                st.rerun()
        
        elif st.session_state.page == "upload":
            render_upload_page()
        
        elif st.session_state.page == "dashboard":
            render_dashboard_page()
        
        else:
            st.error(f"Página não encontrada: {st.session_state.page}")
            st.session_state.page = "login"
            st.rerun()
    
    @staticmethod
    def run():
        """
        Executa o controlador principal da aplicação.
        """
        AppController.initialize_session()
        AppController.render_navigation()
        AppController.render_current_page()
