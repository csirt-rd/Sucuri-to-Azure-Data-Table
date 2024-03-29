<p align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img width="946" alt="Ciberseguridad" src="https://user-images.githubusercontent.com/46871300/125079966-38ef8380-e092-11eb-9b5e-8bd0314d9274.PNG">
  </a>
 
   <h3 align="center">Transfiere eventos de Sucuri hacia Azure Data Tables</h3>

  <p>
  Script para transferir eventos del Sucuri Web Application Firewall (WAF) hacia Azure Data Tables, en formato JSON.
  </p>
</p>

## TLP: CLEAR
---

#### Requerimientos:

* [Python3.8+](https://www.python.org/downloads/)

#### Como ejecutar:

Ejecute:

```
python3 -m venv env
```

En Windows, corra:

```
env\Scripts\activate.bat
```

En Unix o MacOS, corra:

```
source env/bin/activate
```

Luego ejecute:

```
pip install -r requirements.txt
```

Finalmente:

```
python3 app.py
```

#### Configuración:

```python
AZURE_ACC_KEY = ...        # Cambiar a la llave de cuenta correspondiente.
AZURE_ACC_NAME = ...       # Cambiar al nombre de cuenta correspondiente.
AZURE_TABLE_NAME = ...     # Cambiar al nombre de tabla correspondiente.
SUCURI_SITES = [
    {
        "secret": "...",   # Añadir tantos API_SECRET como le sea necesario.
        ...
    },
]
```

#### Referencias:

https://waf.sucuri.net/?apidocs
https://docs.microsoft.com/en-us/python/api/overview/azure/data-tables-readme?view=azure-python
https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/tables/azure-data-tables
