import sys

if len(sys.argv) < 2 :
    print "please special the filename that maybe have BOM(SB Microsoft Files)";
    sys.exit(2);

filename = sys.argv[1];

content = open(filename, "r").read().encode("hex");
if "efbbbf" in content:
    print "Oh God!!, the file have stepped on the Microsoft shit";
    print "Cleaning it now!!"
    print "======================================================="
    print content
    content = content.replace("efbbbf","");
    content = content.replace("0d0a","0a");

open(filename+"_noBOM","w").write(content.decode('hex'));



