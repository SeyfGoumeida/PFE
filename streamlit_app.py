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
st.sidebar.title(" 📊 Nombre idéal des caisses")

with st.expander("ℹ️ - À propos de l'application :", expanded=False):
    st.write(
        """     
Ce projet vise à predire le nombre idéal des caisse à mettre en place dans chaque magasin en se basant sur les KPIs, feedback, localisation, type de clientèle... """
    )
    st.write("@Copyrights to Seyf GOUMEIDA")

    
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
option = st.sidebar.selectbox('Pages :',("BaseMagasin","Passage Client","Systemes de scoring" ))
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
	expander = st.expander("", expanded=True)
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
	len(BDDtmpNbClient)
	BDDtmpNbClient = BDDtmpNbClient.drop(columns=['Unnamed: 0'])
	#----------------------------------------------------------------
	BDDtmpNbClient =BDDtmpNbClient.astype({"stoAnabelKey": int,"hour": str})
	#----------------------------------------------------------------
	BDDtmpNbClient= BDDtmpNbClient.rename(columns={"date":"Date"})
	BDDtmpNbClient= BDDtmpNbClient.rename(columns={"stoAnabelKey":"Code"})
	passageClient =BDDtmpNbClient[["Jour","Date","Code","Magasin","nb_client_trad","nb_client_sco"]]
	# Group by Day : 
	passageClient = passageClient.groupby(["Jour","Date","Code","Magasin"]).sum().sort_values(by=['nb_client_trad'], ascending=False).reset_index()
	
	
	expander = st.expander("", expanded=True)
	with expander:
		magasinsIntegres = passageClient["Magasin"].values
		optionNomMagasin = expander.selectbox('Selectionner un magasin :',options= sorted(list(set(list(magasinsIntegres)))))
		magasinPassageCleint = passageClient[passageClient['Magasin'] == optionNomMagasin]
		fig1, ax1 = plt.subplots()
		ax1.set_title('Box Plot du passage client')
		ax1.boxplot(sorted(magasinPassageCleint['nb_client_trad']),vert=False, notch=True)
		
		fig2, ax2 = plt.subplots()
		ax2.set_title('Graphe du passage client')
		ax2.scatter (x=magasinPassageCleint["Jour"], y=magasinPassageCleint['nb_client_trad'])

		#----------------------------------------------------------------------------------
		c1, c2= st.columns(2)
		c1.pyplot(fig1)
		c2.pyplot(fig2)
		expander.write("Focus magasin :")
		magasinPassageCleint

	st.write("Tous les magasins :")
	passageClient
#-----------------------------------------------------------------------------------------------------------------------------------------------------
if (option=="Systemes de scoring"):
	st.markdown("## 🥇🥈🥉 Systemes de scoring : ")	
	optionScoring = st.selectbox('Selectionner un systeme :',options= ["Attente en caisse - Non pénalisant","Attente en caisse - pénalisant","Redondance - Picasso"])
	filepath1_2 = "./Results/Scoring/Scoring1_2.csv"
	scoring1_2 = pd.read_csv(filepath1_2, sep=";",encoding='latin-1')
	scoring1_2= scoring1_2.rename(columns={"Unnamed: 0":"Classement"})
	scoring1_2= scoring1_2.rename(columns={"Scoring_x":"Non pénalisant"})
	scoring1_2= scoring1_2.rename(columns={"Scoring_y":"Pénalisant"})
	filepath3 = "./Results/Scoring/Scoring3.csv"
	scoring3 = pd.read_csv(filepath3, sep=";",encoding='latin-1')
	scoring3= scoring3.rename(columns={"Unnamed: 0":"Classement"})
	#----------------------------------------------------------------------------------
	c1, c2= st.columns(2)


	if(optionScoring=="Attente en caisse - Non pénalisant" or optionScoring=="Attente en caisse - pénalisant"):
		c1.write("Il consiste a aﬀecter des points à un magasin dans chaque quart d’heure d’ouverture selon le nombre des clients dans l’attente en caisse. Plus un magasin a de l’attente moins de point il aura: 0 clients dans l’attente en caisse : 3 points, 1 clients dans l’attente en caisse : 2 points, 2 clients dans l’attente en caisse : 1 points, 3 clients ou plus dans l’attente en caisse : 0 pointsCe système favorise les magasins qui ont moins d’attente mais il ne pénalise pas ceux qui ont trop d’attente, c’est pour cela on a proposé un deuxième système de scoring")
		c2.scoring1_2
	else:
		c2.scoring3
	   
	   
	   
	   
	   
	   
	   
