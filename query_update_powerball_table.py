import os, sys, time
from dotenv import load_dotenv
import mysql.connector
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import csv

# ======== Env variables ========

# Load environment variables
load_dotenv()

# Get credentials from environment variables
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

# CSV file
CSV_file = "./data/powerball.csv"
latest_result_file = "./data/latest_powerball.csv"

# ======== Extract the latest result ========

# URL of the Powerball homepage
url = "https://www.powerball.com/"

def fetch_latest_powerball():
    """Scrape the latest Powerball numbers from the website."""
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch webpage. HTTP Status: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    retries = 5

    while retries > 0:
        winning_numbers_section = soup.find("div", id="numbers")

        if winning_numbers_section:
            try:
                # Extract the draw date (convert to YYYY-MM-DD)
                draw_date_raw = winning_numbers_section.find("h5", class_="card-title mx-auto mb-3 lh-1 text-center title-date").text.strip()
                draw_date = datetime.strptime(draw_date_raw, "%a, %b %d, %Y").strftime("%Y-%m-%d")

                # Extract the winning numbers (white balls)
                white_balls = [num.text.strip() for num in winning_numbers_section.find_all("div", class_="form-control col white-balls item-powerball")]

                # Extract the Powerball number
                powerball = winning_numbers_section.find("div", class_="form-control col powerball item-powerball").text.strip()

                # Extract the Power Play multiplier (if available)
                power_play_tag = winning_numbers_section.find("span", class_="multiplier")
                power_play = power_play_tag.text.strip().replace("x", "") if power_play_tag else None

                # Ensure data consistency
                if len(white_balls) != 5 or not powerball:
                    print("Invalid data format. Retrying...")
                    retries -= 1
                    time.sleep(20)
                    continue

                print(f"Latest Powerball: {draw_date}, {white_balls}, Powerball: {powerball}, Power Play: {power_play}")
                return draw_date, white_balls, powerball, power_play

            except Exception as e:
                print(f"Error parsing data: {e}")
                retries -= 1
                time.sleep(20)
        else:
            print("Winning numbers section not found. Retrying...")
            retries -= 1
            time.sleep(20)

    return None


def check_and_insert_powerball():
    """Check if the latest Powerball results are in the database; insert if not."""
    powerball_data = fetch_latest_powerball()

    if not powerball_data:
        print("Failed to fetch Powerball results.")
        return

    draw_date, white_balls, powerball, power_play = powerball_data

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if the draw date already exists
        query = "SELECT COUNT(*) FROM powerball WHERE draw_date = %s"
        cursor.execute(query, (draw_date,))
        result = cursor.fetchone()

        if result[0] > 0:
            print(f"Powerball results for {draw_date} already exist in the database.")
        else:
            # Insert the new result
            insert_query = """
                INSERT INTO powerball (draw_date, ball1, ball2, ball3, ball4, ball5, powerball, powerplay)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (draw_date, *white_balls, powerball, power_play))
            conn.commit()
            print(f"Inserted new Powerball results for {draw_date} into the database.")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")

if __name__ == "__main__":
    check_and_insert_powerball()


    # Connect to MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)  # Fetch results as dictionaries

    # Query to get the latest record
    query = "SELECT * FROM powerball ORDER BY draw_date DESC LIMIT 1;"
    cursor.execute(query)

    # Fetch and print the latest record
    latest_record = cursor.fetchone()
    print(latest_record)
    print(latest_record['draw_date'])

    if latest_record:
        draw_date = latest_record['draw_date']
        white_balls = [str(latest_record[f'ball{i}']) for i in range(1, 6)]
        powerball = str(latest_record['powerball'])
        powerplay = str(float(latest_record['powerplay']))
        
        formatted_record = [draw_date] + white_balls + [powerball, powerplay]

    # Update latest_result_file
    with open(latest_result_file, "w", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(formatted_record)

    # Add latest results into CSV_file if needed
    record_exists = False
    with open(CSV_file, 'r', newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == str(latest_record['draw_date']):
                record_exists = True
                break

    if not record_exists:
        with open(CSV_file, "a", newline="") as file:
            writer = csv.writer(file, lineterminator="\n")
            writer.writerow(formatted_record)
        print(f"✅ New record added to {CSV_file}: {latest_record}")
    else:
        print("✅ No new records. CSV is up to date.")

    # Close connection
    cursor.close()
    conn.close()
    



