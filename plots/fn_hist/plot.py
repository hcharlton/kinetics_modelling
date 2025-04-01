from kinetics_modelling.config import PROCESSED_DATA_DIR
import polars as pl
import altair as alt
alt.data_transformers.enable("vegafusion")

q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run0')
    .select('fn','center_qual')
)

df = q.collect()

alt.Chart(df).mark_bar().encode(
    alt.X('fn'),
    alt.Y('count()')
).save('./fn_hist_all.svg')