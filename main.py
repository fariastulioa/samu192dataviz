import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from dash.dependencies import Input, Output, State
import numpy as np



df = pd.read_csv('samu_tratado_2019_a_2022.csv', low_memory=False)

df['dia_hora'] = pd.to_datetime(df['dia_hora'])
df['idade'] = df['idade'].astype(int)
df['hora'] = df['hora'].fillna(df['hora'].mean())
df['hora'] = df['hora'].astype(int)

app = dash.Dash(__name__,
                external_stylesheets=[{
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
            dbc.themes.BOOTSTRAP,
            dbc.icons.BOOTSTRAP]) #server = server
server = app.server


# Set the default template to 'seaborn'
pio.templates.default = "seaborn"

# Get the 'seaborn' template
template = pio.templates[pio.templates.default]

# Make all backgrounds transparent
template.layout.paper_bgcolor = 'rgba(0,0,0,0)'
template.layout.plot_bgcolor = 'rgba(0,0,0,0)'

# Update the template in Plotly
pio.templates[pio.templates.default] = template


semana_map = {
    'Domingo':0,
    'Segunda-feira':1,
    'Terça-feira':2,
    'Quarta-feira':3,
    'Quinta-feira':4,
    'Sexta-feira':5,
    'Sábado':6,   
}

mean_idade = sum(df['idade']) / len(df['idade'])


# Grafico de ocorrencias mensais

df_grouped = df.groupby([pd.Grouper(key='dia_hora', freq='M')]).size().reset_index(name='count')

media_mensal = df_grouped['count'].mean()

ocorrencias_mensais = px.line(df_grouped, x='dia_hora', y='count',
              labels={'count': 'Número de ocorrências', 'dia_hora': 'Data'},
             color_discrete_sequence=px.colors.qualitative.D3)

ocorrencias_mensais.update_layout(
    title='Ocorrências mensais',
    title_x=0.5,
)

ocorrencias_mensais.update_traces(mode="markers+lines", hovertemplate=None)
ocorrencias_mensais.update_layout(hovermode="x")

ocorrencias_mensais.add_shape(
    type='line',
    x0=df_grouped['dia_hora'].min(),
    x1=df_grouped['dia_hora'].max(),
    y0=media_mensal,
    y1=media_mensal,
    line=dict(color='gray', dash='dash')
)

ocorrencias_mensais.add_shape(
    type='line',
    x0=df_grouped['dia_hora'].min(),
    x1=df_grouped['dia_hora'].max(),
    y0=media_mensal,
    y1=media_mensal,
    line=dict(color='gray', dash='dash', width=3)
)




# Grafico de ocorrencias diarias

df_grouped = df.groupby([pd.Grouper(key='dia_hora', freq='D')]).size().reset_index(name='count')

media_diaria = df_grouped['count'].mean()

ocorrencias_diarias = px.line(df_grouped, x='dia_hora', y='count',
              labels={'count': 'Número de ocorrências', 'dia_hora': 'Data'},
             color_discrete_sequence=px.colors.qualitative.D3)

ocorrencias_diarias.update_layout(
    title='Ocorrências diárias',
    title_x=0.5,
)

ocorrencias_diarias.update_traces(mode="markers+lines", hovertemplate=None)
ocorrencias_diarias.update_layout(hovermode="x")

ocorrencias_diarias.add_shape(
    type='line',
    x0=df_grouped['dia_hora'].min(),
    x1=df_grouped['dia_hora'].max(),
    y0=media_diaria,
    y1=media_diaria,
    line=dict(color='gray', dash='dash', width=3)
)


# Grafico de ocorrencias por tipo ao longo do tempo

df_grouped = df.groupby(['tipo', pd.Grouper(key='dia_hora', freq='M')]).size().reset_index(name='count')

tipos_tempo = px.line(df_grouped, x='dia_hora', y='count', color='tipo',
              labels={'count': 'Ocorrências por mês', 'dia_hora': 'Data','tipo':''},
             color_discrete_sequence=px.colors.qualitative.D3)

tipos_tempo.update_layout(
    title='Ocorrências por tipo ao longo do tempo',
    title_x=0.5,
)

tipos_tempo.update_traces(mode="markers+lines", hovertemplate=None)
tipos_tempo.update_layout(hovermode="x")


# Grafico de distribuicao de tipos e subtipos

tipos_tmap = px.treemap(
    df, path=['tipo', 'subtipo'],
    color_discrete_map = px.colors.qualitative.Dark2,
    hover_data=['tipo', 'subtipo']
)

tipos_tmap.update_traces(
    hovertemplate='<b>%{label}</b><br>Percentual da seção: %{percentParent:.2%}',
    textinfo='label+percent root',
    textfont=dict(size=14)
)
tipos_tmap.update_layout(
    title={
        'text': "Proporção de ocorrências por tipo",
        'x': 0.5,  # Center the title
        'xanchor': 'center',
        'yanchor': 'top',
        'y':0.97,
        'font': {'size': 16}  # Adjust the font size for the title,
    }, margin={'t': 10, 'l': 8, 'r': 8, 'b': 8}
)


# Grafico das distribuicoes de desfecho e motivo

tmdf = df.applymap(lambda x: x if x else ' ')
tmdf.fillna(' ', inplace=True)

result_tmap = px.treemap(
    tmdf, path=['desfecho', 'motivo'],
    color_discrete_map=px.colors.qualitative.Safe,
    color_discrete_sequence=px.colors.qualitative.Safe,
    hover_data=['desfecho', 'motivo']
)

result_tmap.update_traces(
    hovertemplate='<b>%{label}</b><br>Percentual da seção: %{percentParent:.2%}',
    textinfo='label+percent root',
    textfont=dict(size=14)
)

result_tmap.update_layout(
    title={
        'text': '"Resultado" das ocorrências',
        'x': 0.5,  # Center the title
        'xanchor': 'center',
        'yanchor': 'top',
        'y': 0.97,
        'font': {'size': 16}  # Adjust the font size for the title,
    }, margin={'t': 10, 'l': 8, 'r': 8, 'b': 8}
)


# Grafico de distribuicao das origens de chamado

origem_counts = df['origem_chamado'].value_counts().reset_index()
origem_counts.columns = ['origem_chamado','count']

origens_pie = px.pie(origem_counts, values='count',
    names='origem_chamado',
    hover_name='origem_chamado'
)

origens_pie.update_layout(
    title={
        'text': ""
    },
    legend=dict(
        orientation="v",
        yanchor="bottom",
        y=0.78,
        xanchor="right",
        x=1.02,
        bgcolor='rgba(0, 0, 0, 0)'
    )
)

origens_pie.update_traces(hovertemplate = "%{label}: <br>Ocorrências: %{value}")


# Grafico de distribuicao de tipos de ocorrencia por sexo do paciente

grouped_data = df.groupby(['sexo', 'tipo']).size().reset_index(name='count')
grouped_data['relative_frequency'] = grouped_data.groupby('sexo')['count'].transform(lambda x: x / x.sum())

tipos_sexo = px.bar(grouped_data, x='sexo', y='relative_frequency',
             color='tipo', color_discrete_sequence=px.colors.qualitative.Vivid)

grouped_data['cumulative_relative_frequency'] = grouped_data.groupby('sexo')['relative_frequency'].cumsum() - 0.5 * grouped_data['relative_frequency']
grouped_data['x_annotation'] = grouped_data['sexo']

min_height_threshold = 0.04

for _, row in grouped_data.iterrows():
    if row['relative_frequency'] >= min_height_threshold:
        tipos_sexo.add_annotation(
            x=row['x_annotation'],
            y=row['cumulative_relative_frequency'],
            text=row['tipo'],
            showarrow=False,
            font=dict(color='white', size=12),
            textangle=0,
            xanchor='center',
            yanchor='middle'
        )

tipos_sexo.update_traces(hovertemplate='Proporção: %{y:.2f}')

tipos_sexo.update_layout(
    title='',
    xaxis_title='Sexo',
    yaxis_title='Proporção de cada tipo de ocorrência',
    barmode='relative',
    bargap=0.2,
    showlegend=False,
    title_x=0.5,
)


# Grafico para analise das ocorrencias de transito

subtiposcomp = ['ACIDENTE COM CARROS', 'ACIDENTE COM MOTO', 'ATROPELAMENTO', 'ACIDENTE COM BICICLETA', 'CAPOTAMENTO']
comparacao = df[df['subtipo'].isin(subtiposcomp)]

df_grouped = comparacao.groupby(['subtipo', pd.Grouper(key='dia_hora', freq='M')]).size().reset_index(name='count')

ocorrencias_transito = px.line(df_grouped, x='dia_hora', y='count',
              labels={'count': 'Número de ocorrências', 'dia_hora': 'Mês'},
              color='subtipo',
             color_discrete_sequence=px.colors.qualitative.D3)

ocorrencias_transito.update_layout(
    title='Ocorrências mensais no trânsito',
    title_x=0.5,
)
ocorrencias_transito.update_traces(mode="markers+lines", hovertemplate=None)
ocorrencias_transito.update_layout(hovermode="x")


# Graifco para analise das ocorrencias por suspeita de COVID 19

c19df = df[df['subtipo'] == 'SUSPEITA COVID19']
df_grouped = c19df.groupby([pd.Grouper(key='dia_hora', freq='M')]).size().reset_index(name='count')

ocorrencias_covid = px.line(df_grouped, x='dia_hora', y='count',
              labels={'count': 'Número de ocorrências', 'dia_hora': 'Mês'},
             color_discrete_sequence=px.colors.qualitative.D3)

ocorrencias_covid.update_layout(
    title='',
)
ocorrencias_covid.update_traces(mode="markers+lines", hovertemplate=None)
ocorrencias_covid.update_layout(hovermode="x")


# Grafico para comparacao de bairros

capital_df = df[df['capital'] == 1]
bairro_counts = capital_df['bairro'].value_counts(normalize=True)
top_5_bairros = bairro_counts.nlargest(5).index.tolist()

top_bairros_df = pd.DataFrame({'bairro': top_5_bairros, 'relative_frequency': bairro_counts[top_5_bairros].tolist()})
top_bairros_df['percentage'] = top_bairros_df['relative_frequency'] * 100

category_order = top_bairros_df['bairro'].tolist()

bairros_proporcao = px.bar(top_bairros_df, y='bairro', x='percentage',  # Switch x and y
             labels={'percentage': 'Relative Frequency (%)', 'bairro': 'Bairro'},
             color='bairro',
             color_discrete_sequence=px.colors.qualitative.Vivid,
             category_orders={'bairro': category_order},
             orientation='h')  # Set orientation to 'h' for horizontal bars

bairros_proporcao.update_traces(hovertemplate='Proporção: %{x:.2f}%', textposition='inside', texttemplate='%{x:.2f}%')

bairros_proporcao.update_layout(
    title='Bairros da capital com maior incidência de ocorrências',
    title_x=0.5,
    yaxis_title='Bairro',  # Switch y and x axis titles
    xaxis_title='Percentual de ocorrências (%)',  # Switch y and x axis titles
    showlegend=False,
    barmode='relative',
    bargap=0.2,
)


# Grafico para comparacao entre capital e municipios (tipos metropolitana)

incluir = ['OBSTÉTRICA', 'RESPIRATÓRIA', 'PSIQUIÁTRICA']
cdf = df[df['tipo'].isin(incluir)]

grouped_data = cdf.groupby(['capital', 'tipo']).size().reset_index(name='count')
grouped_data['relative_frequency'] = grouped_data.groupby('capital')['count'].transform(lambda x: x / x.sum())

side_by_side_data = grouped_data.pivot(index='tipo', columns='capital', values='relative_frequency').reset_index()

tipos_metropolitana = px.bar(side_by_side_data, x='tipo', y=[1,0],
             color_discrete_sequence=px.colors.qualitative.Vivid,
            labels={'variable':''})

grouped_data['cumulative_relative_frequency'] = grouped_data.groupby('capital')['relative_frequency'].cumsum() - 0.5 * grouped_data['relative_frequency']

annotations_df = grouped_data[grouped_data['relative_frequency'] >= min_height_threshold].copy()
annotations_df['x_annotation'] = annotations_df.groupby('capital').cumcount() * 3

tipos_metropolitana.update_traces(hovertemplate='Proporção: %{y:.2f}')

tipos_metropolitana.update_layout(
    title='Tipos de ocorrências na região metropolitana',
    xaxis_title='',
    yaxis_title='Proporção de cada tipo de ocorrência',
    barmode='group',  # Change from 'relative' to 'group'
    bargap=0.2,
    title_x=0.5,
    legend=dict(
    orientation="v",
    yanchor="bottom",
    y=0.83,
    xanchor="right",
    x=0.36,
    bgcolor='rgba(0, 0, 0, 0)'
)
)

newnames = {'0':'Outros municípios', '1': 'Capital'}
tipos_metropolitana.for_each_trace(lambda t: t.update(name = newnames[t.name]))


# Grafico de distribuicao de ocorrencias por dia da semana para sexo masculino

mdf = df[df['sexo'] == 'Masculino']

semana_counts = mdf['nd_semana'].value_counts(normalize=True) * 100
semana_data = pd.DataFrame({'nd_semana': semana_counts.index, 'relative_frequency': semana_counts.values})

semana_data.sort_values('nd_semana', inplace=True)

semana_masculino = px.bar(semana_data, x='nd_semana', y='relative_frequency',
             labels={'relative_frequency': 'Proporção de ocorrências (%)', 'nd_semana': 'Dia da semana'},
             title='Ocorrências ao longo da semana (sexo Masculino)',
             color=semana_data['nd_semana'].astype(str),
             color_discrete_sequence=px.colors.qualitative.Set3)

average_value = semana_data['relative_frequency'].mean()
semana_masculino.add_shape(
    type='line',
    x0=-0.5,
    y0=average_value,
    x1=6.5,
    y1=average_value,
    line=dict(color='gray', width=2, dash='dash')
)

semana_masculino.update_layout(title_x=0.5,
                showlegend=False, coloraxis_showscale=False
)
semana_masculino.update_traces(hovertemplate='Dia: %{x}<br>Proporção: %{y:.2f}%')
custom_labels = semana_map
semana_masculino.update_xaxes(tickvals=list(custom_labels.values()),
                 ticktext=list(custom_labels.keys()))

semana_masculino.update_yaxes(range=[10, 16])





# Grafico de distribuicao de ocorrencias por dia da semana para sexo feminino

fdf = df[df['sexo'] == 'Feminino']

semana_counts = fdf['nd_semana'].value_counts(normalize=True) * 100

semana_data = pd.DataFrame({'nd_semana': semana_counts.index, 'relative_frequency': semana_counts.values})

semana_data.sort_values('nd_semana', inplace=True)

semana_feminino = px.bar(semana_data, x='nd_semana', y='relative_frequency',
             labels={'relative_frequency': 'Proporção de ocorrências (%)', 'nd_semana': 'Dia da semana'},
             title='Ocorrências ao longo da semana (sexo Feminino)',
             color=semana_data['nd_semana'].astype(str),
             color_discrete_sequence=px.colors.qualitative.Set3)

average_value = semana_data['relative_frequency'].mean()
semana_feminino.add_shape(
    type='line',
    x0=-0.5,
    y0=average_value,
    x1=6.5,
    y1=average_value,
    line=dict(color='gray', width=2, dash='dash')
)

semana_feminino.update_layout(title_x=0.5,
                showlegend=False, coloraxis_showscale=False
)

custom_labels = semana_map
semana_feminino.update_xaxes(tickvals=list(custom_labels.values()),
                 ticktext=list(custom_labels.keys()))

semana_feminino.update_traces(hovertemplate='Dia: %{x}<br>Proporção: %{y:.2f}%')
semana_feminino.update_yaxes(range=[10, 16])


# Grafico da distribuicao de ocorrencias por horario

average_h = df['hora'].mean()
horas_dist = px.histogram(df, x='hora', 
                   labels={'hora': 'Hora', 'count':'Ocorrências'},
                   title='Distribuição da hora de ocorrência')

for i in range(0, 24, 5):
    horas_dist.add_shape(type='line',
                  x0=i, y0=0,
                  x1=i, y1=1,
                  line=dict(color='gray', width=1, dash='dot'))

horas_dist.add_shape(type='line',
              x0=average_h, y0=0,
              x1=average_h, y1=1,
              line=dict(color='black', width=2))

horas_dist.update_layout(title_x=0.5, yaxis_title='Quantidade de ocorrências')
horas_dist.update_traces(hovertemplate='%{x} hora(s):<br>Ocorrências: %{y}')


# Grafico da distribuicao de ocorrencias por horario de acordo com sexo e fase da semana

grouped_data = df[df['sexo'] != 'Outro/desconhecido'].groupby(['sexo', 'hora', 'fds']).size().reset_index(name='count')
grouped_data['total'] = grouped_data.groupby(['sexo', 'fds'])['count'].transform('sum')
grouped_data['relative_frequency'] = grouped_data['count'] / grouped_data['total'] * 100  # Multiply by 100 for percentage

sexo_hora_fds = px.line(grouped_data, x='hora', y='relative_frequency', color='sexo', line_dash='fds',
              labels={'relative_frequency': 'Relative Frequency (%)', 'hora': 'Hora', 'sexo': 'Sexo'},  # Update the label
              category_orders={'sexo': ['Female', 'Male']},
)

sexo_hora_fds.update_layout(
    title='Frequência de ocorrências por horário e sexo',
    title_x=0.5,
    xaxis_title='Hora do dia',
    yaxis_title='Frequência (%)',  # Update the label
    showlegend=True,
    legend_title='',
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.26,
        xanchor="left",
        x=0.77,
        bgcolor='rgba(0, 0, 0, 0)'
    )
)
sexo_hora_fds.update_traces(mode="lines", hovertemplate=None)
sexo_hora_fds.update_layout(hovermode="x")


