# import os
# import re
# import json
# import math
# import glob
# from collections import Counter , defaultdict
# from typing import List, Dict, Tuple,Pattern
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# # file loading and encoding handling
# def load_text(filepath):

#     encodings_to_try =['utf-8','utf-8-sig','latin-1','ascii']
#     last_error=None
#     for enc in encodings_to_try:
#         try:
#             with open(filepath,"r",encoding=enc) as f:
#                 return f.read()
#         except Exception as e:
#             last_error=e
#             continue

#     raise last_error

# # text = load_text('./data/Alice_in_Wonderland.txt')
# # print(text)

# # ---------- Load multiple text files ----------
# def fetch_text_files(folder,pattern="*.txt"):
#     """  Load all text files in a given folder into a directory. """
#     files_list = glob.glob(os.path.join(folder,pattern))
#     print("Found files:", files_list)
#     contents ={}
#     for file in files_list:
#         try:
#             contents[os.path.basename(file)]=load_text(file)
#         except Exception as e:
#             print(f"Skipping {file} due to read error:{e}")
#     return contents

# fetch_text_files(r"./data")

# # for name, content in texts.items():
# #     print(f"{name}: {len(content)} characters")

# #---- BASIC ANALYSIS-------

# def get_char_count(text):
#     return len(text)

# def get_words(text):
#     """ Convert text to lowercase and split into words. """
#     words = re.findall(r"[A-Za-z0-9]+",text)
#     return [w.lower() for w in words if w.strip()]

# def get_sentences(text):
#     """ split text into sentences using simple regex rules. """
#     sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"\'“])',text.strip())
#     return [s.strip() for s in sentences if s.strip()] 

# def compute_text_summary(text):
#     """ Calculate key metrics for text. """
#     total_chars = get_char_count(text)
#     words = get_words(text)
#     sentences = get_sentences(text)
#     total_words = len(words)
#     total_sents=len(sentences)

#     avg_word_len = (sum(len(w) for w in words)/total_words) if total_words else 0
#     avg_sent_len = (total_words/total_sents) if total_sents else 0

#     return {
#         "Characters":total_chars,
#         "words":total_words,
#         "sentences":total_sents,
#         "avg_word_length":avg_word_len,
#         "avg_sentences_length":avg_sent_len
#     }   

# def make_stats_table(files_data):
#     """  create dataframe with summary stats for each document. """
#     rows=[]
#     for i, (filename,content) in enumerate(files_data.items(),stats=1):
#         stats=compute_text_summary(content)
#         rows.append({
#             "id":i,
#             "filename":filename,
#             "word_count":stats["words"],
#             "char_count":stats["characters"],
#             "sentence_count":stats["sentences"],
#             "avg_word_len":stats["avg_word_length"],
#             "avg_sent_len":stats["avg_sentence_length"]
#         })
#     return pd.DataFrame(rows)

# #---------------------  REGEX EXTRACTiON       ----------------------
# PAT_EMAIL = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
# PAT_PHONE = re.compile(r'(\+?\d{1,3}[\s-]?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}')
# PAT_TAG = re.compile(r'(#\w+)')
# PAT_MENTION = re.compile(r'(@\w+)')
# PAT_URL = re.compile(r'(https?://[^\s]+|www\.[^\s]+)')
# PAT_DATE = re.compile(
#     r'(\b\d{1,2}/\d{1,2}/\d{4}\b|\b\d{1,2}-\d{1,2}-\d{4}\b|'
#     r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},\s*\d{4}\b)',
#     re.IGNORECASE
# )
# PAT_CURRENCY = re.compile(r'(\£|\$|€)\s?\d+(?:,\d{3})*(?:\.\d+)?')

# def extract_text_patterns(text):
#     """Find emails, URLs, hashtags, mentions, etc. in text."""
#     emails = PAT_EMAIL.findall(text)
#     phones = PAT_PHONE.findall(text)
#     hashtags = PAT_TAG.findall(text)
#     mentions = PAT_MENTION.findall(text)
#     urls = PAT_URL.findall(text)
#     dates = PAT_DATE.findall(text)
#     currencies = PAT_CURRENCY.findall(text)

#     raw_phones = re.findall(r'(\+?\d{1,3}[-\s]?)?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4}', text)

#     def clean_phone(num):
#         digits = re.sub(r'\D+', '', num)
#         if len(digits) == 10:
#             return f"+1-{digits[:3]}-{digits[3:6]}-{digits[6:]}"
#         elif len(digits) > 10:
#             cc = digits[:-10]
#             res = digits[-10:]
#             return f"+{cc}-{res[:3]}-{res[3:6]}-{res[6:]}"
#         else:
#             return digits


