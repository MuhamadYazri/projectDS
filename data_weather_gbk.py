import requests
import json
import csv
import os
import datetime
import logging

# Setup directory and file paths
output_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(output_dir, "weather_data_gbk.csv")
log_file = os.path.join(output_dir, "weather_gbk_log.txt")

# Configure logging
os.makedirs(output_dir, exist_ok=True)
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def collect_weather_data():
    try:
        # GBK location code
        data_gbk = requests.get('https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=31.71.07.1001')
        response_gbk = data_gbk.json()
        
        # Get weather data
        prakiraan_cuaca = response_gbk.get('data', {})
        
        if not prakiraan_cuaca:
            logging.error("No data received from API")
            return
        
        # Check if file exists
        file_exists = os.path.isfile(csv_file)
        
        # Open CSV file in append mode
        with open(csv_file, 'a', newline='') as csvfile:
            # Define columns
            fieldnames = ['local_datetime', 'weather', 'weather_desc', 'ws', 'hu', 't']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header if file is new
            if not file_exists:
                writer.writeheader()
            
            # Process and write data
            cuaca = prakiraan_cuaca[0]['cuaca']
            for item in cuaca:
                for item2 in item:
                    # Extract required data
                    writer.writerow({
                        'local_datetime': item2.get('local_datetime', ''),
                        'weather': item2.get('weather', ''),
                        'weather_desc': item2.get('weather_desc', ''),
                        'ws': item2.get('ws', ''),
                        'hu': item2.get('hu', ''),
                        't': item2.get('t', '')
                    })
            
            logging.info(f"Weather data for GBK successfully recorded")
            print("Weather data for GBK successfully recorded")
                    
    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Error: {e}", exc_info=True)

if __name__ == "__main__":
    try:
        logging.info("Script started")
        collect_weather_data()
        logging.info("Script completed successfully")
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}", exc_info=True)