# Grafico da media de idade para cada motivo de finalizacao/desfecho/conclusao

average_idade_by_motivo = df.groupby('motivo')['idade'].mean().reset_index()
average_idade_by_motivo.sort_values(by='idade', inplace=True)

idade_motivo = px.bar(average_idade_by_motivo, x='idade', y='motivo',
             labels={'idade': 'Média de Idade', 'motivo': ''},
             title='Média de idade para cada motivo de finalização',
             orientation='h')
idade_motivo.update_traces(hovertemplate='%{y}: %{x:.0f} anos')
idade_motivo.add_shape(
    type='line',
    x0=mean_idade,
    x1=mean_idade,
    y0='OUTROS',
    y1='ENCONTRADO EM ÓBITO',
    line=dict(color='gray', dash='dash', width=2),
    
)
idade_motivo.update_layout(title_x=0.5)


# Grafico da media de idade das ocorrencias por horario

idade_hora = px.box(df, x='hora', y='idade',
             labels={'hora': 'Hora de ocorrência', 'idade': 'Idade (anos)'},
             title='Distribuição da Idade do paciente por hora')

idade_hora.add_shape(
    type='line',
    x0=-1,  # Set the x-coordinate of the starting point
    x1=24,  # Set the x-coordinate of the ending point
    y0=mean_idade,  # Set the y-coordinate of the starting point (mean of idade)
    y1=mean_idade,  # Set the y-coordinate of the ending point (mean of idade)
    line=dict(color='gray', dash='dash', width=2),  # Specify line color and style
)

