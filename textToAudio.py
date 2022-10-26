#imported required packages
from tkinter.filedialog import *
from langdetect import detect
from gtts import gTTS
import os
import tika
from tika import parser
from playsound import playsound
from fpdf import FPDF 
from PyPDF2 import PdfFileReader, PdfFileWriter

#Window prompting for selecting a particular file
tika.initVM()
file = askopenfilename()
print(end='\n')
print(end='\n')
print("Path of the File which is Selected: ", file)
print(end='\n')
#Extracting paths from the selected file
print("-----------------------------------------------------------------------------------------------------------------",end='\n')
head, tail = os.path.split(file)
print("Location where the file will be saved: ", head,end='\n')
print(end='\n')

#File name is extracted for the path acquired
basename = os.path.basename(file)
print("Name of the File which has been Selected: ", basename)
print(end='\n')
info = os.path.splitext(basename)
filename = info[0]
print("Final name of the output File: ", filename)
print(end='\n')

#For specific range of page in the selected file
print("Do you only a specific range of pages in the book (Yes / No): ")
range_of_page = input()
print("Note: If Yes specify the starting and ending page number.")

#Condition for checking and separating the pages
if range_of_page.lower() == "Yes".lower():
    pdf = FPDF() 
    pdf.add_page() 
    pdf.add_font('gargi', '', 'DRVIE:FOLDER_PATH\\PROJECT_NAME\\gargi.ttf', uni=True) 
    pdf.set_font('gargi', '', 14)
    pdf.ln(20)
    f = open(file, "r", encoding="utf-8") 
    for x in f: 
        pdf.cell(200, 10, txt = x, ln = 1) 
    complete_path = head + "/" + "target.pdf"
    print(complete_path)
    pdf.output(complete_path)

#Gaining page number for separating
    pdf_file_path = complete_path
    file_base_name = pdf_file_path.replace('.pdf', '')
    pdf = PdfFileReader(pdf_file_path)
    print("Enter the Starting page number: ")
    start = int(input())
    print("Enter the Ending page number: ")
    end = int(input())
    pages = [start - 1, end - 1]
    pdfWriter = PdfFileWriter()
    for page_num in pages:
        pdfWriter.addPage(pdf.getPage(page_num))  
    with open('{0}_subset.pdf'.format(file_base_name), 'wb') as f:
        pdfWriter.write(f)
        f.close()
    text = parser.from_file(head + "/" + 'target_subset.pdf')
    #Removal of files
    os.remove(complete_path)
    os.unlink(head + "/" + 'target_subset.pdf')


elif range_of_page.lower() == "No".lower():
    #Else whole file will be converted as audio
    text = parser.from_file(file)


#Showing the extracted content
print("***************************************************************************************************************")
print("Extracted Content of the File: ")
print(text["content"])
print("***************************************************************************************************************")

#Detecting the language
textFile = text["content"]
language = detect(textFile)
print("Language detected from the File: ", language)
print(end='\n')

#Gaining the way through which the output should be
print("If needed to save and play press 0 or just to save 1: ")
way = int(input())
print(end='\n')
path = os.chdir(head)
print(os.getcwd())

#Condition to execute the way selected
if way==0:
    file = gTTS(text=textFile, lang=language)
    file.save(filename + ".mp3")
    playsound(filename + ".mp3")
else:
    file = gTTS(text=textFile, lang=language)
    file.save(filename + ".mp3")
