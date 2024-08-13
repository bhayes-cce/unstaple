import argparse
import os
import fitz  # PyMuPDF

def split_pdf(input_pdf_path, output_folder):
    # Open the input PDF file
    pdf_document = fitz.open(input_pdf_path)
    num_pages = pdf_document.page_count

    # Loop through all the pages and save each one as a separate PDF
    for page_num in range(num_pages):
        pdf_writer = fitz.open()  # Create a new PDF document for each page
        pdf_writer.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)

        output_pdf_path = os.path.join(output_folder, f"page_{page_num + 1}.pdf")
        pdf_writer.save(output_pdf_path)
        pdf_writer.close()
        print(f"Saved: {output_pdf_path}")

    pdf_document.close()

if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Split a PDF into single-page PDFs.")
    parser.add_argument("input_pdf_path", help="Path to the input PDF file.")
    parser.add_argument("output_folder", help="Folder where single-page PDFs will be saved.")

    # Parse the arguments
    args = parser.parse_args()

    # Ensure the output folder exists
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    # Split the PDF
    split_pdf(args.input_pdf_path, args.output_folder)
