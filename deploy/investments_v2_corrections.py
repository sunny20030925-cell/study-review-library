from __future__ import annotations

VERSION = "2026.07.30-1"
OLD_VERSION = "2026.07.29-1"
UPDATED_AT = "2026-07-30"

HTML_REPLACEMENTS = {
    "ch09": [
        (
            "<p>APT 的套利邏輯需要充分分散與近似無套利條件。實務因子模型可以是理論因子或經驗因子，但找到歷史上有效的因子不等於未來一定持續，也不代表任何「因子投資」沒有模型與資料探勘風險。</p>",
            "<p>APT 的套利邏輯需要充分分散與近似無套利條件。實務因子模型可以是理論因子或經驗因子，但找到歷史上有效的因子不等於未來一定持續，也不代表任何「因子投資」沒有模型與資料探勘風險。</p><p>若把報酬式的截距直接寫成 E[R_i]，共同因子 F_j 應定義為相對預期值的「意外變動／已去均值因子」，使 E[F_j]=0；殘差 e_i 也取 E[e_i]=0。若 F_j 不是零均值，截距就不能不加說明地直接等同 E[R_i]。</p>",
        ),
        (
            "<div class=\"formula-card\"><p class=\"math display\">\\[R_i=E[R_i]+\\beta_{i1}F_1+\\cdots+\\beta_{ik}F_k+e_i\\]</p><p>一般多因子報酬表示。</p></div>",
            "<div class=\"formula-card\"><p class=\"math display\">\\[R_i=E[R_i]+\\beta_{i1}F_1+\\cdots+\\beta_{ik}F_k+e_i\\]</p><p>一般多因子報酬表示；此寫法把 F_j 定義為零均值的因子 surprise／去均值因子，且 E[e_i]=0，因此截距才可直接寫成 E[R_i]。</p></div>",
        ),
    ],
    "ch13": [
        (
            "<div class=\"formula-card\"><p class=\"math display\">\\[ROE=\\frac{NI}{Sales}\\times\\frac{Sales}{Assets}\\times\\frac{Assets}{Equity}\\]</p><p>三段 DuPont 分解。</p></div>",
            "<div class=\"formula-card\"><p class=\"math display\">\\[ROE=\\frac{NI}{Sales}\\times\\frac{Sales}{Average\\ Assets}\\times\\frac{Average\\ Assets}{Average\\ Equity}\\]</p><p>三段 DuPont 分解。當分子是期間流量、資產與權益是資產負債表存量時，通常以期初期末平均資產與平均權益配對，以維持期間口徑一致。</p></div>",
        ),
        (
            "<ul><li>ROE 高就一定代表公司品質高。</li><li>用期末權益代替平均權益而不看題目口徑。</li><li>把 b×ROE 當成任何公司的永久成長保證。</li></ul>",
            "<ul><li>ROE 高就一定代表公司品質高。</li><li>自行由財報計算 ROE／資產週轉率／權益乘數時，只拿期末資產或期末權益，卻忽略期間流量通常應和平均存量配對。</li><li>把 b×ROE 當成任何公司的永久成長保證。</li></ul>",
        ),
    ],
    "ch15": [
        (
            "<dt>凸性（Convexity）</dt><dd>債券價格—殖利率曲線二階彎曲程度。</dd><dt>免疫（Immunization）</dt><dd>透過資產負債現值與利率敏感度配對，降低利率變動對目標的影響。</dd>",
            "<dt>凸性（Convexity）</dt><dd>債券價格—殖利率曲線的二階彎曲程度；本章公式採以價格正規化的二階價格敏感度。</dd><dt>免疫（Immunization）</dt><dd>透過資產與負債的現值及利率敏感度配對，降低利率變動使未來給付不足的風險。單一負債常以資產價值與 Macaulay duration 對應負債／投資期限；多筆負債則常比較 market value 與 money duration／BPV，並留意凸性、現金流分散與殖利率曲線形狀風險。</dd>",
        ),
        (
            "<div class=\"formula-card\"><p class=\"math display\">\\[\\frac{\\Delta P}{P}\\approx-D_{mod}\\Delta y+\\frac{1}{2}Conv(\\Delta y)^2\\]</p><p>加入凸性的二階近似。</p></div>",
            "<div class=\"formula-card\"><p class=\"math display\">\\[Conv=\\frac{1}{P}\\frac{\\partial^2P}{\\partial y^2}\\]</p><p>本章凸性口徑；固定現金流並以同一殖利率 y 衡量時，為價格正規化的二階敏感度。</p></div><div class=\"formula-card\"><p class=\"math display\">\\[\\frac{\\Delta P}{P}\\approx-D_{mod}\\Delta y+\\frac{1}{2}Conv(\\Delta y)^2\\]</p><p>加入凸性的二階近似；若採其他 convexity 定義或複利口徑，係數與尺度必須一致。</p></div>",
        ),
        (
            "<ul><li>0.20 個百分點代成 0.20。</li><li>duration 近似被當成任何利率變動下的精確答案。</li><li>Macaulay duration 與 modified duration 不分。</li><li>免疫後就永遠不需再平衡。</li></ul>",
            "<ul><li>0.20 個百分點代成 0.20。</li><li>duration 近似被當成任何利率變動下的精確答案。</li><li>Macaulay duration 與 modified duration 不分。</li><li>只做 duration matching 就宣稱免疫永遠完成；時間、殖利率與曲線形狀變化都可能要求再平衡。</li></ul>",
        ),
    ],
    "ch17": [
        (
            "<div class=\"formula-card\"><p class=\"math display\">\\[F_0\\approx S_0(1+r)^T\\]</p><p>無收益標的簡化成本持有關係；實務需調整股利、收益、儲存成本等。</p></div>",
            "<div class=\"formula-card\"><p class=\"math display\">\\[F_0=S_0(1+r)^T\\]</p><p>無收益、無其他持有成本／利益、可按 r 融資或投資且無套利時的離散複利成本持有等式；有股利、收益、儲存成本或便利收益時必須調整。</p></div>",
        ),
    ],
    "ch19": [
        (
            "<p>共同基金與 ETF 都能把許多標的包成一個投資工具，降低投資人自行建立大型組合的操作成本。指數化策略則試圖複製特定基準，而不是預測每一檔證券的相對勝負。</p>",
            "<p>共同基金與 ETF 都是集合投資工具，可持有一籃子資產並降低投資人自行建立大型組合的操作成本；但 ETF 描述的是「在交易所交易的基金架構」，本身不等於被動指數化。ETF 可以採被動追蹤，也可以採主動管理；指數化策略才是以複製特定基準為主要目標的被動管理方式。</p>",
        ),
        (
            "<dl class=\"term-list\"><dt>淨資產價值（NAV）</dt>",
            "<dl class=\"term-list\"><dt>ETF（Exchange-Traded Fund）</dt><dd>在交易所上市交易的基金架構；可以被動追蹤指數，也可以主動管理，不能把 ETF 與 indexing 當成同義詞。</dd><dt>淨資產價值（NAV）</dt>",
        ),
        (
            "<ul><li>ETF 一定等於低風險且充分分散。</li><li>市價永遠等於 NAV。</li><li>只看費用率，不看追蹤誤差與交易成本。</li><li>把每日槓桿倍數直接乘上長期指數累積報酬。</li></ul>",
            "<ul><li>把 ETF 當成「一定被動追蹤指數」或「一定低風險且充分分散」；ETF 是交易架構，管理方式與集中度要另外判斷。</li><li>市價永遠等於 NAV。</li><li>只看費用率，不看追蹤誤差與交易成本。</li><li>把每日槓桿倍數直接乘上長期指數累積報酬。</li></ul>",
        ),
    ],
    "ch20": [
        (
            "<dt>匯率風險（Currency Risk）</dt><dd>外幣資產換回本幣時因匯率變動造成的報酬不確定性。</dd>",
            "<dt>匯率風險（Currency Risk）</dt><dd>外幣資產換回本幣時因匯率變動造成的報酬不確定性。本章固定 S_t 為「1 單位外幣可兌換的本幣金額」，因此外幣升值代表 S 上升。</dd>",
        ),
        (
            "<div class=\"formula-card\"><p class=\"math display\">\\[R_{home}\\approx(1+R_{foreign})(1+R_{FX})-1\\]</p><p>外幣資產本幣報酬的乘法關係；R_FX 定義需先固定匯率方向。</p></div>",
            "<div class=\"formula-card\"><p class=\"math display\">\\[1+R_{home}=(1+R_{foreign})(1+R_{FX}),\\qquad R_{FX}=\\frac{S_1}{S_0}-1\\]</p><p>外幣資產本幣報酬的精確乘法關係；本章 S_t 固定為本幣／外幣報價。只有在報酬都很小時，R_home≈R_foreign+R_FX 才是可用的一階近似。</p></div>",
        ),
        (
            "<p>再平衡不是為了預測哪一類資產下一期一定上漲，而是控制風險暴險回到既定政策。</p>",
            "<p>再平衡不是為了預測哪一類資產下一期一定上漲，而是控制風險暴險回到既定政策。</p><p>國際投資例：若外幣資產以外幣計價上漲 10%，同期間該外幣相對本幣升值 5%，則本幣報酬=(1.10)(1.05)−1=15.5%，不是把 10% 與 5% 直接相加成精確的 15%。</p>",
        ),
        (
            "<ul><li>分散化保證不會虧損。</li><li>時間視野長就能忽略所有風險。</li><li>再平衡等於看到下跌就隨意加碼。</li><li>國際分散只增加好處、不增加匯率或制度風險。</li></ul>",
            "<ul><li>分散化保證不會虧損。</li><li>時間視野長就能忽略所有風險。</li><li>再平衡等於看到下跌就隨意加碼。</li><li>國際分散只增加好處、不增加匯率或制度風險。</li><li>沒有先固定匯率報價方向，或把 R_foreign+R_FX 當成任何幅度下都精確的本幣報酬。</li></ul>",
        ),
    ],
    "ch21": [
        (
            "<div class=\"formula-card\"><p class=\"math display\">\\[IR=\\frac{R_P-R_B}{\\sigma(R_P-R_B)}\\]</p><p>資訊比率；分子通常用平均主動報酬。</p></div>",
            "<div class=\"formula-card\"><p class=\"math display\">\\[IR=\\frac{\\overline{R_P-R_B}}{\\sigma(R_P-R_B)}\\]</p><p>資訊比率；分子是同一評估期間內的平均主動報酬，分母是主動報酬的標準差（tracking error），兩者的期間與年化口徑必須一致。</p></div>",
        ),
    ],
    "appendix-a": [
        (
            "\\(R_i=E[R_i]+\\beta_{i1}F_1+\\cdots+\\beta_{ik}F_k+e_i\\)</td><td>一般多因子報酬表示。</td>",
            "\\(R_i=E[R_i]+\\beta_{i1}F_1+\\cdots+\\beta_{ik}F_k+e_i\\)</td><td>此寫法要求 F_j 為零均值的因子 surprise／去均值因子，且 E[e_i]=0。</td>",
        ),
        (
            "\\(ROE=\\frac{NI}{Sales}\\times\\frac{Sales}{Assets}\\times\\frac{Assets}{Equity}\\)</td><td>三段 DuPont 分解。</td>",
            "\\(ROE=\\frac{NI}{Sales}\\times\\frac{Sales}{Average\\ Assets}\\times\\frac{Average\\ Assets}{Average\\ Equity}\\)</td><td>三段 DuPont；期間流量通常與平均資產／平均權益存量配對。</td>",
        ),
        (
            "\\(F_0\\approx S_0(1+r)^T\\)</td><td>無收益標的簡化成本持有關係；實務需調整股利、收益、儲存成本等。</td>",
            "\\(F_0=S_0(1+r)^T\\)</td><td>無收益、無其他 carry、可按 r 融資／投資且無套利時的離散複利等式。</td>",
        ),
        (
            "\\(R_{home}\\approx(1+R_{foreign})(1+R_{FX})-1\\)</td><td>外幣資產本幣報酬的乘法關係；R_FX 定義需先固定匯率方向。</td>",
            "\\(1+R_{home}=(1+R_{foreign})(1+R_{FX})\\)</td><td>精確乘法關係；本章固定 S 為本幣／外幣，R_FX=S_1/S_0-1。</td>",
        ),
        (
            "\\(IR=\\frac{R_P-R_B}{\\sigma(R_P-R_B)}\\)</td><td>資訊比率；分子通常用平均主動報酬。</td>",
            "\\(IR=\\frac{\\overline{R_P-R_B}}{\\sigma(R_P-R_B)}\\)</td><td>平均主動報酬除以 tracking error；期間／年化口徑需一致。</td>",
        ),
    ],
    "appendix-c": [
        (
            "<tr><td>Exchange-Traded Fund</td><td>指數股票型基金 ETF</td></tr>",
            "<tr><td>Exchange-Traded Fund</td><td>交易所交易基金 ETF（臺灣被動式 ETF 法規中文名稱為「指數股票型基金」；另有主動式 ETF）</td></tr>",
        ),
    ],
}

