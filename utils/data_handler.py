import csv
import os
import json
from collections import defaultdict
from datetime import datetime
from pprint import pprint
from config.config import JSON_PATH_DIR, CSV_FILE_PATH

def build_vocabulary_dict(csv_file_path) -> dict:
    vocabulary_dict = {}

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # comma is the default delimiter

        for row in reader:
            vocab = row['Vocabulary'].strip()
            if not vocab:  # skip empty vocabulary entries
                continue

            vocabulary_dict[vocab] = {
                'Meaning': row.get('Meaning', '').strip() or None,
                'Collocation': row.get('Collocation', '').strip() or None,
                'Context': row.get('Context', '').strip() or None,
                'IPA': row.get('IPA', '').strip() or None,
                'Time': row.get('Time', '').strip() or None
            }

    return vocabulary_dict

def from_dict_to_json_file(vocabulary_dict: dict, date: str = None):
    # Group vocabulary into the same Time
    working_dict = defaultdict(list)
    if date:
        # If a date is provided, filter the vocabulary by that date
        for key, value in vocabulary_dict.items():
            noted_time = value.get('Time', None)
            if noted_time and noted_time == date:
                value['Vocabulary'] = key
                working_dict[noted_time].append(value)
    else:
        # If no date is provided, use all vocabulary
        for key, value in vocabulary_dict.items():
            noted_time = value.get('Time', None)
            if noted_time:
                value['Vocabulary'] = key
                working_dict[noted_time].append(value)

    # Since the working_dict is too large
    # - split to multiple json files, named as whatever can be unique
    # - each file contains maximum 20 entries
    # - each file is saved in a folder named as the date in Time field
    for time, entries in working_dict.items():
        if not entries:
            continue
        noted_time = time.replace('/', '-')
        date_folder = os.path.join(JSON_PATH_DIR, noted_time)
        if not os.path.exists(date_folder):
            os.makedirs(date_folder)
        for i in range(0, len(entries), 20):
            chunk = entries[i:i + 20]
            file_name = f"{i // 20 + 1}.json"
            file_path = os.path.join(date_folder, file_name)
            with open(file_path, 'w', encoding='utf-8') as json_file:
                json.dump(chunk, json_file, ensure_ascii=False, indent=4)

# Example usage:
if __name__ == "__main__":
    vocab_dict = build_vocabulary_dict(CSV_FILE_PATH)
    len_vocab = len(vocab_dict)
    # pprint(vocab_dict)
    print("---------------------------")
    from_dict_to_json_file(vocab_dict)
    print(f"Vocabulary dictionary created with {len_vocab} entries.")
