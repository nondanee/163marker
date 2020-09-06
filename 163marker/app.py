# -*- coding: utf-8 -*-
import argparse, traceback
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __package__ is None:
    from core import *
else:
    from .core import *

parser = argparse.ArgumentParser(prog = '163marker')
parser.add_argument('file', metavar = 'file', help = 'audio file path (MP3/FLAC)')
parser.add_argument('uri', metavar = 'uri', nargs = '?', help = 'meta data source (URL/PATH)')
parser.add_argument('id', metavar = 'id', nargs = '?', help = 'specific song id')

def main():
    args = parser.parse_args()
    try:
        if args.uri is not None:
            mark(args.file, parse(args.uri), args.id)
        else:
            print(json.dumps(extract(args.file), ensure_ascii = False, indent = 4))
    except:
        traceback.print_exc()

if __name__ == '__main__':
    main()