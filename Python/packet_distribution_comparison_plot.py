import matplotlib.pyplot as plt
import pandas as pd
import os

# Liste des noms de fichiers CSV pour l'ajout
addition_file_names = ['Ajout vidéo.csv', 'Ajout raw.csv', 'Ajout pdf.csv', 'Ajout mp3.csv']

# Liste des noms de fichiers CSV pour le téléchargement
download_file_names = ['Téléch vidéo.csv', 'Tel raw.csv', 'Tel pdf.csv', 'Tel mp3.csv']

# Couleurs pour chaque courbe
colors = ['tab:blue','tab:red']
names = ['Ajout vidéo', 'Ajout raw', 'Ajout pdf', 'Ajout mp3', 'Téléchargement vidéo', 'Téléchargement raw', 'Téléchargement pdf', 'Téléchargement mp3']
Namestel =['Téléchargement vidéo', 'Téléchargement raw', 'Téléchargement pdf', 'Téléchargement mp3']

# Initialiser une liste pour stocker le nombre total de paquets pour chaque fonction
total_packets_addition = []
total_packets_download = []

# Créer une nouvelle figure
plt.figure(figsize=(12, 8))

# Parcourir les fichiers CSV pour l'ajout et tracer les courbes
for i, (addition_file, download_file) in enumerate(zip(addition_file_names, download_file_names), start=1):
    # Tracer la courbe pour l'ajout
    plt.subplot(2, 2, i)
    
    # Charger les données CSV pour l'ajout
    data = pd.read_csv(addition_file, delimiter=',')
    intervals = data['Interval start']
    packets = data['All Packets']
    plt.plot(intervals, packets, colors[0], label=names[i-1])
    total_packets_addition.append(packets.sum())
    
    # Charger les données CSV pour le téléchargement
    data = pd.read_csv(download_file, delimiter=',')
    intervals = data['Interval start']
    packets = data['All Packets']
    plt.plot(intervals, packets, colors[1], label=names[i+3])
    total_packets_download.append(packets.sum())

    # Ajouter des légendes et des étiquettes pour la courbe pour l'ajout
    plt.xlabel('Secondes')
    plt.ylabel('Packets par intervalle de 1 seconde')
    plt.title(f'{names[i-1]} vs {names[i+3]}')
    plt.legend()
    plt.grid(True)

# Afficher les graphiques
plt.tight_layout()
plt.savefig('packet_distribution_comparison_plot.png')
plt.show()

