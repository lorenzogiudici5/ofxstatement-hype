import os
import subprocess
import sys
import logging

def convert_pdf_to_ofx(pdf_file):
    """
    Create a function that takes every pdf file in a directory.
    For each file, call a function in which the ofxstatement command is called with the file name as a parameter.
    The function will create a new file with the same name but with the extension .ofx.
    """
    ofx_file = os.path.splitext(pdf_file)[0] + ".ofx"
    ofx_statement = subprocess.run(["ofxstatement", "convert", "-t", "hype", pdf_file, ofx_file])
    return ofx_statement

logging.basicConfig(level=logging.INFO)
logging.info("START")
# Take all pdf from directory passed as input parameter
folder_path = sys.argv[1]
files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".pdf")]

# Iterate on each file and call the function convert_pdf_to_ofx
for file in files:
    print("***" + file + "***")
    ofx_statement = convert_pdf_to_ofx(file)
    print(ofx_statement)