from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator

import re
import os
import sys


def find_absorintro(s):
    r = re.compile('(abstract|introduction)', re.I)
    if re.search(r, s) is not None:
        return True
    else:
        return False


def main():
    for i in range(1, len(sys.argv)):
        path_filename = str(sys.argv[i])
        path_split = path_filename.rsplit('\\', 1)
        path = path_split[0]
        filename = path_split[1]
        os.chdir(path)
        try:
            fp = open(filename, 'rb')
        except IOError:
            continue
        else:
            parser = PDFParser(fp)
            doc = PDFDocument(parser)
            if not doc.is_extractable:
                raise PDFTextExtractionNotAllowed
            else:
                rsrcmgr = PDFResourceManager()
                laparams = LAParams()
                device = PDFPageAggregator(rsrcmgr, laparams=laparams)
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                pages = PDFPage.create_pages(doc)
                page = pages.__next__()
                interpreter.process_page(page)
                layout = device.get_result()

                size = 0

                for box in layout:
                    if isinstance(box, LTTextBoxHorizontal):
                        text = box.get_text()
                        if find_absorintro(text):
                            break
                        else:
                            for line in box:
                                if isinstance(line, LTTextLineHorizontal):
                                    for ch in line:
                                        if ch.size > size:
                                            title = box.get_text()
                                            size = ch.size
                                        elif ch.size == size:
                                            title = title + box.get_text()
                                        break
                                break

                title = title.replace('\n', ' ')
                title = title.translate({ord(c): None for c in '<>:"/\|?*'})
                fp.close()
                #print(title.rstrip()+'.pdf')
                os.rename(filename, title.rstrip()+'.pdf')


if __name__ == "__main__":
    main()

