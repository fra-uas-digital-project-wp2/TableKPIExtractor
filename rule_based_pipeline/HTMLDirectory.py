# ============================================================================================================================
# PDF_Analyzer
# File   : HTMLDirectory.py
# Author : Ismail Demir (G124272)
# Date   : 12.06.2020
#
# Note   : 1 HTMLDirectory consistens of * HTMLPages
# Note   : 1 HTMLDirectory corresponds to 1 PDF-File
# ============================================================================================================================
from HTMLPage import HTMLPage
from glob import glob
from globals import config_for_rb, get_html_out_dir, print_verbose, remove_trailing_slash
from os import system
from shutil import rmtree
import subprocess

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
        # Print a verbose message indicating the call to pdftohtml_mod
        print_verbose(1, '-> call pdftohtml_mod ' + infile)
        exe = remove_trailing_slash(config_for_rb.global_exec_folder)  + r'/pdftohtml_mod/pdftohtml_mod'
        pdf = infile
        out = remove_trailing_slash(outdir)
        command = [exe,pdf,out]
        print(command)
        subprocess.run(command, check=True,shell=True)
       


    @staticmethod
    def convert_pdf_to_html(pdf_file, info_file_contents, out_dir=None):
        """
        Cleans the target directory for PDF to HTML conversion and converts a PDF file to HTML.

        Args:
            pdf_file (str): Path to the PDF file.
            info_file_contents (dict): Information loaded from an info file.
            out_dir (str, optional): Directory to store HTML files. If not provided, it's generated based on the PDF file.

        Returns:
            None
        """
        # Determine the output directory for HTML files
        out_dir = get_html_out_dir(pdf_file) if out_dir is None else remove_trailing_slash(out_dir)

        try:
            # Remove the existing output directory if it exists
            rmtree(out_dir)
        except OSError:
            pass

        # Call the pdftohtml function to convert the PDF to HTML
        HTMLDirectory.call_pdftohtml(pdf_file, out_dir)

        # Write the information from the info file to the info.txt file in the working directory
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
        # Open the info.txt file in the specified HTML directory "/html"
        with open(remove_trailing_slash(html_dir) + '/info.txt') as file:
            # Read the contents of the file and set it as the PDF filename
            self.src_pdf_filename = file.read()

    def parse_html_directory(self, html_dir, page_wildcard):
        """
        Parses the contents of an HTML Directory into a data structure.

        Args:
            html_dir (str): HTML Directory of the current PDF.
            page_wildcard (str): String used to filter pages in the HTML Directory.

        Returns:
            None
        """
        # Ensure the HTML directory path does not have a trailing slash
        html_dir = remove_trailing_slash(html_dir)

        # Construct the pathname using the HTML directory and page wildcard
        pathname = html_dir + '/' + page_wildcard
        print_verbose(1, "PARSING DIR = " + str(pathname))

        # Read the PDF filename from the info.txt file in the HTML directory
        self.read_pdf_filename(html_dir)

        # Iterate through HTML files in the specified directory
        for file in glob(pathname):
            print_verbose(1, "ANALYZING HTML-FILE = " + str(file))

            # Parse the HTML file and create an HTMLPage object
            htmlpage = HTMLPage.parse_html_file(html_dir, file)

            print_verbose(1, "Discovered tables: ")
            print_verbose(1, htmlpage.repr_tables_only())
            print_verbose(1, "Done with page = " + str(htmlpage.page_num))

            # Append the HTMLPage object to the list of HTML pages
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
        # Iterate through each HTMLPage in the HTMLDirectory
        for it in self.htmlpages:
            print_verbose(1, "Render to png : page = " + str(it.page_num))
            # Render the HTMLPage to PNG and save it to the specified output directory
            it.render_to_png(remove_trailing_slash(base_dir), remove_trailing_slash(out_dir))

    def save_to_dir(self, out_dir):
        """
        Serializes parsed HTMLDirectory and saves further objects in special JSON and CSV files.

        Args:
            out_dir (str): Output directory to save data.

        Returns:
            None
        """
        # Iterate over HTML pages in the directory
        for it in self.htmlpages:
            # Print information about saving each HTML page to JSON and CSV
            print_verbose(1, "Save to JSON and CSV: page = " + str(it.page_num))

            # Save HTMLPage to a JSON file
            it.save_to_file(remove_trailing_slash(out_dir) + r'/jpage' + "{:05d}".format(it.page_num) + '.json')

            # Save all tables from the HTMLPage to a CSV file
            it.save_all_tables_to_csv(out_dir)

            # Save all footnotes from the HTMLPage to a text file
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
        # Remove trailing slash from HTML directory path
        html_dir = remove_trailing_slash(html_dir)

        # Create the full path using the provided wildcard
        pathname = html_dir + '/' + page_wildcard

        # Read the PDF filename from the info.txt file in the HTML directory
        self.read_pdf_filename(html_dir)

        # Iterate over JSON files that match the wildcard
        for file in glob(pathname):
            # Print information about loading each JSON file
            print_verbose(1, "LOADING JSON-FILE = " + str(file))

            # Load HTMLPage from the JSON file and append it to the list of HTML pages
            htmlpage = HTMLPage.load_from_file(file)
            self.htmlpages.append(htmlpage)
