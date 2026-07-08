from pathlib import Path
import json
import re

ROOT = Path(r"e:/ENGLISH_TECHER_TUNG/site")
LESSONS = ROOT / "lessons"
DICT_TPL = (LESSONS / "buoi-17-dictation.html").read_text(encoding="utf-8")
READ_TPL = (LESSONS / "buoi-17-reading.html").read_text(encoding="utf-8")
DRILL_TPL = (LESSONS / "buoi-17.html").read_text(encoding="utf-8")

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

DATA = {
  18: {
    "theme": "Financial Planning & Analysis",
    "hint_short": "revenue, expenditure, profitability, forecast, deficit, surplus, overhead, fiscal, budgetary",
    "focus_hint": "Financial Planning & Analysis — Revenue, Expenditure, Profitability, Forecast, Deficit, Surplus, Overhead, Fiscal & Budgetary",
    "tips": [
      "<strong>revenue / profitability:</strong> revenue là doanh thu; profitability là khả năng sinh lời sau khi xét chi phí.",
      "<strong>expenditure / overhead:</strong> expenditure là khoản chi; overhead là chi phí vận hành gián tiếp.",
      "<strong>forecast / fiscal / budgetary:</strong> dự báo tài chính, thuộc năm tài khóa, và liên quan đến ngân sách.",
      "<strong>deficit / surplus:</strong> deficit là thâm hụt; surplus là thặng dư."
    ],
    "vocabulary": [
      {"word":"revenue","hint":"doanh thu tạo ra từ hoạt động kinh doanh","ipa":"/ˈrev.ə.nuː/","syllables":3,"context":"Online subscriptions now generate more revenue than in-store sales."},
      {"word":"expenditure","hint":"khoản chi tiêu hoặc tổng mức chi","ipa":"/ɪkˈspen.dɪ.tʃɚ/","syllables":4,"context":"The report showed a sharp increase in marketing expenditure last quarter."},
      {"word":"profitability","hint":"khả năng sinh lời sau khi trừ các chi phí","ipa":"/ˌprɑː.fə.t̬əˈbɪl.ə.t̬i/","syllables":6,"context":"Management is reviewing the profitability of each product line."},
      {"word":"forecast","hint":"dự báo dựa trên dữ liệu hiện có","ipa":"/ˈfɔːr.kæst/","syllables":2,"context":"The finance team will forecast next year's cash flow this week."},
      {"word":"deficit","hint":"mức thâm hụt khi chi nhiều hơn thu","ipa":"/ˈdef.ə.sɪt/","syllables":3,"context":"The department ended the year with a small budget deficit."},
      {"word":"surplus","hint":"mức thặng dư khi thu nhiều hơn chi","ipa":"/ˈsɝː.plʌs/","syllables":2,"context":"The factory used last year's surplus to upgrade its equipment."},
      {"word":"overhead","hint":"chi phí vận hành gián tiếp như thuê văn phòng, điện, quản trị","ipa":"/ˈoʊ.vɚ.hed/","syllables":3,"context":"Rising overhead has reduced the company's profit margin."},
      {"word":"fiscal","hint":"thuộc tài chính hoặc năm tài khóa","ipa":"/ˈfɪs.kəl/","syllables":2,"context":"The board approved the plan for the next fiscal year."},
      {"word":"budgetary","hint":"thuộc ngân sách hoặc bị giới hạn bởi ngân sách","ipa":"/ˈbʌdʒ.ə.ter.i/","syllables":4,"context":"The expansion was delayed because of budgetary constraints."}
    ],
    "sentences": [
      "Online subscriptions now generate more revenue than in-store sales.",
      "The company expects revenue to rise after the holiday season.",
      "The report showed a sharp increase in marketing expenditure last quarter.",
      "Travel expenditure was reduced after the new video-meeting policy.",
      "Management is reviewing the profitability of each product line.",
      "High sales volume does not always guarantee profitability.",
      "The finance team will forecast next year's cash flow this week.",
      "Analysts forecast strong demand in the second half of the year.",
      "The department ended the year with a small budget deficit.",
      "Without cost controls, the project may create a serious deficit.",
      "The factory used last year's surplus to upgrade its equipment.",
      "A surplus gives the company room to invest in new technology.",
      "Rising overhead has reduced the company's profit margin.",
      "Management is looking for ways to cut overhead without harming quality.",
      "The board approved the plan for the next fiscal year.",
      "The fiscal report will be presented at Friday's meeting.",
      "The expansion was delayed because of budgetary constraints.",
      "Several budgetary decisions must be reviewed before the proposal is approved."
    ],
    "passage": [
      "A business can appear successful from the outside and still face serious financial problems inside.",
      "That is why managers look not only at revenue but also at every category of expenditure.",
      "A product with strong sales may still be weak if its profitability is lower than expected.",
      "To avoid surprises, the finance team prepares a forecast based on current orders and seasonal patterns.",
      "If spending keeps rising faster than income, the company may end the quarter with a deficit.",
      "On the other hand, careful planning can create a surplus that supports future investment.",
      "One common mistake is to ignore overhead, because indirect costs are less visible than raw materials or salaries.",
      "These numbers matter even more near the end of the fiscal year, when leaders must explain results to the board.",
      "In some cases, good ideas are delayed not because they are bad but because of temporary budgetary limits.",
      "Strong financial analysis helps a company decide which opportunities are worth pursuing and which risks are too expensive."
    ],
    "fillblank": [
      ["Online subscriptions now generate more revenue than in-store sales.","Online subscriptions now generate more _____ than in-store sales.","revenue"],
      ["The report showed a sharp increase in marketing expenditure.","The report showed a sharp increase in marketing _____.","expenditure"],
      ["Management is reviewing the profitability of each product line.","Management is reviewing the _____ of each product line.","profitability"],
      ["The finance team will forecast next year's cash flow.","The finance team will _____ next year's cash flow.","forecast"],
      ["The department ended the year with a small deficit.","The department ended the year with a small _____.","deficit"],
      ["The factory used last year's surplus to upgrade equipment.","The factory used last year's _____ to upgrade equipment.","surplus"],
      ["Rising overhead has reduced the company's profit margin.","Rising _____ has reduced the company's profit margin.","overhead"],
      ["The board approved the plan for the next fiscal year.","The board approved the plan for the next _____ year.","fiscal"],
      ["The expansion was delayed because of budgetary constraints.","The expansion was delayed because of _____ constraints.","budgetary"],
      ["The company expects revenue to rise after the holiday season.","The company expects _____ to rise after the holiday season.","revenue"],
      ["Analysts forecast strong demand in the second half of the year.","Analysts _____ strong demand in the second half of the year.","forecast"],
      ["A surplus gives the company room to invest in technology.","A _____ gives the company room to invest in technology.","surplus"],
      ["Management wants to cut overhead without harming quality.","Management wants to cut _____ without harming quality.","overhead"],
      ["The fiscal report will be presented at Friday's meeting.","The _____ report will be presented at Friday's meeting.","fiscal"],
      ["Several budgetary decisions must be reviewed.","Several _____ decisions must be reviewed.","budgetary"]
    ],
    "reading": {
      "words": ["revenue","expenditure","profitability","forecast","deficit","surplus","overhead","fiscal","budgetary"],
      "passage": [
        "A business may report strong {1} and still face financial pressure if its costs rise too quickly.",
        "That is why managers track every category of {2}, not only the most obvious expenses.",
        "High sales do not always guarantee {3}, because some products cost too much to support.",
        "To avoid surprises, the finance team prepares a {4} based on current orders and seasonal patterns.",
        "If spending keeps rising faster than income, the company may end the quarter with a {5}.",
        "Careful planning, however, can create a {6} that supports future investment.",
        "One common mistake is to ignore {7}, because indirect costs are less visible than salaries or materials.",
        "These numbers matter most near the end of the {8} year, when leaders must explain results to the board.",
        "Sometimes good ideas are delayed not because they are weak but because of temporary {9} limits."
      ],
      "answers": {"1":"revenue","2":"expenditure","3":"profitability","4":"forecast","5":"deficit","6":"surplus","7":"overhead","8":"fiscal","9":"budgetary"},
      "sentences": {"1":"A business may report strong revenue and still face pressure.","2":"Managers track every category of expenditure.","3":"High sales do not always guarantee profitability.","4":"The finance team prepares a forecast based on current orders.","5":"The company may end the quarter with a deficit.","6":"Careful planning can create a surplus.","7":"Many firms ignore overhead because it is less visible.","8":"These numbers matter near the end of the fiscal year.","9":"Temporary budgetary limits may delay good ideas."}
    },
    "drill_words": [
      {"word":"revenue","ipa":"/ˈrev.ə.nuː/","meaning":"doanh thu tạo ra từ hoạt động kinh doanh","confusers":["profit","expense","budget"],"confuserMeanings":["lợi nhuận","chi phí","ngân sách"],"grammar":{"original":"Online subscriptions now bring in more money than in-store sales.","target":"Online subscriptions now generate more revenue than in-store sales.","hint":"revenue = doanh thu, không phải profit.","keywords":["revenue"]},"toeic":{"text":"The company expects online sales to generate higher _______ next quarter.","choices":["revenue","overhead","deficit","guideline"],"answer":0,"explain":"generate higher revenue = tạo doanh thu cao hơn."}},
      {"word":"expenditure","ipa":"/ɪkˈspen.dɪ.tʃɚ/","meaning":"khoản chi tiêu hoặc tổng mức chi","confusers":["investment","income","forecast"],"confuserMeanings":["đầu tư","thu nhập","dự báo"],"grammar":{"original":"The report showed a sharp increase in marketing spending.","target":"The report showed a sharp increase in marketing expenditure.","hint":"expenditure = spending/chi tiêu.","keywords":["expenditure"]},"toeic":{"text":"Travel _______ fell after the company adopted video meetings.","choices":["expenditure","surplus","reputation","consensus"],"answer":0,"explain":"travel expenditure = chi tiêu đi lại."}},
      {"word":"profitability","ipa":"/ˌprɑː.fə.t̬əˈbɪl.ə.t̬i/","meaning":"khả năng sinh lời sau khi trừ các chi phí","confusers":["revenue","volume","fiscal"],"confuserMeanings":["doanh thu","sản lượng","thuộc tài khóa"],"grammar":{"original":"Management is reviewing how much profit each product line truly produces.","target":"Management is reviewing the profitability of each product line.","hint":"profitability = khả năng sinh lời.","keywords":["profitability"]},"toeic":{"text":"High sales volume does not always guarantee _______.","choices":["profitability","mandate","retention","guideline"],"answer":0,"explain":"high sales ≠ guaranteed profitability."}},
      {"word":"forecast","ipa":"/ˈfɔːr.kæst/","meaning":"dự báo dựa trên dữ liệu hiện có","confusers":["guess","audit","delay"],"confuserMeanings":["đoán","kiểm toán","trì hoãn"],"grammar":{"original":"Analysts will predict next year's cash flow this week.","target":"Analysts will forecast next year's cash flow this week.","hint":"forecast = dự báo có cơ sở, không chỉ đoán mò.","keywords":["forecast"]},"toeic":{"text":"The finance team will _______ demand before finalizing the production schedule.","choices":["forecast","compensate","authorize","violate"],"answer":0,"explain":"forecast demand = dự báo nhu cầu."}},
      {"word":"deficit","ipa":"/ˈdef.ə.sɪt/","meaning":"mức thâm hụt khi chi nhiều hơn thu","confusers":["surplus","balance","budget"],"confuserMeanings":["thặng dư","số dư/cân bằng","ngân sách"],"grammar":{"original":"The department spent more than it earned this year.","target":"The department ended the year with a deficit.","hint":"deficit = âm hụt, đối lập surplus.","keywords":["deficit"]},"toeic":{"text":"Without tighter cost control, the project may run at a _______.","choices":["deficit","surplus","guideline","revenue"],"answer":0,"explain":"run at a deficit = hoạt động trong tình trạng thâm hụt."}},
      {"word":"surplus","ipa":"/ˈsɝː.plʌs/","meaning":"mức thặng dư khi thu nhiều hơn chi","confusers":["deficit","expense","forecast"],"confuserMeanings":["thâm hụt","chi phí","dự báo"],"grammar":{"original":"The factory used last year's extra funds to upgrade equipment.","target":"The factory used last year's surplus to upgrade equipment.","hint":"surplus = thặng dư, đối lập deficit.","keywords":["surplus"]},"toeic":{"text":"The company used its cash _______ to invest in new software.","choices":["surplus","overhead","mandate","audit"],"answer":0,"explain":"cash surplus = tiền thặng dư."}},
      {"word":"overhead","ipa":"/ˈoʊ.vɚ.hed/","meaning":"chi phí vận hành gián tiếp như thuê văn phòng, điện, quản trị","confusers":["salary","profit","budgetary"],"confuserMeanings":["lương","lợi nhuận","thuộc ngân sách"],"grammar":{"original":"Rising indirect operating costs have reduced the company's margin.","target":"Rising overhead has reduced the company's margin.","hint":"overhead = chi phí gián tiếp/vận hành.","keywords":["overhead"]},"toeic":{"text":"Management is looking for ways to cut _______ without lowering quality.","choices":["overhead","revenue","surplus","alliance"],"answer":0,"explain":"cut overhead = cắt chi phí vận hành gián tiếp."}},
      {"word":"fiscal","ipa":"/ˈfɪs.kəl/","meaning":"thuộc tài chính hoặc năm tài khóa","confusers":["financial","ethical","emerging"],"confuserMeanings":["thuộc tài chính nói chung","đạo đức","mới nổi"],"grammar":{"original":"The board approved the plan for the next budget year.","target":"The board approved the plan for the next fiscal year.","hint":"fiscal year = năm tài khóa.","keywords":["fiscal","year"]},"toeic":{"text":"The company's _______ report will be presented at Friday's board meeting.","choices":["fiscal","loyal","transparent","coordinate"],"answer":0,"explain":"fiscal report = báo cáo tài khóa/tài chính."}},
      {"word":"budgetary","ipa":"/ˈbʌdʒ.ə.ter.i/","meaning":"thuộc ngân sách hoặc bị giới hạn bởi ngân sách","confusers":["legal","fiscal","responsive"],"confuserMeanings":["thuộc pháp lý","thuộc tài khóa nói chung","phản hồi nhanh"],"grammar":{"original":"The expansion was delayed because of limits related to the budget.","target":"The expansion was delayed because of budgetary limits.","hint":"budgetary = thuộc ngân sách / do ngân sách chi phối.","keywords":["budgetary"]},"toeic":{"text":"Several projects were postponed because of _______ constraints.","choices":["budgetary","ethical","courteous","mandate"],"answer":0,"explain":"budgetary constraints = các giới hạn do ngân sách."}}
    ]
  },
  19: {
    "theme": "Customer Experience & Service Recovery",
    "hint_short": "accommodate, courteous, responsive, escalate, compensate, retention, loyal, refund, reputation",
    "focus_hint": "Customer Experience & Service Recovery — Accommodate, Courteous, Responsive, Escalate, Compensate, Retention, Loyal, Refund & Reputation",
    "tips": [
      "<strong>accommodate / compensate:</strong> accommodate là đáp ứng nhu cầu; compensate là đền bù khi có vấn đề xảy ra.",
      "<strong>responsive / escalate:</strong> phản hồi nhanh và biết khi nào cần chuyển vấn đề lên cấp cao hơn.",
      "<strong>retention / loyal:</strong> giữ chân khách hàng và xây sự trung thành dài hạn.",
      "<strong>refund / reputation:</strong> hoàn tiền là hành động; reputation là uy tín bị ảnh hưởng bởi cách xử lý."
    ],
    "vocabulary": [
      {"word":"accommodate","hint":"đáp ứng hoặc tạo điều kiện cho nhu cầu của khách hàng","ipa":"/əˈkɑː.mə.deɪt/","syllables":4,"context":"The hotel agreed to accommodate the guest's late check-in request."},
      {"word":"courteous","hint":"lịch sự, nhã nhặn trong cách cư xử","ipa":"/ˈkɝː.t̬i.əs/","syllables":3,"context":"Even unhappy customers respond better to courteous service."},
      {"word":"responsive","hint":"phản hồi nhanh và phù hợp với yêu cầu hoặc vấn đề","ipa":"/rɪˈspɑːn.sɪv/","syllables":3,"context":"A responsive support team can prevent small complaints from growing."},
      {"word":"escalate","hint":"chuyển vấn đề lên cấp cao hơn hoặc để nó leo thang","ipa":"/ˈes.kə.leɪt/","syllables":3,"context":"If the customer remains unhappy, the case may escalate to a supervisor."},
      {"word":"compensate","hint":"đền bù hoặc bồi thường cho thiệt hại, bất tiện","ipa":"/ˈkɑːm.pən.seɪt/","syllables":3,"context":"The airline offered miles to compensate passengers for the long delay."},
      {"word":"retention","hint":"sự giữ chân khách hàng hoặc nhân viên lâu dài","ipa":"/rɪˈten.ʃən/","syllables":3,"context":"Management is investing in service quality to improve customer retention."},
      {"word":"loyal","hint":"trung thành và tiếp tục ủng hộ một thương hiệu hoặc người bán","ipa":"/ˈlɔɪ.əl/","syllables":2,"context":"Loyal customers often stay even when a competitor offers a lower price."},
      {"word":"refund","hint":"hoàn lại tiền cho khách hàng","ipa":"/ˈriː.fʌnd/","syllables":2,"context":"The store issued a full refund after the product failed twice."},
      {"word":"reputation","hint":"danh tiếng hoặc uy tín trong mắt người khác","ipa":"/ˌrep.jəˈteɪ.ʃən/","syllables":4,"context":"A single public complaint can damage a brand's reputation if handled poorly."}
    ],
    "sentences": [
      "The hotel agreed to accommodate the guest's late check-in request.",
      "We try to accommodate special seating requests whenever possible.",
      "Even unhappy customers respond better to courteous service.",
      "Her courteous tone helped calm the caller almost immediately.",
      "A responsive support team can prevent small complaints from growing.",
      "Customers expect online sellers to be responsive within a few hours.",
      "If the customer remains unhappy, the case may escalate to a supervisor.",
      "Problems often escalate when nobody takes clear responsibility.",
      "The airline offered miles to compensate passengers for the long delay.",
      "The company decided to compensate the client for the repeated errors.",
      "Management is investing in service quality to improve customer retention.",
      "Strong retention is often cheaper than constant customer acquisition.",
      "Loyal customers often stay even when a competitor offers a lower price.",
      "A loyal customer base can protect a brand during difficult periods.",
      "The store issued a full refund after the product failed twice.",
      "Customers usually ask for a refund only after patience runs out.",
      "A single public complaint can damage a brand's reputation if handled poorly.",
      "A strong reputation is built slowly but can be lost very quickly."
    ],
    "passage": [
      "Most customer problems begin as small inconveniences that could be solved quickly with attention and care.",
      "A good service team first tries to accommodate the customer's reasonable request whenever possible.",
      "Even when the answer is no, a courteous explanation reduces frustration and protects trust.",
      "Speed also matters, because a responsive team can stop a minor problem from becoming a public complaint.",
      "If the issue is too large for one agent, the case should escalate quickly instead of being ignored.",
      "When the company is clearly at fault, it may need to compensate the customer for lost time or money.",
      "Handled well, even a complaint can improve retention by showing the customer that the company takes responsibility seriously.",
      "That experience can turn an unhappy buyer into a loyal customer over time.",
      "In some situations, the fastest solution is simply to offer a refund and move on respectfully.",
      "The real goal is not only to solve one problem but also to protect the company's long-term reputation."
    ],
    "fillblank": [
      ["The hotel agreed to accommodate the guest's late check-in request.","The hotel agreed to _____ the guest's late check-in request.","accommodate"],
      ["Even unhappy customers respond better to courteous service.","Even unhappy customers respond better to _____ service.","courteous"],
      ["A responsive support team can prevent small complaints from growing.","A _____ support team can prevent small complaints from growing.","responsive"],
      ["If the customer remains unhappy, the case may escalate to a supervisor.","If the customer remains unhappy, the case may _____ to a supervisor.","escalate"],
      ["The airline offered miles to compensate passengers for the delay.","The airline offered miles to _____ passengers for the delay.","compensate"],
      ["Management is investing in service quality to improve customer retention.","Management is investing in service quality to improve customer _____.","retention"],
      ["Loyal customers often stay even when competitors offer lower prices.","_____ customers often stay even when competitors offer lower prices.","Loyal"],
      ["The store issued a full refund after the product failed twice.","The store issued a full _____ after the product failed twice.","refund"],
      ["A single complaint can damage a brand's reputation.","A single complaint can damage a brand's _____.","reputation"],
      ["We try to accommodate special seating requests whenever possible.","We try to _____ special seating requests whenever possible.","accommodate"],
      ["Her courteous tone helped calm the caller immediately.","Her _____ tone helped calm the caller immediately.","courteous"],
      ["Problems often escalate when nobody takes responsibility.","Problems often _____ when nobody takes responsibility.","escalate"],
      ["The company decided to compensate the client for repeated errors.","The company decided to _____ the client for repeated errors.","compensate"],
      ["Strong retention is cheaper than constant acquisition.","Strong _____ is cheaper than constant acquisition.","retention"],
      ["A strong reputation can be lost very quickly.","A strong _____ can be lost very quickly.","reputation"]
    ],
    "reading": {
      "words": ["accommodate","courteous","responsive","escalate","compensate","retention","loyal","refund","reputation"],
      "passage": [
        "A service team should first try to {1} a customer's reasonable request whenever possible.",
        "Even when the answer is no, a {2} explanation reduces frustration and protects trust.",
        "Speed matters too, because a {3} team can stop a small problem from becoming a public complaint.",
        "If the issue is too serious for one agent, the case should {4} quickly instead of being ignored.",
        "When the company is clearly at fault, it may need to {5} the customer for lost time or money.",
        "Handled well, even a complaint can improve customer {6} over the long term.",
        "That experience may turn an unhappy buyer into a {7} customer.",
        "In some situations, the simplest solution is to offer a full {8}.",
        "The real goal is not only to solve one case but also to protect the company's {9}."
      ],
      "answers": {"1":"accommodate","2":"courteous","3":"responsive","4":"escalate","5":"compensate","6":"retention","7":"loyal","8":"refund","9":"reputation"},
      "sentences": {"1":"A service team should try to accommodate a reasonable request.","2":"A courteous explanation reduces frustration.","3":"A responsive team can stop a small problem from growing.","4":"A serious case may escalate quickly.","5":"The company may need to compensate the customer.","6":"Good handling can improve customer retention.","7":"An unhappy buyer may become a loyal customer.","8":"Sometimes the simplest solution is a full refund.","9":"The company wants to protect its reputation."}
    },
    "drill_words": [
      {"word":"accommodate","ipa":"/əˈkɑː.mə.deɪt/","meaning":"đáp ứng hoặc tạo điều kiện cho nhu cầu của khách hàng","confusers":["compensate","reject","postpone"],"confuserMeanings":["đền bù sau sự cố","từ chối","hoãn lại"],"grammar":{"original":"The hotel agreed to meet the guest's late check-in request.","target":"The hotel agreed to accommodate the guest's late check-in request.","hint":"accommodate a request/guest/need.","keywords":["accommodate"]},"toeic":{"text":"We will try to _______ your seating request if space is available.","choices":["accommodate","refund","forecast","endorse"],"answer":0,"explain":"accommodate your request = đáp ứng yêu cầu của bạn."}},
      {"word":"courteous","ipa":"/ˈkɝː.t̬i.əs/","meaning":"lịch sự, nhã nhặn trong cách cư xử","confusers":["strict","loyal","transparent"],"confuserMeanings":["nghiêm khắc","trung thành","minh bạch"],"grammar":{"original":"Her polite tone helped calm the angry caller.","target":"Her courteous tone helped calm the angry caller.","hint":"courteous = polite and respectful.","keywords":["courteous"]},"toeic":{"text":"Even frustrated clients respond better to _______ service.","choices":["courteous","budgetary","emerging","deficit"],"answer":0,"explain":"courteous service = dịch vụ lịch sự, nhã nhặn."}},
      {"word":"responsive","ipa":"/rɪˈspɑːn.sɪv/","meaning":"phản hồi nhanh và phù hợp với yêu cầu hoặc vấn đề","confusers":["silent","loyal","reactive"],"confuserMeanings":["im lặng","trung thành","phản ứng bị động"],"grammar":{"original":"A support team that replies quickly can prevent complaints from growing.","target":"A responsive support team can prevent complaints from growing.","hint":"responsive = phản hồi nhanh/chủ động.","keywords":["responsive"]},"toeic":{"text":"Customers expect online sellers to be highly _______ to questions.","choices":["responsive","saturated","ethical","budgetary"],"answer":0,"explain":"responsive to questions = phản hồi nhanh các câu hỏi."}},
      {"word":"escalate","ipa":"/ˈes.kə.leɪt/","meaning":"chuyển vấn đề lên cấp cao hơn hoặc để nó leo thang","confusers":["solve","delay","ignore"],"confuserMeanings":["giải quyết","trì hoãn","phớt lờ"],"grammar":{"original":"If the customer remains unhappy, the case should be moved to a supervisor.","target":"If the customer remains unhappy, the case should escalate to a supervisor.","hint":"escalate to a supervisor/manager.","keywords":["escalate"]},"toeic":{"text":"Complaints often _______ when no one takes clear responsibility.","choices":["escalate","refund","adhere","streamline"],"answer":0,"explain":"complaints escalate = khiếu nại leo thang."}},
      {"word":"compensate","ipa":"/ˈkɑːm.pən.seɪt/","meaning":"đền bù hoặc bồi thường cho thiệt hại, bất tiện","confusers":["accommodate","retain","mandate"],"confuserMeanings":["đáp ứng nhu cầu","giữ lại","quy định bắt buộc"],"grammar":{"original":"The company offered miles to make up for the long delay.","target":"The company offered miles to compensate passengers for the long delay.","hint":"compensate someone for something.","keywords":["compensate","for"]},"toeic":{"text":"The airline decided to _______ passengers for the canceled flight.","choices":["compensate","forecast","authorize","audit"],"answer":0,"explain":"compensate passengers = bồi thường cho hành khách."}},
      {"word":"retention","ipa":"/rɪˈten.ʃən/","meaning":"sự giữ chân khách hàng hoặc nhân viên lâu dài","confusers":["acquisition","refund","revenue"],"confuserMeanings":["thu hút khách mới","hoàn tiền","doanh thu"],"grammar":{"original":"Management is investing in service quality to keep more customers over time.","target":"Management is investing in service quality to improve customer retention.","hint":"customer retention = giữ chân khách hàng.","keywords":["retention"]},"toeic":{"text":"Strong customer _______ is often cheaper than constant acquisition.","choices":["retention","guideline","surplus","mandate"],"answer":0,"explain":"customer retention = giữ chân khách hàng."}},
      {"word":"loyal","ipa":"/ˈlɔɪ.əl/","meaning":"trung thành và tiếp tục ủng hộ một thương hiệu hoặc người bán","confusers":["courteous","responsive","ethical"],"confuserMeanings":["lịch sự","phản hồi nhanh","có đạo đức"],"grammar":{"original":"These customers continue buying from the brand for many years.","target":"These customers remain loyal to the brand for many years.","hint":"loyal TO a brand/company/person.","keywords":["loyal","to"]},"toeic":{"text":"A generous rewards program can help build a _______ customer base.","choices":["loyal","fiscal","transparent","deficit"],"answer":0,"explain":"a loyal customer base = tệp khách hàng trung thành."}},
      {"word":"refund","ipa":"/ˈriː.fʌnd/","meaning":"hoàn lại tiền cho khách hàng","confusers":["discount","exchange","retention"],"confuserMeanings":["giảm giá","đổi hàng","giữ chân"],"grammar":{"original":"The store returned the customer's money after the product failed twice.","target":"The store issued a full refund after the product failed twice.","hint":"issue/give a refund.","keywords":["refund"]},"toeic":{"text":"Customers may request a full _______ if the item arrives damaged.","choices":["refund","forecast","guideline","audit"],"answer":0,"explain":"a full refund = hoàn tiền đầy đủ."}},
      {"word":"reputation","ipa":"/ˌrep.jəˈteɪ.ʃən/","meaning":"danh tiếng hoặc uy tín trong mắt người khác","confusers":["identity","policy","segment"],"confuserMeanings":["bản sắc","chính sách","phân khúc"],"grammar":{"original":"A single public complaint can damage the brand's good name.","target":"A single public complaint can damage the brand's reputation.","hint":"damage/protect/build a reputation.","keywords":["reputation"]},"toeic":{"text":"The company responded quickly to protect its online _______.","choices":["reputation","overhead","surplus","mandate"],"answer":0,"explain":"protect its reputation = bảo vệ uy tín của công ty."}}
    ]
  },
  20: {
    "theme": "Market Expansion & Competition",
    "hint_short": "penetrate, diversify, acquisition, alliance, segment, saturated, emerging, dominate, scalable",
    "focus_hint": "Market Expansion & Competition — Penetrate, Diversify, Acquisition, Alliance, Segment, Saturated, Emerging, Dominate & Scalable",
    "tips": [
      "<strong>penetrate / segment:</strong> thâm nhập thị trường và xác định phân khúc khách hàng cụ thể.",
      "<strong>diversify / scalable:</strong> đa dạng hóa để giảm rủi ro và mở rộng quy mô hiệu quả.",
      "<strong>acquisition / alliance:</strong> mua lại doanh nghiệp khác hoặc lập liên minh chiến lược.",
      "<strong>saturated / emerging / dominate:</strong> thị trường bão hòa, thị trường mới nổi, và chiếm ưu thế cạnh tranh."
    ],
    "vocabulary": [
      {"word":"penetrate","hint":"thâm nhập vào một thị trường hoặc nhóm khách hàng","ipa":"/ˈpen.ə.treɪt/","syllables":3,"context":"The company is trying to penetrate the Southeast Asian market."},
      {"word":"diversify","hint":"đa dạng hóa để giảm phụ thuộc vào một nguồn duy nhất","ipa":"/daɪˈvɝː.sə.faɪ/","syllables":4,"context":"The retailer wants to diversify its product range before the holiday season."},
      {"word":"acquisition","hint":"sự mua lại hoặc thâu tóm một công ty khác","ipa":"/ˌæk.wəˈzɪʃ.ən/","syllables":4,"context":"The acquisition will give the company access to new distribution channels."},
      {"word":"alliance","hint":"liên minh hoặc quan hệ hợp tác chiến lược","ipa":"/əˈlaɪ.əns/","syllables":3,"context":"The two brands formed an alliance to share research and logistics costs."},
      {"word":"segment","hint":"phân khúc thị trường hoặc nhóm khách hàng có đặc điểm chung","ipa":"/ˈseɡ.mənt/","syllables":2,"context":"The luxury segment remained strong even during the slowdown."},
      {"word":"saturated","hint":"bão hòa, gần như không còn chỗ tăng trưởng thêm","ipa":"/ˈsætʃ.ə.reɪ.t̬ɪd/","syllables":4,"context":"The domestic market is already saturated, so expansion abroad is necessary."},
      {"word":"emerging","hint":"mới nổi, đang phát triển nhanh","ipa":"/ɪˈmɝː.dʒɪŋ/","syllables":3,"context":"The firm sees strong potential in several emerging markets."},
      {"word":"dominate","hint":"chiếm ưu thế hoặc kiểm soát phần lớn thị trường","ipa":"/ˈdɑː.mə.neɪt/","syllables":3,"context":"A few large platforms dominate the online advertising industry."},
      {"word":"scalable","hint":"có thể mở rộng quy mô hiệu quả mà không tăng chi phí quá nhanh","ipa":"/ˈskeɪ.lə.bəl/","syllables":3,"context":"Investors want a scalable business model, not just short-term growth."}
    ],
    "sentences": [
      "The company is trying to penetrate the Southeast Asian market.",
      "New pricing strategies helped the brand penetrate a younger customer base.",
      "The retailer wants to diversify its product range before the holiday season.",
      "Diversifying suppliers can reduce the risk of sudden disruption.",
      "The acquisition will give the company access to new distribution channels.",
      "Shareholders approved the acquisition after reviewing the expected synergies.",
      "The two brands formed an alliance to share research and logistics costs.",
      "A strong alliance can open doors that one company cannot open alone.",
      "The luxury segment remained strong even during the slowdown.",
      "Marketing messages must be adjusted for each customer segment.",
      "The domestic market is already saturated, so expansion abroad is necessary.",
      "Growth becomes expensive when a market is close to saturated.",
      "The firm sees strong potential in several emerging markets.",
      "Emerging technologies often attract investors before they become stable.",
      "A few large platforms dominate the online advertising industry.",
      "Low prices alone will not help a new entrant dominate the market.",
      "Investors want a scalable business model, not just short-term growth.",
      "A scalable system can support more users without major redesign."
    ],
    "passage": [
      "A company that wants long-term growth must decide where its next customers will come from.",
      "Sometimes the best move is to penetrate a new region before competitors do.",
      "At other times, the safer choice is to diversify products so the business depends less on one source of demand.",
      "Some firms grow by making an acquisition that gives them immediate access to technology or customers.",
      "Others prefer an alliance, sharing costs and local knowledge with a trusted partner.",
      "The right strategy often depends on which segment of the market still offers room for growth.",
      "In a saturated market, even strong companies may struggle to expand without lowering prices too far.",
      "That is why many brands turn to emerging markets, where demand is growing more quickly.",
      "The ultimate goal is not only to dominate today but to build a scalable model that can support larger operations tomorrow.",
      "Companies that expand too quickly without that foundation often create complexity instead of real advantage."
    ],
    "fillblank": [
      ["The company is trying to penetrate the Southeast Asian market.","The company is trying to _____ the Southeast Asian market.","penetrate"],
      ["The retailer wants to diversify its product range.","The retailer wants to _____ its product range.","diversify"],
      ["The acquisition will give the company access to new channels.","The _____ will give the company access to new channels.","acquisition"],
      ["The two brands formed an alliance to share costs.","The two brands formed an _____ to share costs.","alliance"],
      ["The luxury segment remained strong during the slowdown.","The luxury _____ remained strong during the slowdown.","segment"],
      ["The domestic market is already saturated.","The domestic market is already _____.","saturated"],
      ["The firm sees strong potential in several emerging markets.","The firm sees strong potential in several _____ markets.","emerging"],
      ["A few large platforms dominate the industry.","A few large platforms _____ the industry.","dominate"],
      ["Investors want a scalable business model.","Investors want a _____ business model.","scalable"],
      ["New pricing helped the brand penetrate a younger customer base.","New pricing helped the brand _____ a younger customer base.","penetrate"],
      ["Diversifying suppliers can reduce disruption risk.","_____ suppliers can reduce disruption risk.","Diversifying"],
      ["A strong alliance can open doors a company cannot open alone.","A strong _____ can open doors a company cannot open alone.","alliance"],
      ["Growth becomes expensive when a market is saturated.","Growth becomes expensive when a market is _____.","saturated"],
      ["Emerging technologies often attract investors early.","_____ technologies often attract investors early.","Emerging"],
      ["A scalable system can support more users without redesign.","A _____ system can support more users without redesign.","scalable"]
    ],
    "reading": {
      "words": ["penetrate","diversify","acquisition","alliance","segment","saturated","emerging","dominate","scalable"],
      "passage": [
        "Some companies try to {1} a new region before their competitors do.",
        "Others prefer to {2} products so the business depends less on one source of demand.",
        "One fast way to grow is through an {3} that brings immediate access to technology or customers.",
        "Another strategy is to build an {4} with a trusted local partner.",
        "The best choice often depends on which customer {5} still offers room for growth.",
        "In a {6} market, even strong brands struggle to expand without cutting prices too far.",
        "That is why many companies turn to {7} markets, where demand is increasing more quickly.",
        "The long-term goal is not only to {8} today but also to prepare for future competition.",
        "Investors prefer a {9} model that can support larger operations tomorrow."
      ],
      "answers": {"1":"penetrate","2":"diversify","3":"acquisition","4":"alliance","5":"segment","6":"saturated","7":"emerging","8":"dominate","9":"scalable"},
      "sentences": {"1":"Some companies try to penetrate a new region quickly.","2":"Others diversify products to reduce risk.","3":"An acquisition can bring immediate access to customers.","4":"An alliance can reduce costs and risk.","5":"Growth depends on which segment still has room.","6":"A saturated market is hard to expand in.","7":"Emerging markets often grow faster.","8":"Some brands hope to dominate the market.","9":"Investors prefer a scalable business model."}
    },
    "drill_words": [
      {"word":"penetrate","ipa":"/ˈpen.ə.treɪt/","meaning":"thâm nhập vào một thị trường hoặc nhóm khách hàng","confusers":["enter","escape","withdraw"],"confuserMeanings":["đi vào (chung)","thoát ra","rút lui"],"grammar":{"original":"The brand is trying to enter the Southeast Asian market successfully.","target":"The brand is trying to penetrate the Southeast Asian market.","hint":"penetrate a market/customer base.","keywords":["penetrate"]},"toeic":{"text":"The company launched a low-cost line to _______ a younger customer base.","choices":["penetrate","refund","audit","mentor"],"answer":0,"explain":"penetrate a customer base = thâm nhập tệp khách hàng."}},
      {"word":"diversify","ipa":"/daɪˈvɝː.sə.faɪ/","meaning":"đa dạng hóa để giảm phụ thuộc vào một nguồn duy nhất","confusers":["simplify","depend","dominate"],"confuserMeanings":["đơn giản hóa","phụ thuộc","chiếm ưu thế"],"grammar":{"original":"The retailer wants to expand into several different product categories.","target":"The retailer wants to diversify its product range.","hint":"diversify products/suppliers/investments.","keywords":["diversify"]},"toeic":{"text":"The firm plans to _______ its suppliers to reduce risk.","choices":["diversify","enforce","forecast","endorse"],"answer":0,"explain":"diversify suppliers = đa dạng hóa nhà cung cấp."}},
      {"word":"acquisition","ipa":"/ˌæk.wəˈzɪʃ.ən/","meaning":"sự mua lại hoặc thâu tóm một công ty khác","confusers":["alliance","sale","refund"],"confuserMeanings":["liên minh","việc bán ra","hoàn tiền"],"grammar":{"original":"Buying the smaller company will give the group access to new technology.","target":"The acquisition of the smaller company will give the group access to new technology.","hint":"acquisition = mua lại/thâu tóm.","keywords":["acquisition"]},"toeic":{"text":"The board approved the _______ after reviewing expected cost savings.","choices":["acquisition","guideline","deficit","retention"],"answer":0,"explain":"approve the acquisition = phê duyệt thương vụ mua lại."}},
      {"word":"alliance","ipa":"/əˈlaɪ.əns/","meaning":"liên minh hoặc quan hệ hợp tác chiến lược","confusers":["contract","conflict","mandate"],"confuserMeanings":["hợp đồng","xung đột","quy định bắt buộc"],"grammar":{"original":"The two brands formed a strategic partnership to share costs.","target":"The two brands formed an alliance to share costs.","hint":"form/build an alliance.","keywords":["alliance"]},"toeic":{"text":"The airline entered an _______ with a regional carrier to expand routes.","choices":["alliance","audit","refund","forecast"],"answer":0,"explain":"enter an alliance = tham gia liên minh hợp tác."}},
      {"word":"segment","ipa":"/ˈseɡ.mənt/","meaning":"phân khúc thị trường hoặc nhóm khách hàng có đặc điểm chung","confusers":["market","alliance","region"],"confuserMeanings":["thị trường chung","liên minh","khu vực"],"grammar":{"original":"The luxury customer group remained strong during the slowdown.","target":"The luxury segment remained strong during the slowdown.","hint":"market/customer segment.","keywords":["segment"]},"toeic":{"text":"Marketing messages must be adapted for each customer _______.","choices":["segment","mandate","overhead","audit"],"answer":0,"explain":"customer segment = phân khúc khách hàng."}},
      {"word":"saturated","ipa":"/ˈsætʃ.ə.reɪ.t̬ɪd/","meaning":"bão hòa, gần như không còn chỗ tăng trưởng thêm","confusers":["emerging","growing","transparent"],"confuserMeanings":["mới nổi","đang tăng trưởng","minh bạch"],"grammar":{"original":"The domestic market is already too full for easy expansion.","target":"The domestic market is already saturated.","hint":"a saturated market = thị trường bão hòa.","keywords":["saturated"]},"toeic":{"text":"Price competition is intense because the market is nearly _______.","choices":["saturated","ethical","responsive","budgetary"],"answer":0,"explain":"nearly saturated = gần bão hòa."}},
      {"word":"emerging","ipa":"/ɪˈmɝː.dʒɪŋ/","meaning":"mới nổi, đang phát triển nhanh","confusers":["saturated","declining","ethical"],"confuserMeanings":["bão hòa","đang suy giảm","đạo đức"],"grammar":{"original":"The company sees strong potential in several fast-growing new markets.","target":"The company sees strong potential in several emerging markets.","hint":"emerging markets/technology.","keywords":["emerging"]},"toeic":{"text":"Investors are showing interest in several _______ markets in the region.","choices":["emerging","transparent","courteous","fiscal"],"answer":0,"explain":"emerging markets = các thị trường mới nổi."}},
      {"word":"dominate","ipa":"/ˈdɑː.mə.neɪt/","meaning":"chiếm ưu thế hoặc kiểm soát phần lớn thị trường","confusers":["enter","support","coordinate"],"confuserMeanings":["tham gia","hỗ trợ","phối hợp"],"grammar":{"original":"A few large platforms control most of the online advertising market.","target":"A few large platforms dominate the online advertising market.","hint":"dominate a market/industry/sector.","keywords":["dominate"]},"toeic":{"text":"Low prices alone will not help a new brand _______ the market.","choices":["dominate","adhere","refund","mentor"],"answer":0,"explain":"dominate the market = chiếm ưu thế thị trường."}},
      {"word":"scalable","ipa":"/ˈskeɪ.lə.bəl/","meaning":"có thể mở rộng quy mô hiệu quả mà không tăng chi phí quá nhanh","confusers":["flexible","temporary","loyal"],"confuserMeanings":["linh hoạt","tạm thời","trung thành"],"grammar":{"original":"Investors want a business model that can grow efficiently without major redesign.","target":"Investors want a scalable business model.","hint":"scalable system/model/platform.","keywords":["scalable"]},"toeic":{"text":"The software must be _______ enough to support millions of users.","choices":["scalable","budgetary","courteous","fiscal"],"answer":0,"explain":"scalable enough = có thể mở rộng đủ tốt."}}
    ]
  }
}


