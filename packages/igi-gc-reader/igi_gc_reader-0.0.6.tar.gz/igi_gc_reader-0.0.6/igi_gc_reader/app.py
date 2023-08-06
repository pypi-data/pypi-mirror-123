"""
Transform a GC lab Excel file to a format ready for p:IGI+/Metis import. 
"""
from igi_gc_reader.status import TransformationResult, Status, SuccessStatus
from typing import List
from collections import defaultdict
from argparse import ArgumentParser

from igi_gc_reader.reader.classification import GcFileClass
from igi_gc_reader.reader.gc_reader import IGcSheet, get_gc_sheets
from igi_gc_reader.writer import write_sheets
from igi_gc_reader.utils import gc_logger

SUPPORTED_FILE_CLASSES = [GcFileClass.One]
UNASSIGNED_OUT_PATH = "<AutoAssign>"


def try_transform_file(in_path: str, out_path: str = UNASSIGNED_OUT_PATH) -> TransformationResult:
    """
    Transform GC lab file ready for p:IGI+/Transform import.str
    Returns: path to transformed file
    """
    try:
        if out_path == UNASSIGNED_OUT_PATH:
            out_path = in_path.replace('.xls', '_transformed.xls')  # works for 'xls' or 'xlsx'
            if out_path.endswith('.xls'):
                out_path = out_path.replace('.xls', '.xlsx')

        supported_sheets = get_supported_sheets(in_path)
        if len(supported_sheets) == 0:  # if all sheets are not supported file class...
            return TransformationResult(Status(success=False, only_unsupported_sheets=True))
        write_sheets(supported_sheets, out_path)
    except Exception as e:  # could have a supported file class but still hit an error....
        result = TransformationResult(Status(success=False, 
                                             only_unsupported_sheets=False, 
                                             igi_exception=e))
        gc_logger.error(result.status.failure_message)
        return result
    result = TransformationResult(SuccessStatus, output_filepath=out_path)
    gc_logger.info(result)
    return result


def transform_file(in_path: str, out_path: str = UNASSIGNED_OUT_PATH) -> str:
    """
    Transform GC lab file ready for p:IGI+/Transform import.str
    Returns: path to transformed file
    """
    if out_path == UNASSIGNED_OUT_PATH:
        out_path = in_path.replace('.xls', '_transformed.xls')  # works for 'xls' or 'xlsx'
        if out_path.endswith('.xls'):
            out_path = out_path.replace('.xls', '.xlsx')
    write_sheets(get_supported_sheets(in_path), out_path)
    return out_path


def pick_and_transform_file() -> str:
    """
    Command line option to open file picker to select input file. 
    Can also be used if you are using this lib within a Python script. 
    For use in a web service use `transform_file` instead.
    """
    import tkinter.filedialog
    import tkinter as tk
    root = tk.Tk()   # to allow file selection dialog
    root.withdraw()  # hide root window 
    input_path = tk.filedialog.askopenfilename(title="Select GC lab file (Excel)",
                                               filetypes=[("Excel files", ".xlsx .xls .xls*")])
    return transform_file(input_path)


def get_supported_sheets(in_path: str) -> List[IGcSheet]:
    sheets_by_file_class = defaultdict(list)
    
    for sheet in get_gc_sheets(in_path):
        sheets_by_file_class[sheet.file_class].append(sheet)

    supported, unsupported = [], []
    for file_class in sheets_by_file_class.keys():  # i.e. if it's in supported classes
        if file_class in SUPPORTED_FILE_CLASSES:
            supported += sheets_by_file_class[file_class]
        else:
            unsupported += sheets_by_file_class[file_class]

    if len(supported) >= 1:
        if len(unsupported) == 0:
            names = [sh.sheet_name for sh in unsupported]
            gc_logger.info(f"Some unsupported sheets found: {names}")
        return supported
    return []


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-i", dest="input_file_path", type=str, required=False, default="")
    parser.add_argument("-t", dest="use_try_func", type=str, required=False, default="n")
    args = parser.parse_args()
    if not args.input_file_path:
        pick_and_transform_file() 
    else:
        if args.use_try_func.lower()[0] != 'n':
            try_transform_file(args.input_file_path)
        else:
            transform_file(args.input_file_path)
