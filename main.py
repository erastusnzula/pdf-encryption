import os
from tkinter.filedialog import askopenfilename, asksaveasfilename

from PyPDF2 import PdfFileReader, PdfFileWriter

# Select the pdf to encrypt.
pdf = askopenfilename()


def encrypt_pdf_file(password):
    """Encrypt a pdf file."""
    file = PdfFileReader(pdf)  # Read the file.
    new_file = PdfFileWriter()
    pages = file.getNumPages()
    for page in range(pages):
        new_file.addPage(file.getPage(page))
    new_file.encrypt(user_pwd=password, use_128bit=True)
    # Enter a name for the new encrypted file.
    save_as = asksaveasfilename()
    with open(os.path.join(save_as + ".pdf"), 'wb') as f:
        new_file.write(f)


if __name__ == "__main__":
    encrypt_pdf_file("twitter")
    print("file encrypted successfully.")
