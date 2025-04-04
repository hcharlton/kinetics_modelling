from kinetics_modelling.config import PROCESSED_DATA_DIR
import polars as pl
import altair as alt
alt.data_transformers.enable("vegafusion")

q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run2_full')
    .select('fn','center_qual', 'center_seq')
    .with_columns(
    (pl.col('center_qual').list[0].alias('center_qual_0')),
    (pl.col('center_qual').list[1].alias('center_qual_1')),
    (pl.col('center_qual').list[2].alias('center_qual_2')))
    .group_by('fn')
    .agg(((pl.col('center_qual_1') >= 90).sum()/pl.col('center_qual_1').count()).alias('percentGEQ90'))
)

df = q.collect()

chart = alt.Chart(df).mark_line().encode(
    alt.X('fn:Q'),
    alt.Y('percentGEQ90:Q')
).properties(
    title='Percent GEQ Q90 by Passes',
    width=500,
    height=500
)

chart.save('./percentGEQ90_fn.svg')