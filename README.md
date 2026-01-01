# Sonarr Season Auto-Unmonitor

A python script that checks your Sonarr library. If it finds a Season where **every single episode** is unmonitored, it will automatically toggle the monitoring status of the **Season itself** to "Unmonitored".

This helps keep the "Wanted" and "Cutoff Unmet" lists clean.

## Prerequisites
*   Python 3.x
*   A Sonarr API Key

## Installation

1. Clone this repository or download the script.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
