# ProyectoDistribuidas
El problema a resolver fue calcular el coeficiente de similitud de TANIMOTO e imprimirlo en un archivo con la utilizacion de programacion paralela.Para el caso del archivo en C++ se utilizo la libreria OPEN MP y para la implementacio en python se utilizo la libreria MULTIPROCESSING e importamos POOL.

El proyecto consta de dos partes :
1. implemetacion en C++ de el calculo del coeficiente de TANIMOTO
2. implemetacion en python del calculo del coeficiente de TANIMOTO

Los comandos para la ejecucion de los archivo en UBUNTU son:

ARCHIVO UNO
PARA COMPILAR :    
          
          g++ -fopenmp implementacionC.cpp -o main
          
PARA EJECUTAR : 

         ./main

ARCHIVO DOS
PARA COMPILAR Y EJECUTAR :    
              
          python implementacio.py



