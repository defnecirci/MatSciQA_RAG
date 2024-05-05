import pandas as pd
import re  

# Load the Excel file into a DataFrame
df = pd.read_excel("all_questions_llama3_with_corresponding_values.xlsx")
# Print the DataFrame with the new column
#print(df['Corresponding Value'])

def extract_corresponding_value(question, correct_answer):
    # Find the option corresponding to the correct answer letter
    match = re.search(r'\({}\)\s*(.*?)(?:\s*\(|$)'.format(correct_answer), question)
    if match:
        extracted_value = match.group(1).strip()
        if correct_answer == 'D':
            extracted_value = extracted_value[:-2]  # Exclude the last two characters
        return extracted_value
    return None

# Apply the function to create a new column
#df['Corresponding Value'] = df.apply(lambda row: extract_corresponding_value(row['QUESTION'], row['Correct Answer']), axis=1)
#df.to_excel("all_questions_llama3_updated.xlsx", index=False)

# Function to check if a prediction is correct for a given row
def is_correct_prediction(row):
    ground_truth = str(row['Correct Answer'])
    # Change the below line with the model name that you are interested in evaluating
    predicted = row['LLAMA3-8B']
    question_type = row['Question Type']
    
    # Select NUM category
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

    # For MATCH category
    else:
        # First, check if the predicted answer matches the ground truth
        if str(predicted) == ground_truth:
            return True
        # If not, check if the ground truth matches the corresponding answer
        corresponding_answer = row['Corresponding Value']
        if corresponding_answer and predicted == corresponding_answer:
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
#print(incorrect_predictions[['Row', 'Question Info', 'Correct Answer', 'LLAMA3-8B', 'Question Type']].to_string(index=False))
#print(incorrect_predictions[['Row', 'Question Info', 'Correct Answer',  'Question Type','Corresponding Value']].to_string(index=False))


def calculate_accuracy(df):
    results_by_category = df.apply(is_correct_prediction, axis=1).groupby([df['Question Type'], df['TOPIC']]).agg(['sum', 'count'])

    accuracies = {}
    total_correct_predictions = 0
    total_questions = 0

    print("\nResults by category (Correct Predictions / Total Questions):")
    for category, result in results_by_category.iterrows():
        correct_predictions = result['sum']
        total = result['count']
        accuracy = correct_predictions / total
        accuracies[category] = accuracy
        total_correct_predictions += correct_predictions
        total_questions += total
        print(f"{category}: {correct_predictions} / {total} (Accuracy: {accuracy:.2%})")

    # Calculate accuracy for specific question types (NUM, MATCH, etc.)
    for question_type in df['Question Type'].unique():
        if question_type not in accuracies:
            accuracies[question_type] = 0
        questions_subset = df[df['Question Type'] == question_type]
        correct_predictions_subset = questions_subset.apply(is_correct_prediction, axis=1).sum()
        total_questions_subset = len(questions_subset)
        accuracy_subset = correct_predictions_subset / total_questions_subset
        print(f"{question_type} Accuracy: {correct_predictions_subset} / {total_questions_subset} (Accuracy: {accuracy_subset:.2%})")

    overall_accuracy = total_correct_predictions / total_questions
    print(f"\nOverall Accuracy: {total_correct_predictions} / {total_questions} (Accuracy: {overall_accuracy:.2%})")

    return accuracies, overall_accuracy

category_accuracies, overall_accuracy = calculate_accuracy(df)



