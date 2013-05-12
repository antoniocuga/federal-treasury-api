from datetime import datetime
import pandas as pd
import os
from collections import defaultdict
import types
import re

test_paths = [
    "11011400_t1.csv",
    "11102100_t2.csv",
    "11102100_t3.csv",
    "12080100_t4.csv",
    "11072000_t5.csv",
    "12042700_t6.csv",
    "12042700_t7.csv",
    "13020700_t8.csv"
]
root = "fms_parser_data/daily_csv/"
fps = [root+f for f in test_paths]

t1 = pd.read_csv(fps[0])
t2 = pd.read_csv(fps[1])
t3 = pd.read_csv(fps[2])
t4 = pd.read_csv(fps[3])
t5 = pd.read_csv(fps[4])
t6 = pd.read_csv(fps[5])
t7 = pd.read_csv(fps[6])
t8 = pd.read_csv(fps[7])

# TYPES
NUM = (int, long, float, complex)
STR = (str, unicode)
NONE = (types.NoneType)
DATE = (datetime)
SIMPLE = (int, long, float, complex, str, unicode, types.NoneType)

#
DATE_FORMAT = re.compile(r"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}")

def is_none(val):
    if isinstance(val, NONE) or val=="":
        return True
    else:
        False

def is_str(val):
    if isinstance(val, STR):
        return True
    else:
        return False

def is_num(val):
    if isinstance(val, NUM):
        return True
    else:
        return False

def is_date(val):
    if isinstance(val, DATE):
        return True
    elif isinstance(val, STR):
        if DATE_FORMAT.search(val):
            return True
        else:
            return False
    else:
        False

def is_bool(val):
    if val in [0,1]:
        return True
    elif val in[True, False]:
        return True
    else:
        return False

def test_table_name(val):
    if re.match("TABLE.*", val):
        return True
    else:
        return False

def is_wkdy(wkdy):

    WKDYS = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Satuday",
        "Sunday"
    ]

    if is_none(wkdy):
        return None
    elif wkdy.strip() in frozenset(WKDYS):
        return True
    else:
        return False

def test_text_field(text):
    if is_str(text):
        if re.match("[A-Za-z0-9_-: ]+", text):
            return True
        else:
            return False

def test_col_match(tab, expected):
    return all([True if c in frozenset(expected) else False for c in tab.keys()])

def apply_test(val, fx):
    return all([fx(v) for v in val if not is_none(v)])


def test_table_columns(tab, tab_index):

    T1_COLS = ['table', 'date', 'day', 'account', 'is_total', 'close_today', 'open_today', 'open_mo', 'open_fy', 'footnote']
    T23_COLS = ['table', 'date', 'day', 'account', 'type', 'subtype', 'item', 'is_total', 'today', 'mtd', 'fytd', 'footnote']
    T45_COLS = ['table', 'date', 'day', 'surtype', 'type', 'subtype', 'item', 'is_total', 'today', 'mtd', 'fytd', 'footnote']
    T6_COLS = ['table', 'date', 'day', 'type', 'item', 'is_total', 'close_today', 'open_today', 'open_mo', 'open_fy', 'footnote']
    T78_COLS = ['table', 'date', 'day', 'type', 'classification', 'is_total', 'today', 'mtd', 'fytd', 'footnote']

    # text indiviable tables for proper columns
    if tab_index=="t1":
        return test_col_match(tab, T1_COLS)
    elif tab_index in ["t2", "t3"]:
        return test_col_match(tab, T23_COLS)
    elif tab_index in ["t4", "t5"]:
        return test_col_match(tab, T45_COLS)
    elif tab_index=="t6":
        return test_col_match(tab, T6_COLS)
    elif tab_index in ["t7", "t8"]:
        return test_col_match(tab, T78_COLS)
    else:
        raise ValueError("tab index must be in \"t1\":\"t8\"")


def test_table(tab, tab_index):

    tests = []
    # test for cols:
    tests.append({tab_index+"_has_cols": test_table_columns(tab, tab_index)})

    for c in tab.keys():
        the_key = "%s_%s" % (tab_index, c)

        if c=="table":
            if tab_index=="t3":
                tests.append({the_key: None})
            else:
                tests.append({the_key: apply_test(tab[c], test_table_name)})

        elif c=="date":
            tests.append({the_key: apply_test(tab[c], is_date)})

        elif c=="open_today":
            tests.append({the_key: apply_test(tab[c], is_num)})

        elif c=="surtype":
            tests.append({the_key: apply_test(tab[c], is_str)})

        elif c=="account":
            tests.append({the_key: apply_test(tab[c], is_str)})

        elif c=="close_today":
            tests.append({the_key: apply_test(tab[c], is_num)})

        elif c=="classification":
            tests.append({the_key: apply_test(tab[c], is_str)})

        elif c=="item":
            tests.append({the_key: apply_test(tab[c], is_str)})

        elif c=="footnote":
            tests.append({the_key: apply_test(tab[c], is_str)})

        elif c=="open_fy":
            tests.append({the_key: apply_test(tab[c], is_num)})

        elif c=="open_mo":
            tests.append({the_key: apply_test(tab[c], is_num)})

        elif c=="subtype":
            tests.append({the_key: apply_test(tab[c], is_str)})

        elif c=="mtd":
            tests.append({the_key: apply_test(tab[c], is_num)})

        elif c=="mtd":
            tests.append({the_key: apply_test(tab[c], is_bool)})

        elif c=="day":
            tests.append({the_key: apply_test(tab[c], is_wkdy)})

        elif c=="type":
            tests.append({the_key: apply_test(tab[c], is_str)})

        elif c=="today":
            tests.append({the_key: apply_test(tab[c], is_num)})

        elif c=="fytd":
             tests.append({the_key: apply_test(tab[c], is_num)})

    return tests












