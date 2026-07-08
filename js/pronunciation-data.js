// Dữ liệu từ vựng phát âm cho 13 buổi. Mỗi từ: { word, ipa, meaning }
const PRON_LESSONS = {
  "1": {
    title: "Buổi 1 — Core Verbs",
    words: [
      { word: "lack", ipa: "/læk/", meaning: "thiếu" },
      { word: "alter", ipa: "/ˈɔːl.tɚ/", meaning: "thay đổi" },
      { word: "consider", ipa: "/kənˈsɪd.ɚ/", meaning: "cân nhắc" },
      { word: "develop", ipa: "/dɪˈvel.əp/", meaning: "phát triển" },
      { word: "require", ipa: "/rɪˈkwaɪr/", meaning: "yêu cầu" },
      { word: "satisfy", ipa: "/ˈsæt̬.ɪs.faɪ/", meaning: "làm hài lòng" },
      { word: "value", ipa: "/ˈvæl.juː/", meaning: "giá trị / coi trọng" }
    ]
  },
  "2": {
    title: "Buổi 2 — Performance",
    words: [
      { word: "acquire", ipa: "/əˈkwaɪr/", meaning: "đạt được / tiếp thu" },
      { word: "perform", ipa: "/pɚˈfɔːrm/", meaning: "thực hiện / biểu diễn" },
      { word: "decline", ipa: "/dɪˈklaɪn/", meaning: "suy giảm / từ chối" },
      { word: "permit", ipa: "/pɚˈmɪt/", meaning: "cho phép" },
      { word: "compare", ipa: "/kəmˈper/", meaning: "so sánh" },
      { word: "indifferent", ipa: "/ɪnˈdɪf.ɚ.ənt/", meaning: "thờ ơ" }
    ]
  },
  "3": {
    title: "Buổi 3 — Cognition",
    words: [
      { word: "perspective", ipa: "/pɚˈspek.tɪv/", meaning: "góc nhìn" },
      { word: "perception", ipa: "/pɚˈsep.ʃən/", meaning: "nhận thức" },
      { word: "awareness", ipa: "/əˈwer.nəs/", meaning: "sự nhận biết" },
      { word: "consciousness", ipa: "/ˈkɑːn.ʃəs.nəs/", meaning: "ý thức" },
      { word: "cognition", ipa: "/kɑːɡˈnɪʃ.ən/", meaning: "nhận thức (tư duy)" },
      { word: "recognition", ipa: "/ˌrek.əɡˈnɪʃ.ən/", meaning: "sự công nhận" },
      { word: "mutual", ipa: "/ˈmjuː.tʃu.əl/", meaning: "lẫn nhau" }
    ]
  },
  "4": {
    title: "Buổi 4 — Change & Compliance",
    words: [
      { word: "revise", ipa: "/rɪˈvaɪz/", meaning: "sửa đổi" },
      { word: "amend", ipa: "/əˈmend/", meaning: "tu chỉnh" },
      { word: "renovate", ipa: "/ˈren.ə.veɪt/", meaning: "cải tạo" },
      { word: "restore", ipa: "/rɪˈstɔːr/", meaning: "khôi phục" },
      { word: "enhance", ipa: "/ɪnˈhæns/", meaning: "nâng cao" },
      { word: "implement", ipa: "/ˈɪm.plə.ment/", meaning: "triển khai" },
      { word: "comply", ipa: "/kəmˈplaɪ/", meaning: "tuân thủ" },
      { word: "eligible", ipa: "/ˈel.ɪ.dʒə.bəl/", meaning: "đủ điều kiện" },
      { word: "substantial", ipa: "/səbˈstæn.ʃəl/", meaning: "đáng kể" }
    ]
  },
  "5": {
    title: "Buổi 5 — Ambition & Influence",
    words: [
      { word: "ambition", ipa: "/æmˈbɪʃ.ən/", meaning: "tham vọng" },
      { word: "ambitious", ipa: "/æmˈbɪʃ.əs/", meaning: "đầy tham vọng" },
      { word: "advantage", ipa: "/ədˈvæn.tɪdʒ/", meaning: "lợi thế" },
      { word: "effective", ipa: "/ɪˈfek.tɪv/", meaning: "hiệu quả" },
      { word: "determined", ipa: "/dɪˈtɝː.mɪnd/", meaning: "quyết tâm" },
      { word: "varied", ipa: "/ˈver.id/", meaning: "đa dạng" },
      { word: "demonstrate", ipa: "/ˈdem.ən.streɪt/", meaning: "chứng minh" },
      { word: "influence", ipa: "/ˈɪn.flu.əns/", meaning: "ảnh hưởng" },
      { word: "influential", ipa: "/ˌɪn.fluˈen.ʃəl/", meaning: "có ảnh hưởng" }
    ]
  },
  "6": {
    title: "Buổi 6 — Precision",
    words: [
      { word: "ambiguous", ipa: "/æmˈbɪɡ.ju.əs/", meaning: "mơ hồ" },
      { word: "ambiguity", ipa: "/ˌæm.bɪˈɡjuː.ə.t̬i/", meaning: "sự mơ hồ" },
      { word: "consist", ipa: "/kənˈsɪst/", meaning: "bao gồm" },
      { word: "consistent", ipa: "/kənˈsɪs.tənt/", meaning: "nhất quán" },
      { word: "persist", ipa: "/pɚˈsɪst/", meaning: "kiên trì" },
      { word: "persistence", ipa: "/pɚˈsɪs.təns/", meaning: "sự kiên trì" },
      { word: "resolve", ipa: "/rɪˈzɑːlv/", meaning: "giải quyết" },
      { word: "related", ipa: "/rɪˈleɪ.t̬ɪd/", meaning: "liên quan" },
      { word: "involve", ipa: "/ɪnˈvɑːlv/", meaning: "liên quan / bao gồm" }
    ]
  },
  "7": {
    title: "Buổi 7 — Opportunity & Competence",
    words: [
      { word: "invest", ipa: "/ɪnˈvest/", meaning: "đầu tư" },
      { word: "investment", ipa: "/ɪnˈvest.mənt/", meaning: "sự đầu tư" },
      { word: "familiar", ipa: "/fəˈmɪl.i.ɚ/", meaning: "quen thuộc" },
      { word: "compete", ipa: "/kəmˈpiːt/", meaning: "cạnh tranh" },
      { word: "competent", ipa: "/ˈkɑːm.pə.t̬ənt/", meaning: "có năng lực" },
      { word: "condition", ipa: "/kənˈdɪʃ.ən/", meaning: "điều kiện" },
      { word: "equality", ipa: "/ɪˈkwɑː.lə.t̬i/", meaning: "sự bình đẳng" },
      { word: "privilege", ipa: "/ˈprɪv.əl.ɪdʒ/", meaning: "đặc quyền" },
      { word: "priority", ipa: "/praɪˈɔːr.ə.t̬i/", meaning: "ưu tiên" }
    ]
  },
  "8": {
    title: "Buổi 8 — Commitment",
    words: [
      { word: "allocate", ipa: "/ˈæl.ə.keɪt/", meaning: "phân bổ" },
      { word: "dedicate", ipa: "/ˈded.ɪ.keɪt/", meaning: "cống hiến" },
      { word: "dedicated", ipa: "/ˈded.ɪ.keɪ.t̬ɪd/", meaning: "tận tâm" },
      { word: "commit", ipa: "/kəˈmɪt/", meaning: "cam kết" },
      { word: "committed", ipa: "/kəˈmɪt̬.ɪd/", meaning: "tận tụy" },
      { word: "submit", ipa: "/səbˈmɪt/", meaning: "nộp / phục tùng" },
      { word: "submissive", ipa: "/səbˈmɪs.ɪv/", meaning: "phục tùng" },
      { word: "cause", ipa: "/kɑːz/", meaning: "gây ra / nguyên nhân" },
      { word: "suffer", ipa: "/ˈsʌf.ɚ/", meaning: "chịu đựng" }
    ]
  },
  "9": {
    title: "Buổi 9 — Reasoning",
    words: [
      { word: "assume", ipa: "/əˈsuːm/", meaning: "giả định" },
      { word: "assumption", ipa: "/əˈsʌmp.ʃən/", meaning: "sự giả định" },
      { word: "evidence", ipa: "/ˈev.ɪ.dəns/", meaning: "bằng chứng" },
      { word: "infer", ipa: "/ɪnˈfɝː/", meaning: "suy luận" },
      { word: "conclusion", ipa: "/kənˈkluː.ʒən/", meaning: "kết luận" },
      { word: "evaluate", ipa: "/ɪˈvæl.ju.eɪt/", meaning: "đánh giá" },
      { word: "alternative", ipa: "/ɑːlˈtɝː.nə.t̬ɪv/", meaning: "lựa chọn thay thế" },
      { word: "consequence", ipa: "/ˈkɑːn.sə.kwens/", meaning: "hậu quả" },
      { word: "justify", ipa: "/ˈdʒʌs.tɪ.faɪ/", meaning: "biện minh" }
    ]
  },
  "10": {
    title: "Buổi 10 — Cause & Impact",
    words: [
      { word: "factor", ipa: "/ˈfæk.tɚ/", meaning: "yếu tố" },
      { word: "affect", ipa: "/əˈfekt/", meaning: "ảnh hưởng (động từ)" },
      { word: "effect", ipa: "/ɪˈfekt/", meaning: "ảnh hưởng / kết quả (danh từ)" },
      { word: "influence", ipa: "/ˈɪn.flu.əns/", meaning: "ảnh hưởng" },
      { word: "contribute", ipa: "/kənˈtrɪb.juːt/", meaning: "góp phần" },
      { word: "trigger", ipa: "/ˈtrɪɡ.ɚ/", meaning: "kích hoạt" },
      { word: "outcome", ipa: "/ˈaʊt.kʌm/", meaning: "kết quả" },
      { word: "result", ipa: "/rɪˈzʌlt/", meaning: "kết quả" },
      { word: "impact", ipa: "/ˈɪm.pækt/", meaning: "tác động" }
    ]
  },
  "11": {
    title: "Buổi 11 — Risk & Prevention",
    words: [
      { word: "risk", ipa: "/rɪsk/", meaning: "rủi ro" },
      { word: "mistake", ipa: "/mɪˈsteɪk/", meaning: "lỗi" },
      { word: "avoid", ipa: "/əˈvɔɪd/", meaning: "tránh" },
      { word: "prevent", ipa: "/prɪˈvent/", meaning: "ngăn chặn" },
      { word: "warning", ipa: "/ˈwɔːr.nɪŋ/", meaning: "cảnh báo" },
      { word: "careful", ipa: "/ˈker.fəl/", meaning: "cẩn thận" },
      { word: "check", ipa: "/tʃek/", meaning: "kiểm tra" },
      { word: "fix", ipa: "/fɪks/", meaning: "sửa" },
      { word: "protect", ipa: "/prəˈtekt/", meaning: "bảo vệ" }
    ]
  },
  "12": {
    title: "Buổi 12 — Comparison",
    words: [
      { word: "compare", ipa: "/kəmˈper/", meaning: "so sánh" },
      { word: "contrast", ipa: "/ˈkɑːn.træst/", meaning: "đối chiếu" },
      { word: "similar", ipa: "/ˈsɪm.ə.lɚ/", meaning: "tương tự" },
      { word: "different", ipa: "/ˈdɪf.ɚ.ənt/", meaning: "khác biệt" },
      { word: "advantage", ipa: "/ədˈvæn.tɪdʒ/", meaning: "lợi thế" },
      { word: "disadvantage", ipa: "/ˌdɪs.ədˈvæn.tɪdʒ/", meaning: "bất lợi" },
      { word: "criteria", ipa: "/kraɪˈtɪr.i.ə/", meaning: "tiêu chí" },
      { word: "suitable", ipa: "/ˈsuː.t̬ə.bəl/", meaning: "phù hợp" },
      { word: "prefer", ipa: "/prɪˈfɝː/", meaning: "thích hơn" }
    ]
  },
  "13": {
    title: "Buổi 13 — Strategy & Execution",
    words: [
      { word: "strategy", ipa: "/ˈstræt̬.ə.dʒi/", meaning: "chiến lược" },
      { word: "approach", ipa: "/əˈproʊtʃ/", meaning: "cách tiếp cận" },
      { word: "objective", ipa: "/əbˈdʒek.tɪv/", meaning: "mục tiêu cụ thể" },
      { word: "initiative", ipa: "/ɪˈnɪʃ.ə.t̬ɪv/", meaning: "sáng kiến" },
      { word: "implement", ipa: "/ˈɪm.plə.ment/", meaning: "triển khai" },
      { word: "execute", ipa: "/ˈek.sə.kjuːt/", meaning: "thực hiện" },
      { word: "monitor", ipa: "/ˈmɑː.nə.t̬ɚ/", meaning: "theo dõi" },
      { word: "adjust", ipa: "/əˈdʒʌst/", meaning: "điều chỉnh" },
      { word: "efficient", ipa: "/ɪˈfɪʃ.ənt/", meaning: "hiệu quả (thời gian/công sức)" }
    ]
  },
  "14": {
    title: "Buổi 14 — Negotiation & Persuasion",
    words: [
      { word: "negotiate", ipa: "/nɪˈɡoʊ.ʃi.eɪt/", meaning: "thương lượng, đàm phán" },
      { word: "persuade", ipa: "/pɚˈsweɪd/", meaning: "thuyết phục" },
      { word: "persuasive", ipa: "/pɚˈsweɪ.sɪv/", meaning: "có sức thuyết phục" },
      { word: "propose", ipa: "/prəˈpoʊz/", meaning: "đề xuất" },
      { word: "compromise", ipa: "/ˈkɑːm.prə.maɪz/", meaning: "thỏa hiệp" },
      { word: "concede", ipa: "/kənˈsiːd/", meaning: "nhượng bộ / thừa nhận" },
      { word: "leverage", ipa: "/ˈlev.ɚ.ɪdʒ/", meaning: "đòn bẩy / lợi thế" },
      { word: "reconcile", ipa: "/ˈrek.ən.saɪl/", meaning: "hòa giải / dung hòa" },
      { word: "consensus", ipa: "/kənˈsen.səs/", meaning: "sự đồng thuận" }
    ]
  },
  "15": {
    title: "Buổi 15 — Problem-Solving & Innovation",
    words: [
      { word: "innovate", ipa: "/ˈɪn.ə.veɪt/", meaning: "đổi mới" },
      { word: "innovative", ipa: "/ˈɪn.ə.veɪ.tɪv/", meaning: "mang tính đổi mới" },
      { word: "streamline", ipa: "/ˈstriːm.laɪn/", meaning: "tinh giản quy trình" },
      { word: "diagnose", ipa: "/ˈdaɪ.əɡ.noʊz/", meaning: "chẩn đoán / tìm gốc vấn đề" },
      { word: "optimize", ipa: "/ˈɑːp.tə.maɪz/", meaning: "tối ưu hóa" },
      { word: "breakthrough", ipa: "/ˈbreɪk.θruː/", meaning: "bước đột phá" },
      { word: "feasible", ipa: "/ˈfiː.zə.bəl/", meaning: "khả thi" },
      { word: "overcome", ipa: "/ˌoʊ.vɚˈkʌm/", meaning: "vượt qua / khắc phục" },
      { word: "resourceful", ipa: "/rɪˈsɔːrs.fəl/", meaning: "tháo vát" }
    ]
  },
  "16": {
    title: "Buổi 16 — Leadership & Delegation",
    words: [
      { word: "delegate", ipa: "/ˈdel.ə.ɡeɪt/", meaning: "ủy quyền / giao việc" },
      { word: "supervise", ipa: "/ˈsuː.pɚ.vaɪz/", meaning: "giám sát trực tiếp" },
      { word: "oversee", ipa: "/ˌoʊ.vɚˈsiː/", meaning: "trông coi cấp cao" },
      { word: "empower", ipa: "/ɪmˈpaʊ.ɚ/", meaning: "trao quyền" },
      { word: "accountable", ipa: "/əˈkaʊn.t̬ə.bəl/", meaning: "có trách nhiệm giải trình" },
      { word: "authorize", ipa: "/ˈɑː.θɚ.aɪz/", meaning: "cho phép chính thức" },
      { word: "mentor", ipa: "/ˈmen.tɔːr/", meaning: "cố vấn / dìu dắt" },
      { word: "coordinate", ipa: "/koʊˈɔːr.də.neɪt/", meaning: "phối hợp / điều phối" },
      { word: "endorse", ipa: "/ɪnˈdɔːrs/", meaning: "ủng hộ chính thức" }
    ]
  },
  "17": {
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
};