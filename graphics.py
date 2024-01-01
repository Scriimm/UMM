import matplotlib.pyplot as plt
from UMM import umm

def generate_and_plot(param_name, param_values, fixed_params, phrase_mystere):
    times = []

    for param_value in param_values:

        # Construire les arguments pour umm en fonction du paramètre à faire varier
        args = dict(fixed_params)
        args[param_name] = param_value

        # Appel de la fonction UMM avec les paramètres en cours
        time_taken = umm(phrase_mystere=phrase_mystere, **args)
        times.append(time_taken)

    # Trouver l'indice du minimum
    min_index = times.index(min(times))

    plt.plot(param_values, times, marker='o')

    # Annoter le point correspondant au minimum
    plt.annotate('Min: {min(times):.3f}', xy=(param_values[min_index], min(times)),
                 xytext=(param_values[min_index] + 100, min(times) + 0.1),
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 )

    plt.title(f'Efficacité de l\'algorithme UMM en variant {param_name}')
    plt.xlabel(param_name)
    plt.ylabel('Temps (s)')
    plt.show()

# Exemple d'utilisation
N_values = list(range(500, 5000, 100))
TS_values = [i * 0.02 for i in range(1, 41)]
TM_values = [i * 0.02 for i in range(1, 41)]

# Choisissez une valeur fixe pour les deux autres paramètres
fixed_params = {'N': 2900, 'TS': 0.26, 'TM': 0.44, 'utilisation': 'auto'}
phrase_mystere = "Je suis une phrase de test et je suis assez longue pour que l'algorithme UMM soit efficace."

# Générer et afficher les graphiques pour N, TS, et TM
generate_and_plot('N', N_values, fixed_params, phrase_mystere)
generate_and_plot('TS', TS_values, fixed_params, phrase_mystere)
generate_and_plot('TM', TM_values, fixed_params, phrase_mystere)
