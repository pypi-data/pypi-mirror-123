# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 20:45:52 2021

@author: eva_gonzalez
"""

#Función números primos
def numPrimoA (n):
    resto=[]
    for i in range(2,n):
        resto.append(n%i)
    if (0 in resto):
        print("El número ", n, "no es primo" )
    else: 
        print("El número ", n, "es primo")
    return

def numPrimoB (n):
    if (n==1):
        return False
    for i in range (2,n):
        if (n%i==0):
            print(n, "no es primo,", i, "es divisor")
            return 
    print(n, "es primo")
    return 

#Calculo de numeros primos en un intervalo
def Primos(n):
    primo=[]
    for i in range(2,n+1):
        residuo=[]
        for j in range(2,i):
            residuo.append(i%j)
        if (0 in residuo):
            False
        else:
            primo.append(i)
            print(i, "es primo")       
    return




















