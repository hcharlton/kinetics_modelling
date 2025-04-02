from kinetics_modelling.config import PROCESSED_DATA_DIR
import polars as pl
import altair as alt
alt.data_transformers.enable("vegafusion")

q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run1')
    .select(
        'center_qual', 
        'center_seq', 
        'fn', 
        # 'center_sx_0',
        # 'center_sx_1',
        # 'center_sx_2',
        # 'center_sm_0',
        # 'center_sm_1',
        # 'center_sm_2',
        # 'center_ipd_fwd_0', 
        # 'center_ipd_rev_0', 
        # 'center_pw_fwd_0',
        # 'center_pw_rev_0',
        'center_ipd_fwd_1', 
        # 'center_ipd_rev_1', 
        # 'center_pw_fwd_1',
        # 'center_pw_rev_1',
        # 'center_ipd_fwd_2', 
        # 'center_ipd_rev_2', 
        # 'center_pw_fwd_2',
        # 'center_pw_rev_2',)
    )
    .filter(pl.col('center_qual') == [93,93,93])
    .group_by('fn','center_seq')
    .agg(pl.col('center_ipd_fwd_1').mean().alias('ipd_mean'), pl.len())
    # .unpivot(index='fn')
)

df = q.collect()
print(df.head())

chart = alt.Chart(df).mark_line().encode(
    alt.X('fn'),
    alt.Y('ipd_mean'),
    alt.Color('center_seq')
).properties(
    title ='Kinetics Mean ~ Passes',
    width = 500,
    height = 500
).facet(
    facet=alt.Facet('center_seq:N'),
    columns = 12
)
chart.save('./fn-ipd_mean.svg')
