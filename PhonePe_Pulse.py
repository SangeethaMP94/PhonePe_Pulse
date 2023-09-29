import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from PIL import Image
import webbrowser
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="PhonePe Data Visualization",
    page_icon="chart_with_upwards_trend",
    initial_sidebar_state="expanded",)

with st.sidebar:
   main = option_menu(None, ["Home","About","Visualization","Map_Visualization"],menu_icon='cast')

if main == "Home":
    st.title(":violet[PHONEPE PULSE DATA VISUALIZATION]")
    url = "https://download.logo.wine/logo/PhonePe/PhonePe-Logo.wine.png"
    st.image(url)

if main == "About":
    st.title(":violet[ABOUT]")
    st.markdown("### Welcome to the PhonePe Pulse Dashboard ,This PhonePe Pulse Data Visualization and Exploration dashboard is a user-friendly tool designed to provide insights and information about the data in the PhonePe Pulse GitHub repository. This dashboard offers a visually appealing and interactive interface for users to explore various metrics and statistics.")
    st.write("Email Id: sangeethamp94@gmail.com")
    st.write("Linkedin Id: https://www.linkedin.com/in/sangeetha-m-a66aa1251/")

mydb = psycopg2.connect(host = 'localhost',user = 'postgres',password = 'Sangeetha@2000',port = 5432,database = 'Phonepe')
mycursor = mydb.cursor()


if main== "Visualization":
   with st.sidebar:
      main1 = option_menu(None, ["Transactions","Users"],menu_icon='cast')

   if main1 == "Transactions":
        with st.sidebar:
          Topic = ["Aggregated","Map","Top"]
          select_topic = st.selectbox("Transactions", Topic)

        with st.sidebar:
          Topic = ["2018","2019","2020","2021","2022"]
          year = st.selectbox("Year",Topic)
          Topic = ["1","2","3","4"]
          quarter = st.selectbox("Quarter",Topic)
         
        if select_topic == "Aggregated":     
              st.title("Aggregated Transactions")        
              mycursor.execute(f"SELECT State,Transaction_amount,Total_transaction,Transaction_type FROM aggregated_transactions  where Year = {year} and Quarter = {quarter} order by transaction_amount desc limit 10")
              records1 = mycursor.fetchall()
              aggregated_transactions = pd.DataFrame(records1,
                                              columns=[i[0] for i  in mycursor.description])
              st.dataframe(aggregated_transactions)

              df = px.bar(aggregated_transactions,
                                                x = 'state',
                                                y = 'transaction_amount',
                                                color = 'total_transaction',
                                                title='Aggregrated_Transaction',
                                                color_continuous_scale='oranges' )
              df.update_traces(width = 0.8)
              st.plotly_chart(df)

              fig = px.scatter (aggregated_transactions,
                                x = 'transaction_type', 
                                y = 'total_transaction',
                                color = 'state')
              st.plotly_chart(fig)

        if select_topic == "Map":             
                    st.title("Map Transactions")
                    mycursor.execute(f"SELECT State,Amount,District,Count FROM map_transactions where Year = {year} and Quarter = {quarter} order by Amount desc limit 10")
                    records2 = mycursor.fetchall()
                    map_transactions = pd.DataFrame(records2,
                                                    columns=[i[0] for i  in mycursor.description])
                    st.dataframe(map_transactions)

                    df = px.bar(map_transactions,
                                        x = 'district',
                                        y = 'amount',
                                        color = 'state',
                                        title='Map_Transaction',
                                        color_continuous_scale='reds')
                    df.update_traces(width = 0.8)
                    st.plotly_chart(df)

                    fig = px.scatter (map_transactions,
                                      x = 'district', 
                                      y = 'count',
                                      color = 'state')
                    st.plotly_chart(fig)

        if select_topic == "Top":
                    st.title("Top Transactions")             
                    mycursor.execute(f"SELECT State,Amount,District,Topuser_count FROM top_transactions where Year = {year} and Quarter = {quarter} order by Amount desc limit 10")
                    records3 = mycursor.fetchall()
                    top_transaction = pd.DataFrame(records3,
                                                    columns=[i[0] for i  in mycursor.description])
                    st.dataframe(top_transaction)

                    df = px.bar(top_transaction,
                                        x = 'district',
                                        y = 'amount',
                                        color = 'state',
                                        title='Top_Transaction',
                                        color_continuous_scale='thermal')
                    df.update_traces(width = 0.8)
                    st.plotly_chart(df)

                    fig = px.scatter (top_transaction,
                                      x = 'district', 
                                      y = 'topuser_count',
                                      color = 'state')
                    st.plotly_chart(fig)

   if main1 == "Users":
        with st.sidebar:
          Topic = ["Aggregated","Map","Top"]
          select_topic = st.selectbox("Users", Topic)

        with st.sidebar:
          Topic = ["2018","2019","2020","2021","2022"]
          year = st.selectbox("Year",Topic)
          Topic = ["1","2","3","4"]
          quarter = st.selectbox("Quarter",Topic)
         
        if select_topic == "Aggregated":
                    st.title("Aggregated Users")             
                    mycursor.execute(f"SELECT State,User_brand,Count,Percentage FROM aggregated_user1  where Year = {year} and Quarter = {quarter} order by count desc limit 10")
                    records4 = mycursor.fetchall()
                    aggregated_user1 = pd.DataFrame(records4,
                                                    columns=[i[0] for i  in mycursor.description])
                    st.dataframe(aggregated_user1)
                    
                    fig = go.Figure(go.Scatter(x=aggregated_user1['state'],
                                                y=aggregated_user1['user_brand'], 
                                                mode='markers+text+lines',
                                                text=aggregated_user1['count'],
                                                textposition="bottom left"))
                    st.plotly_chart(fig)
                    
                    fig = px.pie(aggregated_user1, names = "user_brand",values = "percentage")
                    st.plotly_chart(fig)

          
        if select_topic == "Map":      
                    st.title("Map Users")       
                    mycursor.execute(f"SELECT State,Register_users,District,App_open FROM map_users  where Year = {year} and Quarter = {quarter} order by app_open desc limit 10")
                    records5 = mycursor.fetchall()
                    map_users = pd.DataFrame(records5,
                                                    columns=[i[0] for i  in mycursor.description])
                    st.dataframe(map_users)
                    
                    fig = go.Figure(go.Scatter(x=map_users['district'],
                                                y=map_users['app_open'], 
                                                mode='markers+text+lines',
                                                text=map_users['register_users'],
                                                textposition="bottom left"))
                    st.plotly_chart(fig)
                    
                    fig = px.pie(map_users, names = "district",values = "register_users")
                    st.plotly_chart(fig)

        if select_topic == "Top":
                    st.title("Top Users")             
                    mycursor.execute(f"SELECT State,Register_users,District FROM top_users  where Year = {year} and Quarter = {quarter} order by register_users desc limit 10")
                    records6 = mycursor.fetchall()
                    top_users = pd.DataFrame(records6,
                                                    columns=[i[0] for i  in mycursor.description])
                    st.dataframe(top_users)
                    
                    fig = go.Figure(go.Scatter(x=top_users['district'],
                                                y=top_users['state'], 
                                                mode='markers+text+lines',
                                                text=top_users['register_users'],
                                                textposition="bottom left"))
                    st.plotly_chart(fig)
                    
                    fig = px.pie(top_users, names = "district",values = "register_users")
                    st.plotly_chart(fig)
                 
