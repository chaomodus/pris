from . import process_pris

def main():
    import sys
    result = process_pris.load(open(sys.argv[1]))
    for item in result:
        print item, '=', result[item]


if __name__ == '__main__':
    main()
