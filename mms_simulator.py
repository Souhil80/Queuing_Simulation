import math
import random
import numpy as np
import matplotlib.pyplot as plt

# print(" =================Sisrlateur du modele M/M/S====================")
arrival_rate = float(input("Entrez le taux des arrivées : "))
service_rate = float(input("Entrez le taux de service : "))
# Demander à l'utilisateur d'entrer le nombre de serveurs (S)
num_max_servers = int(input("Entrez le nombre max de serveurs (S): "))
end_t = float(input("Entrez le temps de sisrlation: "))


def exponential(rate):
    return math.log(random.random()) / (-rate)

def sisrlate(ar, sr, num_servers, end_time):
    # Initialisation des paramètres de la sisrlation
    clock = 0  # Horloge de la sisrlation
    queue = []  # File d'attente des entités 
    next_arrival = exponential(ar)  # Prochain événement d'arrivée
    next_departure = [float('inf')] * num_servers  #************* Prochains événements de départ pour chaque serveur #
    # alternative 1 next_departure = [];    for i in range(num_servers ): next_departure.append(float('inf')) # alternative 2 next_departure = [float('inf') for _ in range(num_servers)]

        
    #T, Tq, Ts = 0, 0, 0  # Initialisation des métriques temporelles
    #Nq, N = 0, 0  # Initialisation des métriques liées à la file d'attente
    SU  = [0] * num_servers   # Initialisation de l'utilisation des serveurs #*************
    nb_arr, nb_dep = 0, 0  # Compteurs d'arrivées et de départs

    # Variables supplémentaires pour le calcul métriques
    sumN, nbN, upN, sumQ, nbQ, upQ = 0, 0, 0, 0, 0, 0
    sumSU = [0] * num_servers #*************
    upSU = [0] * num_servers #*************
    sumT, sumTq, sumTs = 0, 0, 0
    
    Nw = 0
    
    busy_servers = [False] * num_servers  # ************* Liste de booléens indiquant si chaque serveur est occupé
   # # alternative 1 busy_servers = []; for i in range(num_servers ): busy_servers.append(False) # alternative 2 busy_servers = [False for _ in range(num_servers)]

    # Boucle de sisrlation
    while queue or next_arrival <= end_time or any(next_departure[i] != float('inf') for i in range(num_servers)): # *************
        if (next_arrival <= min(next_departure) and next_arrival <= end_time): # *************
            # Si l'événement suivant est l'arrivée d'un client à next_arrival, exécution de l'événement d'arrivée
            clock = next_arrival

            # Mise à jour des variables pour le suivi du nombre d'entités dans le système
            sumN = sumN + nbN * (clock - upN)
            nbN = nbN + 1
            upN = clock

            nb_arr += 1  # Incrémentation du compteur d'arrivées

            # Planification du prochain événement d'arrivée
            interArrT = exponential(ar)
            next_arrival = clock + interArrT

            # Chercher le premier serveur disponible
            
            
            if False in busy_servers :   # *************
                server_index = busy_servers.index(False)
            else: 
                server_index = None
            
            # alternative server_index = busy_servers.index(False) if False in busy_servers else None

            if server_index is not None:   # Si un serveur est disponible, servir le client (Exécution du début de service)  # *************
                # Planification du prochain départ pour le serveur disponible
                serviceT = exponential(sr)
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
            # Exécution de l'événement de départ pour le premier serveur disponible
            clock = min(next_departure)
            server_index = next_departure.index(clock) 

            # Mise à jour des métriques pour le nombre d'entités dans le système
            sumN = sumN + nbN * (clock - upN)
            nbN = nbN - 1
            upN = clock
            nb_dep += 1  # Incrémentation du compteur de départs

            if nbQ > 0:
                # Si la file d'attente n'est pas vide, servir le prochain client dans la file (Exécution du début de service)
                sumQ = sumQ + nbQ * (clock - upQ)
                nbQ -= 1
                upQ = clock

                first = queue.pop(0)
                next_departure[server_index] = clock + exponential(sr)

                # Mise à jour des métriques pour le temps total, le temps en file d'attente et le temps de service
                sumT += (next_departure[server_index] - first)
                sumTq += (clock - first)
                sumTs += (next_departure[server_index] - clock)

            else:
                # Si la file d'attente est vide, mettre à jour les métriques pour l'utilisation du serveur
                sumSU[server_index] += clock - upSU[server_index]
                busy_servers[server_index] = False
                next_departure[server_index] = float('inf')

    # Calculer et afficher les résultats de la sisrlation
    Pw = Nw/nb_arr
    N = sumN / clock
    Nq = sumQ / clock
    
    SU = sum(sumSU) / (num_servers * clock)
    Ns = sum(sumSU) / clock
    T = sumT / nb_dep
    Tq = sumTq / nb_arr
    Ts = sumTs / nb_dep
    
    # Conversion en minutes
    T = T*60
    Tq = Tq*60
    Ts = Ts*60

    print(" ================= S=", num_servers,"====================")
    print("a :", round(SU, 3))
    print("Pw :", round(Nw, 3))
    print("N =", round(N, 3))
    print("Nq =", round(Nq, 3))
    print("Ns =", round(Ns, 3))
    print("T =", round(T, 3))
    print("Tq =", round(Tq, 3))
    print("Ts =", round(Ts, 3))
    

    return SU, Pw, N, Nq, Ns, T, Tq, Ts

