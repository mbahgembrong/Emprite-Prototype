from attr import has
import streamlit as st
from helper import preprocessing_data, graph_sentiment, analyse_mention, analyse_hastag, download_data

st.set_page_config(
     page_title="Data Analysis Web App",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://github.com/everydaycodings/Data-Analysis-Web-App',
         'Report a bug': "https://github.com/everydaycodings/Data-Analysis-Web-App/issues/new",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
)


st.title("ANALISIS SENTIMEN KALIMAT ")

function_option = st.sidebar.selectbox("Filter: ", ["Search By #Tag and Words", "Search By Username"])

if function_option == "Search By #Tag and Words":
    word_query = st.text_input("Masukan Hastag / kalimat")

if function_option == "Search By Username":
    word_query = st.text_input("Masukan Username ( tanpa @ )")

number_of_tweets = st.slider("Berapa banyak tweets yang anda butuhkan {}".format(word_query), min_value=100, max_value=10000)
st.info("1 Tweets membutuhkan waktu 0.05 detik jadi jadi tolong tunggu sekitar {} menit untuk {} Tweets, mohon sabar.".format(round((number_of_tweets*0.05/60),2), number_of_tweets))

if st.button("Mulai"):

    data = preprocessing_data(word_query, number_of_tweets, function_option)
    analyse = graph_sentiment(data)
    mention = analyse_mention(data)
    hastag = analyse_hastag(data)

    st.write(" ")
    st.write(" ")
    st.header("Hasil Pencarian dan Preproses Dataset")
    st.write(data)
    download_data(data, label="hasil analisis")
    st.write(" ")
    
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown("### EDA On the Data")


    col1, col2 = st.columns(2)

    with col1:
        st.text("Top 10 @ Mentions dari {} tweets".format(number_of_tweets))
        st.bar_chart(mention)
    with col2:
        st.text("Top 10 Hastags dari {} tweets".format(number_of_tweets))
        st.bar_chart(hastag)
    
    col3, col4 = st.columns(2)
    with col3:
        st.text("Top 10 link yang pernah di klik dari {} tweets".format(number_of_tweets))
        st.bar_chart(data["links"].value_counts().head(10).reset_index())
    
    with col4:
        st.text("Top 10 semua tweets yang berisi link")
        filtered_data = data[data["links"].isin(data["links"].value_counts().head(10).reset_index()["index"].values)]
        st.write(filtered_data)

    st.subheader("Hasil Analisa Sentimen")
    st.bar_chart(analyse)
    