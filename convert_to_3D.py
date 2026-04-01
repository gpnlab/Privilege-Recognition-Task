import numpy as np
import glob
import os
import pandas as pd

COLUMNS = [
    'tick', 'coins_left',
    'player_coins', 'e1_coins', 'e2_coins', 'e3_coins',
    'player_x', 'player_y',
    'enemy1_x', 'enemy1_y',
    'enemy2_x', 'enemy2_y',
    'enemy3_x', 'enemy3_y',
]

files = sorted(glob.glob(os.path.expanduser('~/Desktop/logs/*/*/*.npz')))
print(f"Found {len(files)} participants")

participants = []
arrays = []
for f in files:
    d = np.load(f, allow_pickle=True)
    arrays.append(d['ticks'])
    participants.append({
        'ticks': d['ticks'],
        'coins': d['coins'],
        'coin_round_keys': list(d['coin_round_keys']),
        'participant_id': d['participant_id'][0],
        'date': d['date'][0],
        'columns': list(d['columns']),
    })

# need to pad everything to the same shape
max_rounds = max(a.shape[0] for a in arrays)
max_ticks  = max(a.shape[1] for a in arrays)
n_cols     = arrays[0].shape[2]

# build numpy array with all PATs data
final = np.full((len(arrays), max_rounds, max_ticks, n_cols), np.nan)
for i, a in enumerate(arrays):
    final[i, :a.shape[0], :a.shape[1], :] = a

print(f"Full array shape: {final.shape}")

# rounds vary a little bit so need to find last true tick
last_ticks = np.full((len(arrays), max_rounds, n_cols), np.nan)
for p in range(final.shape[0]):
    for r in range(final.shape[1]):
        row = final[p, r, :, :]
        real = row[~np.isnan(row[:, 0])]
        if len(real) > 0:
            last_ticks[p, r, :] = real[-1]


df = pd.DataFrame(
    np.nanmean(final[:, :, :, COLUMNS.index('player_coins')], axis=2),
    columns=['round_0', 'round_1', 'round_2']
)
df.index = [p['participant_id'] for p in participants]
print(df)

print(pd.Series({
    'enemy1': np.nanmean(final[:, :, :, COLUMNS.index('e1_coins')]),
    'enemy2': np.nanmean(final[:, :, :, COLUMNS.index('e2_coins')]),
    'enemy3': np.nanmean(final[:, :, :, COLUMNS.index('e3_coins')]),
}))

p0 = participants[0]
idx = p0['coin_round_keys'].index('level 1 round 0')
print(len(p0['coins'][idx]))

numpy_save_path = os.path.expanduser('~/Desktop/logs/all_pats_numpy_data.npz')
np.savez(
    numpy_save_path,
    final=final,
    last_ticks=last_ticks,
    participant_ids=np.array([p['participant_id'] for p in participants]),
    columns=np.array(COLUMNS),
)
print(f"Saved combined data to {numpy_save_path}")

loaded = np.load(numpy_save_path, allow_pickle=True)
final_loaded       = loaded['final']
last_ticks_loaded  = loaded['last_ticks']
participant_ids = [str(p) for p in loaded['participant_ids']]

print(f"Reloaded shape: {final_loaded.shape}")
print(f"Participants: {participant_ids}")
print(f"Columns: {COLUMNS}")

# last tick of round 0 for every participant
print(pd.DataFrame(last_ticks[:, 0, :], columns=COLUMNS))
