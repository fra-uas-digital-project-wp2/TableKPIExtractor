# ============================================================================================================================
# PDF_Analyzer
# File   : HTMLDirectory.py
# Author : Ismail Demir (G124272)
# Date   : 12.06.2020
#
# Note   : 1 HTMLDirectory consistens of * HTMLPages
# Note   : 1 HTMLDirectory corresponds to 1 PDF-File
# ============================================================================================================================
import os
import glob
import shutil
import subprocess
from HTMLPage import HTMLPage
from globals import print_verbose, config_for_rb, remove_trailing_slash, get_html_out_dir


class HTMLDirectory:
    """
    Represents a directory containing HTML pages related to a PDF file.
    """

    def __init__(self):
        """
        Initialize an HTMLDirectory instance.
        """
        self.htmlpages = []
        self.src_pdf_filename = None

    @staticmethod
    def call_pdftohtml(infile, outdir):
        """
        System Call "pdftohtml.exe". Converts PDF to HTML.

        Args:
            infile (str): Path to the PDF file.
            outdir (str): Directory to store HTML files.

        Returns:
            None
        """
        print_verbose(1, '-> call pdftohtml_mod ' + infile)
        exe = remove_trailing_slash(config_for_rb.global_exec_folder)  + r'/pdftohtml_mod/pdftohtml_mod'
        pdf = infile
        out = remove_trailing_slash(outdir)
        command = [exe,pdf,out]
        print(command)
        #command = ['"'+remove_trailing_slash(config_for_rb.global_exec_folder)  + r'/pdftohtml_mod/pdftohtml_mod'+'"','"./'+infile+'"', '"./'+remove_trailing_slash(outdir)+'"']
        subprocess.run(command, check=True,shell=True)
        #os.system(
        #    config_for_rb.global_exec_folder + r'/pdftohtml_mod/pdftohtml_mod "' + infile + '" "' +
        #    remove_trailing_slash(outdir) + '"')



    @staticmethod
    def fix_strange_encryption(html_dir):
        """
        Fixes strange encryption in HTML files.

        Args:
            html_dir (str): Path to the directory containing HTML files.

        Returns:
            None
        """
        html_dir = remove_trailing_slash(html_dir)
        pathname = html_dir + '/page*.html'
        print_verbose(2, "Fixing strange encryption = " + str(pathname))

        for f in glob.glob(pathname):
            print_verbose(3, "---> " + str(f))
            HTMLPage.fix_strange_encryption(f)

    @staticmethod
    def convert_pdf_to_html(pdf_file, info_file_contents, out_dir=None):
        """
        Cleans target dir for PDF to HTML conversion and Converts a PDF file to HTML.

        Args:
            pdf_file (str): Path to the PDF file.
            info_file_contents (dict): Information loaded from an info file.
            out_dir (str, optional): Directory to store HTML files. If not provided, it's generated based on the PDF file.

        Returns:
            None
        """
        out_dir = get_html_out_dir(pdf_file) if out_dir is None else remove_trailing_slash(out_dir)

        try:
            shutil.rmtree(out_dir)
        except OSError:
            pass
        HTMLDirectory.call_pdftohtml(pdf_file, out_dir)

        # Fix strange encryption
        # HTMLDirectory.fix_strange_encryption(out_dir) # TODO: Uncomment if needed.

        with open(out_dir + '/info.txt', 'w') as file:
            file.write(info_file_contents[pdf_file])

    def read_pdf_filename(self, html_dir):
        """
        Reads the PDF filename from the info.txt file in the HTML directory.

        Args:
            html_dir (str): Path to the HTML directory.

        Returns:
            None
        """
        with open(remove_trailing_slash(html_dir) + '/info.txt') as file:
            self.src_pdf_filename = file.read()
            print_verbose(2, 'PDF-Filename: ' + self.src_pdf_filename)

    def parse_html_directory(self, html_dir, page_wildcard):
        """
        Parses the contents of a HTML Directory into a data structure.

        Args:
            html_dir (str): HTML Directory of current pdf.
            page_wildcard (str): String used to filter pages in HTML Directory.

        Returns:
            None
        """
        html_dir = remove_trailing_slash(html_dir)
        pathname = html_dir + '/' + page_wildcard
        print_verbose(1, "PARSING DIR = " + str(pathname))

        self.read_pdf_filename(html_dir)

        for file in glob.glob(pathname):
            print_verbose(1, "ANALYZING HTML-FILE = " + str(file))

            htmlpage = HTMLPage.parse_html_file(html_dir, file)

            print_verbose(1, "Discovered tables: ")
            print_verbose(1, htmlpage.repr_tables_only())
            print_verbose(1, "Done with page = " + str(htmlpage.page_num))

            self.htmlpages.append(htmlpage)

    def render_to_png(self, base_dir, out_dir):
        """
        Converts HTMLPages into PNGs.

        Args:
            base_dir (str): Path to HTMLDirectory
            out_dir (str): Path to save pngs of HTMLPages.

        Returns:
            None
        """
        for it in self.htmlpages:
            print_verbose(1, "Render to png : page = " + str(it.page_num))
            it.render_to_png(remove_trailing_slash(base_dir), remove_trailing_slash(out_dir))

    def print_all_tables(self):
        """
        Prints tables in all HTML pages.

        Returns:
            None
        """
        for it in self.htmlpages:
            print(it.repr_tables_only())

    def save_to_dir(self, out_dir):
        """
        Serializes parsed HTMLDirectory and saves further objects in special JSON and CSV files.

        Args:
            out_dir (str): Output directory to save data.

        Returns:
            None
        """
        for it in self.htmlpages:
            print_verbose(1, "Save to JSON and CSV: page = " + str(it.page_num))
            it.save_to_file(
                remove_trailing_slash(out_dir) + r'/jpage' + "{:05d}".format(it.page_num) + '.json')
            it.save_all_tables_to_csv(out_dir)
            it.save_all_footnotes_to_txt(out_dir)

    def load_from_dir(self, html_dir, page_wildcard):
        """
        Loads HTMLDirectory (Report) from JSON files.

        Args:
            html_dir (str): Directory Path to HTMLDirectory.
            page_wildcard (str): Wildcard determining for which JSON files to filter.

        Returns:
            None
        """
        html_dir = remove_trailing_slash(html_dir)
        pathname = html_dir + '/' + page_wildcard

        self.read_pdf_filename(html_dir)

        for file in glob.glob(pathname):
            print_verbose(1, "LOADING JSON-FILE = " + str(file))
            htmlpage = HTMLPage.load_from_file(file)
            self.htmlpages.append(htmlpage)
