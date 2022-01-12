import argparse
import os
from typing import IO
from typing import Optional
from typing import Sequence

from pre_commit_dbt.utils import add_filenames_args


def check_semicolon(file_obj: IO[bytes],last_char, replace) -> int:
    # Test for newline at end of file
    # Empty files will throw IOError here
    status_code = 0
#     try:
#         file_obj.seek(-1, os.SEEK_END)
#     except OSError:
#         return status_code
#     last_character = file_obj.read(1)  # pragma: no mutate

#     while last_character in {b"\n", b"\r"}:  # pragma: no mutate
#         # Deal with the beginning of the file
#         if file_obj.tell() == 1:
#             return status_code

#         # Go back two bytes and read a character
#         file_obj.seek(-2, os.SEEK_CUR)
#         last_character = file_obj.read(1)  # pragma: no mutate

    # If last character is semicolon
    if last_char == b";":
        if replace:
            with open('file_obj', 'r') as infile,open('file_obj', 'w') as outfile:
                data = infile.read()
                data = data.replace(";", "")
                outfile.write(data)
                status_code = 1
    return status_code


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    add_filenames_args(parser)

    args = parser.parse_args(argv)
    status_code = 0
    
    for filename in args.filenames:
        # Read as binary so we can read byte-by-byte
        lines = []
        default = True
        with open(filename, "rb+") as file_obj:
            for line in file_obj:
                line = str(line)
                if line.startswith("--"):
                    continue
                if line.startswith("/*"):
                    print("inside /* block")
                    default = False
                    continue
                if line.startswith("*/") or line.endswith("*/"):
                    print("inside */ block")
                    default = True
                    continue
                if default:
                    print("Inside Default Block")
                    lines.append(line)
            print(lines)        
            chars = str(lines[-1])
            last_char = chars[-1]
            print(last_char)
            status_code_file = check_semicolon(file_obj,last_char,replace=True)
            if status_code_file:
                print(
                    f"{filename}: contains a semicolon at the end. "
                    f"dbt does not support that."
                )
                status_code = status_code_file

    return status_code


if __name__ == "__main__":
    exit(main())
