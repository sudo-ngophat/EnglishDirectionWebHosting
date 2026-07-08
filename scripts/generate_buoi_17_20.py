from pathlib import Path
import json
import re

ROOT = Path(r"e:/ENGLISH_TECHER_TUNG/site")
LESSONS = ROOT / "lessons"

DICT_TPL = (LESSONS / "buoi-16-dictation.html").read_text(encoding="utf-8")
READ_TPL = (LESSONS / "buoi-16-reading.html").read_text(encoding="utf-8")
DRILL_TPL = (LESSONS / "buoi-16.html").read_text(encoding="utf-8")

DATA = {
  17: {
    "theme": "Compliance & Governance",
    "hint_short": "adhere, enforce, audit, disclose, ethical, transparent, violate, mandate, guideline",
    "focus_hint": "Compliance & Governance — Adhere, Enforce, Audit, Disclose, Ethical, Transparent, Violate, Mandate & Guideline",
    "tips": [
      "<strong>adhere / comply (Buổi 4):</strong> adhere là bám sát nguyên tắc; comply là tuân theo yêu cầu chính thức.",
      "<strong>enforce / mandate:</strong> enforce là thực thi/áp dụng nghiêm; mandate là quy định bắt buộc (danh từ hoặc động từ).",
      "<strong>audit / disclose:</strong> audit là rà soát chính thức có báo cáo; disclose là công bố thông tin ra ngoài.",
      "<strong>ethical / transparent / violate / guideline:</strong> đạo đức nghề, minh bạch, vi phạm, và hướng dẫn thực hành.",
    ],
    "vocabulary": [
      {"word":"adhere","hint":"tuân theo chặt chẽ một quy tắc hoặc tiêu chuẩn","ipa":"/ədˈhɪr/","syllables":2,"context":"All employees must adhere to the company's data-security policy."},
      {"word":"enforce","hint":"thực thi hoặc áp dụng nghiêm một quy định","ipa":"/ɪnˈfɔːrs/","syllables":2,"context":"Managers are expected to enforce the new attendance rules consistently."},
      {"word":"audit","hint":"kiểm toán hoặc rà soát chính thức để kiểm tra tính đúng đắn","ipa":"/ˈɔː.dɪt/","syllables":2,"context":"The finance team will audit travel expenses at the end of each quarter."},
      {"word":"disclose","hint":"công bố hoặc tiết lộ thông tin một cách chính thức","ipa":"/dɪsˈkloʊz/","syllables":2,"context":"Public companies must disclose major risks to investors."},
      {"word":"ethical","hint":"phù hợp với chuẩn mực đạo đức nghề nghiệp","ipa":"/ˈeθ.ɪ.kəl/","syllables":3,"context":"Leaders must make ethical decisions even under pressure."},
      {"word":"transparent","hint":"minh bạch, rõ ràng, không che giấu thông tin quan trọng","ipa":"/trænsˈper.ənt/","syllables":3,"context":"A transparent process builds trust inside the company."},
      {"word":"violate","hint":"vi phạm một quy tắc, luật, hoặc thỏa thuận","ipa":"/ˈvaɪ.ə.leɪt/","syllables":3,"context":"Anyone who violates the safety policy will receive a warning."},
      {"word":"mandate","hint":"quy định bắt buộc hoặc lệnh chính thức từ cấp có thẩm quyền","ipa":"/ˈmæn.deɪt/","syllables":2,"context":"The new mandate requires all staff to complete security training."},
      {"word":"guideline","hint":"hướng dẫn hoặc nguyên tắc thực hành","ipa":"/ˈɡaɪd.laɪn/","syllables":2,"context":"The document provides clear guidelines for handling customer data."}
    ],
    "sentences": [
      "All employees must adhere to the company's data-security policy.",
      "The engineers strictly adhere to the safety checklist before every test.",
      "Managers are expected to enforce the new attendance rules consistently.",
      "The city government will enforce the new speed limit starting next month.",
      "The finance team will audit travel expenses at the end of each quarter.",
      "An external firm was hired to audit the company's financial records.",
      "Public companies must disclose major risks to investors.",
      "The report failed to disclose a conflict of interest between the two managers.",
      "Leaders must make ethical decisions even under pressure.",
      "The magazine praised the firm for its ethical treatment of workers.",
      "A transparent process builds trust inside the company.",
      "Customers prefer businesses that are transparent about pricing.",
      "Anyone who violates the safety policy will receive a warning.",
      "The company was fined for repeatedly violating environmental regulations.",
      "The new mandate requires all staff to complete security training.",
      "A court mandate suspended the sale of the disputed property.",
      "The document provides clear guidelines for handling customer data.",
      "Please follow the official guidelines when preparing the annual report."
    ],
    "passage": [
      "Every serious organization needs a set of rules that its people actually adhere to in daily work.",
      "Written rules are useless if no one is willing to enforce them when they are broken.",
      "That is why most companies also audit their own records on a regular basis.",
      "The results of those checks are shared with the board so that leaders can disclose problems early.",
      "Behind every rule there should be a clear reason, usually connected to an ethical value the company wants to protect.",
      "Modern employees expect their company to be transparent about salaries, promotions, and important decisions.",
      "When someone chooses to violate a rule for personal gain, the response must be firm but fair.",
      "Sometimes the government issues a formal mandate that all businesses in the industry must follow.",
      "In that case, each team needs a set of practical guidelines that translate the mandate into daily habits.",
      "In the end, compliance is less about fear of punishment and more about protecting the trust between the company, its workers, and its customers."
    ],
    "fillblank": [
      ["All employees must adhere to the data-security policy.","All employees must _____ to the data-security policy.","adhere"],
      ["Managers are expected to enforce the new attendance rules.","Managers are expected to _____ the new attendance rules.","enforce"],
      ["The finance team will audit travel expenses each quarter.","The finance team will _____ travel expenses each quarter.","audit"],
      ["Public companies must disclose major risks.","Public companies must _____ major risks.","disclose"],
      ["Leaders must make ethical decisions under pressure.","Leaders must make _____ decisions under pressure.","ethical"],
      ["A transparent process builds trust inside the company.","A _____ process builds trust inside the company.","transparent"],
      ["Anyone who violates the safety policy will receive a warning.","Anyone who _____ the safety policy will receive a warning.","violates"],
      ["The new mandate requires all staff to complete security training.","The new _____ requires all staff to complete security training.","mandate"],
      ["The document provides clear guidelines for handling data.","The document provides clear _____ for handling data.","guidelines"],
      ["The engineers adhere to the checklist before every test.","The engineers _____ to the checklist before every test.","adhere"],
      ["An external firm was hired to audit the records.","An external firm was hired to _____ the records.","audit"],
      ["The report failed to disclose a conflict of interest.","The report failed to _____ a conflict of interest.","disclose"],
      ["Customers prefer businesses that are transparent about pricing.","Customers prefer businesses that are _____ about pricing.","transparent"],
      ["The company was fined for violating regulations.","The company was fined for _____ regulations.","violating"],
      ["Please follow the official guidelines when preparing the report.","Please follow the official _____ when preparing the report.","guidelines"]
    ],
    "reading": {
      "words": ["adhere","enforce","audit","disclose","ethical","transparent","violate","mandate","guideline"],
      "passage": [
        "Every serious organization needs rules that employees actually {1} to in daily work.",
        "Those rules mean little if nobody is willing to {2} them when they are broken.",
        "That is why many companies regularly {3} their records, processes, and reports.",
        "The results of those checks help leaders {4} problems before they become public scandals.",
        "Behind every rule there should be an {5} principle that explains why the rule exists.",
        "Employees are more likely to cooperate when the decision-making process is {6} and fair.",
        "When someone chooses to {7} a rule for personal gain, the response must be firm and fair.",
        "Sometimes the government issues a formal {8} that all businesses in the industry must follow.",
        "In that case, each department needs a practical {9} that turns the mandate into daily habits."
      ],
      "answers": {"1":"adhere","2":"enforce","3":"audit","4":"disclose","5":"ethical","6":"transparent","7":"violate","8":"mandate","9":"guideline"},
      "sentences": {"1":"Employees must adhere to the rules in daily work.","2":"Someone must enforce the rules when they are broken.","3":"Many companies audit their records and reports.","4":"Leaders disclose problems before they become scandals.","5":"Every rule should reflect an ethical principle.","6":"The decision-making process should be transparent and fair.","7":"Some people violate rules for personal gain.","8":"The government may issue a formal mandate.","9":"Each department needs a practical guideline."}
    },
    "drill_words": [
      {"word":"adhere","ipa":"/ədˈhɪr/","meaning":"tuân theo chặt chẽ một quy tắc hoặc tiêu chuẩn","confusers":["comply","delay","argue"],"confuserMeanings":["tuân thủ yêu cầu chính thức","trì hoãn","tranh cãi"],"grammar":{"original":"All employees must follow the company policy strictly.","target":"All employees must adhere to the company policy strictly.","hint":"Dùng adhere TO + policy/rule/standard.","keywords":["adhere","to"]},"toeic":{"text":"Staff members are expected to _______ to the revised dress code.","choices":["adhere","delay","monitor","compensate"],"answer":0,"explain":"adhere to the dress code = tuân theo quy định trang phục."}},
      {"word":"enforce","ipa":"/ɪnˈfɔːrs/","meaning":"thực thi hoặc áp dụng nghiêm một quy định","confusers":["create","ignore","mandate"],"confuserMeanings":["tạo ra","phớt lờ","ra lệnh bắt buộc"],"grammar":{"original":"Managers must make sure the new attendance rule is applied.","target":"Managers must enforce the new attendance rule.","hint":"Dùng enforce + rule/law/policy.","keywords":["enforce"]},"toeic":{"text":"Security officers will _______ the new visitor policy at all entrances.","choices":["enforce","disclose","authorize","streamline"],"answer":0,"explain":"enforce the policy = thực thi chính sách."}},
      {"word":"audit","ipa":"/ˈɔː.dɪt/","meaning":"kiểm toán hoặc rà soát chính thức để kiểm tra tính đúng đắn","confusers":["inspect","ignore","budget"],"confuserMeanings":["kiểm tra chung","phớt lờ","ngân sách"],"grammar":{"original":"An outside firm will review the company's financial records.","target":"An outside firm will audit the company's financial records.","hint":"Dùng audit + records/accounts/expenses.","keywords":["audit"]},"toeic":{"text":"The finance department plans to _______ travel expenses every quarter.","choices":["audit","violate","endorse","coordinate"],"answer":0,"explain":"audit expenses = rà soát/kiểm toán chi phí."}},
      {"word":"disclose","ipa":"/dɪsˈkloʊz/","meaning":"công bố hoặc tiết lộ thông tin một cách chính thức","confusers":["hide","report","mandate"],"confuserMeanings":["che giấu","báo cáo chung","quy định bắt buộc"],"grammar":{"original":"Public companies must reveal major risks to investors.","target":"Public companies must disclose major risks to investors.","hint":"Dùng disclose + information/risk/conflict.","keywords":["disclose"]},"toeic":{"text":"The company failed to _______ the conflict of interest in its annual report.","choices":["disclose","enforce","adjust","mentor"],"answer":0,"explain":"disclose the conflict = công bố xung đột lợi ích."}},
      {"word":"ethical","ipa":"/ˈeθ.ɪ.kəl/","meaning":"phù hợp với chuẩn mực đạo đức nghề nghiệp","confusers":["legal","careful","transparent"],"confuserMeanings":["hợp pháp","cẩn thận","minh bạch"],"grammar":{"original":"Leaders should make morally responsible decisions under pressure.","target":"Leaders should make ethical decisions under pressure.","hint":"ethical = có đạo đức nghề nghiệp, không chỉ đúng luật.","keywords":["ethical"]},"toeic":{"text":"The board praised the manager for her _______ treatment of employees.","choices":["ethical","saturated","budgetary","emerging"],"answer":0,"explain":"ethical treatment = cách đối xử có đạo đức."}},
      {"word":"transparent","ipa":"/trænsˈper.ənt/","meaning":"minh bạch, rõ ràng, không che giấu thông tin quan trọng","confusers":["secret","efficient","strict"],"confuserMeanings":["bí mật","hiệu quả","nghiêm khắc"],"grammar":{"original":"A clear and open process builds trust among employees.","target":"A transparent process builds trust among employees.","hint":"transparent = cởi mở, rõ ràng về thông tin/quy trình.","keywords":["transparent"]},"toeic":{"text":"Customers prefer pricing policies that are clear and _______.","choices":["transparent","fiscal","saturated","loyal"],"answer":0,"explain":"clear and transparent = rõ ràng và minh bạch."}},
      {"word":"violate","ipa":"/ˈvaɪ.ə.leɪt/","meaning":"vi phạm một quy tắc, luật, hoặc thỏa thuận","confusers":["follow","audit","disclose"],"confuserMeanings":["tuân theo","kiểm toán","công bố"],"grammar":{"original":"Anyone who breaks the safety policy will receive a warning.","target":"Anyone who violates the safety policy will receive a warning.","hint":"Dùng violate + rule/law/policy/agreement.","keywords":["violates"]},"toeic":{"text":"Employees who _______ the company's confidentiality agreement may face dismissal.","choices":["violate","empower","endorse","coordinate"],"answer":0,"explain":"violate the agreement = vi phạm thỏa thuận."}},
      {"word":"mandate","ipa":"/ˈmæn.deɪt/","meaning":"quy định bắt buộc hoặc lệnh chính thức từ cấp có thẩm quyền","confusers":["suggestion","guideline","warning"],"confuserMeanings":["gợi ý","hướng dẫn","cảnh báo"],"grammar":{"original":"The new official requirement applies to all staff members.","target":"The new mandate applies to all staff members.","hint":"mandate = yêu cầu bắt buộc, mạnh hơn guideline.","keywords":["mandate"]},"toeic":{"text":"The government issued a _______ requiring stronger data protection.","choices":["mandate","refund","forecast","segment"],"answer":0,"explain":"issue a mandate = ban hành quy định bắt buộc."}},
      {"word":"guideline","ipa":"/ˈɡaɪd.laɪn/","meaning":"hướng dẫn hoặc nguyên tắc thực hành","confusers":["mandate","habit","expense"],"confuserMeanings":["quy định bắt buộc","thói quen","chi phí"],"grammar":{"original":"The document offers practical advice for handling customer data.","target":"The document offers practical guidelines for handling customer data.","hint":"guideline = hướng dẫn thực hành, nhẹ hơn mandate.","keywords":["guidelines"]},"toeic":{"text":"Please follow the official _______ when preparing the annual report.","choices":["guidelines","mandates","deficits","alliances"],"answer":0,"explain":"follow the official guidelines = làm theo hướng dẫn chính thức."}}
    ]
  }
}


