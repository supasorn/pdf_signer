from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
from PIL import Image
import argparse
from pdf2image import convert_from_path
import cv2
import os
import numpy as np

def sign():
  for i in range(10):
    noise = np.random.normal(0, 1, (128, 128, 3))
    cv2.imwrite(f"a{i}.jpg", noise * 255)
    # cv2.imshow("im", noise)
    # cv2.waitKey(0)

if __name__ == "__main__":
  sign()
