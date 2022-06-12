class Analisis():
    def __init__(self):
        self.analisis = ""
        self.analisisDesc = ""
        self.wordsAnalisis = ""
        self.wordsAnalisisDesc = ""
        #FALTAN EL 4,7 Y ESTAMOS
        self.verbos = [] #Smell 01
        self.abreviatura = [] #Smell 17
        self.tecnisismos = [] #Smell 18
        self.comparativos = [] #Smell 10
        self.debilidad = [] #Smell 04
        self.subjetividad = [] #Smell 07
        self.ambiguo = [] #Smell 09
        self.vagueness = [] #Smell 06
        self.superlativo = [] #Smell 08
        self.loopholes = [] #Smell 11
        self.openEndTerm = [] #Smell 14
        self.cargarDatos()

    def cargarDatos(self):
        verbos = open('C:/Users/User/Documents/Memoria/Programa/Django/accounts/diccionarios/verbos.txt', 'r')
        for line in verbos:
            self.verbos.append(line[:len(line)-1])
        verbos.close()
        
        ambiguos = open('C:/Users/User/Documents/Memoria/Programa/Django/accounts/diccionarios/DiccionarioAmbiguo.txt', 'r')
        for line in ambiguos:
            self.comparativos.append(line[:len(line)-1])
        ambiguos.close()
        
        comparaciones = open('C:/Users/User/Documents/Memoria/Programa/Django/accounts/diccionarios/DiccionarioComparativos.txt', 'r')
        for line in comparaciones:
            self.comparativos.append(line[:len(line)-1])
        comparaciones.close()
        
        abreviaturas = open('C:/Users/User/Documents/Memoria/Programa/Django/accounts/diccionarios/DiccionarioAbreviaturas.txt', 'r')
        for line in abreviaturas:
            self.abreviatura.append(line[:len(line)-1])
        abreviaturas.close()
        
        vagueness = open('C:/Users/User/Documents/Memoria/Programa/Django/accounts/diccionarios/DiccionarioVagueness.txt', 'r')
        for line in vagueness:
            self.vagueness.append(line[:len(line)-1])
        vagueness.close()
        
        tecnicimo = open('C:/Users/User/Documents/Memoria/Programa/Django/accounts/diccionarios/DiccionarioTecnico.txt', 'r')
        for line in tecnicimo:
            self.tecnisismos.append(line[:len(line)-1])
        tecnicimo.close()
        
        loopholes = open('C:/Users/User/Documents/Memoria/Programa/Django/accounts/diccionarios/DiccionarioLoopholes.txt', 'r')
        for line in loopholes:
            self.loopholes.append(line[:len(line)-1])
        loopholes.close()
        
        superlative = open('C:/Users/User/Documents/Memoria/Programa/Django/accounts/diccionarios/DiccionarioSuperlatives.txt', 'r')
        for line in superlative:
            self.superlativo.append(line[:len(line)-1])
        superlative.close()

        debilidades = open('C:/Users/User/Documents/Memoria/Programa/Django/accounts/diccionarios/DiccionarioSuperlatives.txt', 'r')
        for line in debilidades:
            self.debilidad.append(line[:len(line)-1])
        debilidades.close()

        subjetivo = open('C:/Users/User/Documents/Memoria/Programa/Django/accounts/diccionarios/DiccionarioSuperlatives.txt', 'r')
        for line in subjetivo:
            self.subjetividad.append(line[:len(line)-1])
        subjetivo.close()
        
        openEnd = open('C:/Users/User/Documents/Memoria/Programa/Django/accounts/diccionarios/DiccionarioOpenEndTerms.txt', 'r')
        for line in openEnd:
            self.openEndTerm.append(line[:len(line)-1])
        openEnd.close()

    def iniciarAnalisis(self, requisito, codigo, descripcion):
        self.requisitoNormal = requisito
        self.requisito = requisito.lower()
        self.descripcionNormal = descripcion
        self.descripcion = descripcion.lower()
        self.codigo = codigo
        self.requisito.split(" ")
        self.descripcion.split(" ")
        self.smell01()
        return self.analisis, self.analisisDesc, self.wordsAnalisis, self.wordsAnalisisDesc
    
    def smell01(self):
        contador = 0
        contadorDesc = 0
        verbos = ""
        verbosd = ""
        verbo = "a"
        verboDesc = "a"
        for verb in self.verbos:
            if self.requisito.__contains__(verb.lower()):
                if verbo != verb:
                    verbos = verbos + verbo + " - "
                    verbo = verb
                    contador += 1
            if self.descripcion.__contains__(verb.lower()):
                if verboDesc != verb:
                    verbosd = verbosd + verboDesc + " - "
                    verboDesc = verb
                    contadorDesc += 1
        if contador > 1:
            self.analisis += "Sm-01:Multiplicidad "
            self.wordsAnalisis += verbos
        if contadorDesc > 1:
            self.analisisDesc += "Sm-01:Multiplicidad "
            self.wordsAnalisisDesc += verbosd
        self.smell04()

    def smell04(self):
        for debil in self.debilidad:
            for word in self.requisito:
                if word == debil:
                    self.analisis += "Sm-04:Debilidad "
                    self.wordsAnalisis += debil+" "
            for word in self.descripcion:
                if word == debil:
                    self.analisisDesc += "Sm-04:Debilidad "
                    self.wordsAnalisisDesc += debil+" "
        self.smell06()

    def smell06(self):
        for word in self.vagueness:
            for word2 in self.requisito:
                if word == word2:
                    self.analisis += "Sm-06:Vaguedad "
                    self.wordsAnalisis += word+" "
                    break
            for word2 in self.descripcion:
                if word == word2:
                    self.analisisDesc += "Sm-06:Vaguedad "
                    self.wordsAnalisisDesc += word+" "
                    break
        self.smell07()

    def smell07(self):
        for sentence in self.subjetividad:
            if self.requisitoNormal.__contains__(sentence):
                self.analisis += "Sm-07:Subjetividad "
                self.wordsAnalisis += sentence+" "
            if self.descripcionNormal.__contains__(sentence):
                self.analisisDesc += "Sm-07:Subjetividad "
                self.wordsAnalisisDesc += sentence+" "
        self.smell08()

    def smell08(self):
        for word in self.superlativo:
            if self.requisitoNormal.__contains__(word.lower()):
                self.analisis += "Sm-08:Superlativo "
                self.wordsAnalisis += word+" "
                break
            if self.descripcionNormal.__contains__(word.lower()):
                self.analisisDesc += "Sm-08:Superlativo "
                self.wordsAnalisisDesc += word+" "
                break
        self.smell09()
    
    def smell09(self):
        for word in self.comparativos:
            if self.requisitoNormal.__contains__(word.lower()):
                self.analisis += "Sm-09:Ambiguo "
                self.wordsAnalisis += word+" "
                break
            if self.descripcionNormal.__contains__(word.lower()):
                self.analisisDesc += "Sm-09:Ambiguo "
                self.wordsAnalisisDesc += word+" "
                break
        self.smell10()

    def smell10(self):
        for sentence in self.comparativos:
            if self.requisitoNormal.__contains__(sentence.lower()):
                self.analisis += "Sm-10:Frases-Comparativas "
                self.wordsAnalisis += sentence+" "
                break
            if self.descripcionNormal.__contains__(sentence.lower()):
                self.analisisDesc += "Sm-10:Frases-Comparativas "
                self.wordsAnalisisDesc += sentence+" "
                break
        self.smell11()

    def smell11(self):
        for sentence in self.loopholes:
            if self.requisitoNormal.__contains__(sentence):
                self.analisis += "Sm-11:Loopholes "
                self.wordsAnalisis += sentence+" "
                break
            if self.descripcionNormal.__contains__(sentence):
                self.analisisDesc += "Sm-11:Loopholes "
                self.wordsAnalisisDesc += sentence+" "
                break
        self.smell12()

    def smell12(self):
        for word in self.requisito:
            if word.lower() == "no":
                self.analisis += "Sm-12:Oraciones-Negativas "
                self.wordsAnalisis += "no "
                break
        for word in self.descripcion:
            if word.lower() == "no":
                self.analisisDesc += "Sm-12:Oraciones-Negativas "
                self.wordsAnalisisDesc += "no "
                break
        self.smell14()

    def smell14(self):
        for sentence in self.openEndTerm:
            if self.requisitoNormal.__contains__(sentence):
                self.analisis += "Sm-14:Terminos-de-inicio-final "
                self.wordsAnalisis += sentence+" "
                break
            if self.descripcionNormal.__contains__(sentence):
                self.analisisDesc += "Sm-14:Terminos-de-inicio-final "
                self.wordsAnalisisDesc += sentence+" "
                break
        self.smell16()

    def smell16(self):
        if self.requisito[0] == "como" or self.requisito[0] == "cómo":
            self.analisis += "Sm-16:Inicia-Como-No-Que "
        if self.descripcion[0] == "como" or self.descripcion[0] == "cómo":
            self.analisisDesc += "Sm-16:Inicia-Como-No-Que "
        self.smell17()

    def smell17(self):
        for word in self.abreviatura:
            for word2 in self.requisito:
                if word2 == (word.lower()):
                    self.analisis +="Sm-17:Siglas/Abreviaturas "
                    self.wordsAnalisis += word+" "
                    break
            for word2 in self.descripcion:
                if word2 == (word.lower()):
                    self.analisisDesc +="Sm-17:Siglas/Abreviaturas "
                    self.wordsAnalisis += word+" "
                    break
        self.smell18()

    def smell18(self):
        if self.codigo.__contains__("RU"):
            for word in self.tecnisismos:
                for word2 in self.requisito:
                    if word2 == (word.lower()):
                        self.analisis += "Sm-18:Tecnisismos-en-RU "
                        break
                if self.descripcion.__contains__(word.lower()):
                    self.analisisDesc += "Sm-18:Tecnisismos-en-RU "
                    break
        self.smell19()

    def smell19(self):
        self.sm19 = ["sistema", "programa", "aplicación", "aplicacion"]
        if self.codigo.__contains__("RS") and self.requisito.__contains__("usuario"):
            self.analisis += "Sm-19:Inicio-en-RU-y-RS "
        if self.codigo.__contains__("RS") and self.descripcion.__contains__("usuario"):
            self.analisisDesc += "Sm-19:Inicio-en-RU-y-RS "
        for word in self.sm19:
            if self.codigo.__contains__("RU") and self.requisito.__contains__(word):
                self.analisis += "Sm-19:Inicio-en-RU-y-RS "
                break
            if self.codigo.__contains__("RU") and self.descripcion.__contains__(word):
                self.analisisDesc += "Sm-19:Inicio-en-RU-y-RS "
                break
        self.smell20()

    def smell20(self):
        reqSplit = self.requisitoNormal.split(" ")
        for word in reqSplit:
            count = 0
            for word2 in reqSplit:
                if word == word2:
                    count += 1
            if count > 2:
                self.analisis += "Sm-20:Redundancia"
                break
        descSplit = self.descripcionNormal.split(" ")
        for word in descSplit:
            count = 0
            for word2 in descSplit:
                if word == word2:
                    count += 1
            if count > 2:
                self.analisisDesc += "Sm-20:Redundancia"
                break