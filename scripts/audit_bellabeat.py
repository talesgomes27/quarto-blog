"""Audit the archived Bellabeat table; optionally compare the original Zenodo ZIP.

No network, R execution or participant-level output. Usage:
  python3 scripts/audit_bellabeat.py [--source-zip /tmp/bellabeat-source-2016.zip]
"""
import argparse
import collections
import csv
import hashlib
import io
import json
import math
import re
import statistics
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / '_freeze/posts/bellabeat/index/execute-results/html.json'
FIELDS = ('total_steps', 'total_distance', 'calories', 'heartrate', 'bmi',
          'total_time_asleep', 'sedentary_time')
SOURCE_URL = 'https://zenodo.org/records/53894/files/mturkfitbit_export_4.12.16-5.12.16.zip'
MD5 = '7afbecdce29814e1be2e9a7c94f8f165'


def number(value):
    return None if value in (None, '', 'NA') else float(value)


def summary(rows, field):
    usable = [r for r in rows if number(r.get(field)) is not None]
    values = [number(r[field]) for r in usable]
    return dict(observations=len(values), users=len({r['id'] for r in usable}),
                missing=len(rows)-len(values), mean=statistics.mean(values) if values else None,
                min=min(values) if values else None, max=max(values) if values else None)


def period(date):
    month, day, year = date.split()[0].split('/')
    return f'{year}-{int(month):02d}-{int(day):02d}'


def source_metrics(path, frozen_rows):
    raw = path.read_bytes()
    assert hashlib.md5(raw).hexdigest() == MD5, 'ZIP differs from the pinned Zenodo file'
    data = {}
    info = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        for basename in ('dailyActivity_merged.csv', 'sleepDay_merged.csv', 'weightLogInfo_merged.csv'):
            candidates = [name for name in archive.namelist() if name.endswith('/'+basename)]
            assert len(candidates) == 1, f'Expected one {basename}'
            with archive.open(candidates[0]) as stream:
                rows = list(csv.DictReader(io.TextIOWrapper(stream, encoding='utf-8-sig')))
            date_field = 'ActivityDate' if basename.startswith('daily') else 'SleepDay' if basename.startswith('sleep') else 'Date'
            days = [(r['Id'], period(r[date_field])) for r in rows]
            info[basename] = dict(rows=len(rows), users=len({r['Id'] for r in rows}),
                                 unique_user_days=len(set(days)), exact_duplicate_excess=len(rows)-len({tuple(r.items()) for r in rows}),
                                 first_date=min(d[1] for d in days), last_date=max(d[1] for d in days))
            data[basename] = rows
        candidates = [name for name in archive.namelist() if name.endswith('/heartrate_seconds_merged.csv')]
        assert len(candidates) == 1, 'Expected one heart-rate file'
        hr_sums, hr_n, hr_ids = collections.defaultdict(float), collections.Counter(), set()
        records = 0
        with archive.open(candidates[0]) as stream:
            for r in csv.DictReader(io.TextIOWrapper(stream, encoding='utf-8-sig')):
                key = (r['Id'], period(r['Time']))
                hr_sums[key] += float(r['Value'])
                hr_n[key] += 1
                hr_ids.add(r['Id'])
                records += 1
        heart = {key: hr_sums[key]/count for key,count in hr_n.items()}
        info['heartrate_seconds_merged.csv'] = dict(rows=records, users=len(hr_ids), unique_user_days=len(heart),
              first_date=min(key[1] for key in heart), last_date=max(key[1] for key in heart))
    activity = data['dailyActivity_merged.csv']
    ids = sorted({r['Id'] for r in activity}, key=int)
    names = {original:f'U{i+1}' for i,original in enumerate(ids)}
    sleep, weight = collections.defaultdict(list), collections.defaultdict(list)
    for r in data['sleepDay_merged.csv']: sleep[(r['Id'], period(r['SleepDay']))].append(r)
    for r in data['weightLogInfo_merged.csv']: weight[(r['Id'], period(r['Date']))].append(r)
    joined = []
    for a in activity:
        key=(a['Id'],period(a['ActivityDate']))
        for s in sleep.get(key,[{}]):
            for w in weight.get(key,[{}]):
                joined.append(dict(id=names[a['Id']], date=key[1],total_steps=float(a['TotalSteps']),
                  total_distance=float(a['TotalDistance']),calories=float(a['Calories']),heartrate=heart.get(key),
                  bmi=number(w.get('BMI')), total_time_asleep=number(s.get('TotalMinutesAsleep'))/60 if s else None,
                  sedentary_time=float(a['SedentaryMinutes'])/60))
    frozen_groups=collections.defaultdict(list)
    for r in frozen_rows: frozen_groups[(r['id'],r['date'])].append(r)
    assert collections.Counter((r['id'],r['date']) for r in joined) == collections.Counter(
        (r['id'],r['date']) for r in frozen_rows
    ), 'Reconstructed user-day multiplicities differ from the archive'
    mismatches=0
    for r in joined:
        candidates=frozen_groups.get((r['id'],r['date']),[])
        def equal(candidate):
            for field in FIELDS:
                x,y=number(r[field]),number(candidate[field])
                if x is None or y is None:
                    if x != y: return False
                elif not math.isclose(x,y,abs_tol=1e-5,rel_tol=0): return False
            return True
        if not any(equal(c) for c in candidates): mismatches+=1
    assert mismatches == 0, 'Reconstructed values differ from the archived fields'
    return dict(url=SOURCE_URL,md5=MD5,sha256=hashlib.sha256(raw).hexdigest(),file_size_bytes=len(raw),
                tables=info,reconstructed_left_join_rows=len(joined),
                reconstructed_rows_without_matching_archived_values=mismatches,
                comparison_fields=list(FIELDS),comparison_absolute_tolerance=1e-5,
                caveat='Upstream Zenodo archive; equality to the original local Kaggle download cannot be asserted.')


