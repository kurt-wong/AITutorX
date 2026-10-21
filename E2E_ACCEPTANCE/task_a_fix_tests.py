from pathlib import Path
p = Path(r"D:\Project\AITutors-v3\backend\tests\test_task_a_option_content_span.py")
s = p.read_text(encoding="utf-8")
s = s.replace('"unit_type": "standalone_question"', '"unit_type": "standalone_unit"')
s = s.replace(
    '''                "stem": {"question_label": qn},
                "options": [{"label": x} for x in "ABCD"],
                "answer": {"answer_zone": "inline_answer", "question_label": qn},''',
    '''                "stem": {"role": "stem", "question_label": qn},
                "options": [{"role": "option", "label": x} for x in "ABCD"],
                "answer": {"role": "answer", "answer_zone": "inline_answer", "question_label": qn},''',
)
p.write_text(s, encoding="utf-8")
print("patched payload")
