





# PDF EXTRACTOR

- This is an PDF Extractor which can extract Text,Images,Table and Summarize the whole PDF text from the PDF. 

# GITHUB REPO LINK:
- https://github.com/shehrozkapoor/PDFEXTRACTOR.git



# How to Install

- pip install pdfextractor
## or 
- dowload source file from GITHUB


## HOW to Use

## Extract Table 

- from pdfextractor import Table

- table = Table("pdfPath")

- extractTableCsv = table.extractTableCsv()

- extractTableJson = table.extractTableJson()

- extractTableHTML = table.extractTableHTML()

- extractSpecPageTableHTML = table.extractSpecPageTableHTML(page_num)


- extractSpecPageTableCsv = table.extractSpecPageTableCsv(page_num)

- extractSpecPageTableJson = table.extractSpecPageTableJson(page_num)

## Extract Images 
- from pdfextractor import Image

- image = Image("pdfPath")

- extractImageAll = image.extractImageAll()

- extractSpecImageMulti = image.extract_images([page_num,page_num...])

- extractImageSpecPage = image.extractImageSpecPage(page_num)



## Extract Text 
- from pdfextractor import Text

- text = Text(pdfPath)

- extractTextAll = text.extractTextAll()

- extractTextSpecPage = text.extractTextSpecPage()


## Extract Summarize 
- from pdfextractor import Summarize

- summary = Summarize(pdfPath)

- summarizer = summary.summarizer()
