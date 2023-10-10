# IMPORTING REQUIRED LIBRARIES
import pandas as pd
import pymongo
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu

# SETTING THE PAGE CONFIGURATION
st.set_page_config(
    layout="wide",  # Use "wide" layout
)

# CREATING OPTION MENU
selected = option_menu(menu_title = "Airbnb Analysis",
                       options = ["Home", "Overview", "Insights", "Explore"], 
                           icons=["house","graph-up-arrow","lightbulb", "bar-chart-line"],
                           menu_icon= "menu-button-wide",
                           default_index=0,
                           orientation = "horizontal"
                          )

# CREATING CONNECTION WITH MONGODB ATLAS AND RETRIEVING THE DATA
client = pymongo.MongoClient("Your Client ID")
db = client['sample_airbnb']
col = db['listingsAndReviews']

# READING THE CLEANED DATAFRAME
df = pd.read_csv('C:\\Users\\HP\\Desktop\\GUVI Projects\\Airbnb Project\\Airbnb_data.csv')

# HOME PAGE
if selected == "Home":
    col1,col2 = st.columns(2,gap= 'medium')
    col1.image("Airbnblogo.png")
    col2.markdown("### :blue[Domain] : Travel Industry, Property Management and Tourism")
    col2.markdown("### :blue[Technologies used] : Python, Pandas, Plotly, Streamlit, MongoDB")
    col2.markdown("### :blue[Overview] : To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")
    col2.markdown("#   ")
    col2.markdown("#   ")
    

# OVERVIEW PAGE
if selected == "Overview":

    # CREATING COLUMNS    
    col1,col2 = st.columns(2)

    # DISPLAY THE RAW DATA
    if col1.button("Click to view Raw data"):
        col1.write(col.find_one())
    # DISPLAY THE DATAFRAME FORMAT
    if col2.button("Click to view Dataframe"):
        col2.write(df)

if selected == "Insights":
        
    # CREATING COLUMNS
    col1,col2 = st.columns(2,gap='medium')  

    with col1:
            
        # TOP 10 PROPERTY TYPES BAR CHART
        top_property_types = df['Property_type'].value_counts().head(10)

        fig1 = px.bar(
            x=top_property_types.values,
            y=top_property_types.index,
            orientation='h',
            title="Top 10 Property Types available",
            labels={"x": "Count", "y": "Property Type"},
        )
        fig1.update_layout(yaxis_autorange='reversed')
        st.plotly_chart(fig1)

        # TOP 10 HOSTS BAR CHART
        top_hosts = df['Host_name'].value_counts().head(10)
        
        fig2 = px.bar(
            x=top_hosts.values,
            y=top_hosts.index,
            orientation='h',
            title="Top 10 Hosts",
            labels={"x": "Count", "y": "Host Name"},
        )
        fig2.update_layout(yaxis_autorange='reversed')
        st.plotly_chart(fig2)
    
    with col2:
        
        # COUNTRY WISE PRICING 
        country_df = df.groupby('Country',as_index=False)['Price'].mean()
        country_names = country_df['Country']
        prices = country_df['Price']

        fig3 = px.bar(
            data_frame=country_df,
            x='Country',
            y='Price',
            title='Average Listing Price in Each Country',
            labels={'Country': 'Country', 'Price': 'Price'},
        )
        fig3.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig3)

# EXPLORE PAGE
if selected == "Explore":
    st.markdown("## Explore more about the Airbnb data")
    
    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
    prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
    price = st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))
    
    # CONVERTING THE USER INPUT INTO QUERY
    query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
    
    # HEADING 1
    st.markdown("## Price Analysis")
    
    # CREATING COLUMNS
    col1,col2 = st.columns(2,gap='medium')
    
    with col1:
        
        # AVG PRICE BY ROOM TYPE BARCHART
        pr_df = df.query(query).groupby('Room_type',as_index=False)['Price'].mean().sort_values(by='Price')
        fig = px.bar(data_frame=pr_df,
                     x='Room_type',
                     y='Price',
                     color='Price',
                     title='Avg Price in each Room type'
                    )
        st.plotly_chart(fig,use_container_width=True)
        
        # HEADING 2
        st.markdown("## Availability Analysis")
        
        # AVAILABILITY BY ROOM TYPE BOX PLOT
        fig = px.box(data_frame=df.query(query),
                     x='Room_type',
                     y='Availability_365',
                     color='Room_type',
                     title='Availability by Room_type'
                    )
        st.plotly_chart(fig,use_container_width=True)
        
    with col2:
        
        # AVG PRICE IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('Country',as_index=False)['Price'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Price', 
                                       hover_data=['Price'],
                                       locationmode='country names',
                                       size='Price',
                                       title= 'Avg Price in each Country',
                                       color_continuous_scale='agsunset'
                            )
        col2.plotly_chart(fig,use_container_width=True)
        
        # BLANK SPACE
        st.markdown("#   ")
        st.markdown("#   ")
        
        # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('Country',as_index=False)['Availability_365'].mean()
        country_df.Availability_365 = country_df.Availability_365.astype(int)
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Availability_365', 
                                       hover_data=['Availability_365'],
                                       locationmode='country names',
                                       size='Availability_365',
                                       title= 'Avg Availability in each Country',
                                       color_continuous_scale='agsunset'
                            )
        st.plotly_chart(fig,use_container_width=True)
