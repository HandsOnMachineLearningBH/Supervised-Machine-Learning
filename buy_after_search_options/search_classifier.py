import pathlib
DIR=str(pathlib.Path(__file__).resolve().parent)

from collections import Counter
import pandas as pd

# teste inicial: home, busca, logado => comprou
# home, busca
# home, logado
# busca, logado
# busca: 85.71% (7 testes)

df = pd.read_csv(DIR + '/normalized_search.csv')

X_df = df[['home', 'busca', 'logado']]
Y_df = df['comprou']

Xdummies_df = pd.get_dummies(X_df)
Ydummies_df = Y_df

X = Xdummies_df.values
Y = Ydummies_df.values

porcentagem_de_treino = 0.8
porcentagem_de_teste = 0.1

tamanho_de_treino = porcentagem_de_treino * len(Y)
tamanho_de_teste = porcentagem_de_teste * len(Y)
tamanho_de_validacao = len(Y) - tamanho_de_treino - tamanho_de_teste
fim_de_teste = tamanho_de_treino + tamanho_de_teste

from examples import Examples
trainig_examples = Examples(X[0:int(tamanho_de_treino)], Y[0:int(tamanho_de_treino)])
test_examples = Examples(X[int(tamanho_de_treino):int(fim_de_teste)], Y[int(tamanho_de_treino):int(fim_de_teste)])
real_examples = Examples(X[int(fim_de_teste):], Y[int(fim_de_teste):])

def fit_and_predict(nome, modelo, treino_dados, treino_marcacoes, teste_dados, teste_marcacoes):
	modelo.fit(treino_dados, treino_marcacoes)

	resultado = modelo.predict(teste_dados)
	acertos = (resultado == teste_marcacoes)

	total_de_acertos = sum(acertos)
	total_de_elementos = len(teste_dados)
	taxa_de_acerto = 100.0 * total_de_acertos / total_de_elementos

	msg = "Taxa de acerto do {0}: {1}".format(nome, taxa_de_acerto)
	print(msg)
	return taxa_de_acerto


from sklearn.naive_bayes import MultinomialNB
modeloMultinomial = MultinomialNB()
resultadoMultinomial = fit_and_predict("MultinomialNB", modeloMultinomial, trainig_examples.features, trainig_examples.target, test_examples.features, test_examples.target)


from sklearn.ensemble import AdaBoostClassifier
modeloAdaBoost = AdaBoostClassifier()
resultadoAdaBoost = fit_and_predict("AdaBoostClassifier", modeloAdaBoost, trainig_examples.features, trainig_examples.target, test_examples.features, test_examples.target)


if resultadoMultinomial > resultadoAdaBoost:
	vencedor = modeloMultinomial
else:
	vencedor = modeloAdaBoost

resultado = vencedor.predict(real_examples.features)
acertos = (resultado == real_examples.target)

total_de_acertos = sum(acertos)
total_de_elementos = len(real_examples.target)
taxa_de_acerto = 100.0 * total_de_acertos / total_de_elementos

msg = "Taxa de acerto do vencedor entre os dois algoritmos no mundo real: {0}".format(taxa_de_acerto)
print(msg)











# a eficacia do algoritmo que chuta
# tudo um unico valor
acerto_base = max(Counter(real_examples.target).values())
taxa_de_acerto_base = 100.0 * acerto_base / len(real_examples.target)
print("Taxa de acerto base: %f" % taxa_de_acerto_base)
print("Total de testes: %d " % len(real_examples.features))






