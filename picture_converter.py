#!/usr/bin/env python

import Image
import pickle


class DisplayImage(object):
    """Image that could be displayed on e-paper screen."""
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_hex(self, hex_list):
        """set_hex initialize image using hex image representation."""
        self.img_bin = "".join([format(x, '08b') for x in hex_list])

    def get_hex(self):
        """get_hex return hex representation of image."""
        data = list()

        for i in xrange(0, len(self.img_bin), 8):
            bin_chunk = self.img_bin[i:i+8]
            data.append(int(bin_chunk, 2))

        return data

    def set_bin(self, bin_list):
        """set_bin loda image from provided binary data."""
        self.img_bin = bin_list

    def get_bin(self):
        """get_bin return binary representation of image."""
        return self.img_bin

    def show(self):
        """Show image preview (not on target device)."""
        img = Image.new('RGB', (self.width, self.height), "white")
        pixels = img.load()

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                color = int(self.img_bin[self.height*i + j]) * 255
                pixels[i, j] = (color, color, color)

        img.show()

    def _gamma(self, input, G):
        import math

        return int(
            math.pow(
                float(input)/255.0,
                1.0/G
            ) * 255)

    def load_file(self, filename, threshold=10):
        """Load image from image file."""
        img = Image.open(filename)
        data = list()

        if img.size[0] > 296 or img.size[1] > 128:
            img = img.resize((296, 128), Image.ANTIALIAS)

        self.width = img.size[0]
        self.height = img.size[1]

        pixels = img.load()
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                color = sum(pixels[i, j])/len(pixels[i, j])  # average RGB chan
                if color > threshold:
                    color = 1
                else:
                    color = 0
                data.append(str(color))

        self.img_bin = "".join(data)


def usage():
    """Display usage if not all parameters provided."""
    from sys import argv, exit

    if len(argv) < 3:
        print "USAGE: %s <INPUT_FILE.PNG> <OUTPUT_FILE.DAT>" % argv[0]
        exit(0)

    return(argv[1], argv[2])


def main():
    """Read from image file and export Pickle."""
    from optparse import OptionParser
    parser = OptionParser()
    help = "Input image (.png, .jpeg, ...) filename."
    parser.add_option("-i", "--input", dest="input_filename", help=help,
                      default="img/lena.png")
    help = "Ouput filename for Pickle representation."
    parser.add_option("-o", "--output", dest="output_filename", help=help,
                      default="lena.hex")
    (options, args) = parser.parse_args()

    print "Reading file '%s' ..." % options.input_filename
    d = DisplayImage(296, 128)
    d.load_file(options.input_filename, 80)
    d.show()

    print "Saving file '%s'" % options.output_filename
    data_list = d.get_hex()
    with open(options.output_filename, "wb") as f:
        pickle.dump(data_list, f)


def test_fonts():
    """Display 3 letters from Font1206 contained in EPD_driver."""
    Font1206 = [
        [0x00, 0x40, 0x07, 0xC0, 0x39, 0x00, 0x0F, 0x00, 0x01, 0xC0, 0x00, 0x40],  #"A", 33*/
        [0x20, 0x40, 0x3F, 0xC0, 0x24, 0x40, 0x24, 0x40, 0x1B, 0x80, 0x00, 0x00],  #"B", 34*/
        [0x1F, 0x80, 0x20, 0x40, 0x20, 0x40, 0x20, 0x40, 0x30, 0x80, 0x00, 0x00]  #"C",35*/
    ]

    for char in Font1206:
        d = DisplayImage(6, 16)
        d.set_hex(char)
        d.show()


if __name__ == "__main__":
    main()
