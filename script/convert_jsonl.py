import json

# Paths (adjust based on your project)
INPUT_JSONL = "data/mental_health_resources/mental_health_dataset.jsonl"
OUTPUT_JSONL = "data/mental_health_resources/mental_health_dataset_improved.jsonl"

def convert_jsonl(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as infile, \
         open(output_path, "w", encoding="utf-8") as outfile:
        for line in infile:
            data = json.loads(line)
            new_entry = {
                "question": data["instruction"],
                "answer": data["output"],
                "metadata": {
                    "topic": "self-worth",  # TODO: Auto-detect topics (see below)
                    "source": "original_dataset"
                }
            }
            outfile.write(json.dumps(new_entry) + "\n")

if __name__ == "__main__":
    convert_jsonl(INPUT_JSONL, OUTPUT_JSONL)
    print(f"✅ Converted {INPUT_JSONL} -> {OUTPUT_JSONL}")