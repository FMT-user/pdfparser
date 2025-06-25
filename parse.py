from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import pandas as pd

def convert_pdf_to_text(path, pages=None):
    if not pages: 
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    with open(path, 'rb') as infile:
        for page in PDFPage.get_pages(infile, pagenums):
            interpreter.process_page(page)

    converter.close()
    text = output.getvalue()
    output.close()
    return text

# Example usage
text = convert_pdf_to_text('invoice.pdf', pages=[0, 3])
df = pd.DataFrame({'text': [text]})
def save_to_csv(df, filename='output.csv'):
    df.to_csv(filename, index=False)
save_to_csv(df, 'invoice_text.csv')
