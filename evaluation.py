import pandas as pd
import re  

# Load the Excel file into a DataFrame
df = pd.read_excel("all_questions_llama3.xlsx")

# Function to check if a prediction is correct for a given row
def is_correct_prediction(row):
    ground_truth = str(row['Correct Answer'])
    #change the below line with the model name that you are interested in evaluating
    predicted = row['GPT3.5']
    question_type = row['Question Type']
     # select NUM category
    if question_type == 'NUM':
        if 'to' in ground_truth or ':' in ground_truth:
            try:
                range_numbers = re.findall(r'\d+\.\d+|\d+', ground_truth)
                range_start, range_end = map(float, [range_numbers[0], range_numbers[-1]])
                if range_start <= float(predicted) <= range_end:
                    return True
            except (ValueError, IndexError):
                pass
        elif str(predicted) == ground_truth:
            return True

    # For other question types, check for exact match
    return str(predicted) == ground_truth


results_by_category = df.apply(is_correct_prediction, axis=1).groupby([df['Question Type'], df['TOPIC']]).agg(['sum', 'count'])

print("\nResults by category (Correct Predictions / Total Questions):")
for category, result in results_by_category.iterrows():
    correct_predictions = result['sum']
    total_questions = result['count']
    print(f"{category}: {correct_predictions} / {total_questions}")

# Print the rows where the prediction did not match the correct answer

pd.options.display.max_rows = None
pd.options.display.max_columns = None

print("\nRows with incorrect predictions:")
incorrect_predictions = df[~df.apply(is_correct_prediction, axis=1)]

# Reset the index and add a new column 'Row' with row numbers
incorrect_predictions = incorrect_predictions.reset_index(drop=True)
incorrect_predictions.index += 1  # Start row numbering from 1
incorrect_predictions.insert(0, 'Row', incorrect_predictions.index)

# Print the DataFrame
print(incorrect_predictions[['Row', 'Question Info', 'Correct Answer', 'GPT3.5', 'Question Type']].to_string(index=False))