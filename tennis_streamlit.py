import streamlit as st
import pandas as pd
import mysql.connector


connection= mysql.connector.connect(

 host= "localhost",
 user= "root",
 password="",
 database="tennis"

)
mycursor = connection.cursor()

# Total number of competitors.
#Numberof countries represented.
#Highest points scored by a competitor.
st.title("TENNIS SPORT RADAR")
st.write("\n")
st.subheader("COMPETITOR TABLE")
mycursor.execute("select * from table_6 ")
data=mycursor.fetchall()
df=pd.DataFrame(data,columns=mycursor.column_names)

mycursor.execute("""SELECT table_6.name,table_5.rank,table_5.points
                FROM table_6 inner join table_5 ON 
                 table_6.competitor_id=table_5.competitor_id""")
D1=mycursor.fetchall()
A1=pd.DataFrame(D1,columns=mycursor.column_names)


data1=df["competitor_id"].count()
st.sidebar.metric(label="TOTAL NO OF COMPETITOR",value=data1)
data2=df["country"].nunique()
st.sidebar.metric(label="TOTAL COUNTRY",value=data2)

mycursor.execute("""select name,max(points) from(SELECT table_6.name,table_5.rank,table_5.points
                FROM table_6 inner join table_5 ON 
                 table_6.competitor_id=table_5.competitor_id) as JOINT_TABLE""")
D1=mycursor.fetchall()
A1=pd.DataFrame(D1,columns=mycursor.column_names)
st.sidebar.dataframe(A1,hide_index=True)

#name, country  country_code  category_id  competition_id  abbrivation \\ - compititor table 6
#compitition played   competitior id  rank,  point - competitor ranking table 5
#table 5 - competitor ranking table
#table 6 - competitor table

mycursor.execute("""select table_6.competitor_id, table_6.name,table_6.country,
                 table_6.country_code,table_6.abbreviation
                  ,table_5.rank,table_5.points from table_6 inner 
                 join table_5 on table_6.competitor_id=table_5.competitor_id""")
C1=mycursor.fetchall()
C2=pd.DataFrame(C1,columns=mycursor.column_names)
st.dataframe(C2,hide_index=True)

search_name = st.text_input("Search for a competitor by name:")
if search_name:
    filtered_df = C2[C2['name'].str.contains(search_name, case=False, na=False)]
else:
    filtered_df = C2

# Display the filtered DataFrame
st.dataframe(filtered_df, hide_index=True)
min_rank, max_rank = st.sidebar.slider("Select rank range", 1, 1000, (1, 100))

# Filter the DataFrame based on the selected rank range
filtered_df = C2[(C2['rank'] >= min_rank) & (C2['rank'] <= max_rank)]

st.subheader("FILTER TABLE BY RANK")
# Display the filtered DataFrame
st.dataframe(filtered_df, hide_index=True)



country = st.selectbox("Select country", C2['country'].unique())
filtered_df = C2[C2['country'] == country]

# Display the filtered dataframe
st.dataframe(filtered_df)

#TOP 3 COUNTRIES WITH POINTS


mycursor.execute("""SELECT country,sum(points) as Total_points from (select table_6.competitor_id, table_6.name,table_6.country,
                 table_6.country_code,table_6.abbreviation
                  ,table_5.rank,table_5.points from table_6 inner 
                 join table_5 on table_6.competitor_id=table_5.competitor_id) as jointable group by country 
                 ORDER BY Total_points DESC LIMIT 3""")


joined_tab = mycursor.fetchall()
df4 = pd.DataFrame(joined_tab,columns=mycursor.column_names)
st.sidebar.write("TOP THREE COUNTRIES")
st.sidebar.dataframe(df4, hide_index=True)


# Leaderboards
st.header("Leaderboards")

# Top-ranked competitors
mycursor.execute("""
    SELECT table_6.name, table_6.country, table_5.rank, table_5.points
    FROM table_6
    INNER JOIN table_5 ON table_6.competitor_id = table_5.competitor_id
    ORDER BY table_5.rank ASC
    LIMIT 10
""")
top_ranked = mycursor.fetchall()
top_ranked_df = pd.DataFrame(top_ranked, columns=["Name", "Country", "Rank", "Points"])
st.subheader("Top-Ranked Competitors")
st.dataframe(top_ranked_df, hide_index=True)

