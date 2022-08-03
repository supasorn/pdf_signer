from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
from PIL import Image
import argparse
from pdf2image import convert_from_path

parser = argparse.ArgumentParser()
parser.add_argument('-pdf', type=str, default="")
args = parser.parse_args()

def pdf2jpg(f):
  images = convert_from_path(f, dpi=200)
  for i, img in enumerate(images):
    img.save(f.replace(".pdf", "_%02d.jpg" % i))


def gen():
  if args.pdf == "":
    exit()

  pdf2jpg(args.pdf)

if __name__ == "__main__":
  gen()
