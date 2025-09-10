import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px

st.set_page_config(
    page_title="Custo de Eletricidade",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")



df=pd.read_csv(r"Custo de eletricidade.csv")


st.title("📊 Custo de Eletricidade Dashboard")

containerMetric = st.container(border=True)
with containerMetric:
    col1, col2,col3 = st.columns(3)
    containerMetric = st.container(border=True)
    with col1:
        st.metric("💰 Custo Médio de Eletricidade ",f"${df["Custo de Eletrecidade"].mean():.0f}")
    with col2:
        st.metric("💧 Consumo Médio de Água",f"{df["Consumo de Água"].mean():.0f} Litros/Dia")
    with col3:
        st.metric("⚡️ Média de Utilização de Energia",f"{df["Utilização de Energia"].mean():.0f}%")  

chart_dataAreaEletri = df.groupby("Área do Local")["Custo de Eletrecidade"].mean().reset_index()

chart_dataAreaEletri = chart_dataAreaEletri.sort_values("Área do Local")


st.subheader("Custo Médio de Eletricidade por Área", divider="blue")
st.write("Média do custo de eletricidade por área do local (m²).")
st.line_chart(
    chart_dataAreaEletri.set_index("Área do Local"),
    height=400,  
    use_container_width=True ,
    color="#F0ED26"
)
#--------------------------------------------------------------------
chart_dataaguaeletri = df.groupby("Consumo de Água")["Custo de Eletrecidade"].mean().reset_index()

chart_dataaguaeletri = chart_dataaguaeletri.sort_values("Consumo de Água")


st.subheader("Custo Médio de Eletricidade por Consumo de Água", divider="blue")
st.write("Custo Médio de Eletricidade por Consumo de Água")
st.area_chart(
    chart_dataaguaeletri.set_index("Consumo de Água"),
    height=400,  
    use_container_width=True, 
    color="#F0ED26"
    )
#--------------------------------------------------------------------

eletricidade_data = df.groupby("Tipo de Estrutura")["Custo de Eletrecidade"].sum().reset_index()
agua_data = df.groupby("Tipo de Estrutura")["Consumo de Água"].sum().reset_index()
energia_data = df.groupby("Tipo de Estrutura")["Utilização de Energia"].sum().reset_index()


with st.container(border=True):
    st.subheader("Distribuição por Tipo de Estrutura", divider="blue")
    st.write("Proporções dos custos e consumos médios por tipo de estrutura.")

    
    col1, col2, col3 = st.columns(3)

   
    with col1:
        fig1, ax1 = plt.subplots(figsize=(4, 4))
        fig1.set_facecolor("none")  
        ax1.set_facecolor("none")   
        ax1.pie(
            eletricidade_data["Custo de Eletrecidade"],
            labels=eletricidade_data["Tipo de Estrutura"],
        
            autopct="%1.1f%%",
            startangle=90,
            
            textprops={"color": "white", "fontsize": 10}, 
            labeldistance=1.1,  
            pctdistance=0.7  
            
        )
        
        ax1.set_title("Custo de Eletricidade\npor Estrutura",color="white")
        st.pyplot(fig1)

    
    with col2:
        fig2, ax2 = plt.subplots(figsize=(4, 4))
        fig2.set_facecolor("none")
        ax2.set_facecolor("none")
        ax2.pie(
            agua_data["Consumo de Água"],
            labels=agua_data["Tipo de Estrutura"],
            autopct="%1.1f%%",
            startangle=90,
            
            textprops={"color": "white", "fontsize": 10},
            labeldistance=1.1,
            pctdistance=0.7
        )
        ax2.set_title("Consumo de Água\npor Estrutura",color="white")
        st.pyplot(fig2)

    
    with col3:
        fig3, ax3 = plt.subplots(figsize=(4, 4))
        fig3.set_facecolor("none")
        ax3.set_facecolor("none")
        ax3.pie(
            energia_data["Utilização de Energia"],
            labels=energia_data["Tipo de Estrutura"],
            autopct="%1.1f%%",
            startangle=90,
            
            textprops={"color": "white", "fontsize": 10},
            labeldistance=1.1,
            pctdistance=0.7
        )
        ax3.set_title("Utilização de Energia\npor Estrutura",color="white")
        st.pyplot(fig3)
        #-------------------------------------
    chart_dataaguaeletri = (
    df.groupby("Tipo de Estrutura")["Área do Local"]
    .sum()
    .reset_index()
)


chart_dataaguaeletri = chart_dataaguaeletri.sort_values("Tipo de Estrutura")


st.subheader("Área por Tipo de Estrutura", divider="blue")
st.write("Soma da área por Estrutura ")


chart = (
    alt.Chart(chart_dataaguaeletri)
    .mark_bar(color="#F0ED26")
    .encode(
        x=alt.X("Tipo de Estrutura:N", title="Tipo de Estrutura"),
        y=alt.Y("Área do Local:Q", title="Soma da Área")
    )
)


text = chart.mark_text(
    align="center",
    baseline="bottom",
    dy=-3,  
    fontSize=12
).encode(
    text=alt.Text("Soma da Área do Local (m²):Q", format=".1f")  
)


final_chart = chart + text


st.altair_chart(final_chart, use_container_width=True)