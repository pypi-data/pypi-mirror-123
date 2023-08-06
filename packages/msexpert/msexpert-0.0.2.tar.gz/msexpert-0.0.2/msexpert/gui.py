#!python
import sys
import os
from streamlit import cli as stcli


_this_file = os.path.abspath(__file__)
_this_directory = os.path.dirname(_this_file)

def run():

    file_path = os.path.join(_this_directory, 'app.py')
    sys.argv = ["streamlit", "run", file_path]
    sys.exit(stcli.main())