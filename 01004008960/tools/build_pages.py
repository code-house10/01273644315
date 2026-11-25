# -*- coding: utf-8 -*-
"""
مولّد صفحات نقل العفش (RTL).
التشغيل من داخل مجلد المشروع:   python tools/build_pages.py
يكتب index.html وصفحات الكلمات المفتاحية في جذر المشروع.
عدّل الإعدادات في الأعلى (الاسم/الرقم) ثم أعد التشغيل.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BRAND = "خدمات نقل العفش"          # اسم مؤقت - غيّره لاسم نشاطك
BRAND_SUB = "نقل • ونش • تغليف"
PHONE = "01042723928"
PHONE_INTL = "+201042723928"
WHATSAPP = "201042723928"           # افتراض: نفس الرقم عليه واتساب
HOURS = "يومياً من 8 صباحاً حتى 10 مساءً"   # افتراض - عدّله
IMG = "assets/images/moving/"

# ---------------- أيقونات SVG ----------------
I = {
 "phone": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>',
 "wa": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.7.3-.2.3-.9.9-.9 2.1s.9 2.5 1 2.6c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>',
 "truck": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h11v9h1V8h3.6L22 12v5h-2a2.5 2.5 0 0 1-5 0H9a2.5 2.5 0 0 1-5 0H2V6a1 1 0 0 1 1-1zm13 5v3h4.3L18 10h-2zM6.5 16.2a1.3 1.3 0 1 0 0 2.6 1.3 1.3 0 0 0 0-2.6zm11 0a1.3 1.3 0 1 0 0 2.6 1.3 1.3 0 0 0 0-2.6z"/></svg>',
 "check": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z"/></svg>',
 "pin": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5z"/></svg>',
 "clock": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm1 10.4 3.5 2.1-.8 1.3L11 13V7h2z"/></svg>',
 "shield": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2 4 5v6c0 5 3.4 9.7 8 11 4.6-1.3 8-6 8-11V5l-8-3zm-1.2 14.2-3.5-3.5 1.4-1.4 2.1 2.1 4.6-4.6 1.4 1.4-6 6z"/></svg>',
 "box": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2 3 6.5v11L12 22l9-4.5v-11L12 2zm0 2.2 6.6 3.3L12 10.8 5.4 7.5 12 4.2zM5 9.1l6 3v7.4l-6-3V9.1zm8 10.4v-7.4l6-3v7.4l-6 3z"/></svg>',
 "crane": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 21V9l9-6h2v2h-1.4L8 8.7V21H4zm6-12 9-5v2l-7.5 4.2H10zm9 0h2v5h-1v2a2 2 0 1 1-2-2h1v-5zM10 21v-2h11v2H10z"/></svg>',
 "users": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zm7 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM9 13c-3.3 0-7 1.6-7 4v3h14v-3c0-2.4-3.7-4-7-4zm7 0c-.4 0-.8 0-1.2.1 1.3.9 2.2 2.2 2.2 3.9v3h5v-3c0-2.4-3.4-4-6-4z"/></svg>',
}

# ---------------- الصور ----------------
PHOTOS = [
 ("winch-lift-villa", "ونش رفع العفش على فيلا"),
 ("winch-lift-building", "ونش رفع عفش للأدوار العالية"),
 ("winch-lift-truck", "ونش رفع وعربية نقل عفش أمام عمارة"),
 ("loading-wrapped-furniture", "تحميل العفش بعد التغليف"),
 ("wrapped-furniture-room", "تغليف الأثاث داخل الشقة"),
 ("furniture-wrapping-salon", "تغليف الأنتريه والصالون"),
 ("packing-team-living-room", "فريق التغليف أثناء العمل"),
 ("truck-loaded-inside", "رص العفش داخل العربية المغلقة"),
 ("moving-work-collage", "مراحل نقل العفش من الفك للتحميل"),
 ("trucks-residential", "عربيات نقل العفش في المناطق السكنية"),
 ("truck-fleet-row", "أسطول عربيات نقل العفش"),
 ("truck-fleet-yard", "عربيات نقل عفش مغلقة جاهزة"),
 ("trucks-street-buildings", "عربيات نقل العفش أمام العمارات"),
]
PH = dict(PHOTOS)

def img(name, alt, cls="", lazy=True, w=800, h=1000):
    l = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="{IMG}{name}.jpg" alt="{alt}" width="{w}" height="{h}"{c}{l}>'

# ---------------- الصفحات ----------------
LOCATIONS = [
 dict(slug="naql-afsh-madinet-nasr", area="مدينة نصر", hero="trucks-residential", about_img="winch-lift-truck",
  points=["الحي السابع والحي الثامن والحي العاشر","شارع عباس العقاد ومكرم عبيد","مصطفى النحاس والطيران","زهراء مدينة نصر والمنطقة التاسعة","المنطقة السادسة ورابعة العدوية","عمارات المساكن والأبراج العالية"],
  local="مدينة نصر من أكثر مناطق القاهرة زحاماً، وأغلب عماراتها أدوار عالية وسلالمها ضيقة. عشان كده بنحدد ميعاد التحميل في أوقات أخف للشارع، وبنستخدم ونش رفع العفش للأدوار العالية بدل ما القطع الكبيرة تتعطل على السلم، وبنركن العربية في أقرب مكان للعمارة بدون ما نعطل الجيران.",
  faq=("هل تنقلون من مدينة نصر لأي منطقة تانية؟","أيوه، بننقل من مدينة نصر لكل مناطق القاهرة والجيزة: التجمع، مدينتي، المعادي، أكتوبر، الشيخ زايد والمقطم، وكمان العكس.")),
 dict(slug="naql-afsh-tagamoa-5", area="التجمع الخامس", hero="winch-lift-villa", about_img="wrapped-furniture-room",
  points=["النرجس والياسمين والبنفسج","اللوتس الشمالية والجنوبية","الحي الأول والثالث والخامس","جنوب الأكاديمية وشارع التسعين","الكمبوندات المغلقة والفيلات","مستشفى الجوي ومحور محمد نجيب"],
  local="في التجمع الخامس أغلب السكن فيلات وكمبوندات ووحدات واسعة فيها أثاث كبير ومطابخ ودريسنج. بننسق مع أمن الكمبوند على ميعاد الدخول، وبنستخدم ونش رفع العفش للفيلات والأدوار العليا، وبنغلف الرخام والزجاج والتحف بعناية زيادة.",
  faq=("هل تدخلون الكمبوندات في التجمع الخامس؟","أيوه، بنتعامل مع الكمبوندات بشكل مستمر. كل اللي محتاجه تبلغ الأمن أو الإدارة بميعاد النقل، واحنا بنلتزم بمواعيدهم وتعليماتهم.")),
 dict(slug="naql-afsh-madinaty", area="مدينتي", hero="trucks-street-buildings", about_img="packing-team-living-room",
  points=["مجموعات العمارات B1 لحد B15","الفيلات والتاون هاوس","البوابات الرئيسية ومداخل المجموعات","المول والمنطقة الخدمية","الشقق الجديدة واستلام الوحدات","النقل من وإلى مدينتي"],
  local="مدينتي ليها نظام دخول وتصاريح خاص للعربيات وعمال النقل. بنساعدك تجهز تصريح النقل من إدارة المدينة، وبنلتزم بالمواعيد المسموحة للتحميل، وبنستخدم عربيات مغلقة وونش رفع للعمارات والفيلات عشان الشغل يخلص بسرعة ومن غير مشاكل.",
  faq=("محتاج تصريح عشان أنقل عفشي في مدينتي؟","غالباً أيوه، مدينتي بتطلب تصريح من إدارة المدينة قبل النقل. اتصل بينا وهنقولك الخطوات ونرتب الميعاد على حسب التصريح.")),
 dict(slug="naql-afsh-maadi", area="المعادي", hero="furniture-wrapping-salon", about_img="winch-lift-building",
  points=["المعادي السرايات وشارع 9","دجلة وزهراء المعادي","المعادي الجديدة والبساتين","كورنيش المعادي","الفيلات القديمة والشقق الواسعة","النقل من المعادي لأي مكان"],
  local="المعادي فيها فيلات قديمة وشقق واسعة بأثاث كلاسيك تقيل، وشوارع ضيقة وأشجار في بعض المناطق. بنعاين المكان قبل النقل، وبنستخدم ونش رفع العفش لما السلم أو المدخل ما يستحملش القطع الكبيرة، وبنغلف الأنتيكات والخشب الكلاسيك بطبقات حماية.",
  faq=("عندي أثاث كلاسيك تقيل في المعادي، تقدروا تنقلوه؟","أيوه، الأثاث الكلاسيك والبيانو والنيش والسفرة التقيلة بنفكها بعناية ونغلفها، ولو السلم ضيق بنستخدم الونش من البلكونة أو الشباك.")),
 dict(slug="naql-afsh-october", area="6 أكتوبر", hero="truck-fleet-row", about_img="trucks-residential",
  points=["الأحياء السكنية والحي المتميز","الحصري ومنطقة المحور","حدائق أكتوبر","المدن الجامعية وسكن الطلاب","الكمبوندات والفيلات","النقل بين أكتوبر والقاهرة"],
  local="مدينة 6 أكتوبر واسعة والمسافات فيها كبيرة، وكتير من النقل بيكون منها للقاهرة أو العكس. بنحدد الطريق والميعاد المناسب عشان نتجنب زحمة المحور والدائري، وعندنا عربيات مقاسات مختلفة تناسب الشقة الصغيرة أو الفيلا الكاملة.",
  faq=("بتنقلوا من أكتوبر للقاهرة في نفس اليوم؟","أيوه، النقل من أكتوبر لأي منطقة في القاهرة أو الجيزة بيخلص في نفس اليوم في أغلب الحالات حسب حجم العفش.")),
 dict(slug="naql-afsh-sheikh-zayed", area="الشيخ زايد", hero="winch-lift-truck", about_img="wrapped-furniture-room",
  points=["أحياء الشيخ زايد السكنية","بيفرلي هيلز والكمبوندات","الفيلات والتوين هاوس","المنطقة المركزية والمولات","زايد الجديدة","النقل بين زايد وأكتوبر والقاهرة"],
  local="في الشيخ زايد أغلب الوحدات فيلات وكمبوندات بأثاث مودرن كبير وأجهزة غالية. بنغلف الأجهزة الكهربائية والشاشات بالفوم والكرتون، وبننسق مع أمن الكمبوند على الدخول، وبنستخدم ونش رفع العفش لما يكون الدور عالي أو المدخل ضيق.",
  faq=("هل تنقلون داخل كمبوندات الشيخ زايد؟","أيوه، بنشتغل داخل كمبوندات الشيخ زايد وبنلتزم بمواعيد ونظام الأمن في كل كمبوند.")),
 dict(slug="naql-afsh-mokattam", area="المقطم", hero="winch-lift-building", about_img="loading-wrapped-furniture",
  points=["الهضبة الوسطى والهضبة العليا","شارع 9 وشارع 10 وشارع 77","منطقة النافورة","مدينة الملاك","العمارات العالية والأبراج","النقل من المقطم لكل المناطق"],
  local="المقطم منطقة مرتفعة وطرقها فيها طلوع ونزول، وأغلب العمارات أدوار متعددة. بنستخدم عربيات بحالة ممتازة وسواقين متعودين على طرق الهضبة، وونش رفع العفش للأدوار العالية عشان القطع الكبيرة تنزل بأمان وبسرعة.",
  faq=("الطريق للمقطم بيأثر على سعر نقل العفش؟","السعر بيتحدد على حسب حجم العفش والدور والمسافة ومحتاج ونش ولا لأ. اتصل بينا وهنديك سعر واضح قبل التحميل.")),
]

GENERIC = [
 dict(slug="naql-afsh", kw="نقل عفش", hero="truck-fleet-yard", about_img="loading-wrapped-furniture",
  title="نقل عفش | ونش وتغليف وعمالة مدربة | اتصل 01042723928",
  desc="نقل عفش بالقاهرة والجيزة مع تغليف كامل وونش رفع وفك وتركيب بعمالة مدربة وعربيات مغلقة. اتصل الآن 01042723928 واحجز ميعادك.",
  h1="<em>نقل عفش</em> آمن وسريع من باب لباب",
  lead="خدمة نقل عفش متكاملة: فك وتغليف وتحميل ونقل وتركيب، بفريق مدرب وعربيات مغلقة وونش رفع للأدوار العالية. اتصل واحجز ميعادك النهاردة.",
  about_t="نقل عفش بيتك من غير قلق",
  about=["نقل عفش البيت مش مجرد تحميل وتنزيل. إحنا بنبدأ بمعاينة وعرض سعر واضح، وبعدين فك الأثاث وتغليفه بالفوم والاستريتش والكرتون، ورصه في عربية مغلقة بطريقة تمنع الاحتكاك.","في المكان الجديد بنركب الأثاث ونرجعه زي ما كان، وبنتأكد معاك إن كل قطعة وصلت سليمة. خدمة نقل عفش واحدة بتغنيك عن التعامل مع عمال وعربيات وونش كل واحد لوحده."]),
 dict(slug="naql-al-afsh", kw="نقل العفش", hero="wrapped-furniture-room", about_img="furniture-wrapping-salon",
  title="نقل العفش بالقاهرة والجيزة | تغليف وونش | 01042723928",
  desc="نقل العفش بأمان مع تغليف احترافي وفك وتركيب وونش رفع للأدوار العالية. سعر واضح قبل التحميل. اتصل 01042723928.",
  h1="<em>نقل العفش</em> بدون خدش ولا تعب",
  lead="سيب علينا نقل العفش كله: من فك الدولاب وتغليف الأنتريه لحد تركيب المطبخ في بيتك الجديد. شغل منظم وعمالة مدربة ومواعيد مضبوطة.",
  about_t="ليه نقل العفش معانا مختلف؟",
  about=["أكتر حاجة بتقلق الناس في نقل العفش هي الخدوش والكسر والضياع. عشان كده كل قطعة بتتغلف لوحدها، والأجهزة الكهربائية بتتحط في كراتين وفوم، والزجاج والمرايات ليهم تغليف خاص.","وبنعمل حصر للعفش قبل التحميل، ونرص العربية بالترتيب اللي يسهل التنزيل والتركيب، عشان نقل العفش يخلص في أقل وقت."]),
 dict(slug="sharika-li-naql-al-afsh", kw="شركة لنقل العفش", hero="trucks-street-buildings", about_img="packing-team-living-room",
  title="شركة لنقل العفش بالقاهرة | عمالة مدربة وونش | 01042723928",
  desc="بتدور على شركة لنقل العفش تثق فيها؟ تغليف كامل، فك وتركيب، ونش رفع، وعربيات مغلقة في كل مناطق القاهرة والجيزة. اتصل 01042723928.",
  h1="<em>شركة لنقل العفش</em> تعتمد عليها في كل خطوة",
  lead="لو بتدور على شركة لنقل العفش بأسعار واضحة ومواعيد مضبوطة، فريقنا جاهز يعاين ويغلف وينقل ويركب، وانت مرتاح.",
  about_t="إزاي تختار شركة لنقل العفش؟",
  about=["الشركة الصح لنقل العفش هي اللي عندها عربيات مغلقة نضيفة، وعمالة متدربة على الفك والتركيب، وونش رفع للأدوار العالية، وبتديك سعر واضح قبل ما تبدأ.","ده بالظبط اللي بنقدمه: فريق واحد مسؤول عن نقل عفشك من أول مكالمة لحد آخر قطعة تتركب في مكانها."]),
 dict(slug="winch-rafa-al-afsh", kw="ونش رفع العفش", hero="winch-lift-building", about_img="winch-lift-villa",
  title="ونش رفع العفش للأدوار العالية | متاح يومياً | 01042723928",
  desc="ونش رفع العفش للأدوار العالية والفيلات والسلالم الضيقة. رفع وتنزيل آمن للأثاث الكبير والأجهزة بفريق مدرب. اتصل 01042723928.",
  h1="<em>ونش رفع العفش</em> للأدوار العالية بأمان",
  lead="عندك دور عالي أو سلم ضيق أو قطعة أكبر من الباب؟ ونش رفع العفش بيطلع وينزل الأثاث من البلكونة أو الشباك بسرعة وبدون خدش.",
  about_t="إمتى تحتاج ونش رفع العفش؟",
  about=["ونش رفع العفش هو الحل لما يكون السلم ضيق أو الأسانسير صغير أو الدور عالي، أو لما عندك قطع كبيرة زي الكنب والدواليب والثلاجات اللي ما ينفعش تعدي من المدخل.","الونش بيختصر وقت النقل لأكتر من النص، وبيقلل احتمالية خدش الحيطان والأثاث. وبنغلف كل قطعة قبل ما تتحط على الونش ونأمنها كويس."]),
 dict(slug="sharikat-naql-afsh", kw="شركة نقل عفش", hero="truck-fleet-row", about_img="truck-loaded-inside",
  title="شركة نقل عفش بالقاهرة والجيزة | عربيات مغلقة | 01042723928",
  desc="شركة نقل عفش بعربيات مغلقة وعمالة مدربة وتغليف كامل وونش رفع. نقل شقق وفيلات ومكاتب. اتصل الآن 01042723928.",
  h1="<em>شركة نقل عفش</em> بعربيات مغلقة وعمالة مدربة",
  lead="شركة نقل عفش بتشتغل في كل مناطق القاهرة والجيزة، عندها أسطول عربيات مغلقة بمقاسات مختلفة وونش رفع وفريق تغليف وفك وتركيب.",
  about_t="شركة نقل عفش عندها كل اللي محتاجه",
  about=["مع شركة نقل عفش واحدة مش هتحتاج تدور على عربية وعمال وونش ونجار كل واحد لوحده. كل ده موجود عندنا وبيشتغل بتنسيق واحد.","عربياتنا مغلقة ومقاساتها مختلفة تناسب الاستوديو والشقة والفيلا والمكتب، وفريقنا بيرص العفش جواها بطريقة تحميه طول الطريق."]),
]

for L in LOCATIONS:
    a = L["area"]; kw = "نقل عفش " + a
    L.update(kw=kw,
      title=f"{kw} | ونش وتغليف وفك وتركيب | 01042723928",
      desc=f"{kw} بفريق مدرب وعربيات مغلقة وتغليف كامل وونش رفع للأدوار العالية. خدمة سريعة لكل مناطق {a}. اتصل الآن 01042723928.",
      h1=f"<em>{kw}</em> بسرعة وأمان",
      lead=f"خدمة {kw} متكاملة: معاينة وتغليف وفك وتحميل ونقل وتركيب، مع ونش رفع العفش للأدوار العالية. فريقنا قريب منك في {a}.",
      about_t=f"{kw} بخبرة في طبيعة المنطقة",
      about=[L["local"], f"سواء بتنقل جوه {a} أو منها لأي منطقة تانية في القاهرة والجيزة، بنديك سعر واضح قبل التحميل وميعاد مضبوط، وبنسلمك العفش متركب في مكانه."])

ALL = GENERIC + LOCATIONS

HOME = dict(slug="index", kw="نقل عفش", hero="winch-lift-villa", about_img="loading-wrapped-furniture",
  title="نقل عفش بالقاهرة والجيزة | ونش رفع العفش وتغليف | 01042723928",
  desc="شركة نقل عفش بالقاهرة والجيزة: تغليف كامل، فك وتركيب، ونش رفع العفش للأدوار العالية وعربيات مغلقة. مدينة نصر، التجمع، مدينتي، المعادي، أكتوبر، زايد، المقطم. اتصل 01042723928.",
  h1="<em>نقل عفش</em> بالقاهرة والجيزة مع ونش رفع وتغليف كامل",
  lead="فك وتغليف وتحميل ونقل وتركيب بفريق مدرب وعربيات مغلقة وونش رفع العفش للأدوار العالية. خدمة باب لباب في مدينة نصر والتجمع ومدينتي والمعادي وأكتوبر والشيخ زايد والمقطم.",
  about_t="شركة نقل عفش بتشيل عنك الهم كله",
  about=["من أول مكالمة بنحدد معاك حجم العفش والمكان والدور ونقولك لو محتاج ونش رفع العفش. وبنديك سعر واضح قبل التحميل من غير مفاجآت.","يوم النقل فريقنا بيفك الأثاث ويغلفه بالفوم والاستريتش والكرتون، ويرصه في عربية مغلقة، وفي المكان الجديد بنركب كل حاجة في مكانها."])

def services(p):
    a = p.get("area")
    sfx = f" في {a}" if a else ""
    S = [
     ("trucks-residential", "نقل عفش المنازل والشقق", "نقل كامل للشقق والفيلات والاستوديوهات بعربيات مغلقة بمقاسات مختلفة."),
     ("winch-lift-villa", "ونش رفع العفش", "ونش هيدروليك لرفع وتنزيل الأثاث للأدوار العالية والسلالم الضيقة."),
     ("wrapped-furniture-room", "تغليف الأثاث باحتراف", "تغليف بالفوم والاستريتش والكرتون والبطانيات لحماية كل قطعة."),
     ("packing-team-living-room", "فك وتركيب الأثاث", "نجارين لفك وتركيب غرف النوم والدواليب والمطابخ والستائر."),
     ("truck-loaded-inside", "نقل الأجهزة الكهربائية", "تغليف ونقل الثلاجات والغسالات والشاشات والتكييفات بأمان."),
     ("truck-fleet-row", "نقل المكاتب والشركات", "نقل المكاتب والملفات والأجهزة في أقل وقت لعدم تعطيل الشغل."),
    ]
    if p["slug"] == "winch-rafa-al-afsh":
        S.insert(0, S.pop(1))
    cards = "\n".join(f'''      <article class="card">{img(i, t + sfx, w=800, h=600)}
        <div class="card-body"><h3>{t}{sfx}</h3><p>{d}</p></div></article>''' for i, t, d in S)
    return cards

def gallery(p):
    order = [p["hero"]] + [n for n, _ in PHOTOS if n != p["hero"]]
    out = []
    for k, n in enumerate(order):
        cap = PH[n]
        cls = ' class="wide"' if k == 0 else ""
        out.append(f'      <figure{cls}>{img(n, cap + " - " + p["kw"], w=600, h=600)}<figcaption>{cap}</figcaption></figure>')
    return "\n".join(out)

def faqs(p):
    kw = p["kw"]; a = p.get("area")
    F = [
     (f"بكام سعر {kw}؟", "السعر بيتحدد على حسب كمية العفش والدور والمسافة ومحتاج ونش رفع ولا لأ. اتصل على " + PHONE + " وهتاخد سعر واضح قبل التحميل."),
     ("هل التغليف والفك والتركيب ضمن الخدمة؟", "أيوه، الخدمة الكاملة بتشمل الفك والتغليف والتحميل والنقل والتنزيل والتركيب. وممكن تختار جزء منها بس لو حابب."),
     ("إمتى أحتاج ونش رفع العفش؟", "لو الدور عالي أو السلم والأسانسير ضيقين أو عندك قطع كبيرة زي الكنب والدواليب، الونش بيوفر وقت كبير وبيحمي الأثاث والحيطان."),
     ("أحجز قبل الميعاد بقد إيه؟", "يفضل تحجز قبلها بيوم أو اتنين، وفي حالات كتير بنقدر ننقل في نفس اليوم حسب المواعيد المتاحة."),
    ]
    if p.get("faq"):
        F.insert(1, p["faq"])
    return "\n".join(f'      <details><summary>{q}</summary><p>{ans}</p></details>' for q, ans in F), F

def area_links(cur):
    return "\n".join(
      '      <li><a href="%s.html"%s>%sنقل عفش %s</a></li>' % (L["slug"], ' aria-current="page"' if L["slug"] == cur else "", I["pin"], L["area"])
      for L in LOCATIONS)

def page(p):
    kw = p["kw"]; a = p.get("area"); slug = p["slug"]
    faq_html, F = faqs(p)
    local_block = ""
    if a:
        pts = "\n".join(f'        <li>{I["pin"]}{x}</li>' for x in p["points"])
        local_block = f'''
  <section class="section" id="area">
    <div class="wrap">
      <div class="sec-head"><span class="tag">مناطق الخدمة</span>
        <h2>{kw} لكل أحياء {a}</h2>
        <p>فريقنا بيغطي كل مناطق {a} وبيوصلك بسرعة. من ضمن الأماكن اللي بنخدمها:</p></div>
      <ul class="local-points">
{pts}
      </ul>
      <p style="text-align:center;margin-top:10px"><a class="btn btn-amber" href="tel:{PHONE_INTL}">{I["phone"]}اطلب {kw} الآن</a></p>
    </div>
  </section>'''
    ld = {
      "@context": "https://schema.org",
      "@graph": [
        {"@type": "MovingCompany", "name": BRAND, "telephone": PHONE_INTL,
         "image": IMG + p["hero"] + ".jpg", "description": p["desc"],
         "areaServed": [a] if a else ["القاهرة", "الجيزة"] + [L["area"] for L in LOCATIONS],
         "address": {"@type": "PostalAddress", "addressLocality": a or "القاهرة", "addressCountry": "EG"},
         "openingHours": "Mo-Su 08:00-22:00"},
        {"@type": "FAQPage", "mainEntity": [
          {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in F]}
      ]}
    wa_text = f"مرحباً، محتاج {kw}"
    why_items = [
      "سعر واضح ومتفق عليه قبل التحميل",
      "عمالة مدربة على الفك والتغليف والتركيب",
      "عربيات مغلقة نضيفة بمقاسات مختلفة",
      "ونش رفع العفش للأدوار العالية",
      "التزام بالمواعيد وسرعة في التنفيذ",
    ]
    why = "\n".join(f'          <li>{I["check"]}<span>{x}</span></li>' for x in why_items)
    about_ps = "\n".join(f"        <p>{x}</p>" for x in p["about"])
    nav_home = "index.html"
    cands = [n for n, _ in PHOTOS if n not in (p["hero"], p["about_img"], "moving-work-collage")]
    side_img = cands[sum(map(ord, slug)) % len(cands)]
    foot_areas = "\n".join('          <li><a href="%s.html">نقل عفش %s</a></li>' % (L["slug"], L["area"]) for L in LOCATIONS)
    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p["title"]}</title>
<meta name="description" content="{p["desc"]}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:locale" content="ar_EG">
<meta property="og:title" content="{p["title"]}">
<meta property="og:description" content="{p["desc"]}">
<meta property="og:image" content="{IMG}{p["hero"]}.jpg">
<meta name="theme-color" content="#0e2a3c">
<link rel="icon" type="image/png" sizes="32x32" href="assets/images/favicons/favicon-32x32.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="{IMG}{p["hero"]}.jpg">
<link rel="stylesheet" href="assets/css/moving-rtl.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>

<div class="topbar"><div class="wrap">
  <span>{I["clock"]}{HOURS}</span>
  <span class="hide-sm">{I["pin"]}{("نخدم كل مناطق " + a) if a else "القاهرة والجيزة وكل المدن الجديدة"}</span>
  <span>{I["phone"]}<a href="tel:{PHONE_INTL}" class="ltr">{PHONE}</a></span>
</div></div>

<header class="header"><div class="wrap">
  <a class="brand" href="{nav_home}"><span class="brand-mark">{I["truck"]}</span><span>{BRAND}<small>{BRAND_SUB}</small></span></a>
  <nav class="nav" aria-label="القائمة الرئيسية">
    <a href="#services">الخدمات</a><a href="#about">عن الخدمة</a><a href="#gallery">صور من شغلنا</a><a href="#areas">المناطق</a><a href="#faq">أسئلة شائعة</a>
  </nav>
  <a class="btn btn-amber btn-sm" href="tel:{PHONE_INTL}">{I["phone"]}<span>اتصل الآن</span></a>
</div></header>

<main>
  <section class="hero" style="background-image:url('{IMG}{p["hero"]}.jpg')">
    <div class="wrap">
      <div>
        <span class="eyebrow">{I["truck"]}{kw}</span>
        <h1>{p["h1"]}</h1>
        <p class="lead">{p["lead"]}</p>
        <div class="hero-ctas">
          <a class="btn btn-amber" href="tel:{PHONE_INTL}">{I["phone"]}اتصل الآن <span class="ltr">{PHONE}</span></a>
          <a class="btn btn-green" href="https://wa.me/{WHATSAPP}?text={wa_text.replace(" ", "%20")}" target="_blank" rel="noopener">{I["wa"]}كلمنا واتساب</a>
        </div>
        <ul class="checks">
          <li>{I["check"]}تغليف كامل</li><li>{I["check"]}فك وتركيب</li><li>{I["check"]}ونش رفع</li><li>{I["check"]}عربيات مغلقة</li>
        </ul>
      </div>
      <div class="hero-photo">{img(p["about_img"], kw, lazy=False)}</div>
    </div>
  </section>

  <div class="trust"><div class="wrap">
    <div>{I["box"]}تغليف بالفوم والاستريتش</div>
    <div>{I["crane"]}ونش رفع للأدوار العالية</div>
    <div>{I["users"]}عمالة مدربة</div>
    <div>{I["shield"]}سعر واضح قبل التحميل</div>
  </div></div>

  <section class="section soft" id="services">
    <div class="wrap">
      <div class="sec-head"><span class="tag">خدماتنا</span>
        <h2>خدمات {kw} كاملة في مكان واحد</h2>
        <p>كل اللي تحتاجه عشان تنقل بيتك أو مكتبك من غير تعب: من التغليف لحد التركيب.</p></div>
      <div class="grid-3">
{services(p)}
      </div>
    </div>
  </section>

  <section class="section" id="about">
    <div class="wrap split">
      <div class="split-img">{img(side_img, p["about_t"])}<div class="badge">{I["phone"]} <span class="ltr">{PHONE}</span><br>اتصل واعرف السعر</div></div>
      <div>
        <span class="eyebrow" style="background:#fff3dd;color:#b36f00">{kw}</span>
        <h2>{p["about_t"]}</h2>
{about_ps}
        <ul class="list">
{why}
        </ul>
        <a class="btn btn-amber" href="tel:{PHONE_INTL}">{I["phone"]}احجز {kw} الآن</a>
      </div>
    </div>
  </section>
{local_block}
  <section class="section soft" id="steps">
    <div class="wrap">
      <div class="sec-head"><span class="tag">خطوات بسيطة</span><h2>إزاي بنتمم {kw}؟</h2></div>
      <div class="steps">
        <div class="step"><h3>اتصل بينا</h3><p>كلمنا على <span class="ltr">{PHONE}</span> وقولنا المكان والدور وحجم العفش.</p></div>
        <div class="step"><h3>عرض سعر</h3><p>نحدد معاك الاحتياجات ولو محتاج ونش، ونديك سعر واضح وميعاد.</p></div>
        <div class="step"><h3>فك وتغليف وتحميل</h3><p>الفريق يفك الأثاث ويغلفه ويرصه في عربية مغلقة.</p></div>
        <div class="step"><h3>نقل وتركيب</h3><p>ننزل العفش في مكانه الجديد ونركبه ونتأكد إن كل حاجة سليمة.</p></div>
      </div>
    </div>
  </section>

  <section class="section" id="gallery">
    <div class="wrap">
      <div class="sec-head"><span class="tag">صور حقيقية</span><h2>صور من شغلنا في {kw}</h2>
        <p>عربيات مغلقة، ونش رفع العفش، وتغليف كل قطعة قبل التحميل.</p></div>
      <div class="gallery">
{gallery(p)}
      </div>
    </div>
  </section>

  <section class="section soft" id="areas">
    <div class="wrap">
      <div class="sec-head"><span class="tag">بنوصلك فين؟</span><h2>مناطق نقل العفش</h2>
        <p>بنقدم خدمة نقل عفش وونش رفع العفش في القاهرة والجيزة، ومن أهم المناطق:</p></div>
      <ul class="areas">
{area_links(slug)}
      </ul>
    </div>
  </section>

  <section class="section" id="faq">
    <div class="wrap">
      <div class="sec-head"><span class="tag">أسئلة شائعة</span><h2>أسئلة عن {kw}</h2></div>
      <div class="faq">
{faq_html}
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0">
    <div class="wrap">
      <div class="cta">
        <div><h2>جاهز لـ{kw}؟</h2><p>اتصل دلوقتي واحجز ميعادك، وفريقنا يوصلك في الوقت اللي يناسبك.</p></div>
        <a class="btn btn-amber" href="tel:{PHONE_INTL}">{I["phone"]}<span class="big-phone ltr" style="color:inherit;font-size:inherit">{PHONE}</span></a>
      </div>
    </div>
  </section>
</main>

<footer class="footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <h3>{BRAND}</h3>
        <p>نقل عفش وونش رفع وتغليف وفك وتركيب في القاهرة والجيزة. خدمة باب لباب بعمالة مدربة وعربيات مغلقة.</p>
        <p>{I["phone"]} <a href="tel:{PHONE_INTL}" class="ltr">{PHONE}</a></p>
      </div>
      <div>
        <h3>خدماتنا</h3>
        <ul>
          <li><a href="naql-afsh.html">نقل عفش</a></li>
          <li><a href="naql-al-afsh.html">نقل العفش</a></li>
          <li><a href="winch-rafa-al-afsh.html">ونش رفع العفش</a></li>
          <li><a href="sharikat-naql-afsh.html">شركة نقل عفش</a></li>
          <li><a href="sharika-li-naql-al-afsh.html">شركة لنقل العفش</a></li>
        </ul>
      </div>
      <div>
        <h3>المناطق</h3>
        <ul>
{foot_areas}
        </ul>
      </div>
    </div>
    <div class="copy">© {BRAND} - <a href="index.html">الرئيسية</a></div>
  </div>
</footer>

<a class="float-call" href="tel:{PHONE_INTL}" aria-label="اتصل الآن على {PHONE}">
  <span class="ring">{I["phone"]}</span>
  <span><small>اتصل الآن - رد فوري</small><strong class="ltr">{PHONE}</strong></span>
</a>

</body>
</html>
'''

if __name__ == "__main__":
    for p in [HOME] + ALL:
        path = os.path.join(ROOT, p["slug"] + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(page(p))
        print("written", p["slug"] + ".html")
