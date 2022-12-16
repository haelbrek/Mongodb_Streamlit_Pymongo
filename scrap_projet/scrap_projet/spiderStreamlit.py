import streamlit as st
from pymongo import MongoClient
import pandas as pd 

# Replace with your MongoDB URI
mongo_uri = "mongodb://localhost:27017"

# Create a client instance
client = MongoClient(mongo_uri)

# Connect to a specific database
db = client['Scraping']
my_collection = db['movies']
# Create input fields for search criteria
#titre  = st.text_input("Enter a titre de film")


# with st.columns(column_widths=[25, 75]) as (col1, col2):
#     acteur  = col1.text_input("Enter a l'acteur ")
#     genre   = col1.text_input("Enter le genre de film")
#     duree   = col1.number_input("Entrer la durée maximum de film")
#     score   = col1.number_input("Entrer note minimale", min_value=0, max_value=10)


acteur  = st.sidebar.text_input("choisissez votre acteur préféré ")
acteur=acteur.split(',')
genre  =st.sidebar.text_input("Choisissez le genre de film")
genre  = genre.split(',')
duree=st.sidebar.number_input("Entrer la durée maximum de film")
score = st.sidebar.number_input("Entrer note minimale", min_value=0, max_value=10)
st.title("Vos film préféré")
# Build the query based on the input fields
query = {}

query["casting_principal"] = {"$elemMatch":{"$in":acteur}}
query["genre"] = {"$elemMatch":{"$in":genre}}
query["runtime"] = {"$lt": duree} 
query["rating_score"] = {"$gt": score} 
# Retrieve documents matching the query

result = my_collection.find(query)

# Convert the cursor to a list
df=pd.DataFrame()
for film in result:
        new_rows=pd.DataFrame({
                               'years':[film['years']],
                               'title':[film['title']],
                               'titre_originale':[film['titre_original']],
                               'genre':[film['genre']],
                               'score':[film['rating_score']],
                               'durrée':[film['runtime']],
                               'public':[film['public']],
                               'acteurs':[str(film['casting_principal'])],
                               'summary':[str(film['summary'])],
                               })
        df=pd.concat([df,new_rows],ignore_index=True)
if st.sidebar.button("Exécuter") :

    st.dataframe(df.transpose(), width=600)
    #st.write(acteur)





