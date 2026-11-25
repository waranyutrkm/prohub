# ProHub — Global Market Breadth & Rotation Intelligence

> **Deterministic Multi-Asset Quantitative Research Terminal**  
> วิเคราะห์ความแข็งแรงของตลาดผ่าน MACD Breadth · 169 Symbols · 8 Market Groups · Historical Heatmap & Breadth Rotation

[![Daily refresh](https://github.com/waranyutrkm/prohub/actions/workflows/publish.yml/badge.svg)](https://github.com/waranyutrkm/prohub/actions/workflows/publish.yml)
[Dashboard](https://waranyutrkm.github.io/prohub/) · [Workflow](https://github.com/waranyutrkm/prohub/actions) · [Design Standard](DESIGN.md)

## 1. System Overview — ระบบนี้ตอบคำถามอะไร

ProHub เป็นเครื่องมือวิจัยอิสระที่ต่อยอดแนวคิด Penguin Market Breadth จาก Pine Script และใช้สถาปัตยกรรมจาก [Global Capital Flow Lab](https://github.com/waranyutrkm/global-capital-flow-lab) โดยย้ายการคำนวณไป Python เพื่อไม่ต้องจำกัด Universe ตามจำนวน request.security ของ TradingView

คำถามหลักคือ ตลาดส่วนใหญ่ในแต่ละกลุ่มอยู่ในขาขึ้นหรือขาลง? โมเมนตัมสอดคล้องกับแนวโน้มหรือไม่? และการเปลี่ยนสภาวะเริ่มจากกลุ่มใด? ระบบวัด **การมีส่วนร่วมของสมาชิกในแนวโน้ม** ไม่ใช่ผลตอบแทนถ่วงน้ำหนักตามมูลค่าตลาด ไม่ใช่เงินทุนไหลเข้าออก และไม่ได้ส่งคำสั่งซื้อขาย

| มิติ | Penguin รายสินทรัพย์ | ProHub |
|---|---|---|
| หน่วยวิเคราะห์ | ราคาและความผันผวนรายตัว | สัดส่วนสถานะของสมาชิกแต่ละตลาด |
| ภาพอดีต | Indicator บนกราฟ | Historical Heatmap |
| ภาพปัจจุบัน | Trend / RSI / Diff | Rotation และ Ranking |

## 2. Asset Universe — ขอบเขตข้อมูล

| Market | Requested | ตัวอย่าง |
|---|---:|---|
| US Stocks | 39 | `AAPL`, `MSFT`, `NVDA`, `AMZN` |
| Global Index | 30 | `^GSPC`, `^DJI`, `^IXIC`, `^RUT` |
| Thailand Sectors (stock proxies) | 30 | `BBL.BK`, `KBANK.BK`, `KTB.BK`, `SCB.BK` |
| Crypto | 30 | `BTC-USD`, `ETH-USD`, `SOL-USD`, `XRP-USD` |
| Bond Yield (US curve) | 4 | `^IRX`, `^FVX`, `^TNX`, `^TYX` |
| Currency (vs USD) | 15 | `EURUSD=X`, `GBPUSD=X`, `AUDUSD=X`, `NZDUSD=X` |
| Agriculture | 16 | `ZC=F`, `ZS=F`, `ZW=F`, `KC=F` |
| Metals | 5 | `GC=F`, `SI=F`, `HG=F`, `PL=F` |
| **Total** | **169** | |

Universe ตั้งค่าใน [universe.json](universe.json) เป็นรายการคงที่ ไม่ใช่สมาชิกดัชนีย้อนหลังตามเวลา หุ้นไทยเป็นตัวแทนรายบริษัท ไม่ใช่ดัชนี Sector จริง; Bond Yield เป็นเส้นผลตอบแทนพันธบัตรสหรัฐฯ ไม่ใช่พันธบัตรทั่วโลก; FX เป็นคู่เทียบ USD ตาม ticker ที่กำหนด และต้องตรวจสอบความพร้อมของแต่ละ ticker; futures เป็นราคา continuous ตามผู้ให้ข้อมูล ไม่ได้จำลองการ roll หรือผลตอบแทนจากการถือสัญญาจริง

<details><summary>Full configured universe</summary>

**US Stocks (39)**: `AAPL`, `MSFT`, `NVDA`, `AMZN`, `GOOG`, `META`, `BRK-B`, `TSLA`, `LLY`, `UNH`, `V`, `WMT`, `XOM`, `JPM`, `JNJ`, `PG`, `MA`, `AVGO`, `HD`, `ORCL`, `CVX`, `MRK`, `ABBV`, `COST`, `KO`, `ADBE`, `PEP`, `CSCO`, `BAC`, `CRM`, `MCD`, `LIN`, `ACN`, `NFLX`, `PFE`, `TMO`, `TMUS`, `CMCSA`, `ABT`

**Global Index (30)**: `^GSPC`, `^DJI`, `^IXIC`, `^RUT`, `^FTSE`, `^GDAXI`, `^FCHI`, `^STOXX50E`, `^N225`, `^HSI`, `000001.SS`, `399001.SZ`, `^KS11`, `^TWII`, `^AXJO`, `^NZ50`, `^STI`, `^JKSE`, `^KLSE`, `^SET.BK`, `^BSESN`, `^NSEI`, `^BVSP`, `^MXX`, `^GSPTSE`, `^SSMI`, `^AEX`, `^IBEX`, `^OMX`, `^TA125.TA`

**Thailand Sectors (stock proxies) (30)**: `BBL.BK`, `KBANK.BK`, `KTB.BK`, `SCB.BK`, `TTB.BK`, `PTT.BK`, `PTTEP.BK`, `TOP.BK`, `BANPU.BK`, `GULF.BK`, `CPALL.BK`, `CPAXT.BK`, `BJC.BK`, `HMPRO.BK`, `GLOBAL.BK`, `ADVANC.BK`, `TRUE.BK`, `BDMS.BK`, `BH.BK`, `BCH.BK`, `AOT.BK`, `BEM.BK`, `BTS.BK`, `SCC.BK`, `SCGP.BK`, `IVL.BK`, `CPF.BK`, `TU.BK`, `CPN.BK`, `AWC.BK`

**Crypto (30)**: `BTC-USD`, `ETH-USD`, `SOL-USD`, `XRP-USD`, `BNB-USD`, `ADA-USD`, `DOGE-USD`, `TRX-USD`, `TON-USD`, `LINK-USD`, `DOT-USD`, `LTC-USD`, `BCH-USD`, `SHIB-USD`, `AVAX-USD`, `XLM-USD`, `XMR-USD`, `ATOM-USD`, `ETC-USD`, `UNI-USD`, `FIL-USD`, `ICP-USD`, `HBAR-USD`, `LDO-USD`, `CRO-USD`, `VET-USD`, `NEAR-USD`, `QNT-USD`, `AAVE-USD`, `SUI-USD`

**Bond Yield (US curve) (4)**: `^IRX`, `^FVX`, `^TNX`, `^TYX`

**Currency (vs USD) (15)**: `EURUSD=X`, `GBPUSD=X`, `AUDUSD=X`, `NZDUSD=X`, `JPYUSD=X`, `CADUSD=X`, `CHFUSD=X`, `MXNUSD=X`, `BRLUSD=X`, `ZARUSD=X`, `NOKUSD=X`, `SEKUSD=X`, `PLNUSD=X`, `SGDUSD=X`, `THBUSD=X`

**Agriculture (16)**: `ZC=F`, `ZS=F`, `ZW=F`, `KC=F`, `CC=F`, `DC=F`, `GF=F`, `HE=F`, `KE=F`, `LE=F`, `SB=F`, `ZL=F`, `ZM=F`, `ZO=F`, `ZR=F`, `CT=F`

**Metals (5)**: `GC=F`, `SI=F`, `HG=F`, `PL=F`, `PA=F`

</details>

## 3. Deterministic MACD State Engine

สำหรับราคาปิดของสินทรัพย์แต่ละตัว คำนวณ EMA บนวันที่มีข้อมูลจริงก่อนจัดแนวปฏิทิน ใช้ EMA แบบ recursive (adjust=False) และ min_periods ตามความยาวของแต่ละเส้น

$$EMA_t=\alpha P_t+(1-\alpha)EMA_{t-1},\quad \alpha=\frac{2}{L+1}$$

$$M_t=EMA_{12}(P_t)-EMA_{26}(P_t),\quad S_t=EMA_9(M_t)$$

| State | เงื่อนไข | ค่า | ความหมาย |
|---|---|---:|---|
| UF — Up Full | M > 0 และ M > S | +2 | แนวโน้มบวก โมเมนตัมบวก |
| UP — Up Pause | M > 0 และ M < S | +1 | แนวโน้มบวก โมเมนตัมลบ |
| DP — Down Pause | M < 0 และ M > S | -1 | แนวโน้มลบ โมเมนตัมบวก |
| DF — Down Full | M < 0 และ M < S | -2 | แนวโน้มลบ โมเมนตัมลบ |
| Neutral | M = 0 หรือ M = S เมื่อข้อมูลพร้อม | 0 | ไม่เข้าเงื่อนไขสี่สถานะ |
| Missing | ข้อมูลไม่พร้อม | NaN | ไม่รวมในตัวหาร |

ต้องมีราคาปิดจริงอย่างน้อย 34 ตัวอย่างสำหรับ MACD และ Signal ตามค่าเริ่มต้น 12/26/9 ก่อนสถานะแรกที่คำนวณได้ การคำนวณใช้ Close ที่ Yahoo ส่งกลับเมื่อ auto_adjust=False ไม่ใช่การวิเคราะห์ total return ที่ปรับเงินปันผลครบถ้วน

## 4. Breadth Mathematics — สูตรคะแนนทั้งห้า

กำหนด UF, UP, DP, DF เป็นจำนวนสมาชิกแต่ละสถานะ, N เป็นจำนวนสมาชิกที่คำนวณสถานะได้ (รวม Neutral) และ w เป็นน้ำหนัก Pause

| Metric | Formula | Interpretation |
|---|---|---|
| Trend | 100 × (UF + UP − DF − DP) / N | สัดส่วน MACD บวกหัก MACD ลบ |
| Momentum | 100 × (UF + DP − DF − UP) / N | สัดส่วน MACD เหนือ Signal หักใต้ Signal |
| Full | 100 × (UF − DF) / N | ความต่างของแนวโน้มเต็มตัว |
| Pausing | 100 × (UP − DP) / N | ความต่างของกลุ่มพักตัว |
| Composite | 100 × (UF + w×UP − DF − w×DP) / N | คะแนนรวมลดน้ำหนักสถานะพักตัว |

ทุกคะแนนอยู่ในช่วง -100 ถึง +100 เมื่อ 0 ≤ w ≤ 1 ค่าเริ่มต้น w=0.5; w=0 เท่ากับ Full และ w=1 เท่ากับ Trend โดยประมาณเมื่อปัดเศษข้อมูลใน UI

$$Composite=\frac{1+w}{2}Trend+\frac{1-w}{2}Momentum$$

สมการนี้แสดงว่า Composite เป็นผลรวมเชิงเส้นของสองแกน ไม่ใช่สัญญาณอิสระเพิ่มเติม ค่า w=0.5 เทียบเท่าน้ำหนัก Trend 75% และ Momentum 25%

### ตัวอย่างคำนวณ (ข้อมูลสมมติ)

มีสมาชิกที่ใช้ได้ 20 ตัว: UF=8, UP=4, DP=3, DF=4, Neutral=1

| Metric | Result |
|---|---:|
| UF / UP / DP / DF / Neutral | 40% / 20% / 15% / 20% / 5% |
| Trend | +25 |
| Momentum | +15 |
| Full | +20 |
| Pausing | +5 |
| Composite (w=0.5) | +22.5 |

หาก Universe มี 25 ตัว Coverage=20/25=80% จึงผ่านเกณฑ์ 60% คะแนนจะไม่คำนวณเมื่อ Coverage ต่ำกว่าเกณฑ์ ตัวอย่างนี้ไม่ใช่ผลตลาดจริงหรือผล Backtest

## 5. Historical Heatmap — อ่านประวัติตลาด

แกน X เป็นวันปฏิทิน แกน Y เป็นกลุ่มตลาด สีใช้สเกลคงที่ -100 ถึง +100 ทำให้เปรียบเทียบคะแนนระหว่างวันได้โดยไม่ต้องปรับสีตามช่วงข้อมูล

| สี / คะแนน | การตีความ |
|---|---|
| เขียวเข้ม ใกล้ +100 | สมาชิกส่วนมากสนับสนุนคะแนนด้านบวก |
| เขียวอ่อน | คะแนนบวกแต่ไม่ทั่วทั้งตลาด |
| เทา ใกล้ 0 | คะแนนสุทธิใกล้สมดุล ไม่จำเป็นต้องเป็น Neutral ทุกตัว |
| แดงอ่อน | คะแนนลบ |
| แดงเข้ม ใกล้ -100 | สมาชิกส่วนมากสนับสนุนคะแนนด้านลบ |
| ช่องว่าง | ข้อมูลไม่ผ่านเกณฑ์ ไม่ใช่คะแนนศูนย์ |

เลือก Composite เพื่ออ่านภาพรวม, Trend เพื่อดูทิศทาง MACD, Momentum เพื่อดูการเปลี่ยนแรง, Full เพื่อดูความต่างของแนวโน้มเต็มตัว และ Pausing เพื่อดูสภาวะพักตัว

ตัวอย่างการศึกษา: เปรียบเทียบช่วงที่ Trend ยังติดลบแต่ Momentum เริ่มบวก หรือช่วงที่หลายกลุ่มเปลี่ยนจากเขียวเป็นแดงพร้อมกัน ห้ามตีความว่าเหตุการณ์เหล่านี้รับประกันผลตอบแทนในอนาคต

## 6. Breadth Rotation Map — แผนที่การเปลี่ยนสภาวะ

แกน X = Trend Breadth; แกน Y = Momentum Breadth; ทั้งสองแกนมีหน่วยเป็นคะแนนสุทธิ ไม่ใช่ผลตอบแทน ไม่ได้เปรียบเทียบกับ benchmark และไม่ใช่ RRG แบบ relative strength

| Quadrant | X | Y | ความหมาย |
|---|---|---|---|
| Leading | >0 | >0 | แนวโน้มและโมเมนตัมบวก |
| Weakening | >0 | <0 | แนวโน้มบวก แต่โมเมนตัมลบ |
| Lagging | <0 | <0 | แนวโน้มและโมเมนตัมลบ |
| Recovering | <0 | >0 | แนวโน้มลบ แต่โมเมนตัมบวก |

ตาราง Ranking ใช้ Transition เมื่อ |Trend| ≤ 10 หรือ |Momentum| ≤ 10 และ No data เมื่อไม่มีคะแนน ส่วนแผนภาพแสดงเส้นศูนย์เป็นขอบ Quadrant โดยไม่ได้วาดพื้นที่ Transition แยก

เส้น Trail เชื่อมพิกัดอดีตตามลำดับเวลา จุดใหญ่คือวันที่เลือก จุดเล็กคือประวัติ ระยะ Trail step นับวันปฏิทิน ไม่ใช่ trading sessions ตัวอย่าง 10 จุด ห่างกัน 5 วัน ครอบคลุม 45 วันระหว่างจุดแรกกับจุดล่าสุด

การเคลื่อนจาก Lagging → Recovering → Leading → Weakening เป็นเพียงรูปแบบที่อาจเกิดขึ้น ตลาดสามารถข้าม Quadrant ย้อนกลับ หรือค้างอยู่จุดเดิมได้ การเปรียบเทียบ Bond Yield ต้องระวัง: yield เพิ่มไม่เท่ากับราคาพันธบัตรเพิ่ม

## 7. Market Ranking & Dashboard Controls

ตารางเรียง Composite จากสูงไปต่ำ ณ วันที่เลือก; Coverage แสดง Valid/Requested; Regime มาจาก Trend/Momentum ไม่ใช่จากอันดับ Composite

| Control | Default | Behavior |
|---|---|---|
| As of | วันที่ล่าสุดในไฟล์ | ย้อนดูข้อมูล ณ วันที่เลือก |
| History | 365 วัน | 90 วัน, 1 ปี, 5 ปี, All history |
| Heatmap metric | Composite | เลือกหนึ่งในห้าคะแนน |
| Pause weight | 0.5 | 0–1; คำนวณ Composite ใหม่ใน browser |
| Trail points | 10 | 1–40 |
| Trail step | 5 วัน | 1–90 วันปฏิทิน |
| Export CSV | — | ส่งออก Ranking ณ วันที่เลือก |

MACD periods 12/26/9, Coverage 60% และ stale limit 4 วันเป็นค่าฝั่ง Python ในรุ่นปัจจุบัน ยังไม่มี UI สำหรับเปลี่ยนค่าดังกล่าวหรือ smoothing

## 8. Data Engineering & Architecture

```text
Yahoo Finance / yfinance
  -> batch 15 tickers, up to 3 attempts per batch
  -> observed daily Close (period=max)
  -> MACD state per symbol
  -> align calendar dates; carry state up to 4 days
  -> compute equal-member breadth + coverage
  -> site/breadth.json (atomic replacement)
  -> GitHub Pages / static HTML + JS + Plotly
  -> heatmap, rotation, ranking, CSV
```

ตัดวัน UTC ปัจจุบันออกจากข้อมูลที่เผยแพร่ เพื่อลดความเสี่ยงจากแท่งรายวันที่ยังไม่จบ แต่ไม่ได้ตรวจสอบเวลาปิดตลาดแต่ละแห่งแบบ synchronized timestamp ข้อมูลที่ forward-fill ไม่ใช่ข้อมูลราคาใหม่; สมาชิกที่ขาดข้อมูลเกิน 4 วันจะไม่ถูกนับ การคำนวณ EMA ทำก่อน forward-fill เพื่อไม่สร้าง session เทียม

Coverage = 100 × Valid / Requested; ตัวหาร Requested คือจำนวนสมาชิกที่กำหนดใน Universe แม้ดาวน์โหลดบางตัวไม่สำเร็จ ไม่ใช่จำนวนที่โหลดสำเร็จเท่านั้น ไม่มีการแทน Missing ด้วยคะแนนศูนย์

ไฟล์ JSON มี dates, columns, groups (symbols, available, rows), generated_at และ parameters; ค่า available หมายถึงเคยมีข้อมูลดาวน์โหลดได้ ไม่ใช่สถานะสด ณ วันล่าสุด ข้อมูลราคา raw ไม่อยู่ใน artifact ที่เผยแพร่

## 9. Automation & Deployment

GitHub Actions รันทุกวัน 06:30 UTC (13:30 ICT) รวมวันหยุด, รันเมื่อ push เข้า main และรองรับ workflow_dispatch

1. Checkout และติดตั้ง Python 3.11 / dependencies
2. รัน unit tests
3. ดาวน์โหลดและคำนวณใหม่ทั้ง Universe
4. Configure Pages
5. Upload artifact ด้วยชื่อเฉพาะ run ID / attempt
6. ตรวจสอบว่าพบ artifact ที่ยังไม่หมดอายุหนึ่งชุด
7. Deploy ด้วย artifact ชื่อเดียวกัน

ขั้นตอน 5–6 ถูกเพิ่มหลังพบปัญหา artifact ไม่ปรากฏและ artifact ชื่อซ้ำในการเผยแพร่รอบแรก ๆ ดูสถานะจริงที่ [Actions](https://github.com/waranyutrkm/prohub/actions) ไม่ถือว่าการ commit เป็นหลักฐานว่าเว็บไซต์ออนไลน์แล้ว

ยังไม่มี persistent cache หรือ incremental downloads; การอัปเดตรอบหนึ่งดาวน์โหลดประวัติใหม่ทั้งหมด

## 10. Repository Structure

```text
.
├── .github/workflows/publish.yml
├── engine.py              # MACD states and breadth mathematics
├── refresh.py             # Data download and JSON generation
├── universe.json          # Configured asset universe
├── test_engine.py         # Calculation tests
├── requirements.txt
├── site/
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   └── breadth.json       # Generated at runtime; not committed
├── README.md
├── DESIGN.md
├── AGENTS.md
└── LICENSE
```

## 11. Local Setup

```bash
git clone https://github.com/waranyutrkm/prohub.git
cd prohub
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m unittest -v
python refresh.py
python -m http.server 8000 --directory site
```

เปิด http://localhost:8000 ผ่าน browser (ไม่เปิด HTML ผ่าน file:// เพราะ fetch JSON อาจถูกบล็อก)

สำหรับ GitHub Pages ให้เลือก Settings → Pages → Source: GitHub Actions แล้วตรวจสอบ workflow publish.yml ไม่ต้องสร้าง Static HTML workflow เพิ่ม

## 12. Validation & Empirical Research

ชุด Unit Tests ปัจจุบันตรวจสอบช่วงคะแนนและผลรวมสถานะ, การปิดคะแนนเมื่อ Coverage ไม่พอ และ prefix invariance ของ MACD (ข้อมูลอนาคตไม่เปลี่ยนสถานะในอดีต) ทั้งสามรายการผ่านใน workflow รอบแรก

ยังไม่มีหลักฐานว่า Breadth ทำนายผลตอบแทนหรือชนะ benchmark ไม่มีการรายงาน CAGR, Sharpe, Max Drawdown หรือผล Backtest ที่ยังไม่ได้คำนวณ

แนวทางวิจัยต่อไป (ยังไม่ implement):
- Event study ของการเปลี่ยน Quadrant และ forward returns 5/20/60/120 trading sessions
- เปรียบเทียบ baseline unconditional return, sample size, dispersion และ confidence intervals
- ทดสอบ out-of-sample, walk-forward, transaction costs และ point-in-time universe ก่อนสรุปผลเชิงกลยุทธ์
- เพิ่ม cache/incremental update และ data freshness report ราย Symbol

## 13. Limitations & Disclaimer

- Fixed universe มี survivorship / selection bias; ไม่ใช่ประวัติสมาชิกที่ลงทุนได้จริงทุกช่วง
- ทุกสมาชิกมีน้ำหนักเท่ากันภายในกลุ่ม; กลุ่มที่มี 4 ตัวมีความละเอียดต่ำกว่ากลุ่ม 39 ตัว
- ตลาดมีวันหยุด เวลา close และสกุลเงินต่างกัน; calendar alignment ไม่รับประกันข้อมูลพร้อมกัน
- MACD เป็นตัวชี้วัดแบบ lagging; ไม่ใช่การวัด fund flows หรือ causal signal
- Yahoo Finance อาจจำกัดการร้องขอ เปลี่ยน ticker หรือส่งข้อมูลไม่ครบ; code license ไม่ได้ให้สิทธิ์เผยแพร่ข้อมูลจากผู้ให้บริการ ต้องตรวจสอบเงื่อนไขการใช้และสิทธิ์เผยแพร่ข้อมูล
- ไม่มีการส่งคำสั่งซื้อขาย ไม่มีการรับประกันผลตอบแทน และไม่ได้ตรวจสอบ WCAG conformance โดยอิสระ

จัดทำเพื่อการศึกษาและการวิจัยเชิงปริมาณ ไม่ใช่คำแนะนำลงทุนส่วนบุคคล ดู [LICENSE](LICENSE), [DESIGN.md](DESIGN.md) และ [AGENTS.md](AGENTS.md) สำหรับรายละเอียดเพิ่มเติม
