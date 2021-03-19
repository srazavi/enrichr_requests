import json
import requests


library_list = ['BioPlanet_2019', 'KEGG_2016', 'GO_Biological_Process_2018',
				'GO_Molecular_Function_2018', 'GO_Cellular_Component_2018',
				'Human_Phenotype_Ontology', 'Panther_2016', 'Reactome_2016',
				'WikiPathways_2016']

test_gene_list = \
	 ['PHF14', 'RBM3', 'MSL1', 'PHF21A', 'ARL10', 'INSR', 'JADE2', 'P2RX7',
     'LINC00662', 'CCDC101', 'PPM1B', 'KANSL1L', 'CRYZL1', 'ANAPC16', 'TMCC1',
     'CDH8', 'RBM11', 'CNPY2', 'HSPA1L', 'CUL2', 'PLBD2', 'LARP7', 'TECPR2', 
     'ZNF302', 'CUX1', 'MOB2', 'CYTH2', 'SEC22C', 'EIF4E3', 'ROBO2',
     'ADAMTS9-AS2', 'CXXC1', 'LINC01314', 'ATF7', 'ATP5F1']

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

def download_file(user_list_id, library):
	ENRICHR_URL = 'http://maayanlab.cloud/Enrichr/export'
	query_string = '?userListId=%s&filename=%s&backgroundType=%s'
	filename = library
	gene_set_library = library

	url = ENRICHR_URL + query_string % (user_list_id, filename, gene_set_library)
	response = requests.get(url, stream=True)

	with open(filename + '.tsv', 'wb') as f:
	    for chunk in response.iter_content(chunk_size=1024): 
	        if chunk:
	            f.write(chunk)

def main():
	for library in library_list:
		download_file(get_user_list_id(test_gene_list), library)


if __name__ == '__main__':
	main()
