import pandas as pd
from os import path

filedir = "raw_qa/"
model = "llama3_8b"
df_aq = pd.read_excel("scoresheets/all_questions.xlsx")

columns_list = df_aq.columns[:-1].to_list()
columns_list.append('LLAMA3-8B')
columns_list.append('TOPIC')

llama3_all_questions = pd.DataFrame(columns=columns_list)

def reader(filename: str):
    with open(filename, 'r', encoding="utf8") as file:
        lines = file.readlines()
        file.close()
        exist = False
        for j in lines:
                # Pattern to find
                if "{'answer':" in j:
                        m=j.split(':')[1]
                        exist = True
    return m.split('}')[0] if exist else 'Could not find pattern'

for idx, val in enumerate(df_aq['Question Info']):
    filename_ = val.lower().split('-')
    filename_  = ['gate' if x == 'g' else x for x in filename_]

    exam, subject, year = filename_[0], filename_[1], filename_[2]
    question, question_type = filename_[3], df_aq['Question Type'][idx].lower()
    
    if question_type == 'mcqs-num':
          question_type = 'mcqs'
    
    filename = f"{exam}_{subject}_{year}/{model}_{question}_{question_type}.txt"
    
    if path.exists(filedir+filename):
        print(filename)
        print(f"llama 3 answer = {reader(filedir+filename)} correct answer = {df_aq['Correct Answer'][idx]}")
        llama3_all_questions.loc[idx] = [df_aq['Question Info'][idx], df_aq['Question Type'][idx],
                                         df_aq['Correct Answer'][idx], df_aq['GPT3.5'][idx],
                                         df_aq['GPT3.5-COT'][idx], df_aq['GPT4'][idx],
                                         df_aq['GPT4-COT'][idx], reader(filedir+filename), df_aq['TOPIC'][idx]]

llama3_all_questions.to_excel("all_questions_llama3.xlsx")