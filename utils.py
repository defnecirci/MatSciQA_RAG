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
                        m=j.strip().split(':')[-1]
                        # m = j.strip()
                        exist = True
    return m.split('}')[0].split('[')[-1].split(']')[0] if exist else 'Could not find pattern'

def reader_try(filename: str):
     with open(filename, 'r', encoding="utf8") as file:
          lines = file.readlines()
          file.close()
          if 'answer' in lines[-1]:
               print(lines[-1])

for idx, val in enumerate(df_aq['Question Info']):
    filename_ = val.lower().split('-')
    filename_  = ['gate' if x == 'g' else x for x in filename_]

    exam, subject, year = filename_[0], filename_[1], filename_[2]
    question, question_type = filename_[3], df_aq['Question Type'][idx].lower()

    if question_type == 'mcqs-num':
          question_type = 'mcqs'
    
    filename_format_1 = f"{exam}_{subject}_{year}/{model}_{question}_{question_type}.txt"

    
    print(path.exists(filedir+filename_format_1), filedir+filename_format_1)
    if path.exists(filedir+filename_format_1):
        # print(filename_format_1)
        # print(reader(filedir+filename_format_1))
        # print(f"llama 3 answer = {reader(filedir+filename_format_1)} correct answer = {df_aq['Correct Answer'][idx]}")
        llama3_all_questions.loc[idx] = [df_aq['Question Info'][idx], df_aq['Question Type'][idx],
                                         df_aq['Correct Answer'][idx], df_aq['GPT3.5'][idx],
                                         df_aq['GPT3.5-COT'][idx], df_aq['GPT4'][idx],
                                         df_aq['GPT4-COT'][idx], reader(filedir+filename_format_1), df_aq['TOPIC'][idx]]

    else:
        # print(filename_)
        question = filename_[4]
        filename_format_2 = f"{exam}_{subject}_{year}/{model}_{question}_{question_type}.txt"
        print(path.exists(filedir+filename_format_2), filedir+filename_format_2)
        if path.exists(filedir+filename_format_2):
            # print(filename_format_2)
            # print(reader(filedir+filename_format_2))
            # print(f"llama 3 answer = {reader(filedir+filename_format_2)} correct answer = {df_aq['Correct Answer'][idx]}")
            llama3_all_questions.loc[idx] = [df_aq['Question Info'][idx], df_aq['Question Type'][idx],
                                            df_aq['Correct Answer'][idx], df_aq['GPT3.5'][idx],
                                            df_aq['GPT3.5-COT'][idx], df_aq['GPT4'][idx],
                                            df_aq['GPT4-COT'][idx], reader(filedir+filename_format_2), df_aq['TOPIC'][idx]]
llama3_all_questions.to_excel("all_questions_llama3_new.xlsx")