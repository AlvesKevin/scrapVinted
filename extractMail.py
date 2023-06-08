import json
import re

def extractEmails(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    emails = []
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    for entry in data:
        snippet = entry.get('snippet', '')
        title = entry.get('title', '')

        # Recherche d'adresses e-mail dans le snippet et le titre
        snippet_emails = re.findall(email_regex, snippet)
        title_emails = re.findall(email_regex, title)

        # Ajout des adresses e-mail à la liste
        emails.extend(snippet_emails)
        emails.extend(title_emails)

    # Suppression des doublons
    unique_emails = list(set(emails))

    return unique_emails

json_file = 'resultatRecherche/laposteResult.json'
emails = extractEmails(json_file)

# Enregistrement des adresses e-mail dans un nouveau fichier JSON
output_file = 'resultatMail/laposteEmails.json'
with open(output_file, 'w') as file:
    json.dump(emails, file, indent=4)

print('Emails have been extracted and saved to emails.json')