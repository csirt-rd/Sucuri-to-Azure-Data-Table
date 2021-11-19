#!/usr/bin/env python3
from datetime import datetime, timedelta
from os import getcwd, makedirs
import random, string
import requests
from azure.data.tables import TableClient

# Azure Data Tables
AZURE_ACC_KEY = ""
AZURE_ENDPOINT_SUFFIX = "core.windows.net"
AZURE_ACC_NAME = ""
AZURE_ENDPOINT = "{}.table.{}".format(AZURE_ACC_NAME, AZURE_ENDPOINT_SUFFIX)
AZURE_CONN_STR = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix={}".format(
    AZURE_ACC_NAME, AZURE_ACC_KEY, AZURE_ENDPOINT_SUFFIX
)

# Sucuri Info
AZURE_TABLE_NAME = ""
SUCURI_API_URL = "https://waf.sucuri.net/api?v2"
SUCURI_SITES = []

CHARS = 'abcdef' + string.digits

LOG_FILE = '-'.join([
    '/'.join([getcwd(), 'logs', 'log']),
    datetime.now().strftime("%Y%m%d")
]) + '.txt'
yesterday = datetime.now() - timedelta(1)

# Azure Data Tables sh!t
def sucuri_to_azure_table():
    try:   
        makedirs('/'.join([getcwd(), 'logs']))
    except FileExistsError:
        pass
    for i in SUCURI_SITES:
        if i["enabled"]:   
            body = requests.post(
                SUCURI_API_URL,
                data={
                    "k": i["key"], 
                    "s": i["secret"],  
                    "a": "audit_trails",   
                    "date": yesterday.strftime("%Y-%m-%d"),   
                    "format": "json"
                }
            ).json() 
            if len(body) > 2:
                with open(LOG_FILE, 'a', encoding='utf-8') as l:
                    l.write(
                        ' '.join([
                            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3],
                            '+00:00',
                            '[INF]',
                            'Getting 1000 logs from',
                            i["domain"],
                            'at',
                            datetime.now().strftime("%Y-%m-%d"),
                            '\n'
                        ])
                    )
                l.close()  
                for x in body:
                    ROW_KEY = '-'.join([
                        ''.join(random.choices(CHARS, k=8)),
                        ''.join(random.choices(CHARS, k=4)),
                        ''.join(random.choices(CHARS, k=4)),
                        ''.join(random.choices(CHARS, k=4)),
                        ''.join(random.choices(CHARS, k=12))
                    ])
                    ENTITY_TEMPLATE = {
                        "PartitionKey": i["domain"],
                        "RowKey": ROW_KEY,
                    }
                    x["request_date"] = yesterday.strftime("%d-%b-%Y")
                    x["request_time"] = datetime.now().strftime("%H:%M:%S")
                    try:
                        del x['geo_location']
                    except KeyError:
                        ENTITY = ENTITY_TEMPLATE | x
                        with TableClient.from_connection_string(AZURE_CONN_STR, AZURE_TABLE_NAME) as table_client:
                            resp = table_client.create_entity(entity=ENTITY)
                            print(resp)
                        continue
                    except TypeError:
                        pass
                    else:
                        ENTITY = ENTITY_TEMPLATE | x
                        with TableClient.from_connection_string(AZURE_CONN_STR, AZURE_TABLE_NAME) as table_client:
                            resp = table_client.create_entity(entity=ENTITY)
                            print(resp)
                with open(LOG_FILE, 'a', encoding='utf-8') as l:
                    l.write(
                        ' '.join([
                            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3],
                            '+00:00',
                            '[INF]',
                            'Sending to',
                            'Sucuri Azure Table',
                            '\n'
                        ])
                    )
                l.close()  

if __name__ == "__main__":
    sucuri_to_azure_table()
