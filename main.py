from re import M
from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename


print ('Print today date and desired location on a PDF')
# get today date (d-m-y)
date=datetime.today().strftime('%d-%m-%y')
# get the name to give to the output file
name=input("Insert output file desired name: ")
place=input("Insert location to be printed on the document: ")

print ('Select original PDF file path: ')

filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)

temporary = BytesIO() #temporary variable used to allocate memory space for the creation of the watermark PDF

# create a new watermark PDF containing date and place with Reportlab 
p = canvas.Canvas(temporary, pagesize=A4)
p.drawString(70,200,"%s, %s" %(date,place)) # insert here the position the date should occupy in your document ( the position is x,y calculated starting from the lower left corner of the page) 
p.showPage()
p.save()

newPdf = PdfFileReader(temporary)

watermark = temporary.getvalue()
open('watermark.pdf', 'wb').write(watermark)

# read your existing PDF
existingPdf = PdfFileReader(open("%s" %(filename), 'rb')) # reading the original PDF you want to add the date to
output = PdfFileWriter()
# add the "watermark" (which is the new pdf containing just the date and place) over the existing page
page = existingPdf.getPage(0)
page.mergePage(newPdf.getPage(0))
output.addPage(page)
# write the result to a file, naming it with the chosen name followed by the date
outputStream = open("%s %s.pdf" %(name,date), 'wb')
output.write(outputStream)
outputStream.close()
# delete the watermark PDF, since it's useless
os.remove("watermark.pdf")
    
