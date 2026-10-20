#!/usr/bin/env python3
"""Read-only validation for the public game-stats CSV before deployment."""

import csv
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / 'game-stats' / 'games.csv'
HTML_PATH = ROOT / 'game-stats' / 'index.html'
FIELDS = [
    'id', 'date', 'game', 'variant', 'winner', 'clock_type', 'base_seconds',
    'delay_seconds', 'side_mark', 'papa_drunk', 'count', 'source_entry', 'notes',
    'checkers_type', 'ending',
]
VARIANTS = {
    'checkers': {'breakthrough', 'standard'},
    'chess': {'three_check', 'standard'},
    'quoridouble': {'default'},
    'hexagon': {'default'},
}
CLOCKS = {'bd', 'sdel', 'hg', 'sd', 'nt'}


def check(condition, line, message):
    if not condition:
        raise ValueError(f'CSV line {line}: {message}')


def validate():
    if not HTML_PATH.is_file() or not HTML_PATH.stat().st_size:
        raise ValueError('game-stats/index.html is missing or empty')
    if not CSV_PATH.is_file() or not CSV_PATH.stat().st_size:
        raise ValueError('game-stats/games.csv is missing or empty')

    with CSV_PATH.open('r', encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError('CSV header does not match the existing dashboard schema')
        rows = list(reader)

    if not rows:
        raise ValueError('CSV has no game records')

    ids = set()
    totals = {'lekha': 0, 'papa': 0, 'draw': 0}
    for line, row in enumerate(rows, start=2):
        check(None not in row and all(value is not None for value in row.values()), line,
              'wrong number of fields')
        game, variant, winner = row['game'], row['variant'], row['winner']
        check(row['id'] != '' and row['id'] not in ids, line, 'missing or duplicate ID')
        ids.add(row['id'])
        check(re.fullmatch(r'\d{4}-\d{2}-\d{2}', row['date']) is not None, line,
              'date must use YYYY-MM-DD')
        try:
            date.fromisoformat(row['date'])
        except ValueError as exc:
            raise ValueError(f'CSV line {line}: invalid calendar date') from exc
        check(variant in VARIANTS.get(game, set()), line, 'unknown game or variant')
        check(row['checkers_type'] in ({'international', 'russian'} if game == 'checkers' else {''}),
              line, 'invalid checkers type')
        check(row['ending'] in {'', 'time'}, line, 'invalid ending marker')
        check(winner in totals, line, 'unknown winner')
        check(row['side_mark'] in {'', 'w', 'b', 'wb'}, line, 'invalid side mark')
        check(row['papa_drunk'] in {'true', 'false'}, line, 'invalid source flag')
        check(re.fullmatch(r'[1-9]\d*', row['count']) is not None, line,
              'count must be a positive integer')
        count = int(row['count'])
        check(count <= 2**53 - 1, line, 'count exceeds dashboard safe integer range')
        totals[winner] += count

        clock = row['clock_type']
        base, delay = row['base_seconds'], row['delay_seconds']
        check(clock in CLOCKS | {''}, line, 'unknown clock type')
        check(game == 'checkers' or clock == 'nt', line,
              'other games currently require nt (no timer support)')
        if clock in {'', 'nt'}:
            check(base == '' and delay == '', line, 'time provided for missing/no timer')
            check(not (clock == 'nt' and row['ending'] == 'time'), line,
                  'time expiry cannot occur without timer')
        else:
            check(re.fullmatch(r'[1-9]\d*', base) is not None and
                  int(base) <= 2**53 - 1, line, 'invalid base_seconds')
            if clock in {'bd', 'sdel'}:
                check(re.fullmatch(r'\d+', delay) is not None and
                      int(delay) <= 2**53 - 1, line, 'invalid delay_seconds')
            else:
                check(delay == '', line, 'delay must be blank for hg/sd')

    print(f'Valid CSV: {len(rows)} records, {sum(totals.values())} games; '
          f"Lekha {totals['lekha']}, Papa {totals['papa']}, Draw {totals['draw']}")


if __name__ == '__main__':
    validate()
