import streamlit as st
import pandas as pd
import plotly.express as px

st.write("""
Ecological Footprint Data
""")
df = pd.read_csv('NFA.csv')

option = st.sidebar.selectbox( label =  'Visualizations',options = ('World', 'Year and Region'))
if option == 'Year and Region':
       year = st.sidebar.slider('Year',df['year'].min(), df['year'].max())
       record = st.sidebar.selectbox(label='Record',options=df['record'].unique())
       col1, col2= st.columns(2)
       col1.metric(label="Year", value=year)
       col2.metric(label="Record", value=record)
       df_year_record = df[(df['year']==year) & (df['record']==record)]

       df_pop = df_year_record[['country','population','ISO alpha-3 code']]
       df_land = df_year_record[['country', 'crop_land', 'grazing_land', 'forest_land', 'fishing_ground',
              'built_up_land', 'carbon','total']].dropna(subset=['crop_land', 'grazing_land', 'forest_land', 'fishing_ground',
              'built_up_land', 'carbon','total'])
       df_non_world = df_year_record[df_year_record['country']!='World']
       df_land.sort_values(by='total',ascending=False,inplace=True)
       df_land = df_land[['country', 'crop_land', 'grazing_land', 'forest_land', 'fishing_ground',
              'built_up_land', 'carbon']]

       df_land.set_index('country',inplace=True)


       st.bar_chart(df_land.head(10))
       st.bar_chart(df_land.tail(10))# download countries geojson file

       st.plotly_chart(px.choropleth(df_pop, locations="ISO alpha-3 code",
                           color="population", # lifeExp is a column of gapminder
                           hover_name="country", # column to add to hover information
                           color_continuous_scale=px.colors.sequential.Cividis_r))
       st.plotly_chart(px.choropleth(df_non_world,locations="ISO alpha-3 code",hover_name="country",color="total",height=500))



       st.plotly_chart(px.scatter(df_non_world, x="population", y="Percapita GDP (2010 USD)",
                    size="population", color="UN_region",
                        hover_name="country", log_x=True, size_max=60))

       st.plotly_chart(px.scatter(df_non_world,y="total",x="Percapita GDP (2010 USD)",hover_name="country",height=500,color="UN_region",\
                  size="population",size_max=60,log_x=True))
elif option == 'World':
       df_world = df[(df['country']=='World')]
       st.plotly_chart(px.line(pd.pivot_table(df_world,values = 'total',index=['year'],columns=['record'],aggfunc='sum')[['BiocapPerCap','EFConsPerCap']]))
       st.plotly_chart(px.line(pd.pivot_table(df_world,values = 'total',index=['year'],columns=['record'],aggfunc='sum')[['BiocapPerCap','EFConsPerCap']]))
