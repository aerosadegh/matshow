"""
MAT File Struct Show

Useing Two Methods to show structer
You Can Use it as MAT-File Diff

author: Sadegh
"""

import scipy.io as scio
import numpy as np
from io import StringIO
import scipy
import sys
import argparse

USE_MAT_TREE = False
MAT_TREE_USE_SAFE_CHAR = True   # if set to False, you can only run `python matdiff.py <file.mat>` to see output!


parser = argparse.ArgumentParser(description='Process some matfile.')
parser.add_argument('filename', metavar='matfile', type=str, help='mat for show mat structe.')
parser.add_argument('--output', '-o', dest="output", help='output to file')
parser.add_argument('--mat-tree', '-t', dest="tree", action="store_true", help='show tree instead default path')
parser.add_argument('--unsafe-char', '-s', dest="unsafe", action="store_true", help='use safe char (in tree mode!)')

args = parser.parse_args()
# print(parser.parse_args())

file = args.filename

if args.tree:
    USE_MAT_TREE = True
if args.unsafe and args.tree:
    MAT_TREE_USE_SAFE_CHAR = False



mm = scio.loadmat(file, struct_as_record=True)

keys = [key for key in mm if not key.startswith("__")]


if MAT_TREE_USE_SAFE_CHAR:
    c1, c2, c3, c4, c5 = "|-ILT"
    cc = "|---"
else:
    c1, c2, c3, c4, c5 = "╟━╨╙╥"
    cc = "╟━━"


def _last(line, ret_par=False):
    num = line[:line.find("->")].count(".")
    if ret_par:
        return line.split(".", num)
    else:
        return line.split(".", num)[-1]

def _rrepalce(sub, old, new):
    idx = sub.rfind(old)
    return sub[:idx] + sub[idx:].replace(old, new)


def mat_tree(ourstr):
    string = ourstr.split("\n")
    fstring = StringIO()
    tree = []
    printed_tree = [""]*10
    last_line = []

    for line in string:
        if "->" not in line:
            fstring.write(line+"\n")
            printed_tree[0] = line[:-2]
            printed_tree[1:] = [""]*10
            continue

        pp = _last(line, True)
        field = pp[-1]
        tree = pp[:-1]
        for i, c in enumerate(tree):
            if c not in printed_tree:
                last_line.append(f'{cc*i}{c5} {c}.\n')     # branch!
                
                if len(last_line)>1:
                    wtw = last_line.pop(0)
                    while wtw.count(c1)>last_line[0].count(c1):
                        wtw = _rrepalce(wtw, c1, c3)
                        
                    fstring.write(wtw)
                printed_tree[i] = c
                printed_tree[i+1:] = [""]*10
        
        
        last_line.append(f'{cc*(i+1)} {field.replace("-", c2, 1)}\n')   # val
        if len(last_line)>1:
            wtw = last_line.pop(0)
            while wtw.count(c1)>last_line[0].count(c1):
                wtw = _rrepalce(wtw, c1, c3)

            fstring.write(wtw)
    

    fstring.seek(len(fstring.getvalue())-1)
    last_line.append("")
    if len(last_line)>1:
        wtw = c4+last_line.pop(0)[1:]
        while wtw.count(c1)>last_line[0].count(c1):
            wtw = _rrepalce(wtw, c1, c3)
        fstring.write(wtw)
    else:
        fstring.write(last_line[0])

    return (fstring.getvalue())

    


def last(prfix):
    return prfix.split(".")[-1]

def remove_last(prfix):
    return prfix[:prfix.rfind(last(prfix))-1]

def clean(stp):
    return str(stp).replace("\n", "").replace("  ", " ").replace("  ", " ").replace("  ", " ")

def pretmat(struct, prefix="", level=0):
    dti = struct.dtype
    try:
        dti = list(dti.fields)
        if last(prefix) in dti:
            prefix = remove_last(prefix)

        for i, key in enumerate(struct):
            if key.dtype.fields:

                prefix2 = (prefix + f".{dti[i]}")
                pretmat(key, prefix=prefix2, level=level+1)
            else:

                prefix3 = (prefix+f".{dti[i]}")
                f.write(f"{prefix3}-> {clean(key)}"+"\n")
    except:
        pass

if args.output:
    fl = open(args.output, "w", encoding="utf8")
    writer = fl.write
else:
    writer = sys.stdout.write



for key in keys:
    f = StringIO("")
    f.write(f"{key}:>\n")
    pretmat(mm[key], prefix=key)
    if USE_MAT_TREE:
        writer(mat_tree(f.getvalue())+"\n")
    else:
        writer(f.getvalue()+"\n")

if args.output:
    fl.close()


