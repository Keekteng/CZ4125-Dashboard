import networkx as nx

# mapping is done with google scholar url since url is unique
def create_collab_network_graph(author_details, mapping):
    G = nx.Graph()
    edges = set()

    # Add nodes
    # color code to differentiate academic collaborators from non-academic collaborators
    type_list = []
    # Name of author
    name_list = []
    for idx,a in enumerate(mapping.keys()):
        G.add_node(a)
        if idx==0:
            type_list.append('#FFFF00')
            name_list.append(author_details['name'])
        else:
            co_author_details = author_details['co_authors_url'][idx-1]
            co_author_aff = co_author_details['aff']
            co_author_name = co_author_details['name']
            # If from University 
            if 'University' in co_author_aff or 'Institute' in co_author_aff or 'College' in co_author_aff:
                type_list.append('#FF0000')
                name_list.append(co_author_name)
            # If external collaborator
            else:
                type_list.append('#808080')
                name_list.append(co_author_name)

    author_url = author_details['goog_sch_url']
    # Add edges for direct collaborations
    for co_author in mapping[author_url]:
        G.add_edge(author_url, co_author)
        edges.add((author_url, co_author))

    # Add connections between co-authors who have collaborated with each other before
    for co_author in mapping[author_url]:
        if co_author in mapping:
            for co_co_author in mapping[co_author]:
                if co_co_author != author_url and co_co_author in mapping[author_url] and (co_co_author, co_author) not in edges:
                    G.add_edge(co_author, co_co_author)
                    edges.add((co_author, co_co_author))
    return G, name_list,type_list