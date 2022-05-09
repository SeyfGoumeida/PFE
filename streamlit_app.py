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
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
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
st.markdown("## 📄 Articles : ")
#--------------------------------------------------------------------------------
#--------------------------------Functions---------------------------------------
#--------------------------------------------------------------------------------

def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")


def google_drive(id:str) -> DataFrame:
    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
    creds = Credentials.from_service_account_file(
        "service-account.json",
        scopes=SCOPES,
    )
    service = build(
        "drive",
        "v3",
        credentials=creds,
        cache_discovery=False,
    )
    request = service.files().get_media(fileId=id)
    file = BytesIO()
    downloader = MediaIoBaseDownload(file,request)
    done = False
    while done is False: _,done = downloader.next_chunk()
    file.seek(0)
    return read_csv(file)
#---------------------------------------------------------------------------------
# Key words
option = st.sidebar.selectbox(
     'Choose words to creat dataset :',
     #('Covid19 & Severity',
      ('BDD finale',
      'Covid19 & Severity & Asthma',
      'Covid19 & Severity & Cancer',
      'Covid19 & Severity & Pneumonia',
      'Covid19 & Severity & Diabetes',
      'Covid19 & Severity & Hypertension')
     )
st.sidebar.write('You selected   :', option)

#---------------------------------------------------------------------------------
# number of articles to fetch
nb = st.sidebar.slider('choose the number of articles to fetch', 0,10000,500)
st.sidebar.write("You choosed    :", nb, ' articles')
space(1)

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------"Covid19 & Severity & Asthma"-----------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
  
