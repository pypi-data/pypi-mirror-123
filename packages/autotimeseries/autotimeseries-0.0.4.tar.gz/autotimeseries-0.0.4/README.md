# Time Series as a Service



```python
#! pip install autotimeseries
```

```python
import os
import time

import pandas as pd
from autotimeseries.core import AutoTS
from dotenv import load_dotenv

load_dotenv()
```




    True



```python
autotimeseries = AutoTS(bucket_name=os.environ['BUCKET_NAME'],
                        api_id=os.environ['API_ID'], 
                        api_key=os.environ['API_KEY'],
                        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], 
                        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
```

## M5 example

```python
filename_target = autotimeseries.upload_to_s3('../data/target.parquet')
filename_static = autotimeseries.upload_to_s3('../data/static.parquet')
filename_temporal = autotimeseries.upload_to_s3('../data/temporal.parquet')
filename_calendar_holidays = autotimeseries.upload_to_s3('../data/calendar-holidays.txt')
```

```python
print(filename_target, filename_static, filename_temporal, filename_calendar_holidays, sep='\n')
```

    target.parquet
    static.parquet
    temporal.parquet
    calendar-holidays.txt


Each time series of the uploaded datasets is defined by the column `item_id`. Meanwhile the time column is defined by `timestamp` and the target column by `demand`. We need to pass this arguments to each call.

```python
columns = dict(unique_id_column='item_id',
               ds_column='timestamp',
               y_column='demand')
```

## Computing calendar features

```python
response_calendar = autotimeseries.calendartsfeatures(filename=filename_temporal,
                                                      country='USA',
                                                      events=filename_calendar_holidays,
                                                      **columns)
```

```python
response_calendar
```




    {'id_job': '7781f21f-2d89-4709-b0f5-15ad26a74c44',
     'dest_url': 's3://nixtla-user-test/calendar-features.csv',
     'status': 200,
     'message': 'Check job status at GET /jobs/{job_id}'}



To check the status of your job use the method `get_status`:

```python
autotimeseries.get_status(response_calendar['id_job'])
```




    {'status': 'InProgress', 'processing_time_seconds': 1}



If you want to use the result of your job, you have to wait until its status is `Completed`.

```python
autotimeseries.check_progress_logs(response_calendar['id_job'])
```

    File written...
    Merging finished...
    Writing file...





    'Completed'



## Make forecasts

We will use the calendar features created by the previous process, so we pass `calendar-features.parquet` as `filename_temporal` argument.

```python
response_forecast = autotimeseries.tsforecast(filename_target=filename_target,
                                              freq='D',
                                              horizon=28, 
                                              filename_static=filename_static,
                                              filename_temporal='calendar-features.parquet',
                                              objective='tweedie',
                                              metric='rmse',
                                              n_estimators=170,
                                              **columns)
```

```python
response_forecast
```




    {'id_job': '08b5e4d2-293f-426d-98c4-0ef642a21a1f',
     'dest_url': 's3://nixtla-user-test/forecasts.csv',
     'status': 200,
     'message': 'Check job status at GET /jobs/{job_id}'}



```python
autotimeseries.get_status(response_forecast['id_job'])
```




    {'status': 'InProgress', 'processing_time_seconds': 0}



