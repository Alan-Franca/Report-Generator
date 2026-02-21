# 📊 Gerador de Dashboards Dinâmicos e Relatórios PDF

Este projeto é uma ferramenta de análise de dados interativa desenvolvida em Python. O sistema permite que o usuário carregue qualquer arquivo Excel, configure dinamicamente quais colunas deseja analisar, personalize o visual dos gráficos e exporte um relatório executivo formal em PDF.

## 🚀 Funcionalidades

- **Upload de Dados Dinâmico:** Aceita arquivos `.xlsx` com diferentes estruturas de colunas.
- **Mapeamento de Colunas:** Interface amigável para o usuário selecionar qual coluna representa o Eixo X (Categorias) e o Eixo Y (Valores).
- **Visualização Interativa:** Gráficos gerados com **Plotly** que permitem zoom e interação.
- **Personalização Visual:**
  - Seletor de cores (Color Picker) para ajustar a identidade visual.
  - Seleção de temas (Dark Mode, Minimalista, etc.).
- **Exportação PDF:** Geração automática de relatórios contendo:
  - Cabeçalho e título personalizados.
  - Resumo estatístico (Soma Total, Média, etc.).
  - Versão estática do gráfico mantendo a cor escolhida pelo usuário.

## 🛠️ Tecnologias Utilizadas

- **[Python 3](https://www.python.org/):** Linguagem base.
- **[Streamlit](https://streamlit.io/):** Framework para criação da interface web interativa.
- **[Pandas](https://pandas.pydata.org/):** Manipulação e análise de dados.
- **[Plotly](https://plotly.com/python/):** Biblioteca de gráficos interativos.
- **[Matplotlib](https://matplotlib.org/):** Geração de gráficos estáticos para inserção no PDF.
- **[FPDF](https://pyfpdf.readthedocs.io/):** Criação e formatação do arquivo PDF.

## 📦 Como executar o projeto

1.  **Clone o repositório:**

    ```bash
    git clone [https://github.com/Alan-Franca/Report-Generator](https://github.com/Alan-Franca/Report-Generator)
    cd NOME-DO-PROJETO
    ```

2.  **Crie um ambiente virtual (Opcional, mas recomendado):**

    ```bash
    python -m venv venv
    # No Windows:
    venv\Scripts\activate
    # No Mac/Linux:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install streamlit pandas plotly fpdf matplotlib openpyxl
    ```

4.  **Execute a aplicação:**

    ```bash
    streamlit run app_relatorio.py
    ```

5.  **Acesse no navegador:**
    O Streamlit abrirá automaticamente uma aba no seu navegador (geralmente em `http://localhost:8501`).

## 📂 Estrutura do Projeto

- `app_relatorio.py`: Código principal da aplicação.
- `requirements.txt`: Lista de dependências do projeto.
- `README.md`: Documentação do projeto.

---

Desenvolvido com Python 🐍
