# The World in One Day — Tuesday 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/surya215/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/surya215/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A broadsheet front page summing up Tuesday 24 November 2026 in a single
1024×1024 image: a big masthead, one dominant lead story, a schematic
share-price chart of Nvidia's 33% bounce, six story panels, and an "In
Brief" strip. The whole image is drawn from scratch in Python with
Pillow — deterministic, no network, no randomness.

## Stories in this edition

- **Lead — HUANG IS BACK:** Nvidia's board voted unanimously on Monday
  to reinstate co-founder Jensen Huang as president and chief executive,
  11 days after he resigned over revelations of extramarital affairs,
  including one with a woman US officials suspect of spying for China.
  Shares jumped about 33% on Monday, adding roughly $1 trillion in
  market value, and the Nasdaq rose 7%. President Trump told CNBC:
  "I made the deal." Huang is due to testify publicly before the Senate
  Banking Committee on 3 December about export controls.
- **Libya:** President Zelenskyy confirmed on Monday that seven
  Ukrainian naval drones sank the Russian corvette Merkury off Benghazi
  on Sunday; a Ka-27 helicopter was destroyed and the cargo ship
  MV Angara hit.
- **Europe:** the European Commission proposed its 22nd sanctions
  package against Russia on Monday — about 60 banks cut from SWIFT,
  70+ more shadow-fleet ships listed, a crypto crackdown, and a ban on
  the Russian flag at EU sports events. All 27 member states must agree.
- **India–Nepal:** India announced on Monday a $1.62bn package for
  flood-hit Nepal — a $377m grant and a $1.24bn credit line — after
  talks with PM Balendra Shah. August floods killed about 1,500 people;
  5,200 are missing.
- **Gaza:** an Israeli airstrike killed at least three Palestinians on
  Tuesday near a police outpost in Khan Younis, medics said; five were
  wounded. Australia, Canada, Italy and the UK urged aid access to
  flooded Gaza.
- **Sport:** FIFA confirmed the 2031 Women's World Cup will be hosted
  by the US, Mexico, Costa Rica and Jamaica; the 2035 edition goes to
  the United Kingdom.
- **Gulf:** Iran's army said on Tuesday it shot down a US drone over
  the Gulf. The US Treasury sanctioned more than two dozen Iranian
  exchange houses and front firms under "Operation Economic Outcast".
- **In Brief:** fresh Russian strikes in the Kyiv region, 24 killed in
  South Sudan, UN talks on lethal AI weapons ending without a pact, the
  ICJ's Thursday ruling that Myanmar committed genocide against the
  Rohingya, the India–New Zealand Wellington Test drawn, the Sparta II
  crew evacuated after a drone hit, three tankers hitting sea mines in
  the Strait of Hormuz, two Russian diplomats expelled from Cyprus,
  North Korean aircraft violating South Korean airspace, and Trump
  halting the Army's Iowa bomb-chemicals plan.

Monday events are labelled as such ("announced Monday", "confirmed on
Monday", "proposed on Monday"); claims by one party are attributed
("Iran's army said", "Zelenskyy confirmed", "medics said"). Sources and
dates are documented in `NEWS.md`.

## How to run

```sh
python3 draw.py        # writes entry.png (1024x1024, RGB, < 1 MiB)
```

`main.ts` (Node 22, stdlib only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).

<sub>Entered on [make.fun](https://make.fun/?ref=vfpg0cj5&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
