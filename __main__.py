import argparse
import obfuscator
import json
import sys
import stringencoder
import os
import time


rec_version = (3, 4, 3)
cur_version = sys.version_info

if cur_version < rec_version:
    print("WARNING!!! Your Python version is older than 3.4.3")
    print("The obfuscator may not work correctly!")


VERSION = "Beta 1.0.3"
VERSION_DATE = time.strftime("%b %d, %Y @ %I:%M %p", time.localtime(os.path.getmtime(__file__)))

print("Version: {0} (Updated on {1})".format(VERSION, VERSION_DATE))



in_file = "input.lua"
out_file = "output.lua"
global_file = "globals.json"
dontcopy = False
debug_mode = False


parser = argparse.ArgumentParser()
parser.add_argument('--input',
                    help='The input file path',
                    default=in_file)
parser.add_argument('--output',
                    help='The output file path',
                    default=out_file)
parser.add_argument("--level",
                    help='0 = original strings, 1 = small file, 2 = large file, 3 = huge file',
                    default=1)
parser.add_argument("--dontcopy",
                    help='Disable copying the output',
                    action='store_true')
parser.add_argument("--debug",
                    help="Enable debug mode",
                    action='store_true')
args = parser.parse_args()


in_file = args.input
out_file = args.output
encoder = stringencoder.get_by_level(int(args.level))
dontcopy = args.dontcopy
debug_mode = args.debug


lua = None
decrypt = None
globs = None


try:
    with open(in_file, "rb") as f:
        lua = f.read().decode("utf-8")

    with open(global_file, "r") as f:
        globs = json.loads(f.read())


    # Do the obfuscation
    lua, tokens, strings, comments = obfuscator.obfuscate(lua, encoder, globs, debug_mode)

except:
    if not debug_mode:
        print("Fatal error occurred.")
        exit(0)
    else:
        raise


if not dontcopy:
    try:
        import pyperclip
        pyperclip.copy(lua)
        print("Code copied to clipboard.")
    except:
        pass


# Write the results
with open(out_file, "wb") as f:
    f.write(lua.encode("utf-8"))