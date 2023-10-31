import streamlit as st
import pandas as pd
import json


st.set_page_config(
    page_title="SCSE Profile",
    page_icon="👋",
    layout="wide",
)

st.header('Nanyang Technological University 🏫')
st.divider()
st.subheader('School of Computer Science & Engineering')

row1 =st.columns(4)
with open('./data_source/processed_data/scse_metric.json','r') as f:
    scse_metric = json.load(f)

row1[0].metric(
    label='Total Publications',
    value = scse_metric['pubs']['Total Publications'],
    delta = f"{scse_metric['pubs']['delta']} YTD"
)

row1[1].metric(
    label='Total Citations',
    value= scse_metric['citations']['Total Citations'],
    delta = f"{scse_metric['citations']['delta']} YTD"
)

row1[2].metric(
    label = 'Total Patents',
    value = scse_metric['total_patents']
)

row1[3].metric(
    label = 'Total Grants',
    value = scse_metric['total_grants']
)

tab_list = ['About Us','Trends','Faculty Members']
whitespace = 6
tabs = st.tabs([s.center(whitespace,"\u2001") for s in tab_list])
tab_css = """
<style>
button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
font-size: 24px;
}
</style>
"""
st.markdown(tab_css, unsafe_allow_html=True)
with tabs[0]:
    with open('./data_source/prof_raw_data/scse_intro.json','r')as f:
        intro = json.load(f)['intro'][:-1]
    for paragraphs in intro:
        st.write(paragraphs)    

with tabs[1]:
    with open('./data_source/processed_data/scse_trend.json','r') as f:
          faculty_trend = json.load(f)

    total_pub_df = pd.DataFrame({'Year': faculty_trend['pub_trend'].keys(), 'Num of Publications':faculty_trend['pub_trend'].values()})
    total_pub_df['Year'] = total_pub_df['Year'].astype('str')
    total_pub_df = total_pub_df.sort_values(by='Year')
    st.markdown("<font size='5'>Publication</font>", unsafe_allow_html=True)
    st.bar_chart(data=total_pub_df, x='Year', y='Num of Publications')

    total_citation_df = pd.DataFrame({'Year': faculty_trend['cite_trend'].keys(),'Num of Citations':faculty_trend['cite_trend'].values()})
    total_citation_df['Year'] = total_citation_df['Year'].astype('str')
    total_citation_df = total_citation_df.sort_values(by='Year')
    st.markdown("<font size='5'>Citation</font>", unsafe_allow_html=True)
    st.bar_chart(data=total_citation_df, x='Year', y='Num of Citations')



# st.subheader('Faculty Members')
with tabs[2]:
    faculty_table = pd.read_csv('./data_source/processed_data/faculty_member.csv')
    faculty_table.drop(columns=['Unnamed: 0'],inplace=True)

    # extract unique set of research topics
    unique_topics = set()
    for interests in faculty_table['Recent Research Interest'].tolist():
            for interest in interests.split(','):
                if interest!= ' ':
                    unique_topics.add(interest)
    unique_topics = sorted(list(unique_topics))

    options = st.multiselect(label='Filter by Recent Research Interest',options=unique_topics,default=None)

    faculty_table['Recent Research Interest'] = faculty_table['Recent Research Interest'].str.split(',')
    # Filter by all the options selected
    df_filtered = faculty_table[faculty_table['Recent Research Interest'].apply(lambda x: all(option in x for option in options))]
    # Display the filtered dataframe
    st.dataframe(df_filtered,use_container_width=True,hide_index=True)



