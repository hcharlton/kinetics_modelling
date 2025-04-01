
from kinetics_modelling.config import load_config, PROCESSED_DATA_DIR
import polars as pl
import altair as alt
alt.data_transformers.enable("vegafusion")


q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'sample_bam_null')
    .select('center_qual', 'fn')
    .with_columns(
        (pl.col('center_qual').list[0].alias('center_qual_0')),
        (pl.col('center_qual').list[1].alias('center_qual_1')),
        (pl.col('center_qual').list[2].alias('center_qual_2')))
    .group_by('fn')
    .agg(pl.col('center_qual_1').var().alias('center_qual_1_var'),
         pl.col('center_qual_1').mean().alias('center_qual_1_mean'))
    )

df = q.collect()

alt.Chart(df).mark_circle().encode(
    alt.X('fn:Q'),
    alt.Y('center_qual_1_mean:Q')
).save('./qualityVar-fn.svg')