#     norm_phones = [clean_phone(p) for p in raw_phones]

#     # EXTRACT domains
#     def get_domain(url):
#         if not url.statswith("http"):
#             url="http://"+url
#             m= re.match(r'https?://(?:www\.)?([^/]+)',url)
#             return m.group(1).lower() if m else url.

#         domains = [get_domain(u) for u in urls]

#         return {
#             "email":sorted(set(email)),
#             "phones":sorted(set(norm_phones)),
#             "hashtags":hashtags,
#             "mentions":mentions,
#             "urls":urls,
#             "domains":domains,
#             "dates":dates,
#             "currencies":currencies
#         }

# # -------------- STATS AND VISUALS -----------------
# def word_stats(words):
#     return Counter(words)


# def word_lengths_plot(words):
#     lengths = [len(w) for w in words]
#     plt.figure(figsize=(8,5))
#     plt.hist(lengths,bins=20,desity=True)
#     plt.title("Word Length Distribution")
#     plt.xlabel("Length")
#     plt.ylabel("Density")
#     plt.show()

# def char_frequency(text):
#     chars = [c for c in text if not c.isspace()]
#     return Counter(chars)


# def top_words_bar(word_counter,n=20):
#     top_items = word_counter.most_common(n)
#     words,freqs = zip(*top_items)
#     plt.figure(figsize=(10,6))
#     plt.barh(words,freqs)
#     plt.title("Tops Words")
#     plt.tight_layout()
#     plt.show()


# # ------------ MAIN RUNNER -------------------------

# def run_text_analysis(input_folder,output_folder="results"):
#     os.makedirs(output_folder,exist_ok=True)
#     files = fetch_text_files(input_folder)
#     if not files:
#         raise FileNotFoundError("No Text files found.")


#    df = make_stats_table(files)
#    df.to_csv(os.path.join(output_folder,"summary.csv"),index=False)


#    combined_text = "\n".join(files.values())
#    words = get_words(words)
#    word_counts = word_stats(words)
#    patterns = extract_text_patterns(combined_text)

#    with.open(os.path.join(output_folder,"pattern.json"),"w",encoding="utf-8") as f:
#         json.dump(patterns,f,index=2)

#    word_lengths_plot(words)
#    top_words_bar(word_counts)   


#    print(f"Analysis complete! Results saved in '{output_folder}'.")  



# # ---------- MAIN EXECUTION -----------------

# if __main__="__main__":
#     folder="data"
#     out="results"
#     run_text_analysis(folder,output_folder=out)

import os
import re
import json
import math
import glob
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Pattern
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ---------- File Loading ----------
def load_text(filepath):
    """Load text file with multiple encoding fallbacks."""
    encodings_to_try = ['utf-8', 'utf-8-sig', 'latin-1', 'ascii']
    last_error = None
    for enc in encodings_to_try:
        try:
            with open(filepath, "r", encoding=enc) as f:
                return f.read()
        except Exception as e:
            last_error = e
            continue
    raise last_error


def fetch_text_files(folder, pattern="*.txt"):
    """Load all text files in a given folder into a dictionary."""
    files_list = glob.glob(os.path.join(folder, pattern))
    print("Found files:", files_list)
    contents = {}
    for file in files_list:
        try:
            contents[os.path.basename(file)] = load_text(file)
        except Exception as e:
            print(f"Skipping {file} due to read error: {e}")
    return contents


# ---------- Basic Analysis ----------
def get_char_count(text):
    return len(text)


def get_words(text):
    """Convert text to lowercase and split into words."""
    words = re.findall(r"[A-Za-z0-9]+", text)
    return [w.lower() for w in words if w.strip()]


def get_sentences(text):
    """Split text into sentences using regex."""
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"\'“])', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def compute_text_summary(text):
    """Calculate key metrics for text."""
    total_chars = get_char_count(text)
    words = get_words(text)
    sentences = get_sentences(text)
    total_words = len(words)
    total_sents = len(sentences)

    avg_word_len = (sum(len(w) for w in words) / total_words) if total_words else 0
    avg_sent_len = (total_words / total_sents) if total_sents else 0

    return {
        "characters": total_chars,
        "words": total_words,
        "sentences": total_sents,
        "avg_word_length": avg_word_len,
        "avg_sentence_length": avg_sent_len
    }


