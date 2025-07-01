import streamlit as st
import pandas as pd
from streamlit.components.v1 import html

st.set_page_config(page_title="Organograma Dinâmico", layout="wide")
st.title("Organograma - Gerado via Excel")

# 📄 Carrega diretamente o Excel da mesma pasta
df = pd.read_excel("modelo_organograma.xlsx")

# 🔧 Corrigir ID Superior (caso esteja com valores vazios)
df["ID Superior"] = pd.to_numeric(df["ID Superior"], errors="coerce")

# 🔁 Função recursiva para montar árvore
def build_html_tree(df, parent_id=None):
    children = df[df["ID Superior"].isna() if parent_id is None else df["ID Superior"] == parent_id]
    if children.empty:
        return ""
    
    html_tree = '<div class="children">'
    for _, row in children.iterrows():
        html_tree += f'''
        <div class="child">
            <div class="node">
                <img src="{row['URL da Foto']}" />
                <div><strong>{row['Nome do Cargo']}</strong><br>{row['Nome da Pessoa']}</div>
            </div>
            <div class="line-vertical"></div>
            {build_html_tree(df, row['ID'])}
        </div>
        '''
    html_tree += '</div>'
    return html_tree

# Gera o HTML do organograma
html_tree = build_html_tree(df)

# 🎨 Estilo visual
html_code = f"""
<style>
* {{
  box-sizing: border-box;
}}
.org-container {{
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  font-family: sans-serif;
}}
.node {{
  text-align: center;
  margin: 10px;
}}
.node img {{
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 2px solid #333;
}}
.line-vertical {{
  width: 2px;
  height: 30px;
  background-color: #333;
  margin: 0 auto;
}}
.children {{
  display: flex;
  justify-content: center;
  align-items: flex-start;
  position: relative;
}}
.children::before {{
  content: "";
  position: absolute;
  top: 0;
  left: 10%;
  right: 10%;
  border-top: 2px solid #333;
  height: 2px;
  z-index: 0;
}}
.child {{
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 20px;
}}
</style>

<div class="org-container">
  {html_tree}
</div>
"""

# 🖥️ Renderiza no app
html(html_code, height=1000)






