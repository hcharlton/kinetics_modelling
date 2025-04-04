from kinetics_modelling.config import PROCESSED_DATA_DIR
import polars as pl
import altair as alt
alt.data_transformers.enable("vegafusion")


q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run2_full')
    .select(
        'center_qual', 
        'center_seq', 
        'fn', 
    )
    .filter((pl.col('fn')>14) & (pl.col('center_qual').list.get(1) == 93))
    .group_by(['center_seq', 'fn'])
    .agg(pl.len().alias('count'))
)

df = q.collect()

kinetics_chart = alt.Chart(df).mark_bar().encode(
    alt.X('fn'),
    alt.Y('count'),
).properties(
    title ='Instances by FN for each 3mer',
    width = 500,
    height = 500
).facet(
    facet=alt.Facet('center_seq:N'),
    columns = 11
).resolve_scale(
    x='independent',
    y='independent'
)

kinetics_chart.save('./fn_count_by_3mer_g14_q93.svg')


