from kinetics_modelling.config import PROCESSED_DATA_DIR
import polars as pl
import altair as alt
alt.data_transformers.enable("vegafusion")

q = (
    pl.scan_parquet(PROCESSED_DATA_DIR / 'ob006-run2_full')
    # .head(1000)
    .select(
        'center_qual', 
        'fn', 
        'center_ipd_fwd_1', 
        'center_ipd_rev_1',
        'center_pw_rev_1',
        'center_pw_fwd_1'
    )
    .filter((pl.col('center_qual') == [93,93,93]) & (pl.col('fn') < 25))
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
)

df = q.collect()
# print(df.head())
# print(df.filter(pl.col('variable') == 'count').min())

sd_chart = alt.Chart(df.filter(~pl.col('variable').str.ends_with('mean'))).mark_line().encode(
    alt.X('fn').title('Forward Passes'),
    alt.Y('value').title('StDev'),
    alt.Color('variable')
).properties(
    width = 500,
    height = 500,
)

mean_chart = alt.Chart(df.filter(~pl.col('variable').str.ends_with('stdev'))).mark_line(strokeDash=[4,2]).encode(
    alt.X('fn'),
    alt.Y('value').title('Mean'),
    alt.Color('variable')
).properties(
    width = 500,
    height = 500,
)

final_chart = alt.layer(sd_chart, mean_chart).resolve_scale(
    y='independent'
).properties(
    title ='Kinetics StDev & Mean ~ Passes',
).configure_title(
    fontSize=25,
    anchor = 'middle'
)

final_chart.save('./ipd_meanANDsd_by_fn.svg')


