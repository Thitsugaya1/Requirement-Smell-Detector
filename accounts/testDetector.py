from smellDetector import *


def prueba():
	requisito = "Escritura del documento para su desarrollo"
	splitReq = requisito.split(" ")
	for word in splitReq:
		count = 0
		for word2 in splitReq:
			if word == word2:
				print (word)
				count += 1
		if count > 1:
			print ("Sm-20")

def testDetector():
	codigo = []
	for i in range (1,3):
		if i%2==0:
			string = "RU0"+str(i)
		else:
			string = "RS0"+str(i)
		codigo += [string]

	requisito = "El sistema debe realizar un analisis de los requisitos"
	splitReq = requisito.split(" ")

	analisis = []
	for req in codigo:
		resultado = Analisis()
		analisis = resultado.iniciarAnalisis(requisito, req)
		print("resultado de", req, "es:",analisis)

#prueba()
testDetector()