```python
autotimeseries.check_progress_logs(response_forecast['id_job'])
```

    Starting preprocessing
    Done
    Processing static features
    Reading file...
    File read.
    Done
    Starting preprocessing
    Done
    Done
    Processing temporal features
    Processing static features
    Reading file...
    File read.
    Starting training
    Done
    Starting preprocessing
    Done
    Done
    Processing temporal features
    Processing static features
    Reading file...
    File read.
    [140]#011train's rmse: 2.4413#011valid's rmse: 2.41412
    [100]#011train's rmse: 2.4601#011valid's rmse: 2.4318
    [60]#011train's rmse: 2.50007#011valid's rmse: 2.46812
    [40]#011train's rmse: 2.56329#011valid's rmse: 2.53034
    [20]#011train's rmse: 3.07992#011valid's rmse: 3.05776
    [LightGBM] [Warning] bagging_fraction is set=1.0, subsample=1.0 will be ignored. Current value: bagging_fraction=1.0
    [LightGBM] [Warning] min_data_in_leaf is set=20, min_child_samples=20 will be ignored. Current value: min_data_in_leaf=20
    [LightGBM] [Warning] bagging_freq is set=0, subsample_freq=0 will be ignored. Current value: bagging_freq=0
    Starting training
    Done
    Starting preprocessing
    Done
    Done
    Processing temporal features
    Processing static features
    Reading file...
    File read.
    Done
    [160]#011train's rmse: 2.43104#011valid's rmse: 2.40545
    [140]#011train's rmse: 2.4413#011valid's rmse: 2.41412
    [120]#011train's rmse: 2.45143#011valid's rmse: 2.4238
    [100]#011train's rmse: 2.4601#011valid's rmse: 2.4318
    [80]#011train's rmse: 2.47825#011valid's rmse: 2.44776
    [60]#011train's rmse: 2.50007#011valid's rmse: 2.46812
    [40]#011train's rmse: 2.56329#011valid's rmse: 2.53034
    [20]#011train's rmse: 3.07992#011valid's rmse: 3.05776
    [LightGBM] [Warning] bagging_fraction is set=1.0, subsample=1.0 will be ignored. Current value: bagging_fraction=1.0
    [LightGBM] [Warning] min_data_in_leaf is set=20, min_child_samples=20 will be ignored. Current value: min_data_in_leaf=20
    [LightGBM] [Warning] bagging_freq is set=0, subsample_freq=0 will be ignored. Current value: bagging_freq=0
    Starting training
    Done
    Starting preprocessing
    Done
    Done
    Processing temporal features
    Processing static features
    Reading file...
    File read.
    Done
    [160]#011train's rmse: 2.43104#011valid's rmse: 2.40545
    [140]#011train's rmse: 2.4413#011valid's rmse: 2.41412
    [120]#011train's rmse: 2.45143#011valid's rmse: 2.4238
    [100]#011train's rmse: 2.4601#011valid's rmse: 2.4318
    [80]#011train's rmse: 2.47825#011valid's rmse: 2.44776
    [60]#011train's rmse: 2.50007#011valid's rmse: 2.46812
    [40]#011train's rmse: 2.56329#011valid's rmse: 2.53034
    [20]#011train's rmse: 3.07992#011valid's rmse: 3.05776
    [LightGBM] [Warning] bagging_fraction is set=1.0, subsample=1.0 will be ignored. Current value: bagging_fraction=1.0
    [LightGBM] [Warning] min_data_in_leaf is set=20, min_child_samples=20 will be ignored. Current value: min_data_in_leaf=20
    [LightGBM] [Warning] bagging_freq is set=0, subsample_freq=0 will be ignored. Current value: bagging_freq=0
    Starting training
    Done
    Starting preprocessing
    Done
    Done
    Processing temporal features
    Processing static features
    Reading file...
    File read.
    Done
    [160]#011train's rmse: 2.43104#011valid's rmse: 2.40545
    [140]#011train's rmse: 2.4413#011valid's rmse: 2.41412
    [120]#011train's rmse: 2.45143#011valid's rmse: 2.4238
    [100]#011train's rmse: 2.4601#011valid's rmse: 2.4318
    [80]#011train's rmse: 2.47825#011valid's rmse: 2.44776
    [60]#011train's rmse: 2.50007#011valid's rmse: 2.46812
    [40]#011train's rmse: 2.56329#011valid's rmse: 2.53034
    [20]#011train's rmse: 3.07992#011valid's rmse: 3.05776
    [LightGBM] [Warning] bagging_fraction is set=1.0, subsample=1.0 will be ignored. Current value: bagging_fraction=1.0
    [LightGBM] [Warning] min_data_in_leaf is set=20, min_child_samples=20 will be ignored. Current value: min_data_in_leaf=20
    [LightGBM] [Warning] bagging_freq is set=0, subsample_freq=0 will be ignored. Current value: bagging_freq=0
    Starting training
    Done
    Starting preprocessing
    Done
    Done
    Processing temporal features
    Processing static features
    Reading file...
    File read.
    Done
    [160]#011train's rmse: 2.43104#011valid's rmse: 2.40545
    [140]#011train's rmse: 2.4413#011valid's rmse: 2.41412
    [120]#011train's rmse: 2.45143#011valid's rmse: 2.4238
    [100]#011train's rmse: 2.4601#011valid's rmse: 2.4318
    [80]#011train's rmse: 2.47825#011valid's rmse: 2.44776
    [60]#011train's rmse: 2.50007#011valid's rmse: 2.46812
    [40]#011train's rmse: 2.56329#011valid's rmse: 2.53034
    [20]#011train's rmse: 3.07992#011valid's rmse: 3.05776
    [LightGBM] [Warning] bagging_fraction is set=1.0, subsample=1.0 will be ignored. Current value: bagging_fraction=1.0
    [LightGBM] [Warning] min_data_in_leaf is set=20, min_child_samples=20 will be ignored. Current value: min_data_in_leaf=20
    [LightGBM] [Warning] bagging_freq is set=0, subsample_freq=0 will be ignored. Current value: bagging_freq=0
    Starting training
    Done
    Starting preprocessing
    Done
    Done
    Processing temporal features
    Processing static features
    Reading file...
    File read.
    Done
    [160]#011train's rmse: 2.43104#011valid's rmse: 2.40545
    [140]#011train's rmse: 2.4413#011valid's rmse: 2.41412
    [120]#011train's rmse: 2.45143#011valid's rmse: 2.4238
    [100]#011train's rmse: 2.4601#011valid's rmse: 2.4318
    [80]#011train's rmse: 2.47825#011valid's rmse: 2.44776
    [60]#011train's rmse: 2.50007#011valid's rmse: 2.46812
    [40]#011train's rmse: 2.56329#011valid's rmse: 2.53034
    [20]#011train's rmse: 3.07992#011valid's rmse: 3.05776
    [LightGBM] [Warning] bagging_fraction is set=1.0, subsample=1.0 will be ignored. Current value: bagging_fraction=1.0
    [LightGBM] [Warning] min_data_in_leaf is set=20, min_child_samples=20 will be ignored. Current value: min_data_in_leaf=20
    [LightGBM] [Warning] bagging_freq is set=0, subsample_freq=0 will be ignored. Current value: bagging_freq=0
    Starting training
    Done
    Starting preprocessing
    Done
    Done
    Processing temporal features
    Processing static features
    Reading file...
    File read.
    Done
    [160]#011train's rmse: 2.43104#011valid's rmse: 2.40545
    [140]#011train's rmse: 2.4413#011valid's rmse: 2.41412
    [120]#011train's rmse: 2.45143#011valid's rmse: 2.4238
    [100]#011train's rmse: 2.4601#011valid's rmse: 2.4318
    [80]#011train's rmse: 2.47825#011valid's rmse: 2.44776
    [60]#011train's rmse: 2.50007#011valid's rmse: 2.46812
    [40]#011train's rmse: 2.56329#011valid's rmse: 2.53034
    [20]#011train's rmse: 3.07992#011valid's rmse: 3.05776
    [LightGBM] [Warning] bagging_fraction is set=1.0, subsample=1.0 will be ignored. Current value: bagging_fraction=1.0
    [LightGBM] [Warning] min_data_in_leaf is set=20, min_child_samples=20 will be ignored. Current value: min_data_in_leaf=20
    [LightGBM] [Warning] bagging_freq is set=0, subsample_freq=0 will be ignored. Current value: bagging_freq=0
    Starting training
    Done
    Starting preprocessing
    Done
    Done
    Processing temporal features
    Processing static features
    Reading file...
    File read.
    Done
    [160]#011train's rmse: 2.43104#011valid's rmse: 2.40545
    [140]#011train's rmse: 2.4413#011valid's rmse: 2.41412
    [120]#011train's rmse: 2.45143#011valid's rmse: 2.4238
    [100]#011train's rmse: 2.4601#011valid's rmse: 2.4318
    [80]#011train's rmse: 2.47825#011valid's rmse: 2.44776
    [60]#011train's rmse: 2.50007#011valid's rmse: 2.46812
    [40]#011train's rmse: 2.56329#011valid's rmse: 2.53034
    [20]#011train's rmse: 3.07992#011valid's rmse: 3.05776
    [LightGBM] [Warning] bagging_fraction is set=1.0, subsample=1.0 will be ignored. Current value: bagging_fraction=1.0
    [LightGBM] [Warning] min_data_in_leaf is set=20, min_child_samples=20 will be ignored. Current value: min_data_in_leaf=20
    [LightGBM] [Warning] bagging_freq is set=0, subsample_freq=0 will be ignored. Current value: bagging_freq=0
    Starting training
    Done
    Starting preprocessing
    Done
    Done
    Processing temporal features
    Processing static features
    Reading file...
    File read.
    Done
    [160]#011train's rmse: 2.43104#011valid's rmse: 2.40545
    [140]#011train's rmse: 2.4413#011valid's rmse: 2.41412
    [120]#011train's rmse: 2.45143#011valid's rmse: 2.4238
    [100]#011train's rmse: 2.4601#011valid's rmse: 2.4318
    [80]#011train's rmse: 2.47825#011valid's rmse: 2.44776
    [60]#011train's rmse: 2.50007#011valid's rmse: 2.46812
    [40]#011train's rmse: 2.56329#011valid's rmse: 2.53034
    [20]#011train's rmse: 3.07992#011valid's rmse: 3.05776
    [LightGBM] [Warning] bagging_fraction is set=1.0, subsample=1.0 will be ignored. Current value: bagging_fraction=1.0
    [LightGBM] [Warning] min_data_in_leaf is set=20, min_child_samples=20 will be ignored. Current value: min_data_in_leaf=20
    [LightGBM] [Warning] bagging_freq is set=0, subsample_freq=0 will be ignored. Current value: bagging_freq=0
    Starting training
    Done
    Starting preprocessing
    Done
    Done
    Processing temporal features
    Processing static features
    Reading file...
    File read.
    Done
    [160]#011train's rmse: 2.43104#011valid's rmse: 2.40545
    [140]#011train's rmse: 2.4413#011valid's rmse: 2.41412
    [120]#011train's rmse: 2.45143#011valid's rmse: 2.4238
    [100]#011train's rmse: 2.4601#011valid's rmse: 2.4318
    [80]#011train's rmse: 2.47825#011valid's rmse: 2.44776
    [60]#011train's rmse: 2.50007#011valid's rmse: 2.46812
    [40]#011train's rmse: 2.56329#011valid's rmse: 2.53034
    [20]#011train's rmse: 3.07992#011valid's rmse: 3.05776
    [LightGBM] [Warning] bagging_fraction is set=1.0, subsample=1.0 will be ignored. Current value: bagging_fraction=1.0
    [LightGBM] [Warning] min_data_in_leaf is set=20, min_child_samples=20 will be ignored. Current value: min_data_in_leaf=20
    [LightGBM] [Warning] bagging_freq is set=0, subsample_freq=0 will be ignored. Current value: bagging_freq=0
    Starting training
    Done
    Starting preprocessing
    Done
    Done
    Processing temporal features
    Processing static features
    Reading file...
    File read.





    'Completed'