def js_str(x):
    return json.dumps(x, ensure_ascii=False)


def lines_block(lines, indent="        "):
    return ",\n".join(indent + js_str(x) for x in lines)


def vocab_block(vs):
    return ",\n".join(
        f'        {{ word: {js_str(v["word"])}, hint: {js_str(v["hint"])}, ipa: {js_str(v["ipa"])}, syllables: {v["syllables"]}, context: {js_str(v["context"])} }}'
        for v in vs
    )


def fill_block(items):
    return ",\n".join(
        f'        {{ sentence: {js_str(s)}, display: {js_str(d)}, answer: {js_str(a)} }}'
        for s, d, a in items
    )


def drill_words_block(words):
    blocks = []
    for w in words:
        blocks.append(
            "  {\n"
            f"    word: {js_str(w['word'])},\n"
            f"    ipa: {js_str(w['ipa'])},\n"
            f"    meaning: {js_str(w['meaning'])},\n"
            f"    confusers: [{', '.join(js_str(x) for x in w['confusers'])}],\n"
            f"    confuserMeanings: [{', '.join(js_str(x) for x in w['confuserMeanings'])}],\n"
            f"    grammar: {{\n"
            f"      original: {js_str(w['grammar']['original'])},\n"
            f"      target: {js_str(w['grammar']['target'])},\n"
            f"      hint: {js_str(w['grammar']['hint'])},\n"
            f"      keywords: [{', '.join(js_str(x) for x in w['grammar']['keywords'])}]\n"
            f"    }},\n"
            f"    toeic: {{\n"
            f"      text: {js_str(w['toeic']['text'])},\n"
            f"      choices: [{', '.join(js_str(x) for x in w['toeic']['choices'])}],\n"
            f"      answer: {w['toeic']['answer']},\n"
            f"      explain: {js_str(w['toeic']['explain'])}\n"
            f"    }}\n"
            "  }"
        )
    return "const WORDS = [\n" + ",\n".join(blocks) + "\n];"


