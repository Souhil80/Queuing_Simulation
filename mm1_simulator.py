import math
import random

# print(" =================Sisrlateur du modele M/M/1====================")
arrival_rate = float(input("Entrez le taux des arrivées: "))
service_rate = float(input("Entrez le taux de service: "))
end_t = float(input("Entrez le temps de sisrlation: "))

def exponential(rate):
    return - math.log(random.random()) / (rate)

def sisrlate(ar, sr, end_time):
    clock = 0
    queue = []
    next_arrival = exponential(ar)
    next_departure = float('inf')
    T, Tq, Ts = 0, 0, 0
    Nq, N = 0, 0
    su = 0
    nb_arr, nb_dep = 0, 0


 
    sumQ, nbQ, sumN, nbS, susum, upN, upQ, upU = 0, 0, 0, 0, 0, 0, 0, 0
    sumT, sumTq, sumTs = 0, 0, 0
    busy = False

    while not (not queue and next_arrival > end_time and next_departure == float('inf')):
        if (next_arrival <= next_departure and next_arrival < end_time):
            
            clock = next_arrival
            
            sumN = sumN + nbS * (clock - upN)
            nbS = nbS + 1
            upN = clock
            
            
           
            nb_arr += 1
            
            interArrT = exponential(ar)
            next_arrival = next_arrival + interArrT
            
            if not busy:
                
                
                serviceT = exponential(sr)
                next_departure = clock + serviceT
                
                sumT = sumT + (next_departure - clock)
                sumTs = sumTs + (next_departure - clock)
                
                #susum += busy * (clock - upU)
                upU = clock

                
                busy = True
            else:
                
                sumQ = sumQ + nbQ * (clock - upQ)
                upQ = clock
                nbQ += 1

                queue.append(clock)
                
        else:
            clock = next_departure
            
            
            sumN = sumN + nbS * (clock - upN)
            nbS = nbS - 1
            upN = clock
            nb_dep += 1
            
            
            if nbQ > 0:
                
                sumQ = sumQ + nbQ * (clock - upQ)
                nbQ -= 1
                upQ = clock
                
                first = queue.pop(0)
                next_departure = clock + exponential(sr)
                
                sumT += (next_departure - first)
                sumTq += (clock - first)
                sumTs += (next_departure - clock)
              
            else:
                susum += clock - upU
                upU = clock
    
                busy = False
               
                next_departure = float('inf')
               

    N = sumN / clock
    Nq = sumQ / clock
    su = susum / clock
    T = sumT / nb_dep
    Tq = sumTq / nb_arr
    Ts = sumTs / nb_dep


    print(" =================Sisrlateur du modele M/M/1====================")

    print("N =", round(N,3))
    print("Nq =", round(Nq,3))
    print("T =", round(T,3))
    print("Tq =", round(Tq,3))
    print("Ts =", round(Ts,3))
    print("Server Utilization:", round(su,3))
    return N, Nq, T, Tq, Ts, su


# sisrlate(ar,sr,end_t )
#%=======================================================================================================================================
import matplotlib.pyplot as plt


# Probabilité d'attente d'un client
# Probabilité que le serveur est occupé
# Nombre moyen de clients en service (au guichet)
def rho(): 
   return ar / sr

# Probabilité que le système est vide (Aucun client dans le système)
def p_0():
   return 1 - rho()

# Probabilité de n clients dans le système 
def p_n(n):
   return (1 - rho())*rho()**n

# Nombre moyen de clients dans le système
def N_():
   return rho() / (1 - rho())
# Nombre moyen de clients en attente
def Nq_():
   return rho()**2 / (1 - rho())

# Nombre moyen de clients en service (au guichet)
def Ns_(): 
   return rho()

# Temps moyen qu’un client passe dans le système (attente + service). (temps moyen de séjour d’un client dans le système)
def T_():
   return 1 / (sr - ar)
# Temps moyen d'attente d'un client
def Tq_():
   return rho() / (sr * (1 - rho()))

# Temps moyen de service
def Ts_():
   return 1 / sr

if  rho() < 1:
    N, Nq, T, Tq, Ts, su = sisrlate(arrival_rate,service_rate,end_t ) 

    print(" ================= M/M/1 analytique ====================")

    print ("N = ",  round(N_(),3))
    print ("Nq = " ,  round(Nq_(),3))
    print ("Ns = ",  round(Ns_(),3))
    print ("T = ",  round(T_(),3) )
    print ("Tq = ",  round(Tq_(),3))
    print ("Ts = ",  round(Ts_(),3))
    print ("rho = ",  round(rho(),3))
    print ("P_0 = ", round(p_0(),3))
    
    print(" ================= Ecart normaliséanalytique sisrlation ====================")
    
    print ("Ecart N = ",  round((N_()-N)/N_(),3),"%")
    print ("Ecart Nq = " ,  round((Nq_()-Nq)/Nq_(),3),"%")
    print ("Ecart Ns = ",  round((Ns_()-su)/Ns_(),3),"%")
    print ("Ecart T = ",  round((T_()-T)/T_(),3),"%")
    print ("Ecart Tq = ",  round((Tq_()-Tq)/Tq_(),3),"%")
    print ("Ecart Ts = ",  round((Ts_()-Ts)/Ts_(),3),"%")
    print ("Ecart rho = ",  round((rho()-su)/rho(),3),"%")
 
else:
   print("Le systeme n'est pas stationnaire: rho = ", round(rho(),3)," > 1")