#=============================================================================================




def plot_performance_vs_servers(ar, sr, end_time, num_max_servers):
    """
    Fonction pour tracer un graphique en fonction du nombre de serveurs.

    Paramètres :
        ar (float) : Taux d'arrivée de clients.
        sr (float) : Taux de service.
        num_servers_list (list) : Liste des nombres de serveurs à tester.
        end_time (float) : Durée de sisrlation.
    """
    # Initialiser des listes pour stocker les résultats de la sisrlation
    SU_values = []
    Pw_values = []
    N_values = []
    Nq_values = []
    Ns_values = []
    T_values = []
    Tq_values = []
    Ts_values = []
    num_servers_list = []
    i = 1
    a =  ar/(sr*i)
    while a >= 1:
        a = ar/(sr*i)
        i = i + 1
    
    num_min_servers = i

    # Sisrler pour chaque nombre de serveurs dans la liste
    for num_servers in  range( num_min_servers, num_max_servers + 1):
        SU, Pw, N, Nq, Ns, T, Tq, Ts = sisrlate(ar, sr, num_servers, end_time)
        SU_values.append(SU)
        Pw_values.append(Pw)
        N_values.append(N)
        Nq_values.append(Nq)
        Ns_values.append(Ns)
        T_values.append(T)
        Tq_values.append(Tq)
        Ts_values.append(Ts)
        num_servers_list.append(num_servers)

    # Tracer les résultats
    plt.figure(figsize=(10, 6))
    plt.plot(num_servers_list, N_values, label='Nombre moyen de patients dans le service des urgences')
    plt.plot(num_servers_list, Nq_values, label='Nombre moyen de patients en file d\'attente')
    plt.plot(num_servers_list, Ns_values, label='Nombre moyen de patients en salles de soins')

    plt.xlabel('Nombre de salles de soins')
    plt.ylabel('Nombre moyen de patiens')
    plt.legend()
    plt.title('Nombre moyen de patiens en fonction du nombre de salles de soins')
    plt.show()
    
    
    
    # Tracer les résultats
    #T_values_min = [x * 60 for x in T_values]
    #Tq_values_min = [x * 60 for x in Tq_values]
    # Ts_values_min = [x * 60 for x in Ts_values]
    plt.figure(figsize=(10, 6))
    plt.plot(num_servers_list, T_values, label='Temps moyen de sejour d\'un patient')
    plt.plot(num_servers_list, Tq_values, label='Temps moyen d\'attente d\'un patient')
    plt.plot(num_servers_list, Ts_values, label='Temps moyen de service')

    plt.xlabel('Nombre de serveurs')
    plt.ylabel('Temps moyen (minutes)')
    plt.legend()
    plt.title('Temps moyen de séjour et d\'attente de patients en fonction du nombre de serveurs')
    plt.show()
    
    # Tracer les résultats
    plt.figure(figsize=(10, 6))
    plt.plot(num_servers_list, SU_values, label='Taux d\'utilisation des salles de soins')
    plt.plot(num_servers_list, Pw_values, label='Probabilité d\'attente d\'un patient')

    plt.xlabel('Nombre de salles de soins')
    plt.ylabel('Probabilités et taux')
    plt.legend()
    plt.title('Probabilités et taux')
    plt.show()



plot_performance_vs_servers(arrival_rate, service_rate, end_t, num_max_servers)