if (option=="BDD finale"):

  df = google_drive("https://drive.google.com/file/d/1CvFtqIgC_1LwciVPZ6oyEpCEYUlloh9u/view?usp=sharing")
  st.write(df)  
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------"Covid19 & Severity & Cancer"-----------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------  
elif (option=="Covid19 & Severity & Cancer"):
  df = pd.read_csv("./PPD 2022/Datasets/Covid19 _ Severity _ Cancer/text_cleaned_cancer_alldf.csv")  
  linkTopWords = "./PPD 2022/Datasets/Covid19 _ Severity _ Cancer/top_words_cancer_cocluster_"
  nbClusters = 3
  df.drop(columns="Unnamed: 0",inplace=True)
  df["mytext_new"] = df['processed_text'].str.lower().str.replace('[^\w\s]','')
  new_df = df.mytext_new.str.split(expand=True).stack().value_counts().reset_index()
  new_df.columns = ['Word', 'Frequency'] 
  expandernb = st.expander("ℹ️ℹ️ - About articles ", expanded=True)
  with expandernb:
     col1nb, col2nb, col3nb = st.columns(3)
     #st.dataframe(df.head(nb))
     col1nb.metric(label="NUMBER OF ARTICLES", value=len(df))
     col2nb.metric(label="NUMBER OF WORDS", value=new_df.Frequency.sum())
     col3nb.metric(label="NUMBER OF UNIQUE WORDS", value=len(new_df))

  expander = st.expander("See all articles :", expanded=False)
  with expander:
    st.dataframe(df.head(nb))
  #--------------------------------------------------------------------------------------------------------------------------------
  st.header("")
  st.markdown("## 📊 Co-Clusters : ")
  expander = st.expander("Cluster sizes :", expanded=False)
  with expander:
    c1, c2,c3= st.columns([2,6,2])
    image = c2.image("./PPD 2022/Datasets/Covid19 _ Severity _ Pneumonia/clusters_size_pneumonia.png",caption='Co-clusters sizes (nb of articles - nb of words)')
  selectedCluster = st.selectbox('Select the cluster number  :',('1', '2', '3'))
  linkSimilarity = "./PPD 2022/Datasets/Covid19 _ Severity _ Cancer/graph_sim_cancer_cluster_"
  linkNER = "./PPD 2022/Datasets/Covid19 _ Severity _ Cancer/NER_cancer_cocluster_"

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------"Covid19 & Severity & Diabetes"-----------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------- 
elif (option=="Covid19 & Severity & Diabetes"):
  df = pd.read_csv("./PPD 2022/Datasets/Covid19 _ Severity _ Diabetes/text_cleaned_diabetes_alldf.csv")
  linkTopWords = "./PPD 2022/Datasets/Covid19 _ Severity _ Diabetes/top_words_diabetes_cocluster_"
  nbClusters = 5  
  df.drop(columns="Unnamed: 0",inplace=True)
  df["mytext_new"] = df['processed_text'].str.lower().str.replace('[^\w\s]','')
  new_df = df.mytext_new.str.split(expand=True).stack().value_counts().reset_index()
  new_df.columns = ['Word', 'Frequency'] 
  expandernb = st.expander("ℹ️ℹ️ - About articles ", expanded=True)
  with expandernb:
     col1nb, col2nb, col3nb = st.columns(3)
     #st.dataframe(df.head(nb))
     col1nb.metric(label="NUMBER OF ARTICLES", value=len(df))
     col2nb.metric(label="NUMBER OF WORDS", value=new_df.Frequency.sum())
     col3nb.metric(label="NUMBER OF UNIQUE WORDS", value=len(new_df))
  expander = st.expander("See all articles :", expanded=False)
  with expander:
    st.dataframe(df.head(nb))
  #--------------------------------------------------------------------------------------------------------------------------------
  st.header("")
  st.markdown("## 📊 Co-Clusters : ")
  expander = st.expander("Cluster sizes :", expanded=False)
  with expander:
    c1, c2,c3= st.columns([2,6,2])
    image = c2.image("./PPD 2022/Datasets/Covid19 _ Severity _ Pneumonia/clusters_size_pneumonia.png",caption='Co-clusters sizes (nb of articles - nb of words)')
  selectedCluster = st.selectbox('Select the cluster number  :',('1', '2', '3','4','5'))
  linkSimilarity = "./PPD 2022/Datasets/Covid19 _ Severity _ Diabetes/graph_sim_diabetes_cluster_"
  linkNER =  "./PPD 2022/Datasets/Covid19 _ Severity _ Diabetes/NER_diabetes_cocluster_"

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------"Covid19 & Severity & Hypertension"-----------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
elif (option=="Covid19 & Severity & Hypertension"):
  df = pd.read_csv("./PPD 2022/Datasets/Covid19 _ Severity _ Hypertension/text_cleaned_hypertension_alldf.csv")
  linkTopWords = "./PPD 2022/Datasets/Covid19 _ Severity _ Hypertension/top_words_hypertension_cocluster_"
  nbClusters = 5
  df.drop(columns="Unnamed: 0",inplace=True)
  df["mytext_new"] = df['processed_text'].str.lower().str.replace('[^\w\s]','')
  new_df = df.mytext_new.str.split(expand=True).stack().value_counts().reset_index()
  new_df.columns = ['Word', 'Frequency'] 
  expandernb = st.expander("ℹ️ℹ️ - About articles ", expanded=True)
  with expandernb:
     col1nb, col2nb, col3nb = st.columns(3)
     #st.dataframe(df.head(nb))
     col1nb.metric(label="NUMBER OF ARTICLES", value=len(df))
     col2nb.metric(label="NUMBER OF WORDS", value=new_df.Frequency.sum())
     col3nb.metric(label="NUMBER OF UNIQUE WORDS", value=len(new_df))
  expander = st.expander("See all articles :", expanded=False)
  with expander:
    st.dataframe(df.head(nb))
  #--------------------------------------------------------------------------------------------------------------------------------
  st.header("")
  st.markdown("## 📊 Co-Clusters : ")
  expander = st.expander("Cluster sizes :", expanded=False)
  with expander:
    c1, c2,c3= st.columns([2,6,2])
    image = c2.image("./PPD 2022/Datasets/Covid19 _ Severity _ Hypertension/clusters_size_hypertension.png",caption='Co-clusters sizes (nb of articles - nb of words)')
  selectedCluster = st.selectbox('Select the cluster number  :',('1', '2', '3','4','5'))
  linkSimilarity = "./PPD 2022/Datasets/Covid19 _ Severity _ Hypertension/graph_sim_hypertension_cluster_"
  linkNER = "./PPD 2022/Datasets/Covid19 _ Severity _ Hypertension/NER_hypertension_cocluster_"

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------"Covid19 & Severity & Obesity"-----------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------  
elif (option=="Covid19 & Severity & Obesity"):
  df = pd.read_csv("./PPD 2022/Datasets/Covid19 _ Severity _ Obesity/text_cleaned_obesity_alldf.csv")  
  linkTopWords = "./PPD 2022/Datasets/Covid19 _ Severity _ Obesity/top_words_obesity_cocluster_"
  nbClusters = 4
  df.drop(columns="Unnamed: 0",inplace=True)
  df["mytext_new"] = df['processed_text'].str.lower().str.replace('[^\w\s]','')
  new_df = df.mytext_new.str.split(expand=True).stack().value_counts().reset_index()
  new_df.columns = ['Word', 'Frequency'] 
  expandernb = st.expander("ℹ️ℹ️ - About articles ", expanded=True)
  with expandernb:
     col1nb, col2nb, col3nb = st.columns(3)
     #st.dataframe(df.head(nb))
     col1nb.metric(label="NUMBER OF ARTICLES", value=len(df))
     col2nb.metric(label="NUMBER OF WORDS", value=new_df.Frequency.sum())
     col3nb.metric(label="NUMBER OF UNIQUE WORDS", value=len(new_df))
  expander = st.expander("See all articles :", expanded=False)
  with expander:
    st.dataframe(df.head(nb))
  #--------------------------------------------------------------------------------------------------------------------------------
  st.header("")
  st.markdown("## 📊 Co-Clusters : ")
  expander = st.expander("Cluster sizes :", expanded=False)
  with expander:
    c1, c2,c3= st.columns([2,6,2])
    image = c2.image("./PPD 2022/Datasets/Covid19 _ Severity _ Obesity/clusters_size_obesity.png",caption='Co-clusters sizes (nb of articles - nb of words)')
  selectedCluster = st.selectbox('Select the cluster number  :',('1', '2', '3','4'))
  linkSimilarity = "./PPD 2022/Datasets/Covid19 _ Severity _ Obesity/graph_sim_obesity_cluster_"
  linkNER = "./PPD 2022/Datasets/Covid19 _ Severity _ Obesity/NER_obesity_cocluster_"

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------"Covid19 & Severity & Pneumonia"-----------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------- 
elif (option=="Covid19 & Severity & Pneumonia"):
  df = pd.read_csv("./PPD 2022/Datasets/Covid19 _ Severity _ Pneumonia/text_cleaned_pneumonia_alldf.csv")
  linkTopWords = "./PPD 2022/Datasets/Covid19 _ Severity _ Pneumonia/top_words_pneumonia_cocluster_"
  nbClusters = 5  
  df.drop(columns="Unnamed: 0",inplace=True)
  df["mytext_new"] = df['processed_text'].str.lower().str.replace('[^\w\s]','')
  new_df = df.mytext_new.str.split(expand=True).stack().value_counts().reset_index()
  new_df.columns = ['Word', 'Frequency'] 
  expandernb = st.expander("ℹ️ℹ️ - About articles ", expanded=True)
  with expandernb:
     col1nb, col2nb, col3nb = st.columns(3)
     #st.dataframe(df.head(nb))
     col1nb.metric(label="NUMBER OF ARTICLES", value=len(df))
     col2nb.metric(label="NUMBER OF WORDS", value=new_df.Frequency.sum())
     col3nb.metric(label="NUMBER OF UNIQUE WORDS", value=len(new_df))
  expander = st.expander("See all articles :", expanded=False)
  with expander:
    st.dataframe(df.head(nb))
  #--------------------------------------------------------------------------------------------------------------------------------
  st.header("")
  st.markdown("## 📊 Co-Clusters : ")
  expander = st.expander("Cluster sizes :", expanded=False)
  with expander:
    c1, c2,c3= st.columns([2,6,2])
    image = c2.image("./PPD 2022/Datasets/Covid19 _ Severity _ Pneumonia/clusters_size_pneumonia.png",caption='Co-clusters sizes (nb of articles - nb of words)')
  selectedCluster = st.selectbox('Select the cluster number  :',('1', '2', '3','4','5'))
  linkSimilarity = "./PPD 2022/Datasets/Covid19 _ Severity _ Pneumonia/graph_sim_pneumonia_cluster_"
  linkNER = "./PPD 2022/Datasets/Covid19 _ Severity _ Pneumonia/NER_pneumonia_cocluster_"
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