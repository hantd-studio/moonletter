"""Sinh index.html (trang chủ song ngữ) từ nội dung bên dưới. Sửa chữ ở đây rồi chạy: python3 tools/gen_home.py"""
import html
import os

ICON = {
    "account": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="3.5"/><path d="M5 20c1.2-3.5 4-5 7-5s5.8 1.5 7 5"/><path d="M4 4l16 16"/></svg>',
    "device": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M10.5 18.5h3"/></svg>',
    "faceid": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 8V6a2 2 0 0 1 2-2h2M16 4h2a2 2 0 0 1 2 2v2M20 16v2a2 2 0 0 1-2 2h-2M8 20H6a2 2 0 0 1-2-2v-2"/><path d="M9 9.5v1M15 9.5v1M12 9.5v3.5h-1M9.5 15.5c1.4 1 3.6 1 5 0"/></svg>',
    "noads": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M6 6l12 12"/></svg>',
}

T = {
    "en": dict(
        store="https://apps.apple.com/app/id6832021926",
        nav=[("features", "Features"), ("privacy", "Privacy"), ("pricing", "Pricing"), ("support", "Support")],
        get="Get the app",
        badge=("Download on the", "App Store"),
        h1="Some words are better written than sent.",
        sub="Unsent letters, a no-contact counter and an SOS for the urge to text. For the days after a breakup.",
        free="Free to use. Better with Pro.",
        trust=[("account", "No account"), ("noads", "No ads"), ("device", "Nothing leaves your iPhone")],
        alts=["Writing an unsent letter", "Typing a text that is never sent", "No-contact day counter", "SOS: breathe for one minute"],
        rows=[
            ("1", "Unsent letters", "Write the letter you'll never send.",
             ["Say it all, to them, to yourself, or to who you used to be. Gentle prompts help when you don't know where to start.",
              "Seal it when you're done. Lock it for 30 days and read it again when you're stronger."]),
            ("3", "Text without sending", "Type the text. Then keep it.",
             ["It's 2 a.m. and you want to message them. Type it here instead, like a real chat. It never leaves the app."]),
            ("4", "No contact", "A slip is noted, never a reset to zero.",
             ["Count the days since you last talked, with milestones at 3, 7, 14, 30, 60 and 90 days. One hard night doesn't erase the progress you've made."]),
            ("5", "SOS", "When the urge hits, breathe first.",
             ["One tap: a minute of slow breathing, then the reasons you wrote yourself. Then write instead of texting. SOS is always free."]),
            ("2", "Share", "Keep a line. Share it if you want.",
             ["Turn a few sentences of a sealed letter into an image. Their name is always hidden."]),
        ],
        priv_h="Private by design",
        priv_p="Moonletter has no server to send your words to. What you write stays yours.",
        points=[("account", "No account", "No sign-up, no email."),
                ("device", "On your iPhone", "Letters and texts are never uploaded."),
                ("faceid", "Face ID lock", "Lock the app if you want."),
                ("noads", "No ads", "We never sell data.")],
        price_h="Free to start",
        plans=[("Free", "The no-contact counter, milestones and SOS, forever. Plus 1 letter, 3 unsent texts and 3 prompts."),
               ("Pro", "Unlimited letters and unsent texts, all 20 prompts and the 30-day lock. Pay once for Lifetime, or go monthly or weekly.")],
        close="Write it here. Not to them.",
        note="Moonletter is not therapy and does not promise to bring anyone back. If you are in danger or thinking about harming yourself, call your local emergency number right away.",
        sup_h="Support",
        sup_p='Questions, problems or feedback: <a href="mailto:support.moonletter@gmail.com">support.moonletter@gmail.com</a>. We usually reply within a few days.',
        sup=[("Restore Pro on a new phone:", "open the upgrade screen and tap Restore purchases."),
             ("Cancel a subscription:", "iOS Settings › [your name] › Subscriptions."),
             ("Delete your data:", "in the app, Settings › Delete all data.")],
        privacy_link=("privacy.html", "Privacy Policy"),
        terms_link=("terms.html", "Terms of Use"),
    ),
    "vi": dict(
        store="https://apps.apple.com/vn/app/id6832021926",
        nav=[("features", "Tính năng"), ("privacy", "Riêng tư"), ("pricing", "Giá"), ("support", "Hỗ trợ")],
        get="Tải app",
        badge=("Tải về trên", "App Store"),
        h1="Có những lời viết ra thì nhẹ hơn là gửi đi.",
        sub="Thư không gửi, đếm ngày không liên lạc và SOS khi muốn nhắn tin. Cho những ngày sau chia tay.",
        free="Dùng miễn phí. Đầy đủ hơn với Pro.",
        trust=[("account", "Không cần tài khoản"), ("noads", "Không quảng cáo"), ("device", "Không gì rời khỏi iPhone")],
        alts=["Viết thư không gửi", "Gõ tin nhắn không bao giờ gửi đi", "Đếm ngày không liên lạc", "SOS: thở chậm một phút"],
        rows=[
            ("1", "Thư không gửi", "Viết lá thư bạn sẽ không bao giờ gửi.",
             ["Nói hết, với người ấy, với chính mình, hay với con người cũ của bạn. Có gợi ý nhẹ nhàng khi chưa biết bắt đầu từ đâu.",
              "Niêm phong khi viết xong. Khoá thư 30 ngày rồi đọc lại khi bạn đã vững hơn."]),
            ("3", "Nhắn mà không gửi", "Gõ tin nhắn. Rồi giữ nó lại.",
             ["Hai giờ sáng, bạn muốn nhắn cho người ấy. Hãy gõ ở đây, như một cuộc trò chuyện thật. Không gì rời khỏi ứng dụng."]),
            ("4", "Không liên lạc", "Lỡ một lần, không bao giờ về số 0.",
             ["Đếm số ngày từ lần cuối hai người nói chuyện, có mốc 3, 7, 14, 30, 60 và 90 ngày. Một đêm khó khăn không xoá đi những gì bạn đã cố gắng."]),
            ("5", "SOS", "Khi muốn nhắn, hãy thở trước.",
             ["Một chạm: một phút thở chậm, rồi đọc lại những lý do chính bạn đã viết. Sau đó viết thay vì nhắn. SOS luôn miễn phí."]),
            ("2", "Chia sẻ", "Giữ một câu. Chia sẻ nếu bạn muốn.",
             ["Biến vài câu trong lá thư đã niêm phong thành ảnh. Tên người ấy luôn được ẩn."]),
        ],
        priv_h="Riêng tư ngay từ đầu",
        priv_p="Moonletter không có máy chủ nào để gửi lời của bạn tới. Những gì bạn viết là của bạn.",
        points=[("account", "Không tài khoản", "Không đăng ký, không cần email."),
                ("device", "Trên iPhone của bạn", "Thư và tin nhắn không bao giờ được tải lên."),
                ("faceid", "Khoá bằng Face ID", "Khoá ứng dụng nếu bạn muốn."),
                ("noads", "Không quảng cáo", "Không bao giờ bán dữ liệu.")],
        price_h="Bắt đầu miễn phí",
        plans=[("Miễn phí", "Đếm ngày không liên lạc, các mốc và SOS, mãi mãi. Kèm 1 lá thư, 3 lần nhắn mà không gửi và 3 gợi ý."),
               ("Pro", "Thư và nhắn mà không gửi không giới hạn, đủ 20 gợi ý và khoá thư 30 ngày. Trả một lần cho gói Trọn đời, hoặc chọn gói tháng hay gói tuần.")],
        close="Viết ở đây. Đừng gửi cho người ấy.",
        note="Moonletter không phải liệu pháp tâm lý và không hứa giúp bạn quay lại với ai. Nếu bạn gặp nguy hiểm hoặc có ý định tự làm hại mình, hãy gọi ngay số khẩn cấp tại nơi bạn ở.",
        sup_h="Hỗ trợ",
        sup_p='Câu hỏi, lỗi hoặc góp ý: <a href="mailto:support.moonletter@gmail.com">support.moonletter@gmail.com</a>. Chúng tôi thường trả lời trong vài ngày.',
        sup=[("Mở lại Pro trên máy mới:", "mở màn nâng cấp và bấm Khôi phục giao dịch."),
             ("Huỷ gói đăng ký:", "Cài đặt iOS › [tên bạn] › Đăng ký."),
             ("Xoá dữ liệu:", "trong ứng dụng, Cài đặt › Xoá toàn bộ dữ liệu.")],
        privacy_link=("privacy.html#vi", "Chính sách quyền riêng tư"),
        terms_link=("terms.html#vi", "Điều khoản sử dụng"),
    ),
}

