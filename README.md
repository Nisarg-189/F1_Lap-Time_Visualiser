# F1_Lap-Time_Visualiser


> Qualifying lap time & sector visualiser powered by [FastF1](https://docs.fastf1.dev/)

Pull every driver's best qualifying lap from any F1 race weekend and visualise who was fastest in each sector — and by exactly how much. Three clean, dark-themed charts saved as PNGs.

---

## What it produces

| Chart | Description |
|---|---|
| `sector_bars.png` | Grouped bar chart of S1 / S2 / S3 times for all drivers. Gold star marks the sector fastest. |
| `lap_times.png` | Horizontal bar chart of full lap times sorted pole → slowest, with delta labels. |
| `sector_deltas.png` | Delta-to-fastest bar chart per sector — shows exactly where time is lost across the grid. |

---

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/f1-lap-lens.git
cd f1-lap-lens
pip install fastf1 matplotlib pandas
```

Requires Python 3.8+.

---

## Usage

```bash
python main.py --year 2024 --gp Bahrain --session Q
```

### All flags

| Flag | Default | Description |
|---|---|---|
| `--year` | `2024` | Championship season |
| `--gp` | `Bahrain` | Grand Prix name (e.g. Monaco, Silverstone, Monza) |
| `--session` | `Q` | `Q` qualifying · `R` race · `FP1/FP2/FP3` practice · `SQ` sprint qualifying |
| `--out` | `output` | Folder to save PNG files |

### Examples

```bash
# 2024 Monaco Qualifying
python main.py --year 2024 --gp Monaco --session Q

# 2023 Italian GP Race
python main.py --year 2023 --gp Monza --session R --out monza_race

# Sprint qualifying weekend
python main.py --year 2024 --gp China --session SQ
```

---

## Project structure

```
f1-lap-lens/
├── main.py          # Entry point + all visualisation logic
├── cache/           # FastF1 auto-populates this (gitignored)
├── output/          # Generated PNGs land here (gitignored)
└── README.md
```

Add this to `.gitignore`:
```
cache/
output/
__pycache__/
*.pyc
```

---

## How it works (FastF1 concepts)

```python
# 1. Enable cache — avoids re-downloading on every run
fastf1.Cache.enable_cache('cache')

# 2. Load a session
session = fastf1.get_session(2024, 'Bahrain', 'Q')
session.load()

# 3. Access laps as a pandas DataFrame
laps = session.laps

# 4. Filter to clean laps only (removes in/out laps, safety car laps)
clean = laps.pick_quicklaps()

# 5. Get each driver's best lap
best = clean.groupby('Driver').apply(lambda x: x.sort_values('LapTime').iloc[0])

# 6. Sector times are timedeltas — convert to float seconds for plotting
best['S1'] = best['Sector1Time'].dt.total_seconds()
```

Key columns in the `laps` DataFrame: `Driver`, `Team`, `LapTime`, `Sector1Time`, `Sector2Time`, `Sector3Time`, `Compound`, `TyreLife`, `IsPersonalBest`.

---

## First run note

The first time you run a session, FastF1 downloads data from Ergast and the official F1 timing feed. This can take 30–60 seconds depending on your connection. Subsequent runs for the same session load from cache in under 2 seconds.

---

## Ideas to extend this project

- Add telemetry overlays (speed trace comparison between two drivers)
- Plot lap-by-lap tyre degradation across a race
- Build a mini web dashboard with Streamlit
- Add corner-by-corner mini-sector analysis using telemetry distance data

---

## Data source

All data is fetched via the [FastF1](https://github.com/theOehrly/Fast-F1) library, which sources from the official Ergast Motor Racing API and Formula 1's timing feed. Data is for personal/educational use.

---

## Licence

MIT
