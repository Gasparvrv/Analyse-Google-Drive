import pyshark
import pandas as pd
import whois
import socket
import pydig 
import dns.name
import dns.resolver
from ipwhois import IPWhois

# Chemin vers le fichier de capture pcapng
pcapng_file = "/Users/gaspar/Documents/Résauxfiles/Ouverture+ajout+telechargement+ermer.pcapng"

# Fonction pour extraire les informations sur les noms de domaine contenant "google"
def extract_dns_info(pcapng_file):
    dns_info = []
    resolved_domains = set()
    cap = pyshark.FileCapture(pcapng_file, only_summaries=False)
    for pkt in cap:
        if 'DNS' in pkt:
            domain = pkt['DNS'].get_field_value('dns.qry.name')
            
            if 'google' in domain.lower():  # Vérification si le nom de domaine contient "google"
                dns_type = pkt['DNS'].get_field_value('dns.qry.type')
                # Conversion du type DNS en texte lisible`
                if dns_type == '1':
                    dns_type = 'A'
                elif dns_type == '2':
                    dns_type = 'NS'
                elif dns_type == '5':
                    dns_type = 'CNAME'
                elif dns_type == '28':
                    dns_type = 'AAAA'
                elif dns_type == '65':
                    dns_type = 'HTTPS'
                dns_resp = pkt['DNS'].get_field_value('dns.resp.name')
                response = 'Response' if dns_resp else 'Query'
                authoritative_servers = get_authoritative_servers(domain)
                owner = get_domain_owner(domain)
            
                
                #answer = pkt['DNS'].get_field_value('dns.a')
                answer = pkt['DNS'].get_field_value('dns.a')
                time = pkt.sniff_time.strftime("%M:%S")
                
                
                
             
                company = get_company_from_ip(answer)
                
                if answer:
                    print(get_company_from_ip(answer))
                    
                dns_info.append({'Time':time, 'Domain': domain, 'Type': dns_type, 'Response': response,
                                 'Authoritative Servers': authoritative_servers, 'Owner': owner,'Answer_ip':answer,'Company': company})
    return dns_info

def get_company_from_ip(ip_address):
    try:
        obj = IPWhois(ip_address)
        res=obj.lookup_whois()
        if res:
            return res["nets"][0]['name']
    except Exception as e:
        return 'Unknown'
# Fonction pour obtenir les serveurs autoritatifs pour un nom de domaine
def get_authoritative_servers(domain):
    n = dns.name.from_text(domain)
    try:
        while True:
            try:
                # On envoie une requête de type NS :
                answer = dns.resolver.query(n, 'NS')
            except dns.resolver.NoAnswer:
                # On n'a pas trouvé d'enregistrement, on ignore l'exception et on continue
                print("Aucun enregistrement NS trouvé pour " + n.to_text() + ", tentative avec le parent.")
            else:
                # Aucune exception levée, on a trouvé un enregistrement NS
                #print("Enregistrement NS trouvé pour le domaine " + n.to_text())
                authoritative_servers = [rdata.to_text() for rdata in answer]
                return ', '.join(authoritative_servers) if authoritative_servers else 'Unknown'
            # Si on arrive ici, c'est qu'on n'a pas trouvé, on réessaie avec le parent :
            n = n.parent()
    except dns.name.NoParent:
        # Cette exception est levée si le domaine n'a plus de parent, on a atteint la racine du DNS
        return 'Unknown'
    

# Fonction pour obtenir le propriétaire du nom de domaine
def get_domain_owner(domain):
    return "Google LLC"
    
   

# Fonction pour créer un fichier Excel avec les informations sur les noms de domaine résolus
def create_dns_excel(dns_info):
    df = pd.DataFrame(dns_info)
    writer = pd.ExcelWriter('google_dns_info.xlsx', engine='openpyxl')
    df.to_excel(writer, index=False)
    writer.save()

# Exécution de l'analyse et création du fichier Excel
google_dns_info = extract_dns_info(pcapng_file)
create_dns_excel(google_dns_info)



#print(get_domain_owner("googl"))