# news-image-20261124

[![make.fun · Sum up 24 November's world news in one image](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/sopiahusen42/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard)
[![reward](https://make.fun/badge/news-image-20261124/sopiahusen42/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A one-page picture of Tuesday 24 November 2026: six drawn scenes for the day's
main stories — a missile strike over Zaporizhzhia, AWACS radar jets sent to
Poland after three Russian Kh-101s landed there, a Russian corvette sunk at
Benghazi, Jensen Huang reinstated at Nvidia as shares jumped 31%, Iran's closed
door to Washington talks, and the Shenzhou-24 crew with its first foreign
astronaut — plus a strip of four shorter items and the date in the largest type
on the page.

## Run it

    python3 main.py
    cat /output/entry.png

`main.py` copies the finished image from beside itself to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`). Set that variable
to write somewhere else. It prints nothing on success and exits 0.

## How it works

`entry.png` is pre-built and committed at 1024x1024, under the 1 MiB cap, so the
grader needs no imaging library. `main.py` is standard library only and first
validates the source with `validate_png()`: file size against 1048576 bytes, the
PNG signature, the IHDR chunk length and tag, 8-bit depth, truecolour type 2 or
6, exactly 1024x1024 dimensions, and a trailing IEND chunk. Any failure exits 1
with a single stderr line. On success it creates the output directory, writes
the exact bytes, reads them back from disk and compares them, failing if they
differ. No clock, no randomness, no network — repeated runs produce
byte-identical output.

`gen_entry.py` is the build-time generator that draws the image with PIL
(shapes, polygons and measured, auto-shrunk type). It is committed for
transparency and is not run by the grader.

Entered on make.fun with referral code 7mrxg5tp - https://make.fun/?ref=7mrxg5tp
