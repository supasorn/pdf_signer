from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
from PIL import Image
import argparse
from pdf2image import convert_from_path

parser = argparse.ArgumentParser()
parser.add_argument('-pdf', type=str, default="pdf/memo.pdf")
parser.add_argument('-x', type=float, default=0.58101388)
parser.add_argument('-y', type=float, default=0.37852583)
parser.add_argument('--signature', type=str, default="signature.png", help="Path to signature image file")

args = parser.parse_args()

def sign():

  input_file = PdfFileReader(open(args.pdf, "rb"))
  c.drawImage(signature_img, args.x * float(w), args.y * float(h), sw, sw * sig.size[1] / sig.size[0], mask='auto')

  signature_img = args.signature
  sig = Image.open(signature_img)

  signature_width = 0.16

  c = canvas.Canvas('watermark.pdf')
  c.setPageSize((w, h))
  sw = float(w) * signature_width
  c.drawImage("signature.png", args.x * float(w), args.y * float(h), sw, sw * sig.size[1] / sig.size[0], mask='auto')
  c.save()


  watermark = PdfFileReader(open("watermark.pdf", "rb"))
  output_file = PdfFileWriter()
  input_file = PdfFileReader(open(args.pdf, "rb"))

  for page_number in range(input_file.getNumPages()):
    input_page = input_file.getPage(page_number)
    input_page.mergePage(watermark.getPage(0))
    output_file.addPage(input_page)

  # finally, write "output" to document-output.pdf
  with open("document-output.pdf", "wb") as outputStream:
    output_file.write(outputStream)


if __name__ == "__main__":
  sign()
