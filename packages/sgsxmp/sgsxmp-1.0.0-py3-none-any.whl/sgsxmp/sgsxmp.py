from libxmp import XMPFiles
from libxmp import consts
import sys


def main():
    args = sys.argv[1:]
    print(args)
    data = {
        'filepath': args[0],
        'fcdfilename': args[1]
    }

    xmpfile = XMPFiles(file_path=data['filepath'], open_forupdate=True)
    xmp = xmpfile.get_xmp()

    for key, value in data.items():
        xmp.set_property(consts.XMP_NS_XMP, key, value)

    print(xmp)

    if xmpfile.can_put_xmp(xmp):
        xmpfile.put_xmp(xmp)
        xmpfile.close_file()
    else:
        xmpfile.close_file()


