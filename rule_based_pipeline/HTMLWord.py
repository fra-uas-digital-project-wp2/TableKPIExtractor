# ============================================================================================================================
# PDF_Analyzer
# File   : HTMLWord.py
# Author : Ismail Demir (G124272)
# Date   : 12.06.2020
#
# Note   : 1 HTMLItem consists of * HTMLWords
# ============================================================================================================================


from Rect import *


class HTMLWord:
    """
    Represents a word in an HTML context, typically extracted from a PDF file.

    Attributes:
        txt (str): The text content of the word.
        rect (Rect): The rectangle coordinates of the word, an instance of the Rect class.
        item_id (int): The ID of the HTMLItem to which this word belongs.
    """

    def __init__(self):
        """
        Initializes an instance of the HTMLWord class.
        """
        self.txt = ''
        self.rect = Rect(99999, 99999, -1, -1)
        self.item_id = -1
