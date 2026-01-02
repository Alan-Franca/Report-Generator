import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Gerador de Relatórios Customizável", layout="wide")


def carregar_dados(arquivo):
    try:
        return pd.read_excel(arquivo)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return None

def gerar_pdf(df, col_x, col_y, titulo_relatorio, cor_personalizada):
    """
    Gera o PDF usando a cor escolhida pelo usuário também no gráfico estático.
    """
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt="Relatório Executivo", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Título: {titulo_relatorio}", ln=True)
    
    if pd.api.types.is_numeric_dtype(df[col_y]):
        total = df[col_y].sum()
        pdf.cell(0, 10, txt=f"Total acumulado: {total:,.2f}", ln=True)
    
    pdf.ln(10)
    plt.figure(figsize=(10, 6))
    df_grouped = df.groupby(col_x)[col_y].sum().reset_index() if pd.api.types.is_numeric_dtype(df[col_y]) else df.head(10)
    
    plt.bar(df_grouped[col_x].astype(str), df_grouped[col_y], color=cor_personalizada)
    
    plt.title(f"Gráfico: {col_x} vs {col_y}")
    plt.xlabel(col_x)
    plt.ylabel(col_y)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    temp_chart = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.savefig(temp_chart.name)
    plt.close()

    pdf.image(temp_chart.name, x=10, y=None, w=190)
    os.unlink(temp_chart.name)

    return pdf.output(dest='S').encode('latin-1')


st.title("Dashboard Personalizável & PDF")
st.markdown("Carregue seus dados, escolha as cores e gere seu relatório.")

arquivo_upload = st.file_uploader("Carregue seu arquivo Excel (.xlsx)", type=["xlsx"])

if arquivo_upload is not None:
    df = carregar_dados(arquivo_upload)

    if df is not None:
        st.sidebar.header("1. Configuração de Dados")
        colunas = df.columns.tolist()
        
        col_categoria = st.sidebar.selectbox("Eixo X (Categorias):", colunas)
        col_valor = st.sidebar.selectbox("Eixo Y (Valores):", colunas)
        st.sidebar.markdown("---")
        st.sidebar.header("2. Personalização Visual")
        
        cor_usuario = st.sidebar.color_picker("Escolha a cor das barras:", "#1F77B4")
        
        temas_disponiveis = ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn"]
        tema_usuario = st.sidebar.selectbox("Estilo do Gráfico:", temas_disponiveis)
        
        titulo_analise = st.sidebar.text_input("Título do Gráfico:", "Minha Análise")

        st.subheader(f"Visualização: {titulo_analise}")
        
        grafico = px.bar(
            df, 
            x=col_categoria, 
            y=col_valor, 
            title=titulo_analise,
            template=tema_usuario,
            color_discrete_sequence=[cor_usuario] 
        )
        
        st.plotly_chart(grafico, use_container_width=True)

        st.markdown("---")
        if st.button("Gerar PDF com este Estilo"):
            with st.spinner('Gerando PDF personalizado...'):
                pdf_bytes = gerar_pdf(df, col_categoria, col_valor, titulo_analise, cor_usuario)
                
                st.download_button(
                    label="Baixar PDF Personalizado",
                    data=pdf_bytes,
                    file_name="relatorio_custom.pdf",
                    mime="application/pdf"
                )