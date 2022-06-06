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
#--------------------------------------------------------------------------------
#--------------------------------Functions---------------------------------------
#--------------------------------------------------------------------------------

def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")
#---------------------------------------------------------------------------------
# Key words
option = st.sidebar.selectbox('Choose words to creat dataset :',("BaseMagasin","Passage Client" ))
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
	st.markdown("## 📄 BaseMagasin : ")
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
			c2.metric(label="Nombre de caisses traditionnelles :", value= list(BaseMagasin.loc[BaseMagasin["Nom d'usage"]==optionNomMagasin]["Nombre Caisses (hors SCO et périphéries)"])[0])
			c2.metric(label="Nombre de caisses SCO :", value= list(BaseMagasin.loc[BaseMagasin["Nom d'usage"]==optionNomMagasin]["Nombre total de Caisses SCO"])[0])
			c2.metric(label="Cluster du magasin :", value= list(BaseMagasin.loc[BaseMagasin["Nom d'usage"]==optionNomMagasin]["Cluster"])[0])
			c2.metric(label="Type de clients :", value= list(BaseMagasin.loc[BaseMagasin["Nom d'usage"]==optionNomMagasin]["Cluster Profil de Clientèle"])[0])
			

		if (OptionStatusMagasin =="FRANCHISE"):
			c1.metric(label="Nombre des magasins ", value=len(magasinsFranchise))
			c1.write(magasinsFranchise) 
			optionNomMagasin = c2.selectbox('Selectionner un magasin :',options= list(magasinsFranchise["Nom d'usage"].values))
			c2.metric(label="Nombre de caisses traditionnelles :", value= list(BaseMagasin.loc[BaseMagasin["Nom d'usage"]==optionNomMagasin]["Nombre Caisses (hors SCO et périphéries)"])[0])
			c2.metric(label="Nombre de caisses SCO :", value= list(BaseMagasin.loc[BaseMagasin["Nom d'usage"]==optionNomMagasin]["Nombre total de Caisses SCO"])[0])
			c2.metric(label="Cluster du magasin :", value= list(BaseMagasin.loc[BaseMagasin["Nom d'usage"]==optionNomMagasin]["Cluster"])[0])
			c2.metric(label="Type de clients :", value= list(BaseMagasin.loc[BaseMagasin["Nom d'usage"]==optionNomMagasin]["Cluster Profil de Clientèle"])[0])#------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------------------------------
if (option=="Passage Client"):
	st.markdown("## 📊 Passage Client : ")	
	
	frames =[]
	for i in range(1,4):
	  filepath = "./Data/WEX/passageClientWexFinale_0"+str(i)+".csv"
	  part = pd.read_csv(filepath, sep=",",encoding='latin-1')
	  frames.append(part)
	BDDtmpNbClient = pd.concat(frames)
	BDDtmpNbClient = BDDtmpNbClient.drop(columns=['Unnamed: 0'])
	#----------------------------------------------------------------
	BDDtmpNbClient =BDDtmpNbClient.astype({"stoAnabelKey": int,"hour": str})
	#----------------------------------------------------------------
	#BDDtmpNbClient= BDDtmpNbClient.rename(columns={"creationDate":"Date"})
	BDDtmpNbClient= BDDtmpNbClient.rename(columns={"stoAnabelKey":"Code"})
	passageClient =BDDtmpNbClient[["Jour","creationDate","Code","Magasin","nb_client_trad","nb_client_sco"]]
	# Group by Day : 
	passageClient = passageClient.groupby(["creationDate","Code","Magasin","Jour"]).sum().sort_values(by=['nb_client_trad'], ascending=False).reset_index()
	passageClient
	
	expander = st.expander("", expanded=False)
	with expander:
		c1, c2= st.columns(2)
			
