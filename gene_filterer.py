import pandas as pd 

def filter_positive(row):
    zipped = zip(row['p_val_adj'], row['avg_log2FC'])
    bool_list = []
    for (p_val, avg_log) in zipped:
        bool_list.append(p_val < float(0.05) and avg_log >= 0)

    return bool_list

def filter_negative(row):
    zipped = zip(row['p_val_adj'], row['avg_log2FC'])
    bool_list = []
    for (p_val, avg_log) in zipped:
        bool_list.append(p_val < float(0.05) and avg_log < 0)

    return bool_list

def get_gene_list(file_path, relative_expression):
    dataFrame = pd.read_csv(file_path)
    if(relative_expression == 'positive'):
        gene_list = dataFrame[lambda x: filter_positive(x)].iloc[:,0]
        return gene_list.tolist()
    if(relative_expression == 'negative'):
        gene_list = dataFrame[lambda x: filter_negative(x)].iloc[:,0]
        return gene_list.tolist()
    else:
        raise Exception("The argument relative_expression must be either of 'positive' or 'negative'")