def render_dictation(num, d):
    t = DICT_TPL.replace("Buổi 17", f"Buổi {num}").replace("Compliance & Governance", d["theme"])
    t = re.sub(r"<ul>[\s\S]*?</ul>", "<ul>\n" + "\n".join("        <li>" + x + "</li>" for x in d["tips"]) + "\n      </ul>", t, count=1)
    t = re.sub(r"vocabulary: \[[\s\S]*?\n\s*\],\n\s*sentences:", "vocabulary: [\n" + vocab_block(d["vocabulary"]) + "\n      ],\n      sentences:", t, count=1)
    t = re.sub(r"sentences: \[[\s\S]*?\n\s*\],\n\s*passage:", "sentences: [\n" + lines_block(d["sentences"]) + "\n      ],\n      passage:", t, count=1)
    t = re.sub(r"passage: \[[\s\S]*?\n\s*\],\n\s*fillblank:", "passage: [\n" + lines_block(d["passage"]) + "\n      ],\n      fillblank:", t, count=1)
    t = re.sub(r"fillblank: \[[\s\S]*?\n\s*\]\n\s*\};", "fillblank: [\n" + fill_block(d["fillblank"]) + "\n      ]\n    };", t, count=1)
    t = t.replace("lessonId: 'buoi-17'", f"lessonId: 'buoi-{num}'")
    return t


