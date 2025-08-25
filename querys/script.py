import pandas as pd

csv_path = r'C:\IA\personal-data-organizer\artifacts\pdfs_enriched.csv'
column_name = 'extension'


def get_extensions():
    """Get unique file extensions from the CSV file."""
    try: 
        df = pd.read_csv(csv_path)
        extensions = df[column_name].unique()
        return list(extensions)
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
    except KeyError:
        print(f"Column '{column_name}' not found in the CSV file.")


def get_documents_extensions():
    """Get unique document file extensions from the CSV file."""
    try:
        df = pd.read_csv(csv_path)
        extensions = df[df['category'] == 'documents'][column_name].unique()
        return list(extensions)
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
    except KeyError:
        print(f"Column '{column_name}' not found in the CSV file.")


def each_documents_extension():
    """Count each document file extension from the CSV file."""
    try:
        df = pd.read_csv(csv_path)
        extensions = df[df['category'] == 'documents'][column_name].value_counts()
        return extensions.to_dict()
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
    except KeyError:
        print(f"Column '{column_name}' not found in the CSV file.")


def save_pdf_category():
    try:
        df = pd.read_csv(csv_path)
        pdf = df[df['category'] == 'documents']
        pdf = pdf[pdf['extension'] == '.pdf']
        pdf.to_csv(r'C:\IA\personal-data-organizer\artifacts\documents.csv', index=False)
        print("PDF documents saved.")
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
    except Exception as e:
        print(f"Error: {e}")
    except KeyError:
        print(f"Column '{column_name}' not found in the CSV file.")


def count_null_fields():
    """Count null fields in the CSV file."""
    try:
        df = pd.read_csv(csv_path)
        null_counts = df.isnull().sum()
        return null_counts[null_counts > 0]
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
    except Exception as e:
        print(f"Error: {e}")