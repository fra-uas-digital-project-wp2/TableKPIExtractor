# ============================================================================================================================
# PDF_Analyzer
# File   : DataImportExport.py
# Author : Ismail Demir (G124272)
# Date   : 05.08.2020
# ============================================================================================================================
import config_for_rb
from Format_Analyzer import Format_Analyzer
import glob
from globals import remove_trailing_slash, print_verbose, file_exists
import jsonpickle
import shutil


class DataImportExport:

    @staticmethod
    def import_files(src_folder, dst_folder, file_list, file_type):
        def ext(f):
            res = [f]
            res.extend(Format_Analyzer.extract_file_path(f))
            return res

        # print(src_folder)
        file_paths = glob.glob(src_folder + '/**/*.' + file_type, recursive=True)
        file_paths = [ext(f.replace('\\', '/')) for f in file_paths]  # unixize all file paths

        res = []

        info_file_contents = {}

        for fname in file_list:
            fname_clean = fname.lower().strip()  # (new)
            if fname_clean[-4:] == '.' + file_type:
                fname_clean = fname_clean[:-4]

            fpath = None

            # look case-sensitive
            for f in file_paths:
                if f[2] + '.' + f[3] == fname:
                    # match!
                    fpath = f
                    break

            # look case-insensitive
            if fpath is None:
                for f in file_paths:
                    if f[2].lower() == fname_clean:
                        # match!
                        fpath = f
                        break

            # print('SRC: "' + fname + '" -> ' + str(fpath))
            new_file_name = None
            if fpath is None:
                print_verbose(0, 'Warning: "' + fname + '" not found.')
            else:
                new_file_name = Format_Analyzer.cleanup_filename(fpath[2] + '.' + fpath[3])
                new_file_path = remove_trailing_slash(dst_folder) + '/' + new_file_name
                info_file_contents[new_file_path] = fpath[0]

                if not file_exists(new_file_path):
                    print_verbose(1, 'Copy "' + fpath[0] + '" to "' + new_file_path + '"')
                    shutil.copyfile(fpath[0], new_file_path)

            res.append((fname, new_file_name))

        # print(info_file_contents)

        # save info file contents:
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
        data = jsonpickle.encode(info_file_contents)
        f_info = open(remove_trailing_slash(config_for_rb.global_working_folder) + '/info.json', "w")
        f_info.write(data)
        f_info.close()

        return res

    @staticmethod
    def load_path_files_from_json_file(json_file):
        """
        Load the paths of the files from a JSON file.

        Args:
            json_file (str): Path to the JSON file.

        Returns:
            json_data: The loaded object.
        """
        with open(json_file, "r") as file:
            data = file.read()
        json_data = jsonpickle.decode(data)
        return json_data

    @staticmethod
    def save_path_files_to_json_file(file_paths):
        """
        Saves paths of the files to a JSON file named 'info.json'.

        Args:
            file_paths (list): A list of file paths.

        Returns:
            None
        """
        info_file_contents = {}

        for file_info in file_paths:
            # save paths of the files to info_file_contents:
            # example: "raw_pdf/example.pdf": "raw_pdf/example.pdf"
            info_file_contents[file_info[0]] = file_info[0]

        # Set up jsonpickle options for encoding
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)

        # Encode the info_file_contents dictionary into JSON format
        json_data = jsonpickle.encode(info_file_contents)

        # Construct the file path for the 'info.json' file
        info_file_path = remove_trailing_slash(config_for_rb.global_working_folder) + '/info.json'

        # Write the JSON data to the 'info.json' file
        with open(info_file_path, "w") as info_file:
            info_file.write(json_data)
