import requests
import logging
import os
import sys

# ================= CONFIGURATION =================
# Users can edit these lines, OR use Environment Variables
SONARR_URL = os.getenv('SONARR_URL', 'http://localhost:8989')
API_KEY = os.getenv('SONARR_API_KEY', 'YOUR_API_KEY_HERE')

# Set to 'False' for Dry Run (no changes), 'True' to apply changes
# Defaults to False for safety
ENABLE_WRITE = os.getenv('ENABLE_WRITE', 'False').lower() == 'true'
# =================================================

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def get_headers():
    return {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }

def validate_config():
    if "YOUR_API_KEY" in API_KEY:
        logging.error("Error: API Key not set. Please edit the script or set SONARR_API_KEY env var.")
        sys.exit(1)

def get_all_series():
    """Fetch all series from Sonarr."""
    endpoint = f"{SONARR_URL}/api/v3/series"
    try:
        response = requests.get(endpoint, headers=get_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to get series: {e}")
        return []

def get_episodes_for_series(series_id):
    """Fetch all episodes for a specific series."""
    endpoint = f"{SONARR_URL}/api/v3/episode"
    params = {"seriesId": series_id}
    try:
        response = requests.get(endpoint, headers=get_headers(), params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to get episodes for series {series_id}: {e}")
        return []

def update_series(series_data):
    """Send the updated series data back to Sonarr."""
    series_id = series_data['id']
    endpoint = f"{SONARR_URL}/api/v3/series/{series_id}"
    try:
        response = requests.put(endpoint, json=series_data, headers=get_headers())
        response.raise_for_status()
        logging.info(f"Successfully updated series: {series_data['title']}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to update series {series_data['title']}: {e}")

def process_series():
    validate_config()
    series_list = get_all_series()
    logging.info(f"Found {len(series_list)} series. Checking status... (Write Enabled: {ENABLE_WRITE})")

    for series in series_list:
        series_id = series['id']
        series_title = series['title']
        
        if not series['monitored']:
            continue

        episodes = get_episodes_for_series(series_id)
        
        # Map: { season_number: [is_monitored_bool, ...] }
        season_map = {}
        for ep in episodes:
            s_num = ep['seasonNumber']
            if s_num not in season_map:
                season_map[s_num] = []
            season_map[s_num].append(ep['monitored'])

        series_dirty = False
        
        for season_data in series['seasons']:
            season_num = season_data['seasonNumber']
            is_currently_monitored = season_data['monitored']
            
            if not is_currently_monitored:
                continue
            
            if season_num in season_map:
                ep_statuses = season_map[season_num]
                
                # If episodes exist AND all are False (unmonitored)
                if ep_statuses and not any(ep_statuses):
                    logging.info(f"[{series_title}] Season {season_num}: All episodes unmonitored. Unmonitoring Season.")
                    season_data['monitored'] = False
                    series_dirty = True

        if series_dirty:
            if ENABLE_WRITE:
                update_series(series)
            else:
                logging.info(f"[{series_title}] DRY RUN: Would unmonitor specific seasons.")

if __name__ == "__main__":
    process_series()
