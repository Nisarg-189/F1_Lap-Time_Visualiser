"""
utils.py: shared helper functions used across the project.
"""

import pandas as pd


def timedelta_to_seconds(td) -> float:
    """
    Convert a pandas Timedelta to float seconds.
    Returns None if the value is NaT or None.

    Example:
        td = pd.Timedelta('0 days 00:01:28.432000')
        timedelta_to_seconds(td)  # → 88.432
    """
    if pd.isna(td):
        return None
    return td.total_seconds()


def format_laptime(seconds: float) -> str:
    """
    Convert float seconds to m:ss.mmm display format.

    Example:
        format_laptime(88.432)  # → '1:28.432'
    """
    if seconds is None:
        return 'N/A'
    minutes = int(seconds // 60)
    secs    = seconds % 60
    return f'{minutes}:{secs:06.3f}'


def print_summary(df, session) -> None:
    """
    Print a formatted results table to the terminal.
    Useful as a sanity check before opening the charts.
    """
    event = f"{session.event.year} {session.event['EventName']}"
    print(f'  {"─" * 52}')
    print(f'  {event}')
    print(f'  {"─" * 52}')
    print(f'  {"Pos":<4} {"Driver":<6} {"S1":>8} {"S2":>8} {"S3":>8} {"Lap":>10}')
    print(f'  {"─" * 52}')

    df_sorted = df.sort_values('LapTimeSec').reset_index(drop=True)
    for i, row in df_sorted.iterrows():
        print(f'  {i+1:<4} {row["Driver"]:<6} '
              f'{format_laptime(row["Sector1TimeSec"]):>8} '
              f'{format_laptime(row["Sector2TimeSec"]):>8} '
              f'{format_laptime(row["Sector3TimeSec"]):>8} '
              f'{format_laptime(row["LapTimeSec"]):>10}')
    print(f'  {"─" * 52}\n')