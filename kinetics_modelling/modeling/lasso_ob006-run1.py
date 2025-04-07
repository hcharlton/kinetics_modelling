from kinetics_modelling.config import PROCESSED_DATA_DIR
from sklearn.linear_model import LassoCV 
import polars as pl
import altair as alt
alt.data_transformers.enable("vegafusion")


q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run1')
    .head(100000)
    .select(
        'center_qual', 
        'center_seq', 
        'fn', 
        'center_sx_0',
        'center_sx_1',
        'center_sx_2',
        'center_sm_0',
        'center_sm_1',
        'center_sm_2',
        'center_ipd_fwd_0', 
        'center_ipd_rev_0', 
        'center_pw_fwd_0',
        'center_pw_rev_0',
        'center_ipd_fwd_1', 
        'center_ipd_rev_1', 
        'center_pw_fwd_1',
        'center_pw_rev_1',
        'center_ipd_fwd_2', 
        'center_ipd_rev_2', 
        'center_pw_fwd_2',
        'center_pw_rev_2',
    )
    .with_columns(
        (pl.col('center_qual').list[0].alias('center_qual_0')),
        (pl.col('center_qual').list[1].alias('center_qual_1')),
        (pl.col('center_qual').list[2].alias('center_qual_2'))
    )
    .drop('center_qual')
    .group_by('center_qual_2')
    .agg(pl.all().head(1000))
    .explode(pl.exclude('center_qual_2'))
    )

df = q.collect()


from sklearn.model_selection import train_test_split
from sklearn import linear_model
features = [
    'fn', 
    'center_sx_0',
    'center_sx_1',
    'center_sx_2',
    'center_sm_0',
    'center_sm_1',
    'center_sm_2',
    'center_ipd_fwd_0', 
    'center_ipd_rev_0', 
    'center_pw_fwd_0',
    'center_pw_rev_0',
    'center_ipd_fwd_1', 
    'center_ipd_rev_1', 
    'center_pw_fwd_1',
    'center_pw_rev_1',
    'center_ipd_fwd_2', 
    'center_ipd_rev_2', 
    'center_pw_fwd_2',
    'center_pw_rev_2'
    ]

# X = df.select(
#     'fn', 
#     'center_sx_0',
#     'center_sx_1',
#     'center_sx_2',
#     'center_sm_0',
#     'center_sm_1',
#     'center_sm_2',
#     'center_ipd_fwd_0', 
#     'center_ipd_rev_0', 
#     'center_pw_fwd_0',
#     'center_pw_rev_0',
#     'center_ipd_fwd_1', 
#     'center_ipd_rev_1', 
#     'center_pw_fwd_1',
#     'center_pw_rev_1',
#     'center_ipd_fwd_2', 
#     'center_ipd_rev_2', 
#     'center_pw_fwd_2',
#     'center_pw_rev_2')

X = df.select(
    features
).to_numpy()
y = df.select('center_qual_2').to_numpy().reshape(-1,)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1337)

reg = LassoCV(cv=5, random_state=0).fit(X_train, y_train)

print(list(zip(reg.coef_, features)))