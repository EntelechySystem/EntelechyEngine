## 导入第三方包（#NOTE 动态使用，严禁删除。如果 IDE 显示没有被使用，是正常的。因为这个是在其他文件内被导入使用的）
import platform
import sys
import os
import csv
import glob
import shutil
import warnings
import re
from pathlib import Path, PurePath
import importlib
import pkgutil
from openpyxl import load_workbook
from dataclasses import dataclass
import itertools
from enum import Enum
import time
import datetime
import numpy as np
import pandas as pd
from pandas import DataFrame
from copy import deepcopy, copy
from dataclasses import dataclass
import logging
import pickle
from typing import Union, Any, Optional
from functools import reduce
import random
import string
import locale
import subprocess
import base64
from multiprocessing import Pool
import multiprocessing
import warnings
import matplotlib.pyplot as plt
import noise
import random
import ast
import builtins
# import cv2
# import scipy

## NOTE 以下是绘图用的。如果不需要，可以注释掉。但是请先不要删除！因为目前开发期间，需要作为参考。后续可以删除。
# if sgv['need_visualization']:
#     import igraph as ig
#     import matplotlib.pyplot as plt
#     import drawsvg as dw
#     import fitz
#     from svglib.svglib import svg2rlg
#     from reportlab.graphics import renderPDF
#     from reportlab.pdfbase.ttfonts import TTFont
#     from reportlab.pdfbase import pdfmetrics
#     import matplotlib.font_manager as fm
#     from matplotlib.font_manager import FontProperties
