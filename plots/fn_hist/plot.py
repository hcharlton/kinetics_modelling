from kinetics_modelling.config import PROCESSED_DATA_DIR
import polars as pl
import altair as alt
alt.data_transformers.enable("vegafusion")

q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run2_full')
    .select('fn','center_qual')
    .filter(pl.col('fn')>14)
)

df = q.collect()

alt.Chart(df).mark_bar().encode(
    alt.X('fn'),
    alt.Y('count()')
).properties(
    width=500,
    height=500,
    title='FN Histogram (fn>14)'
).save('./fn_hist_g14.svg')