import wx
import construct as cs
import this
from construct_editor.wx_widgets import WxConstructHexEditor


def printobj(obj, ctx):
    print(obj)

constr = cs.Struct(
    "a" / cs.Int16sb,
    "b" / cs.Int16sb,
)


DPSHdr=cs.Struct(
#    "HDR" / cs.Array(4,cs.Byte),
    "FORM" / cs.PaddedString(4,"utf8"),
    "tail" / cs.Array(4,cs.Byte),
    "DPS1BANK" / cs.PaddedString(8,"utf8"),
    "tail2" / cs.Array(5,cs.Byte),
    "DPSV" / cs.Byte, #Bankfile version, only 23 (0x17) works
)

PTRNHdr=cs.Struct(
#    "HDR" / cs.Array(4,cs.Byte),
    "PTRN" / cs.PaddedString(4,"utf8"),
    "UNK0" / cs.Array(4,cs.Const(b"\x00")),
    #"tail" / cs.Array(4,cs.Byte)
)

Atrack=cs.Struct(
    'ATRA' / cs.Const(b"TRAC\x00\x00\x00\x00"),
    'ANTNM' / cs.Byte * printobj,               #audio number 
    "UNK0" / cs.Array(64,cs.Const(b"\x00")),
    #cs.Probe(this.UNK0),
    cs.Probe(lookahead=32),
    "UNK1" / cs.Array(8,cs.Const(b"\xAA")),
    "UNK2" / cs.Bytes(16),
    'UNK21' / cs.Const(b"\x00"),
    #"TRAC" / cs.PaddedString(4,"utf8"),
    "data" / cs.Array(0x8c0,cs.Byte),
    #'TAIL' / cs.GreedyBytes,  #2176 -128
)

Mtrack=cs.Struct(
#    "MTRA" / cs.PaddedString(4,"utf8"),
    'MTRA' / cs.Const(b"MTRA\x00\x00\x00\x00"),
    'NTNM' / cs.Byte * printobj,               #MIDI track number 
    "UNK60" / cs.Array(24,cs.Const(b"\x00")),
    "UNK61" / cs.Array(8,cs.Const(b"\xAA")),
    "UNK62" / cs.Bytes(16),
    "UNK63" / cs.Array(2048,cs.Const(b"\xff")),
    #"UNK4" / cs.Array(128,cs.Const(b"\x00")),
    "UNK64" / cs.Array(128,cs.Byte),
    #'TAIL' / cs.GreedyBytes,  #2176 -128
)

Pattern= cs.Struct(
        "HDR" / PTRNHdr,
        "ATracks" / cs.Array(8,Atrack),
        "MTracks" / cs.Array(8,Mtrack),
        'extra' / cs.Array(12,cs.Byte) * printobj, 
        )

PartNames= cs.Struct(
    'P1name' / cs.PaddedString(7,"utf8") * printobj,
    'P2name' / cs.PaddedString(7,"utf8") * printobj,
    'P3name' / cs.PaddedString(7,"utf8") * printobj,
    'P4name' / cs.PaddedString(7,"utf8") * printobj,
)



Part= cs.Struct(
    'PART' / cs.Const(b"PART\x00\x00\x00\x00"),
    'PNUM' / cs.Byte * printobj, 
    'FOURS' / cs.Bytes(8),
    'EIGHTS' / cs.Bytes(8),
    'UNK01' / cs.Const(b"\x00\x08"),
    'SIXCs' / cs.Bytes(16),
    'UNK03' / cs.Array(8,cs.Const(b"\x00")),
    'UNK04' / cs.Array(1,
        cs.Struct(
            "UNK11" / cs.Array(8,cs.Bytes(30)),
            "UNK12" / cs.Array(8,cs.Bytes(24)),
            "UNK13" / cs.Array(8,cs.Bytes(30)),
            "UNK131" / cs.Bytes(40),
            "UNK14" / cs.Array(8,cs.Bytes(30)),
            "UNK15" / cs.Array(8,cs.Bytes(32)),
            #"UNK151" / cs.Bytes(16),
            "UNK16" / cs.Array(8,cs.Bytes(36)),
            "UNK17" / cs.Array(8,cs.Bytes(12)),
        ),
    #'UNK20' / cs.Array(42,cs.Const(b"\xff")), #4256
    #'UNK21' / cs.Array(58,cs.Const(b"\x00")),
    
    ),
    'UNK20' / cs.Array(4256,cs.Const(b"\xff")), #4256
    'UNK21' / cs.Array(288,cs.Const(b"\x00")), #288
    'UNK23' / cs.Array(16,cs.Const(b"\xff")), #16
    'UNK24' / cs.Array(128,cs.Const(b"\x00")), #128
    #'Trailing' / cs.GreedyBytes,
)


Parts= cs.Struct(
    'saved' / cs.Array(4,Part),
    'current' / cs.Array(4,Part),

    'UNK43' / cs.Array(5,cs.Const(b"\x00")),
    'names' / PartNames,
    )


CRC= cs.Bytes(4)



bankfile=cs.Struct(
    "Header" / DPSHdr,
    'Patterns' / cs.Array(16,Pattern),
    #'next' / cs.Array(2,cs.Byte),
    #'filler' / cs.Bytes(48),
    'Parts' / Parts,
    'filler' / cs.Bytes(2),
#    'CRC' / CRC,
#    'Trailing' / cs.GreedyBytes,
)




def usage():
    """Basic helper function"""
    print("""
         Visualize a binary file according to Struct""")


import getopt, sys

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:vs:i:", ["help", "output=","struct=","input="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    format=bankfile

    output = None
    verbose = False
    filename='bank01.strd'

    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-s", "--struct"):
            format = eval(a)
        elif o in ("-i", "--input"):
            filename = a
        else:
            assert False, "unhandled option"
    # ...

#b = bytes([0x12, 0x34, 0x56, 0x78])
#fileName='bank01.strd'


    with open(filename, mode='rb') as file: # b is important -> binary
        fileContent = file.read()

    format.parse(fileContent)
    print('parsed !')

    if verbose == True :
        app = wx.App(False)
        frame = wx.Frame(None, title="Construct Hex Editor", size=(800, 1000))
        #editor_panel = WxConstructHexEditor(frame, construct=constr, binary=b)
        editor_panel = WxConstructHexEditor(frame, construct=format, binary=fileContent)
        editor_panel.construct_editor.expand_all()
        frame.Show(True)
        app.MainLoop()

if __name__ == "__main__":
    main()
