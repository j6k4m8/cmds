"""
Resume-File Unborker
Jordan Matelsky (github.com/j6k4m8)

Does a pretty decent job of guessing resume file extensions if they've
been removed from a file collection.

Usage:

    python guess_ext.py operator path/to/badfiles path/to/results

Operator can be either `mv` or `cp`, depending on if you want the
results to be copied or moved.

For instance, with a dir `badfiles`, run:

    mkdir goodfiles
    python guess_ext.py cp badfiles goodfiles

This will COPY the files to goodfiles, appending them with extensions.

"""


import sys
import glob
import subprocess

if len(sys.argv) != 4:
    raise ValueError("Usage: python guess_ext.py operator src/ target/")

op, src, tgt = sys.argv[1], sys.argv[2].rstrip('/'), sys.argv[3].rstrip('/')

if op not in ['mv', 'cp']:
    raise ValueError("Operator must be 'mv' or 'cp'.")

for f in glob.glob("{}/*".format(src)):
    bashCommand = "file {}".format(f)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    if "Microsoft Word 2007+" in output:
        ext = "docx"
    elif "PDF document" in output:
        ext = "pdf"
    elif "ASCII text" in output:
        ext = "txt"
    elif "Word" in output:
        ext = "doc"
    else:
        ext = "unknown"
    f = f[len(src) + 1:]
    cmd = "{} {}/{} {}/{}.{}".format(op, src, f, tgt, f, ext)
    process = subprocess.Popen(cmd.split())
