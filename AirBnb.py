import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import os
import pymongo
from PIL import Image
import warnings
import seaborn as sns
import matplotlib.pyplot as plt
import base64


vishnu = pymongo.MongoClient("mongodb+srv://vishnu:vishnu@cluster0.qvjcykt.mongodb.net/")
db = vishnu['sample_airbnb']
col = db['listingsAndReviews'] 


warnings.filterwarnings('ignore')

# Configuring Streamlit GUI

st.set_page_config(layout="wide")
st.title("AirBnb-Analysis")

selected = option_menu(None,
                           options = ["Home","Overview","Data Visualization"],
                           icons = ["house","toggles","clipboard-data"],
                           default_index=0,
                           orientation="horizontal",
                           styles={"container": {"width": "100%"},
                                   "icon": {"color": "white", "font-size": "24px"},
                                   "nav-link": {"font-size": "24px", "text-align": "center", "margin": "-2px"},
                                   "nav-link-selected": {"background-color": "#6F36AD"}})

                                   
# READING THE DATAFRAME
df = pd.read_csv('Airbnbfinal.csv')

# # # MENU 1 - Home
if selected == "Home":
    col1,col2 = st.columns(2)
    with col1:
        
        st.write("Airbnb, is an American company operating an online marketplace for short- and long-term homestays and experiences. The company acts as a broker and charges a commission from each booking. ")
        st.write("The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. Airbnb is a shortened version of its original name, AirBedandBreakfast.com. Airbnb is the most well-known company for short-term housing rentals.")
        st.write("Airbnb connects people with places to stay and things to do around the world. The community is powered by hosts, who provide their guests with the unique opportunity to travel like a local")
    with col2:
        st.image("airbnb.jpg")

#MENU -2 "Explore Data"

