from kinetics_modelling.config import PROCESSED_DATA_DIR
import polars as pl
import altair as alt
alt.data_transformers.enable("vegafusion")

q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run0')
    .select('fn','center_qual')
    .with_columns(
        (pl.col('center_qual').list[0].alias('center_qual_0')),
        (pl.col('center_qual').list[1].alias('center_qual_1')),
        (pl.col('center_qual').list[2].alias('center_qual_2')))
    .filter(pl.col('fn')>15)
)

df = q.collect()

alt.Chart(df).mark_circle(opacity=0.4).encode(
    alt.X('fn:Q'),
    alt.Y('center_qual_1:Q')
).save('./fn_qual_g15_scatter.svg')