"""
visualiser.py: generates and saves the three core charts.
Each function takes a processed DataFrame, the session object, and an output path.
"""

import os
import matplotlib.pyplot as plt
import numpy as np
from data import driver_color


def _dark_axes(ax):
    """Apply consistent dark theme to a single Axes object."""
    ax.set_facecolor('#1a1a1a')
    ax.spines[:].set_visible(False)
    ax.tick_params(colors='white')
    ax.xaxis.set_tick_params(labelcolor='white')
    ax.yaxis.set_tick_params(labelcolor='white')


def _event_label(session) -> str:
    """Return a human-readable event title, e.g. '2024 Bahrain Grand Prix'."""
    return f"{session.event.year} {session.event['EventName']}"


def plot_sector_bars(df, session, output_dir: str):
    """
    Three side-by-side bar charts — one per sector.
    Gold star marks the fastest driver in each sector.
    """
    drivers = df['Driver'].tolist()
    colors  = [driver_color(d, session) for d in drivers]
    x       = np.arange(len(drivers))

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.patch.set_facecolor('#0f0f0f')

    for ax, col, num in zip(axes,
                            ['Sector1TimeSec', 'Sector2TimeSec', 'Sector3TimeSec'],
                            [1, 2, 3]):
        bars = ax.bar(x, df[col], color=colors, edgecolor='none', width=0.65)
        _dark_axes(ax)

        ax.set_xticks(x)
        ax.set_xticklabels(drivers, rotation=45, ha='right', fontsize=9, color='white')
        ax.set_title(f'Sector {num}', color='white', fontsize=13, pad=10)
        ax.set_ylabel('Time (s)', color='#aaaaaa', fontsize=10)

        # Highlight sector fastest with gold border and star
        min_idx = df[col].idxmin()
        bars[min_idx].set_edgecolor('gold')
        bars[min_idx].set_linewidth(2)
        ax.annotate('★',
                    xy=(min_idx, df[col].iloc[min_idx]),
                    ha='center', va='bottom',
                    color='gold', fontsize=12)

    fig.suptitle(f'{_event_label(session)} — Sector Times',
                 color='white', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()

    path = os.path.join(output_dir, 'sector_bars.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'  Saved → {path}')


def plot_lap_times(df, session, output_dir: str):
    """
    Horizontal bar chart of full lap times, sorted fastest → slowest.
    Delta to pole annotated on the right of each bar.
    """
    df_sorted    = df.sort_values('LapTimeSec').reset_index(drop=True)
    drivers      = df_sorted['Driver'].tolist()
    colors       = [driver_color(d, session) for d in drivers]
    fastest_time = df_sorted['LapTimeSec'].min()

    fig, ax = plt.subplots(figsize=(10, 0.55 * len(drivers) + 2))
    fig.patch.set_facecolor('#0f0f0f')
    _dark_axes(ax)

    bars = ax.barh(drivers, df_sorted['LapTimeSec'],
                   color=colors, edgecolor='none', height=0.65)

    for bar, t in zip(bars, df_sorted['LapTimeSec']):
        delta = t - fastest_time
        label = 'POLE' if delta == 0 else f'+{delta:.3f}s'
        color = 'gold' if delta == 0 else '#cccccc'
        ax.text(bar.get_width() + 0.05,
                bar.get_y() + bar.get_height() / 2,
                label, va='center', ha='left', fontsize=9, color=color)

    ax.invert_yaxis()
    ax.set_xlabel('Lap Time (s)', color='#aaaaaa')
    ax.set_title(f'{_event_label(session)} — Qualifying Lap Times',
                 color='white', fontsize=14, fontweight='bold', pad=14)

    plt.tight_layout()
    path = os.path.join(output_dir, 'lap_times.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'  Saved → {path}')


def plot_sector_deltas(df, session, output_dir: str):
    """
    Three stacked horizontal bar charts — delta to fastest per sector.
    Gold dashed line at x=0 is the benchmark (sector fastest).
    """
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    fig.patch.set_facecolor('#0f0f0f')

    for ax, col, num in zip(axes,
                            ['Sector1TimeSec', 'Sector2TimeSec', 'Sector3TimeSec'],
                            [1, 2, 3]):
        df_s    = df.sort_values(col).copy()
        fastest = df_s[col].min()
        df_s['delta'] = df_s[col] - fastest
        drivers = df_s['Driver'].tolist()
        colors  = [driver_color(d, session) for d in drivers]

        _dark_axes(ax)
        ax.barh(drivers, df_s['delta'], color=colors, edgecolor='none', height=0.65)
        ax.axvline(0, color='gold', linewidth=1, linestyle='--')
        ax.set_xlabel('Delta to fastest (s)', color='#aaaaaa', fontsize=9)
        ax.set_title(f'Sector {num} — delta to fastest',
                     color='white', fontsize=11)

    fig.suptitle(f'{_event_label(session)} — Sector Deltas',
                 color='white', fontsize=14, fontweight='bold')
    plt.tight_layout()

    path = os.path.join(output_dir, 'sector_deltas.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'  Saved → {path}')