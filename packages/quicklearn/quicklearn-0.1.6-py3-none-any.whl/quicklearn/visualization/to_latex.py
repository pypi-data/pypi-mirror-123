import numpy as np 
from pdb import set_trace

data = dict(np.load('output/final_result.npz', allow_pickle=True))
text = ''

algorithms = ['xgboost', 'svm','dnn', 'qsvm']

for n_qubit in data:
	for n_event in data[n_qubit].item():
		text += '\\cellcolor{{almond}}\\textcolor{{black}}{{{}}} &  \\cellcolor{{almond}}\\textcolor{{black}}{{{}}}&\n'.format(n_qubit, n_event)
		result = data[n_qubit].item()[n_event]
		for algo in algorithms:
			if algo not in result:
				tt = {'auc': 0, 'std':0}	
			else:
				tt = {'auc': result[algo]['auc'], 'std':result[algo]['std']}
			text += '\\cellcolor{{almond}}\\textcolor{{black}}{{{:.3f}$\\pm${:.3f}}}&\n'.format(tt['auc'], tt['std'])
		text = text[:-2]
		text += '\\\\\\thickhline\n'

print(text)


f = open('output/latex.text','w')
f.write(text)
f.close()