"""
data.py: all FastF1 session loading and lap data extraction.
This is where you interact with the FastF1 library directly.
"""

import fastf1
import fastf1.plotting
import pandas as pd

# Enable cache once, at import time — applies for the whole program run
fastf1.Cache.enable_cache('cache')
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False)


def load_session(year: int, gp: str, session_type: str):
    """
    Load and return a FastF1 session object.

    Args:
        year:         Championship season, e.g. 2024
        gp:           Grand Prix name, e.g. 'Bahrain', 'Monaco', 'Silverstone'
        session_type: 'Q', 'R', 'FP1', 'FP2', 'FP3', 'S', 'SQ'

    Returns:
        fastf1.core.Session — fully loaded, ready to query
    """
    session = fastf1.get_session(year, gp, session_type)
    session.load(telemetry=False, weather=False)
    return session


def best_laps(session) -> pd.DataFrame:
    """
    Extract each driver's best lap from a session.

    pick_quicklaps() filters out:
      - In-laps and out-laps
      - Laps with deleted times (track limits)
      - Laps under safety car / VSC

    Returns a DataFrame with one row per driver, sector times in seconds.
    """
    laps = session.laps.pick_quicklaps()

    # Group by driver, sort by LapTime, take the fastest
    best = (
        laps.groupby('Driver')
        .apply(lambda x: x.sort_values('LapTime').iloc[0])
        .reset_index(drop=True)
    )

    # Convert timedelta → float seconds for maths and plotting
    for col in ['Sector1Time', 'Sector2Time', 'Sector3Time', 'LapTime']:
        best[f'{col}Sec'] = best[col].dt.total_seconds()

    return best[['Driver', 'Team',
                 'Sector1TimeSec', 'Sector2TimeSec',
                 'Sector3TimeSec', 'LapTimeSec']].dropna().reset_index(drop=True)


def driver_color(driver: str, session) -> str:
    """
    Return the official hex colour for a driver's team.
    Falls back to neutral grey if FastF1 doesn't recognise the driver code.
    """
    try:
        return fastf1.plotting.driver_color(driver)
    except Exception:
        return '#888888'