idade_hora.update_layout(title_x=0.5)


# Grafico das medias de idade por tipo de ocorrencia

average_idade_by_tipo = df.groupby('tipo')['idade'].mean().reset_index()
average_idade_by_tipo.sort_values(by='idade', inplace=True)
idade_tipo = px.bar(average_idade_by_tipo, x='idade', y='tipo',
             labels={'idade': 'Média de idade', 'tipo': 'Tipo'},
             title='Média de idade para cada tipo de ocorrência',
             orientation='h')  # Set orientation to 'h' for horizontal bars
idade_tipo.update_traces(hovertemplate='%{y}: %{x:.0f} anos')
idade_tipo.add_shape(
    type='line',
    x0=mean_idade,
    x1=mean_idade,
    y0='OBSTÉTRICA',
    y1='ENDOCRINOLÓGICA',
    line=dict(color='gray', dash='dash', width=4)
)
idade_tipo.update_layout(title_x=0.5)


# Grafico das medias de idade por subtipo de ocorrencia

average_idade_by_subtipo = df.groupby('subtipo')['idade'].mean().reset_index()
average_idade_by_subtipo.sort_values(by='idade', inplace=True)

idade_subtipo = px.bar(average_idade_by_subtipo, x='idade', y='subtipo',
             labels={'idade': 'Média de idade', 'subtipo': ''},
             title='Média de idade para cada subtipo de ocorrência',
             orientation='h')  # Set orientation to 'h' for horizontal bars

