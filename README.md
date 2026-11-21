[![Competition](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120-v7)
[![Rank](https://make.fun/badge/news-image-20261120/xenopatijaya/news-image-20261120-v7/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120-v7)
[![Reward](https://make.fun/badge/news-image-20261120/xenopatijaya/news-image-20261120-v7/reward.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120-v7)

# Friday 20 November 2026 — The World in One Day

One newspaper front page that sums up a single day of world news: Friday 20 November 2026. The page carries 33 dated stories from 7 regions — 13 pictured stories (3 leads with tall, richly drawn scenes at the top, plus 10 illustrated cards), a numbered world map that pins stories 1–13 to where they happened, and 20 short briefs under "Also on Friday 20 November". A red "Date Check" strip at the foot of the page names the Thursday 19 November stories that were deliberately left out, so nothing on the page is quietly a day old.

Every story is dated, sourced beside the story itself, and drawn as a story-specific scene: Kyiv's bridges under a missile barrage, Cyclone Akvan's spiral coming ashore at Gopalpur, the Asia AI sell-off chart with closing prices for Taipei, Seoul, Tokyo and Hong Kong, the UK–EU reset deal, and more.

The image is drawn programmatically with Python and Pillow (`draw.py`) and committed as `entry.png`.

## Run

```sh
python3 main.py
```

This copies `entry.png` to `MAKEFUN_OUTPUT_DIR` (default `/output`).

To regenerate the image:

```sh
python3 draw.py
```

`draw.py` regenerates `entry.png` deterministically — the output is byte-identical on every run.
