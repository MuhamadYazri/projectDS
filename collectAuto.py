import requests
import json
import csv
import os
import datetime
import logging

# Gunakan os.path.join untuk path yang lebih portabel
import os

# Path file output
output_dir = os.path.dirname(os.path.abspath(__file__)) # Direktori script
csv_file = os.path.join(output_dir, "air_quality_data_update_github.csv")

# Setup logging di awal script
log_file = os.path.join(output_dir, "air_quality_log.txt")
os.makedirs(output_dir, exist_ok=True)
logging.basicConfig(filename=log_file, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def collect_air_quality_data():
    # API URLs dan token
    token = 'a30fea92caae312f5d6dbb5a55e12dbb13f0fc1e'
    urls = [
        f'https://api.waqi.info/feed/A416842/?token={token}',
        f'https://api.waqi.info/feed/@8294/?token={token}'
    ]
    
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Periksa apakah file CSV sudah ada
    file_exists = os.path.isfile(csv_file)
    
    # Buka file CSV dalam mode append
    with open(csv_file, 'a', newline='') as csvfile:
        # Tentukan kolom yang ingin disimpan
        fieldnames = ['timestamp', 'station_id', 'station_name', 'aqi', 'pm25', 'pm10', 'temperature', 'humidity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Tulis header jika file baru dibuat
        if not file_exists:
            writer.writeheader()
        
        # Kumpulkan data dari setiap URL
        for url in urls:
            try:
                response = requests.get(url)
                data = response.json()
                
                if data['status'] == 'ok':
                    # Ekstrak data yang diperlukan
                    station_id = data['data']['idx']
                    station_name = data['data']['city']['name']
                    aqi = data['data']['aqi']
                    
                    # Ekstrak data tambahan jika tersedia
                    iaqi = data['data'].get('iaqi', {})
                    pm25 = iaqi.get('pm25', {}).get('v', None)
                    pm10 = iaqi.get('pm10', {}).get('v', None)
                    temperature = iaqi.get('t', {}).get('v', None)
                    humidity = iaqi.get('h', {}).get('v', None)
                    
                    # Tulis data ke CSV
                    writer.writerow({
                        'timestamp': current_time,
                        'station_id': station_id,
                        'station_name': station_name,
                        'aqi': aqi,
                        'pm25': pm25,
                        'pm10': pm10,
                        'temperature': temperature,
                        'humidity': humidity
                    })
                    
                    print(f"Data untuk stasiun {station_name} berhasil dicatat.")
                    logging.info(f"Data untuk stasiun {station_name} berhasil dicatat.")
                else:
                    print(f"Error mengambil data: {data['status']}")
                    logging.error(f"Error mengambil data: {data['status']}")
                    
            except Exception as e:
                print(f"Error: {e}")
                logging.error(f"Error: {e}", exc_info=True)

if __name__ == "__main__":
    try:
        logging.info("Script dimulai")
        collect_air_quality_data()
        logging.info("Script selesai dengan sukses")
    except Exception as e:
        logging.error(f"Kesalahan fatal: {str(e)}", exc_info=True)