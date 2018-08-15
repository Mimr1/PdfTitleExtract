# PDF Title Extraction

Extract and rename the title of academic paper pdfs using pdfminer, based on the font size, given that the font size of the title is largest in academic papers in most cases.

Develop and test on Windows 10, python 3.6.4

## Usage

python PDFTitleExtract.py File1 [File2 ...]

## Notes

### Packages

* [pdfminer.six](https://github.com/pdfminer/pdfminer.six)

### Major Processes

Obatin the first page. There are two variables to store the max fontsize ```size``` and the characters with the max fontsize ```title```. Then for each horizontal text box, if the max fontsize in the first line is larger than ```size```, assign ```title``` with contents of the current box; if equal, append ```title``` with contents of the current box.

Notice that in a line, if the number of characters with the max fontsize is equal to 1, the character is a [initial drop cap letter](http://www.magazinedesigning.com/drop-caps-and-initial-letters/) probably, which should be ignored.



