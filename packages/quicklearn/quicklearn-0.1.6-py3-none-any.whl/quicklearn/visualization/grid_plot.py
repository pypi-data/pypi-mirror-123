import os
import numpy as np 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

indir = '/afs/cern.ch/work/c/chlcheng/Repository/qml_work/ttH/output/'
outdir = '/afs/cern.ch/work/c/chlcheng/Repository/qml_work/ttH/plots/'
result = dict(np.load(os.path.join(indir,'combined_result_final.npz'), allow_pickle=True))
algorithms = ['qsvm', 'xgboost', 'svm','dnn']
n_qubits = [ 15, 12, 10, 7, 5]
n_events = [100,200,400,800,1600, 3200]

for algo in algorithms:
    grid = np.zeros((len(n_qubits), len(n_events)))
    for i, n_qubit in enumerate(n_qubits):
        for j, n_event in enumerate(n_events):
            if (n_qubit, n_event) in result[algo].item():
                d = result[algo].item()[(n_qubit, n_event)]
                grid[i,j] = d['auc']
    plt.clf()
    plt.title('{} AUC heatmap'.format(algo))
    ax = sns.heatmap(grid, xticklabels=[str(i) for i in n_events],
    	yticklabels=[str(i) for i in n_qubits], cmap="YlGnBu", mask= (grid==0))
    plt.xlabel('N Event')
    plt.ylabel('N Qubit')
    plt.savefig(os.path.join(outdir, '{}_auc_heatmap.eps'.format(algo)))
    plt.savefig(os.path.join(outdir, '{}_auc_heatmap.png'.format(algo)), dpi=300, bbox_inches = 'tight', pad_inches = 0)
