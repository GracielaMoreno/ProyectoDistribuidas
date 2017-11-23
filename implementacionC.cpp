#include <iostream>
#include <fstream>
#include <string>
#include <cstddef>
#include <list>
#include <iomanip>
#include <omp.h>
#include <time.h>
using namespace std;


//CONDICION DEL ARROBA
list<char> ControlDelArroba(string a)
{
    list<char> array;
    array.push_back(a[0]);
    for(unsigned int i=1; i<a.length(); i++)
    {
        if(array.back()!='@' || a[i]!='@')
        {
            array.push_back(a[i]);
        }
        else{

        }
    }
    //ENTREGA UN ARRAY
    return array;
}
//NUMERO DE REPETICION DE UN ELEMENTO
int numeroRepiteElemento(list<char> array ,char elemento)
{
    int contador=0;
    for (std::list<char>::iterator it=array.begin(); it!=array.end() ; ++it)
        if(*it==elemento)
        contador++;
//RETORNA EL NUMERO DE REPETICION DE UN ELEMENTO
    return contador;
}

//REEMPLAZA PARA PODER CONTAR LOS CARACTERES
string reemCadena(string str, const string from, const string to) {
    if(from.empty())
        return str;
    size_t start_pos = 0;
    while((start_pos = str.find(from, start_pos)) != std::string::npos) {
        str.replace(start_pos, from.length(), to);
        start_pos += to.length();
    }

    return str;
}

//OBTENERE EL NUMERO DE LOS ELEMENTOS Q NOS SE REPITEN
list<char> obtenerArrayDeElementoUnico(list<char> array)
{
    list<char> elementoUnico;
    for (std::list<char>::iterator it=array.begin(); it!=array.end() ; ++it)
    {
         if(numeroRepiteElemento(elementoUnico,*it)==0 && *it!='(' && *it !=')' && *it!='[' && *it !=']' && *it!='=' && *it !='-' && *it !='+' && !isdigit(*it) && *it !='n' )
         {
             elementoUnico.push_back(*it);
         }
    }
//OBTIENE LOS ELEMENTOS QUE NO SE REPITEN DESDE LA LISTA
    return elementoUnico;

}
//SE REALIZA EL CONTEO DE LOS ELEMENTOS Q TIENE EL ARCHIVO 
int contarElementos(list<char> array)
{
    int nroElementos=0;
    list<char> elementoUnico=obtenerArrayDeElementoUnico(array);
    for (std::list<char>::iterator it=elementoUnico.begin(); it!=elementoUnico.end() ; ++it)
    nroElementos+=numeroRepiteElemento(array,*it);
    return nroElementos;
}

//CUENTA LA CANTIDAD DE ELEMETOS QUE SE REPITEN 
int contarElementosComunes(list<char> array1,list<char> array2)
{
    list<char> elementoUnico=obtenerArrayDeElementoUnico(array1);
    int cont=0;
    for (std::list<char>::iterator it1=elementoUnico.begin(); it1!=elementoUnico.end() ; ++it1)
    cont+=min(numeroRepiteElemento(array1,*it1),numeroRepiteElemento(array2,*it1));
    //CUANTA EL NUMERO DE ELELEMTOS COMUNES
    return cont;
}

//RECIBE COMO PARAMETRO LA CADENA1 Y LA CADENA 2 A COMPARAR
double IndiceJaccardTanimoto(string cadena1, string cadena2)
{
    double indice=0;
    cadena1=reemCadena(reemCadena(cadena1,"Br","$"),"Cl","*");
    cadena2=reemCadena(reemCadena(cadena2,"Br","$"),"Cl","*");

    //CALCULO DEL INDICE DE TINOMOTO
    int Na=contarElementos(ControlDelArroba(cadena1));
    int Nb=contarElementos(ControlDelArroba(cadena2));
    int Nc=contarElementosComunes(ControlDelArroba(cadena1),ControlDelArroba(cadena2));
    indice=(double)Nc/(Na+Nb-Nc);
    return indice;
}

int main(void)
{
//LECTURA DEL DOCUMENTO DE ENTRADA
    string lineaDeEntrada;
    ifstream docEntrada;
//SE DEFINE CUANTOS ID SE DEBE LEER EN EL ARCHIVO 
    string id[12423];
//SE DEFINE CUANTOS ID SE DEBE LEER EN EL ARCHIVO 
    string clave[12423];
    docEntrada.open("ZINC_chemicals.tsv");
    int cont=0;
    getline(docEntrada,lineaDeEntrada);
   //SE CARGAN LAS VARIABLES A UTILIZAR PARA EL CALCULO E IMPRESION 

    while(docEntrada)
    {
        getline(docEntrada,lineaDeEntrada);
        int lin = lineaDeEntrada.find_last_of("\t");
        int lin1=lineaDeEntrada.find_first_of("\t");
        id[cont]=lineaDeEntrada.substr(lin1+1,13);
        clave[cont]=lineaDeEntrada.substr(lin+1,*lineaDeEntrada.end()-lin);
        cont++;
    }
    docEntrada.close();
    printf("Lectura conpletada del archivo ZINC_chemical\n");
	clock_t start,end;
	start=clock();
    ofstream docSalida;
    docSalida.open("SOLUCION.txt");
    docSalida << fixed;
    docSalida << setprecision(2);
    //12422
    //SE UTILIZA PARA OBTENER EL MAXIMO NUMERO DE PROCESASORES QUE TIENE EL ORDENADOR
     int omp_get_num_threads(omp_get_max_threads());
    //SE REALIZA LA PARALELIZACION CON LA AYUDA DE LA LIBRERIA OPEN MP 
    #pragma omp parallel for ordered

    for(int i=0; i<12422; i++)
    {
	//HACE SOLO LA PARTE TRIANGULAR
        for (int j=i; j<12422; j++)
        {
           
		#pragma omp ordered
                docSalida<<id[i]<<"\t"<<id[j]<<"\t"<<IndiceJaccardTanimoto(clave[i],clave[j])<<endl;

           
        }

    }
	//SE CALCULA EL TIEMPO DE EJCUCION DE TODO EL PROCESO 
	float time=((double)clock()-start)/CLOCKS_PER_SEC;
	printf("El archivo se escribio sin problemas \n");
	//SE IMPRIME EL TIEMPO DE EJCUCION 
	printf("El tiempo que se demoro en la ejecucion fue :%f\n",time);
    return 0;
}
