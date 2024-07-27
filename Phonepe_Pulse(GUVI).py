# Importing necessary libraries
import pandas as pd
import sqlite3
import streamlit as st
import plotly.express as px
from PIL import Image

# Setting up page configuration
icon = Image.open(r"C:\Users\vardhan\Desktop\PhonePePulse\Image.png")
st.set_page_config(
    page_title="PhonePe Pulse - Project By Vardhan Choudhary",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': """ Project by Vardhan Choudhary"""
    }
)

# SQLite Connection
conn = sqlite3.connect('phonepe_pulse.db')

# Sidebar menu
st.sidebar.header(":wave: :violet[**WELCOME**]")

# Option menu in the sidebar
selected = st.sidebar.selectbox(
    "Menu",
    ["Home", "Top Charts", "Explore Data", "About"],
    index=0
)

# MENU 1 - HOME
if selected == "Home":
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    st.markdown("### :violet[Domain :] Fintech")
    st.markdown("### :violet[Technologies used :] GitHub Cloning, Python, Pandas, SQLite, Streamlit, and Plotly")
    st.markdown("### :violet[Overview :] In this Streamlit web app, you can visualize PhonePe Pulse data")

# MENU 2 - TOP CHARTS
elif selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))

    # Year and Quarter selection
    col1, col2 = st.columns([1, 1.5])
    with col1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022, key="top_charts_year")
        Quarter = st.slider("Quarter", min_value=1, max_value=4, key="top_charts_quarter")

    # Information about top charts
    with col2:
        st.info(
            """
            #### From this menu, you can get insights like:
            - Overall ranking for a particular Year and Quarter.
            - Top 10 State, District, Pincode based on Total number of transactions and Total amount spent on PhonePe.
            - Top 10 State, District, Pincode based on Total PhonePe users and their app opening frequency.
            - Top 10 mobile brands and their percentage based on how many people use PhonePe.
            """,
            icon="🔍"
        )

    # Top Charts - TRANSACTIONS
    if Type == "Transactions":
        col1, col2, col3 = st.columns([1, 1, 1])

        # Top States by Transactions
        with col1:
            st.markdown("### :violet[State]")
            query = f"SELECT State, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total FROM aggregated_transaction WHERE year = {Year} AND quarter = {Quarter} GROUP BY State ORDER BY Total DESC LIMIT 10"
            df = pd.read_sql(query, conn)
            fig = px.pie(df, values='Total',
                         names='State',
                         title='Top 10 States',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Transactions_Count'],
                         labels={'Total_Transactions_Count': 'Transactions Count'})
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        # Top Districts by Transactions
        with col2:
            st.markdown("### :violet[District]")
            query = f"SELECT District, sum(Transaction_count) as Total_Count, sum(Transaction_amount) as Total FROM map_transaction WHERE year = {Year} AND quarter = {Quarter} GROUP BY District ORDER BY Total DESC LIMIT 10"
            df = pd.read_sql(query, conn)
            fig = px.pie(df, values='Total',
                         names='District',
                         title='Top 10 Districts',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Count'],
                         labels={'Total_Count': 'Transactions Count'})
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        # Top Pincodes by Transactions
        with col3:
            st.markdown("### :violet[Pincode]")
            query = f"SELECT District_Pincode as Pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total FROM top_transaction WHERE year = {Year} AND quarter = {Quarter} GROUP BY District_Pincode ORDER BY Total DESC LIMIT 10"
            df = pd.read_sql(query, conn)
            fig = px.pie(df, values='Total',
                         names='Pincode',
                         title='Top 10 Pincodes',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Transactions_Count'],
                         labels={'Total_Transactions_Count': 'Transactions Count'})
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    # Top Charts - USERS
    elif Type == "Users":
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

        # Top Brands by Users
        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2, 3, 4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2, 3, 4")
            else:
                query = f"SELECT Brands, sum(User_Count) as Total_Users, avg(User_Percentage)*100 as Avg_Percentage FROM aggregated_user WHERE year = {Year} AND quarter = {Quarter} GROUP BY Brands ORDER BY Total_Users DESC LIMIT 10"
                df = pd.read_sql(query, conn)
                fig = px.bar(df, x="Total_Users", y="Brands", orientation='h', color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset,
                             title='Top 10 Brands by Users')
                st.plotly_chart(fig, use_container_width=True)

        # Top Districts by Users
        with col2:
            st.markdown("### :violet[District]")
            query = f"SELECT District, sum(Registered_User) as Total_Users FROM map_user WHERE year = {Year} AND quarter = {Quarter} GROUP BY District ORDER BY Total_Users DESC LIMIT 10"
            df = pd.read_sql(query, conn)
            fig = px.bar(df, x="Total_Users", y="District", orientation='h', color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset,
                         title='Top 10 Districts by Users')
            st.plotly_chart(fig, use_container_width=True)

        # Top Pincodes by Users
        with col3:
            st.markdown("### :violet[Pincode]")
            query = f"SELECT District_Pincode as Pincode, sum(Registered_User) as Total_Users FROM top_user WHERE year = {Year} AND quarter = {Quarter} GROUP BY District_Pincode ORDER BY Total_Users DESC LIMIT 10"
            df = pd.read_sql(query, conn)
            fig = px.pie(df, values='Total_Users', names='Pincode', title='Top 10 Pincodes by Users',
                         color_discrete_sequence=px.colors.sequential.Agsunset, hole=0.3)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        # Top States by Users
        with col4:
            st.markdown("### :violet[State]")
            query = f"SELECT State, sum(Registered_User) as Total_Users FROM map_user WHERE year = {Year} AND quarter = {Quarter} GROUP BY State ORDER BY Total_Users DESC LIMIT 10"
            df = pd.read_sql(query, conn)
            fig = px.pie(df, values='Total_Users', names='State', title='Top 10 States by Users',
                         color_discrete_sequence=px.colors.sequential.Agsunset, hole=0.3)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

