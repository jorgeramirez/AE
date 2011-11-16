#coding: UTF-8
from ga import GaSolution
class Cluster:
    
    def __init__(self):
        self.lista = []
        
    def agregar_solucion(self,sol):
        self.lista.append(sol)

    def calcular_distancia(self,cluster2):
        cont = 0
        distancia =0
        for solucion1 in self.lista :
            for solucion2 in cluster2.lista :
                distancia = distancia + solucion1.distance(solucion2)
                cont = cont +1
                
        return distancia/cont
    
    def setlista(self,list):
        self.lista = list
    
    def getlista(self):
        return self.lista
    
    def unir(self,cluster):
        cluster_nuevo = Cluster()
        cluster_nuevo.setlista(self.lista)

        for solucion in cluster.lista:
            cluster_nuevo.agregar_solucion(solucion)

        return cluster_nuevo
    
    def centroide(self):
        menor_distancia = -1
        centroide = None
        if len(self.lista)==1:
            centroide = self.lista[0]
            return centroide
        
        for solucion1 in self.lista :
            distancia=0 
            for solucion2 in self.lista:
                distancia = distancia + solucion1.distance(solucion2)
            if menor_distancia==-1 or distancia < menor_distancia:
                menor_distancia = distancia
                centroide = solucion1 
            
        return centroide
        
