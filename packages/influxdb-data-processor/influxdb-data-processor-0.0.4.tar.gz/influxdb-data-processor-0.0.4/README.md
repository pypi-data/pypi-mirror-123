# influxdb-data-processor
A data processor for data in influxDB.


Developed by Chai Wen Xuan 2021

## Uses:
- To fill in missing value cause by random error from data collector
- To produce fixed time sampling range data


### Processing CSV file

```python
import pandas as pd

from influxdbDataProcessor.processor import processCsvData

df = processCsvData()
```

#### User will be required to input:
1. Token
2. influxDb url
3. Organization
4. Bucket name
5. CSV file location
6. Sampling frequency (1 day: '1d', 1hour: '1h', 1 minute: '1t', 1 second: '1s')
7. Data range (1 day: '1d', 1hour: '1h', 1 minute: '1m', 1 second: '1s')

#### CSV file format:
- Contains two column ("Measurement", "Field")


### Processing array data

```python
import pandas as pd

from influxdbDataProcessor.processor import processArrayData

measurementArr = ["Air Conditioner"]
fieldArr = ["Temperature"]

df = processArrayData(measurementArr,fieldArr)
```

#### User will be required to input:
1. Token
2. influxDb url
3. Organization
4. Bucket name
5. Sampling frequency (1 day: '1d', 1hour: '1h', 1 minute: '1t', 1 second: '1s')
6. Data range (1 day: '1d', 1hour: '1h', 1 minute: '1m', 1 second: '1s')

### Ready input by user before calling function
```python
import pandas as pd

from influxdbDataProcessor.processor import processArrayData

df = processData(token,url,org,bucket,samplerange,length,mea,field)
```

#### User will be required to input:
1. Token
2. influxDb url
3. Organization
4. Bucket name
5. Sampling frequency (1 day: '1d', 1hour: '1h', 1 minute: '1t', 1 second: '1s')
6. Data range (1 day: '1d', 1hour: '1h', 1 minute: '1m', 1 second: '1s')
7. MeasurementArr
8. FieldArr



