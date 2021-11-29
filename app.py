import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Ecological Footprint per Capita Dataset visualization")

df = pd.read_csv('NFA.csv')
option = st.sidebar.selectbox( label =  'Visualizations',options = ('World', 'Year and Record'))
if option == 'Year and Record':
       min_year = 1961
       max_year = 2014
       year = st.sidebar.slider('Year',min_value = min_year, max_value = max_year,step=1)
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

       st.write(record +'Top 10 countries by total area land distribution and carbon emission for year '+ str(year))
       st.bar_chart(df_land.head(10))
       st.write(record + 'Bottom 10 countries by total area land distribution and carbon emission for year' + str(year))
       st.bar_chart(df_land.tail(10))# download countries geojson file

       st.plotly_chart(px.choropleth(df_pop, locations="ISO alpha-3 code",
                           color="population", # lifeExp is a column of gapminder
                           hover_name="country", # column to add to hover information
                           color_continuous_scale=px.colors.sequential.Cividis_r,
                           title = "Countrywise Population in the year "+str(year)))
       st.plotly_chart(px.choropleth(df_non_world,locations="ISO alpha-3 code",hover_name="country",color="total",height=500,title=record +" for countries during the year  "+str(year)))



       st.plotly_chart(px.scatter(df_non_world, x="population", y="Percapita GDP (2010 USD)",
                    size="population", color="UN_region",
                        hover_name="country", log_x=True, size_max=60,  title = "Population vs Percapita GDP in year "+str(year)))

       st.plotly_chart(px.scatter(df_non_world,y="total",x="Percapita GDP (2010 USD)",hover_name="country",height=500,color="UN_region",\
                  size="population",size_max=60,log_x=True,title = "Total land vs Percapita GDP in year "+str(year)))

elif option == 'World':
       df_world = df[(df['country']=='World')]
       df_non_world = df[df['country'] != 'World']
       st.plotly_chart(px.line(pd.pivot_table(df_world,values = 'total',index=['year'],columns=['record'],aggfunc='sum')[['BiocapPerCap','EFConsPerCap']]))
       st.plotly_chart(px.line(pd.pivot_table(df_world,values = 'total',index=['year'],columns=['record'],aggfunc='sum')[['BiocapTotGHA','EFConsTotGHA']]))
       st.plotly_chart(px.line(df_world[df_world['record']=='EFConsTotGHA'], x="year",
               y=["carbon", "crop_land", "grazing_land", "fishing_ground", "forest_land", "built_up_land"], \
               title='Evolution of the total Consumption per land type as well as Carbon Emission for the world',
               labels={"value": "Total EF Consumption (GHA)"}))
       st.plotly_chart(px.line(df_world[df_world['record']=='EFConsPerCap'], x="year", y=["carbon"], \
               title='Evolution of the carbon emission per capita for the world',
               labels={"value": "Carbon emission per capita (GHA)"}))

       pt1 = (pd.pivot_table(df_non_world,values = 'total',index=['UN_region', 'year'],columns=['record'],aggfunc='sum')\
              [['BiocapTotGHA','EFConsTotGHA']].reset_index().set_index('UN_region'))
       pt2 = \
       pd.pivot_table(df_non_world, values='population', index=['UN_region', 'year'], columns=['record'], aggfunc='sum') \
           [['BiocapTotGHA']].rename(index=str, columns={'BiocapTotGHA': 'population'}).reset_index().drop(['year'],
                                                                                                           axis=1) \
           .set_index('UN_region')
       result_pt = pd.concat([pt1, pt2], axis=1)
       result_pt['BiocapPerCap_region'] = result_pt['BiocapTotGHA'] / result_pt['population']
       result_pt['EFConsPerCap_region'] = result_pt['EFConsTotGHA'] / result_pt['population']
       regional = result_pt.reset_index()
       reserve_deficit = regional.groupby(['UN_region', 'year'])[
           ['BiocapPerCap_region', 'EFConsPerCap_region']].sum().reset_index()
       min_year = 1961
       max_year = 2014
       year = st.slider('Year', min_value=min_year, max_value=max_year, step=1)
       reserve_deficit_year = reserve_deficit[reserve_deficit['year'] == year]
       reserve_deficit_year['reserve_or_deficit'] = reserve_deficit_year['BiocapPerCap_region'] - reserve_deficit_year[
           'EFConsPerCap_region']
       final = reserve_deficit_year.reset_index()
       st.plotly_chart(px.bar(final, x="reserve_or_deficit", y="UN_region", orientation='h', color='reserve_or_deficit'
              , title='Regional Biocapacity Reserve(+) or Deficit(-)'
              , labels={"UN_region": "World's Regions",
                        "reserve_or_deficit": "Biocapacity Reserve or Deficit Per Capita - "+str(year)}))