idade_subtipo.add_shape(
    type='line',
    x0=mean_idade,
    x1=mean_idade,
    y0='CAPOTAMENTO',
    y1='EDEMA AGUDO PULMAO',
    line=dict(color='gray', dash='dash', width=2)
)
idade_subtipo.update_traces(hovertemplate='%{y}: %{x:.0f} anos')
idade_subtipo.update_layout(title_x=0.5)


# Grafico de distribuicao de idade dos pacientes


average_x = df['idade'].mean()
idade_dist = px.histogram(df, x='idade', 
                   labels={'idade': 'Idade'},
                   title='Distribuição da idade dos pacientes')

shapes = []
for i in range(int(df['idade'].min()), int(df['idade'].max()) + 1, 5):
    shapes.append(
        {
            'type': 'line',
            'xref': 'x',
            'yref': 'paper',
            'x0': i,
            'y0': 0,
            'x1': i,
            'y1': 1,
            'line': {'color': 'gray', 'width': 1, 'dash': 'dot'}
        }
    )

shapes.append(
    {
        'type': 'line',
        'xref': 'x',
        'yref': 'paper',
        'x0': average_x,
        'y0': 0,
        'x1': average_x,
        'y1': 1,
        'line': {'color': 'black', 'width': 2}
    }
)

idade_dist.update_layout(title_x=0.5, shapes=shapes,
                 yaxis_title='Quantidade de ocorrências')

idade_dist.update_traces(hovertemplate='Idade: %{x} <br>Ocorrências: %{y}')


# Grafico de distribuicao de idade por sexo

idade_violin = px.violin(df, y='idade', color='sexo', box=True, points=False,
               labels={'sexo': 'Sexo'})

idade_violin.update_layout(
    title='Idade dos pacientes por sexo',
    xaxis_title='',
    yaxis_title='Idade (anos)', title_x=0.5,
    legend=dict(
        orientation="h",
        #yanchor="bottom",
        #y=0.8,
        #xanchor="left",
        #x=1,
        bgcolor='rgba(0, 0, 0, 0)'
    )
)




