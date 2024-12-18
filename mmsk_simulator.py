import math
import random
import matplotlib.pyplot as plt


def interArrivalsG(rate):
    return math.log(random.random()) / (-rate)
    #return random.gammavariate(5, rate)
    #return random.gammavariate(4, 0.005)
    
def serviceG(rate):
     #return random.lognormvariate(-1.598612, 1)
   return math.log(random.random()) / (-rate)
    #a = rate-rate/2
    #b = rate + rate/2
    # return a + random.betavariate(2, 5) * (b-a)
    

def simulate(lam, mu, num_servers, K, end_time):
    # Initialisation des paramètres de la simulation
    clock = 0  # Horloge de la simulation
    queue = []  # File d'attente des entités 
    next_arrival = interArrivalsG(lam)  # Prochain événement d'arrivée
    next_departure = [float('inf')] * num_servers  #************* Prochains événements de départ pour chaque serveur #
    # alternative 1 next_departure = [];    for i in range(num_servers ): next_departure.append(float('inf')) # alternative 2 next_departure = [float('inf') for _ in range(num_servers)]

        
    #T, Tq, Ts = 0, 0, 0  # Initialisation des métriques temporelles
    #Nq, N = 0, 0  # Initialisation des métriques liées à la file d'attente
    SU  = [0] * num_servers   # Initialisation de l'utilisation des serveurs #*************
    nb_arr, nb_dep, nb_rej = 0, 0, 0  # Compteurs d'arrivées, de départs et de rejet

    # Variables supplémentaires pour le calcul métriques
    sumN, nbN, upN, sumQ, nbQ, upQ, upV = 0, 0, 0, 0, 0, 0, 0
    sumSU = [0] * num_servers #*************
    upSU = [0] * num_servers #*************
    sumT, sumTq, sumTs, sumV = 0, 0, 0, 0
    
    TabN = []
    TabUpN = []
    Nw = 0
   # v = True
    
    
    busy_servers = [False] * num_servers  # ************* Liste de booléens indiquant si chaque serveur est occupé
   # # alternative 1 busy_servers = []; for i in range(num_servers ): busy_servers.append(False) # alternative 2 busy_servers = [False for _ in range(num_servers)]

    # Boucle de simulation
    while queue or next_arrival <= end_time or any(next_departure[i] != float('inf') for i in range(num_servers)): # *************
        if (next_arrival <= min(next_departure) and next_arrival <= end_time): # *************
            if nbN < K:
                # Si l'événement suivant est l'arrivée d'un client à next_arrival, exécution de l'événement d'arrivée
                clock = next_arrival
    
                # Mise à jour des variables pour le suivi du nombre d'entités dans le système
                sumN = sumN + nbN * (clock - upN)
                nbN = nbN + 1
                upN = clock
                
                TabN.append(nbN)
                TabUpN.append(upN)
    
                nb_arr += 1  # Incrémentation du compteur d'arrivées
    
                # Planification du prochain événement d'arrivée
                interArrT = interArrivalsG(lam)
                next_arrival = clock + interArrT
    
                # Chercher le premier serveur disponible
                
                if all(element is False for element in busy_servers) :
                    sumV = sumV + (clock - upV)
                   # v = False
                
                
                if False in busy_servers :   # *************
                    server_index = busy_servers.index(False)
                else: 
                    server_index = None
                
                # alternative server_index = busy_servers.index(False) if False in busy_servers else None
                    

                if server_index is not None:   # Si un serveur est disponible, servir le client (Exécution du début de service)  # *************
                    # Planification du prochain départ pour le serveur disponible
                    serviceT = serviceG(mu)
                    next_departure[server_index] = clock + serviceT  # *************
    
                    # Mise à jour des métriques pour le temps total, le temps de service et l'utilisation du serveur
                    sumT = sumT + (next_departure[server_index] - clock)
                    sumTs = sumTs + (next_departure[server_index] - clock)
                    upSU[server_index] = clock  # *************
                    busy_servers[server_index] = True
                    
                
                       
    
                else:
                    # Si tous les serveurs sont occupés, mettre le client arrivant en file d'attente
                    queue.append(clock)
                    sumQ = sumQ + nbQ * (clock - upQ)
                    nbQ += 1
                    upQ = clock
                    Nw =Nw +1
        
            else:
                clock = next_arrival
                # Planification du prochain événement d'arrivée
                interArrT = interArrivalsG(lam)
                next_arrival = clock + interArrT
                nb_rej = nb_rej + 1

        else:
            # Exécution de l'événement de départ pour le premier serveur disponible
            clock = min(next_departure)
            server_index = next_departure.index(clock) 

            # Mise à jour des métriques pour le nombre d'entités dans le système
            sumN = sumN + nbN * (clock - upN)
            nbN = nbN - 1
            upN = clock
            
            TabN.append(nbN)
            TabUpN.append(upN)
            
            nb_dep += 1  # Incrémentation du compteur de départs

            if nbQ > 0:
                # Si la file d'attente n'est pas vide, servir le prochain client dans la file (Exécution du début de service)
                sumQ = sumQ + nbQ * (clock - upQ)
                nbQ -= 1
                upQ = clock

                first = queue.pop(0)
                next_departure[server_index] = clock + serviceG(mu)

                # Mise à jour des métriques pour le temps total, le temps en file d'attente et le temps de service
                sumT += (next_departure[server_index] - first)
                sumTq += (clock - first)
                sumTs += (next_departure[server_index] - clock)

            else:
                # Si la file d'attente est vide, mettre à jour les métriques pour l'utilisation du serveur
                sumSU[server_index] += clock - upSU[server_index]
                busy_servers[server_index] = False
                next_departure[server_index] = float('inf')
                upV = clock                
               # v = True

    # Calculer et afficher les résultats de la simulation
    Pw = Nw/nb_dep
    N = sumN / clock
    Nq = sumQ / clock
    
    SU = sum(sumSU) / (num_servers * clock)
    Ns = sum(sumSU) / clock
    T = sumT / nb_dep
    Tq = sumTq / nb_dep
    Ts = sumTs / nb_dep
    p_rej = nb_rej/ (nb_arr + nb_rej)
    P0 = sumV/clock
    
    # Conversion en minutes
   # T = T*60
   # Tq = Tq*60
   # Ts = Ts*60

    print(" ================= lamda=", lam," mu=",mu," S=", num_servers," ,K=", K,"====================")
    print("a :", round(SU, 3))
    
    print("P0 :", round(P0, 3))
    print("Pw :", round(Pw, 3))
    print("P_rej :", round(p_rej, 3))
    print("N =", round(N, 3))
    print("Nq =", round(Nq, 3))
    print("Ns =", round(Ns, 3))
    print("T =", round(T, 3))
    print("Tq =", round(Tq, 3))
    print("Ts =", round(Ts, 3))
    
    
    print("nb_dep =", round(nb_dep, 3))
    
    print("nb_arr =", round(nb_arr, 3))
    print("Nw =", round(Nw, 3))
    

    return SU,P0, Pw, p_rej, N, Nq, Ns, T, Tq, Ts, TabN, TabUpN

