import asyncio
import io
from pyppeteer import launch
from PyPDF2 import PdfFileMerger, PdfFileReader

# Configurations
chromiumPath = r"C:\Users\dhinesh.ks\Desktop\.local-chromium\Win64-884014\chrome-win\chrome.exe"
viewPort = {'width': 2000, 'height': 1200}
url = 'http://127.0.0.1:5500/html/index4.html'
urlConfig = {'timeout': 90000, 'waitUntil': 'domcontentloaded'}
pdfConfig = {'path': 'page.pdf', 'width': 1900, 'height': 1200,
             'margin': {'top': 50, 'left': 50, 'right': 50, 'bottom': 50}}


# PDF Merging
def mergePDF(bytes):
    merger = PdfFileMerger()
    merger.append(PdfFileReader(io.BytesIO(bytes)))
    merger.write("document-output.pdf")


# HTML to PDF
async def htmlToPdf(name):
    browser = await launch(headless=True, executablePath=chromiumPath)
    page = await browser.newPage()
    await page.setViewport(viewPort)
    await page.goto(url)  # can take urlconfig as second arg
    doc = await page.pdf(
        {'path': name, 'width': 1900, 'height': 1200, 'margin': {'top': 50, 'left': 50, 'right': 50, 'bottom': 50}})
    mergePDF(doc)
    await browser.close()


async def main():
    tasks = []
    print("Process Started")
    for x in range(5):
        tasks.append(asyncio.create_task(htmlToPdf(f"test{x}.pdf")))
    L = await asyncio.gather(*tasks)
    print("Process Completed")


asyncio.get_event_loop().run_until_complete(main())
