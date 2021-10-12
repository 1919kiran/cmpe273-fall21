import binascii


def encode(x):
    crc = '%08X' % (binascii.crc32(bytes(x, 'utf-8')) & 0xffffffff)
    return crc


