from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
from PIL import Image
import argparse
from pdf2image import convert_from_path
import cv2
import os
import glob

parser = argparse.ArgumentParser()
parser.add_argument('-folder', type=str, default="pdf")

args = parser.parse_args()

def multisign():
  for f in glob.glob(args.folder + "/*.pdf"):
    sgn = f.replace(".pdf", "_signed.pdf")
    if os.path.exists(sgn) or f[-11:] == "_signed.pdf":
      continue
    os.system("python pysigner.py -pdf " + f)
    print(f)
  
if __name__ == "__main__":
  multisign()