def render_reading(num, d):
    t = READ_TPL.replace("Buổi 17", f"Buổi {num}").replace("Compliance & Governance", d["theme"]).replace("adhere, enforce, audit, disclose, ethical, transparent, violate, mandate, guideline", d["hint_short"])
    r = d["reading"]
    passage_data = "const PASSAGE_DATA = {\n"
    passage_data += "  words: [" + ", ".join(js_str(x) for x in r["words"]) + "],\n"
    passage_data += "  passage: [\n" + lines_block(r["passage"], "    ") + "\n  ],\n"
    passage_data += "  answers: {\n" + ",\n".join(f"    {k}: {js_str(v)}" for k, v in r["answers"].items()) + "\n  },\n"
    passage_data += "  sentences: {\n" + ",\n".join(f"    {k}: {js_str(v)}" for k, v in r["sentences"].items()) + "\n  }\n};"
    t = re.sub(r"const PASSAGE_DATA = \{[\s\S]*?\n\};", passage_data, t, count=1)
    return t


def render_drill(num, d):
    t = DRILL_TPL.replace("Buổi 17", f"Buổi {num}").replace("Compliance & Governance — Adhere, Enforce, Audit, Disclose, Ethical, Transparent, Violate, Mandate & Guideline", d["focus_hint"])
    t = t.replace("../lessons/buoi-17-reading.html", f"../lessons/buoi-{num}-reading.html")
    t = t.replace("const key = 'drill_b17_history';", f"const key = 'drill_b{num}_history';")
    t = re.sub(r"const WORDS = \[[\s\S]*?\n\];", drill_words_block(d["drill_words"]), t, count=1)
    return t