# Competitors with the highest points
mycursor.execute("""
    SELECT table_6.name, table_6.country, table_5.rank, table_5.points
    FROM table_6
    INNER JOIN table_5 ON table_6.competitor_id = table_5.competitor_id
    ORDER BY table_5.points DESC
    LIMIT 10
""")
highest_points_competitors = mycursor.fetchall()
highest_points_df = pd.DataFrame(highest_points_competitors, columns=["Name", "Country", "Rank", "Points"])
st.subheader("Competitors with Highest Points")
st.dataframe(highest_points_df, hide_index=True)

st.subheader("Analysis of the Tennis Competition Rankings:")
st.write("""The tennis competition features 1,000 competitors from 79 countries, showcasing global participation. Pavic Mate 
         leads with an impressive 9,530 points, reflecting his dominance in the sport. 
         The USA stands out as the top-performing country,
          accumulating 88,009 points, demonstrating its strength in tennis.""")

st.header("COMPLEXES AND VENUE'S")
st.sidebar.header("COMPLEX AND VENUE")
mycursor.execute("""SELECT table_3.complex_id,table_3.complex_name,table_4.venue_name,table_4.city_name,
                     table_4.country_name,table_4.country_code,table_4.timezone FROM table_4 
                 inner join table_3 ON table_4.complex_id=table_3.complex_id""")
data_1 = mycursor.fetchall()
df_1 = pd.DataFrame(data_1,columns=mycursor.column_names)
df_2 = pd.DataFrame(data_1,columns=mycursor.column_names)

TOTAL_COMPLEX = df_1["complex_name"].nunique()
st.sidebar.metric(label="TOTAL COMPLEX",value=TOTAL_COMPLEX)

st.write("VENUES IN  EACH COMPLEXES")
mycursor.execute(""" SELECT 
                             c.complex_name, 
                             COUNT(v.venue_name) AS venue_count
                             FROM table_4 v
                             JOIN 
                             table_3 c 
                             ON 
                             v.complex_id = c.complex_id
                             GROUP BY 
                             c.complex_name order by venue_count DESC;
                        """)
data_2 = mycursor.fetchall()
df_2 = pd.DataFrame(data_2,columns=mycursor.column_names)
st.dataframe(df_2,hide_index=True)

TOTAL_VENUE = df_1["venue_name"].nunique()
st.sidebar.metric(label="TOTAL VENUE",value=TOTAL_VENUE)

st.subheader("COMPLEXES AND VENUE'S ANALYSIS")
st.write("""
The tennis complexes host a diverse range of venues, with a total of unique complexes and venues. The app highlights the distribution of venues across complexes, helping to understand the scale and reach of each facility.""")

mycursor.execute("""SELECT table_1.category_id,table_1.name,table_2.category_name,table_1.gender,table_1.parent_id,
                        table_1.type FROM table_1
                  INNER JOIN table_2 ON table_2.category_id = table_2.category_id;""")
out=mycursor.fetchall()   
table1_data = pd.DataFrame(out,columns=mycursor.column_names)
st.header("COMPETITION'S & CATEGORY TABLE")
st.sidebar.header("COMPETITION'S & CATEGORY")
st.dataframe(table1_data)

count_competitions = len(table1_data["name"].unique())
st.sidebar.metric(label="TOTAL_COMPETITIONS",value=count_competitions)


st.sidebar.header("Filter by Gender")
gender = st.sidebar.selectbox("Select Gender:",table1_data ["gender"].unique())


st.subheader("FILTER TABLE BY GENDER")
# Filter data based on gender selection
if gender:
    gen_name= table1_data[table1_data['gender']==gender]
st.dataframe(gen_name,hide_index=True)

st.subheader("COMPETITION ANALYSIS")
st.write("""Out of 5,796 total competitions analyzed,
          male participation 
         is significantly higher compared to 
         female and mixed categories, highlighting a gender
           disparity in competition representation.""")