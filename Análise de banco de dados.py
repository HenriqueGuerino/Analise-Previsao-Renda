import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st # type: ignore
from urllib.error import URLError
import plotly.express as px
from datetime import time

st.set_page_config(layout='wide', page_title='Análise | Base de clientes', page_icon='🗺️')

st.markdown('# Análise da base de clientes de um banco')
st.markdown('''Nesta análise tentamos trazer e entender alguns dados
            importantes sobre os clientes.''')
st.markdown('----')


df = pd.read_csv('./input/previsao_de_renda.csv')
df['data_ref'] = pd.to_datetime(df['data_ref'])


# Distribuição de renda
st.markdown('''## Distribuição de renda''')
st.markdown('#### Renda média X Data de coleta dos dados (por sexo)')
container = st.container()
left_column, right_column = container.columns(2)
date_min = df.data_ref.min()
date_max = df.data_ref.max()
data = df.groupby(['data_ref', 'sexo'])['renda'].mean().reset_index()
with left_column:
    date_start = st.date_input(label='Data inicial',
                                value=date_min,
                                min_value=date_min,
                                max_value=date_max, key=1)
with right_column:
    date_finish = st.date_input(label='Data final',
                                value=date_max,
                                min_value=date_min,
                                max_value=date_max, key=2)
with container:
    data = data[(data['data_ref'] <= pd.to_datetime(date_finish)) &
                (data['data_ref'] >= pd.to_datetime(date_start))]
    fig = px.bar(data,
                  x= 'data_ref',
                  y='renda',
                  barmode='group',
                  color='sexo').update_layout(
                  xaxis_title='Data',
                  yaxis_title='Renda média')
    st.plotly_chart(fig)
    
    st.markdown('----')

with container:
    st.markdown('#### Renda média X Idade média (por sexo)')
    data = df.groupby(['idade', 'sexo'])['renda'].mean().reset_index()
    idade_min = data.idade.min()
    idade_max = data.idade.max()
    values = st.slider(label='Selecione uma faixa de idade',
                       min_value=data['idade'].min(),
                       max_value=data['idade'].max(),
                       value=(data['idade'].min(),
                       data['idade'].max()))
    fig = px.line(data[(data['idade'] >= values[0]) & (data['idade'] <= values[1])],
                  x= 'idade',
                  y='renda',
                  color='sexo').update_layout(
                  xaxis_title='Idade média',
                  yaxis_title='Renda média')
    st.plotly_chart(fig)

st.markdown('----')

left_column, right_column = st.columns([.7, .3])
with left_column:
    # Renda média X Estado civil
    data = df.groupby(['estado_civil', 'sexo'])['renda'].mean().reset_index().set_index('estado_civil').T
    data = data[['Casado',
                 'Solteiro',
                 'União',
                 'Separado',
                 'Viúvo']].T.reset_index()
    fig = px.line(data,
                  x= 'estado_civil',
                  y='renda',
                  color='sexo',
                  title='Renda média X Estado civil (por sexo)').update_layout(
                  xaxis_title='Estado civil',
                  yaxis_title='Renda média')
    st.plotly_chart(fig)
    
with right_column:
    # Distribuição de estado civil
    data = df['estado_civil'].value_counts().reset_index()
    fig = px.pie(data,
                 values='count',
                 names='estado_civil',
                 hole=.5,
                 title='Distribuição de estado civil')
    st.plotly_chart(fig)

st.markdown('----')

left_column, right_column = st.columns([.3, .7])
with left_column:
    # Distribuição de estado civil
    data = df['tipo_residencia'].value_counts().reset_index()
    fig = px.pie(data,
                 values='count',
                 names='tipo_residencia',
                 hole=.5,
                 title='Distribuição de residência')
    st.plotly_chart(fig)

with right_column:
    # Renda média X Tipo de residência
    data = df.groupby(['tipo_residencia', 'sexo'])['renda'].mean().reset_index().set_index('tipo_residencia').T
    data = data[['Casa',
                 'Com os pais',
                 'Governamental',
                 'Aluguel',
                 'Estúdio',
                 'Comunitário']].T.reset_index()
    fig = px.line(data,
                  x= 'tipo_residencia',
                  y='renda',
                  color='sexo',
                  title='Renda média X Tipo de residência (por sexo)').update_layout(
                  xaxis_title='Tipo de residência',
                  yaxis_title='Renda média')
    st.plotly_chart(fig)

st.markdown('----')

left_column, right_column = st.columns([.7, .3])

with left_column:
    # Renda média X Tipo de renda
    data = df.groupby(['tipo_renda', 'sexo'])['renda'].mean().reset_index().set_index('tipo_renda').T
    data = data[['Assalariado',
                 'Empresário',
                 'Pensionista',
                 'Servidor público',
                 'Bolsista']].T.reset_index()
    fig = px.line(data,
                  x= 'tipo_renda',
                  y='renda',
                  color='sexo',
                  title='Renda média X Tipo de renda (por sexo)').update_layout(
                  xaxis_title='Tipo de renda',
                  yaxis_title='Renda')
    st.plotly_chart(fig)

with right_column:
    # Distribuição de estado civil
    data = df['tipo_renda'].value_counts().reset_index()
    fig = px.pie(data,
                 values='count',
                 names='tipo_renda',
                 hole=.5,
                 title='Distribuição de tipo de renda')
    st.plotly_chart(fig)

st.markdown('----')

left_column, right_column = st.columns([.3, .7])

with left_column:
    # Distribuição de escolaridade
    data = df['educacao'].value_counts().reset_index()
    fig = px.pie(data,
                 values='count',
                 names='educacao',
                 hole=.5,
                 title='Distribuição de níveis de escolaridade')
    st.plotly_chart(fig)

with right_column:
    # Renda média X Tipo de renda
    data = df.groupby(['educacao', 'sexo'])['renda'].mean().reset_index().set_index('educacao').T
    data = data[['Primário',
                 'Secundário',
                 'Superior incompleto',
                 'Superior completo',
                 'Pós graduação']].T.reset_index()
    fig = px.line(data,
                  x= 'educacao',
                  y='renda',
                  color='sexo',
                  title='Renda média X Nível de escolaridade (por sexo)').update_layout(
                  xaxis_title='Tipo de renda',
                  yaxis_title='Renda')
    st.plotly_chart(fig)

st.markdown('----')

left_column, right_column = st.columns(2)

with left_column:
    data = df.groupby(['posse_de_veiculo', 'sexo'])['renda'].mean().reset_index()
    fig = px.bar(data,
                 x='posse_de_veiculo',
                 y='renda',
                 color='sexo',
                 title='Renda média X Posse de veículo (por sexo)',
                 barmode='group').update_layout(
                 xaxis_title='Posse de veículo',
                 yaxis_title='Renda')
    st.plotly_chart(fig)

with right_column:
    data = df.groupby(['posse_de_imovel', 'sexo'])['renda'].mean().reset_index()
    fig = px.bar(data,
                 x='posse_de_imovel',
                 y='renda',
                 color='sexo',
                 title='Renda média X Posse de imóvel (por sexo)',
                 barmode='group').update_layout(
                 xaxis_title='Posse de imóvel',
                 yaxis_title='Renda', xaxis_ticks='inside')
    st.plotly_chart(fig)

with st.expander('Mostrar base de dados'):
    if st.toggle('Expandir'):
        st.write(df.drop('Unnamed: 0', axis=1))
    else:
        st.write(df.drop('Unnamed: 0', axis=1).head())