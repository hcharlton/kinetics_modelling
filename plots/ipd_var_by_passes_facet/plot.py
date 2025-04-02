from kinetics_modelling.config import PROCESSED_DATA_DIR
import polars as pl
import altair as alt
alt.data_transformers.enable("vegafusion")

q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run2_full')
    .select(
        'center_qual', 
        'center_seq', 
        'fn', 
        'center_ipd_fwd_1', 
        'center_ipd_rev_1',
        'center_pw_rev_1',
        'center_pw_fwd_1'
    )
    .filter((pl.col('center_qual') == [93,93,93]) & (pl.col('fn') < 15))
    .group_by('center_seq')
    .agg(pl.all().head(1000))
    .explode(pl.exclude('center_seq'))
    .group_by('fn','center_seq')
    .agg(
        pl.col('center_ipd_fwd_1').std().alias('ipd_fwd_var'),
        pl.col('center_ipd_rev_1').std().alias('ipd_rev_var'), 
        pl.col('center_pw_fwd_1').std().alias('pw_fwd_var'), 
        pl.col('center_pw_rev_1').std().alias('pw_rev_var'),
        # pl.len().alias('count')
        )
    .unpivot(index = ['fn', 'center_seq'])
)

df = q.collect()
# print(df.filter(pl.col('variable') == 'count').min())

kinetics_chart = alt.Chart(df.filter(pl.col('variable')!='count')).mark_line().encode(
    alt.X('fn'),
    alt.Y('value'),
    alt.Color('variable')
).properties(
    title ='Kinetics Var ~ Passes',
    width = 500,
    height = 500
).facet(
    facet=alt.Facet('center_seq:N'),
    columns = 11
)

kinetics_chart.save('./fn-ipd_var_3mer_facet.svg')