#=============================================================================================

##########################################################################################################################################################
def display_simulation ():
    
    
    lam = float(input("Entrez le taux des arrivées (lamdba): "))
    mu = float(input("Entrez le taux de service (mu): "))
    num_servers = num_max_servers = int(input("Entrez le nombre de serveurs : "))
    K = int(input("Entrez la capacité maximale du systeme (K): "))
    end_time = float(input("Entrez le temps de simulation: ")) 
    
    SU,P0, Pw, p_rej, N, Nq, Ns, T, Tq, Ts, TabN, TabUpN = simulate(lam, mu, num_servers, K, end_time)
    
    ##========================================================================================================
    plt.figure(figsize=(15, 6))
    plt.plot(TabUpN, TabN, label='Nombre de patients dans le service des urgences', color = 'blue')
    #plt.fill_between(TabUpN, TabN, color='blue', alpha=0.4,)

    plt.xlabel('Temps')
    plt.ylabel('Nombre de patiens')
    plt.legend()
    plt.title(f'Nombre de patients aux urgences en fonction du Temps ')
    plt.grid(True)
    plt.show()
##=======================================================================================================



##########################################################################################################################################################


def plot_perform_servers ():
    """
    Fonction pour tracer un graphique en fonction du nombre de serveurs.

    Paramètres :
        lam (float) : Taux d'arrivée de clients.
        mu (float) : Taux de service.
        num_servers_list (list) : Liste des nombres de serveurs à tester.
        end_time (float) : Durée de simulation.
    """
    lam = float(input("Entrez le taux des arrivées (lamdba): "))
    mu = float(input("Entrez le taux de service (mu): "))
    num_min_servers = num_max_servers = int(input("Entrez le nombre min de serveurs : "))
    # Demander à l'utilisateur d'entrer le nombre de serveurs (S)
    num_max_servers = int(input("Entrez le nombre max de serveurs : "))
    K = int(input("Entrez la capacité maximale du systeme (K): "))
    end_time = float(input("Entrez le temps de simulation: ")) 
    
    
    
    
    # Initialiser des listes pour stocker les résultats de la simulation
    SU_values = []
    P0_values = []
    Pw_values = []
    N_values = []
    Nq_values = []
    Ns_values = []
    T_values = []
    Tq_values = []
    Ts_values = []
    Prej_values = []
    num_servers_list = []
    i = 1
    a =  lam/(mu*i)
    while a >= 1:
        a = lam/(mu*i)
        i = i + 1
    
    #num_min_servers = 1

    # Simuler pour chaque nombre de serveurs dans la liste
    for num_servers in  range( num_min_servers, num_max_servers + 1):
        SU,P0, Pw, p_rej, N, Nq, Ns, T, Tq, Ts, TabN, TabUpN = simulate(lam, mu, num_servers, K, end_time)
        SU_values.append(SU)
        P0_values.append(P0)
        Pw_values.append(Pw)
        N_values.append(N)
        Nq_values.append(Nq)
        Ns_values.append(Ns)
        T_values.append(T)
        Tq_values.append(Tq)
        Ts_values.append(Ts)
        Prej_values.append(p_rej)
        num_servers_list.append(num_servers)
