import os
import argparse
import pandas as pd
from PyPDF2 import PdfReader


def moveFromTo(current,destination):
    os.replace(current,destination)

def check_file(fullfile):
    with open(fullfile, 'rb') as f:
        try:
            pdf = PdfReader(f)
            info = pdf.metadata
            if info:
                return True
            else:
                return False
        except Exception as e:
            return False


def search_files(dirpath: str, corrupted_path:str) -> pd.DataFrame:
    pwdpath = os.path.dirname(os.path.realpath(__file__))
    print("Running path : %s" %pwdpath)
    files = []
    if os.access(dirpath, os.R_OK):
        print("Path %s validation OK \n" %dirpath)
        listfiles = os.listdir(dirpath)
        for f in listfiles:
            fullfile = os.path.join(dirpath, f)
            if check_file(fullfile):
                print("OK " + fullfile + "\n################")
                files.append((f, fullfile, 'good'))
            else:
                print("ERROR " + fullfile + "\n################")
                files.append((f, fullfile, 'corrupted'))
                destination = os.path.join(corrupted_path, f)
                moveFromTo(fullfile,destination)
    else:
        print("Path is not valid")

    df = pd.DataFrame(files, columns=['filename', 'fullpath', 'status'])
    return df


def main(args):
    save_as = os.path.join(args.output,'result.csv')
    print(save_as)
    df = search_files(args.dirpath,args.corruptedpath)
    df.to_csv(save_as,index = False)
    #df.to_csv(args.output, index=False)
    print(f'Final report saved to {args.dirpath}')

    print(df['status'].value_counts())

    


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--dirpath', type=str, required=True, help='Path to directory containing PDFs.')
    parser.add_argument('--output', type=str, required=True, help='Path to output CSV file.')
    parser.add_argument('--corruptedpath',type=str,required=True)
    args = parser.parse_args()
    main(args)
    print("Path is not valid")

