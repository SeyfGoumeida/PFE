from os import sep
import streamlit as st
from datetime import datetime
import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit.components.v1 import html
import json
import base64
import textwrap
import streamlit.components.v1 as components
from io import BytesIO
from pandas import read_csv
from pandas import DataFrame
#--------------------------------------------------------------------------------
st.set_page_config(layout="wide", page_icon="microbe", page_title="Covid19 Severity app")
st.title("📊 Nombre des caisses idéal APP")
st.sidebar.title(" 📊 Nombre des caisses idéal APP")

with st.expander("ℹ️ - À propos de l'application :", expanded=False):

    st.write(
        """     
Ce projet vise à predire le nombre idéal des caisse à mettre en place dans chaque magasin en se basant sur les KPIs, feedback, localisation, type de clientèle... """
    )
    
st.markdown("")
st.markdown("## 📄 BaseMagasin : ")
#--------------------------------------------------------------------------------
#--------------------------------Functions---------------------------------------
#--------------------------------------------------------------------------------

def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")
#---------------------------------------------------------------------------------
# Key words
option = st.sidebar.selectbox('Choose words to creat dataset :',("BaseMagasin", ))
st.sidebar.write('You selected   :', option)

#---------------------------------------------------------------------------------
# number of articles to fetch
nb = st.sidebar.slider('choisir le nombre des magasins top', 0,270,100)
st.sidebar.write("Vous avez choisi :", nb, ' magasins')
space(1)

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------       "BaseMagasin"         -----------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
  
  
if (option=="BaseMagasin"):
	OptionStatusMagasin = st.selectbox('Integré / Franchisé :',options= ('INTEGRE','FRANCHISE',))
	BaseMagasin = pd.read_csv("./Data/BaseMagasin/BaseMagasin.csv", sep=";",encoding='latin-1')
	magasinsIntegre =BaseMagasin.loc[BaseMagasin['Statut'] == "INTEGRE"][["Nom d'usage","CADANA : Anabel"]].reset_index().drop(columns=['index'])
	magasinsFranchise =BaseMagasin.loc[BaseMagasin['Statut'] == "FRANCHISE"][["Nom d'usage","CADANA : Anabel"]].reset_index().drop(columns=['index'])
	expander = st.expander("", expanded=False)
	with expander:
		c1, c2= st.columns(2)
		if (OptionStatusMagasin =="INTEGRE"):
			c1.metric(label="Nombre des magasins ", value=len(magasinsIntegre))
			c1.write(magasinsIntegre)
			optionNomMagasin = c2.selectbox('Selectionner un magasin :',options= list(magasinsIntegre["Nom d'usage"].values))
			c2.metric(label="Cluster", value= BaseMagasin.loc[BaseMagasin["Nom d'usage"]==optionNomMagasin]["Cluster"][0])

		if (OptionStatusMagasin =="FRANCHISE"):
			c1.metric(label="Nombre des magasins ", value=len(magasinsFranchise))
			c1.write(magasinsFranchise) 
			optionNomMagasin = c2.selectbox('Selectionner un magasin :',options= list(magasinsFranchise["Nom d'usage"].values))
			c1.write(optionNomMagasin)
#------------------------------------------------------------------------------------------------------------------------
c1, c2= st.columns([9,3])
expander1 = c1.expander('Most frequente works :', expanded=False)
expander2 = c2.expander('Show cluster words : ', expanded=False)
link = linkTopWords+str(selectedCluster)+".csv"
cluster = pd.read_csv(link)
cluster = cluster.sort_values(by=['count'],ascending=False)
#---------------------------------------------------------
fig = plt.figure(figsize=(8, 2))
ax = sns.barplot(x="words", y="count", data=cluster.head(20), alpha=0.9)
ax.set_xticklabels(ax.get_xticklabels(),rotation = 90)
expander1.pyplot(fig)
expander2.write(cluster)
#----------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------
st.header("")
st.markdown("## 📌 NER Named Entity Recognition : ")
col1, col2 = st.columns([6,2])
expander3 = col1.expander('Show deseases plot :', expanded=False)
expander3.image(linkNER+str(selectedCluster)+".png",use_column_width ="always",caption='Word cloud of desease names found in the co-cluster')
expander4 = col2.expander('Show deseases table : ')
df_desease = pd.read_csv(linkNER+str(selectedCluster)+".csv")
expander4.write(df_desease)

#----------------------------------------------------------------------------------------------------------------------------

st.header("")
st.markdown("## 🧬 Similarities : ")
expander2 = st.expander("Similarities  :", expanded=False)
with expander2:
  col1, col2 ,col3= st.columns([2,6,2])	
  image2 = col2.image(linkSimilarity+str(selectedCluster)+".png",caption='Similarity graph of top frequent terms (Red color = Desease name)')
#----------------------------------------------------------------------------------------------------------------------------
st.markdown("## 📥 Download Datasets and results :")
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv(sep=";").encode('utf-8')
dfcsv = convert_df(df)
clusterdf = convert_df(cluster)


expander = st.expander("Downloads", expanded=False)
with expander:
	c1, c2,c3= st.columns(3)
	
	c1.header("Dataset :")
	result = c1.download_button(label="📥 Download (.csv)",data=dfcsv,file_name=option+'_df.csv',mime='text/csv')
	
	c2.header("Cluster :")
	dataset = c2.download_button(label="📥 Download(.csv)",data=clusterdf,file_name=option+selectedCluster+'_df.csv',mime='text_/csv')
	
	c3.header("Deseases :")
	dataset = c3.download_button(label="📥 Download( .csv)",data=convert_df(df_desease),file_name=option+"_deseases_"+selectedCluster+'_df.csv',mime='text_/csv')
