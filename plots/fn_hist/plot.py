from kinetics_modelling.config import PROCESSED_DATA_DIR
import polars as pl
import altair as alt
alt.data_transformers.enable("vegafusion")

q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run2_full')
    .select('fn','center_qual')
)

df = q.collect()

alt.Chart(df).mark_bar().encode(
    alt.X('fn'),
    alt.Y('count()').scale(type="log")
).properties(
    width=500,
    height=500,
    title='FN Histogram (Log Scale)'
).save('./fn_hist_all_log.svg')