# Define the app layout
app.layout = html.Div([

    html.Img(src='/assets/banner.png', style={'width': '100%', 'marginBottom':'36px'}),
    
    html.Br(),
    
    html.Div(
    [
        dcc.Markdown(
            """
            Esse dashboard baseado em Dash e Plotly serve para a visualização dinâmica de dados de ocorrências registradas no sistema do SAMU.  
              
            A base de dados utilizada foi construida a partir da união e tratamento de dados anuais divulgados pela Prefeitura do Recife, referentes aos anos de 2019, 2020, 2021 e 2022.  
              
            Há um período entre Novembro e Dezembro de 2019 em que a quantidade de registros cai drasticamente, fenômeno para o qual não se encontrou explicação.
            
              
                
            
            Autor:  
            [GitHub](https://github.com/fariastulioa)  
            [LinkedIn](https://www.linkedin.com/in/tuliofarias/)
            """
        ),
    ],
    style={'textAlign': 'center', 'textJustify': 'inter-word', 'padding': '20px'},
    ),
    
    
    
    # Content
    
    
        
    # 1st row title
    dbc.Row([html.H4(children='Total de ocorrências ao longo do tempo', style={'textAlign': 'center', 'marginBottom': '1px'})]),
    # 1st row content
    dbc.Row([
        dbc.Col([dcc.Graph(figure=ocorrencias_mensais), html.Div([dcc.Markdown("""Há uma inconsistência devido à falta de registros referentes a um período entre Novembro e Dezembro de 2019, o que explica o mínimo do gráfico.  
                                                                               Os picos de Maio de 2020 e Abril de 2021 estão relacionados à pandemia de COVID-19.
"""),],style={'textAlign': 'center', 'max-width': '640px', 'marginLeft': '40px', 'marginRight':'10px'},)],
                xs=7, sm=7, md=7, lg=5, xl=5),
        dbc.Col([dcc.Graph(figure=ocorrencias_diarias), html.Div([dcc.Markdown("""O período com dados faltantes pode ser melhor observado nesse gráfico.  
                                                                               Também é possível perceber outliers ou dias atípicos, indicando circunstâncias extraordinárias na região metropolitana do Recife, no funcionamento do SAMU ou no sistema de registro.
""")],
                                                        style={'textAlign': 'center', 'max-width': '640px', 'marginLeft': '70px', 'marginRight':'0px'})],
        xs=7, sm=7, md=7, lg=5, xl=5)

    ], className="g-0",  justify="evenly"),

    
    
    # 2nd row title
    dbc.Row([html.H4(children='Distribuição dos tipos de ocorrência', style={'textAlign': 'center', 'marginBottom': '1px', 'marginTop':'25px'})]),
    # 2nd row content
    dbc.Row([
        dbc.Col([dcc.Graph(figure=tipos_tempo), ],
        ), # xs=7, sm=7, md=7, lg=5, xl=5

    ], className="g-0",  justify="evenly"),
    
    dbc.Row([html.Div([dcc.Markdown("""As ocorrências do tipo geral são as mais numerosas em geral e se mantém no topo ao longo dos meses consistentemente.  
                                    A pandemia de COVID-19, entretanto, provocou momentos de exceção em que as ocorrências relacionadas a causas respiratórias foram mais numerosas.  
                                    Há também um grande número de ocorrências por causas externas, que se mantém entre os 3 tipos mais frequentes em todo o período analisado.
""")],
            style={'textAlign': 'center'})]),
    
    # 2nd row content
    dbc.Row([

        dbc.Col([dcc.Graph(figure=tipos_tmap), html.P("""O gráfico acima permite visualização específica dos subtipos mais frequentes em cada tipo de ocorrência, com mais informações da causa.  
                                                      Dentre os subtipos identificáveis (desconsiderando 'OUTROS'), destacam-se os acidentes com moto, suspeitas de COVID-19, quedas da própria altura, convulsão e agressividade.
""",
                                                style={'textAlign': 'center'})],
                ) # xs=7, sm=7, md=7, lg=5, xl=5

    ], className="g-0",  justify="evenly"),
    
    
    # 3rd row title
    dbc.Row([html.H4(children='Distribuição das ocorrências por desfecho e motivo', style={'textAlign': 'center', 'marginBottom': '1px', 'marginTop':'25px'})]),
    # 3rd row content
    dbc.Row([
        dbc.Col([dcc.Graph(figure=result_tmap), html.Div([dcc.Markdown("""Ocorrências concluídas são aquelas em que os agentes deslocados conseguem acompanhar as situações até seus desfechos.  
                                                                       Nota-se o grande percentual de casos em que a situação é estabilizada com orientações e diálogo via telefone e em que os solicitantes desistem da requisição.  
                                                                       Há também uma grande quantidade de casos em que o deslocamento do paciente não ocorre pelos agentes, por falta de necessidade, permissão ou preferência pelo deslocamento por particulares.
""")],
                                                        style={'textAlign': 'center'})],
        ), # xs=7, sm=7, md=7, lg=5, xl=5

    ], className="g-0",  justify="evenly"),
    
    # 4th row title
    dbc.Row([html.H4(children='Origem das ocorrências', style={'textAlign': 'center'})]),
    # 4th row content
    dbc.Row([
        dbc.Col([dcc.Graph(figure=origens_pie), html.Div([dcc.Markdown("""Quase dois terços das ocorrências é notificada de residências, onde boa parte da população mais frágil passa a maior parte do tempo (idosos, bebês, doentes, etc.).
""")],
                                                        style={'textAlign': 'center'})],
        ), # xs=7, sm=7, md=7, lg=5, xl=5
    ], className="g-0",  justify="evenly"),
      
    # 5th row title
    dbc.Row([html.H4(children='Distribuição de tipos de ocorrência de acordo com o sexo', style={'textAlign': 'center', 'marginBottom': '1px', 'marginTop':'25px'})]),
    # 5th row content
    dbc.Row([
        dbc.Col([dcc.Graph(figure=tipos_sexo), html.Div([dcc.Markdown("""Percebe-se que mulheres são consideravelmente menos suscetíveis a ocorrências de causa externa e levemente mais suscetíveis a ocorrências gastrointestinais.  
                                                                      Há também a expressiva incidência de ocorrências obstétricas, exclusiva do grupo capaz de gestar.
""")],
                                                        style={'textAlign': 'center'})],
        ), # xs=7, sm=7, md=7, lg=5, xl=5
    ], className="g-0",  justify="evenly"),
    
    # 6th row title
    dbc.Row([html.H4(children='Ocorrências de trânsito ao longo do tempo', style={'textAlign': 'center', 'marginBottom': '1px', 'marginTop':'25px'})]),
    # 6th row content
    dbc.Row([
        dbc.Col([dcc.Graph(figure=ocorrencias_transito), html.Div([dcc.Markdown("""Detalhamento da evolução dos números de ocorrências relacionadas ao trânsito.  
                                                                                Percebe-se que, além de ser o subtipo mais numeroso, o acidente com moto também é o que apresenta maior tendência de crescimento.
""")],
                                                        style={'textAlign': 'center'})],
        ), # xs=7, sm=7, md=7, lg=5, xl=5
    ], className="g-0",  justify="evenly"),
    
    # 7th row title
    dbc.Row([html.H4(children='Ocorrências por suspeita de COVID-19 ao longo do tempo', style={'textAlign': 'center', 'marginBottom': '1px', 'marginTop':'25px'})]),
    # 7th row content
    dbc.Row([
        dbc.Col([dcc.Graph(figure=ocorrencias_covid), html.Div([dcc.Markdown("""O gráfico acima permite observar o desenvolvimento da situação da pandemia de COVID-19 na região metropolitana.  
                                                                             É importante ressaltar que:  
                                                                             1. as suspeitas não necessariamente são confirmadas,  
                                                                             2. a solicitação do atendimento está relacionada à preocupação da população com o vírus e  
                                                                             3. a necessidade do atendimento depende da gravidade do caso da doença.
""")],
                                                        style={'textAlign': 'center'})],
        ), # xs=7, sm=7, md=7, lg=5, xl=5
    ], className="g-0",  justify="evenly"),


    # 8th row title
    dbc.Row([html.H4(children='Distribuição geográfica das ocorrências', style={'textAlign': 'center', 'marginBottom': '1px', 'marginTop':'25px'})]),
    # 8th row content
    dbc.Row([
        dbc.Col([dcc.Graph(figure=bairros_proporcao), html.Div([dcc.Markdown("""Ressalta-se a concentração das ocorrências na zona sul do Recife, que contém os 3 bairros com maior número de ocorrências.
""")],
                                                        style={'textAlign': 'center', 'max-width': '640px', 'marginLeft': '40px', 'marginRight':'10px'})],
        xs=7, sm=7, md=7, lg=5, xl=5),
        dbc.Col([dcc.Graph(figure=tipos_metropolitana), html.P("""O gráfico acima destaca tipos de ocorrência com diferenças relevantes de frequência entre a capital e demais municípios.  
                                                               É sugerida, por exemplo, uma maior tendência ao uso do SAMU para emergências obstétricas em municípios comuns.
""",
                                                style={'textAlign': 'center', 'max-width': '640px', 'marginLeft': '70px', 'marginRight':'0px'})],
                xs=7, sm=7, md=7, lg=5, xl=5)

    ], className="g-0",  justify="evenly"),

    # 9th row title
    dbc.Row([html.H4(children='Distribuição das ocorrências conforme horário', style={'textAlign': 'center', 'marginBottom': '1px', 'marginTop':'25px'})]),
    # 9th row content
    dbc.Row([
        dbc.Col([dcc.Graph(figure=horas_dist), html.Div([dcc.Markdown("""O padrão diário observado apresenta maior atividade entre as 8 e as 20 horas, com o maior pico às 10 horas e outro mais suave às 18.  
                                                                      Após as 21 e antes das 5 da manhã, há um número muito menor de ocorrências, com mínimo às 4 horas.
""")],
                                                        style={'textAlign': 'center', 'max-width': '640px', 'marginLeft': '40px', 'marginRight':'10px'})],
        xs=7, sm=7, md=7, lg=5, xl=5),
        dbc.Col([dcc.Graph(figure=sexo_hora_fds), html.P("""Para ambos os sexos, a frequência de ocorrências em fins de semana ultrapassa a de dias da semana a partir das 16 horas, o que se mantém até as 5 da manhã.  
                                                         Ao longo da semana ambos os sexos apresentam o maior pico às 10 da manhã.  
                                                         O sexo masculino apresenta, ainda, pico pronunciado às 17 (18, em fins de semana), o que é menos percebido no sexo feminino.
""",
                                                style={'textAlign': 'center', 'max-width': '640px', 'marginLeft': '70px', 'marginRight':'0px'})],
                ) # xs=7, sm=7, md=7, lg=5, xl=5

    ], className="g-0",  justify="evenly"),
    
    
    # 10th row title
    dbc.Row([html.H4(children='Distribuição nos horários conforme sexo e semana', style={'textAlign': 'center', 'marginBottom': '1px', 'marginTop':'25px'})]),
    # 10th row content
    dbc.Row([
        dbc.Col([dcc.Graph(figure=semana_feminino), html.Div([dcc.Markdown("""O sexo feminino tem a maior incidência de ocorrências na segunda-feira e menor aos sábados.
""")],
                                                        style={'textAlign': 'center', 'max-width': '640px', 'marginLeft': '40px', 'marginRight':'10px'})],
        xs=7, sm=7, md=7, lg=5, xl=5),
        dbc.Col([dcc.Graph(figure=semana_masculino), html.P("""O sexo masculino, por outro lado, apresenta mínimo de ocorrências às quartas e números acima da média de sexta à segunda, com pico aos domingos.
""",
                                                style={'textAlign': 'center', 'max-width': '640px', 'marginLeft': '70px', 'marginRight':'0px'})],
                xs=7, sm=7, md=7, lg=5, xl=5)

    ], className="g-0",  justify="evenly"),
    
    
    # 11st row title
    dbc.Row([html.H4(children='Distribuição da idade dos pacientes', style={'textAlign': 'center', 'marginBottom': '1px', 'marginTop':'25px'})]),
    # 11st row content
    dbc.Row([
        dbc.Col([dcc.Graph(figure=idade_dist), html.Div([dcc.Markdown("""O grande número de pacientes com idade informada de 0 anos indica, de forma mais provável que um elevado número de recém-nascidos, o preenchimento do campo idade com 0 em casos em que não se conhece a idade do paciente.  
                                                                      Analogamente, se vê picos nas idades múltiplas de 5 (e, principalmente, 10), comumente selecionadas para estimar idades não conhecidas de forma precisa.
""")],
                                                        style={'textAlign': 'center', 'max-width': '640px', 'marginLeft': '40px', 'marginRight':'10px'})],
        ), # xs=7, sm=7, md=7, lg=5, xl=5
        dbc.Col([dcc.Graph(figure=idade_violin), html.P("""Nota-se que para o sexo masculino os picos característicos de aproximações de idade desconhecida (múltiplos de 10) são mais pronunciados.  
                                                        Isso indica que em ocorrências com o sexo feminino é mais comum conhecer a idade da paciente.
""",
                                                style={'textAlign': 'center', 'max-width': '640px', 'marginLeft': '70px', 'marginRight':'0px'})],
                ) # xs=7, sm=7, md=7, lg=5, xl=5

    ], className="g-0",  justify="evenly"),
    
    # 12nd row title
    dbc.Row([html.H4(children='Relações entre idade, horário e motivo de finalização/conclusão', style={'textAlign': 'center', 'marginBottom': '1px', 'marginTop':'25px'})]),
    # 12nd row content
    dbc.Row([
        dbc.Col([dcc.Graph(figure=idade_motivo), html.Div([dcc.Markdown("""É possível perceber que os casos em que o serviço de deslocamento acabou não sendo necessário tem médias de idade mais baixas.  
                                                                        Por outro lado, óbitos antes ou durante o atendimento apresentam médias de idade mais altas, onde as taxas de mortalidade são superiores.
""")],
                                                        style={'textAlign': 'center', 'max-width': '640px', 'marginLeft': '40px', 'marginRight':'10px'})],
        ), # xs=7, sm=7, md=7, lg=5, xl=5
        dbc.Col([dcc.Graph(figure=idade_hora), html.P("""A tendência observada ao longo do dia é uma concentração das ocorrências com pacientes de maior idade durante o horário comercial.  
                                                      Com isso, tem-se pacientes médios mais jovens em ocorrências noturnas ou durante a madrugada.
""",
                                                style={'textAlign': 'center', 'max-width': '640px', 'marginLeft': '70px', 'marginRight':'0px'})],
                ) # xs=7, sm=7, md=7, lg=5, xl=5

    ], className="g-0",  justify="evenly"),
    
    # 13rd row title
    dbc.Row([html.H4(children='Médias de idade para cada tipo e subtipo de ocorrência', style={'textAlign': 'center', 'marginBottom': '1px', 'marginTop':'25px'})]),
    # 13rd row content
    dbc.Row([
        dbc.Col([dcc.Graph(figure=idade_tipo), html.Div([dcc.Markdown("""Os tipos de ocorrência com média de idade inferior à geral tendem a ser menos fisiológicas (causas externas, drogas, psiquiátrica).  
                                                                      Como exceção, tem-se as obstétricas, o que reflete o comportamento da idade fértil do sexo biológico feminino.
""")],
                                                        style={'textAlign': 'center', 'max-width': '640px', 'marginLeft': '40px', 'marginRight':'10px'})],
        ), # xs=7, sm=7, md=7, lg=5, xl=5
        dbc.Col([dcc.Graph(figure=idade_subtipo), html.P("""Aqui, as tendências são mais detalhadas: boa parte das doenças físicas tem maiores médias de idade enquanto eventos externos ou psicológicos acometem mais frequentemente os mais jovens.
""",
                                                style={'textAlign': 'center', 'max-width': '640px', 'marginLeft': '70px', 'marginRight':'0px'})],
                ) # xs=7, sm=7, md=7, lg=5, xl=5

    ], className="g-0",  justify="evenly"),
    
   
    
    # CUSTOMIZABLE GRAPHS
    
    
    dbc.Row(html.Hr(style={'border-color': 'lightgray', 'marginBottom':'0px', 'marginTop':'25px'})),
    # 0th row title
    dbc.Row([html.H3(children='Gráficos customizáveis', style={'textAlign': 'center', 'marginBottom': '1px', 'marginTop':'30px', 'color': 'darkcyan', 'fontWeight': 'bold'})]),
    dbc.Row([html.H6(children='(Arraste limites iniciais e finais para restringir faixas de idade, horário e mês)', style={'textAlign': 'center', 'marginBottom': '30px', 'marginTop':'5px', 'color': 'lightskyblue'})]),
    
    dbc.Row([html.H5(children='Filtrar idade', style={'textAlign': 'center', 'marginBottom': '1px', 'marginTop':'10px', 'color': 'darkcyan'})]),
    html.Div([
    # Slider for 'idade' variable
    dcc.RangeSlider(
        id='idade-slider',
        marks={i: str(i) for i in range(df['idade'].min(), df['idade'].max() + 1, 5)},
        min=df['idade'].min(),
        max=df['idade'].max(),
        value=[df['idade'].min(), df['idade'].max()],
    ),
    
    dbc.Row([html.H5(children='Filtrar horário', style={'textAlign': 'center', 'marginBottom': '1px', 'marginTop':'10px', 'color': 'darkcyan'})]),
    # Slider for 'hora' variable
    dcc.RangeSlider(
        id='hora-slider',
        marks={i: str(i) for i in range(df['hora'].min(), df['hora'].max() + 1)},
        min=df['hora'].min(),
        max=df['hora'].max(),
        value=[df['hora'].min(), df['hora'].max()],
    ),
    
    dbc.Row([html.H5(children='Filtrar período', style={'textAlign': 'center', 'marginBottom': '1px', 'marginTop':'10px', 'color': 'darkcyan'})]),
    # Slider for 'dia_hora' variable (assuming dia_hora is a datetime column)
    dcc.RangeSlider(
        id='data-hora-slider',
        marks={idx: date.strftime('%Y-%m') for idx, date in enumerate(pd.date_range(df['dia_hora'].min(), df['dia_hora'].max(), freq='Q'))},
        min=0,
        max=len(pd.date_range(df['dia_hora'].min(), df['dia_hora'].max(), freq='Q')) - 1,
        value=[0, len(pd.date_range(df['dia_hora'].min(), df['dia_hora'].max(), freq='Q')) - 1],
    ),]),
    
    
    # 15th row title
    dbc.Row([html.H4(children='Visualizações do contexto definido pelos filtros selecionados:', style={'textAlign': 'center', 'marginBottom': '1px', 'marginTop':'25px'})]),
    # 15th row content
    dbc.Row([
        dbc.Col([dcc.Graph(id='sexo-pie-chart'), html.Div([dcc.Markdown("""
""")],
                                                        style={'textAlign': 'center', 'max-width': '640px', 'marginLeft': '40px', 'marginRight':'10px'})],
        ), # xs=7, sm=7, md=7, lg=5, xl=5
        dbc.Col([dcc.Graph(id='capital-pie-chart'), html.P("""
""",
                                                style={'textAlign': 'center', 'max-width': '640px', 'marginLeft': '70px', 'marginRight':'0px'})],
                ) # xs=7, sm=7, md=7, lg=5, xl=5

    ], className="g-0",  justify="evenly"),
    
    
    # 16th row content
    dbc.Row([
        dbc.Col([dcc.Graph(id='tipo-subtipo-treemap'), html.Div([dcc.Markdown("""
""")],
                                                        style={'textAlign': 'center', 'max-width': '640px', 'marginLeft': '40px', 'marginRight':'10px'})],
        ), # xs=7, sm=7, md=7, lg=5, xl=5
        dbc.Col([dcc.Graph(id='desfecho-motivo-treemap'), html.P("""
""",
                                                style={'textAlign': 'center', 'max-width': '640px', 'marginLeft': '70px', 'marginRight':'0px'})],
                ) # xs=7, sm=7, md=7, lg=5, xl=5

    ], className="g-0",  justify="evenly"),
    ]
    

    
)


