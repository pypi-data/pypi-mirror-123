import numpy as np 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

result = dict(np.load('output/combined_result_final.npz', allow_pickle=True))


exp = 'ttH'

algorithms = ['qsvm',  'xgboost', 'svm','dnn']
label_map = {
    'qsvm': 'Quantum SVM (Google)',
    'xgboost': 'Classical BDT',
    'svm': 'Classical SVM',
    'dnn': 'Classical Neural Network'
}

color_map = {
    'qsvm': 'r-',
    'xgboost': 'g-',
    'svm': 'y-',
    'dnn': 'b-'
}


n_qubits = [5,7,10, 12, 15]
n_events = [100,200,400,800,1600, 3200]
data = {}
for n_qubit in n_qubits:
    data[str(n_qubit)] = {}
    for n_event in n_events:
        data[str(n_qubit)][str(n_event)] = {}
        plt.clf()
        plt.rcParams["font.weight"] = "bold"
        plt.xlabel("Signal Efficiency", fontsize=18,fontweight='bold')
        plt.ylabel("Background Rejection", fontsize=18,fontweight='bold')
        plt.title("{} ROC Curve, {} qubits, {} events".format(exp, n_qubit, n_event), fontsize=16,fontweight='bold')
        plt.xlim(0.0, 1.0)
        plt.ylim(0.0, 1.0)       
        plt.grid(color='gray', linestyle='--', linewidth=1) 
        for algo in algorithms:
            if (n_qubit, n_event) in result[algo].item():
                d = result[algo].item()[(n_qubit, n_event)]
                data[str(n_qubit)][str(n_event)][algo] = {'auc': d['auc'], 'std': d['std_auc']}
                plt.plot(d['tpr'],1-d['fpr'], color_map[algo],linewidth=2, label='{}, auc = {:.3f} ± {:.3f}'.format(label_map[algo], d['auc'], d['std_auc']), mfc='none')         
        plt.plot([0, 1], [1, 0], linestyle='--', color='black', label='Luck, AUC= 0.5')             
        plt.legend(loc='best',prop={'size': 8})    
        plt.savefig('plots/{}_roc_{}_qubit_{}_event_with_luck.eps'.format(exp.replace(' ','_'), n_qubit, n_event))
        plt.savefig('plots/{}_roc_{}_qubit_{}_event_with_luck.png'.format(exp.replace(' ','_'), n_qubit, n_event), dpi=300)


np.savez('output/final_result.npz', **data)