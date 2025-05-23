"""
Módulo para processamento de dados com Pandas.
"""
import pandas as pd
import io
import os
from typing import Dict, List, Optional, Tuple, Any
import streamlit as st

class DataProcessor:
    """
    Classe responsável pelo processamento de dados CSV e XLSX usando Pandas.
    """
    
    @staticmethod
    def validate_file(file) -> Tuple[bool, Optional[str]]:
        """
        Valida se o arquivo é um CSV ou XLSX válido.
        
        Args:
            file: Arquivo enviado pelo usuário
            
        Returns:
            Tupla com status de validação e mensagem de erro (se houver)
        """
        try:
            # Verificar extensão
            if not (file.name.endswith('.csv') or file.name.endswith('.xlsx')):
                return False, "O arquivo deve ter extensão .csv ou .xlsx"
            
            # Tentar ler o arquivo para validar
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:  # XLSX
                df = pd.read_excel(file)
            
            # Verificar se tem pelo menos uma linha e uma coluna
            if df.empty or len(df.columns) == 0:
                return False, "O arquivo está vazio ou não contém colunas"
                
            return True, None
        except Exception as e:
            return False, f"Erro ao validar arquivo: {str(e)}"
    
    @staticmethod
    def process_file(file) -> Tuple[bool, Optional[pd.DataFrame], Optional[str]]:
        """
        Processa o arquivo CSV ou XLSX e retorna um DataFrame.
        
        Args:
            file: Arquivo enviado pelo usuário
            
        Returns:
            Tupla com status de processamento, DataFrame (se sucesso) e mensagem de erro (se falha)
        """
        try:
            # Resetar o ponteiro do arquivo para o início
            file.seek(0)
            
            # Ler o arquivo de acordo com a extensão
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:  # XLSX
                df = pd.read_excel(file)
            
            # Processar dados básicos (limpeza, formatação)
            # Remover linhas duplicadas
            df = df.drop_duplicates()
            
            # Converter colunas de data se existirem
            for col in df.columns:
                if 'data' in col.lower() or 'date' in col.lower():
                    try:
                        df[col] = pd.to_datetime(df[col])
                    except:
                        pass  # Se não conseguir converter, mantém como está
            
            return True, df, None
        except Exception as e:
            return False, None, f"Erro ao processar arquivo: {str(e)}"
    
    @staticmethod
    def save_dataframe(df: pd.DataFrame, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Salva o DataFrame processado para uso posterior.
        
        Args:
            df: DataFrame a ser salvo
            filename: Nome do arquivo
            
        Returns:
            Tupla com status de salvamento e caminho do arquivo (se sucesso) ou mensagem de erro (se falha)
        """
        try:
            # Criar diretório de dados se não existir
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
            os.makedirs(data_dir, exist_ok=True)
            
            # Salvar DataFrame
            file_path = os.path.join(data_dir, f"{filename}.pkl")
            df.to_pickle(file_path)
            
            return True, file_path
        except Exception as e:
            return False, f"Erro ao salvar DataFrame: {str(e)}"
    
    @staticmethod
    def load_dataframe(file_path: str) -> Tuple[bool, Optional[pd.DataFrame], Optional[str]]:
        """
        Carrega um DataFrame salvo anteriormente.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Tupla com status de carregamento, DataFrame (se sucesso) e mensagem de erro (se falha)
        """
        try:
            df = pd.read_pickle(file_path)
            return True, df, None
        except Exception as e:
            return False, None, f"Erro ao carregar DataFrame: {str(e)}"
    
    @staticmethod
    def get_dataframe_info(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Obtém informações básicas sobre o DataFrame.
        
        Args:
            df: DataFrame a ser analisado
            
        Returns:
            Dicionário com informações sobre o DataFrame
        """
        info = {
            "num_rows": len(df),
            "num_columns": len(df.columns),
            "columns": list(df.columns),
            "dtypes": {col: str(df[col].dtype) for col in df.columns},
            "missing_values": df.isnull().sum().to_dict(),
            "numeric_columns": list(df.select_dtypes(include=['number']).columns),
            "categorical_columns": list(df.select_dtypes(include=['object', 'category']).columns),
            "date_columns": list(df.select_dtypes(include=['datetime']).columns)
        }
        return info
