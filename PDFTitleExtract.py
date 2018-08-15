#!/usr/bin/env python3

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator

import re
import os
import sys


def line_length(s):
    cnt = 0
    size = 0
    for ch in s:
        if isinstance(ch, LTChar):
            if ch.size > size:
                cnt = 1
                size = ch.size
            elif ch.size == size:
                cnt += 1

    # s = s.get_text()
    # result = re.findall(r'[a-z0-9]', s, re.I)
    # if len(result) <= 1:
    if cnt <= 1:
        return False
    else:
        return True


def title_proc(title):
    title = re.sub(r'[\s<>:"/\\|\?*]+', ' ', title)
    return title


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
                        for line in box:
                            if line_length(line) and isinstance(line, LTTextLineHorizontal):
                                for ch in line:
                                    if ch.size > size:
                                        title = box.get_text()
                                        size = ch.size
                                    elif ch.size == size:
                                        title = title + box.get_text()
                                    break
                            break

                title = title_proc(title)
                fp.close()
                print(title.rstrip()+'.pdf')
                os.rename(filename, title.rstrip()+'.pdf')


if __name__ == "__main__":
    main()

