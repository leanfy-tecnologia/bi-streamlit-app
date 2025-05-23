"""
View para a página de login da aplicação Streamlit BI.
"""
import streamlit as st
from utils.auth import login, logout, is_authenticated

def render_login_page():
    """
    Renderiza a página de login.
    
    Returns:
        bool: True se o usuário estiver autenticado, False caso contrário
    """
    if is_authenticated():
        if st.sidebar.button("Logout", key="logout_btn"):
            logout()
            st.rerun()
        return True
    
    col1, col2, col3 = st.columns([1, 2, 1])  # col2 é mais larga

    with col2:
        st.markdown("<h2 style='text-align: center; font-size: 2.75rem; font-weight: 700;padding: 1.25rem 0px 1rem;'>Login</h2>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar")
            
            if submit:
                if username and password:
                    auth_success, user_data = login(username, password)
                    if auth_success:
                        st.session_state.user_data = user_data
                        st.success("Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos.")
                else:
                    st.warning("Por favor, preencha todos os campos.")
    
    return False