##========================================================================================================
        plt.figure(figsize=(15, 6))
        plt.plot(TabUpN, TabN, label='Nombre de patients dans le service des urgences', color = 'blue')
        #plt.fill_between(TabUpN, TabN, color='blue', alpha=0.4,)

        plt.xlabel('Temps')
        plt.ylabel('Nombre de patiens')
        plt.legend()
        plt.title(f'Nombre de patients aux urgences en fonction du Temps - S= {num_servers}')
        plt.grid(True)
        plt.show()
##=======================================================================================================
    # Tracer les résultats
    plt.figure(figsize=(15, 6))
    plt.plot(num_servers_list, N_values, label='Nombre moyen de patients aux urgences (N)')
    plt.plot(num_servers_list, Nq_values, label='Nombre moyen de patients en file d\'attente (Nq)')
    plt.plot(num_servers_list, Ns_values, label='Nombre moyen de patients en salles de soins (Ns)')

    plt.xlabel('Nombre de salles de soins')
    plt.ylabel('Nombre moyen de patiens')
    plt.legend()
    plt.title('Nombre moyen de patiens en fonction du nombre de salles de soins')
    plt.xticks(range(num_min_servers, num_max_servers))
    plt.grid(True)
    plt.show()
    
    
    
    # Tracer les résultats
    T_values = [x * 60 for x in T_values]
    Tq_values = [x * 60 for x in Tq_values]
    Ts_values = [x * 60 for x in Ts_values]
    plt.figure(figsize=(15, 6))
    plt.plot(num_servers_list, T_values, label='Temps moyen de sejour d\'un patient (T)')
    plt.plot(num_servers_list, Tq_values, label='Temps moyen d\'attente d\'un patient (Tq)')
    #plt.plot(num_servers_list, Ts_values, label='Temps moyen de service')

    plt.xlabel('Nombre de serveurs')
    plt.ylabel('Temps moyen (minutes)')
    plt.legend()
    plt.xticks(range(num_min_servers, num_max_servers))
    plt.grid(True)
    plt.title('Temps moyen (en minutes) de séjour et d\'attente de patients en fonction du nombre de salles de soins')
    plt.show()
    
    # Tracer les résultats
    plt.figure(figsize=(15, 6))
    plt.plot(num_servers_list, SU_values, label='Taux d\'utilisation des salles de soins (a)')
    plt.plot(num_servers_list, Pw_values, label='Probabilité d\'attente d\'un patient (Pw)')
    plt.plot(num_servers_list,  Prej_values, label='Probabilité de rejet d\'un patients(Pk)')
    #  plt.plot(num_servers_list,  P0_values, label='Probabilité que le service soit vide')


    plt.xlabel('Nombre de salles de soins')
    plt.ylabel('Probabilités et taux')
    plt.legend()
    plt.xticks(range(num_min_servers, num_max_servers))
    plt.grid(True)
    plt.title('Probabilités et taux')
    plt.show()



##########################################################################################################################################################