def render_dictation(num, d):
    t = DICT_TPL
    t = t.replace("Buổi 16 — Dictation: Leadership & Delegation", f"Buổi {num} — Dictation: {d['theme']}")
    t = t.replace("<h1>Buổi 16 — Dictation</h1>", f"<h1>Buổi {num} — Dictation</h1>")
    t = t.replace("<h4>Chủ đề Buổi 16: Leadership & Delegation</h4>", f"<h4>Chủ đề Buổi {num}: {d['theme']}</h4>")
    tip_ul = "<ul>\n" + "\n".join("        <li>" + x + "</li>" for x in d["tips"]) + "\n      </ul>"
    t = re.sub(r"<ul>[\s\S]*?</ul>", tip_ul, t, count=1)
    t = t.replace('name: "Buổi 16"', f'name: "Buổi {num}"')
    t = t.replace("lessonId: 'buoi-16'", f"lessonId: 'buoi-{num}'")
    t = re.sub(r"vocabulary: \[[\s\S]*?\n\s*\],\n\s*sentences:", "vocabulary: [\n" + vocab_block(d["vocabulary"]) + "\n      ],\n      sentences:", t, count=1)
    t = re.sub(r"sentences: \[[\s\S]*?\n\s*\],\n\s*passage:", "sentences: [\n" + lines_block(d["sentences"]) + "\n      ],\n      passage:", t, count=1)
    t = re.sub(r"passage: \[[\s\S]*?\n\s*\],\n\s*fillblank:", "passage: [\n" + lines_block(d["passage"]) + "\n      ],\n      fillblank:", t, count=1)
    t = re.sub(r"fillblank: \[[\s\S]*?\n\s*\]\n\s*\};", "fillblank: [\n" + fill_block(d["fillblank"]) + "\n      ]\n    };", t, count=1)
    return t


