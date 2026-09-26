import fitz, hashlib, io, sys
out = io.StringIO()
pdf = r"D:\Project\Papers\maintainess\PDF\2012-2021高考真题生物汇编：基因工程（1）（教师版）(1).pdf"
v3  = r"D:\Project\AITutor-X\e2e_baseline\v3_body_text.txt"
d = fitz.open(pdf)
pages = [pg.get_text() for pg in d]
variants = {
  'join_nl'   : "\n".join(pages),
  'join_empty': "".join(pages),
  'join_nlnl' : "\n\n".join(pages),
}
bt = open(v3, encoding='utf-8').read()
print("pdf_pages=%d  pdf_chars=%d" % (len(d), sum(len(p) for p in pages)))
print("v3_body_text chars=%d  sha256=%s" % (len(bt), hashlib.sha256(bt.encode()).hexdigest()))
print("expected body_hash = 6526b8900d17706b804cb4c6080780be3628ab9776282838b3d22cd6bee4245f")
for k,v in variants.items():
    print("  variant %-11s chars=%-7d sha256=%s  MATCH=%s" % (k, len(v), hashlib.sha256(v.encode()).hexdigest()[:16], hashlib.sha256(v.encode()).hexdigest()==hashlib.sha256(bt.encode()).hexdigest()))
# longest common prefix between v3 and the newline join
a, b = bt, variants['join_nl']
n = 0
while n < min(len(a), len(b)) and a[n] == b[n]:
    n += 1
print("common_prefix_len=%d (of v3=%d, joinnl=%d)" % (n, len(a), len(b)))
print("v3_head_repr=%r" % bt[:80])
print("pdf_head_repr=%r" % b[:80])
