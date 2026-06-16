#!/usr/bin/env python3
import re
import sys
import subprocess

def fix_imports(content: str) -> str:
    return re.sub(r'^from \.utils', 'from utils', content, flags=re.MULTILINE)

def fix_syntax(content: str) -> str:
    try:
        compile(content, "tmp.py", "exec")
        return content
    except SyntaxError as e:
        line = e.lineno - 1
        lines = content.splitlines()
        if len(lines) > line and "==" in lines[line] and "=" in lines[line]:
            lines[line] = lines[line].replace("= =", "==")
            return "\n".join(lines)
        return content

if __name__ == "__main__":
    path = sys.argv[1]
    with open(path, "r", encoding="utf‑8") as f:
        txt = f.read()
    fixed = fix_syntax(fix_imports(txt))
    if fixed != txt:
        with open(path, "w", encoding="utf‑8") as f:
            f.write(fixed)
        print(f"✅ Fixed: {path}")
        sys.exit(0)
    sys.exit(1)
