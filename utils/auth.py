"""
Módulo de autenticação para a aplicação Streamlit BI.
Implementa autenticação básica e está preparado para futura integração com JWT.
"""
import streamlit as st
import hashlib
import datetime
import uuid
from typing import Dict, Optional, Tuple

# Credenciais fixas para autenticação inicial
USERS = {
    "admin": {
        "password": "admin",  # Em produção, usar hash em vez de texto puro
        "name": "Administrador",
        "role": "admin"
    }
}

def hash_password(password: str) -> str:
    """
    Cria um hash seguro para a senha.
    
    Args:
        password: Senha em texto puro
        
    Returns:
        Hash da senha
    """
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(username: str, password: str) -> bool:
    """
    Verifica se as credenciais do usuário são válidas.
    
    Args:
        username: Nome de usuário
        password: Senha em texto puro
        
    Returns:
        True se as credenciais forem válidas, False caso contrário
    """
    if username not in USERS:
        return False
    
    # Para implementação inicial, comparação direta
    # Em produção, comparar hashes
    return USERS[username]["password"] == password

def generate_token(username: str) -> str:
    """
    Gera um token de sessão simples.
    Preparado para futura implementação de JWT.
    
    Args:
        username: Nome de usuário
        
    Returns:
        Token de sessão
    """
    # Implementação simples para sessão Streamlit
    # Em produção, usar JWT com chave secreta e expiração
    return str(uuid.uuid4())

def login(username: str, password: str) -> Tuple[bool, Optional[Dict]]:
    """
    Realiza o login do usuário.
    
    Args:
        username: Nome de usuário
        password: Senha
        
    Returns:
        Tupla com status de autenticação e dados do usuário (ou None se falhar)
    """
    if verify_password(username, password):
        user_data = USERS[username].copy()
        user_data.pop("password")  # Não armazenar senha na sessão
        user_data["token"] = generate_token(username)
        user_data["login_time"] = datetime.datetime.now().isoformat()
        return True, user_data
    return False, None

def is_authenticated() -> bool:
    """
    Verifica se o usuário está autenticado na sessão atual.
    
    Returns:
        True se o usuário estiver autenticado, False caso contrário
    """
    return "user_data" in st.session_state and st.session_state.user_data is not None

def logout() -> None:
    """
    Realiza o logout do usuário, limpando os dados da sessão.
    """
    if "user_data" in st.session_state:
        del st.session_state.user_data
