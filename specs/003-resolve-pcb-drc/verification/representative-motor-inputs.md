# 試作前評価に用いる代表モーターの入力

2026-11-15。利用者は代表モーター条件による評価を許容した。以下はいずれもメーカー公表の推奨負荷点であり、起動、拘束、ショートブレーキのピーク値ではない。

| 区分 | 型番・適合 | 適正電圧 | 推奨負荷の電流 | 根拠 |
|---|---|---:|---:|---|
| 標準寄り、両軸 | Tamiya Torque-Tuned 2 Motor PRO、15487 | 2.4–3.0 V | 1.7–2.0 A | [タミヤ](https://www.tamiya.com/japan/products/15487/index.html) |
| 高回転、両軸 | Tamiya Mach-Dash Motor PRO、15433 | 2.4–3.0 V | 2.6–3.5 A | [タミヤ](https://www.tamiya.com/japan/products/15433/index.html) |
| 高負荷参考、片軸 | Tamiya Ultra-Dash Motor、15307 | 2.4–3.0 V | 4.0–5.0 A | [タミヤ](https://www.tamiya.com/japan/products/15307/index.html) |
| 上側参考、片軸 | Tamiya Plasma-Dash Motor、15186 | 2.4–3.0 V | 4.1–5.2 A | [タミヤ](https://www.tamiya.com/japan/products/15186/index.html)。公認レースには使用不可 |

NiMHおよびアルカリ単3形2本を対象とする。資料の適正電圧は、電池開放・負荷変動・過渡を含む実測範囲を示すものではない。既存5 A連続は設計目標であり、上表の5.2 Aを達成済みとも全製品の上限とも扱わない。

実モーターの巻線抵抗、逆起電力、起動・拘束・回生の波形は上表から決定できない。[感度解析](sol-motor-stage-review.md)は明記した仮定で行い、実基板での電流・温度測定は試作後に実施する。試作前には仮定・部品定格・未検証範囲を記録し、実機測定の完了を試作発注の前提としない。
