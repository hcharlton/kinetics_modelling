
from kinetics_modelling.config import PROCESSED_DATA_DIR
import polars as pl
import altair as alt
alt.data_transformers.enable("vegafusion")


q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run0')
    .select('center_qual', 'fn')
    .with_columns(
        (pl.col('center_qual').list[0].alias('center_qual_0')),
        (pl.col('center_qual').list[1].alias('center_qual_1')),
        (pl.col('center_qual').list[2].alias('center_qual_2')))
    .group_by('fn')
    .agg(pl.col('center_qual_1').var().alias('center_qual_1_var'),
         pl.col('center_qual_1').mean().alias('center_qual_1_mean'),
         (pl.col('center_qual_1').var().sqrt() / pl.col('center_qual_1').count().sqrt()).alias('se'))
    .unpivot(index = 'fn')
    )

df = q.collect()

dynamics_chart = alt.Chart(df).mark_circle().encode(
    alt.X('fn:Q').title('Passes'),
    alt.Y('center_qual_1_mean:Q').title('Quality at Locus'),
).properties(title='Mean Quality by Passes')


dynamics_chart.save('./qualityVar-fn-ob006-run0.svg')