LAZY = ' loading="lazy"'


def article(lang):
    t = T[lang]
    p = "" if lang == "en" else "vi-"

    def shot(n, alt, lazy=True):
        return (f'<div class="phone"><img src="img/raw-{lang}-{n}.jpg" width="598" height="1300" '
                f'alt="{html.escape(alt)}"{LAZY if lazy else ""}></div>')

    badge = f'<a class="badge" href="{t["store"]}"><small>{t["badge"][0]}</small><span>{t["badge"][1]}</span></a>'
    o = [f'<article id="{lang}" lang="{lang}">',
         '<nav class="nav"><div class="wrap">',
         '<a class="brand" href="./"><img src="logo.png" alt="">Moonletter</a>',
         '<div class="links">' + "".join(f'<a href="#{p}{i}">{n}</a>' for i, n in t["nav"]) + '</div>',
         '<div class="lang"><a href="#en">EN</a><a href="#vi">VI</a></div>',
         f'<a class="get" href="{t["store"]}">{t["get"]}</a>',
         '</div></nav>',
         '<header class="hero"><div class="wrap">',
         f'<h1>{t["h1"]}</h1>',
         f'<p class="sub">{t["sub"]}</p>',
         badge,
         f'<p class="free">{t["free"]}</p>',
         '<ul class="trust">' + "".join(f'<li>{ICON[i]}{x}</li>' for i, x in t["trust"]) + '</ul>',
         # Giữa: lá thư (có chữ ngay đầu màn); hai bên: đếm ngày, SOS. Màn nhắn để ở phần tính năng (tin nằm cuối màn).
         '<div class="stage">' + shot("4", t["alts"][2], False) + shot("1", t["alts"][0], False)
         + shot("5", t["alts"][3], False) + '</div>',
         '</div></header>',
         f'<section class="features" id="{p}features"><div class="wrap">']
    for n, k, h, ps in t["rows"]:
        o.append('<div class="row"><div class="copy">' + f'<p class="kicker">{k}</p><h2>{h}</h2>'
                 + "".join(f'<p>{x}</p>' for x in ps) + '</div>' + shot(n, h) + '</div>')
    o += ['</div></section>',
          f'<section class="privacy" id="{p}privacy"><div class="wrap">',
          f'<h2>{t["priv_h"]}</h2><p>{t["priv_p"]}</p>',
          '<ul class="points">' + "".join(f'<li>{ICON[i]}<b>{b}</b><span>{s}</span></li>' for i, b, s in t["points"]) + '</ul>',
          '</div></section>',
          f'<section class="pricing" id="{p}pricing"><div class="wrap">',
          f'<h2>{t["price_h"]}</h2><div class="plans">' + "".join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a, b in t["plans"]) + '</div>',
          '</div></section>',
          '<section class="closing"><div class="wrap">',
          f'<h2>{t["close"]}</h2>{badge}<p class="note">{t["note"]}</p>',
          '</div></section>',
          f'<section class="support" id="{p}support"><div class="wrap">',
          f'<h2>{t["sup_h"]}</h2><p>{t["sup_p"]}</p><ul>' + "".join(f'<li><strong>{a}</strong> {b}</li>' for a, b in t["sup"]) + '</ul>',
          '</div></section>',
          f'<footer><div class="wrap"><span>© 2026 Moonletter</span><a href="{t["privacy_link"][0]}">{t["privacy_link"][1]}</a>'
          f'<a href="{t["terms_link"][0]}">{t["terms_link"][1]}</a>'
          '<a href="mailto:support.moonletter@gmail.com">support.moonletter@gmail.com</a></div></footer>',
          '</article>']
    return "\n".join(o)


HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Moonletter: Unsent Letters After a Breakup</title>
<meta name="description" content="A quiet iPhone app for the days after a breakup: write unsent letters, type the text you'll never send, count your no-contact days and get through the urge with SOS. Free, no account, nothing leaves your phone.">
<link rel="canonical" href="https://hantd-studio.github.io/moonletter/">
<link rel="icon" href="logo.png">
<link rel="apple-touch-icon" href="logo.png">
<link rel="preload" href="fonts/BeVietnamPro-Bold.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="home.css">
<!-- iPhone Safari: thanh "Tải" của App Store ở đầu trang. -->
<meta name="apple-itunes-app" content="app-id=6832021926">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Moonletter">
<meta property="og:title" content="Moonletter: Unsent Letters After a Breakup">
<meta property="og:description" content="Write what you can't say. Get through the urge to text. Count your no-contact days. Free on iPhone, nothing leaves your phone.">
<meta property="og:url" content="https://hantd-studio.github.io/moonletter/">
<meta property="og:image" content="https://hantd-studio.github.io/moonletter/img/og-en.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MobileApplication",
  "name": "Moonletter: Breakup Letters",
  "operatingSystem": "iOS",
  "applicationCategory": "HealthApplication",
  "description": "Unsent letters, an unsent text drafter, a no-contact day counter and an SOS breathing exercise for the days after a breakup.",
  "url": "https://hantd-studio.github.io/moonletter/",
  "downloadUrl": "https://apps.apple.com/app/id6832021926",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
  "author": { "@type": "Person", "name": "Hant D" }
}
</script>
<script>
  // Song ngữ: #vi / #en chọn ngôn ngữ (link trong app mở /#vi); không có thì theo ngôn ngữ trình duyệt.
  // Link nội trang (#features…) không đổi ngôn ngữ.
  (function () {
    var root = document.documentElement;
    function apply() {
      if (location.hash === "#vi") root.classList.add("vi");
      else if (location.hash === "#en") root.classList.remove("vi");
      root.lang = root.classList.contains("vi") ? "vi" : "en";
    }
    if (!location.hash && (navigator.language || "").toLowerCase().indexOf("vi") === 0) root.classList.add("vi");
    apply();
    addEventListener("hashchange", apply);
  })();
</script>
</head>
<body>
'''

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "index.html")
    with open(out, "w") as f:
        f.write(HEAD + article("en") + "\n\n" + article("vi") + "\n</body>\n</html>\n")
    print("wrote", os.path.normpath(out))
