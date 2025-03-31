
from kinetics_modelling.config import load_config, PROCESSED_DATA_DIR
import polars as pl
import altair as alt
alt.data_transformers.enable("vegafusion")

df = pl.read_parquet(PROCESSED_DATA_DIR / 'sample_bam_null')#.filter(pl.col('center_qual')==[93,93,93])


df = df.with_columns(
    (pl.col('center_qual').list[0].alias('center_qual_0')),
    (pl.col('center_qual').list[1].alias('center_qual_1')),
    (pl.col('center_qual').list[2].alias('center_qual_2'))
)


df_passes_group = df.group_by('fn').agg(
    pl.col('center_qual_1').var().alias('center_qual_1_var'),
    pl.col('center_qual_1').mean().alias('center_qual_1_mean')
    )


chart_fn_variance = alt.Chart(df_passes_group).mark_circle().encode(
    alt.X('fn:Q'),
    alt.Y('center_qual_1_mean:Q')
)

chart_fn_variance.save('qualityVar-fn.svg')