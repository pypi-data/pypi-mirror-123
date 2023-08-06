#!/usr/bin/env python
# coding: utf-8

# # NÚMEROS PRIMOS
# 
# os números primos son aquellos números que solo son divisibles entre el número 1 y ellos mismos; es decir, que si dividimos ese número por otro que no sea el 1 o mismo, el resultado siempre será un número no entero; en otras palabras, el resultado de la división será un decimal.

# EJEMPLOS: 
#  
#     A) 996 NO es primo. Puede ser dividido por 2 Y y dar un nº entero (Ejemplo: 996 / 2 = 498)
# 
#     B) 113 SI es un número primo. Solo puede ser dividido por el 1 y él mismo.
# 
#     C) 811 SI es un número primo. Solo puede ser dividido por el 1 y él mismo.

# In[95]:


from rpy2.robjects import r
import rpy2.robjects as ro

numeros_primos_R = '''
primos <- function(n){ 
    es_primo=TRUE
    for (i in 2:n){                                     
        for (j in 2:i){
            if(i%%j==0){
                es_primo=FALSE
                }
            }
        if(es_primo){
            print(n)
            print(" es primo, pq SOLAMENTE dividiéndose por si mismo o 1, da un nº Entero, no Decimal")
        } 
    }
}
'''


# In[100]:


ro.r(numeros_primos_R)
conocer_primos=ro.globalenv['primos']
conocer_primos(10)


# In[36]:


def primo(n):
    for i in range(2, n): #por ej.--> si n=3-->; i=2,3 y si n=5, i=2,3,4,5
        es_primo = True #definimos la varible es_primo, que por defecto es True y que tendrá el valor de n
        for j in range(2, i): #si i=2,3,4 -->
                                #cuando i=2--> j=2 ; 
                                #cuando i=3--> j=2,3 ; cuando i=4, j=2,3,4
            if(i%j == 0): #como n=3, i=2,3
                            #si tomamos--> i=3-->j=2,3
                                #3/2 no es = 0
                                #3/3=0
                            #si tomamos-->i=2-->j=2
                                #2/2=0
                es_primo = False 
        if(es_primo):
            print(f"{i} es primo, pq SOLAMENTE dividiéndose por si mismo o 1, da un nº Entero, no Decimal")
                  #cuando se mantiene es_primo=True-->imprimo que ese nº es prim


# In[37]:


primo(10)

