import argparse
import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime

def apiGet(api_key, variable_id, start_time, end_time, file_type):
    base_url = "https://api.fingrid.fi"
    endpoint = f"/v1/variable/{variable_id}/events/{file_type}"
    headers = {
        "x-api-key": api_key
    }
    
    params = {
        "start_time": start_time,
        "end_time": end_time,
    }
    
    response = requests.get(base_url + endpoint, headers=headers, params=params)
    
    if response.status_code == 200:
        tallennus(response, file_type)

    else:
        print(f"Virhe {response.status_code}: Tietojen hakeminen epäonnistui")

def tallennus(response, file_type):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_file = f"data_{timestamp}.{file_type}"

    match file_type:
        case 'json':
            with open(output_file, 'w') as json_file:
                json.dump(response.json(), json_file, indent=4)
        case 'csv':
            with open(output_file, 'w') as csv_file:
                csv_file.write(response.text)
        case 'xml':
            with open(output_file, 'wb') as xml_file:
                xml_file.write(response.content)

    print("Haku onnistunut")
    print(f"Tiedot tallennettu tiedostoon: data_{timestamp}.{file_type}")

def main():
    parser = argparse.ArgumentParser(description="Hae aikasarjan tiedot Fingridin palvelusta")

    # Pakolliset argumentit
    parser.add_argument("api_key", type=str, help="API-avain Fingridin palveluun")
    parser.add_argument("variable_id", type=int, help="Tietoaineiston variable id")
    parser.add_argument("start_time", type=str, help="Aloitusajankohta (YYYY-MM-ddTHH:mm:ssZ)")
    parser.add_argument("end_time", type=str, help="Lopetusajankohta (YYYY-MM-ddTHH:mm:ssZ)")

    # Valinnaiset argumentit
    parser.add_argument("-f", default="csv", choices=["csv", "json", "xml"], help="Tiedostotyyppi (Oletus: csv)")
    
    args = parser.parse_args()
    
    apiGet(args.api_key, args.variable_id, args.start_time, args.end_time, args.f)

if __name__ == "__main__":
    main()