# MENU 3 - EXPLORE DATA
if selected == "Explore Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1, col2 = st.columns(2)

    # EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            query = f"SELECT State, SUM(Transaction_Count) AS Total_Transactions, SUM(Transaction_Amount) AS Total_amount FROM map_transaction WHERE Year = {Year} AND Quarter = {Quarter} GROUP BY State ORDER BY State"
            df1 = pd.read_sql(query, conn)
            df2 = pd.read_csv(r"C:\Users\vardhan\Desktop\PhonePePulse\States.csv")
            df1['State'] = df2['State']

            fig = px.choropleth(
                df1,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='Total_amount',
                color_continuous_scale='sunset'
            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            query = f"SELECT State, SUM(Transaction_Count) AS Total_Transactions, SUM(Transaction_Amount) AS Total_amount FROM map_transaction WHERE Year = {Year} AND Quarter = {Quarter} GROUP BY State ORDER BY State"
            df1 = pd.read_sql(query, conn)
            df2 = pd.read_csv(r"C:\Users\vardhan\Desktop\PhonePePulse\States.csv")
            df1['Total_Transactions'] = df1['Total_Transactions'].astype(int)
            df1['State'] = df2['State']

            fig = px.choropleth(
                df1,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='Total_Transactions',
                color_continuous_scale='sunset'
            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

        # BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        query = f"SELECT Transaction_type, SUM(Transaction_count) AS Total_Transactions, SUM(Transaction_amount) AS Total_amount FROM aggregated_transaction WHERE Year = {Year} AND Quarter = {Quarter} GROUP BY Transaction_type ORDER BY Transaction_type"
        df = pd.read_sql(query, conn)

        fig = px.bar(
            df,
            title='Transaction Types vs Total_Transactions',
            x="Transaction_type",
            y="Total_Transactions",
            orientation='v',
            color='Total_amount',
            color_continuous_scale=px.colors.sequential.Agsunset
        )
        st.plotly_chart(fig, use_container_width=False)

        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("", (
            'andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar',
            'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana',
            'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
            'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry',
            'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand',
            'west-bengal'), index=30)

        query = f"SELECT State, District, Year, Quarter, SUM(Transaction_Count) AS Total_Transactions, SUM(Transaction_Amount) AS Total_amount FROM map_transaction WHERE Year = {Year} AND Quarter = {Quarter} AND State = '{selected_state}' GROUP BY State, District, Year, Quarter ORDER BY State, District"
        df1 = pd.read_sql(query, conn)
        fig = px.bar(
            df1,
            title=selected_state,
            x="District",
            y="Total_Transactions",
            orientation='v',
            color='Total_amount',
            color_continuous_scale=px.colors.sequential.Agsunset
        )
        st.plotly_chart(fig, use_container_width=True)

    # EXPLORE DATA - USERS      
    if Type == "Users":
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        query = f"SELECT State, SUM(Registered_User) AS Total_Users FROM map_user WHERE Year = {Year} AND Quarter = {Quarter} GROUP BY State ORDER BY State"
        df1 = pd.read_sql(query, conn)
        df2 = pd.read_csv(r"C:\Users\vardhan\Desktop\PhonePePulse\States.csv")
        df1['Total_Appopens'] = df1['Total_Users'].astype(float)
        df1['State'] = df2['State']

        # BAR CHART TOTAL USERS - DISTRICT WISE DATA 
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("", (
            'andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar',
            'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana',
            'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
            'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry',
            'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand',
            'west-bengal'), index=30)

        query = f"SELECT State, Year, Quarter, District, SUM(Registered_User) AS Total_Users FROM map_user WHERE Year = {Year} AND Quarter = {Quarter} AND State = '{selected_state}' GROUP BY State, District, Year, Quarter ORDER BY State, District"
        df = pd.read_sql(query, conn)
        df['Total_Users'] = df['Total_Users'].astype(int)

        fig = px.bar(
            df,
            title=selected_state,
            x="District",
            y="Total_Users",
            orientation='v',
            color='Total_Users',
            color_continuous_scale=px.colors.sequential.Agsunset
        )
        st.plotly_chart(fig, use_container_width=True)




# MENU 4 - ABOUT
elif selected == "About":
    st.markdown("# :violet[About]")
    st.markdown("## :violet[PhonePe Pulse Project]")
    st.markdown("### :violet[Author :] Vardhan Choudhary")
    st.markdown("### :violet[Description :] This Streamlit web app visualizes and explores PhonePe Pulse data using Plotly charts.")
    st.markdown("### :violet[Tools :] Python, Streamlit, Plotly, SQLite")
    st.markdown("### :violet[Date Created :] July 2024")

# Closing SQLite connection
conn.close()