def plot_perform_capacity():
    """
    Fonction pour tracer un graphique en fonction de la capacité maximale du système (K).

    Paramètres :
        lam (float) : Taux d'arrivée de clients.
        mu (float) : Taux de service.
        end_time (float) : Durée de simulation.
        num_servers (int) : Nombre de serveurs.
        min_capacity (int) : Capacité minimale du système.
        max_capacity (int) : Capacité maximale du système.
    """
    
    
    lam = float(input("Entrez le taux des arrivées (lamdba): "))
    mu = float(input("Entrez le taux de service (mu): "))
    num_servers = int(input("Entrez le nombre  de serveurs : "))
    # Demander à l'utilisateur d'entrer le nombre de serveurs (S)
    min_capacity = int(input("Entrez  la capacité minimale : "))
    max_capacity = int(input("Entrez la capacité maximale: "))
    end_time = float(input("Entrez le temps de simulation: ")) 
    

    # Initialiser des listes pour stocker les résultats de la simulation
    SU_values = []
    P0_values = []
    Pw_values = []
    N_values = []
    Nq_values = []
    Ns_values = []
    T_values = []
    Tq_values = []
    Ts_values = []
    Prej_values = []
    capacity_list = []
    i = 1
    a =  lam/(mu*i)
    while a >= 1:
        a = lam/(mu*i)
        i = i + 1
    
    #num_min_servers = 1

    # Simuler pour chaque nombre de serveurs dans la liste
    for capacity in  range( min_capacity, max_capacity + 1):
        SU,P0, Pw, p_rej, N, Nq, Ns, T, Tq, Ts, TabN, TabUpN = simulate(lam, mu, num_servers, capacity, end_time)
        SU_values.append(SU)
        P0_values.append(P0)
        Pw_values.append(Pw)
        N_values.append(N)
        Nq_values.append(Nq)
        Ns_values.append(Ns)
        T_values.append(T)
        Tq_values.append(Tq)
        Ts_values.append(Ts)
        Prej_values.append(p_rej)
        capacity_list.append(capacity)

       # plt.figure(figsize=(15, 6))
        #plt.plot(TabUpN, TabN, label='Nombre de patients dans le service des urgences', color = 'blue')
        #plt.fill_between(TabUpN, TabN, color='blue', alpha=0.4,)

        #plt.xlabel('Temps')
        #plt.ylabel('Nombre de patiens')
        #plt.legend()
       # plt.title(f'Nombre de patients aux urgences en fonction du Temps K={capacity} ')
       # plt.grid(True)
       # plt.show()
#############################################################################""

    ticks = [tick for tick in  capacity_list if tick % 10 == 0]


    # Tracer les résultats
    plt.figure(figsize=(15, 6))
    plt.plot(capacity_list, N_values, label='Nombre moyen de patients aux urgences (N)')
    plt.plot(capacity_list, Nq_values, label='Nombre moyen de patients en file d\'attente (Nq)')
    plt.plot(capacity_list, Ns_values, label='Nombre moyen de patients en salles de soins (Ns)')

    plt.xlabel('Nombre de salles de soins')
    plt.ylabel('Nombre moyen de patiens')
    plt.legend()
    plt.title('Nombre moyen de patiens en fonction du nombre de salles de soins')
    plt.xticks(ticks)
    plt.grid(True)
    plt.show()
    
    

    
    # Tracer les résultats
    T_values = [x * 60 for x in T_values]
    Tq_values = [x * 60 for x in Tq_values]
    Ts_values = [x * 60 for x in Ts_values]
    plt.figure(figsize=(15, 6))
    plt.plot(capacity_list, T_values, label='Temps moyen de sejour d\'un patient (T)')
    plt.plot(capacity_list, Tq_values, label='Temps moyen d\'attente d\'un patient (Tq)')
    #plt.plot(num_servers_list, Ts_values, label='Temps moyen de service')

    plt.xlabel('Nombre de serveurs')
    plt.ylabel('Temps moyen (minutes)')
    plt.legend()
    plt.xticks(ticks)
    plt.grid(True)
    plt.title('Temps moyen (en minutes) de séjour et d\'attente de patients en fonction du nombre de salles de soins')
    plt.show()
    
    # Tracer les résultats
    plt.figure(figsize=(15, 6))
    plt.plot(capacity_list, SU_values, label='Taux d\'utilisation des salles de soins (a)')
    plt.plot(capacity_list, Pw_values, label='Probabilité d\'attente d\'un patient (Pw)')
    plt.plot(capacity_list,  Prej_values, label='Probabilité de rejet d\'un patients(Pk)')
    #  plt.plot(num_servers_list,  P0_values, label='Probabilité que le service soit vide')


    plt.xlabel('Nombre de salles de soins')
    plt.ylabel('Probabilités et taux')
    plt.legend()
    plt.xticks(ticks)
    plt.grid(True)
    plt.title('Probabilités et taux')
    plt.show()

##########################################################################################################################################################



# Programme principal
while True:
    print("Menu :")
    print("1. display simulation 1")
    print("2. Performances en fonction du nombre de serveurs")
    print("3. Performances en fonction de la capacité du systeme")
    print("0. Quitter")

    choix = input("Choisissez une fonctionnalité: ")

    if choix == "1":
        display_simulation ()
    elif choix == "2":
        plot_perform_servers()
    elif choix == "3":
        plot_perform_capacity()
    elif choix == "0":
        break
    else:
        print("Choix invalide. Veuillez saisir un nombre valide.")




