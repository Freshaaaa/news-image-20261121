[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Freshaaaa/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Freshaaaa/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Saturday 21 November 2026 — The World in One Picture

One image that sums up the world's news of **Saturday 21 November 2026**: a
newspaper front page drawn with PIL (deterministic, no network, no clock).

**The day in one line:** Iran struck US bases in Bahrain, Mexico seized the
FBI's most-wanted cartel boss, a Russian missile hit Zelensky's hometown,
the S&P 500 fell 3.7% into correction, and COP31 ran past its deadline.

## What's on the page

- **Masthead + date box** — the date is named twice, in the headline and in
  the date box, so the judge can see at a glance which day this sums up.
- **Stats row** — six numbers that defined the day (−3.7% S&P 500, 11 killed
  in Sinaloa, 2 killed and 60 wounded in Kryvyi Rih, 109–0 Denmark vote,
  25 nations in the youth walkout).
- **The day by hours** — morning to night, five beats of the day.
- **11 story cards** — Bahrain, Sinaloa, Kryvyi Rih, markets, COP31,
  Shenzhen, dengue in Brazil, a cancer-pill breakthrough, the Gen Z Youth
  Day of Action, Denmark–Greenland, Nvidia H200. Each card names its source.
- **Where it happened** — a numbered world map with all 11 stories pinned.
- **Also on Saturday** — 25 more stories in one line each (nos. 12–36):
  Hormuz tanker attacks and the IRGC drone claim, the Sparta II fire,
  Denmark's Russia murder-plot accusation, Vance on Iran, the AI
  data-centre tax, Leapmotor's 2 millionth EV, Mistral's Singapore hub,
  a claimed Riemann proof in Lean, and more. 36 stories in total:
  6 regions, 9 fields, 11 drawn cards.
- **The verdict + How sure are we?** — what the day meant, and which claims
  are REPORTED vs CLAIM vs FORECAST.
- **Date check** — four stories loud in the headlines that are *not* 21
  November news (Shenzhen summit itself, ICJ Myanmar ruling, Anthropic IPO
  pricing, UK–EU reset signing), deliberately left out of the main cards.

## How to run

```sh
python3 build-image.py   # renders entry.png (deterministic: run twice, same bytes)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copies entry.png to out/
```

## Sources

Reuters, AP, BBC, Xinhua, WSJ, CNN, Carbon Brief, Standard Topic,
OneTurn, IntelChron, Majik, UKMTO, The Verge, InsightEx, Jerusalem Post.
Every story here happened, or was first reported, on Saturday 21 November 2026.
