import matplotlib.pyplot as plt
import pandas as pd
import os
# Liste des noms de fichiers CSV
file_names = ['Ajout vidéo.csv', 'Ajout raw.csv', 'Ajout pdf.csv', 'Ajout mp3.csv']
file_names_without_extension = [os.path.splitext(file_name)[0] for file_name in file_names]
# Couleurs pour chaque courbe
colors = ['r', 'g', 'b', 'c']

# Initialiser une liste pour stocker le nombre total de paquets pour chaque fichier
total_packets = []

# Parcourir les fichiers CSV et tracer les courbes
for file_name, color in zip(file_names, colors):
    # Charger les données CSV
    data = pd.read_csv(file_name, delimiter=',')
    
    # Extraire les données d'intervalle et de paquets
    intervals = data['Interval start']
    packets = data['All Packets']
    
    # Calculer le nombre total de paquets
    total_packets.append(packets.sum())
    
    
    # Tracer la courbe
    plt.plot(intervals, packets, color, label=os.path.splitext(file_name)[0])

# Ajouter des légendes et des étiquettes pour la courbe
plt.xlabel('Secondes')
plt.ylabel('Packets par intervalle de 1 seconde')
plt.title('Packet Distribution')
plt.legend()

# Afficher le graphe
plt.grid(True)
plt.savefig('packet_distribution_plot.png')
plt.show()
# Tracer le diagramme à barres pour le nombre total de paquets

plt.bar(file_names_without_extension, total_packets, color=colors)
plt.xlabel('Fonctions')
plt.ylabel('Paquets totaux')
plt.title('Total de  Packets pour chaque fonction')
plt.savefig('total_packets_bar_chart.png')
plt.show()