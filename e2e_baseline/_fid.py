import fitz, sys
p = r"D:\Project\Papers\maintainess\PDF\2012-2021高考真题生物汇编：基因工程（1）（教师版）(1).pdf"
d = fitz.open(p)
parts=[]
for pg in d:
    parts.append(pg.get_text())
t = "\n".join(parts)
print("pages=%d chars=%d lines=%d" % (len(d), len(t), t.count("\n")+1))
for k in ["基因工程","限制酶","电泳","选择题"]:
    print("  '%s' -> %s" % (k, t.find(k)))
print("head:", t[:120].replace("\n"," | "))