## Download forecasts from S3

```python
autotimeseries.download_from_s3(filename='forecasts.csv', filename_output='../data/forecasts.csv')
```

    [==================================================]

## Evaluate performance 

```python
response_benchmarks = autotimeseries.tsbenchmarks(filename='forecasts.csv',
                                                  dataset='M5')
```

```python
response_benchmarks
```




    {'id_job': 'fe3f76da-8bbe-45c8-b91b-c9a424449785',
     'dest_url': 's3://nixtla-user-test/benchmarks.csv',
     'status': 200,
     'message': 'Check job status at GET /jobs/{job_id}'}



```python
autotimeseries.get_status(response_benchmarks['id_job'])
```




    {'status': 'InProgress', 'processing_time_seconds': 0}



```python
autotimeseries.check_progress_logs(response_benchmarks['id_job'])
```

    Successfully decompressed data/m5/datasets/m5.zip
    Reading file...
    File readed.
    Computing metrics...
    Successfully downloaded m5.zip, 50219189, bytes.
    Decompressing zip file...





    'Completed'



### Download evaluation

### DataFrame results

```python
autotimeseries.download_from_s3(filename='benchmarks.csv', filename_output='../data/benchmarks.csv')
```

    [==================================================]

```python
pd.read_csv('../data/benchmarks.csv')
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>model</th>
      <th>WRMSSE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>YJ_STU_1st</td>
      <td>0.520</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Matthias_2nd</td>
      <td>0.528</td>
    </tr>
    <tr>
      <th>2</th>
      <td>mf_3rd</td>
      <td>0.536</td>
    </tr>
    <tr>
      <th>3</th>
      <td>YourModel</td>
      <td>0.574</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Rp_50th</td>
      <td>0.576</td>
    </tr>
    <tr>
      <th>5</th>
      <td>AmazonF</td>
      <td>0.789</td>
    </tr>
    <tr>
      <th>6</th>
      <td>sNaive</td>
      <td>0.847</td>
    </tr>
    <tr>
      <th>7</th>
      <td>MLP</td>
      <td>0.977</td>
    </tr>
    <tr>
      <th>8</th>
      <td>RF</td>
      <td>1.010</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Naive</td>
      <td>1.752</td>
    </tr>
  </tbody>
</table>
</div>



### Plot results

```python
autotimeseries.download_from_s3(filename='WRMSSE.pdf', filename_output='../data/WRMSSE.pdf')
```

    [==================================================]

```python
class PDF(object):
    def __init__(self, pdf, size=(200,200)):
        self.pdf = pdf
        self.size = size

    def _repr_html_(self):
        return '<iframe src={0} width={1[0]} height={1[1]}></iframe>'.format(self.pdf, self.size)

    def _repr_latex_(self):
        return r'\includegraphics[width=1.0\textwidth]{{{0}}}'.format(self.pdf)
```

```python
PDF('../data/WRMSSE.pdf', size = (600, 400))
```




<iframe src=../data/WRMSSE.pdf width=600 height=400></iframe>


