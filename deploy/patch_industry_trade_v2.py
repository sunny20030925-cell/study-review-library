#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from pathlib import Path

BOOK='industry-trade'
OLD_VERSION='2026.07.29-1'
VERSION='2026.07.30-1'
UPDATED_AT='2026-07-30'

HTML_REPLACEMENTS=json.loads(r"""{"chapters/ch01.html": [["<dt>需求彈性（demand elasticity）</dt><dd>價格變動 1% 時需求量變動的百分比。</dd>", "<dt>需求彈性（demand elasticity）</dt><dd>需求量變動百分比相對於價格變動百分比的比率；自有價格彈性通常為負，本書在 Lerner 公式中使用其絕對值。</dd>"]], "chapters/ch03.html": [["消費者重視品種時，市場變大可以讓更多品種分攤固定成本；同時競爭加劇可能壓低加成。這種「更多品種＋更大生產規模」是新貿易理論的重要直覺。", "消費者重視品種時，市場整合可讓存活品種以更大銷量分攤各自固定成本，並讓每個市場的消費者接觸更多品種。至於加成是否下降，要看需求彈性與競爭模型；在固定彈性的 CES 基準裡，加成率本身是固定的。"], ["CES 對稱壟斷性競爭常見加成式，要求需求彈性 ε&gt;1 且模型條件成立。", "CES 對稱壟斷性競爭常見加成式，要求需求彈性 ε&gt;1。若 ε 固定，這個基準模型的加成率不會只因市場整合而改變；要得到貿易壓低加成，需再加入有效彈性改變、可變加成或不同競爭機制。"], ["若需求彈性 ε=5、邊際成本 MC=NT$80，簡化 CES 加成下 P=(5/4)×80=NT$100。若貿易開放提高替代性，使有效彈性上升，其他條件不變時加成會下降。", "若需求彈性 ε=5、邊際成本 MC=NT$80，簡化 CES 加成下 P=(5/4)×80=NT$100。若貿易前後 ε 都維持 5，純 CES 基準的加成率仍相同；只有當貿易使有效彈性上升，或模型採可變加成等機制時，加成才會進一步下降。"]], "chapters/ch07.html": [["若補貼支出 S 由本國負擔，必須從國內福利中扣除；不能只看本國廠商利潤 πH。", "若 πH 表示「已包含補貼收入」的本國廠商利潤，而補貼支出 S 由本國政府負擔，國內福利需再扣除 S；若使用的是不含補貼的營業利潤，就不能把同一筆補貼重複扣兩次。"], ["某出口補貼使本國廠商利潤增加 NT$25，但政府補貼支出增加 NT$18；若本國消費者不受影響且暫不計其他效果，簡化國內福利淨變化為 +NT$7。若外國報復造成額外損失，結果還要再扣除。", "某出口補貼使本國廠商「含補貼收入的利潤」增加 NT$25，政府補貼支出增加 NT$18；若本國消費者不受影響且暫不計其他效果，簡化國內福利淨變化為 +NT$7。這個算法的關鍵是利潤口徑已含補貼；若改用不含補貼的營業利潤，福利帳必須改寫，避免重複計帳。若外國報復造成額外損失，結果還要再扣除。"]], "chapters/ch10.html": [["出口固定成本較低，但每單位要承擔運輸與關稅；FDI 固定成本高，卻能避開部分跨境變動成本。市場越大、單位貿易成本越高，直接投資越有吸引力。", "在標準「接近市場—集中生產」基準裡，出口通常需要較低的市場設置固定成本，但每單位要承擔運輸、關稅等貿易成本；FDI 往往需要較高的設廠固定成本，卻能避開部分跨境變動成本。市場越大、可節省的單位貿易成本越高，直接投資通常越有吸引力。"], ["企業取得並控制國外生產或營運資產的投資。", "投資者對國外企業建立持久利益，並具有顯著管理影響力或控制的跨境投資；國際統計常以至少 10% 投票權作為直接投資關係的基準，並不要求 100% 控制。"], ["\\[q^*=F_{FDI}/t\\]</p><p>若 FDI 相對出口多一筆固定成本 FFDI，但每單位節省貿易成本 t，簡化臨界銷量為 FFDI/t。", "\\[q^*=\\Delta F/\\Delta t\\]</p><p>令 ΔF 表示 FDI 相對出口多出的固定成本，Δt 表示 FDI 相對出口每單位可節省的淨變動成本；在兩者皆為常數的簡化比較下，臨界銷量為 ΔF/Δt。"]], "chapters/ch15.html": [["上游與下游各只有一個主要交易對手的情況。", "交易的一側只有一個賣方、另一側只有一個買方，價格與剩餘通常透過議價而非單邊市場定價決定。"], ["\\[S=V-C\\]</p><p>合作可創造的總剩餘可寫成價值 V 減替代成本 C。", "\\[G=S-d_A-d_B\\]</p><p>令 S 表示合作時可分配的總報酬，dA、dB 為雙方談判破裂時的 disagreement payoffs，則可供議價分配的合作增益為 G=S-dA-dB。"], ["\\[Share_A=\\beta S\\]</p><p>最簡 Nash 議價中，若威脅點為零，A 取得權重 β 的合作剩餘。", "\\[u_A=d_A+\\beta G,\\quad u_B=d_B+(1-\\beta)G\\]</p><p>在可轉移剩餘的簡化 Nash 議價中，A、B 先保留各自 disagreement payoff，再按議價權重 β 與 1-β 分配合作增益 G；只有 dA=dB=0 時，才化成 A 取得 βS。"]], "chapters/ch19.html": [["成員間取消多數關稅，但各自保留對外關稅。", "成員間對原產於成員的實質上全部貿易取消關稅與主要限制，但各自保留對非成員的對外關稅。"], ["成員間自由貿易並採共同對外關稅。", "成員間對實質上全部內部貿易取消關稅與主要限制，並對非成員採實質上相同的對外關稅與貿易規則。"], ["\\[True\\ resource\\ cost\\]</p><p>判斷貿易創造／轉向時要看生產的真實資源成本，而非只看含關稅價格。", "\\[\\Delta RC=c_{partner}-c_{nonmember}\\]</p><p>對「原本已從非成員進口、之後轉向夥伴國」的既有進口單位，若夥伴國真實成本較高，ΔRC&gt;0 表示每單位多耗用的真實資源；它與關稅收入變化、消費者剩餘變化是同一福利變化的不同帳面表示，做完整福利帳時不可重複扣除。"], ["本國成本 NT$120；第三國生產成本 NT$70、對外關稅 NT$20，所以整合前進口到岸價格 NT$90。夥伴國成本 NT$80，FTA 後免稅，進口轉向夥伴國。消費價格由 90 降到 80，但真實資源成本由 70 升到 80，每單位有 NT$10 的貿易轉向成本，同時政府也失去原本關稅收入。", "本國成本 NT$120；第三國生產成本 NT$70、對外關稅 NT$20，所以整合前消費者支付 NT$90。夥伴國成本 NT$80，FTA 後免稅，進口轉向夥伴國。若先固定原本的一單位進口量來看：消費者少付 NT$10，但政府少收 NT$20，國內福利淨減 NT$10；這正好等於真實資源成本由 70 升到 80 的 NT$10，而不是再把「關稅收入損失 NT$20」與「資源成本 NT$10」重複相加。若價格下降又新增消費量，還要另外計入新增消費的福利效果。"]], "chapters/appendix-a.html": [["CES 對稱壟斷性競爭常見加成式，要求需求彈性 ε&gt;1 且模型條件成立。", "CES 對稱壟斷性競爭常見加成式，要求 ε&gt;1；若 ε 固定，純 CES 基準的加成率不會只因市場整合而改變。"], ["\\(q^*=F_{FDI}/t\\)</span> — 若 FDI 相對出口多一筆固定成本 FFDI，但每單位節省貿易成本 t，簡化臨界銷量為 FFDI/t。", "\\(q^*=\\Delta F/\\Delta t\\)</span> — ΔF 是 FDI 相對出口增加的固定成本，Δt 是每單位可節省的淨變動成本；簡化臨界銷量為 ΔF/Δt。"], ["\\(S=V-C\\)</span> — 合作可創造的總剩餘可寫成價值 V 減替代成本 C。；<span class=\"math\">\\(Share_A=\\beta S\\)</span> — 最簡 Nash 議價中，若威脅點為零，A 取得權重 β 的合作剩餘。", "\\(G=S-d_A-d_B\\)</span> — S 是合作時可分配的總報酬，dA、dB 是 disagreement payoffs；可供議價分配的合作增益為 G=S-dA-dB。；<span class=\"math\">\\(u_A=d_A+\\beta G,\\quad u_B=d_B+(1-\\beta)G\\)</span> — 可轉移剩餘的簡化 Nash 議價：雙方先保留 disagreement payoff，再按 β 與 1-β 分配合作增益；威脅點皆為 0 時才化為 A 取得 βS。"], ["\\(True\\ resource\\ cost\\)</span> — 判斷貿易創造／轉向時要看生產的真實資源成本，而非只看含關稅價格。", "\\(\\Delta RC=c_{partner}-c_{nonmember}\\)</span> — 對既有進口的貿易轉向，ΔRC&gt;0 表示轉向後每單位真實資源成本增加；與 CS、政府關稅收入變化做福利帳時不可重複計算。"]], "chapters/appendix-c.html": [["<tr><td>外國直接投資（FDI）</td><td>企業取得並控制國外生產或營運資產的投資。</td></tr>", "<tr><td>外國直接投資（FDI）</td><td>投資者對國外企業建立持久利益，並具有顯著管理影響力或控制的跨境投資；國際統計常以至少 10% 投票權作直接投資關係基準。</td></tr>"], ["<tr><td>自由貿易區</td><td>成員間取消多數關稅，但各自保留對外關稅。</td></tr>", "<tr><td>自由貿易區</td><td>成員間對原產於成員的實質上全部貿易取消關稅與主要限制，但各自保留對非成員的對外關稅。</td></tr>"], ["<tr><td>關稅同盟</td><td>成員間自由貿易並採共同對外關稅。</td></tr>", "<tr><td>關稅同盟</td><td>成員間對實質上全部內部貿易取消關稅與主要限制，並對非成員採實質上相同的對外關稅與貿易規則。</td></tr>"], ["<tr><td>需求彈性（demand elasticity）</td><td>價格變動 1% 時需求量變動的百分比。</td></tr>", "<tr><td>需求彈性（demand elasticity）</td><td>需求量變動百分比相對於價格變動百分比的比率；自有價格彈性通常為負，Lerner 反彈性關係使用其絕對值。</td></tr>"], ["<tr><td>雙邊壟斷</td><td>上游與下游各只有一個主要交易對手的情況。</td></tr>", "<tr><td>雙邊壟斷</td><td>交易的一側只有一個賣方、另一側只有一個買方，價格與剩餘通常透過議價而非單邊市場定價決定。</td></tr>"]]}""")
QUESTION_UPDATES=json.loads(r"""{"ch00-q04": {"answer": "不能把出口或產量當成福利本身；應另外列出消費者剩餘、廠商利潤、政府收支與外部效果，再判斷淨福利。", "explanation": "出口額或產量只是市場結果。修正方式是做完整福利帳，並確認是否只是本國與外國、消費者與廠商之間的移轉，而不是新增效率。"}, "ch01-q01": {"answer": "需求量變動百分比相對於價格變動百分比的比率；自有價格彈性通常為負。", "explanation": "需求的自有價格彈性可寫成「需求量變動百分比／價格變動百分比」，通常為負；Lerner 反彈性關係使用其絕對值。"}, "ch01-q04": {"answer": "Lerner 指標要代入邊際成本 MC，不是平均成本 AC；固定成本與 AC 可影響利潤，但不能取代 MC。", "explanation": "L=(P−MC)/P 衡量價格相對邊際成本的加成。把 AC 代入會把固定成本分攤混進邊際定價條件。"}, "ch02-q04": {"answer": "先辨認策略變數與時序：Cournot 選產量、Bertrand 選價格、Stackelberg 有先後移動，再依該模型推最佳反應。", "explanation": "三種模型的策略變數與時序不同，因此反應函數與政策效果不能直接互換。"}, "ch03-q04": {"answer": "產業內貿易可由產品差異化與規模經濟產生，並不否定比較利益或貿易利得；應分別檢查品種、規模與競爭效果。", "explanation": "同一產業同時進出口只是貿易型態。其福利可來自品種增加、固定成本分攤與競爭等來源，不能據此宣稱沒有比較利益或利得。"}, "ch04-q04": {"answer": "規模經濟是相關產量範圍內平均成本隨產量增加而下降；邊際成本不一定下降。", "explanation": "例如 AC=F/q+c 時，產量增加會分攤固定成本使 AC 下降，但 MC 仍可維持常數 c。"}, "ch05-q04": {"answer": "要區分「高生產力廠商較容易自我選擇成為出口者」與「出口後學習使生產力提高」兩種因果方向。", "explanation": "觀察到出口廠商生產力較高，可能早在出口前就存在。若要主張 learning-by-exporting，還需額外的因果證據。"}, "ch06-q04": {"answer": "配額租歸誰取決於配額權如何分配：拍賣可成為政府收入，免費執照可能由國內進口商取得，某些安排下外國出口商也可能取得。", "explanation": "配額造成的國內外價差只是租的來源；租的最終歸屬要看拍賣、執照與交易制度，不能固定算成政府收入。"}, "ch07-q02": {"explanation": "若題目中的「廠商利潤增加 NT$25」已包含補貼收入，則國內福利變化為 25−18=NT$7；若利潤口徑不含補貼，就不能再用同一算法重複扣除補貼。"}, "ch07-q04": {"answer": "應比較完整國內淨福利，而不是只看本國企業利潤；至少扣除政府補貼成本並納入外國反應、報復與政府失靈。", "explanation": "策略性補貼可能提高企業利潤，但納稅人支出、對手反應與報復都可能抵銷利潤移轉，因此企業「贏」不等於國家福利提高。"}, "ch08-q04": {"answer": "垂直整合要同時檢查效率與排除效果：它可能消除雙重加價，也可能造成投入封鎖或提高競爭者成本。", "explanation": "整合的淨福利方向取決於兩類效果的相對大小，不能預設一定反競爭或一定有效率。"}, "ch09-q04": {"answer": "外包描述「企業內部或外部」的組織邊界；離岸描述「國內或國外」的地理位置，兩者可交叉形成四種安排。", "explanation": "企業可以國內外包、海外外包，也可以在國內自製或透過海外子公司離岸自製，因此 outsourcing 與 offshoring 不是同義詞。"}, "ch10-q01": {"answer": "對國外企業建立持久利益，並具有顯著管理影響力或控制的跨境投資。", "explanation": "FDI 的核心是 lasting interest 與 significant influence/control，不等同所有跨境金融投資；國際統計常以至少 10% 投票權作直接投資關係基準，並不要求 100% 控制。"}, "ch10-q02": {"explanation": "令 ΔF=NT$6,000、Δt=NT$8／單位，q*=ΔF/Δt=750。這裡 ΔF 是 FDI 相對出口多出的固定成本，Δt 是每單位可節省的淨變動成本。"}, "ch10-q04": {"answer": "FDI 是對國外企業建立持久利益並具有顯著影響力或控制的直接投資；一般未取得這種影響力的跨境證券投資屬投資組合投資。", "explanation": "修正關鍵是區分 direct investment 與 portfolio investment；FDI 不要求 100% 控制，國際統計常以至少 10% 投票權作直接投資關係基準。"}, "ch11-q04": {"answer": "要把授權收入與產品市場效果一起算；固定費主要移轉剩餘，按量權利金則會改變被授權者的邊際誘因與銷量。", "explanation": "只比較授權金收入會漏掉價格、產量與競爭反應。尤其按量權利金可能提高有效邊際成本，使授權收入與產品市場利潤同時改變。"}, "ch12-q04": {"answer": "先用可比的正常價值與出口價格判斷是否存在傾銷；是否能採反傾銷措施還要另外判斷重大損害與因果關係。", "explanation": "「出口價低於本國價」不一定等於適當的 normal value 比較；而 dumping determination 與能否採取反傾銷措施也是兩個不同步驟。"}, "ch13-q04": {"answer": "先確認商品、交易層級、稅負、保固與服務是否可比，再把所有運輸與交易成本扣除，剩下的才是可套利價差。", "explanation": "觀察到的跨國價差可能反映產品版本、稅費或服務差異；未先做可比性調整，不能直接當成套利利潤。"}, "ch14-q04": {"answer": "範疇經濟比較「多種產品共同生產」與「分開生產」的成本；規模經濟則看同一產品產量增加時平均成本如何變化。", "explanation": "兩者都可能涉及固定成本，但比較維度不同：scope 是產品組合，scale 是單一活動的產量規模。"}, "ch15-q02": {"explanation": "威脅點皆為 0 時，可分配合作增益就是 NT$100；品牌商取得 0.6×100=60，供應商取得 0.4×100=40。若 disagreement payoff 不為 0，應先保留各自威脅點，再分配剩餘增益。"}, "ch15-q04": {"answer": "議價價格要由合作剩餘、雙方 disagreement payoffs／outside options 與議價權重共同決定，不能只從生產成本單邊推出。", "explanation": "更好的外部選項會提高談判破裂時可得收益，因而改變 Nash 議價分配；成本只是合作剩餘的一部分。"}, "ch16-q04": {"answer": "要把總體平均效果與分配效果分開，至少按技能、產業、地區與調整成本判斷哪些勞工可能受益或受損。", "explanation": "全國平均實質工資可以上升，同時特定進口競爭產業或地方勞動市場受損；兩者並不矛盾。"}, "ch17-q04": {"answer": "研發補貼只有在知識外溢等市場失靈下才有矯正理由，並要扣除財政成本、重複補助與可能的市場勢力效果。", "explanation": "企業研發支出不是自動等於社會外部利益；補貼應針對企業無法內部化的部分，而不是把全部研發成本社會化。"}, "ch18-q04": {"answer": "若核心失靈是排放外部性，先用排放稅、總量管制等直接環境工具對準污染；只有另有跨境洩漏等問題時才再評估貿易工具。", "explanation": "一般關稅通常沒有直接對準每單位排放的邊際外部損害，因此不是處理污染的第一最佳工具。"}, "ch19-q01": {"answer": "成員間對原產於成員的實質上全部貿易取消關稅與主要限制，但各自保留對非成員的對外關稅。", "explanation": "自由貿易區的核心是成員內部對原產貨品的實質上全部貿易取消關稅與主要限制，而各成員仍可保留自己的對外關稅；這與關稅同盟的共同／實質相同對外關稅不同。"}, "ch19-q02": {"explanation": "80−70=NT$10，表示既有進口轉向後每單位真實資源成本增加 NT$10。若同時用 CS 與關稅收入做完整福利帳，這 NT$10 是同一福利損失的資源成本表示，不能再重複加扣。"}, "ch19-q04": {"answer": "要同時比較真實資源成本與完整福利帳；消費價格下降可能伴隨貿易轉向與關稅收入損失，且同一損失不能重複計算。", "explanation": "FTA 後低價不保證福利上升。若進口從真實成本較低的非成員轉向成本較高的夥伴國，可能出現貿易轉向；用 CS、PS、G 計帳時要避免再把同一資源成本重複扣除。"}}""")
_SEARCH_RAW=json.loads(r"""{"ch01␟正式定義": "需求彈性（demand elasticity）：需求量變動百分比相對於價格變動百分比的比率；自有價格彈性通常為負，本書在 Lerner 公式中使用其絕對值。 邊際成本（marginal cost, MC）：多生產一單位產品所增加的成本。 加成率（markup）：價格相對邊際成本的差額或比例。 Lerner 指標（Lerner index）：以 (P-MC)/P 衡量價格高於邊際成本的程度。 消費者剩餘（consumer surplus）：消費者願付價格與實際支付價格之間的差額。", "ch03␟白話直覺": "消費者重視品種時，市場整合可讓存活品種以更大銷量分攤各自固定成本，並讓每個市場的消費者接觸更多品種。至於加成是否下降，要看需求彈性與競爭模型；在固定彈性的 CES 基準裡，加成率本身是固定的。 壟斷性競爭不等於單一獨占。每家廠商對自己的品牌有一些定價能力，但仍受到其他差異化產品與進入退出的限制。", "ch03␟核心公式": "P=\\frac{\\varepsilon}{\\varepsilon-1}MC；CES 對稱壟斷性競爭常見加成式，要求需求彈性 ε>1。若 ε 固定，這個基準模型的加成率不會只因市場整合而改變；要得到貿易壓低加成，需再加入有效彈性改變、可變加成或不同競爭機制。 AC=F/q+c；固定成本 F、常數邊際成本 c 時的平均成本。", "ch03␟標準例題": "若需求彈性 ε=5、邊際成本 MC=NT$80，簡化 CES 加成下 P=(5/4)×80=NT$100。若貿易前後 ε 都維持 5，純 CES 基準的加成率仍相同；只有當貿易使有效彈性上升，或模型採可變加成等機制時，加成才會進一步下降。", "ch07␟核心公式": "W=\\pi_H-S+CS_H+其他效果；若 πH 表示「已包含補貼收入」的本國廠商利潤，而補貼支出 S 由本國政府負擔，國內福利需再扣除 S；若使用的是不含補貼的營業利潤，就不能把同一筆補貼重複扣兩次。 \\Delta W=\\Delta\\pi_H-\\Delta S+\\Delta CS_H+...；政策比較看的是淨變化，不是單一項目。", "ch07␟標準例題": "某出口補貼使本國廠商「含補貼收入的利潤」增加 NT$25，政府補貼支出增加 NT$18；若本國消費者不受影響且暫不計其他效果，簡化國內福利淨變化為 +NT$7。這個算法的關鍵是利潤口徑已含補貼；若改用不含補貼的營業利潤，福利帳必須改寫，避免重複計帳。若外國報復造成額外損失，結果還要再扣除。", "ch10␟白話直覺": "在標準「接近市場—集中生產」基準裡，出口通常需要較低的市場設置固定成本，但每單位要承擔運輸、關稅等貿易成本；FDI 往往需要較高的設廠固定成本，卻能避開部分跨境變動成本。市場越大、可節省的單位貿易成本越高，直接投資通常越有吸引力。 授權可降低資本投入，但會把部分控制權交給當地企業，並可能產生品質、技術外洩或未來競爭問題。", "ch10␟正式定義": "外國直接投資（FDI）：投資者對國外企業建立持久利益，並具有顯著管理影響力或控制的跨境投資；國際統計常以至少 10% 投票權作為直接投資關係的基準，並不要求 100% 控制。 水平 FDI：在不同國家複製相似活動以接近市場。 垂直 FDI：依成本或要素優勢把不同生產階段跨國配置。 接近市場—集中生產取捨：FDI 節省貿易成本，但犧牲集中生產的規模經濟。 授權（licensing）：允許另一企業使用技術、專利、商標或其他權利並取得報酬。", "ch10␟核心公式": "q^*=\\Delta F/\\Delta t；令 ΔF 表示 FDI 相對出口多出的固定成本，Δt 表示 FDI 相對出口每單位可節省的淨變動成本；在兩者皆為常數的簡化比較下，臨界銷量為 ΔF/Δt。 C_X=cq+tq+F_X；出口成本含生產、單位貿易成本與出口固定成本。", "ch15␟正式定義": "議價力（bargaining power）：一方在談判中取得較大剩餘份額的能力。 外部選項（outside option）：談判破裂後可取得的替代收益。 Nash 議價：以雙方議價權重與威脅點分配合作剩餘的基準模型。 移轉價格（transfer price）：同一企業集團不同單位之間交易的內部價格。 雙邊壟斷：交易的一側只有一個賣方、另一側只有一個買方，價格與剩餘通常透過議價而非單邊市場定價決定。", "ch15␟核心公式": "G=S-d_A-d_B；令 S 表示合作時可分配的總報酬，dA、dB 為雙方談判破裂時的 disagreement payoffs，則可供議價分配的合作增益為 G=S-dA-dB。 u_A=d_A+\\beta G,\\quad u_B=d_B+(1-\\beta)G；在可轉移剩餘的簡化 Nash 議價中，A、B 先保留各自 disagreement payoff，再按議價權重 β 與 1-β 分配合作增益 G；只有 dA=dB=0 時，才化成 A 取得 βS。", "ch19␟正式定義": "自由貿易區：成員間對原產於成員的實質上全部貿易取消關稅與主要限制，但各自保留對非成員的對外關稅。 關稅同盟：成員間對實質上全部內部貿易取消關稅與主要限制，並對非成員採實質上相同的對外關稅與貿易規則。 貿易創造：區域整合使高成本國內生產被較低成本成員進口取代。 貿易轉向：優惠待遇使進口由更低成本非成員轉向較高成本成員。 競爭政策：維持市場競爭、處理卡特爾、濫用與合併等市場勢力問題的政策。", "ch19␟核心公式": "\\Delta RC=c_{partner}-c_{nonmember}；對「原本已從非成員進口、之後轉向夥伴國」的既有進口單位，若夥伴國真實成本較高，ΔRC>0 表示每單位多耗用的真實資源；它與關稅收入變化、消費者剩餘變化是同一福利變化的不同帳面表示，做完整福利帳時不可重複扣除。 W=CS+PS+G+E；區域整合與競爭政策最終仍回到完整福利帳。", "ch19␟標準例題": "本國成本 NT$120；第三國生產成本 NT$70、對外關稅 NT$20，所以整合前消費者支付 NT$90。夥伴國成本 NT$80，FTA 後免稅，進口轉向夥伴國。若先固定原本的一單位進口量來看：消費者少付 NT$10，但政府少收 NT$20，國內福利淨減 NT$10；這正好等於真實資源成本由 70 升到 80 的 NT$10，而不是再把「關稅收入損失 NT$20」與「資源成本 NT$10」重複相加。若價格下降又新增消費量，還要另外計入新增消費的福利效果。"}""")
SEARCH_UPDATES={tuple(k.split('␟',1)):v for k,v in _SEARCH_RAW.items()}

