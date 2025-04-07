import polars as pl
import altair as alt
from kinetics_modelling.config import PROCESSED_DATA_DIR
alt.data_transformers.enable('vegafusion')

q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run2_full')
    # .head(100000000)
    .select(
        'center_sx_1',
        'center_sm_1',
        'center_qual'
    )
    .filter((pl.col('center_sx_1')<7) &
            (pl.col('center_sm_1').is_between(1,16)))
    .with_columns(
        (pl.col('center_qual').list.get(1)).alias('qual'),
        pl.col('center_sx_1').alias('sx'),
        pl.col('center_sm_1').alias('sm')
    )
    .group_by('sx', 'sm')
    .agg(((pl.col('qual') >= 90).sum()/pl.col('qual').len()).alias('percentGEQ90'))
)



df = q.collect()

print(df.head())

chart = alt.Chart(df).mark_line(opacity=0.4).encode(
    alt.X('sm:Q'),
    alt.Y('percentGEQ90:Q'),
    alt.Color('sx:N')

).properties(
    width=500,
    height=500,
    title='percentGEQ90 ~ SX, SM'
)

chart.save('./sx_grouped_sm_q90_percent_full.svg')