if main == "Map_Visualization":
      state = pd.read_csv(r"C:\Users\sangeetha\Phonepe-Pulse-Data-Visualization-and-Exploration\Longitude_Latitude_State_Table.csv")
      
      with st.sidebar:
        main2 = option_menu(None, ["Transactions","Users"],menu_icon='cast')

      if main2 == "Transactions":
        with st.sidebar:
          Topic = ["Aggregated","Map","Top"]
          select_topic = st.selectbox("Transactions", Topic)

        with st.sidebar:
          Topic = ["2018","2019","2020","2021","2022"]
          year = st.selectbox("Year",Topic)
          Topic = ["1","2","3","4"]
          quarter = st.selectbox("Quarter",Topic)
        
        if select_topic == "Aggregated":
           
           st.title("Aggregated_Transaction")

           mycursor.execute(f"select state,sum(total_transaction) as total_transaction,sum(transaction_amount)as transaction_amount  from aggregated_transactions where year = {year} and quarter = {quarter} group by state")
           records1 = mycursor.fetchall()
           aggregated_transactions = pd.DataFrame(records1,
                                                        columns=[i[0] for i  in mycursor.description])

           aggregated_transactions1 = aggregated_transactions.copy()
           aggregated_transactions1.drop(aggregated_transactions1.index[(aggregated_transactions1['state']=='india')],axis=0,inplace =True)

           state =state.sort_values(by=['state'], ascending=False) 
           Transaction_Amount=[]
           for i in aggregated_transactions1['transaction_amount']:
              Transaction_Amount.append(i)

           state['Transaction_Amount']=Transaction_Amount

           Total_Transaction=[]
           for i in aggregated_transactions1['total_transaction']:
              Total_Transaction.append(i)

           state['Total_Transaction'] = Total_Transaction
      

           fig_ch = px.choropleth(
                              state,
                              geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey='properties.ST_NM',                
                              locations='state',
                              color="Total_Transaction",                                       
                              )
           fig_ch.update_geos(fitbounds="locations", visible=False,)
           st.plotly_chart(fig_ch)

        if select_topic == "Map":
            
           st.title("Map_Transaction")

           mycursor.execute(f"select state,sum(amount) as total_amount from map_transactions where year = {year} and quarter = {quarter} group by state")
           records2 = mycursor.fetchall()
           map_transactions = pd.DataFrame(records2,
                                                        columns=[i[0] for i  in mycursor.description])

           map_transactions1 = map_transactions.copy()
           map_transactions1.drop(map_transactions1.index[(map_transactions1['state']=='india')],axis=0,inplace =True)

           state =state.sort_values(by=['state'], ascending=False) 
           
           Total_Amount=[]
           for i in map_transactions1['total_amount']:
              Total_Amount.append(i)

           state['Total_Amount']=Total_Amount

           fig1_ch = px.choropleth(
                              state,
                              geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey='properties.ST_NM',                
                              locations='state',
                              color="Total_Amount",                                       
                              )
           fig1_ch.update_geos(fitbounds="locations", visible=False,)
           st.plotly_chart(fig1_ch)

        if select_topic == "Top":
          
           st.title("Top_Transaction")

           mycursor.execute(f"select state,sum(amount) as amount from top_transactions where year = {year} and quarter = {quarter} group by state")

           records3 = mycursor.fetchall()
           top_transactions = pd.DataFrame(records3,
                                                        columns=[i[0] for i  in mycursor.description])

           top_transactions1 = top_transactions.copy()
           top_transactions1.drop(top_transactions1.index[(top_transactions1['state']=='india')],axis=0,inplace =True)

           state =state.sort_values(by=['state'], ascending=False) 
           
           Total_Amount=[]
           for i in top_transactions1['amount']:
              Total_Amount.append(i)

           state['Total_Amount']=Total_Amount

           fig3_ch = px.choropleth(
                              state,
                              geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey='properties.ST_NM',                
                              locations='state',
                              color="Total_Amount",                                       
                              )
           fig3_ch.update_geos(fitbounds="locations", visible=False,)
           st.plotly_chart(fig3_ch)

      if main2 == "Users":
        with st.sidebar:
          Topic = ["Aggregated","Map","Top"]
          choice_topic = st.selectbox("Transactions", Topic)

        with st.sidebar:
          Topic = ["2018","2019","2020","2021","2022"]
          year = st.selectbox("Year",Topic)
          Topic = ["1","2","3","4"]
          quarter = st.selectbox("Quarter",Topic)
        
        if choice_topic == "Aggregated":
           
          st.title("Aggregated_User")
          
          mycursor.execute(f"select state,sum(count) as user_count from aggregated_user1 where year = {year} and quarter = {quarter} group by state")

          records4 = mycursor.fetchall()
          aggregated_user1 = pd.DataFrame(records4,
                                                        columns=[i[0] for i  in mycursor.description])

          aggregated_user = aggregated_user1.copy()
          aggregated_user.drop(aggregated_user.index[(aggregated_user['state']=='india')],axis=0,inplace =True)

          state =state.sort_values(by=['state'], ascending=False) 
           
          user_count=[]
          for i in aggregated_user['user_count']:
              user_count.append(i)

          state['user_count']=user_count

          fig4_ch = px.choropleth(
                              state,
                              geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey='properties.ST_NM',                
                              locations='state',
                              color="user_count",                                       
                              )
          fig4_ch.update_geos(fitbounds="locations", visible=False,)
          st.plotly_chart(fig4_ch)

        if choice_topic == "Map":
           
          st.title("Map_User")
          
          mycursor.execute(f"select state,sum(register_users) as registered_user from map_users where year = {year} and quarter = {quarter} group by state")

          records5 = mycursor.fetchall()
          map_users = pd.DataFrame(records5,
                                               columns=[i[0] for i  in mycursor.description])

          map_users1 = map_users.copy()
          map_users1.drop(map_users1.index[(map_users1['state']=='india')],axis=0,inplace =True)

          state =state.sort_values(by=['state'], ascending=False) 
           
          registered_user=[]
          for i in map_users1['registered_user']:
              registered_user.append(i)

          state['registered_user']=registered_user

          fig5_ch = px.choropleth(
                              state,
                              geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey='properties.ST_NM',                
                              locations='state',
                              color="registered_user",                                       
                              )
          fig5_ch.update_geos(fitbounds="locations", visible=False,)
          st.plotly_chart(fig5_ch)

        
        if choice_topic == "Top":
           
          st.title("Top_User")
          
          mycursor.execute(f"select state,sum(register_users) as registered_user from top_users where year = {year} and quarter = {quarter} group by state")

          records6 = mycursor.fetchall()
          top_users = pd.DataFrame(records6,
                                               columns=[i[0] for i  in mycursor.description])

          top_users1 = top_users.copy()
          top_users1.drop(top_users1.index[(top_users1['state']=='india')],axis=0,inplace =True)

          state =state.sort_values(by=['state'], ascending=False) 
           
          registered_user=[]
          for i in top_users1['registered_user']:
              registered_user.append(i)

          state['registered_user']=registered_user

          fig6_ch = px.choropleth(
                              state,
                              geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey='properties.ST_NM',                
                              locations='state',
                              color="registered_user",                                       
                              )
          fig6_ch.update_geos(fitbounds="locations", visible=False,)
          st.plotly_chart(fig6_ch)
          
