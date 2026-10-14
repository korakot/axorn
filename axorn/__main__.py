"""python3 -m axorn thai < roman.txt > thai.txt   (or: roman)"""
import sys
from . import roman_to_thai, thai_to_roman

f = {"thai": roman_to_thai, "roman": thai_to_roman}[sys.argv[1]]
sys.stdout.write(f(sys.stdin.read()))
