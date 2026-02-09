import sys
import os

# 1. Dapatkan lokasi absolut dari folder 'src'
src_path = os.path.join(os.path.dirname(__file__), 'src')

# 2. Masukkan folder 'src' ke dalam daftar pencarian Python (sys.path)
if src_path not in sys.path:
    sys.path.append(src_path)

# 3. Sekarang baru panggil aplikasi utamamu
from src.app import *