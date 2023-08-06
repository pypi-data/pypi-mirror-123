import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

data = dict(np.load('output/final_result.npz',allow_pickle=True))
exp = 'ttH'
label_map = {
    'qsvm': 'Quantum SVM (Google)',
    'xgboost': 'Classical BDT',
    'svm': 'Classical SVM',
    'dnn': 'Classical Neural Network'
}
color_map = {
    'qsvm': 'r--o',
    'xgboost': 'g--o',
    'svm': 'y--o',
    'dnn': 'b--o'
}
algorithms = ['qsvm',  'xgboost', 'svm','dnn']

for n_qubit in data:
    d_qubit = data[n_qubit].item()
    x = list(d_qubit.keys())
    y = {}
    err = {}
    for n_event in x:
        for algo in algorithms:
            d = d_qubit[n_event][algo]
            if algo not in y:
                y[algo] = []
                err[algo] = []
            y[algo].append(d['auc'])
            err[algo].append(d['std'])
    plt.clf()
    for algo in algorithms:
        plt.errorbar(x, y[algo], yerr=err[algo], label=label_map[algo],  fmt=color_map[algo])
    plt.legend(loc='lower right')     
    plt.xlabel('Number of Events')
    plt.ylabel('AUC')
    plt.title("{}, {} qubits".format(exp, n_qubit), fontsize=16,fontweight='bold')
    plt.savefig('plots/{}_auc_progression_{}_qubit.eps'.format(exp.replace(' ','_'), n_qubit))
    plt.savefig('plots/{}_auc_progression_{}_qubit.png'.format(exp.replace(' ','_'), n_qubit), dpi=300)