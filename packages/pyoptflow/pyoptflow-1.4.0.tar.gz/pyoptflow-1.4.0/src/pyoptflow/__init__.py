from pathlib import Path

from .hornschunck import HornSchunck
from .lucaskanade import LucasKanade, getPOI, gaussianWeight


def getimgfiles(stem: Path, pat: str) -> list:

    stem = Path(stem).expanduser()

    print("searching", stem / pat)

    flist = sorted([f for f in stem.glob(pat) if f.is_file()])

    if not flist:
        raise FileNotFoundError(f"no files found under {stem} using {pat}")

    return flist
