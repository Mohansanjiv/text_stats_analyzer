
# Assignments-1:-Text Statistics Analyzer
 
 ## Overview

 A Python tool for analyzing plain-text documents (.txt files).
It extracts statistics, detects patterns (emails, URLs, phone numbers, hashtags, etc.), and visualizes word distributions.

## Features
 - Batch file loading:- reads all .txt files in a folder.
 - Text metrics:- character, word, and sentence counts.
 - Pattern extraction:-finds emails, phone numbers, hashtags, mentions, URLs, dates, and currency values.
- Visualization:- plots word length distribution and top-used words.
- Exports :- saves results as: 
     - summary.csv → statistical summary per file
     - patterns.json → extracted entities
## Usage
 1. Folder setup
 
```python

│
├── data/
│   ├── file1.txt
│   ├── file2.txt
│
└── text_stats_analyzer.py
```

## Run the analyzer

 ```
 python text_stats_analyzer.py

```
- Results will be saved in a new results/ folder.

## Key Functions

| No|  Function  | Description |
|:-----|:--------:|------:|
| 1   | load_text(filepath) | Loads a text file with encoding fallback. |
| 2   |  fetch_text_files(folder, pattern)  |  Loads all text files from a folder into a dictionary. |
| 3   | get_words(text) | Splits text into lowercase words. |
| 4|get_sentences(text)|Divides text into sentences.|
|5|compute_text_summary(text)| Returns total counts and averages for words and sentences. |
|6|make_stats_table(files_data)|Builds a Pandas DataFrame of summaries for each file.|
|7|extract_text_patterns(text)|Extracts emails, phones, URLs, hashtags, mentions, dates, and currencies.|
|8|word_lengths_plot(words)|Displays histogram of word lengths.|
|9|top_words_bar(word_counter, n=20)|Shows the top n most common words.|
|10|run_text_analysis(input_folder, output_folder)|Main function — runs full analysis and exports results.|


## Output Files

| Files  | Description |
|:--------:|    ------:  |
|results/summary.csv|Summary table for all analyzed files|
|results/patterns.json|Extracted entities and patterns|

## Requirements
### Python 3.8+ and the following packages:
```
pip install numpy pandas matplotlib
```

