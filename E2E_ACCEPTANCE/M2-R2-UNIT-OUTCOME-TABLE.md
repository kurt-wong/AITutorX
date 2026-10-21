# M2-R2 逐单元结局表（40 Producer units）

包：`chem-2018-spring-huikao-teacher`  
Annotation：`c38ee1ab-3543-41ad-ad1b-f035f029e2fa`  
SourceVersion：`0df40d7b-183d-4bb1-8b06-1b4d44dce9b7`（preprocessing/canonical_l1, 584 lines）  
生成：有界补跑诊断（同一 annotation + 同一 sealed 行）+ 库内候选/题目主键。

## 汇总

- 总单元：40；已成 Question：21；Candidate pending_review：3；无 Candidate：16

- 未进入 Question：19 （= 3 pending + 16 无 Candidate）

- 语义就绪复现（有界补跑 IR.semantic_status=ready）：24 = 与 M2-R2 Candidate 集合一致


## 逐单元结局

| unit_id | 原卷题号 | 源行区间(stem/options/answer) | Annotation | Candidate | Candidate ID | Gate/Admission | 最终阶段 | 失败/跳过原因 | 证据 |
|---|---|---|---|---|---|---|---|---|---|
| Q1 | 1 | [14, 14]/[16, 16]/[513, 513] | 是 | approved | `acf9c34e` | approve→物化 | Question+Instance | — | Q=47c22b00… I=e01e4dc6… db_qn=1 |
| Q2 | 2 | [18, 18]/[20, 20]/[513, 513] | 是 | approved | `02870df5` | approve→物化 | Question+Instance | — | Q=3332aaa6… I=ace003ae… db_qn=2 |
| Q3 | 3 | [22, 22]/[24, 24]/[513, 513] | 是 | approved | `0581e034` | approve→物化 | Question+Instance | — | Q=d5a8c260… I=7474dc7f… db_qn=3 |
| Q4 | 4 | [26, 26]/[28, 28]/[513, 513] | 是 | approved | `341968c0` | approve→物化 | Question+Instance | — | Q=e65f567d… I=24a3a724… db_qn=4 |
| Q5 | 5 | [30, 30]/[32, 32]/[513, 513] | 是 | approved | `e411b13d` | approve→物化 | Question+Instance | — | Q=2cfa253a… I=d689ebe4… db_qn=5 |
| Q6 | 6 | [34, 34]/[36, 36]/[513, 513] | 是 | approved | `5f9a5410` | approve→物化 | Question+Instance | — | Q=1a66f3bb… I=eb36b324… db_qn=6 |
| Q7 | 7 | [38, 38]/[40, 40]/[513, 513] | 是 | approved | `82bf36ad` | approve→物化 | Question+Instance | — | Q=b9659f78… I=9ce64ca4… db_qn=7 |
| Q8 | 8 | [42, 42]/[44, 44]/[513, 513] | 是 | approved | `cc32656c` | approve→物化 | Question+Instance | — | Q=5f461ef4… I=5ce35672… db_qn=8 |
| Q9 | 9 | [46, 46]/[51, 51]/[513, 513] | 是 | — | `—` | Gate skip（semantic_status≠ready） | Annotation（未进 Candidate） | role option unresolved; role option unresolved; role option unresolved; role option unresolved; option spans unresolved: ['A', 'B', 'C', 'D'] | m3a_skip_reasons.json#focus_units |
| Q10 | 10 | [53, 55]/[57, 63]/[513, 513] | 是 | approved | `adc0bd2e` | approve→物化 | Question+Instance | — | Q=38781392… I=8a4f9b49… db_qn=10 |
| Q11 | 11 | [65, 65]/[67, 73]/[513, 513] | 是 | approved | `424c4019` | approve→物化 | Question+Instance | — | Q=876a38de… I=760fc710… db_qn=11 |
| Q12 | 12 | [83, 83]/[85, 91]/[513, 513] | 是 | approved | `4cfa99c8` | approve→物化 | Question+Instance | — | Q=ad7419ff… I=27ead7ed… db_qn=12 |
| Q13 | 13 | [93, 93]/[95, 95]/[513, 513] | 是 | approved | `b44acf02` | approve→物化 | Question+Instance | — | Q=75d68e1a… I=545d0770… db_qn=13 |
| Q14 | 14 | [97, 97]/[99, 101]/[513, 513] | 是 | approved | `cde03693` | approve→物化 | Question+Instance | — | Q=558866e4… I=418d3916… db_qn=14 |
| Q15 | 15 | [103, 103]/[105, 107]/[513, 513] | 是 | approved | `ea65f468` | approve→物化 | Question+Instance | — | Q=665008a7… I=6030f5aa… db_qn=15 |
| Q16 | 16 | [111, 111]/[113, 119]/[513, 513] | 是 | approved | `1d965d14` | approve→物化 | Question+Instance | — | Q=b22b5c75… I=a6c92843… db_qn=16 |
| Q17 | 17 | [121, 121]/[123, 129]/[513, 513] | 是 | approved | `3ea498b9` | approve→物化 | Question+Instance | — | Q=42f8624a… I=faa456b6… db_qn=17 |
| Q18 | 18 | [136, 136]/[138, 140]/[513, 513] | 是 | approved | `8b15ea14` | approve→物化 | Question+Instance | — | Q=3156701a… I=3b3197bd… db_qn=18 |
| Q19 | 19 | [142, 142]/[145, 145]/[513, 513] | 是 | — | `—` | Gate skip（semantic_status≠ready） | Annotation（未进 Candidate） | role option unresolved; role option unresolved; role option unresolved; option spans unresolved: ['B', 'C', 'D'] | m3a_skip_reasons.json#focus_units |
| Q20 | 20 | [149, 149]/[151, 159]/[513, 513] | 是 | approved | `da726453` | approve→物化 | Question+Instance | — | Q=a616052e… I=7c3eca1c… db_qn=20 |
| Q21 | 21 | [161, 161]/[163, 165]/[513, 513] | 是 | approved | `ce3f13ab` | approve→物化 | Question+Instance | — | Q=a1cdd401… I=20de1195… db_qn=21 |
| Q22 | 22 | [174, 174]/[176, 184]/[513, 513] | 是 | approved | `e16aefed` | approve→物化 | Question+Instance | — | Q=f0607ca0… I=7d8c0137… db_qn=22 |
| Q23 | 23 | [186, 186]/[188, 194]/[513, 513] | 是 | approved | `134640a4` | approve→物化 | Question+Instance | — | Q=a68d2863… I=594ecab8… db_qn=23 |
| Q24 | 24 | [196, 196]/[199, 199]/[513, 513] | 是 | — | `—` | Gate skip（semantic_status≠ready） | Annotation（未进 Candidate） | role option unresolved; role option unresolved; role option unresolved; role option unresolved; option spans unresolved: ['A', 'B', 'C', 'D'] | m3a_skip_reasons.json#focus_units |
| Q25 | 25 | [201, 201]/[204, 204]/[513, 513] | 是 | — | `—` | Gate skip（semantic_status≠ready） | Annotation（未进 Candidate） | role option unresolved; role option unresolved; role option unresolved; option spans unresolved: ['B', 'C', 'D'] | m3a_skip_reasons.json#focus_units |
| U-req1 | 26 | [210, 210]/—/[519, 521] | 是 | — | `—` | Gate skip（semantic_status≠ready） | Annotation（未进 Candidate） | role stem unresolved; stem unresolved | m3a_skip_reasons.json#focus_units |
| U-req2 | 27 | [212, 217]/—/[523, 526] | 是 | — | `—` | Gate skip（semantic_status≠ready） | Annotation（未进 Candidate） | role stem unresolved; stem unresolved | m3a_skip_reasons.json#focus_units |
| U-req3 | 28 | [219, 219]/—/[528, 530] | 是 | — | `—` | Gate skip（semantic_status≠ready） | Annotation（未进 Candidate） | role stem unresolved; stem unresolved | m3a_skip_reasons.json#focus_units |
| U-req4 | 29 | [221, 235]/—/[532, 540] | 是 | — | `—` | Gate skip（semantic_status≠ready） | Annotation（未进 Candidate） | role stem unresolved; stem unresolved | m3a_skip_reasons.json#focus_units |
| U-req5 | 30 | [237, 258]/—/[542, 552] | 是 | — | `—` | Gate skip（semantic_status≠ready） | Annotation（未进 Candidate） | role stem unresolved; stem unresolved | m3a_skip_reasons.json#focus_units |
| U-req6 | 31 | [260, 285]/—/[554, 562] | 是 | — | `—` | Gate skip（semantic_status≠ready） | Annotation（未进 Candidate） | role stem unresolved; stem unresolved | m3a_skip_reasons.json#focus_units |
| U-cl1 | 1 | [291, 299]/—/[566, 568] | 是 | pending_review | `6f46a8cf` | pending_review（未人工批准） | Candidate | IR ready，已产 Candidate，停在 pending_review | CAND=6f46a8cf… |
| U-cl2 | 2 | [301, 317]/—/[570, 572] | 是 | pending_review | `2d78dd8e` | pending_review（未人工批准） | Candidate | IR ready，已产 Candidate，停在 pending_review | CAND=2d78dd8e… |
| U-cl3 | 3 | [319, 350]/—/[574, 584] | 是 | pending_review | `1de00b65` | pending_review（未人工批准） | Candidate | IR ready，已产 Candidate，停在 pending_review | CAND=1de00b65… |
| U-org1 | 1 | [354, 401]/—/— | 是 | — | `—` | Gate skip（semantic_status≠ready） | Annotation（未进 Candidate） | role answer unresolved; answer unresolved | manifest: U-org1: 无 answer_lines（题号 [1]） | m3a_skip_reasons.json#focus_units |
| U-org2 | 2 | [403, 425]/—/— | 是 | — | `—` | Gate skip（semantic_status≠ready） | Annotation（未进 Candidate） | role answer unresolved; answer unresolved | manifest: U-org2: 无 answer_lines（题号 [2]） | m3a_skip_reasons.json#focus_units |
| U-org3 | 3 | [427, 440]/—/— | 是 | — | `—` | Gate skip（semantic_status≠ready） | Annotation（未进 Candidate） | role answer unresolved; answer unresolved | manifest: U-org3: 无 answer_lines（题号 [3]） | m3a_skip_reasons.json#focus_units |
| U-cp1 | 1 | [444, 458]/—/— | 是 | — | `—` | Gate skip（semantic_status≠ready） | Annotation（未进 Candidate） | role answer unresolved; answer unresolved | manifest: U-cp1: 无 answer_lines（题号 [1]） | m3a_skip_reasons.json#focus_units |
| U-cp2 | 2 | [460, 479]/—/— | 是 | — | `—` | Gate skip（semantic_status≠ready） | Annotation（未进 Candidate） | role answer unresolved; answer unresolved | manifest: U-cp2: 无 answer_lines（题号 [2]） | m3a_skip_reasons.json#focus_units |
| U-cp3 | 3 | [481, 502]/—/— | 是 | — | `—` | Gate skip（semantic_status≠ready） | Annotation（未进 Candidate） | role answer unresolved; answer unresolved | manifest: U-cp3: 无 answer_lines（题号 [3]） | m3a_skip_reasons.json#focus_units |

## 库计数（aitutors_test，生成时）

- `documents`: 16
- `document_source_versions`: 4
- `admission_candidates`: 25
- `questions`: 21
- `question_instances`: 21
- `instance_role_contents`: 126
- `materials`: 0
- `knowledge_nodes`: 0
- `question_knowledge_links`: 0

## 证据文件

- `AITutor-X/E2E_ACCEPTANCE/e2e_run/m3a_unit_outcome.json`
- `AITutor-X/E2E_ACCEPTANCE/e2e_run/m3a_skip_reasons.json`
- `AITutor-X/E2E_ACCEPTANCE/e2e_run/m2-real-chem-20261010T132409Z.json`（原跑 funnel）
- `AITutor-X/E2E_ACCEPTANCE/06_M1_PACKAGES/chem-2018-spring-huikao-teacher/manifest.json`
