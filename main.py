import csv

from tqdm import tqdm


def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data



# Provide the path to your CSV file
csv_file_path = 'processNoDupClinicalTrials.csv'

rows=read_csv_file(csv_file_path)


import openai



# Set up the OpenAI API key and model ID
openai.api_key = "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"
model_id = "gpt-4-0314"

def ask_gpt(input_value):
    # Define the prompt to extract the product information
    prompt = f""" {input_value}"""
    try:
        response = openai.ChatCompletion.create(
            temperature=0,
            model=model_id,
            messages=[{"role": "system", "content": """you are an expert in the biomedical domain. I have as Input file a CSV file about clinical trials and 
i want to write the output in csv format.
keep the same order of the rows. also don't change the first column value copy the same from my input and analyse this input as it is.
If you are not respecting the order of the columns, the columns in the output should be in this order (NCTId, PD-L1).
you can get the NCTId from the fist column in the csv file i will send, for example in the fifth row the NCTId is NCT00317200, and so on.
To understand what is PD-L1, The PD-L1 in definition is: An immunohistochemical test result that indicates expression of PD-L1 in a tissue sample of a primary or metastatic malignant neoplasm.
in the input csv file have 3 columns that you should analyze them, they are descriptions about the clinical trials and they are in the order (BriefTitle, BriefSummary, DetailedDescription).
you have to read these 3 columns and conclude the PD-L1 of the clinical trial for each NCTId(clinical trial).so don't write these 3 columns in the output file.
when you find the PD-L1 of the clinical trial(after reading that 3 columns), then in the output write a row with the NCTId(from input file) as the first column and the PD-L1 of the clinical trial is the PD-L1  you found(as the second column).
Here are the possible values to search (PD-L1_Negative, PD-L1_Positive, Lack of Expression of PD-L1). So the output value should be one of these possible values.
Don't copy the whole sentence from the input and write it in the output.
Don't ignore any row in the input file, check them row by row and for each row you should check the NCTId and for each NCTId you have to read BriefTitle, BriefSummary and DetailedDescription.
If there is a NCTId that you can't find the PD-L1 of the clinical trial for it or can't detect the PD-L1 of the clinical trial, then write "NULL" in the output.please don't ignore any row, i want to see all the NCTId in the output.
Do not write any prefix or explanation for your response. Just the response in CSV format
Here is the input CSV\n"""},
                      {"role": "user", "content": prompt}
                      ]
    )
    except:
        return ask_gpt(input_value)

    rows=response


    # Parse the CSV output and extract the title and images URLs
    rows = response.choices[0].message.content

    return rows

def write_results(response):
    with open("PD-L1.csv", "a+", encoding="utf-8") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(response)

#result=[]
#result.append(["DrugID,Interaction,Action,Target,Examples"])
start_row = 0
chunk_size = 1
while start_row < len(rows):
    chunk = rows[start_row:start_row + chunk_size]
    for row in tqdm(chunk):
        response=ask_gpt(row[0]+","+row[1])

        write_results(response)
    start_row += chunk_size