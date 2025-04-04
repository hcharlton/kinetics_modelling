from kinetics_modelling.config import PROCESSED_DATA_DIR
import polars as pl
import altair as alt
alt.data_transformers.enable("vegafusion")

q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run2_full')
    # .head(1000)
    .select(
        'center_qual', 
        'center_seq', 
        'fn', 
        'center_ipd_fwd_1', 
        'center_ipd_rev_1',
        'center_pw_rev_1',
        'center_pw_fwd_1'
    )
    .filter((pl.col('center_qual').list.get(1) == 93) & (pl.col('fn') < 31))
    # .group_by('center_seq')
    # .explode(pl.exclude('center_seq'))
    .group_by('fn','center_seq')
    .agg(
        pl.col('center_ipd_fwd_1').std().alias('ipd_fwd_var'),
        pl.col('center_ipd_rev_1').std().alias('ipd_rev_var'), 
        pl.col('center_pw_fwd_1').std().alias('pw_fwd_var'), 
        pl.col('center_pw_rev_1').std().alias('pw_rev_var'),
        )
    .unpivot(index = ['fn', 'center_seq'])
)

df = q.collect()
print(df.head())

kinetics_chart = alt.Chart(df).mark_line().encode(
    alt.X('fn').title('Forward Passes'),
    alt.Y('value').title('StDev'),
    alt.Color('variable')
).properties(
    width = 500,
    height = 500
).facet(
    facet=alt.Facet('center_seq:N'),
    columns = 11
).properties(
    title ='Kinetics Var ~ Passes',
).configure_title(
    fontSize=50,
    anchor = 'start'

)

kinetics_chart.save('./fn-ipd_var_3mer_facet.svg')


