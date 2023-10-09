# Fingrid data fetcher
Fetches info from [Fingrids API](https://data.fingrid.fi/fi/pages/api) and saves it into a file.

Uses [requests](https://pypi.org/project/requests/) (pip install requests)

## Arguments
Takes four arguments:
- api_key (Your registered accounts API key)
- dataset_id (ID of the dataset you want to search)
- start_time (Search starting time)
- end_time (Search ending time)

Optional arguments:
- -f filetype (filetype can be: csv, json or xml) Defaults to csv

## Example: 
python FingridFetcher.py abc123abc 314 2023-06-01T00:00:00Z 2023-08-01T00:00:00Z -f json
