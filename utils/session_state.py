import streamlit as st
import json
import os
import pickle
from datetime import datetime, timedelta

class SessionManager:
    """
    Classe para gerenciar a persistência do estado da sessão entre recargas da página.
    """
    
    SESSION_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sessions')
    
    @staticmethod
    def initialize():
        """
        Inicializa o gerenciador de sessão e cria o diretório de sessões se não existir.
        """
        os.makedirs(SessionManager.SESSION_DIR, exist_ok=True)
        
        # Inicializar ID de sessão se não existir
        if "session_id" not in st.session_state:
            # Gerar um ID de sessão único baseado no timestamp
            st.session_state.session_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Carregar estado salvo se existir
        SessionManager.load_state()
    
    @staticmethod
    def get_session_file_path():
        """
        Obtém o caminho do arquivo de sessão para o ID de sessão atual.
        
        Returns:
            str: Caminho do arquivo de sessão
        """
        return os.path.join(SessionManager.SESSION_DIR, f"session_{st.session_state.session_id}.pkl")
    
    @staticmethod
    def save_state():
        """
        Salva o estado atual da sessão em um arquivo.
        """
        # Dados a serem salvos
        state_data = {
            'page': st.session_state.get('page', 'login'),
            'user_data': st.session_state.get('user_data', None),
            'dataframes': st.session_state.get('dataframes', {}),
            'current_df': st.session_state.get('current_df', None),
            'timestamp': datetime.now().isoformat()
        }
        
        # Salvar em arquivo
        try:
            with open(SessionManager.get_session_file_path(), 'wb') as f:
                pickle.dump(state_data, f)
        except Exception as e:
            st.error(f"Erro ao salvar estado da sessão: {e}")
    
    @staticmethod
    def load_state():
        """
        Carrega o estado da sessão de um arquivo, se existir.
        
        Returns:
            bool: True se o estado foi carregado com sucesso, False caso contrário
        """
        session_file = SessionManager.get_session_file_path()
        
        if os.path.exists(session_file):
            try:
                with open(session_file, 'rb') as f:
                    state_data = pickle.load(f)
                
                # Verificar se o estado não está expirado (24 horas)
                saved_time = datetime.fromisoformat(state_data['timestamp'])
                if datetime.now() - saved_time > timedelta(hours=24):
                    # Estado expirado, remover arquivo
                    os.remove(session_file)
                    return False
                
                # Restaurar estado
                if 'page' in state_data:
                    st.session_state.page = state_data['page']
                
                if 'user_data' in state_data and state_data['user_data'] is not None:
                    st.session_state.user_data = state_data['user_data']
                
                if 'dataframes' in state_data:
                    st.session_state.dataframes = state_data['dataframes']
                
                if 'current_df' in state_data:
                    st.session_state.current_df = state_data['current_df']
                
                return True
            except Exception as e:
                st.error(f"Erro ao carregar estado da sessão: {e}")
                return False
        
        return False
    
    @staticmethod
    def clear_state():
        """
        Limpa o estado da sessão atual.
        """
        session_file = SessionManager.get_session_file_path()
        
        if os.path.exists(session_file):
            try:
                os.remove(session_file)
            except Exception as e:
                st.error(f"Erro ao remover arquivo de sessão: {e}")
    
    @staticmethod
    def cleanup_old_sessions():
        """
        Remove arquivos de sessão antigos (mais de 24 horas).
        """
        try:
            for filename in os.listdir(SessionManager.SESSION_DIR):
                if filename.startswith("session_") and filename.endswith(".pkl"):
                    file_path = os.path.join(SessionManager.SESSION_DIR, filename)
                    
                    # Verificar data de modificação do arquivo
                    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if datetime.now() - mod_time > timedelta(hours=24):
                        os.remove(file_path)
        except Exception as e:
            st.error(f"Erro ao limpar sessões antigas: {e}")
