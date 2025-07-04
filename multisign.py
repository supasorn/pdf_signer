import os
import glob
import argparse
import time
import datetime
from PyPDF2 import PdfReader

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

def multisign_downloadfolder():
  for f in glob.glob("/Users/supasorn/Downloads/*.pdf"):
    diff = time.time() - os.path.getctime(f)
    if diff > 60 * 20 * 10: continue

    nf = os.path.dirname(f) + "/signed_" + os.path.basename(f)
    if os.path.exists(nf) or "signed_" in f:
      continue
    # count number of pages
    try:
      with open(f, "rb") as pdf_file:
        reader = PdfReader(pdf_file)
        num_pages = len(reader.pages)
    except Exception as e:
      print(f"Could not read {f}: {e}")
      continue
    # ask for confirmation only if more than 20 pages
    if num_pages > 20:
      print("Signing file: " + f)
      confirm = input("Do you want to sign this file? (y/n): ")
      if confirm.lower() != 'y':
        print("Skipping file: " + f)
        continue

    os.system('python pysigner.py -pdf "' + f + '"')
    print(f)


if __name__ == "__main__":
  # multisign()
  multisign_downloadfolder()
