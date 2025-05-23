import streamlit as st
import pandas as pd
import os
import uuid
from datetime import datetime
from models.data_processor import DataProcessor
from utils.auth import is_authenticated

def render_upload_page():

    if not is_authenticated():
        st.warning("Você precisa estar logado para acessar esta página.")
        return False
    
    st.title("Upload de Dados")
    st.write("Faça upload de arquivos CSV ou XLSX para análise e visualização.")
    
    uploaded_file = st.file_uploader("Escolha um arquivo", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        
        is_valid, error_msg = DataProcessor.validate_file(uploaded_file)
        
        if not is_valid:
            st.error(error_msg)
            return False
        
        with st.spinner("Processando arquivo..."):
            success, df, error = DataProcessor.process_file(uploaded_file)
            
            if not success:
                st.error(error)
                return False
            
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            save_success, file_path = DataProcessor.save_dataframe(df, filename)
            
            if not save_success:
                st.error(file_path) 
                return False
            
            if "dataframes" not in st.session_state:
                st.session_state.dataframes = {}
            
            st.session_state.dataframes[filename] = {
                "path": file_path,
                "name": uploaded_file.name,
                "upload_time": datetime.now().isoformat(),
                "rows": len(df),
                "columns": len(df.columns)
            }
            
            # Definir o DataFrame atual
            st.session_state.current_df = filename
            
            if st.button("Prosseguir para Dashboard", key="btn_proceed", type="primary"):
                st.session_state.page = "dashboard"
                st.rerun()
            
            return True
    
    return False
