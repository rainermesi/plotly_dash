import plotly.express as px
import pandas as pd

#data
df = pd.read_csv('/home/rainermesi/Documents/f_min_scrape/union_001.csv')
df_bc = df[df['load_dt'] == (max(df['load_dt']))]
df_bc['index_cd'] = ['>16' if x > 16 else '<=16' for x in df_bc['metric']]
df_bc = df_bc.sort_values('metric',ascending=True)
df_iso_cd = pd.read_csv('/home/rainermesi/Documents/f_min_scrape/country_cd_iso.csv',delimiter=';')
df_merged = pd.merge(df_bc,df_iso_cd,how='left',on='country')


#charts
fig_bc = px.bar(df_bc,x='country',y='metric',color='index_cd',
                color_discrete_map={
                    '>16':'red',
                    '<=16':'blue'
                })
fig_bc.update_xaxes(title='')
fig_bc.update_yaxes(title='')
fig_bc.update_layout(legend_title_text='')

fig_lc = px.line(
    df,
    x='load_dt',
    y='metric',
    facet_col='country',
    facet_col_wrap=6,
    height=1100,
    facet_row_spacing=0.04
)
fig_lc.update_yaxes(matches=None,title='')
fig_lc.for_each_annotation(lambda a: a.update(text=a.text.split('=')[-1]))
fig_lc.update_xaxes(title='')


fig_mp = px.choropleth(df_merged,locations='iso_cd',
                    color='metric',
                    hover_name='country',
                    scope='europe',
                    range_color=(0,16),
                    color_continuous_scale=px.colors.sequential.Peach)
fig_mp.update_layout(coloraxis_showscale=False)

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# for deployment, pass app.server (which is the actual flask app) to WSGI etc
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H3("Välisministeeriumi andmed liikumispiirangute kohta Eestisse saabujatele"))),
    html.Hr(),
    dbc.Row(),
    dbc.Row(dbc.Col(html.P(["Viimase 14 päeva lisandunud nakatunud 100 tuhande elaniku kohta.",html.Br(),"Andmed uuenevad korra päevas Välisministeeriumi kodulehelt (https://vm.ee/et/teave-riikide-ja-eneseisolatsiooninouete-kohta-euroopast-saabujatele).",html.Br(),"Kõik Eestisse saabuvad isikud, kes alustasid reisiteekonda riikidest või läbisid riike, mille koroonaviirusesse nakatanute suhtarv on suurem kui 16 on kohustatud oma liikusmisvabadust 14 päeva piirama."]))),
    dbc.Row(),
    dbc.Row(
        [
            dbc.Col(html.Div([dcc.Graph(id='bc',figure=fig_bc)])),
            dbc.Col(html.Div([dcc.Graph(id='mp',figure=fig_mp)]), width=4)
        ]
    ),
    dbc.Row(dbc.Col(html.H6("Andmed ajajoonel riigi kaupa. Eelneva 14 päevajooksul lisandunud nakatunud 100 tuhande elaniku kohta."))),
    dbc.Row(dbc.Col(html.Div(dcc.Graph(id='lc',figure=fig_lc))))
    ], fluid=True
)

