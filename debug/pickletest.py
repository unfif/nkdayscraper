# %%
import pandas as pd

jockeys = pd.read_pickle('jockeys.pkl')

for targetcol in ['単勝率', '連対率', '複勝率']:
    for place in set(jockeys.index.get_level_values(0)):
        tmprank = jockeys.loc[place, targetcol].rank(method='dense', ascending=False, na_option='bottom')
        tmprank.index = pd.MultiIndex.from_product([(place, ), tmprank.index])
        jockeys.loc[place, targetcol + '順'] = tmprank

    jockeys[targetcol + '順'] = jockeys[targetcol + '順'].astype(int)

pass

# %%
