# ============================================================================================================================
# PDF_Analyzer
# File   : HTMLItem.py
# Author : Ismail Demir (G124272)
# Date   : 12.06.2020
#
# Note   : 1 HTMLItem consists of * HTMLWords
# Note   : 1 HTMLPage consists of * HTMLItems
# ============================================================================================================================

from globals import *
from HTMLWord import *
from Format_Analyzer import Format_Analyzer


class HTMLItem:
    """
    Represents an item in an HTML context.

    Attributes:
        line_num (int): The line number.
        tot_line_num (int): The total line number.
        pos_x (float): The x-coordinate in pixels.
        pos_y (float): The y-coordinate in pixels.
        width (float): The width in pixels.
        height (float): The height in pixels.
        initial_height (float): The initial height in pixels.
        font_size (float): The font size.
        txt (str): The text content.
        is_bold (bool): Indicates if the text is bold.
        brightness (int): The brightness value.
        alignment (int): The alignment (ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER).
        font_file (str): The font file.
        this_id (int): The ID of this HTMLItem.
        next_id (int): The ID of the next HTMLItem. -1 if None
        prev_id (int): The ID of the previous HTMLItem. -1 if None
        left_id (int): The ID of the item to the left. -1 if None
        right_id (int): The ID of the item to the right. -1 if None
        category (int): The category of the item (CAT_DEFAULT, CAT_HEADLINE, etc.).
        temp_assignment (int): A temporary assignment value. that is normally set to 0. It has greater values while table extraction is in progress
        merged_list (list): Indexes of items that this item has been merged with.
        words (list): List of all words (each a HTMLWord).
        space_width (float): The space width.
        has_been_split (bool): Indicates if the item has been split.
        rendering_color (tuple): The rendering color in RGBA format. used only for PNG rendering. not related with KPI extraction
        page_num (int): The page number.
    """

    def __init__(self):
        """
        Initializes an instance of the HTMLItem class.

        The instance variables are initialized with default or empty values.
        """
        self.line_num = 0
        self.tot_line_num = 0
        self.pos_x = 0
        self.pos_y = 0
        self.width = 0
        self.height = 0
        self.initial_height = None
        self.font_size = 0
        self.txt = ""
        self.is_bold = False
        self.brightness = 255
        self.alignment = ALIGN_LEFT
        self.font_file = ""
        self.this_id = -1
        self.next_id = -1
        self.prev_id = -1
        self.category = CAT_DEFAULT
        self.temp_assignment = 0
        self.merged_list = []
        self.words = []
        self.space_width = 0
        self.has_been_split = False
        self.left_id = -1
        self.right_id = -1
        self.rendering_color = (0, 0, 0, 255)  # black by default
        self.page_num = -1

    def is_connected(self):
        """
        Check if the item is connected to other items.

        Returns:
            bool: True if connected, False otherwise.
        """
        return self.next_id != -1 or self.prev_id != -1

    def get_depth(self):
        """
        Get the depth of the item.

        Returns:
            int: The depth value.
        """
        size = self.font_size
        if len(self.words) > 0:
            size = max(w.rect.y1 - w.rect.y0 for w in self.words)
            if size < self.font_size * 0.8:
                size = self.font_size * 0.8
            if size > self.font_size * 1.2:
                size = self.font_size * 1.2
        return 10000 - int(size * 10 + (5 if self.is_bold else 0) + (3 * (255 - self.brightness)) / 255)

    def get_aligned_pos_x(self):
        """
        Get the aligned x-position of the item.

        Returns:
            float: The aligned x-position.
        """
        if self.alignment == ALIGN_LEFT:
            return self.pos_x
        if self.alignment == ALIGN_RIGHT:
            return self.pos_x + self.width
        if self.alignment == ALIGN_CENTER:
            return self.pos_x + self.width * 0.5
        return None  # not yet implemented

    def is_text_component(self):
        """
        Check if the item is a text component.

        Returns:
            bool: True if a text component, False otherwise.
        """
        return self.category in [CAT_HEADLINE, CAT_OTHER_TEXT, CAT_RUNNING_TEXT, CAT_FOOTER]

    def has_category(self):
        """
        Check if the item has a category.

        Returns:
            bool: True if a category is assigned, False otherwise.
        """
        return self.category != CAT_DEFAULT

    def has_category_besides(self, category_to_neglect):
        """
        Check if the item has a category besides a specified one.

        Args:
            category_to_neglect (int): The category to neglect.

        Returns:
            bool: True if a different category is assigned, False otherwise.
        """
        return self.category != CAT_DEFAULT and self.category != category_to_neglect

    def get_rect(self):
        """
        Get the rectangular boundaries of the item.

        Returns:
            Rect: The rectangular boundaries.
        """
        return Rect(self.pos_x, self.pos_y, self.pos_x + self.width, self.pos_y + self.height)

    @staticmethod
    def find_item_by_id(items, id):
        """
        Find an item in a list by its identifier.

        Args:
            items (list): List of HTMLItem objects.
            id (int): The identifier to search for.

        Returns:
            HTMLItem: The found item or None if not found.
        """
        for it in items:
            if it.this_id == id:
                return it
        return None  # not found. should never happen

    def reconnect(self, next_it, all_items):
        """
        Reconnect the item with a new next item.

        Args:
            next_it: The next HTMLItem object.
            all_items (list): List of all HTMLItem objects.
        """
        if self.next_id != -1:
            old_next_it = HTMLItem.find_item_by_id(all_items, self.next_id)
            old_next_it.prev_id = -1

        if next_it.prev_id != -1:
            new_next_olds_prev_it = HTMLItem.find_item_by_id(all_items, next_it.prev_id)
            new_next_olds_prev_it.next_id = -1

        self.next_id = next_it.this_id
        next_it.prev_id = self.this_id

    def is_mergable(self, it):
        """
        Check if the item is mergable with another item.

        Args:
            it: The other HTMLItem object.

        Returns:
            bool: True if mergable, False otherwise.
        """
        if self.next_id == -1 and it.next_id == -1:
            return False
        if self.prev_id == -1 and it.prev_id == -1:
            return False
        return (self.next_id == it.this_id or self.prev_id == it.this_id) \
            and self.pos_x == it.pos_x \
            and self.font_file == it.font_file \
            and self.height == it.height \
            and not Format_Analyzer.looks_numeric(self.txt) \
            and not Format_Analyzer.looks_numeric(it.txt)

    def is_weakly_mergable_after_reconnect(self, it):
        """
        Check if the item is weakly mergable with another item after reconnecting.

        Args:
            it: The other HTMLItem object.

        Returns:
            bool: True if weakly mergable, False otherwise.
        """
        return self.font_file == it.font_file \
            and self.font_size == it.font_size \
            and abs(self.get_initial_height() - it.get_initial_height()) < 0.1

    def get_font_characteristics(self):
        """
        Get the font characteristics of the item.

        Returns:
            str: The font characteristics string.
        """
        return self.font_file + '???' + str(self.font_size) + '???' + str(self.brightness) + '???' + str(self.is_bold)

    def get_initial_height(self):
        """
        Get the initial height of the item.

        Returns:
            float: The initial height.
        """
        if self.initial_height is not None:
            return self.initial_height
        return self.height

    def recalc_width(self):
        """
        Recalculate the width of the item based on its text content and font properties.
        """
        span_font = ImageFont.truetype(self.font_file, self.font_size)
        size = span_font.getsize(self.txt)
        self.width = size[0]
        if self.width == 0:
            # approximate
            size = span_font.getsize('x' * len(self.txt))
            self.width = size[0]

    def merge(self, it):
        """
        Merge the item with another mergable item.

        Args:
            it: The other HTMLItem object.

        Raises:
            ValueError: If items cannot be merged.
        """
        # precondition: both items must be mergable
        if self.next_id == it.this_id:
            self.txt += '\n' + it.txt
            self.initial_height = self.get_initial_height()
            self.height = it.pos_y + it.height - self.pos_y
            self.width = max(self.width, it.width)
            self.words = self.words + it.words
            it.words = []
            it.txt = ''
        elif self.prev_id == it.this_id:
            it.txt += '\n' + self.txt
            it.initial_height = it.get_initial_height()
            it.height = self.pos_y + self.height - it.pos_y
            it.width = max(self.width, it.width)
            it.words = self.words + it.words
            self.txt = ''
            self.words = []
        else:
            raise ValueError('Items ' + str(self) + ' and ' + str(it) + ' cannot be merged.')

        old_merged_list = self.merged_list.copy()
        self.merged_list.append(it.this_id)
        self.merged_list.extend(it.merged_list)
        it.merged_list.append(self.this_id)
        it.merged_list.extend(old_merged_list)

    def fix_overlapping_words(self):
        """
        Fix overlapping words by adjusting their x1 coordinate.
        """
        # assertion: all words are ordered by x ascending
        for i in range(len(self.words) - 1):
            self.words[i].rect.x1 = min(self.words[i].rect.x1, self.words[i + 1].rect.x0 - 0.00001)

    def recalc_geometry(self):
        """
        Recalculate the geometry of the item based on its words' bounding boxes.
        """
        self.pos_x = 9999999
        self.pos_y = 9999999
        x1 = -1
        y1 = -1
        for w in self.words:
            self.pos_x = min(self.pos_x, w.rect.x0)
            self.pos_y = min(self.pos_y, w.rect.y0)
            x1 = max(x1, w.rect.x1)
            y1 = max(y1, w.rect.y1)
        self.width = x1 - self.pos_x
        self.height = y1 - self.pos_y

    def rejoin_words(self):
        """
        Rejoin words into a single text string.
        """
        self.txt = ''
        for w in self.words:
            if self.txt != '':
                self.txt += ' '
            self.txt += w.txt

    def split(self, at_word, next_item_id):
        """
        Split the item at a specified word index.

        Args:
            at_word (int): The word index to split at.
            next_item_id (int): The identifier for the new next item.

        Returns:
            HTMLItem: The new item created after the split.
        """
        # example "abc 123 def" -> split(1, 99) ->
        # result "abc", and new item with item_id=99 "123 def"
        new_item = HTMLItem()
        new_item.line_num = self.line_num
        new_item.tot_line_num = self.tot_line_num
        new_item.font_size = self.font_size
        new_item.words = self.words[at_word:]
        new_item.is_bold = self.is_bold
        new_item.brightness = self.brightness
        new_item.alignment = self.alignment
        new_item.font_file = self.font_file
        new_item.this_id = next_item_id
        new_item.next_id = -1
        new_item.prev_id = -1
        new_item.category = self.category
        new_item.temp_assignment = self.temp_assignment
        new_item.merged_list = self.merged_list
        new_item.space_width = self.space_width
        new_item.has_been_split = True

        self.has_been_split = True

        new_item.left_id = self.this_id
        new_item.right_id = self.right_id
        new_item.page_num = self.page_num
        self.right_id = new_item.this_id

        for k in range(at_word, len(self.words)):
            self.words[k].item_id = next_item_id

        self.words = self.words[0:at_word]
        self.recalc_geometry()
        self.rejoin_words()

        new_item.recalc_geometry()
        new_item.rejoin_words()

        return new_item

    @staticmethod
    def concat_txt(item_list, sep=' '):
        """
        Concatenate the text content of a list of items.

        Args:
            item_list (list): List of HTMLItem objects.
            sep (str): Separator to use between concatenated texts.

        Returns:
            str: The concatenated text.
        """
        res = ''
        for it in item_list:
            if res != '':
                res += sep
            res += it.txt
        return res

    def __repr__(self):
        """
        Return a string representation of the HTMLItem.

        Returns:
            str: The string representation.
        """
        return "<HTMLItem: line_num=" + str(self.line_num) + ", pos_x=" + str(self.pos_x) + ", pos_y=" + str(
            self.pos_y) + ", is_bold=" + str(self.is_bold) + ", width=" + str(self.width) \
            + ", height=" + str(self.height) + ", init_height=" + str(self.get_initial_height()) \
            + ", align=" + (
                "L" if self.alignment == ALIGN_LEFT else "R" if self.alignment == ALIGN_RIGHT else "C") + ", brightness=" + str(
                self.brightness) \
            + (", cat=" + str(self.category) + ", tmp_ass=" + str(
                self.temp_assignment) if config.global_verbosity >= 8 else "") \
            + ", depth=" + str(self.get_depth()) + ",font_size=" + str(
                self.font_size) + ", txt='" + self.txt + "', id=" + str(self.this_id) + ", pid=" + str(
                self.prev_id) + ", nid=" + str(self.next_id) + ">"
