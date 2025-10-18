import os
import re
import json
import math
import glob
from collections import Counter , defaultdict
from typing import List, Dict, Tuple,Pattern
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# file loading and encoding handling
def load_text(filepath):

    encodings_to_try =['utf-8','utf-8-sig','latin-1','ascii']
    last_error=None
    for enc in encodings_to_try:
        try:
            with open(filepath,"r",encoding=enc) as f:
                return f.read()
        except Exception as e:
            last_error=e
            continue

    raise last_error

# text = load_text('./data/Alice_in_Wonderland.txt')
# print(text)

# ---------- Load multiple text files ----------
def fetch_text_files(folder,pattern="*.txt"):
    """  Load all text files in a given folder into a directory. """
    files_list = glob.glob(os.path.join(folder,pattern))
    print("Found files:", files_list)
    contents ={}
    for file in files_list:
        try:
            contents[os.path.basename(file)]=load_text(file)
        except Exception as e:
            print(f"Skipping {file} due to read error:{e}")
    return contents

fetch_text_files(r"./data")

# for name, content in texts.items():
#     print(f"{name}: {len(content)} characters")

#---- BASIC ANALYSIS-------

def get_char_count(text):
    return len(text)

def get_words(text):
    """ Convert text to lowercase and split into words. """
    words = re.findall(r"[A-Za-z0-9]+",text)
    return [w.lower() for w in words if w.strip()]

def get_sentences(text):
    """ split text into sentences using simple regex rules. """
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"\'“])',text.strip())
    return [s.strip() for s in sentences if s.strip()] 

def compute_text_summary(text):
    """ Calculate key metrics for text. """
    total_chars = get_char_count(text)
    words = get_words(text)
    sentences = get_sentences(text)
    total_words = len(words)
    total_sents=len(sentences)

    avg_word_len = (sum(len(w) for w in words)/total_words) if total_words else 0
    avg_sent_len = (total_words/total_sents) if total_sents else 0

    return {
        "Characters":total_chars,
        "words":total_words,
        "sentences":total_sents,
        "avg_word_length":avg_word_len,
        "avg_sentences_length":avg_sent_len
    }   




    

# -------- Analyze All Files from ./data --------
def analyze_folder(folder="./data"):
    texts = fetch_text_files(folder)
    summaries = []

    for name, content in texts.items():
        summary = compute_text_summary(content)
        summary["Filename"] = name
        # Rename keys to match desired output
        summary["Words"] = summary.pop("words")
        summary["Sentences"] = summary.pop("sentences")
        summary["Average Word Length"] = summary.pop("avg_word_length")
        summary["Average Sentence Length"] = summary.pop("avg_sentences_length")
        summaries.append(summary)

    if not summaries:
        print("No text files found or no valid content.")
        return pd.DataFrame()  # empty DataFrame

    df = pd.DataFrame(summaries)
    df = df[["Filename", "Characters", "Words", "Sentences", "Average Word Length", "Average Sentence Length"]]
    return df




# ---------- Run & Save Results ----------
if __name__ == "__main__":
    # Automatically detect absolute path to the 'data' folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(script_dir, "data")

    print(f"🔍 Looking for text files in: {data_folder}\n")

    results = analyze_folder(data_folder)

    if results.empty:
        print("⚠️ No text files found or no valid content.\n")
        print("➡️ Please make sure your .txt files are inside the 'data' folder:")
        print(f"   {data_folder}\n")
    else:
        print("\n📊 TEXT ANALYSIS SUMMARY\n")
        print(results.to_string(index=False))

        # Optional: save results to CSV file
        output_path = os.path.join(script_dir, "text_analysis_summary.csv")
        results.to_csv(output_path, index=False)
        print(f"\n✅ Results saved to: {output_path}")