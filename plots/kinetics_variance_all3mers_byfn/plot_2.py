from kinetics_modelling.config import PROCESSED_DATA_DIR
import polars as pl
import altair as alt
alt.data_transformers.enable("vegafusion")

q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run2_full')
    # .head(10000)
    .select(
        'center_qual', 
        'fn', 
        'center_ipd_fwd_1', 
        'center_ipd_rev_1',
        'center_pw_rev_1',
        'center_pw_fwd_1'
    )
    .filter((pl.col('center_qual').list.get(1) == 93) & (pl.col('fn') < 31))
    .group_by('fn')
    .agg(
        pl.col('center_ipd_fwd_1').std().alias('ipd_fwd_stdev'),
        pl.col('center_ipd_rev_1').std().alias('ipd_rev_stdev'), 
        pl.col('center_pw_fwd_1').std().alias('pw_fwd_stdev'), 
        pl.col('center_pw_rev_1').std().alias('pw_rev_stdev'),
        pl.col('center_ipd_fwd_1').mean().alias('ipd_fwd_mean'),
        pl.col('center_ipd_rev_1').mean().alias('ipd_rev_mean'), 
        pl.col('center_pw_fwd_1').mean().alias('pw_fwd_mean'), 
        pl.col('center_pw_rev_1').mean().alias('pw_rev_mean'),
        )
    .unpivot(index = ['fn'])
    .with_columns([
    pl.col('variable').str.ends_with("mean").alias("mean"),
    pl.col("variable")
        .str.replace("_mean", "")
        .str.replace("_stdev", "")
        .alias("variable")
])
)

df = q.collect()
print(df.head(10))


chart= alt.Chart(df).mark_line().encode(
    alt.X('fn').title('Forward Passes'),
    alt.Y('value'),
    alt.Color('variable'),
    alt.StrokeDash('mean:N', scale=alt.Scale(domain=[False, True], range=[[5, 5], []]))
).properties(
    width = 500,
    height = 500,
    title = 'Kinetics StDev & Mean ~ Passes (Q93)',
).configure_title(
    fontSize = 25,
    anchor = 'middle'
)


chart.save('./ipd_mean_and_sd_by_fn_30_q93.svg')


