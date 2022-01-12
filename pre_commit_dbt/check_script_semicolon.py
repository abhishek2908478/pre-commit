import argparse
import os
from typing import IO
from typing import Optional
from typing import Sequence

from pre_commit_dbt.utils import add_filenames_args


def check_semicolon(filename,last_char, replace) -> int:
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
    with open(filename,"r+") as infile:
        if last_char == ";":
            if replace:
                print("inside replace")
                infile.seek(0)
                file = infile.read()
                print("before replace",file)
                file = file.replace(";","")
                infile.seek(0)
                infile.truncate()
                infile.write(file)
                print("after replace",file)
                status_code = 0
        infile.close()        
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
                if line.startswith(b"--"):
                    continue
                if line.startswith(b"/*"):
                    print("inside /* block")
                    default = False
                    continue
                if line.startswith(b"*/") or line.endswith(b"*/\r\n"):
                    print("inside */ block")
                    default = True
                    continue
                if default:
                    print("Inside Default Block")
                    lines.append(line)
                    
            file_obj.close()   
    
        print(lines)        
        chars = lines[-1].decode('UTF-8')
        last_char = chars[-1]
        print(last_char)
        status_code_file = check_semicolon(filename,last_char,replace=True)
        if status_code_file:
            print(
            f"{filename}: contains a semicolon at the end. "
            f"dbt does not support that."
            )
        status_code = status_code_file
    return status_code


if __name__ == "__main__":
    exit(main())
