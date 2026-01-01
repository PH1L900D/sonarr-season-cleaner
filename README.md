# Sonarr Season Auto-Unmonitor

A Python script that keeps your Sonarr library clean by syncing Season monitoring status with Episode status.

### The Problem (Jellyseerr / Overseerr)
If you delete or unmonitor episodes in Sonarr, the **Season itself** often remains marked as "Monitored".
When this happens, **Jellyseerr** (and Overseerr) assumes you still "Own" or are monitoring that content, causing the **Request Button to be greyed out** or unavailable.

### The Solution
This script scans your library. If it finds a Season where **every single episode** is unmonitored, it automatically updates the **Season itself** to be "Unmonitored".
*   **Jellyseerr:** The "Request" button becomes available again for that season.
*   **Sonarr:** Fixes the visual bookmark icons and prevents future/TBA episodes in ignored seasons from appearing in your "Wanted" list.

## Prerequisites
*   Python 3.x
*   `requests` library
*   A Sonarr API Key

## Installation

**1. Clone the repository**

Clone this repository or download the `unmonitor_seasons.py` script to your desired folder.

**2. Install dependencies**

Run the following command in your terminal:

    pip install -r requirements.txt

*(Alternatively, you can manually run: `pip install requests`)*

## Configuration

You can configure the script in two ways:
1.  **Edit the script**: Open `unmonitor_seasons.py` and edit the variables at the top.
2.  **Environment Variables**: (Recommended for Docker/Advanced users).

| Variable | Default | Description |
| :--- | :--- | :--- |
| `SONARR_URL` | `http://localhost:8989` | Your Sonarr URL (include http/https and port) |
| `SONARR_API_KEY` | `None` | Your API Key (Found in Settings > General) |
| `ENABLE_WRITE` | `False` | Set to `True` to actually apply changes. |

## Usage

### 1. Dry Run (Safe Mode)
By default, `ENABLE_WRITE` is set to `False`. Running the script will only **print** what it intends to do to the logs/console. It will not change data in Sonarr.

    python unmonitor_seasons.py

### 2. Production Run
To actually apply the changes, set `ENABLE_WRITE` to `True` inside the script, or run it with the environment variable:

**Linux / Mac:**

    export ENABLE_WRITE=True
    python unmonitor_seasons.py

**Windows (PowerShell):**

    $env:ENABLE_WRITE="True"
    python unmonitor_seasons.py

## Automation (Cron)

To keep your library clean automatically, you can schedule this script to run once a day.

**Example: Run daily at 4:30 AM**

1. Open your crontab:

       crontab -e

2. Add the following line (adjust paths to match your system):

       30 4 * * * /usr/bin/python3 /path/to/sonarr-season-cleaner/unmonitor_seasons.py >> /path/to/sonarr-season-cleaner/sonarr_unmonitor.log 2>&1

*Note: The `>> ... 2>&1` part ensures that both success messages and error logs are saved to a file so you can troubleshoot if something goes wrong.*

## License
MIT
