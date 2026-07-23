import sys
from pathlib import Path

# 把服务根目录加入 Python 模块搜索路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
