"""
f1-lap-lens: entry point
Run: python main.py
"""

import os
from data import load_session, best_laps
from visualiser import plot_sector_bars, plot_lap_times, plot_sector_deltas
from utils import print_summary


VALID_SESSIONS = {
    'Q':   'Qualifying',
    'R':   'Race',
    'FP1': 'Free Practice 1',
    'FP2': 'Free Practice 2',
    'FP3': 'Free Practice 3',
    'S':   'Sprint',
    'SQ':  'Sprint Qualifying',
}


def get_user_input():
    """Prompt the user for race details interactively."""

    print()
    print('=' * 45)
    print('       🏎️  F1 LAP LENS  ')
    print('=' * 45)

    # Year
    while True:
        year_input = input('\n  Enter season year (e.g. 2024): ').strip()
        if year_input.isdigit() and 2018 <= int(year_input) <= 2026:
            year = int(year_input)
            break
        print('  ⚠  Please enter a year between 2018 and 2026.')

    # Grand Prix name
    print()
    print('  Common GPs: Bahrain, Saudi Arabia, Australia, Japan,')
    print('              China, Miami, Monaco, Canada, Spain,')
    print('              Britain, Hungary, Belgium, Netherlands,')
    print('              Italy, Singapore, USA, Mexico, Brazil, Abu Dhabi')
    gp = input('\n  Enter Grand Prix name: ').strip()
    while not gp:
        gp = input('  ⚠  GP name cannot be empty. Try again: ').strip()

    # Session type
    print()
    print('  Sessions available:')
    for code, name in VALID_SESSIONS.items():
        print(f'    {code:<4} → {name}')
    while True:
        session_input = input('\n  Enter session code: ').strip().upper()
        if session_input in VALID_SESSIONS:
            session_type = session_input
            break
        print(f'  ⚠  Invalid session. Choose from: {", ".join(VALID_SESSIONS.keys())}')

    # Output folder
    default_out = f'output/{year}_{gp.replace(" ", "_")}_{session_type}'
    out = input(f'\n  Output folder [{default_out}]: ').strip()
    if not out:
        out = default_out

    return year, gp, session_type, out


def main():
    year, gp, session_type, out = get_user_input()

    os.makedirs(out, exist_ok=True)
    os.makedirs('cache', exist_ok=True)

    print()
    print(f'  Loading {year} {gp} GP — {VALID_SESSIONS[session_type]}...')
    print('  (first run may take 30–60s to download data)\n')

    try:
        session = load_session(year, gp, session_type)
    except Exception as e:
        print(f'\n  ❌ Could not load session: {e}')
        print('  Check the GP name spelling or try a different year/session.')
        return

    df = best_laps(session)

    if df.empty:
        print('  ❌ No valid lap data found for this session.')
        print('  Try Q or FP sessions — Race sessions have different lap structures.')
        return

    print(f'  ✅ Loaded {len(df)} drivers\n')
    print_summary(df, session)

    plot_sector_bars(df, session, out)
    plot_lap_times(df, session, out)
    plot_sector_deltas(df, session, out)

    print(f'\n  ✅ Done! Charts saved to → {out}/')
    print('=' * 45)


if __name__ == '__main__':
    main()