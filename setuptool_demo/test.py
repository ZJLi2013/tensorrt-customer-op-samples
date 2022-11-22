
import sys

if len(sys.argv) >= 1 and  sys.argv[1] == "local_build":
    import os 
    lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build/lib.linux-x86_64-3.8")
    sys.path.append(lib_path)
from cppextension import add
print(add(3, 5))
