import influxdb_client
import pandas as pd
import numpy as np
import scipy as sp

def processCsvData():

    print("Token: ")
    token = input()

    print("influxDb url: ")
    url = input()

    print("Organization: ")
    org = input()

    print("Bucket name: ")
    bucket = input()

    print("CSV file location: ")
    file = input()

    print("Sampling frequency: ")
    samplerange = input()

    print("Data range: ")
    length = input()

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

    query_api = client.query_api()

    csv = pd.read_csv(file)

    mea = csv["Measurement"]
    mea = mea.to_list()
    mea = [str(int) for int in mea]

    field = csv["Field"]
    field = field.to_list()
    field = [str(int) for int in field]

    # get only one query here using measurement

    df_final = pd.DataFrame([])

    print(len(mea))
    for i in range(len(mea)):
        query = ' from(bucket:"' + bucket + '")\
                |> range(start: -' + length + ')\
                |> filter(fn:(r) => r._measurement == "' + mea[i] + '")\
                |> filter(fn:(r) => r._field == "' + field[i] + '" )'

        print("Measurement : ", mea[i])
        print("field : ", field[i])

        result = query_api.query(org=org, query=query)
        if len(result):
            for table in result:
                dev_name = table.records[0]["dev_name"]
                df = pd.DataFrame([], columns=["Time", str(dev_name) + " Value"])
                print("dev_name: ", dev_name)
                for record in table.records:
                    #                 print(record["dev_name"])
                    value = record.get_value()
                    if value.is_integer():
                        pass
                    else:
                        value = np.nan

                    df = df.append(
                        pd.DataFrame([[record.get_time(), value]], columns=["Time", str(dev_name) + " Value"]),
                        ignore_index=True)

                df['Time'] = pd.to_datetime(df['Time'])
                df.index = df['Time']
                del df['Time']
                #             print(df[:11])
                df_interpol = df.resample(samplerange).mean()
                #             print(df_interpol[:11])

                for x in df:
                    df_interpol[x] = df_interpol[x].interpolate(method="quadratic")

                if df_final.empty:
                    df_final = df_interpol
                else:
                    df_final = pd.concat([df_final, df_interpol], axis=1)
    #             print(df_interpol)

    return df_final


def processArrayData(mea,field):

    print("Token: ")
    token = input()

    print("influxDb url: ")
    url = input()

    print("Organization: ")
    org = input()

    print("Bucket name: ")
    bucket = input()

    print("Sampling frequency: ")
    samplerange = input()

    print("Data range: ")
    length = input()

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

    query_api = client.query_api()

    df_final = pd.DataFrame([])

    print(len(mea))
    for i in range(len(mea)):
        query = ' from(bucket:"' + bucket + '")\
                |> range(start: -' + length + ')\
                |> filter(fn:(r) => r._measurement == "' + mea[i] + '")\
                |> filter(fn:(r) => r._field == "' + field[i] + '" )'

        print("Measurement : ", mea[i])
        print("field : ", field[i])

        result = query_api.query(org=org, query=query)
        if len(result):
            for table in result:
                dev_name = table.records[0]["dev_name"]
                df = pd.DataFrame([], columns=["Time", str(dev_name) + " Value"])
                print("dev_name: ", dev_name)
                for record in table.records:
                    #                 print(record["dev_name"])
                    value = record.get_value()
                    if value.is_integer():
                        pass
                    else:
                        value = np.nan

                    df = df.append(
                        pd.DataFrame([[record.get_time(), value]], columns=["Time", str(dev_name) + " Value"]),
                        ignore_index=True)

                df['Time'] = pd.to_datetime(df['Time'])
                df.index = df['Time']
                del df['Time']
                #             print(df[:11])
                df_interpol = df.resample(samplerange).mean()
                #             print(df_interpol[:11])

                for x in df:
                    df_interpol[x] = df_interpol[x].interpolate(method="quadratic")

                if df_final.empty:
                    df_final = df_interpol
                else:
                    df_final = pd.concat([df_final, df_interpol], axis=1)
    #             print(df_interpol)

    return df_final

def processData(token,url,org,bucket,samplerange,length,mea,field):

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

    query_api = client.query_api()

    df_final = pd.DataFrame([])

    print(len(mea))
    for i in range(len(mea)):
        query = ' from(bucket:"' + bucket + '")\
                |> range(start: -' + length + ')\
                |> filter(fn:(r) => r._measurement == "' + mea[i] + '")\
                |> filter(fn:(r) => r._field == "' + field[i] + '" )'

        print("Measurement : ", mea[i])
        print("field : ", field[i])

        result = query_api.query(org=org, query=query)
        if len(result):
            for table in result:
                dev_name = table.records[0]["dev_name"]
                df = pd.DataFrame([], columns=["Time", str(dev_name) + " Value"])
                print("dev_name: ", dev_name)
                for record in table.records:
                    #                 print(record["dev_name"])
                    value = record.get_value()
                    if value.is_integer():
                        pass
                    else:
                        value = np.nan

                    df = df.append(
                        pd.DataFrame([[record.get_time(), value]], columns=["Time", str(dev_name) + " Value"]),
                        ignore_index=True)

                df['Time'] = pd.to_datetime(df['Time'])
                df.index = df['Time']
                del df['Time']
                #             print(df[:11])
                df_interpol = df.resample(samplerange).mean()
                #             print(df_interpol[:11])

                for x in df:
                    df_interpol[x] = df_interpol[x].interpolate(method="quadratic")

                if df_final.empty:
                    df_final = df_interpol
                else:
                    df_final = pd.concat([df_final, df_interpol], axis=1)
    #             print(df_interpol)

    return df_final

