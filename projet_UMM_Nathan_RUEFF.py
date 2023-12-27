# Creation date: 2020-12-03
# Role: Fichier principal du projet de l'UMM.
# Author: Nathan RUEFF

"""
Règles du jeu et indications :

 On considère une chaîne de caractères de longueur L quelconque
(phrase mystère)

 Les caractères sont des codes ASCII codés sur un octet de 0 à 255
(alphabet de 256 caractères)

 Le jeu consiste à découvrir la phrase mystère. Le joueur soumet des
phrases de longueur L, et le système répond en indiquant simplement le
nombre de caractères en correspondance (match) et le nombre de
caractères mal placés (miss placed).

On souhaite résoudre ce problème en exploitant
un algorithme génétique.

 Pour cet algorithme, les chromosomes sont des
chaînes de caractères de taille L

 Il s’agit donc d’implanter les fonction de fitness,
de genèse, de sélection, de croisement et de
mutation et d’orchestrer la dynamique de
population (produire les générations successives)

Exemple : Si la phrase mystère est « Bonjour » et que le joueur propose la phrase « Bonsoir »,
        le système répondra 5 match et 1 miss placed.
          Si le joueur propose la phrase « Bonjour », le système répondra 7 match et 0 miss placed.
"""


"""
Importation des modules nécessaires au bon fonctionnement du programme.
"""
import random
import Levenshtein
import time
import functools

"""
Paramètres introduits :
 NG : le nombre de générations
 L : longueur des chromosomes (et de la phrase mystère)
 N : la taille de la population (nombre d’individus)
 TS : le taux de sélection (ou de reproduction)
 TM : le taux de mutation
"""

#  Fonction UMM : fonction principale du programme. Ne s'arrête pas tant qu'une solution n'est pas trouvée.
#  On demandera à l’utilisateur de choisir une phrase mystère
#  Puis le programme s’exécutera en listant le meilleur élément courant de la population

"""
Initiialisation des paramètres
"""

# N = 5000
# TS = 0.2
# TM = 0.8
# L = len(phrase_mystere)
# alpha = 0.5


def umm(N, TS, TM, phrase_mystere):
    generation_switch = 300
    L = len(phrase_mystere)
    start_time = time.time()
    stop_time = 0
    generation = 0
    resultat = []
    # On découpe la phrase mystère en portions de 100 caractères
    D = int(L/100)
    L_d = [i*100 for i in range(D+1)]
    # print(D, L_d) # DEBUG
    numero_portion = 1
    # On effectue le processus pour chaque portion
    for p in L_d[:-1]:
        # print(p) # DEBUG
        portion = phrase_mystere[p:p+100]
        # Initialisation des variables
        population = []
        solution_portion_trouvee = False

        # Création de la population initiale
        for i in range(N):
            population.append(genese(len(portion)))

        # Boucle principale du programme
        while not solution_portion_trouvee:
            # print(population) # DEBUG
            # On trie la population en fonction de leur fitness
            partial_fitness_leven = functools.partial(fitness_leven, phrase_reference=portion)
            partial_fitness_positional = functools.partial(fitness_positional, phrase_reference=portion)
            if generation < generation_switch:
                population = sorted(population, key=partial_fitness_leven)
            else:
                population = sorted(population, key=partial_fitness_positional, reverse=True)
            # On affiche le meilleur élément de la population
            print ("Portion : " + population[0] + "\n" + "Fitness : " + str(fitness_leven(population[0],portion)) + "\n" + "Génération : " + str(generation) + "\n" + "Portion n°" + str(numero_portion) + " sur " + str(D+1))
            # On vérifie si la solution est trouvée
            if population[0] == portion:
                resultat.append(population[0])
                solution_portion_trouvee = True
                numero_portion += 1
            else:
                # On crée la nouvelle population
                # print (len(population)) # DEBUG
                population = nouvelle_population(population, TS, TM, N)
                generation += 1
                # print (generation)  # DEBUG

    # On effectue la même chose pour la dernière portion
    derniere_portion = phrase_mystere[L_d[-1]:]
    # print(L_d[-1]) # DEBUG
    # Initialisation des variables
    population = []
    solution_derniere_portion_trouvee = False

    # Création de la population initiale
    for i in range(N):
        population.append(genese(len(derniere_portion)))

    # Boucle principale du programme
    while not solution_derniere_portion_trouvee:
        # print(population) # DEBUG
        # On trie la population en fonction de leur fitness
        partial_fitness_leven = functools.partial(fitness_leven, phrase_reference=derniere_portion)
        partial_fitness_positional = functools.partial(fitness_positional, phrase_reference=derniere_portion)
        if generation < generation_switch:
            population = sorted(population, key=partial_fitness_leven)
        else:
            population = sorted(population, key=partial_fitness_positional, reverse=True)
        # On affiche le meilleur élément de la population
        print("Portion : " + population[0] + "\n" + "Fitness : " + str(
            fitness_leven(population[0],derniere_portion)) + "\n" + "Génération : " + str(generation) + "\n" + "Portion n°" + str(D+1) + " sur " + str(D + 1))
        # On vérifie si la solution est trouvée
        if population[0] == derniere_portion:
            resultat.append(population[0])
            solution_derniere_portion_trouvee = True
            stop_time = time.time()
        else:
            # On crée la nouvelle population
            # print (len(population)) # DEBUG
            population = nouvelle_population(population, TS, TM, N)
            generation += 1
            # print (generation)  # DEBUG

    # On affiche le résultat
    return (round(stop_time - start_time, 3))
    # print("Nombre de générations nécessaires pour trouver la solution : " + str(generation) + "\n" + "Temps d'exécution : " + str(round(stop_time - start_time, 3)) + " secondes.")

