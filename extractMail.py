import json
import re
import codecs

def cleanEmail(email):
    # Supprimer les caractères supplémentaires après le .com ou le .fr dans l'adresse e-mail
    match = re.search(r'(\.(?:com|fr))\S+', email)
    if match:
        return email.replace(match.group(), match.group(1))
    else:
        return email

def extractEmailsAndInfo(json_file):
    with codecs.open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    emails = []
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+(?:\.com|\.fr)\S*\b'
    info_list = []

    for entry in data:
        snippet = entry.get('snippet', '')
        title = entry.get('title', '')

        # Recherche d'adresses e-mail dans le snippet et le titre
        snippet_emails = re.findall(email_regex, snippet)
        title_emails = re.findall(email_regex, title)

        # Ajout des adresses e-mail à la liste
        emails.extend(snippet_emails)
        emails.extend(title_emails)

        # Extraction du nom, prénom et entreprise
        name_match = re.search(r'([\wÀ-ÿ]+) ([\wÀ-ÿ]+)', title)
        if name_match:
            name = name_match.group(1)
            surname = name_match.group(2)
        else:
            name = ''
            surname = ''

        company_match = re.search(r' - (.+)$', title)
        if company_match:
            company = company_match.group(1)
        else:
            company = ''

        # Recherche de numéros de téléphone français dans le snippet
        phone_regex = r'(?<!\d)(?:\+33|0)\s*[1-9](?:[\s.-]*\d{2}){4}(?!\d)'
        phone_numbers = re.findall(phone_regex, snippet)
        if phone_numbers:
            phone_number = phone_numbers[0]
        else:
            phone_number = 'Pas de numéro trouvé'

        info = {
            'name': name,
            'surname': surname,
            'company': company,
            'email': [cleanEmail(email) for email in (snippet_emails + title_emails)],
            'phone_number': phone_number
        }
        info_list.append(info)

    # Suppression des doublons d'e-mails
    unique_emails = list(set(emails))

    return unique_emails, info_list

json_file = 'resultatRechercheLinkedin/linkedin.json'
emails, info = extractEmailsAndInfo(json_file)

# Enregistrement des adresses e-mail et des informations dans un nouveau fichier JSON
output_file = 'resultatRechercheLinkedin/extractResultLinkedin.json'
result = {
    'info': info
}
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(result, file, indent=4, ensure_ascii=False)

print('Emails, names, surnames, companies, and emails have been extracted and saved to extractResultLinkedin.json')
