import matplotlib.pyplot as plt
import pandas as pd
import os

# Liste des noms de fichiers CSV pour l'ajout
addition_file_names = ['Ajout vidéo.csv', 'Ajout raw.csv', 'Ajout pdf.csv', 'Ajout mp3.csv']
names= ['Vidéo', 'Raw', 'Pdf', 'Mp3']
# Liste des noms de fichiers CSV pour le téléchargement
download_file_names = ['Téléch vidéo.csv', 'Tel raw.csv', 'Tel pdf.csv', 'Tel mp3.csv']

# Couleurs pour chaque fonction
colors = ['tab:blue', 'tab:red']

# Initialiser une liste pour stocker le nombre total de paquets pour chaque fonction
total_packets_addition = []
total_packets_download = []

# Créer une nouvelle figure
plt.figure(figsize=(10, 6))

# Tracer les diagrammes à barres pour le nombre total de paquets pour l'ajout et le téléchargement
for i, (addition_file, download_file) in enumerate(zip(addition_file_names, download_file_names), start=1):
    # Charger les données CSV pour l'ajout
    data_addition = pd.read_csv(addition_file, delimiter=',')
    total_packets_addition.append(data_addition['All Packets'].sum())
    
    # Charger les données CSV pour le téléchargement
    data_download = pd.read_csv(download_file, delimiter=',')
    total_packets_download.append(data_download['All Packets'].sum())
    
    
    # Tracer les barres pour l'ajout et le téléchargement
    if i == 1:
        plt.bar([i - 0.2, i + 0.2], [total_packets_addition[-1], total_packets_download[-1]], color=colors, width=0.4, label=['Ajout', 'Téléchargement'])
    else:
        plt.bar([i - 0.2, i + 0.2], [total_packets_addition[-1], total_packets_download[-1]], color=colors, width=0.4)
        
# Ajouter des étiquettes et une légende
plt.xlabel('Fonctions')
plt.ylabel('Paquets totaux')
plt.title('Comparaison du nombre total de paquets')
plt.xticks(range(1, len(names) + 1), names, rotation=45)
plt.legend()

# Afficher le graphique
plt.tight_layout()
plt.savefig('total_packets_comparison_bar_chart.png')
plt.show()