def genese(L):
    """
    Fonction genese : génère un chromosome aléatoire de longueur L.
    :param L: longueur du chromosome
    :return: chromosome aléatoire
    """
    chromosome = ""
    for i in range(L):
        chromosome += chr(random.randint(0, 255))
    return chromosome

def tri_population(population, phrase_mystere):
    """
    Fonction tri_population : trie la population en fonction de leur fitness.
    :param population: population à trier
    :param phrase_mystere: phrase mystère
    :return: population triée
    """
    population_triee = []
    for chromosome in population:
        population_triee.append([chromosome, fitness_leven(chromosome, phrase_mystere)])
    return population_triee

# Fonction fitness :

def fitness_leven(C, phrase_reference):
    return Levenshtein.distance(C,phrase_reference)


def fitness_positional(C,phrase_reference):
    """
    Fonction fitness_leven : calcule le fitness d'un chromosome en prenant en compte l'ordre des caractères.
    :param C: chromosome
    :return: fitness du chromosome
    """
    match = 0
    miss_placed = 0
    for i in range(len(C)):
        if C[i] == phrase_reference[i]:
            match += 1
        elif C[i] in phrase_reference:
            # Pénalise davantage les positions incorrectes
            miss_placed += 0.5
    return match + miss_placed



def nouvelle_population(population, TS, TM, N):
    """
    Fonction nouvelle_population : crée une nouvelle population en fonction de la population actuelle.
    :param population: population actuelle
    :param TS: taux de sélection
    :param TM: taux de mutation
    :return: nouvelle population
    """
    nouvelle_population = []
    # On sélectionne les chromosomes pour la nouvelle population
    nouvelle_population = selection(population, TS)
    # On croise les chromosomes pour la nouvelle population
    nouvelle_population += reproduction_bat(nouvelle_population, N, TS)
    # On mute les chromosomes pour la nouvelle population
    nouvelle_population = mutation(nouvelle_population, TM)
    return nouvelle_population

def selection(population, TS):
    """
    Fonction selection : sélectionne les chromosomes pour la nouvelle population.
    :param population: population actuelle
    :param TS: taux de sélection
    :return: chromosomes sélectionnés
    """
    nouvelle_population = []
    for i in range(int(len(population) * TS)):
        nouvelle_population.append(population[i])
    # print ("Nombre chromosomes sélectionnés : " + str(len(nouvelle_population))) # DEBUG
    return nouvelle_population

# Fonction reproduction : deux individus P et M sont tirés au hasard parmis les
# individus sélectionnés. On tire au hasard un point de cut entre L/3 et 2L/3. On
# constitue un nouveau chromosome (individus) CM de la manière suivante
#  CM = concaténation(P[:cut], M[cut:])
#  Le nouvel individus est ajouté à la population : on itère la procédure
#  de manière à retrouver une population de N individus.

def reproduction(population, N, TS):
    """
    Fonction reproduction : reproduit deux chromosomes.
    :param population: population actuelle
    :return: chromosomes reproduits
    """
    nouvelle_population = []
    while len(nouvelle_population) < (1 - TS)*N :
        nouvelle_population.append(reproduction_chromosome(population))
    # print ("Nombre chromosomes reproduits : " + str(len(nouvelle_population))) # DEBUG
    return nouvelle_population

def reproduction_chromosome(population):
    """
    Fonction reproduction_chromosome : reproduit deux chromosomes.
    :param population: population actuelle
    :return: chromosome reproduit
    """
    P = population[random.randint(0, len(population) - 1)]
    M = population[random.randint(0, len(population) - 1)]
    cut = random.randint(int(len(P) / 3), int(2 * len(P) / 3))
    CM = P[:cut] + M[cut:]
    return CM