def make_stats_table(files_data):
    """Create DataFrame with summary stats for each document."""
    rows = []
    for i, (filename, content) in enumerate(files_data.items(), start=1):
        stats = compute_text_summary(content)
        rows.append({
            "id": i,
            "filename": filename,
            "word_count": stats["words"],
            "char_count": stats["characters"],
            "sentence_count": stats["sentences"],
            "avg_word_len": stats["avg_word_length"],
            "avg_sent_len": stats["avg_sentence_length"]
        })
    return pd.DataFrame(rows)


# ---------- Regex Extraction ----------
PAT_EMAIL = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
PAT_PHONE = re.compile(r'(\+?\d{1,3}[\s-]?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}')
PAT_TAG = re.compile(r'(#\w+)')
PAT_MENTION = re.compile(r'(@\w+)')
PAT_URL = re.compile(r'(https?://[^\s]+|www\.[^\s]+)')
PAT_DATE = re.compile(
    r'(\b\d{1,2}/\d{1,2}/\d{4}\b|\b\d{1,2}-\d{1,2}-\d{4}\b|'
    r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},\s*\d{4}\b)',
    re.IGNORECASE
)
PAT_CURRENCY = re.compile(r'(\£|\$|€)\s?\d+(?:,\d{3})*(?:\.\d+)?')


def extract_text_patterns(text):
    """Find emails, URLs, hashtags, mentions, etc. in text."""
    emails = PAT_EMAIL.findall(text)
    phones = PAT_PHONE.findall(text)
    hashtags = PAT_TAG.findall(text)
    mentions = PAT_MENTION.findall(text)
    urls = PAT_URL.findall(text)
    dates = PAT_DATE.findall(text)
    currencies = PAT_CURRENCY.findall(text)

    raw_phones = re.findall(r'(\+?\d{1,3}[-\s]?)?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4}', text)

    def clean_phone(num):
        digits = re.sub(r'\D+', '', num)
        if len(digits) == 10:
            return f"+1-{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif len(digits) > 10:
            cc = digits[:-10]
            res = digits[-10:]
            return f"+{cc}-{res[:3]}-{res[3:6]}-{res[6:]}"
        else:
            return digits

    norm_phones = [clean_phone(p) for p in raw_phones]

    def get_domain(url):
        if not url.startswith("http"):
            url = "http://" + url
        m = re.match(r'https?://(?:www\.)?([^/]+)', url)
        return m.group(1).lower() if m else url

    domains = [get_domain(u) for u in urls]

    return {
        "emails": sorted(set(emails)),
        "phones": sorted(set(norm_phones)),
        "hashtags": hashtags,
        "mentions": mentions,
        "urls": urls,
        "domains": domains,
        "dates": dates,
        "currencies": currencies
    }


# ---------- Stats and Visuals ----------
def word_stats(words):
    return Counter(words)


def word_lengths_plot(words):
    lengths = [len(w) for w in words]
    plt.figure(figsize=(8, 5))
    plt.hist(lengths, bins=20, density=True)
    plt.title("Word Length Distribution")
    plt.xlabel("Length")
    plt.ylabel("Density")
    plt.show()


def char_frequency(text):
    chars = [c for c in text if not c.isspace()]
    return Counter(chars)


def top_words_bar(word_counter, n=20):
    top_items = word_counter.most_common(n)
    words, freqs = zip(*top_items)
    plt.figure(figsize=(10, 6))
    plt.barh(words, freqs)
    plt.title("Top Words")
    plt.tight_layout()
    plt.show()


# ---------- Main Runner ----------
def run_text_analysis(input_folder, output_folder="results"):
    os.makedirs(output_folder, exist_ok=True)
    files = fetch_text_files(input_folder)
    if not files:
        raise FileNotFoundError("No text files found.")

    df = make_stats_table(files)
    df.to_csv(os.path.join(output_folder, "summary.csv"), index=False)

    combined_text = "\n".join(files.values())
    words = get_words(combined_text)
    word_counts = word_stats(words)
    patterns = extract_text_patterns(combined_text)

    with open(os.path.join(output_folder, "patterns.json"), "w", encoding="utf-8") as f:
        json.dump(patterns, f, indent=2)

    word_lengths_plot(words)
    top_words_bar(word_counts)

    print(f"✅ Analysis complete! Results saved in '{output_folder}'.")


# ---------- Main Execution ----------
if __name__ == "__main__":
    folder = "data"
    out = "results"
    run_text_analysis(folder, output_folder=out)