def jdump(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2) + '\n'

def replace_once(text, old, new, label):
    if new in text:
        return text
    if text.count(old) != 1:
        raise AssertionError(f'{label}: expected one old fragment, got {text.count(old)}')
    return text.replace(old, new, 1)

def next_library_version(current):
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)', current)
    if not m:
        raise AssertionError(f'unexpected library version: {current}')
    date, serial=m.group(1), int(m.group(2))
    if date < UPDATED_AT:
        return f'{UPDATED_AT}-1'
    return f'{date}-{serial+1}'

def main(site_root):
    site=Path(site_root)
    root=site/'books'/BOOK
    lp=site/'data/library.json'; mp=root/'manifest.json'; qp=root/'questions.json'; sp=root/'search.json'
    library=json.loads(lp.read_text(encoding='utf-8'))
    ids=[b['id'] for b in library['books']]
    if ids.count(BOOK)!=1:
        raise AssertionError(f'{BOOK} must exist exactly once')
    manifest=json.loads(mp.read_text(encoding='utf-8'))
    questions=json.loads(qp.read_text(encoding='utf-8'))
    if manifest.get('version')==VERSION and questions.get('version')==VERSION:
        print(library['version'])
        return library['version']
    if manifest.get('version')!=OLD_VERSION or questions.get('version')!=OLD_VERSION:
        raise AssertionError(f'unexpected source version: {manifest.get("version")} / {questions.get("version")}')

    original_chapter_ids=[x['id'] for x in manifest['chapters']]
    original_question_ids=[x['id'] for x in questions['items']]

    for rel, replacements in HTML_REPLACEMENTS.items():
        path=root/rel
        text=path.read_text(encoding='utf-8')
        for i,(old,new) in enumerate(replacements,1):
            text=replace_once(text,old,new,f'{rel} replacement {i}')
        path.write_text(text,encoding='utf-8')

    by_q={q['id']:q for q in questions['items']}
    for qid, updates in QUESTION_UPDATES.items():
        if qid not in by_q:
            raise AssertionError(f'missing question {qid}')
        by_q[qid].update(updates)
    questions['version']=VERSION
    questions['count']=len(questions['items'])
    qp.write_text(jdump(questions),encoding='utf-8')

    search=json.loads(sp.read_text(encoding='utf-8'))
    by_key={(e['chapterId'],e['title']):e for e in search['entries']}
    for key,text in SEARCH_UPDATES.items():
        if key not in by_key:
            raise AssertionError(f'missing search entry {key}')
        by_key[key]['text']=text
    sp.write_text(jdump(search),encoding='utf-8')

    manifest['version']=VERSION
    manifest['updatedAt']=UPDATED_AT
    release={
      'version':VERSION,
      'date':UPDATED_AT,
      'title':'發布後二次內容審計與精確化',
      'changes':[
        '修正需求彈性定義，並補清 Lerner 公式使用自有價格彈性絕對值',
        'CES 固定彈性基準明示固定加成，避免把市場整合自動寫成加成下降',
        '策略性出口補貼明確區分含補貼利潤與營業利潤，避免福利重複計帳',
        'FDI 改為 lasting interest 與 significant influence/control，補 10% 投票權統計基準及相對成本臨界式',
        'Nash 議價加入 disagreement payoffs；雙邊壟斷定義改為單一買方與單一賣方',
        'FTA／關稅同盟定義與貿易轉向福利帳精確化，避免關稅收入與資源成本雙重扣除',
        '全 20 章常見錯誤題答案改為直接糾正原錯誤，移除重複句號生成瑕疵'
      ],
      'progressImpact':'章節 ID、題目 ID、題數與儲存鍵不變，既有閱讀進度與錯題紀錄相容。'
    }
    manifest['releaseNotes']=[release]+[n for n in manifest.get('releaseNotes',[]) if n.get('version')!=VERSION]
    mp.write_text(jdump(manifest),encoding='utf-8')

    manifest2=json.loads(mp.read_text(encoding='utf-8'))
    q2=json.loads(qp.read_text(encoding='utf-8'))
    if [x['id'] for x in manifest2['chapters']] != original_chapter_ids:
        raise AssertionError('chapter IDs changed')
    if [x['id'] for x in q2['items']] != original_question_ids or len(q2['items'])!=100:
        raise AssertionError('question IDs/count changed')

    for b in library['books']:
        if b['id']==BOOK and 'version' in b:
            b['version']=VERSION
    final=next_library_version(library['version'])
    library['version']=final
    lp.write_text(jdump(library),encoding='utf-8')

    swp=site/'sw.js'; sw=swp.read_text(encoding='utf-8')
    sw,n=re.subn(r"const VERSION = 'study-library-[^']+';",f"const VERSION = 'study-library-{final}';",sw,count=1)
    if n!=1:
        raise AssertionError('service worker version marker not found')
    swp.write_text(sw,encoding='utf-8')
    print(final)
    return final

if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('usage: python deploy/patch_industry_trade_v2.py SITE_ROOT')
    main(sys.argv[1])
