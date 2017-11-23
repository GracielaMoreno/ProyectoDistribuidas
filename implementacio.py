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

#extraer los terminos comunes de las formulas ingresadas
def extraerTerminosComunes(c1,c2):
    Aux = set(c1).intersection(set(c2))
    lis3 = {}
    for k in Aux:
        if (c1[k] > c2[k]):
            lis3[k] = c2[k]
        else:
            lis3[k] = c1[k]
    return lis3
#se extraer los caracteres de cada compuesto 
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

def escribirDocSalida(lineas, archivo):
    docSalida = open(archivo, "w")
    for linea in lineas:
        docSalida.write(str(linea) + "\n")
    docSalida.close
    print "Escritura finalizada"

#metodo main para realizar la ejejcucion de las funciones 
def main ():
    #se toma el tiempo de inicio del proceso
    ini = time.time()
    print "El calculo tomara tiempo !!"
    dicAux = []
    dicAux = lecturaDocumento("ZINC_chemicals.tsv")
#se declara la cantidad de procesadores que tiene el ordenados en donde se va ejecutar el codigo
    pool = Pool(processes=4)  
 #pool es los que nos ayuda a la paralelizacion de la funcion llenado de matriz
    coeficienteSimilitud  = pool.map(llenadoDeMatriz, (dicAux,))
   # se obtiene el nombre de los compuestos y se los escribe en el archivo de salida PRUEBAFINAL.tsv
    for i in range (len(coeficienteSimilitud )):
        escribirDocSalida(coeficienteSimilitud [i],"PRUEBAFINAL.tsv")
   #se toma el tiempo de finalizacion del proceso 
    end = time.time()
    # se calcula el tiempo de ejecucion q es la diferencia de tiempofinal -tiempo inicial
    final = end - ini
    print "El tiempo de ejecucion es:",final

if __name__ == '__main__':
    main()

