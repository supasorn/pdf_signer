from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
from PIL import Image
import argparse
from pdf2image import convert_from_path
import cv2
import os

parser = argparse.ArgumentParser()
parser.add_argument('-pdf', type=str, default="pdf/memo.pdf")

args = parser.parse_args()


sm = None
sig = None
sig_small = None
pagei = 0

pos = []
dwidth = 1000
signature_width = 0.16

def signPdf():
  print(pos)
  input_file = PdfFileReader(open(args.pdf, "rb"))
  _, _, w, h = input_file.getPage(0).mediaBox

  signature_img = "signature.png"
  sig = Image.open(signature_img)

  output_file = PdfFileWriter()
  pages = input_file.getNumPages()
  for i in range(pages):
    input_page = input_file.getPage(i)

    if pos[i][0] != -1:
      c = canvas.Canvas('watermark.pdf')
      c.setPageSize((w, h))
      sw = float(w) * signature_width
      x = pos[i][0] / dwidth
      y = 1 - (pos[i][1] + sig_small.shape[0]) / sm.shape[0]
      print(x, y)
      c.drawImage("signature.png", x * float(w), y * float(h), sw, sw * sig.size[1] / sig.size[0], mask='auto')
      c.save()

      watermark = PdfFileReader(open("watermark.pdf", "rb"))
      input_page.mergePage(watermark.getPage(0))

    output_file.addPage(input_page)

  with open(args.pdf.replace(".pdf", "_signed.pdf"), "wb") as outputStream:
    output_file.write(outputStream)

  i = 0
  while True:
    p = getNumberedName(args.pdf, i)
    if os.path.exists(p):
      os.remove(p)
      i += 1
    else:
      break;
  exit()

def nextPage(x, y):
  global pagei
  pos.append([x, y])
  if os.path.exists(getNumberedName(args.pdf, pagei+1)):
    pagei += 1
    setNewPage()
  else:
    signPdf()

def click_and_crop(event, x, y, flags, param):
  global sm, sig, sig_small, pagei
  tsm = sm.copy()
  tsm[y, x] = 0

  rows,cols,channels = sig_small.shape

  print(sig_small.shape)
  # overlay = cv2.addWeighted(background[250:250+rows, 0:0+cols],0.5,overlay,0.5,0)

  alpha = sig_small[:, :, 3:] / 255.0
  tsm[y:y+rows, x:x+cols ] = sig_small[:, :, :3] * alpha + tsm[y:y+rows, x:x+cols] * (1-alpha)
  # tsm[y:y+rows, x:x+cols ] = sig_small[:, :, :3]
  cv2.imshow("pp", tsm)
  if event == cv2.EVENT_LBUTTONUP:
    nextPage(x, y)


def pdf2jpg(f):
  images = convert_from_path(f, dpi=200)
  for i, img in enumerate(images):
    img.save(f.replace(".pdf", "_%02d.jpg" % i))


def getNumberedName(pdf, num):
  return pdf.replace(".pdf", "_%02d.jpg" % num)

def setNewPage():
  global pagei, sm
  img = cv2.imread(getNumberedName(args.pdf, pagei))
  sm = cv2.resize(img, (dwidth, int(dwidth * img.shape[0] / img.shape[1])))
  cv2.imshow("pp", sm)

def sign():
  global sm, sig, sig_small, dwidth

  pdf2jpg(args.pdf)
  sig = cv2.imread("signature.png", cv2.IMREAD_UNCHANGED)
  swidth = int(signature_width * dwidth)
  print(swidth)
  print(sig.shape)
  sig_small = cv2.resize(sig, (swidth, int(swidth * sig.shape[0] / sig.shape[1])))

  setNewPage()
  cv2.setMouseCallback("pp", click_and_crop)
  while True:
    k = cv2.waitKey(0)
    if k == 27:
      exit()
    elif k == 32:
      nextPage(-1, -1)

if __name__ == "__main__":
  sign()
