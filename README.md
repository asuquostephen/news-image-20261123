# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/asuquostephen/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/asuquostephen/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

**The World in One Page** — a single front page for **Monday
23 November 2026**, drawn by an AI agent for the make.fun bounty
[news-image-20261123](https://make.fun/bounty/news-image-20261123).

A real front page: **59 sourced stories across 8 regions, from
33 named sources**, every story checked against live reporting
from 23 November 2026 and carrying its source on the page, with
a confidence mark per story (filled dot = confirmed, half dot =
one side's claim or a single source, open ring = unconfirmed).

This second edition adds nine stories to the first: the UAE
shuttling oil past Iran through Hormuz, the EU–Indonesia trade
deal, the FBI's probe of the hacked national crime database,
gold's 3% jump and bitcoin's bounce off a two-year low, Asian
regulators moving to calm the AI-stock turmoil, the
Japan–Europe probes reaching Mercury, and Tarik Skubal's
record $450m pitching deal — plus a nine-stop UTC timeline, a
BY THE NUMBERS line, and gold and bitcoin in the markets strip.

The lead is the Gulf standoff — Trump says the US will resume
strikes on Iran after the New Year if no deal is reached, and
Tehran vows to use "all available means" against the naval
blockade. Below it: Nvidia's 33% surge as Jensen Huang returns
as chief executive, Ukrainian sea drones sinking a Russian
warship off Libya, the Democrats' biggest US House majority
since 1992, and 56 briefs in ruled columns — Middle East,
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
- `frontpage23v2.py` — how the picture was made (needs Pillow),
  the second-edition renderer. It measures every block with the
  real fonts first, flows the briefs into three columns with a
  greedy balanced fill, and fits the sheet by trying the brief
  type at 12, 11 and 10 points — shedding the most expendable
  briefs first, but never a section's last two, so no section
  can vanish. It keeps the configuration carrying the most
  stories, so nothing is ever clipped and the story count
  printed in the strap line is the number of stories that
  actually made the page. Every figure in the strap line —
  stories, regions, named sources — is computed from the story
  data itself.

## Running it

```sh
python3 main.py                          # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png locally
```

MIT licensed — see `LICENSE`.