#MENU-3 Data Visualization
if selected=="Data Visualization":
    st.title(':violet[Data Visualization]')
    st.write("Users will be able to access the dashboard from a web browser and easily navigate  the different visualizations and facts and figures displayed. The dashboard will provide valuable insights and information about the data, making it a valuable tool for data analysis and decision-making.They are derived from the Analysis of the AirBnb data. It provides a clear idea about the analysed data.")
    options = ["--select--",
               "Top 10 Host Name",
               "Analyzing the prices for the different room and property types.",
               "Analyzing the listings based on room types",
               "Analyzing the listings based on the property type.",
               "Correlation between different variables",
               "Busiest Hosts",
               "Average Listing price in each countries",
               "Anaylzing the listings based on the number of bedrooms",
               "Probability Density Function Graph",
               "Analysis based on Minimum_Nights"]
    select = st.selectbox(":violet[Select the option]",options)
    
    
    #Q1:       
    if select == "Top 10 Host Name":
        col1, col2 = st.columns(2)
        with col1:
            output2=df.groupby(['Host_name']).size().reset_index(name="counts").sort_values(by='counts',ascending=False)[:10]
            st.write(output2)
            st.header("Observations")
            st.write("1.Host name is the name of the host who listed the hotel in airbnb")
            st.write("2.It looks like the person Maria has the largest listings count under 29 bookings")
       
        with col2:
            fig=plt.figure(figsize=(10,8))
            output= sns.countplot(data=df,y=df.Host_name,order=df.Host_name.value_counts().index[:10])
            st.title("Top 10 Host Name")
            st.pyplot(fig)
                   
        
        
    #Q2:
    if select == "Analyzing the prices for the different room and property types.":
        col1, col2 = st.columns(2)
        with col1:
            room_price=df.groupby(['Room_type','Property_type'])['Price'].sum().reset_index()
            output1=room_price.sort_values(by='Price',ascending=False)[:10]
            st.write(output1)
            st.header("Observations")
            st.write("1.We can see that Entire Room/Apt are the most expensive among 3 room types")
            st.write("2.It is also important to note that the highest number of listings which was house and apartments actually have very similar prices for each of the room_type category")
            st.write("3.All of this tells us that the room_type and property_type both play a very important role in the final price of the listing.")
            
        with col2:
            fig = px.pie(df, values='Price',
                             names='Room_type',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Price'],
                             labels={'Room_type':'Price'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
    #Q3:
    if select == "Analyzing the listings based on room types":
        col1, col2 = st.columns(2)
        with col1:
            output2=df.groupby(['Room_type']).size().reset_index(name="counts")
            st.write(output2)
            st.header("Observations")
            st.write("1.As can be seen that most of the listings were Entire Room/Apt")
            st.write("2.There are almost twice as many Entire Home/Apartment listings as Private-Room listings")
            
            
        with col2:
            fig=plt.figure(figsize=(15,3))
            sns.countplot(data=df,x=df.Room_type)
            st.title("Total Listings in each Room Type")
            st.pyplot(fig)
            
    #Q4:
    if select == "Analyzing the listings based on the property type.":
        col1, col2 = st.columns(2)
        with col1:
            output=df.groupby(['Property_type']).size().reset_index(name="counts").sort_values(by='counts',ascending=False)[:10]
            st.write(output)
            st.header("Observations")
            st.write("1.From the above graph we can see that there are a lot more listings of Apartmentm and Full Houses than any other property")
            st.write("2.Together with the early discovery that hosts prefer to list their full property than just a room or shared room")
            
        with col2:
            fig=plt.figure(figsize=(10,8))
            sns.countplot(data=df,y=df.Property_type.values,order=df.Property_type.value_counts().index[:10])
            st.title("Top 10 Property Types available")
            st.pyplot(fig)

    #Q5:
    if select=="Correlation between different variables":
        corr=df.corr(numeric_only=True)
        st.write(corr)
        st.header("Correlation")
        st.write("The strength of the association between two variables can be found from the above table")
        
        
    #Q6:
    if select=="Busiest Hosts":
        col1, col2 = st.columns(2)
        with col1:
            busy=df.groupby(['Host_id','Host_name','Room_type'])['No_of_reviews'].max().reset_index()
            busy1=busy.sort_values(by="No_of_reviews",ascending=False).head(10)
            st.write(busy1)
            st.header("Observations")
            st.write('We find that Listings under the person Dana has highest number of reviews')
        with col2:
            name=busy['Host_name']
            rev=busy['No_of_reviews']
            st.title("Top 10 Hosts with Highest number of Reviews")
            st.bar_chart(data=busy1, x='Host_name', y='No_of_reviews')

    #Q7:
    if select=="Average Listing price in each countries":
        country_df = df.groupby('Country',as_index=False)['Price'].max()
        st.title("Listing Price in each Countries")
        st.scatter_chart(df,x='Country',y='Price',color='Country',size='Price')
        st.header("Observations")
        col1,col2=st.columns([2,15])
        with col1:
            st.image("download.png")
        with col2:
            st.write('From the above plot,we can observe that rent in Hong Kong is quite expensive compared to other cities')
        
    #Q8:
    # Plotting a boxplot to quickly see if there is any trend between price and no. bedrooms
    if select=="Anaylzing the listings based on the number of bedrooms":
        col1,col2=st.columns([7,20])
        with col1:
            st.header("Observations")
            st.write("From the box plots above, it can be seen that listings have higher prices as the number of bedrooms increase")
            
        with col2:
            fig=plt.figure(figsize=(12,12))
            df1 = df.groupby(['Bedrooms','Price']).size().reset_index().sort_values(by='Price',ascending=False)[:10]
            sns.boxplot(data=df,x='Bedrooms',y='Price')
            st.pyplot(fig)
                 
       
    #Q9:
    if select=="Probability Density Function Graph":
        col1,col2=st.columns([7,15])
        with col1:
            st.header("Probability Density Function")
            st.write("The Probability Density Function(PDF) defines the probability function representing the density of a continuous random variable lying between a specific range of values")
        with col2:
            st.write("Probability Distribution")
            fig=plt.figure(figsize=(15,6))
            sns.distplot(df['Price'],color="red")
            st.pyplot(fig)
        
       
    #Q10:
    if select=="Analysis based on Minimum_Nights":
        col1,col2=st.columns([7,15])
        with col1:
            output2=df.groupby(['Minimum_nights']).size().reset_index(name="counts").sort_values(by='counts',ascending=False)[:10]
            st.dataframe(output2)
        with col2:    
            fig=plt.figure(figsize=(5,3))
            sns.countplot(data=df,x='Minimum_nights',order=df['Minimum_nights'].value_counts().index[:10])
            st.title("Analysis based on Minimum_Nights")
            st.pyplot(fig)
      
    
        
# OVERVIEW PAGE
if selected == "Overview":
  
    # original_title = '<h1 style="font-family: serif; color:white; font-size: 20px;">Streamlit CSS Styling✨ </h1>'
    # st.markdown(original_title, unsafe_allow_html=True)
    
    
    # Set the background image
    background_image = """
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-image: url("https://news.airbnb.com/wp-content/uploads/sites/4/2019/06/PJM020719Q202_Luxe_WanakaNZ_LivingRoom_0264-LightOn_R1.jpg?w=2048");
        background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
        background-position: center;  
        background-repeat: no-repeat;
    }
    </style>
    """
    
    st.markdown(background_image, unsafe_allow_html=True)
    
    # st.text_input("", placeholder="Streamlit CSS ")
    
    input_style = """
    <style>
    input[type="text"] {
        background-color: transparent;
        color: #a19eae;  // This changes the text color inside the input box
    }
    div[data-baseweb="base-input"] {
        background-color: transparent !important;
    }
    [data-testid="stAppViewContainer"] {
        background-color: transparent !important;
    }
    </style>
    """
    st.markdown(input_style, unsafe_allow_html=True)


       
    tab1,tab2 = st.tabs(["$\huge 📝 RAW DATA $", "$\huge🚀 INSIGHTS $"])
    
    # RAW DATA TAB
    with tab1:
        # RAW DATA
        col1,col2 = st.columns(2)
        if col1.button("Click to view Raw data"):
            col1.write(col.find_one())
        # DATAFRAME FORMAT
        if col2.button("Click to view Dataframe"):
            col1.write(col.find_one())
            col2.write(df)
# INSIGHTS TAB
    with tab2:
        # GETTING USER INPUTS
        country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
        prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
        room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
        price = st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))
        
        # CONVERTING THE USER INPUT INTO QUERY
        query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
        
        # CREATING COLUMNS
        col1,col2 = st.columns(2,gap='medium')
        
        with col1:
            
            # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
            country_df = df.query(query).groupby(['Country'],as_index=False)['Name'].count().rename(columns={'Name' : 'Total_Listings'})
            fig = px.choropleth(country_df,
                                title='Total Listings in each Country',
                                locations='Country',
                                locationmode='country names',
                                color='Total_Listings',
                                color_continuous_scale=px.colors.sequential.Plasma
                               )
            st.plotly_chart(fig,use_container_width=True)
           
            c=pd.pivot_table(df, index='Country', columns='Room_type', values='Price')
            st.bar_chart(c)
            
        with col2:
            df1 = df.groupby(['Country'],as_index=False)['Price'].sum().rename(columns={'Name' : 'Price'})
            fig = px.choropleth(df1,
                                title='Price in each Country',
                                locations='Country',
                                locationmode='country names',
                                color='Price',
                                color_continuous_scale=px.colors.sequential.Cividis_r
                               )
            st.plotly_chart(fig,use_container_width=True)
            
            # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
            df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name="counts")
            fig = px.pie(df1,
                         title='Total Listings in each Room_types',
                         names='Property_type',
                         values='counts',
                         color_discrete_sequence=px.colors.sequential.Rainbow
                        )
            fig.update_traces(textposition='outside', textinfo='value+label')
            st.plotly_chart(fig,use_container_width=True)
            


        