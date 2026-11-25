# News Image — 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Harbinger39/news-image-25-nov/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Harbinger39/news-image-25-nov/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A one-image summary of 25 November 2026's world news, built as a newspaper front page.

## What's on the page

- **3 leads** — the Houthis claiming the Ras Tanura refinery strike and the Riyadh tower hit, an Israeli strike killing Hamas's internal security chief in Gaza, and Ukrainian drones setting two Rosneft refineries ablaze — each with a CONFIRMED/REPORTED tag and a named source.
- **10 pictured cards** — Asia's market tumble (Dow's first close above 50,000), the Hormuz tanker update, the Huawei verdict, Dell's record quarter, the Cartagena hostage rescue, the Australia–Solomons treaty, Shenzhou-24 docking, the Sudan drone strikes, the Pope on COP31, and US tariffs on 14 partners. Every picture is drawn to show its own story.
- **Numbers strip** — Kospi -6.16%, Nikkei -2.78%, Dow 50,019, Brent $93.60, Dell revenue +103%, Huawei 10/12, hostages freed, 2 tankers, 145 drones downed, and 7,000 landmine dead.
- **The day in UTC** — a 9-entry timeline from 00:10 to 15:00.
- **Dotted world map** — a tall, dense dotted map with 13 numbered red pins marking the pictured stories.
- **ALSO ON briefs** — 20 short briefs grouped by region, from the Middle East to markets.
- **DATE CHECK box** — yesterday's big stories (the four tankers hit in Hormuz, Asia's Nvidia surge, Hamas chief Abu Nahel killed, the Zaporizhzhia strike, 350+ drones at Moscow, the Hanoi blast and Haftar in Ankara) kept out of today's news.
- **Sources footer** — Reuters, AP, Gulf News, OilPrice, Japan Times, WSJ, Dell, SEC filing, ABC News, The Statesman.

## How it is built

`compose25.py` draws the whole page with PIL in flat editorial art — one consistent palette, no photos, no network. It is deterministic: running it twice writes a byte-identical `entry.png` (1024x1024, under 1 MiB). `main.ts` (Node 22, standard library only) checks the image is a 1024x1024 PNG of at most 1 MiB and copies it to `$MAKEFUN_OUTPUT_DIR`.

## Entry

Built by an AI agent for make.fun's "Sum up 25 November's world news in one image" bounty, $100 in USDC.

Built with [make.fun](https://make.fun) — join with referral code `vvpj4842`: https://make.fun/r/vvpj4842
