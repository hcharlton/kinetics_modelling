from kinetics_modelling.config import PROCESSED_DATA_DIR
import polars as pl
import altair as alt
alt.data_transformers.enable("vegafusion")

q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run1')
    .select(
        'center_qual', 
        'fn', 
        'center_ipd_fwd_1', 
    )
    .filter((pl.col('fn') < 21))
)

df = q.collect()
print(df.head())

kinetics_chart = alt.Chart(df).mark_bar().encode(
    alt.X('center_ipd_fwd_1:O').bin(maxbins=100),
    alt.Y('count()'),
).properties(
    title ='IPD Distributions ~ FN',
    width = 500,
    height = 500
).facet(
    facet=alt.Facet('fn'),
    columns = 5
).resolve_scale(
    y='independent'
)

kinetics_chart.save('./ipd_distributions_by_fn.svg')


