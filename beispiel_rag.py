import json
import ollama

def main():
    with open("beispiel.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    new_data = []
    counter = 0

    for item in data:
        exp_id = item.get("experiment")
        extracted_text = item.get("extracted_text", "")

        if not isinstance(extracted_text, str) or extracted_text.strip() == "":
            new_data.append({"experiment": exp_id, "error": "No text found"})
            continue

        if counter >= 10:
            break

        prompt = (
            "Extract the relevant information from the following text and provide a concise summary. "
            "If the text is empty, return an appropriate message indicating that no information is available.\n\n"
            f"Text:\n{extracted_text}\n\nSummary:"
        )

        try:
            response = ollama.chat(
                model="qwen2.5:14b",
                messages=[{"role": "user", "content": prompt}],
                format="json",
                options={"temperature": 0.2},
            )
        except Exception as e:
            new_data.append({"experiment": exp_id, "error": f"API error: {e}"})
            counter += 1
            continue

        # assume response contains a 'content' field or similar; adapt as needed
        summary = None
        if isinstance(response, dict):
            # try common keys
            summary = response.get("content") or response.get("output") or str(response)
        else:
            summary = str(response)

        new_data.append({"experiment": exp_id, "summary": summary})
        counter += 1

    # Output results
    print(json.dumps(new_data, ensure_ascii=False, indent=2))
