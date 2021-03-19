import pandas as pd 

def get_gene_list(file_path):
    dataFrame = pd.read_csv(file_path)
    gene_list = dataFrame[lambda x: x['p_val_adj'] < float(0.05)].iloc[:,0]
    return gene_list.tolist()

