import re

def clean_textbf_in_tabular(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into chunks: tabular vs non-tabular
    parts = re.split(r"(\\begin{tabular}.*?\\end{tabular})", content, flags=re.DOTALL)

    cleaned_parts = []
    for part in parts:
        if part.startswith(r"\begin{tabular}"):
            processed = re.sub(r"\\textbf{(?!Q:|R:)(.*?)}", r"\1", part)
            processed = processed.replace(r"\textbf{}", "")
            cleaned_parts.append(processed)
        else:
            # Outside tabular: Leave completely untouched
            cleaned_parts.append(part)
    cleaned_content = "".join(cleaned_parts)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned_content)

# Example usage
if __name__ == "__main__":
    file_name = input("What is the file name? ")
    clean_textbf_in_tabular(file_name, "output.txt")
    print("Processing complete. Check output.txt")