QUESTION_UPDATES = {
    "ch09-q03": {
        "explanation": "APT 可包含多個共同因子。若報酬生成式把截距直接寫成 E[R_i]，因子通常以零均值的 surprise／去均值變動表示，殘差也取零均值；這和「哪些因子具有風險溢酬」是不同問題。"
    },
    "ch13-q01": {
        "explanation": "題目已直接給淨利率、資產週轉率與權益乘數，因此 ROE=0.05×2×1.5=0.15。若是自行由財報計算後兩項比率，期間銷售通常要和平均資產配對，權益乘數也常以平均資產／平均權益計算。"
    },
    "ch15-q05": {
        "explanation": "時間經過、殖利率與現金流變化都會改變 duration，通常需要再平衡。單一負債常同時關注資產價值與 Macaulay duration；多筆負債還會比較 market value、money duration／BPV，並留意凸性與曲線形狀風險。"
    },
    "ch19-q04": {
        "explanation": "ETF 是在交易所交易的基金架構，不等於一定被動追蹤指數，也不保證充分分散。主動式、產業型、主題型或高度集中 ETF 都可能集中於少數風險來源。"
    },
    "ch20-q04": {
        "explanation": "還可能包含政治、稅務、流動性與市場制度差異。匯率效果要先固定報價方向；若 S 是本幣／外幣，則 1+R_home=(1+R_foreign)(1+R_FX)。"
    },
    "ch21-q04": {
        "explanation": "IR=平均主動報酬/追蹤誤差；tracking error 是 RP−RB 的標準差，分子與分母需使用一致的期間／年化口徑。"
    },
}
