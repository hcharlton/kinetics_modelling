from kinetics_modelling.config import PROCESSED_DATA_DIR
import polars as pl
import altair as alt
alt.data_transformers.enable("vegafusion")

q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run2_full')
    .select(
        'fn',
        'center_seq',
    )
    .group_by(['fn','center_seq'])
    .agg(pl.len().alias('count'))
)

df = q.collect()
print(df.head())

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
)
kinetics_chart.save('./fn_count_by_3mer.svg')


