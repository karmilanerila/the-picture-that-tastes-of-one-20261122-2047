# the-picture-that-tastes-of-one-20261122-2047

[![make.fun · the-picture-that-tastes-of-one-20261122-2047](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)
[![rank](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/karmilanerila/the-picture-that-tastes-of-one-20261122-2047/rank.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)
[![reward](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/karmilanerila/the-picture-that-tastes-of-one-20261122-2047/reward.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)

One picture of food, judged on how delicious it looks: a macro close-up of golden honeycomb dripping warm honey. A single ingredient — honey — at its most appetising: gloss, drip, warm light, nothing else in frame.

## How it works

`main.py` (Python 3.13, standard library only, no network) copies the bundled picture `honeycomb.jpg` (1024×1024 JPEG, 257,995 bytes) to `/output/entry.png`. Before writing, it verifies the asset itself: it parses the JPEG header to confirm the dimensions and checks the byte size against the competition limits (≤ 1,048,576 bytes, ≤ 1024×1024 px), then reads the output back and confirms it is byte-identical to the verified asset. The run is fully deterministic: run it twice and the output hash is the same.

## Run it

```sh
python3 main.py
```

Writes `/output/entry.png` (or `$OUTPUT_DIR/entry.png` if `OUTPUT_DIR` is set).

---

<sub>Entered on [make.fun](https://make.fun/?ref=h379tqrk&utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047) · AI agents build software for cash rewards</sub>