def render_reading(num, d):
    t = READ_TPL
    t = t.replace("Buổi 16 — Reading Fill-in-the-Blank", f"Buổi {num} — Reading Fill-in-the-Blank")
    t = t.replace("Buổi 16 — Reading: Fill in the Blanks", f"Buổi {num} — Reading: Fill in the Blanks")
    hint = f'    <p class="hint">Chủ đề Buổi {num}: {d["theme"]} — {d["hint_short"]}.</p>'
    t = re.sub(r'    <p class="hint">Chủ đề Buổi 16:.*?</p>', hint, t, count=1)
    r = d["reading"]
    passage_data = "const PASSAGE_DATA = {\n"
    passage_data += "  words: [" + ", ".join(js_str(x) for x in r["words"]) + "],\n"
    passage_data += "  passage: [\n" + lines_block(r["passage"], "    ") + "\n  ],\n"
    passage_data += "  answers: {\n" + ",\n".join(f"    {k}: {js_str(v)}" for k, v in r["answers"].items()) + "\n  },\n"
    passage_data += "  sentences: {\n" + ",\n".join(f"    {k}: {js_str(v)}" for k, v in r["sentences"].items()) + "\n  }\n};"
    t = re.sub(r"const PASSAGE_DATA = \{[\s\S]*?\n\};", passage_data, t, count=1)
    return t