app.title = 'SAMU Data'





# Define callback to update graphs based on slider inputs
@app.callback(
    [Output('sexo-pie-chart', 'figure'),
     Output('tipo-subtipo-treemap', 'figure'),
     Output('desfecho-motivo-treemap', 'figure'),
     Output('capital-pie-chart', 'figure')],
    [Input('idade-slider', 'value'),
     Input('hora-slider', 'value'),
     Input('data-hora-slider', 'value')]
)
def update_graphs(idade_range, hora_range, dia_hora_range):
# Create a date range corresponding to the selected quarters
    # Create a date range corresponding to the selected quarters
    quarters = pd.date_range(df['dia_hora'].min(), df['dia_hora'].max(), freq='Q')
    
    # Ensure that the slider values are integers
    start_idx = int(dia_hora_range[0])
    end_idx = int(dia_hora_range[1])
    
    # Extract the start and end dates from the selected quarters using integer indices
    start_date = quarters[start_idx]
    end_date = quarters[end_idx] + pd.DateOffset(months=2)  # Add 2 months to get the end of the quarter

    filtered_df = df[
        (df['idade'] >= idade_range[0]) & (df['idade'] <= idade_range[1]) &
        (df['hora'] >= hora_range[0]) & (df['hora'] <= hora_range[1]) &
        (df['dia_hora'] >= start_date) &
        (df['dia_hora'] <= end_date)
    ]
    
    
    # Grafico de distribuicao das origens de chamado

    sex_counts = filtered_df['sexo'].value_counts().reset_index()
    sex_counts.columns = ['sexo','count']

    sexo_pie_chart = px.pie(sex_counts, values='count',
        names='sexo',
        hover_name='sexo'
    )

    sexo_pie_chart.update_layout(
        title={
            'text': "Sexo dos pacientes"
        },
        legend=dict(
            orientation="v",
            # yanchor="bottom",
            # y=0.78,
            # xanchor="right",
            # x=1.02,
            bgcolor='rgba(0, 0, 0, 0)'
        )
    )

    sexo_pie_chart.update_traces(hovertemplate = "%{label}: <br>Ocorrências: %{value}")
    
    
    # Tree map for 'tipo' and 'subtipo' variables
    tipo_subtipo_treemap = px.treemap(filtered_df, path=['tipo', 'subtipo'], title='Distribution of Tipo and Subtipo')
    
    # Grafico de distribuicao de tipos e subtipos

    tipo_subtipo_treemap = px.treemap(
        filtered_df, path=['tipo', 'subtipo'],
        color_discrete_map = px.colors.qualitative.Dark2,
        hover_data=['tipo', 'subtipo']
    )

    tipo_subtipo_treemap.update_traces(
        hovertemplate='<b>%{label}</b><br>Percentual da seção: %{percentParent:.2%}',
        textinfo='label+percent root',
        textfont=dict(size=14)
    )
    tipo_subtipo_treemap.update_layout(
        title={
            'text': "Proporção de ocorrências por tipo e subtipo",
            'x': 0.5,  # Center the title
            'xanchor': 'center',
            'yanchor': 'top',
            'y':0.97,
            'font': {'size': 16}  # Adjust the font size for the title,
        }, margin={'t': 10, 'l': 8, 'r': 8, 'b': 8}
    )
    
    
        
    # Grafico das distribuicoes de desfecho e motivo

    tmdf = filtered_df.applymap(lambda x: x if x else ' ')
    tmdf.fillna(' ', inplace=True)

    desfecho_motivo_treemap = px.treemap(
        tmdf, path=['desfecho', 'motivo'],
        color_discrete_map=px.colors.qualitative.Safe,
        color_discrete_sequence=px.colors.qualitative.Safe,
        hover_data=['desfecho', 'motivo']
    )

    desfecho_motivo_treemap.update_traces(
        hovertemplate='<b>%{label}</b><br>Percentual da seção: %{percentParent:.2%}',
        textinfo='label+percent root',
        textfont=dict(size=14)
    )

    desfecho_motivo_treemap.update_layout(
        title={
            'text': 'Resultado ("desfecho") das ocorrências',
            'x': 0.5,  # Center the title
            'xanchor': 'center',
            'yanchor': 'top',
            'y': 0.97,
            'font': {'size': 16}  # Adjust the font size for the title,
        }, margin={'t': 10, 'l': 8, 'r': 8, 'b': 8}
    )
    
    

    


    # Convert 'capital' column to integer type
    filtered_df['capital'] = filtered_df['capital'].astype(int).apply(lambda x: 'Outros municípios' if x == 0 else 'Capital')

    # Grafico de distribuicao das origens de chamado
    city_counts = filtered_df['capital'].value_counts().reset_index()
    city_counts.columns = ['capital','count']

    # Create the pie chart with custom labels for legend and hover text
    newnames = {0: 'Outros municípios', 1: 'Capital'}

    capital_pie_chart = px.pie(city_counts, values='count',
        names='capital',
        hover_name='capital',
    )

    capital_pie_chart.update_layout(
        title={
            'text': "Distribuição de ocorrências na região metropolitana"
        },
    )

    capital_pie_chart.update_traces(hovertemplate="%{label}: <br>Ocorrências: %{value}")

    capital_pie_chart.update_traces(
        hoverinfo='label+percent',  # Display both label and percentage in hover text
        textinfo='label+percent'    # Display both label and percentage on the chart
    )

    # Edit legend labels for understandability
    capital_pie_chart.update_layout(
        legend_title_text='',
    )
    
    
    return sexo_pie_chart, tipo_subtipo_treemap, desfecho_motivo_treemap, capital_pie_chart







if __name__ == '__main__':
    app.run_server(debug=True)