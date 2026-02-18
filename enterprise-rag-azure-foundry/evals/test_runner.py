
import json

def run_eval(eval_file: str):
    results = []
    with open(eval_file) as f:
        for line in f:
            item = json.loads(line)
            print(f"Q: {item['question']}")
            print(f"Expected: {item['gold_answer']}")
            print("---")
            results.append({"id": item["id"], "status": "pending"})
    print(f"Loaded {len(results)} eval items")
    return results

if __name__ == "__main__":
    run_eval("hr_eval.jsonl")