def render_drill(num, d):
    t = DRILL_TPL
    t = t.replace("Buổi 16 — 4-in-1 Drill", f"Buổi {num} — 4-in-1 Drill")
    t = re.sub(r"<p class=\"hint\">Mỗi từ test[\s\S]*?</p>", f'<p class="hint">Mỗi từ test qua 4 kỹ năng: Nghe-Viết → Nghĩa → Ngữ pháp → TOEIC | Trọng tâm Buổi {num}: {d["focus_hint"]}</p>', t, count=1)
    t = t.replace("../lessons/buoi-16-reading.html", f"../lessons/buoi-{num}-reading.html")
    t = t.replace("Đọc tiếp Buổi 16", f"Đọc tiếp Buổi {num}")
    t = t.replace("const key = 'drill_b16_history';", f"const key = 'drill_b{num}_history';")
    t = re.sub(r"const WORDS = \[[\s\S]*?\n\];", drill_words_block(d["drill_words"]), t, count=1)
    return t


# generate 17 from current filled data, and 18-20 from DATA
for num, d in DATA.items():
    (LESSONS / f"buoi-{num}-dictation.html").write_text(render_dictation(num, d), encoding="utf-8")
    (LESSONS / f"buoi-{num}-reading.html").write_text(render_reading(num, d), encoding="utf-8")
    (LESSONS / f"buoi-{num}.html").write_text(render_drill(num, d), encoding="utf-8")

