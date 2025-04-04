from kinetics_modelling.config import PROCESSED_DATA_DIR
import polars as pl
import altair as alt
alt.data_transformers.enable("vegafusion")


q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run2_full')
    .head(100000)
    .select(
        'center_sm_1',
        'center_sx_1',
        'center_qual'
    )
    .with_columns(
        (pl.col('center_sm_1')/(pl.col('center_sx_1')+pl.col('center_sm_1'))).alias('sm_ratio'),
        (pl.col('center_qual').list.get(1)).alias('center_qual_1')
    )
)

df = q.collect()
print(df.head(10))

chart = alt.Chart(df).mark_circle(opacity=0.3).encode(
    alt.X('sm_ratio:Q'),
    alt.Y('center_qual_1:Q')
).properties(
    width=500,
    height=500,
    title='Quality ~ SM/(SM+SX)'
)

chart.save('./sm_sx_ratio_quality.svg')