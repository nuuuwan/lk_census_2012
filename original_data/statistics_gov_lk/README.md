# Census of Population and Housing 2012 — Data Tables

Population and housing data from Sri Lanka's 2012 Census, organised by Divisional Secretariat Division (DSD).

## Source

Originally extracted from [@alexstorer/srilanka](https://github.com/alexstorer/srilanka), an app built by @alexstorer for the Department of Census and Statistics and the World Bank. The source data has since been removed, but the app remains accessible [here](https://s3-us-west-2.amazonaws.com/worldbank-srilanka/choropleth-example.html).

## Data Format

Each JSON file covers one DSD, named `data_<DSD numeric ID>.json`. For example, Thimbirigasyaya DSD (ID `LK_1127`) is in `data_1127.json`.

Each file is a nested map structured as:

```
GND numeric ID → Table ID → Field ID → Field Value
```

Table and field metadata are in `tables.json` and `fields.json`.
