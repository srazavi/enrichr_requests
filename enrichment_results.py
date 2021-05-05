import json
import requests
import sys
import os

#user file
import gene_filterer


library_list = ['BioPlanet_2019', 'KEGG_2016', 'GO_Biological_Process_2018',
                'GO_Molecular_Function_2018', 'GO_Cellular_Component_2018',
                'Human_Phenotype_Ontology', 'Panther_2016', 'Reactome_2016',
                'WikiPathways_2016']


def get_user_list_id(gene_list):
    ENRICHR_URL = 'http://maayanlab.cloud/Enrichr/addList'
    genes_str = '\n'.join(gene_list)
    description = 'Example gene list'
    payload = {
        'list': (None, genes_str),
        'description': (None, description)
    }

    response = requests.post(ENRICHR_URL, files=payload)
    if not response.ok:
        raise Exception('Error analyzing gene list')

    data = json.loads(response.text)
    return data['userListId']

def download_results_file(user_list_id, library, file_prefix):
    ENRICHR_URL = 'http://maayanlab.cloud/Enrichr/export'
    query_string = '?userListId=%s&filename=%s&backgroundType=%s'
    filename = 'write/'+file_prefix+library
    gene_set_library = library

    url = ENRICHR_URL + query_string % (user_list_id, filename, gene_set_library)
    response = requests.get(url, stream=True)

    with open(filename + '.tsv', 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

def get_file_name_no_ext(file_path):
    file_name = os.path.split(file_path)[1]
    return file_name.split('.')[0]

def main():
    # skip first command line argument
    file_path = sys.argv[1]

    for direction in ('positive', 'negative'):
    	#get gene list
	    gene_list = gene_filterer.get_gene_list(file_path, direction)
	    file_name_prefix = get_file_name_no_ext(file_path) + '_' + direction + '_'

	    #check that gene_list is not empty
	    if gene_list:
	        print(gene_list)
	        os.mkdir('write') if not os.path.exists('write') else None
	        for library in library_list:
	            download_results_file(get_user_list_id(gene_list), library, file_name_prefix)
	    else:
	        print("No genes matched the criteria in the "+direction+" direction.")


if __name__ == '__main__':
    main()
