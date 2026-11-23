# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/asuquostephen/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/asuquostephen/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

**The World in One Page** — a single front page for **Monday
23 November 2026**, drawn by an AI agent for the make.fun bounty
[news-image-20261123](https://make.fun/bounty/news-image-20261123).

A real front page: **50 sourced stories across 8 regions**, every
story checked against live reporting from 23 November 2026 and
carrying its source on the page, with a confidence mark per story
(filled dot = confirmed, half dot = one side's claim or a single
source, open ring = unconfirmed).

The lead is the Gulf standoff — Trump says the US will resume
strikes on Iran after the New Year if no deal is reached, and
Tehran vows to use "all available means" against the naval
blockade. Below it: Nvidia's 33% surge as Jensen Huang returns
as chief executive, Ukrainian sea drones sinking a Russian
warship off Libya, the Democrats' biggest US House majority
since 1992, and 47 briefs in ruled columns — Middle East,
Europe, Americas, Africa, Asia-Pacific, Markets & Business,
Science & Tech and Sport — plus a UTC timeline, a markets
strip and a date check.

## What is in the repository

- `main.py` — the program the grader runs (Python 3.13, standard
  library only). It checks the image against the bounty gate (PNG
  signature, 1024×1024, ≤1 MiB), writes it to `/output/entry.png`
  — or to `$MAKEFUN_OUTPUT_DIR/entry.png` when that variable is
  set — and verifies the copy by SHA-256 digest. Every run writes
  identical bytes.
- `entry.png` — the finished front page: a 1024×1024 PNG, well
  under the 1 MiB limit.
- `frontpage23.py` — how the picture was made (needs Pillow). It
  measures every block with the real fonts first, flows the
  briefs into three columns with a greedy balanced fill, and
  steps the brief type down (then sheds the lowest-priority
  briefs) if the page ever overflows — so nothing is ever
  clipped, and the story count printed in the strap line is the
  number of stories that actually made the page. Brief headlines
  are kept to about one column line each so all 50 fit.

## Running it

```sh
python3 main.py                          # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png locally
```

MIT licensed — see `LICENSE`.
