import gzip
import os
import sys

from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path


# additional command descriptions for help text
EPILOG = """command list:
  compress      Compress .blend file using gzip and create .blend.gz file
  uncompress    Uncompress .blend.gz file using gzip and create .blend file
  install       Setup pre-commit hook for automatic compression before committing.
"""

parser = ArgumentParser(description='Tools for stylized-blender-setup', formatter_class=RawTextHelpFormatter, epilog=EPILOG)
parser.add_argument('command', type=str, choices=['compress', 'uncompress', 'install'], help='Determines type of operation. See command list below.', metavar="command")
parser.add_argument("file", type=Path, help="Path to target file")


BLEND_FILENAME = "stylized-blender-setup.blend"
GZIP_COMPRESSLEVEL = 9 # highest and slowest compression

def compress_blend_file(path):
    """ write a gzip-compressed file and append ".gz" to the filename """
    with open(path, "rb") as f:
        content = f.read()

    # append ".gz" original suffix of path
    path = path.with_suffix(path.suffix + ".gz")

    with gzip.open(path, "wb", compresslevel=GZIP_COMPRESSLEVEL) as f:
        f.write(content)

def uncompress_blend_file(path):
    """ uncompress a file and write output to a file, delete ".gz" from suffix """
    with gzip.open(path, "rb") as f:
        content = f.read()

    # remove ".gz" from suffix of path
    if path.suffix == ".gz":
        path = path.with_suffix("")
    
    with open(path, "wb") as f:
        f.write(content)

def install_hook():
    """ attempt to install a pre-commit hook that executes this script """
    pass

def main():
    args = parser.parse_args()

    if args.command == "install":
        install_hook()
        sys.exit(0)
 
    try:
        if args.command == "compress":
            compress_blend_file(args.file)
        elif args.command == "uncompress":
            uncompress_blend_file(args.file)
    except:
        print("File not found")
        sys.exit(1)
 

if __name__ == "__main__":
    main()
