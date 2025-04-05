from kinetics_modelling.config import PROCESSED_DATA_DIR
import polars as pl
import altair as alt
import numpy as np

alt.data_transformers.enable("vegafusion")


q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run2_full')
    .select(
        'center_sm_1',
        'center_sx_1',
    )
)


df = q.collect()
print(df.head())

sx_hist = alt.Chart(df).mark_bar().encode(
    alt.X('center_sx_1:Q').scale(domain=[0,20]),
    alt.Y('count():Q'),
).properties(
    width=500,
    height=500,
    title='SX Distribution ob006'
)

sm_hist = alt.Chart(df).mark_bar().encode(
    alt.X('center_sm_1:Q').scale(domain=[0,40]),
    alt.Y('count():Q'),
).properties(
    width=500,
    height=500,
    title='SM Distribution ob006'
)

final_chart = sm_hist | sx_hist

final_chart.save('./sm_sx_hist_concat.svg')

