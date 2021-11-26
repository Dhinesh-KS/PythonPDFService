import asyncio
import io
from pyppeteer import launch
from PyPDF2 import PdfFileMerger, PdfFileReader
import time

# Configurations
chromiumPath = r"C:\Users\dhinesh.ks\Desktop\.local-chromium\Win64-884014\chrome-win\chrome.exe"
viewPort = {'width': 2000, 'height': 1200}
url = 'http://127.0.0.1:5500/html/index4.html'
urlConfig = {'timeout': 90000, 'waitUntil': ['load', 'domcontentloaded', 'networkidle0']}
pdfConfig = {'width': 1900, 'height': 1200,
             'margin': {'top': 50, 'left': 50, 'right': 50, 'bottom': 50}}
# 'path': 'page.pdf'
pages = [];


# PDF Merging
def mergePDF():
    merger = PdfFileMerger()
    if len(pages) > 0:
        for item in pages:
            merger.append(PdfFileReader(io.BytesIO(item)))
        merger.write("document-output.pdf")
    else:
        print("No pages found!")


# HTML to PDF
async def htmlToPdf():
    browser = await launch(headless=True, executablePath=chromiumPath)
    page = await browser.newPage()
    await page.setViewport(viewPort)
    await page.goto(url, urlConfig)  # can take urlconfig as second arg
    doc = await page.pdf(pdfConfig)
    pages.append(doc)
    await browser.close()


async def main():
    tasks = []
    print("Process Started")
    start_time = time.perf_counter()
    for x in range(5):
        tasks.append(asyncio.create_task(htmlToPdf()))
    await asyncio.gather(*tasks)
    mergePDF()
    print("Process Completed")
    end_time = time.perf_counter()
    print("Total duration in seconds -", end_time - start_time)


asyncio.get_event_loop().run_until_complete(main())
