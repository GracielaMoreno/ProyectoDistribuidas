from multiprocessing import Pool
import time

def lecturaDocumento(docEntrada):
    file = open(docEntrada, "r")
    listaCompuestos = []
    contenido = file.readlines()

    for i in range(1, len(contenido), 1):
        colunma1 = contenido[i].find('\t')
        colunma2 = contenido[i].find('\t', colunma1 + 1)
        colunma3 = contenido[i].find('\t', colunma2 + 1)

        if i == len(contenido)-1:
            colunma4 = (contenido[i].__len__())
        else:
            colunma4 = contenido[i].find('\t',colunma3 + 1)

        id = (contenido[i][colunma1 + 1:colunma2])
        compuesto = (contenido[i][colunma3 + 1:colunma4])
        listaIdCompuesto = id,compuesto
        listaCompuestos.append(listaIdCompuesto)

    return listaCompuestos

def escribirDocSalida(lineas, archivo):
    docSalida = open(archivo, "w")
    for linea in lineas:
        docSalida.write(str(linea) + "\n")
    docSalida.close
    print "Escritura finalizada"

#Calculo del coeficiente
def CoeficienteTanimoto(cadena1, cadena2):

    c1 = extraerArrayCaracteres(cadena1)
    c2 = extraerArrayCaracteres(cadena2)

    n1 = NumumeroCompuestos(c1)
    n2 = NumumeroCompuestos(c2)
    ArregloElementosComunes = extraerTerminosComunes(c1,c2)
    n3 = NumumeroCompuestos(ArregloElementosComunes)
    #print n1,n2,n3
    coeficienteSimilitud  = (n3/float (n1+n2-n3))
    return "{0:.2f}".format(coeficienteSimilitud )

def extraerTerminosComunes(c1,c2):
    Aux = set(c1).intersection(set(c2))
    lis3 = {}
    for k in Aux:
        if (c1[k] > c2[k]):
            lis3[k] = c2[k]
        else:
            lis3[k] = c1[k]
    return lis3

def extraerArrayCaracteres(comp1):
    diccionario = {}
    for letra in comp1:
        if diccionario.has_key(letra):
            diccionario[letra] = diccionario[letra] + 1
        else:
            diccionario[letra] = 1

    for k in diccionario.keys():
        if k == "@":
            if diccionario["@"] > 1:
                diccionario["@"] = 1
    return diccionario

def NumumeroCompuestos(diccionario):
    n = 0
    for k, v in diccionario.items():
        n += (int(v))
    return n

#Llenado de la matriz a imrpimir
def llenadoDeMatriz(formulaDicionario):
    coeficiente = 0
    listaCoeficienteSimilitud = []
    for i in range (len(formulaDicionario)):
        for j in range (0,i):
            coeficiente = formulaDicionario[i][0],formulaDicionario[j][0] ,(CoeficienteTanimoto(cadena1=formulaDicionario[i][1] ,cadena2=formulaDicionario[j][1]))
            #SE RETORNA EL COEFICIENTE DE TINOMOTO
            listaCoeficienteSimilitud.append(coeficiente)
    return listaCoeficienteSimilitud


def main ():
    ini = time.time()
    print "El calculo tomara tiempo !!"
    dicAux = []
    dicAux = lecturaDocumento("pru.tsv")

    pool = Pool(processes=4)  # start 4 worker processes
    inPs = time.time()
    
    coeficienteSimilitud  = pool.map(llenadoDeMatriz, (dicAux,))
    endPS = time.time()
    for i in range (len(coeficienteSimilitud )):
        escribirDocSalida(coeficienteSimilitud [i],"SOLUCIONES.tsv")
    end = time.time()
    final = end - ini
    print "El tiempo de ejecucion es:",final

if __name__ == '__main__':
    main()
end = time.time()

