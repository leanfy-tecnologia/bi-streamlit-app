import numpy as np
import streamlit as st
import folium
from streamlit_folium import st_folium
import branca.colormap
from folium.plugins import HeatMap
from models.data_processor import DataProcessor
from utils.auth import is_authenticated
import pandas as pd

def render_dashboard_page():
    """
    Renderiza a página de dashboards interativos.
    """

    geojson_estado_sp = "https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-35-mun.json"
    geojson_piracicaba_sp = "RMP_Limite_Municipal.json"


    if not is_authenticated():
        st.warning("Você precisa estar logado para acessar esta página.")
        return
    
    st.title("📊 Dashboards")
    
    # Verificar se há um DataFrame selecionado
    if "current_df" not in st.session_state or not st.session_state.current_df:
        st.info("Por favor, faça upload ou selecione um dataset na página de Upload.")
        # Botão para voltar para a página de upload
        if st.button("Voltar para Upload"):
            st.session_state.page = "upload"
            st.rerun()
        return
    
    # Carregar o DataFrame selecionado
    df_key = st.session_state.current_df
    df_info_session = st.session_state.dataframes[df_key]
    file_path = df_info_session["path"]
    
    success, df, error = DataProcessor.load_dataframe(file_path)
    
    if not success:
        st.error(f"Erro ao carregar o dataset: {error}")
        # Remover dataset inválido da sessão
        del st.session_state.dataframes[df_key]
        if st.session_state.current_df == df_key:
            if st.session_state.dataframes:
                st.session_state.current_df = list(st.session_state.dataframes.keys())[0]
            else:
                del st.session_state.current_df
        st.rerun()
        return
    
    st.subheader("Mapa de calor")
    st.subheader("Estado de SP")

    dados = pd.read_csv("lat_long.csv")
    dados2 = np.genfromtxt("lat_long.csv", delimiter = ",")
    dados2 = dados2[~np.isnan(dados2).any(axis=1)]

    mapa_estado_sp_calor = folium.Map([-22.71579000, -47.77297000], 
                            tiles = "cartodbpositron",
                            zoom_start = 6)

    #Adicionar o fundo branco
    folium.TileLayer(tiles = branca.utilities.image_to_url([[1,1], [1,1]]),
                    attr = "Leanfy", name = "Sem Imagem Fundo").add_to(mapa_estado_sp_calor)

    #Adicionando a fronteira dos municipios
    estilo = lambda x: {"color" : "black",
                    "fillOpacity": 0,
                    "weight": 1}

    folium.GeoJson(geojson_estado_sp, style_function = estilo,
        name = "Municipios", key="A").add_to(mapa_estado_sp_calor)

    #Paleta de cores
    indices = [0, 0.3, 0.7, 1]

    colormap = branca.colormap.StepColormap(["green", "yellow", "red"], index = indices,
                                        caption = "Índice Aleatório")

    dicionario_cores = {0: "green",
                    0.3: "green",
                    0.301: "yellow",
                    0.7: "yellow",
                    0.701: "red",
                    1: "red"}


    colormap.scale(0, 500).add_to(mapa_estado_sp_calor)

    #Mapa de Calor
    HeatMap(data = dados2.tolist()).add_to(mapa_estado_sp_calor)


    #Controle de camadas
    folium.LayerControl(position = "topleft").add_to(mapa_estado_sp_calor)
        
    st_data = st_folium(mapa_estado_sp_calor, width="100%", height=500, key="mapa_estado_sp_calor")
    
    st.subheader("Mapa Coropleto")

    st.subheader("Estado de SP")

    mapa_estado_sp = folium.Map([-22.71579000, -47.77297000], 
                            tiles = "cartodbpositron",
                            zoom_start = 7)

    folium.Choropleth(geo_data = geojson_estado_sp,
                    data = df,
                    columns = ["CIDADE", "VALOR"],
                    key_on = "feature.properties.name",
                    fill_color = "GnBu",
                    fill_opacity = 0.9,
                    line_opacity = 0.5,
                    legend_name = "CIDADES",
                    nan_fill_color = "white",
                    name = "Dados").add_to(mapa_estado_sp)
    
    st_data = st_folium(mapa_estado_sp, width="100%", height=500, key="mapa_estado_sp")

    # #Adicionando a função de destaque
    # estilo = lambda x: {"fillColor": "white",
    #                 "color": "black",
    #                 "fillOpacity": 0.001,
    #                 "weight": 0.001}

    # estilo_destaque = lambda x: {"fillColor": "darkblue",
    #                             "color": "black",
    #                             "fillOpacity": 0.5,
    #                             "weight": 1}

    # highlight = folium.features.GeoJson(data = geojson_url,
    #                                 style_function = estilo,
    #                                 highlight_function = estilo_destaque,
    #                                 name = "Destaque")

    # #Adicionando caixa de texto
    # folium.features.GeoJsonTooltip(fields = ["name"],
    #                             aliases = ["Cidade"],
    #                             labels = False,
    #                             style = ("background-color: white; color: black; font-family: arial; font-size: 16px; padding: 10px;")).add_to(highlight)

    # #Adicionando o destaque ao mapa
    # mapa_idhm_rj.add_child(highlight)

    # #Adicionando o controle de camadas
    # folium.LayerControl().add_to(mapa_idhm_rj)
    
    # # Obter informações do DataFrame
    # df_info = DataProcessor.get_dataframe_info(df)
    
    # # --- Filtros na Sidebar ---
    # st.sidebar.header("Filtros")
    
    # # Filtro por Data (se houver coluna de data)
    # date_columns = df_info["date_columns"]
    # selected_date_col = None
    # if date_columns:
    #     selected_date_col = st.sidebar.selectbox("Coluna de Data para Filtro", ["Nenhuma"] + date_columns)
    #     if selected_date_col != "Nenhuma":
    #         min_date = df[selected_date_col].min()
    #         max_date = df[selected_date_col].max()
            
    #         # Verificar se min_date e max_date são NaT
    #         if pd.isna(min_date) or pd.isna(max_date):
    #             st.sidebar.warning(f"Coluna '{selected_date_col}' contém valores inválidos para filtro de data.")
    #             date_range = None
    #         else:
    #             try:
    #                 date_range = st.sidebar.date_input(
    #                     "Selecione o Período",
    #                     value=(min_date.date(), max_date.date()),
    #                     min_value=min_date.date(),
    #                     max_value=max_date.date()
    #                 )
    #                 if len(date_range) == 2:
    #                     start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    #                     df = df[(df[selected_date_col] >= start_date) & (df[selected_date_col] <= end_date)]
    #                 else:
    #                      st.sidebar.warning("Selecione um intervalo de datas válido.")
    #             except Exception as e:
    #                 st.sidebar.error(f"Erro ao aplicar filtro de data: {e}")
    #                 date_range = None # Resetar para evitar erros

    # # Filtros por Categoria (colunas categóricas)
    # categorical_columns = df_info["categorical_columns"]
    # selected_filters = {}
    # if categorical_columns:
    #     st.sidebar.subheader("Filtros Categóricos")
    #     for col in categorical_columns:
    #         unique_values = df[col].unique().tolist()
    #         # Limitar número de opções para evitar sobrecarga da interface
    #         if len(unique_values) < 50:
    #             selected_values = st.sidebar.multiselect(f"Filtrar por {col}", unique_values, default=[])
    #             if selected_values:
    #                 selected_filters[col] = selected_values
    #         else:
    #             st.sidebar.text(f"{col}: Muitos valores únicos para filtro interativo.")
                
    # # Aplicar filtros categóricos
    # for col, values in selected_filters.items():
    #     df = df[df[col].isin(values)]
        
    # # Verificar se o DataFrame ficou vazio após filtros
    # if df.empty:
    #     st.warning("Nenhum dado encontrado com os filtros aplicados.")
    #     return
        
    # # --- Visualizações --- 
    # st.header("Visualizações")
    
    # numeric_columns = df_info["numeric_columns"]
    
    # # Seleção de colunas para gráficos
    # st.subheader("Configuração dos Gráficos")
    # col1, col2 = st.columns(2)
    
    # with col1:
    #     x_axis = st.selectbox("Eixo X (Gráficos de Barras/Linhas)", ["Nenhum"] + categorical_columns + date_columns + numeric_columns)
    #     y_axis = st.selectbox("Eixo Y (Gráficos de Barras/Linhas)", ["Nenhum"] + numeric_columns)
    #     color_axis = st.selectbox("Cor (Agrupamento)", ["Nenhum"] + categorical_columns)
        
    # with col2:
    #     pie_col = st.selectbox("Coluna para Gráfico de Pizza", ["Nenhum"] + categorical_columns)
    #     heatmap_num_col1 = st.selectbox("Coluna Numérica 1 (Mapa de Calor)", ["Nenhum"] + numeric_columns)
    #     heatmap_num_col2 = st.selectbox("Coluna Numérica 2 (Mapa de Calor)", ["Nenhum"] + numeric_columns)
    #     heatmap_cat_col = st.selectbox("Coluna Categórica (Mapa de Calor)", ["Nenhum"] + categorical_columns)

    # # Gráfico de Barras
    # if x_axis != "Nenhum" and y_axis != "Nenhum":
    #     st.subheader(f"Gráfico de Barras: {y_axis} por {x_axis}")
    #     try:
    #         fig_bar = px.bar(df, x=x_axis, y=y_axis, 
    #                          color=color_axis if color_axis != "Nenhum" else None, 
    #                          title=f"{y_axis} por {x_axis}")
    #         st.plotly_chart(fig_bar, use_container_width=True)
    #     except Exception as e:
    #         st.error(f"Erro ao gerar gráfico de barras: {e}")

    # # Gráfico de Linhas (útil para séries temporais)
    # if x_axis != "Nenhum" and y_axis != "Nenhum" and x_axis in date_columns:
    #     st.subheader(f"Gráfico de Linhas: {y_axis} ao longo do tempo ({x_axis})")
    #     try:
    #         fig_line = px.line(df.sort_values(by=x_axis), x=x_axis, y=y_axis, 
    #                            color=color_axis if color_axis != "Nenhum" else None, 
    #                            title=f"{y_axis} ao longo do tempo")
    #         st.plotly_chart(fig_line, use_container_width=True)
    #     except Exception as e:
    #         st.error(f"Erro ao gerar gráfico de linhas: {e}")

    # # Gráfico de Pizza
    # if pie_col != "Nenhum":
    #     st.subheader(f"Distribuição por {pie_col}")
    #     try:
    #         # Contar ocorrências para o gráfico de pizza
    #         pie_data = df[pie_col].value_counts().reset_index()
    #         pie_data.columns = [pie_col, 'count']
    #         fig_pie = px.pie(pie_data, names=pie_col, values='count', title=f"Distribuição por {pie_col}")
    #         st.plotly_chart(fig_pie, use_container_width=True)
    #     except Exception as e:
    #         st.error(f"Erro ao gerar gráfico de pizza: {e}")

    # # Mapa de Calor (Heatmap)
    # st.subheader("Mapa de Calor")
    # if heatmap_num_col1 != "Nenhum" and heatmap_num_col2 != "Nenhum":
    #     try:
    #         # Usar correlação se duas colunas numéricas forem selecionadas
    #         st.write(f"Correlação entre {heatmap_num_col1} e {heatmap_num_col2}")
    #         correlation_matrix = df[[heatmap_num_col1, heatmap_num_col2]].corr()
    #         fig_heatmap_corr = px.imshow(correlation_matrix, text_auto=True, aspect="auto",
    #                                      title=f"Mapa de Calor da Correlação")
    #         st.plotly_chart(fig_heatmap_corr, use_container_width=True)
    #     except Exception as e:
    #         st.error(f"Erro ao gerar mapa de calor de correlação: {e}")
            
    # elif heatmap_num_col1 != "Nenhum" and heatmap_cat_col != "Nenhum":
    #      try:
    #         # Usar pivot table para categórica vs numérica
    #         st.write(f"Média de {heatmap_num_col1} por {heatmap_cat_col}")
    #         pivot_table = pd.pivot_table(df, values=heatmap_num_col1, index=heatmap_cat_col, aggfunc='mean')
    #         fig_heatmap_pivot = px.imshow(pivot_table, text_auto=True, aspect="auto",
    #                                       title=f"Mapa de Calor: Média de {heatmap_num_col1} por {heatmap_cat_col}")
    #         st.plotly_chart(fig_heatmap_pivot, use_container_width=True)
    #      except Exception as e:
    #         st.error(f"Erro ao gerar mapa de calor (pivot): {e}")
    # else:
    #     st.info("Selecione duas colunas numéricas ou uma numérica e uma categórica para gerar o mapa de calor.")

    # # Tabela Dinâmica (Exibição dos dados filtrados)
    # st.subheader("Dados Filtrados")
    # st.dataframe(df)