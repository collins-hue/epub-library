from django.db import models

from django.db import models
from ebooklib import epub
import fitz  # PyMuPDF
import os

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class PDF(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='pdfs/')
    epub_file = models.FileField(upload_to='epubs/', blank=True, null=True)
    epub_content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    
    def convert_pdf_to_epub(self):
        """Converts the uploaded PDF to EPUB and extracts the content."""
        if not self.pdf_file:

            return

        # PDF to Text Conversion
        doc = fitz.open(self.pdf_file.path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text("text")
        doc.close()

        # Set EPUB content for display
        self.epub_content = text

        # Create EPUB file
        epub_path = os.path.join('media', 'epubs', f"{self.title}.epub")
        book = epub.EpubBook()
        book.set_title(self.title)
        book.set_language('en')

        # Create chapter with bold title using inline CSS
        chapter = epub.EpubHtml(title='Chapter 1', file_name='chap_01.xhtml')
        chapter.content = f"""
        <html>
        <head>
            <style>
               h1 {{
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <h1>{self.title}</h1>
            <p>{text}</p>
        </body>
        </html>
        """
    
        book.add_item(chapter)
        
        # Define the Table of Contents and spine
        book.toc = (epub.Link('chap_01.xhtml', 'Chapter 1', 'chapter_1'),)
        book.spine = ['nav', chapter]

        # Add navigation files
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # Write the EPUB file
        epub.write_epub(epub_path, book)

        # Save the EPUB file path and content
        self.epub_file = epub_path
        self.save()



#    def convert_pdf_to_epub(self):
#        """Converts the uploaded PDF to EPUB and extracts the content."""
 #       if not self.pdf_file:
 #           return
#
#        # PDF to Text Conversion
#        doc = fitz.open(self.pdf_file.path)
#        text = ""
#        for page_num in range(len(doc)):
#            page = doc.load_page(page_num)
#            text += page.get_text("text")
#        doc.close()

        # Set EPUB content for display
#        self.epub_content = text

        # Create EPUB file
#        epub_path = os.path.join('media', 'epubs', f"{self.title}.epub")
#        book = epub.EpubBook()
#        book.set_title(self.title)
#        book.set_language('en')
#        chapter = epub.EpubHtml(title='Chapter 1', file_name='chap_01.xhtml')
#        chapter.content = f"<h1>{self.title}</h1><p>{text}</p>"
#        book.add_item(chapter)
#        book.toc = (epub.Link('chap_01.xhtml', 'Chapter 1', 'chapter_1'),)
#        book.spine = ['nav', chapter]
#        book.add_item(epub.EpubNcx())
#        book.add_item(epub.EpubNav())
 #       epub.write_epub(epub_path, book)

        # Save the EPUB file path and content
#        self.epub_file = epub_path
#        self.save()