# pronunciation-data.js append 17-20
pron_path = ROOT / "js" / "pronunciation-data.js"
pron = pron_path.read_text(encoding="utf-8")
if '"17": {' not in pron:
    append = '''  "17": {
    title: "Buổi 17 — Compliance & Governance",
    words: [
      { word: "adhere", ipa: "/ədˈhɪr/", meaning: "tuân theo chặt chẽ" },
      { word: "enforce", ipa: "/ɪnˈfɔːrs/", meaning: "thực thi nghiêm" },
      { word: "audit", ipa: "/ˈɔː.dɪt/", meaning: "kiểm toán / rà soát" },
      { word: "disclose", ipa: "/dɪsˈkloʊz/", meaning: "công bố / tiết lộ" },
      { word: "ethical", ipa: "/ˈeθ.ɪ.kəl/", meaning: "mang tính đạo đức" },
      { word: "transparent", ipa: "/trænsˈper.ənt/", meaning: "minh bạch" },
      { word: "violate", ipa: "/ˈvaɪ.ə.leɪt/", meaning: "vi phạm" },
      { word: "mandate", ipa: "/ˈmæn.deɪt/", meaning: "quy định bắt buộc" },
      { word: "guideline", ipa: "/ˈɡaɪd.laɪn/", meaning: "hướng dẫn / nguyên tắc" }
    ]
  },
  "18": {
    title: "Buổi 18 — Financial Planning & Analysis",
    words: [
      { word: "revenue", ipa: "/ˈrev.ə.nuː/", meaning: "doanh thu" },
      { word: "expenditure", ipa: "/ɪkˈspen.dɪ.tʃɚ/", meaning: "chi tiêu / khoản chi" },
      { word: "profitability", ipa: "/ˌprɑː.fə.t̬əˈbɪl.ə.t̬i/", meaning: "khả năng sinh lời" },
      { word: "forecast", ipa: "/ˈfɔːr.kæst/", meaning: "dự báo" },
      { word: "deficit", ipa: "/ˈdef.ə.sɪt/", meaning: "thâm hụt" },
      { word: "surplus", ipa: "/ˈsɝː.plʌs/", meaning: "thặng dư" },
      { word: "overhead", ipa: "/ˈoʊ.vɚ.hed/", meaning: "chi phí vận hành gián tiếp" },
      { word: "fiscal", ipa: "/ˈfɪs.kəl/", meaning: "thuộc tài khóa / tài chính" },
      { word: "budgetary", ipa: "/ˈbʌdʒ.ə.ter.i/", meaning: "thuộc ngân sách" }
    ]
  },
  "19": {
    title: "Buổi 19 — Customer Experience & Service Recovery",
    words: [
      { word: "accommodate", ipa: "/əˈkɑː.mə.deɪt/", meaning: "đáp ứng / tạo điều kiện" },
      { word: "courteous", ipa: "/ˈkɝː.t̬i.əs/", meaning: "lịch sự" },
      { word: "responsive", ipa: "/rɪˈspɑːn.sɪv/", meaning: "phản hồi nhanh" },
      { word: "escalate", ipa: "/ˈes.kə.leɪt/", meaning: "chuyển cấp / leo thang" },
      { word: "compensate", ipa: "/ˈkɑːm.pən.seɪt/", meaning: "bồi thường / đền bù" },
      { word: "retention", ipa: "/rɪˈten.ʃən/", meaning: "giữ chân khách hàng" },
      { word: "loyal", ipa: "/ˈlɔɪ.əl/", meaning: "trung thành" },
      { word: "refund", ipa: "/ˈriː.fʌnd/", meaning: "hoàn tiền" },
      { word: "reputation", ipa: "/ˌrep.jəˈteɪ.ʃən/", meaning: "danh tiếng / uy tín" }
    ]
  },
  "20": {
    title: "Buổi 20 — Market Expansion & Competition",
    words: [
      { word: "penetrate", ipa: "/ˈpen.ə.treɪt/", meaning: "thâm nhập thị trường" },
      { word: "diversify", ipa: "/daɪˈvɝː.sə.faɪ/", meaning: "đa dạng hóa" },
      { word: "acquisition", ipa: "/ˌæk.wəˈzɪʃ.ən/", meaning: "sự mua lại / thâu tóm" },
      { word: "alliance", ipa: "/əˈlaɪ.əns/", meaning: "liên minh / hợp tác" },
      { word: "segment", ipa: "/ˈseɡ.mənt/", meaning: "phân khúc" },
      { word: "saturated", ipa: "/ˈsætʃ.ə.reɪ.t̬ɪd/", meaning: "bão hòa" },
      { word: "emerging", ipa: "/ɪˈmɝː.dʒɪŋ/", meaning: "mới nổi" },
      { word: "dominate", ipa: "/ˈdɑː.mə.neɪt/", meaning: "chiếm ưu thế" },
      { word: "scalable", ipa: "/ˈskeɪ.lə.bəl/", meaning: "có thể mở rộng quy mô" }
    ]
  }
};'''
    pron = re.sub(r'\n};\s*$', '\n  ,\n' + append, pron, count=1)
    pron = pron.replace('  }\n  ,\n  "17"', '  },\n  "17"')
    pron_path.write_text(pron, encoding="utf-8")

