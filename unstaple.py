import argparse
import os
import hashlib
import fitz

def get_md5_hash(data):
    """Compute the MD5 hash of the given data."""
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()

def split_pdf(input_pdf_path, output_folder, sequential=False):
    pdf_document = fitz.open(input_pdf_path)
    num_pages = pdf_document.page_count
    base_name = os.path.splitext(os.path.basename(input_pdf_path))[0]

    for page_num in range(num_pages):
        # Create a new PDF document for each page
        pdf_writer = fitz.open()
        pdf_writer.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)

        # Save the single page PDF to a temporary file
        temp_pdf_path = os.path.join(output_folder, f"temp_page_{page_num + 1}.pdf")
        pdf_writer.save(temp_pdf_path)
        pdf_writer.close()

        # Read the content of the temporary PDF file and compute the MD5 hash
        with open(temp_pdf_path, 'rb') as temp_pdf_file:
            page_content = temp_pdf_file.read()
            md5_hash = get_md5_hash(page_content)

        # Determine final file name based on naming scheme
        if sequential:
            final_pdf_path = os.path.join(output_folder, f"{base_name}_{page_num + 1}.pdf")
        else:
            final_pdf_path = os.path.join(output_folder, f"{md5_hash}.pdf")

        # Rename the file with the MD5 hash or sequential name
        os.rename(temp_pdf_path, final_pdf_path)
        print(f"Saved: {final_pdf_path}")

    pdf_document.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a PDF into single-page PDFs with naming options.")
    parser.add_argument("-i", "--input_pdf", required=True, help="Path to the input PDF file.")
    parser.add_argument("-o", "--output_folder", help="Folder where single-page PDFs will be saved.")
    parser.add_argument("-s", "--sequential", action="store_true", help="Use sequential naming for output files.")
    args = parser.parse_args()
    if args.output_folder:
        output_folder = args.output_folder
    else:
        base_name = os.path.splitext(os.path.basename(args.input_pdf))[0]
        output_folder = os.path.join(os.path.dirname(args.input_pdf), base_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    split_pdf(args.input_pdf, output_folder, sequential=args.sequential)
