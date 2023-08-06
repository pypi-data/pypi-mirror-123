from pathlib import Path

for path in Path('.').rglob('*.py'):
    ll = open(path).readlines()
    for l in ll:
        if l.find("import") != -1:
            if l.find("PyAstronomy") != -1:
                continue
            if l.find("numpy") != -1:
                continue    
            if l.find("six") != -1:
                continue
            if l.find("gzip") != -1:
                continue            
            if l.find("__future__") != -1:
                continue
            if l.find("from .") != -1:
                continue
            if l.find("#") != -1:
                continue
            if l.find("import os") != -1:
                continue
            if l.find("matplotlib") != -1:
                continue
            if l.find("datetime") != -1:
                continue
            if l.find("scipy") != -1:
                continue
            
            print(l, end="")