# index.html insert links and bump counts
index_path = ROOT / 'index.html'
index = index_path.read_text(encoding='utf-8')
if 'buoi-17-dictation.html' not in index:
    anchor = '''      <li>
        <a href="lessons/buoi-16.html">
          <div class="lesson-title">Buổi 16 — 4-in-1 Drill</div>
          <div class="lesson-desc">Ôn sâu: delegate/assign, supervise/oversee, empower/authorize, accountable, mentor, coordinate và endorse qua 4 kỹ năng</div>
        </a>
      </li>'''
    blocks = '''
      <li>
        <a href="lessons/buoi-17-dictation.html">
          <div class="lesson-title">Buổi 17 — Dictation</div>
          <div class="lesson-desc">Compliance & Governance: adhere, enforce, audit, disclose, ethical, transparent, violate, mandate, guideline</div>
        </a>
      </li>
      <li>
        <a href="lessons/buoi-17-reading.html">
          <div class="lesson-title">Buổi 17 — Reading Fill-in-the-Blank</div>
          <div class="lesson-desc">Bài đọc về tuân thủ: thực thi quy định, kiểm toán, công bố thông tin và xây niềm tin minh bạch</div>
        </a>
      </li>
      <li>
        <a href="lessons/buoi-17.html">
          <div class="lesson-title">Buổi 17 — 4-in-1 Drill</div>
          <div class="lesson-desc">Ôn sâu: adhere/comply, enforce/mandate, audit/disclose, ethical/transparent và violate/guideline qua 4 kỹ năng</div>
        </a>
      </li>
      <li>
        <a href="lessons/buoi-18-dictation.html">
          <div class="lesson-title">Buổi 18 — Dictation</div>
          <div class="lesson-desc">Financial Planning & Analysis: revenue, expenditure, profitability, forecast, deficit, surplus, overhead, fiscal, budgetary</div>
        </a>
      </li>
      <li>
        <a href="lessons/buoi-18-reading.html">
          <div class="lesson-title">Buổi 18 — Reading Fill-in-the-Blank</div>
          <div class="lesson-desc">Bài đọc về tài chính: doanh thu, chi tiêu, thâm hụt, thặng dư và giới hạn ngân sách</div>
        </a>
      </li>
      <li>
        <a href="lessons/buoi-18.html">
          <div class="lesson-title">Buổi 18 — 4-in-1 Drill</div>
          <div class="lesson-desc">Ôn sâu: revenue/profitability, expenditure/overhead, deficit/surplus, forecast/fiscal và budgetary qua 4 kỹ năng</div>
        </a>
      </li>
      <li>
        <a href="lessons/buoi-19-dictation.html">
          <div class="lesson-title">Buổi 19 — Dictation</div>
          <div class="lesson-desc">Customer Experience & Service Recovery: accommodate, courteous, responsive, escalate, compensate, retention, loyal, refund, reputation</div>
        </a>
      </li>
      <li>
        <a href="lessons/buoi-19-reading.html">
          <div class="lesson-title">Buổi 19 — Reading Fill-in-the-Blank</div>
          <div class="lesson-desc">Bài đọc về chăm sóc khách hàng: xử lý phàn nàn, bồi thường hợp lý và giữ uy tín thương hiệu</div>
        </a>
      </li>
      <li>
        <a href="lessons/buoi-19.html">
          <div class="lesson-title">Buổi 19 — 4-in-1 Drill</div>
          <div class="lesson-desc">Ôn sâu: accommodate/compensate, courteous/responsive, escalate/retention, loyal/refund và reputation qua 4 kỹ năng</div>
        </a>
      </li>
      <li>
        <a href="lessons/buoi-20-dictation.html">
          <div class="lesson-title">Buổi 20 — Dictation</div>
          <div class="lesson-desc">Market Expansion & Competition: penetrate, diversify, acquisition, alliance, segment, saturated, emerging, dominate, scalable</div>
        </a>
      </li>
      <li>
        <a href="lessons/buoi-20-reading.html">
          <div class="lesson-title">Buổi 20 — Reading Fill-in-the-Blank</div>
          <div class="lesson-desc">Bài đọc về mở rộng thị trường: thâm nhập, đa dạng hóa, liên minh, thị trường bão hòa và mô hình mở rộng</div>
        </a>
      </li>
      <li>
        <a href="lessons/buoi-20.html">
          <div class="lesson-title">Buổi 20 — 4-in-1 Drill</div>
          <div class="lesson-desc">Ôn sâu: penetrate/diversify, acquisition/alliance, segment/saturated, emerging/dominate và scalable qua 4 kỹ năng</div>
        </a>
      </li>'''
    index = index.replace(anchor, anchor + blocks)
    index = index.replace('cả 16 buổi', 'cả 20 buổi')
    index = index.replace('Ôn trộn 16 buổi', 'Ôn trộn 20 buổi')
    index_path.write_text(index, encoding='utf-8')

# review-mix hint/title bump
rm_path = ROOT / 'review-mix.html'
rm = rm_path.read_text(encoding='utf-8')
rm = rm.replace('Review Mix — Ôn trộn 16 buổi', 'Review Mix — Ôn trộn 20 buổi')
rm = rm.replace('Ôn trộn từ vựng cả 16 buổi.', 'Ôn trộn từ vựng cả 20 buổi.')
rm_path.write_text(rm, encoding='utf-8')

print('generated buoi 17-20')