def audit(source_zip=None):
    raw=FROZEN.read_bytes()
    markdown=json.loads(raw)['result']['markdown']
    match=re.search(r'<script\b[^>]*data-pagedtable-source[^>]*>(.*?)</script>',markdown,re.S)
    assert match, 'Archived paged table not found'
    table=json.loads(match[1]); columns={str(c['name'][0]):c['label'][0] for c in table['columns']}
    rows=[{columns[key]:value for key,value in row.items()} for row in table['data']]
    assert all(field in rows[0] for field in FIELDS), 'Expected archived fields missing'
    counts=collections.Counter((r['id'],r['date']) for r in rows)
    unique=list({(r['id'],r['date']):r for r in rows}.values())
    # Exact duplicate equality matters: grouping by user-day must not discard distinct records silently.
    assert all(len({tuple(r.items()) for r in rows if (r['id'],r['date'])==key})==1 for key,n in counts.items() if n>1)
    result=dict(frozen_path=FROZEN.relative_to(ROOT).as_posix(),frozen_sha256=hashlib.sha256(raw).hexdigest(),
      rows=len(rows),unique_user_days=len(unique),users=len({r['id']for r in rows}),
      first_date=min(r['date']for r in rows),last_date=max(r['date']for r in rows),duplicate_excess=len(rows)-len(unique),
      archived_summary={f:summary(rows,f)for f in FIELDS},
      exact_user_day_deduplicated_sensitivity={f:summary(unique,f)for f in FIELDS},
      long_table_rows_implied_by_code=sum(n*n*4 for n in counts.values()),
      long_table_rows_if_one_row_per_user_day=len(unique)*4,
      caveat='Deduplication is a sensitivity check, not a correction applied to the published article.')
    result['sleep_groups']={}
    for label,condition in [('<6',lambda h:h<6),('6-10',lambda h:6<=h<=10),('>10',lambda h:h>10)]:
        group=[r for r in rows if number(r['total_time_asleep']) is not None and condition(number(r['total_time_asleep']))]
        result['sleep_groups'][label]=dict(observations=len(group),users=len({r['id']for r in group}),
          calories=summary(group,'calories'),heartrate=summary(group,'heartrate'))
    by_day=collections.defaultdict(list)
    for r in unique: by_day[r['day_of_the_week']].append(r)
    result['weekday_sensitivity']={day:dict(unique_user_days=len(rr),dates=len({r['date']for r in rr}),
        mean_distance_km=statistics.mean(number(r['total_distance'])for r in rr),
        mean_steps=statistics.mean(number(r['total_steps'])for r in rr))for day,rr in by_day.items()}
    bmi_per_person=collections.Counter(r['id']for r in rows if number(r['bmi']) is not None)
    result['bmi_observation_counts_per_person_sorted']=sorted(bmi_per_person.values(),reverse=True)
    if source_zip: result['upstream_source_check']=source_metrics(Path(source_zip),rows)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-zip',type=Path)
    parser.add_argument('--output',type=Path,default=ROOT/'docs/reviews/evidence/bellabeat-audit.json')
    args=parser.parse_args()
    result=audit(args.source_zip)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f'Audit saved: {args.output}; {result["rows"]} archived rows, {result["unique_user_days"]} unique user-days.')
