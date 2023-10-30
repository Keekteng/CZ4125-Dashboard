import streamlit as st
from streamlit_d3graph import d3graph
import json
import pandas as pd
import datetime
import networkx as nx
from components import create_collab_network_graph
import numpy as np
from PIL import Image


@st.cache_data
def retrieve_names_list():
    return pd.read_csv('./prof_raw_data/scse_profiles.csv')['name']

@st.cache_data
def retrieve_profile(name):
    if name:
        with open(f'./processed_data/{name.lower().replace(" ", "_")}.json', 'r') as f:
            profile = json.load(f)
        return profile
    return None

@st.cache_data
def retrieve_goog_sch_profile(name):
    if name:
        with open(f'./prof_raw_data/goog_sch_{name.lower().replace(" ", "_")}.json', 'r') as f:
            profile = json.load(f)
        return profile
    return None

st.set_page_config(
    page_title="Individual Profile",
    page_icon="👋",
    layout="wide",
    # initial_sidebar_state="expanded",
)

st.title('Personal Dashboard')

name = st.selectbox(
    label='Professor', 
    options=retrieve_names_list(), 
    index=None
)
if name:
    profile = retrieve_profile(name)
    goog_sch_profile = retrieve_goog_sch_profile(name)

    row1_col1, row1_col2 = st.columns([2,3])

    with row1_col1:
        img = Image.open(profile['image_path'])
        img= img.resize((500,500))
        st.image(img)

    # subheader with reduced margin
    st.markdown("""
        <style>
        .reduce-margin {
            margin-bottom: -50px;
        }
        </style>
        """, unsafe_allow_html=True)

    with row1_col2:

        row1_col2.header(f"{profile['full_name']}")
        
        st.markdown('<h3 class="reduce-margin">Designation</h3>', unsafe_allow_html=True)
        st.markdown('---')

        for designation in profile['designations']:
            row1_col2.text(f"{designation}")
        st.markdown('<h3 class="reduce-margin">Education 🎓</h3>', unsafe_allow_html=True)
        st.markdown('---')        

        for key,value in profile['education'].items():
            if value:
                st.text(f"{key} : {value}")

        st.markdown('<h3 class="reduce-margin">External Links 🔗</h3>', unsafe_allow_html=True)
        st.markdown('---') 

        btn_1,btn_2,btn_3,btn_4,btn_5 = st.columns(5)

        btn_1.link_button(
            label=':link: NTU', 
            url=profile['urls']['dr_ntu']if profile['urls']['dr_ntu'] is not None else '', 
            disabled=True if profile['urls']['dr_ntu'] is None else False,
        )

        btn_2.link_button(
            label=":link: Google Scholar", 
            url=profile['urls']['google_scholar'] if profile['urls']['google_scholar'] is not None else '', 
            disabled=True if profile['urls']['google_scholar'] is None else False,
        )

        btn_3.link_button(
            label=':link: ORCID', 
            url=profile['urls']['orcid']if profile['urls']['orcid'] is not None else '', 
            disabled=True if profile['urls']['orcid'] is None else False,
        )    

        btn_4.link_button(
            label=':link: Personal', 
            url=profile['urls']['personal']if profile['urls']['personal'] is not None else '', 
            disabled=True if profile['urls']['personal'] is None else False,
        )    


        btn_5.link_button(
            label=':email: Contact me',
            url = 'mailto:'+profile['email'],
            disabled=True if profile['email'] is None else False
        )

    st.header('Productivity Metrics 📈')
    row2_col1,row2_col2,row2_col3,row2_col4,row2_col5,row2_col6 = st.columns(6)

    cur_year = datetime.date.today().year

    if profile['avg_citation_graph']:
        avg_citation_delta = round(profile['avg_citation_graph'][str(cur_year)] - profile['avg_citation_graph'][str(cur_year-1)],1)

    if profile['avg_pub_graph']:
        avg_pub_delta = round(profile['avg_pub_graph'][str(cur_year)] - profile['avg_pub_graph'][str(cur_year-1)],1)

    if profile['h_index_graph']:
        h_index_delta = int(profile['h_index_graph'][str(cur_year)] - profile['h_index_graph'][str(cur_year-1)])

    if profile['i10_index_graph']:
        i10_index_delta = int(profile['i10_index_graph'][str(cur_year)] - profile['i10_index_graph'][str(cur_year-1)])

    row2_col1.metric(
        label='Total Publications',
        value=sum(profile['pub_graph'].values()) if profile['pub_graph'] else "NA",
        delta=f"{profile['pub_graph'][str(cur_year)] if profile['pub_graph'] else 'NA' } YTD"
    )

    row2_col2.metric(
        label='Total Citations',
        value=sum(profile['citation_graph'].values()) if profile['citation_graph'] else "NA",
        delta = f"{profile['citation_graph'][str(cur_year)]if profile['citation_graph'] else 'NA'} YTD"
    )

    row2_col3.metric(
        label='Avg Citations per Publication',
        value=round(profile['avg_citation_graph'][str(cur_year)],1) if profile['avg_citation_graph'] else "NA",
        delta=f"{avg_citation_delta if profile['avg_citation_graph'] else 'NA'} YTD"
    )

    row2_col4.metric(
        label = 'Avg Publication per Year',
        value=round(profile['avg_pub_graph'][str(cur_year)],1) if profile['avg_pub_graph'] else "NA",
        delta=f"{avg_pub_delta if profile['avg_pub_graph'] else 'NA'} YTD"
    )

    row2_col5.metric(
        label='h-index',
        value=profile['h_index_graph'][str(cur_year)] if profile['h_index_graph'] else "NA",
        delta = f"{h_index_delta if profile['h_index_graph'] else 'NA'}  YTD"
    )

    row2_col6.metric(
        label='i10-index',
        value=profile['i10_index_graph'][str(cur_year)] if profile['i10_index_graph'] else "NA",
        delta = f"{i10_index_delta if profile['i10_index_graph'] else 'NA'}  YTD"
    )

    row_3_col1,row3_col2,row3_col3 = st.columns(3)


    tab_list = ['About','Productivity Trend','Collaborators']
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

        st.markdown("""
            <style>
            .streamlit-expanderHeader p{
                font-size: 20px;
            }

        """, unsafe_allow_html=True)

        with st.expander('Biography'):
            st.write(profile['biography'])
        with st.expander('Research Interest'):
            if profile['interests']:
                for interest in profile['interests']:
                    st.write(f"- {interest}")
            else:
                st.write('NA')

    with tabs[1]:
        total_pub_df = pd.DataFrame({'Year': profile['pub_graph'].keys(), 'Num of Publications':profile['pub_graph'].values()})
        total_pub_df['Year'] = total_pub_df['Year'].astype('str')
        total_pub_df = total_pub_df.sort_values(by='Year')
        st.markdown("<font size='5'>Publication</font>", unsafe_allow_html=True)
        st.bar_chart(data=total_pub_df, x='Year', y='Num of Publications')


        total_citation_df = pd.DataFrame({'Year': profile['citation_graph'].keys(),'Num of Citations':profile['citation_graph'].values()})
        total_citation_df['Year'] = total_citation_df['Year'].astype('str')
        total_citation_df = total_citation_df.sort_values(by='Year')
        st.markdown("<font size='5'>Citation</font>", unsafe_allow_html=True)
        st.bar_chart(data=total_citation_df, x='Year', y='Num of Citations')

        avg_citation_df = pd.DataFrame({'Year': profile['avg_citation_graph'].keys(),'Avg Citation per Paper':profile['avg_citation_graph'].values()})
        avg_citation_df['Year'] = avg_citation_df['Year'].astype('str')
        avg_citation_df = avg_citation_df.sort_values(by='Year')
        st.markdown("<font size='5'>Avg Citation Per Paper</font>", unsafe_allow_html=True)
        st.bar_chart(data=avg_citation_df, x='Year', y='Avg Citation per Paper')


        avg_pub_df = pd.DataFrame({'Year': profile['avg_pub_graph'].keys(),'Avg Publication per Year':profile['avg_pub_graph'].values()})
        avg_pub_df['Year'] = avg_pub_df['Year'].astype('str')
        avg_pub_df = avg_pub_df.sort_values(by='Year')
        st.markdown("<font size='5'>Avg Publication Per Year</font>", unsafe_allow_html=True)
        st.bar_chart(data=avg_pub_df, x='Year', y='Avg Publication per Year')

        h_index_df = pd.DataFrame({'Year': profile['h_index_graph'].keys(),'All Time h-index':profile['h_index_graph'].values()})
        h_index_df['Year'] = h_index_df['Year'].astype('str')
        h_index_df = h_index_df.sort_values(by='Year')
        st.markdown("<font size='5'>All Time h-index</font>", unsafe_allow_html=True)
        st.bar_chart(data=h_index_df, x='Year', y='All Time h-index')

        i10_index_df = pd.DataFrame({'Year': profile['i10_index_graph'].keys(),'All Time i10-index':profile['i10_index_graph'].values()})
        i10_index_df['Year'] = i10_index_df['Year'].astype('str')
        i10_index_df = i10_index_df.sort_values(by='Year')
        st.markdown("<font size='5'>All Time i10-index</font>", unsafe_allow_html=True)
        st.bar_chart(data=i10_index_df, x='Year', y='All Time i10-index')
    
    with tabs[2]:
        st.markdown("<font size='5'>Collaborator Details</font>", unsafe_allow_html=True)
        collab_df = pd.DataFrame({'Name':[],'All Time Citation':[],'All Time h-index':[],'All Time i10-index':[],'Since 2018 Citation':[],'Since 2018 h-index':[],'Since 2018 i10-index':[],'Affiliation':[],'Google Scholar URL':[]})
        for co_author in profile['co_authors_url']:
            if co_author['citation_table']:
                new_row = pd.DataFrame({'Name':[co_author['name']],'All Time Citation':[co_author['citation_table']['Citations'][0]],'All Time h-index':[co_author['citation_table']['h-index'][0]],'All Time i10-index':[co_author['citation_table']['i10-index'][0]],'Since 2018 Citation':[co_author['citation_table']['Citations'][1]],'Since 2018 h-index':[co_author['citation_table']['h-index'][1]],'Since 2018 i10-index':[co_author['citation_table']['i10-index'][1]],'Affiliation':[co_author['aff']],'Google Scholar URL':[co_author['url']]})
                collab_df = pd.concat([collab_df,new_row],ignore_index=True)
        
        st.dataframe(collab_df,
                     column_config={
                         'Google Scholar URL':st.column_config.LinkColumn('URL Link')
                     }
                     )
        
        st.markdown("<font size='5'>Collaborator Network</font>", unsafe_allow_html=True)
        
        if profile['co_authors_url']:
            G,name_list,type_list = create_collab_network_graph(goog_sch_profile,profile['co_author_network'])
            adjmat = nx.to_numpy_array(G)
            d3 = d3graph(charge=2000)
            d3.graph(adjmat)
            d3.set_node_properties(label=name_list,color=type_list)
            d3.show(show_slider=False,figsize=(1600,900))
            
        

