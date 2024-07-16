import requests
import csv

headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

def Biofalcon_call(text):
    url = 'https://labs.tib.eu/sdm/biofalcon/api?mode=short'
    entities_wiki = []
    payload = '{"text":"' + text + '"}'
    r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
    if r.status_code == 200:
        response = r.json()
        entities = response.get('entities', [])
        if isinstance(entities, list) and len(entities) > 1:
            entities_wiki = entities[1]
    else:
        r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
        if r.status_code == 200:
            response = r.json()
            entities = response.get('entities', [])
            if isinstance(entities, list) and len(entities) > 1:
                entities_wiki = entities[1]

    if entities_wiki:
        return entities_wiki[0]
    else:
        return []

csv_file_path = 'CR-DrugsChemotherapy.csv'
columns = ['drugName1', 'drugName2', 'drugName3']

rows = []
with open(csv_file_path, 'r', encoding='utf-8', errors='ignore') as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames

    new_fieldnames = []
    for column in fieldnames:
        new_fieldnames.append(column)
        if column in columns:
            new_fieldnames.append(f'{column} CUI')

    for row in reader:
        texts = [row[column] for column in columns]

        results = []
        for text in texts:
            if text == "":
                results.append("")
            else:
                nouns = [noun.strip() for noun in text.split(',')]
                noun_results = []
                for noun in nouns:
                    noun_result = Biofalcon_call(noun)
                    noun_results.append(noun_result)
                results.append(noun_results)

        new_row = {}
        for column, value in row.items():
            new_row[column] = value
            if column in columns:
                index = columns.index(column)
                new_row[f'{column} CUI'] = results[index]

        rows.append(new_row)


output_file_path = 'output.csv'  

with open(output_file_path, 'w',encoding='utf-8', newline="") as file:
    writer = csv.DictWriter(file, fieldnames=new_fieldnames)
    writer.writeheader()
    writer.writerows(rows)


print("the file is already updated")
