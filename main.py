import asyncio
import io
from pyppeteer import launch
from PyPDF2 import PdfFileMerger, PdfFileReader
import time

# Configurations
chromiumPath = r"C:\Users\dhinesh.ks\Desktop\.local-chromium\Win64-884014\chrome-win\chrome.exe"
viewPort = {'width': 2000, 'height': 1200}
url = 'http://127.0.0.1:5500/html/index4.html'
urlConfig = {'timeout': 9000000, 'waitUntil': ['load', 'domcontentloaded', 'networkidle0']}
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


async def fetchPages(browser):
    page = await browser.newPage()
    await page.setViewport(viewPort)
    await page.goto(url, urlConfig)  # can take urlconfig as second arg
    doc = await page.pdf(pdfConfig)
    pages.append(doc)


# HTML to PDF
async def htmlToPdf():
    tasks = []
    browser = await launch(headless=True, executablePath=chromiumPath)
    for x in range(2):
        tasks.append(asyncio.create_task(fetchPages(browser)))
    await asyncio.gather(*tasks)
    mergePDF()
    await browser.close()


def main():
    print("Process Started")
    start_time = time.perf_counter()
    asyncio.get_event_loop().run_until_complete(htmlToPdf())
    print("Process Completed")
    end_time = time.perf_counter()
    print("Total duration in seconds -", end_time - start_time)


main()
