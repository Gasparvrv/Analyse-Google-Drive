import pyshark
from collections import Counter
import matplotlib.pyplot as plt
import sys

# Chemin vers le fichier de capture pcapng
pcapng_file = "/Users/gaspar/Documents/Résauxfiles/Ouverture+ajout+telechargement+ermer.pcapng"

# Fonction pour extraire les noms de domaine résolus pour les paquets liés à Google Drive
def extract_google_drive_domains(pcapng_file):
    domains = []
    cap = pyshark.FileCapture(pcapng_file, only_summaries=False)
    for pkt in cap:
        if 'DNS' in pkt:
            domain = pkt['DNS'].get_field_value('dns.qry.name')
            # Vérifier si le domaine appartient à Google Drive
            if domain and 'google' in domain:
                src_port = pkt['UDP'].get_field_value('udp.srcport')
                dst_port = pkt['UDP'].get_field_value('udp.dstport')
                domains.append(domain)
    return domains

# Fonction pour créer un diagramme rond avec le nombre de chaque domaine
def create_pie_chart(domains_count):
    domain_names = list(domains_count.keys())
    domain_counts = list(domains_count.values())

    plt.figure(figsize=(8, 8))
    plt.pie(domain_counts, labels=domain_names, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Noms de domaines résolus pour Google Drive', pad=10)  # Ajout de l'espacement supplémentaire pour le titre
    #plt.tight_layout()  # Ajustement automatique de la disposition pour éviter les superpositions
    plt.savefig('google_drive_domains_pie_chart.png')  # Enregistrement du diagramme dans un fichier

def affichage(domains_count):
   # Affichage d'un tableau avec le nom de domaine et le nombre d'occurrences
    print("\nTableau des noms de domaine et nombre d'occurrences :")
    print("----------------------------------------------------")
    print("Nom de domaine\t\tNombre d'occurrences")
    print("----------------------------------------------------")
    for domain, count in domains_count.items():
        print(f"{domain}\t\t{count}")
        
# Exécution de l'analyse et création du diagramme
google_drive_domains = extract_google_drive_domains(pcapng_file)
domains_count = Counter(google_drive_domains)
create_pie_chart(domains_count)
affichage(domains_count)

