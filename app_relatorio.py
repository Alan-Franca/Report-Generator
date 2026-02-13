import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Construtor de Dashboards", layout="wide")

if 'graficos_adicionados' not in st.session_state:
    st.session_state['graficos_adicionados'] = []

def carregar_dados(arquivo):
    try:
        return pd.read_excel(arquivo)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return None

def gerar_pdf_multiplo(df, lista_graficos, titulo_relatorio):
    """
    Gera um PDF iterando sobre a lista de gráficos criados pelo usuário.
    Mapeia os tipos do Plotly para Matplotlib (para funcionar no PDF estático).
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 20, txt="Relatório de Dashboard", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Projeto: {titulo_relatorio}", ln=True)
    pdf.cell(0, 10, txt=f"Total de Gráficos: {len(lista_graficos)}", ln=True)
    pdf.ln(10)

    for i, config in enumerate(lista_graficos):
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, txt=f"{i+1}. {config['titulo']}", ln=True)
        pdf.ln(5)
        col_x = config['x']
        col_y = config['y']
        tipo = config['tipo']
        cor = config['cor'] 
        
        if pd.api.types.is_numeric_dtype(df[col_y]):
            if tipo == 'Pizza':
                df_grouped = df.groupby(col_x)[col_y].sum().reset_index().sort_values(by=col_y, ascending=False).head(8)
            else:
                df_grouped = df.groupby(col_x)[col_y].sum().reset_index()
        else:
            df_grouped = df.head(15)

        plt.figure(figsize=(10, 6))
        
        try:
            if tipo == 'Barra':
                plt.bar(df_grouped[col_x].astype(str), df_grouped[col_y], color=cor)
            elif tipo == 'Linha':
                plt.plot(df_grouped[col_x].astype(str), df_grouped[col_y], color=cor, marker='o')
                plt.grid(True, linestyle='--', alpha=0.6)
            elif tipo == 'Pizza':
                plt.pie(df_grouped[col_y], labels=df_grouped[col_x], autopct='%1.1f%%', startangle=140)
            elif tipo == 'Dispersão':
                plt.scatter(df_grouped[col_x], df_grouped[col_y], color=cor)
            
            plt.title(config['titulo'])
            if tipo != 'Pizza':
                plt.xlabel(col_x)
                plt.ylabel(col_y)
                plt.xticks(rotation=45)
            
            plt.tight_layout()
            temp_chart = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            temp_chart.close()
            plt.savefig(temp_chart.name)
            plt.close()
            pdf.image(temp_chart.name, x=10, y=None, w=190)
            os.unlink(temp_chart.name)
            
            if pd.api.types.is_numeric_dtype(df[col_y]):
                pdf.ln(10)
                pdf.set_font("Arial", size=10)
                pdf.cell(0, 10, txt=f"Total acumulado neste gráfico: {df_grouped[col_y].sum():,.2f}", ln=True)

        except Exception as e:
            pdf.cell(0, 10, txt=f"Não foi possível gerar a imagem estática deste gráfico. Erro: {str(e)}", ln=True)

    return pdf.output(dest='S').encode('latin-1')


st.title("Construtor de Dashboards & Relatórios")

arquivo_upload = st.file_uploader("1. Carregue seu arquivo Excel (.xlsx)", type=["xlsx"])

if arquivo_upload is not None:
    df = carregar_dados(arquivo_upload)

    if df is not None:
        colunas = df.columns.tolist()

        st.sidebar.header("⚙️ Criar Novo Gráfico")
        
        with st.sidebar.form("form_novo_grafico"):
            st.write("Configure o componente:")
            tipo_grafico = st.selectbox("Tipo de Gráfico", ["Barra", "Linha", "Pizza", "Dispersão"])
            
            c_x = st.selectbox("Eixo X (Categorias/Tempo)", colunas)
            c_y = st.selectbox("Eixo Y (Valores)", colunas)
            
            cor_picker = st.color_picker("Cor Principal", "#1F77B4")
            titulo = st.text_input("Título do Componente", "Análise de Dados")
            
            largura = st.radio("Tamanho no Dashboard", ["Largura Total (100%)", "Meia Largura (50%)"])
            
            btn_adicionar = st.form_submit_button("➕ Adicionar ao Dashboard")

            if btn_adicionar:
                novo_config = {
                    "tipo": tipo_grafico,
                    "x": c_x,
                    "y": c_y,
                    "cor": cor_picker,
                    "titulo": titulo,
                    "largura": "full" if "100" in largura else "half"
                }
                st.session_state['graficos_adicionados'].append(novo_config)
                st.success("Gráfico adicionado com sucesso!")

        st.markdown("---")
        
        if st.button("Limpar Dashboard"):
            st.session_state['graficos_adicionados'] = []
            st.rerun()

        st.subheader("Visualização do Dashboard")
        
        if not st.session_state['graficos_adicionados']:
            st.info("Utilize a barra lateral para criar e adicionar gráficos ao seu painel.")
        
        chart_idx = 0
        while chart_idx < len(st.session_state['graficos_adicionados']):
            config = st.session_state['graficos_adicionados'][chart_idx]
            
            if config['largura'] == 'full':
                with st.container():
                    st.markdown(f"### {config['titulo']}")
                    if config['tipo'] == 'Barra':
                        fig = px.bar(df, x=config['x'], y=config['y'], color_discrete_sequence=[config['cor']])
                    elif config['tipo'] == 'Linha':
                        fig = px.line(df, x=config['x'], y=config['y'], color_discrete_sequence=[config['cor']])
                    elif config['tipo'] == 'Pizza':
                        fig = px.pie(df, names=config['x'], values=config['y'], color_discrete_sequence=[config['cor']])
                    elif config['tipo'] == 'Dispersão':
                        fig = px.scatter(df, x=config['x'], y=config['y'], color_discrete_sequence=[config['cor']])
                    
                    st.plotly_chart(fig, use_container_width=True)
                chart_idx += 1
            
            else: 
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"#### {config['titulo']}")
                    if config['tipo'] == 'Barra':
                        fig = px.bar(df, x=config['x'], y=config['y'], color_discrete_sequence=[config['cor']])
                    elif config['tipo'] == 'Linha':
                        fig = px.line(df, x=config['x'], y=config['y'], color_discrete_sequence=[config['cor']])
                    elif config['tipo'] == 'Pizza':
                        fig = px.pie(df, names=config['x'], values=config['y'])
                    elif config['tipo'] == 'Dispersão':
                        fig = px.scatter(df, x=config['x'], y=config['y'], color_discrete_sequence=[config['cor']])
                    st.plotly_chart(fig, use_container_width=True)
                
                chart_idx += 1
                
                if chart_idx < len(st.session_state['graficos_adicionados']):
                    prox_config = st.session_state['graficos_adicionados'][chart_idx]
                    if prox_config['largura'] == 'half':
                        with col2:
                            st.markdown(f"#### {prox_config['titulo']}")
                            if prox_config['tipo'] == 'Barra':
                                fig = px.bar(df, x=prox_config['x'], y=prox_config['y'], color_discrete_sequence=[prox_config['cor']])
                            elif prox_config['tipo'] == 'Linha':
                                fig = px.line(df, x=prox_config['x'], y=prox_config['y'], color_discrete_sequence=[prox_config['cor']])
                            elif prox_config['tipo'] == 'Pizza':
                                fig = px.pie(df, names=prox_config['x'], values=prox_config['y'])
                            elif prox_config['tipo'] == 'Dispersão':
                                fig = px.scatter(df, x=prox_config['x'], y=prox_config['y'], color_discrete_sequence=[prox_config['cor']])
                            st.plotly_chart(fig, use_container_width=True)
                        chart_idx += 1

        st.markdown("---")
        st.subheader("Exportar Relatório Completo")
        
        titulo_pdf = st.text_input("Nome do Arquivo PDF:", "Relatorio_Dashboard")
        
        if st.button("📄 Gerar PDF com todos os gráficos"):
            if not st.session_state['graficos_adicionados']:
                st.warning("Adicione pelo menos um gráfico antes de gerar o PDF.")
            else:
                with st.spinner('Compilando relatório PDF... Isso pode levar alguns segundos.'):
                    pdf_bytes = gerar_pdf_multiplo(df, st.session_state['graficos_adicionados'], titulo_pdf)
                    
                    st.download_button(
                        label="Baixar Relatório PDF",
                        data=pdf_bytes,
                        file_name=f"{titulo_pdf}.pdf",
                        mime="application/pdf"
                    )