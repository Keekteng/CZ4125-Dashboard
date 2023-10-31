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


st.subheader('Faculty Members')
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




