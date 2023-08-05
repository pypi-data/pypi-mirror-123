import pandas as pd
import numpy as np

# import gzip
import os.path
# import scipy.sparse
from scipy.sparse import csr_matrix



def ReadCSV(path, dset_name):

    data_path = path + dset_name + '/' + dset_name + "_data.csv"
    celldata_path = path + dset_name + '/' + dset_name + "_celldata.csv"
    genedata_path = path + dset_name + '/' + dset_name + "_genedata.csv"

    if os.path.isfile(data_path):
        data = pd.read_csv(data_path, index_col=0)
    else: 
        msg = "File <" + data_path + "> does not exist"
        raise ValueError(msg)

    if os.path.isfile(celldata_path):
        celldata = pd.read_csv(celldata_path, index_col=0)
    else:
        celldata = None

    if os.path.isfile(genedata_path):
        genedata = pd.read_csv(genedata_path, index_col = 0)
    else:
        genedata = None 
    

    return data, genedata, celldata




def Read10X(path, dset_name):

    with open(path + dset_name + '/matrix.mtx', 'r') as f:
        while True:
            header = f.readline()
            if not header.startswith('%'):
                break
        header = header.rstrip().split()
        n_genes, n_cells = int(header[0]), int(header[1])

        data, i, j = [], [], []
        for line in f:
            fields = line.rstrip().split()
            data.append(float(fields[2]))
            i.append(int(fields[1])-1)
            j.append(int(fields[0])-1)
        X = csr_matrix((data, (i, j)), shape=(n_cells, n_genes)).toarray()

    genes = []
    with open(path + dset_name + '/genes.tsv', 'r') as f:
        for line in f:
            fields = line.rstrip().split()
            genes.append(fields[1])
    assert(len(genes) == n_genes)

    barcodes = []
    with open(path + dset_name + '/barcodes.tsv', 'r') as f:
        for line in f:
            fields = line.rstrip().split()
            barcodes.append(fields[0])
    assert(len(barcodes) == n_cells)

    return X, np.array(genes), np.array(barcodes)