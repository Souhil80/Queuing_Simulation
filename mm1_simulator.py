import random

lam = 5
mu = 7
time_sim = 100000
def simulate_mm1 (l , m, time_sim) :
    clock = 0
    queue= []
    
    arrival = random.expovariate(lam)
    departure = float('inf') 
    
    NbC = 0
    
    Ni = 0
    sumNi = 0
    upSumNi = 0
    
    Nqi = 0
    sumNqi = 0
    upSumNqi = 0
    
    sumTS = 0
    upServer = 0
    
    
    sumTi = 0
    sumTqi = 0
    sumTsi = 0
    
    
    server_free = True

    while clock <= time_sim:
        # print(f"clock = {clock}")
        if arrival < departure:
            clock = arrival
            sumNi = sumNi + Ni*(clock - upSumNi)
            upSumNi = clock
            Ni=Ni+1
            if server_free : # Debut de service
                  departure =  clock + random.expovariate(mu)  
                  server_free = False
                  upServer = clock
                  
                  sumTi = sumTi + (departure - arrival)
                  
                  sumTsi = sumTsi + (departure - clock)
             
                  start = clock
            else:
                sumNqi = sumNqi + Nqi*(clock - upSumNqi)
                upSumNqi = clock
                Nqi = Nqi + 1
                
                
                
                queue.append(arrival)
                
            arrival = clock + random.expovariate(lam)  
        else :
            clock = departure
            sumNi = sumNi + Ni*(clock - upSumNi)
            upSumNi = clock
            Ni=Ni - 1
            
            #sumTi = sumTi + (departure - ....)
            NbC = NbC + 1
            if queue: # Debut de service 
                firstArr = queue.pop(0)
                departure =  clock + random.expovariate(mu)  
                sumTi = sumTi + (departure - firstArr)
               
                sumTqi = sumTqi + (clock - firstArr)
                
                sumTsi = sumTsi + (departure - clock)
                
                sumNqi = sumNqi + Nqi*(clock - upSumNqi)
                upSumNqi = clock
                
                Nqi = Nqi - 1
            else:
                server_free = True
                sumTS = sumTS + clock - upServer
                departure = float('inf') 
            
            
    N = sumNi/clock
    
    Nq = sumNqi/clock
    
    SU = sumTS/clock
    
    T = sumTi/NbC
    
    Tq = sumTqi/NbC
    
    Ts = sumTsi/NbC
    
    print(" =================Simulateur du modele M/M/1====================")
    print("N =", round(N, 3))
    print("Nq =", round(Nq, 3))
    print("T =", round(T, 3))
    print("Tq =", round(Tq, 3))
    print("Ts =", round(Ts, 3))
    print("Utilisation du serveur :", round(SU, 3))

    return N, Nq, T, Tq, Ts, SU


# simulate(lam,mu,end_t )
#%=======================================================================================================================================


# Probabilité d'attente d'un client
# Probabilité que le serveur est occupé
# Nombre moyen de clients en service (au guichet)
def rho(): 
   return lam / mu

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
   return 1 / (mu - lam)
# Temps moyen d'attente d'un client
def Tq_():
   return rho() / (mu * (1 - rho()))

# Temps moyen de service
def Ts_():
   return 1 / mu

if  rho() < 1:
    N, Nq, T, Tq, Ts, su = simulate(lam,mu,time_sim ) 

    print(" ================= M/M/1 analytique ====================")

    print ("N = ",  round(N_(),3))
    print ("Nq = " ,  round(Nq_(),3))
    print ("Ns = ",  round(Ns_(),3))
    print ("T = ",  round(T_(),3) )
    print ("Tq = ",  round(Tq_(),3))
    print ("Ts = ",  round(Ts_(),3))
    print ("rho = ",  round(rho(),3))
    print ("P_0 = ", round(p_0(),3))
    
    print(" ================= Erreurs relatives: |analytique - simulation|*100/ analytique ====================")
    
    print ("Erreur relative N = ",  round(abs((N_()-N))*100/N_(),3),"%")
    print ("Erreur relative  Nq = " ,  round(abs((Nq_()-Nq))*100/Nq_(),3),"%")
    print ("Erreur relative  Ns = ",  round(abs((Ns_()-su))*100/Ns_(),3),"%")
    print ("Erreur relative  T = ",  round(abs((T_()-T))*100/T_(),3),"%")
    print ("Erreur relative  Tq = ",  round(abs((Tq_()-Tq))*100/Tq_(),3),"%")
    print ("Erreur relative  Ts = ",  round(abs((Ts_()-Ts))*100/Ts_(),3),"%")
    print ("Erreur relative  rho = ",  round(abs((rho()-su))*100/rho(),3),"%")
 
else:
   print("Le systeme n'est pas stationnaire: rho = ", round(rho(),3)," > 1")