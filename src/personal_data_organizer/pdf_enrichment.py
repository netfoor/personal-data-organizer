import os 
import pandas as pd
from pypdf import PdfReader
from pathlib import Path



def clean_text(text: str) -> str:
    """Clean the extracted text."""
    text = text.strip()
    text = " ".join(text.split())
    return text


def truncate_sentence(text: str, max_len: int = 300) -> str:
    if len(text) <= max_len:
        return text
    truncated = text[:max_len]

    last_period = truncated.rfind(".")
    if last_period != -1:
        return truncated[:last_period+1]
    return truncated



def enrich_pdf(input_csv: Path, output_csv: Path) -> None:
    """Enrich the CSV file with PDF metadata."""
    
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f"File not found: {input_csv}")
        return
    except pd.errors.EmptyDataError:
        print(f"No data: {input_csv} is empty")
        return
    except pd.errors.ParserError:
        print(f"Parse error: Could not parse {input_csv}")
        return

    enriched_data = []
    
    for _, row in df.iterrows():
        file_path = row["path"]
        # Validate file path to prevent path traversal
        if not file_path or '..' in file_path:
            print(f"⚠️ Skipping invalid path: {file_path}")
            continue
        enrichment = {
            "path": file_path,
            "page_count": None,
            "title": None,
            "author": None,
            "created_date": None,
            "modified_date": None,
            "text": None
        }

        try:
            reader = PdfReader(file_path)
            enrichment["page_count"] = len(reader.pages)

            first_page_text = reader.pages[0].extract_text() or ""
            cleaned = clean_text(first_page_text)

            if cleaned:
                text = truncate_sentence(cleaned)
            else:
                text = "[NO TEXT EXTRACTED]"

            enrichment["text"] = text


            if reader.metadata:
                enrichment["title"] = getattr(reader.metadata, "title", None)
                if not enrichment["title"]:
                    enrichment['title'] = os.path.splitext(os.path.basename(file_path))[0]    
                enrichment["author"] = getattr(reader.metadata, "author", None)
                if not enrichment["author"]:
                    enrichment["author"] = "Unknown"
                enrichment["created_date"] = getattr(reader.metadata, "creation_date", None)
                if not enrichment["created_date"]:
                    enrichment["created_date"] = os.path.getctime(file_path)
                enrichment["modified_date"] = getattr(reader.metadata, "mod_date", None)
                if not enrichment["modified_date"]:
                    enrichment["modified_date"] = os.path.getmtime(file_path) or os.path.getctime(file_path)

        except Exception as e:
            print(f"⚠️ Could not process {file_path}: {e}")
            with open("bad_files.log", "a") as log_file:
                log_file.write(f"{file_path}\n")

        enriched_data.append(enrichment)
        
    enriched_df = pd.DataFrame(enriched_data)
    merged = df.merge(enriched_df, on="path", how="left")
    merged.to_csv(output_csv, index=False)
    print(f"✅ Enriched PDF data saved to {output_csv}")