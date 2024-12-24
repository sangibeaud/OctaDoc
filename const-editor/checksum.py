import sys

def compute(filename="./bankfile.bin"):
    add = 0
    with open(filename, "rb") as f:
        ## Read first 2 bytes of data
        while True:
            byte = f.read(2)
            if not byte:
                break
            add ^= int.from_bytes(byte, byteorder='big')
        print(b'%02X' % add )
        print(b'%02X' % (~add & 0xFFFF))


if __name__=='__main__':
    
    if len(sys.argv) == 1:
        compute()
    else:
        compute(filename=sys.argv[1])

