#!/usr/bin/env python3
"""각 SVG가 실제로 쓰는 글자만 손글씨 폰트에서 추려 인라인으로 심는다.

외부 폰트 로딩 없이 어디서 열어도 손글씨로 보이게 하려는 것.
사용: python3 embed_fonts.py <입력폴더> <출력폴더>
"""
import sys, os, re, base64, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "NanumPen.ttf")
PYFT = os.path.join(HERE, "fontenv", "bin", "pyftsubset")

def embed(svg_path, out_path):
    svg = open(svg_path, encoding="utf-8").read()
    chars = set()
    for m in re.findall(r'>([^<>]*)</text>', svg):
        chars.update(m)
    chars.discard("\n")
    txt = "".join(sorted(chars))

    with tempfile.TemporaryDirectory() as td:
        tf = os.path.join(td, "chars.txt")
        open(tf, "w", encoding="utf-8").write(txt)
        of = os.path.join(td, "sub.woff2")
        subprocess.run([PYFT, FONT, f"--text-file={tf}", f"--output-file={of}",
                        "--flavor=woff2", "--layout-features=", "--no-hinting",
                        "--desubroutinize"], check=True, capture_output=True)
        b64 = base64.b64encode(open(of, "rb").read()).decode()

    style = ("<defs><style>"
             "@font-face{font-family:'PenKR';font-style:normal;font-weight:400;"
             f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
             "text{font-family:'PenKR','Nanum Pen Script',-apple-system,sans-serif;}"
             "</style></defs>")
    svg = svg.replace("__HANDFONT__, ", "")
    i = svg.index(">") + 1
    svg = svg[:i] + style + svg[i:]
    open(out_path, "w", encoding="utf-8").write(svg)
    return len(chars), os.path.getsize(out_path)

if __name__ == "__main__":
    indir, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    total = 0
    for fn in sorted(os.listdir(indir)):
        if not fn.endswith(".svg"):
            continue
        n, size = embed(os.path.join(indir, fn), os.path.join(outdir, fn))
        total += size
        print(f"{fn:34s} {n:4d}자  {size/1024:6.1f} KB")
    print(f"{'합계':34s}        {total/1024:6.1f} KB")