def reproduction_bat(population, N, TS):
    """
    Pour créer un nouveau chromosome, on choisit aléatoirement deux chromosomes parmis la population et pour chaque
    caractère du chromosome, je choisis aléatoirement le caractère du premier ou du deuxième chromosome.
    """
    nouvelle_population = []
    while len(nouvelle_population) < (1 - TS)*N :
        nouvelle_population.append(reproduction_bat_chromosome(population))
    # print ("Nombre chromosomes reproduits : " + str(len(nouvelle_population))) # DEBUG
    return nouvelle_population

def reproduction_bat_chromosome(population):
    """
    Pour créer un nouveau chromosome, on choisi aléatoirement deux chromosomes parmis la population et pour chaque
    caractère du chromosome, je choisis aléatoirement le caractère du premier ou du deuxième chromosome.
    """
    P = population[random.randint(0, len(population) - 1)]
    M = population[random.randint(0, len(population) - 1)]
    CM = ""
    for i in range(len(P)):
        if random.randint(0, 1) == 0:
            CM += P[i]
        else:
            CM += M[i]
    return CM

# Fonction de mutation : on sélectionne au
#hasard TM x N individus sur lesquels la
#mutation d’un gène va porter.
# Pour chaque individus sélectionné, on tire au
#hasard un gène (un caractère) parmi L et on
#change aléatoirement sa valeur

def mutation(population, TM):
    """
    Fonction mutation : mute les chromosomes pour la nouvelle population.
    :param population: population actuelle
    :param TM: taux de mutation
    :return: chromosomes mutés
    """
    nouvelle_population = []
    for chromosome in population:
        if random.random() < TM:
            nouvelle_population.append(mutation_chromosome(chromosome))
        else:
            nouvelle_population.append(chromosome)
    return nouvelle_population

def mutation_chromosome(chromosome):
    """
    Fonction mutation_chromosome : on tire au
    hasard un gène (un caractère) parmi L et on
    change aléatoirement sa valeur
    :param chromosome: chromosome à muter
    :return: chromosome muté
    """
    gene = random.randint(0, len(chromosome) - 1)
    chromosome = chromosome[:gene] + chr(random.randint(0, 255)) + chromosome[gene + 1:]
    return chromosome


phrase_1 = "La lueur douce du crépuscule baigne la ville endormie d'une atmosphère calme et apaisante."
phrase_2 = "Les étoiles scintillent, éclairant le ciel nocturne d'une splendeur mystérieuse et envoûtante."
phrase_3 = "Dans une petite ville tranquille, les rues pavées murmuraient des histoires du passé. Les maisons au style ancien bordaient les trottoirs, témoins silencieux du temps qui s'écoulait. Au centre de la place, une fontaine gracieuse dansait avec l'eau qui scintillait sous le doux éclat du soleil. Les habitants vaquaient à leurs occupations quotidiennes, créant une atmosphère chaleureuse et accueillante. Un café pittoresque, aux chaises en fer forgé et aux parasols colorés, attirait les passants en quête d'une pause bien méritée. L'odeur envoûtante du café fraîchement moulu flottait dans l'air, créant une symphonie olfactive qui invitaient les gens à s'installer et à savourer le moment. Les conversations animées et les rires légers remplissaient l'atmosphère, créant une toile sonore qui enveloppait le lieu. À l'angle de la rue, une librairie indépendante aux étagères remplies d'histoires captivantes invitait les amateurs de lecture à explorer des mondes imaginaires. Le son familier des pages tournées résonnait dans l'espace, tandis que les lecteurs se perdaient dans des aventures qui transcendaient le temps et l'espace. C'était un refuge pour l'esprit, un endroit où l'imagination pouvait s'épanouir librement. À quelques pas de là, un parc verdoyant offrait une échappatoire à ceux qui cherchaient la sérénité. Les enfants riaient en jouant sur les balançoires, les couples se promenaient main dans la main, et les aînés trouvaient refuge sur les bancs ombragés. Les arbres majestueux, témoins d'innombrables saisons, racontaient silencieusement l'histoire du temps qui s'écoulait. Le soleil commençait à décliner lentement à l'horizon, baignant la ville d'une lumière dorée. Les façades des bâtiments s'illuminaient, créant une palette de couleurs éblouissantes qui capturaient l'essence de la vie urbaine. Les bruits de la journée faisaient place à une quiétude paisible, laissant place à la contemplation et à la réflexion. C'était dans ces moments, lorsque le crépuscule enveloppait la ville de son manteau, que l'on pouvait ressentir la magie subtile qui émanait de chaque rue, de chaque coin. La petite ville tranquille, loin des tumultes du monde moderne, était un sanctuaire intemporel où les moments simples se transformaient en souvenirs éternels."


# umm(2900, 0.26, 0.44, phrase_3)