for num in [18, 19, 20]:
    d = DATA[num]
    (LESSONS / f"buoi-{num}-dictation.html").write_text(render_dictation(num, d), encoding="utf-8")
    (LESSONS / f"buoi-{num}-reading.html").write_text(render_reading(num, d), encoding="utf-8")
    (LESSONS / f"buoi-{num}.html").write_text(render_drill(num, d), encoding="utf-8")

# update pronunciation-data.js append if missing
pron_path = ROOT / "js" / "pronunciation-data.js"
pron = pron_path.read_text(encoding="utf-8")
if '"18": {' not in pron:
    append = '''  "18": {
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
    pron = pron.replace('  }\n  ,\n  "18"', '  },\n  "18"')
    pron_path.write_text(pron, encoding='utf-8')

index_path = ROOT / 'index.html'
index = index_path.read_text(encoding='utf-8')
if 'buoi-18-dictation.html' not in index:
    anchor = '''      <li>
        <a href="lessons/buoi-17.html">
          <div class="lesson-title">Buổi 17 — 4-in-1 Drill</div>
          <div class="lesson-desc">Ôn sâu: adhere/comply, enforce/mandate, audit/disclose, ethical/transparent và violate/guideline qua 4 kỹ năng</div>
        </a>
      </li>'''
    blocks = '''
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
    index = index.replace('cả 17 buổi', 'cả 20 buổi')
    index = index.replace('cả 16 buổi', 'cả 20 buổi')
    index = index.replace('Ôn trộn 17 buổi', 'Ôn trộn 20 buổi')
    index = index.replace('Ôn trộn 16 buổi', 'Ôn trộn 20 buổi')
    index_path.write_text(index, encoding='utf-8')

rm_path = ROOT / 'review-mix.html'
rm = rm_path.read_text(encoding='utf-8')
rm = rm.replace('Review Mix — Ôn trộn 17 buổi', 'Review Mix — Ôn trộn 20 buổi')
rm = rm.replace('Review Mix — Ôn trộn 16 buổi', 'Review Mix — Ôn trộn 20 buổi')
rm = rm.replace('Ôn trộn từ vựng cả 17 buổi.', 'Ôn trộn từ vựng cả 20 buổi.')
rm = rm.replace('Ôn trộn từ vựng cả 16 buổi.', 'Ôn trộn từ vựng cả 20 buổi.')
rm_path.write_text(rm, encoding='utf-8')

print('generated buoi 18-20')
