from kinetics_modelling.config import PROCESSED_DATA_DIR
import polars as pl
import altair as alt
import numpy as np

alt.data_transformers.enable("vegafusion")

breaks = np.arange(0, 1.05, 0.05)

###### This works but I'm suspiciuos of the logic 
q1 = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run2_full')
    .select(
        'center_sm_1',
        'center_sx_1',
        'center_qual'
    )
    .with_columns(
        (pl.col('center_sm_1')/(pl.col('center_sx_1')+pl.col('center_sm_1'))).alias('sm_ratio'),
        (pl.col('center_qual').list.get(1)).alias('center_qual_1')
    )
    .with_columns(
        pl.col('sm_ratio').round(1).alias('sm_ratio_bin')
    )
    .group_by('sm_ratio_bin')
    .agg(((pl.col('center_qual_1') >= 90).sum()/pl.col('center_qual_1').len()).alias('percentGEQ90'))
)


q2 = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run2_full')
    .select(
        'center_sm_1',
        'center_sx_1',
        'center_qual'
    )
    .with_columns(
        (pl.col('center_sm_1')/(pl.col('center_sx_1')+pl.col('center_sm_1'))).alias('sm_ratio'),
        (pl.col('center_qual').list.get(1)).alias('center_qual_1')
    )
    .with_columns(
        pl.col('sm_ratio').round(1).alias('sm_ratio_bin')
    )
    .group_by('sm_ratio_bin')
    .agg(((pl.col('center_qual_1') >= 90).sum()/pl.col('center_qual_1').len()).alias('percentGEQ90'))
)


df = q2.collect()
print(df.shape, df.head(10),breaks)

chart = alt.Chart(df).mark_line(opacity=0.5).encode(
    alt.X('sm_ratio_bin:Q'),
    alt.Y('percentGEQ90:Q')
).properties(
    width=500,
    height=500,
    title='percentGEQ90 ~ Bin(SM/(SM+SX))'
)

chart.save('./sm_sx_ratio_quality.svg')