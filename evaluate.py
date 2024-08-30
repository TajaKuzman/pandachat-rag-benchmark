import json
import pandas as pd
import numpy as np
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("submission_directory", help="path to the submission directory, e.g. systems/embedding-models-evaluation")
    parser.add_argument("top_k", help= "number of retrieved sources to consider as hits, e.g. '1' - evaluates only the first hit")
    args = parser.parse_args()

submission_directory = args.submission_directory
top_k_number = int(args.top_k)

# Calculate in how many queries the right source text was retrieved
def evaluate_retrieval(test_df, top_k_number):
	correct_context = []

	retrieved_sources = test_df["sources"].to_list()

	# Change type to list if it was opened as str
	if type(retrieved_sources[0]) == str:
		from ast import literal_eval
		retrieved_sources = [literal_eval(x) for x in retrieved_sources]

	correct_source_count = 0
	evaluated_sources = []

	# Take only so much first hits as decided by the top_k_number
	print(f"Evaluating top {top_k_number} retrieved source(s)")
	retrieved_sources = [x[:top_k_number] for x in retrieved_sources]

	for true_source, retr_sources in list(zip(test_df["document"].to_list(), retrieved_sources)):
		current_count = 0
		current_eval = {"correct_source": [], "incorrect_source": []}
		for source in retr_sources:
			if source == true_source:
				current_count = 1
				current_eval["correct_source"].append(source)
			else:
				current_eval["incorrect_source"].append(source)
		if current_count == 0:
			correct_context.append("no")
		else:
			correct_context.append("yes")
		evaluated_sources.append(current_eval)
		correct_source_count += current_count

	test_df[f"sources-eval-{top_k_number}"] = evaluated_sources
	test_df[f"sources-correct-context-{top_k_number}"] = correct_context

	correct_source_per = correct_source_count/len(retrieved_sources)*100

	print(f"Number of queries with correct retrieved sources: {correct_source_count} ({correct_source_per} %)")

	return [test_df, correct_source_count, correct_source_per]

# For each scenario, create a table with results
def results_table(result_df):
	# Get a list of eval scenarios
	scenarios = list(result_df["eval_scenario"].unique())

	for scenario in scenarios:
		dataset_df = result_df[result_df["eval_scenario"] == scenario]

		# Sort values based on highest count (percentage)
		dataset_df = dataset_df.sort_values(by="correct_retrieval_per", ascending=False)

		print("New benchmark scores:\n")

		print(dataset_df.to_markdown(index=False))

		print("\n------------------------------------------\n")

		# Save the table in markdown
		with open("results/results-{}.md".format(scenario), "w") as result_file:
			result_file.write(dataset_df.to_markdown(index=False))



def evaluate_pipeline(submission_path):
	# Open the submission to be evaluated
	with open("{}".format(submission_path), "r") as sub_file:
		results_dict = json.load(sub_file)

	test_df = pd.DataFrame(results_dict["df"])

	eval_scenario = results_dict["eval_scenario"]
	print("Eval scenario:\n")
	print(eval_scenario)

	print("\nEvaluated submission: {}".format(submission_path))

	# Evaluate the submission
	print("\nEvaluating retrieval ...")

	resulting_df, correct_count, correct_per = evaluate_retrieval(test_df, top_k_number)

	# Save the resulting_df
	results_dict["df"] = resulting_df.to_dict(orient="records")

	# Save as json
	with open("{}_results.json".format(submission_path), "w") as new_file:
		json.dump(results_dict, new_file, indent=2)

	print("Results saved to {}_results.json".format(submission_path))

	# Open the jsonl file with all results
	with open("results/results.json", "r") as result_file:
		results_list = json.load(result_file)

	# Append current results
	current_res_dict = {"eval_scenario": eval_scenario, "system": results_dict["system"], "evaluated-top-k":top_k_number, "time_per_question (s)": results_dict["time_per_question"], "correct_retrieval_count": correct_count, "correct_retrieval_per": correct_per}

	# Add the results to all results
	results_list.append(current_res_dict)

	with open("results/results.json", "w") as new_result_file:
		json.dump(results_list, new_result_file, indent = 2)

	print("The evaluation is completed. The results are added to the `results/results.json` file.")

	# Create a dataframe from all results
	result_df = pd.DataFrame(results_list)

	# Create a results table
	results_table(result_df)


# Identify all submission files in the directory
file_name_list = []

current = os.listdir(submission_directory)

for file in current:
	if "submission_" in file:
		if ".json" in file:
			if "results" not in file:
				file_name_list.append(f"{submission_directory}/{file}")

for submission_path in file_name_list:
	evaluate_pipeline(submission_path)