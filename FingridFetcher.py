import argparse
import requests
import json
import csv
import xml.dom.minidom
import xml.etree.ElementTree as ET
from datetime import datetime

def apiGet(api_key, variable_id, start_time, end_time, file_type):

    # Määritetään URL, endpoint, header-tiedot ja parametrit
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
    
    # Palautetaan onnistunut tulos, tai näytetään virhekoodi
    if response.status_code == 200:
        return response

    else:
        print(f"Virhe {response.status_code}: Tietojen hakeminen epäonnistui")

def saveToFile(response, file_type):

    # Haetaan hakuhetki ja muotoillaan tiedostonimi sen mukaan
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_file = f"data_{timestamp}.{file_type}"

    # Tallennetaan tiedostotyypin mukaan
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

    print(f"Tiedot tallennettu tiedostoon: data_{timestamp}.{file_type}")

def printResult(response, file_type):

    # Tulostetaan hakutulos tiedostotyypin mukaan
    match file_type:
        case 'json':
            try:
                parsed_json = json.loads(response.text)
                formatted_json = json.dumps(parsed_json, indent=4)
                print(formatted_json)
            except json.JSONDecodeError as e:
                print(f"JSON Parsing Error: {e}")

        case 'csv':
            try:
            # Oletetaan, että response.txt on muotoiltu pilkkujaolla
                csv_reader = csv.reader(response.text.splitlines())
                for row in csv_reader:
                    print(', '.join(row))
            except csv.Error as e:
                print(f"CSV Parsing Error: {e}")

        case 'xml':
            try:
                dom = xml.dom.minidom.parseString(response.text)
                formatted_xml = dom.toprettyxml()
                print(formatted_xml)
            except Exception as e:
                print(f"XML Formatting Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Hae aikasarjan tiedot Fingridin palvelusta")

    # Pakolliset argumentit
    parser.add_argument("api_key", type=str, help="API-avain Fingridin palveluun")
    parser.add_argument("variable_id", type=int, help="Tietoaineiston variable id")
    parser.add_argument("start_time", type=str, help="Aloitusajankohta (YYYY-MM-ddTHH:mm:ssZ)")
    parser.add_argument("end_time", type=str, help="Lopetusajankohta (YYYY-MM-ddTHH:mm:ssZ)")

    # Valinnaiset argumentit
    parser.add_argument("-f", default="csv", choices=["csv", "json", "xml"], help="Tiedostotyyppi (Oletus: csv)")
    parser.add_argument("--save", "-s", action="store_true", help="Tallenna hakutulos tiedostoon")
    
    args = parser.parse_args()
    
    # Suoritetaan haku ja tallennetaan/tulostetaan argumenttien mukaisesti
    response = apiGet(args.api_key, args.variable_id, args.start_time, args.end_time, args.f)
    if args.save:
        saveToFile(response, args.f)
    else:
        printResult(response, args.f)

if __name__ == "__main__":
    main()