import requests
from datetime import datetime
from bs4 import BeautifulSoup

# URL of the Powerball homepage
url = "https://www.powerball.com/"

# Fetch the webpage content
response = requests.get(url)

# Make sure the request is successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    retries = 5
    while retries > 0:

        # Locate the section containing the latest winning numbers
        winning_numbers_section = soup.find("div", id="numbers")
        
        if winning_numbers_section:
        
            # Extract the draw date and format it (convert to MM/DD/YYYY)
            draw_date_raw = winning_numbers_section.find("h5", class_="card-title mx-auto mb-3 lh-1 text-center title-date").text.strip()
            
            if draw_date_raw:
                #draw_date = datetime.strptime(draw_date_raw, "%a, %b %d, %Y").strftime("%m/%d/%Y")
                draw_date = datetime.strptime(draw_date_raw, "%a, %b %d, %Y").strftime("%Y-%m-%d")
                # Extract the winning numbers (white balls)
                white_balls = [num.text.strip() for num in winning_numbers_section.find_all("div", class_="form-control col white-balls item-powerball")]

                # Extract the Powerball number
                powerball = winning_numbers_section.find("div", class_="form-control col powerball item-powerball").text.strip()

                # Extract the Power Play multiplier (if available)
                power_play_tag = winning_numbers_section.find("span", class_="multiplier")
                power_play = power_play_tag.text.strip().replace("x", "") if power_play_tag else "N/A"

                # Format and print the results
                #print(f"Draw Date,Winning Numbers,Multiplier")
                #print(f"{draw_date},{' '.join(white_balls)} {powerball},{power_play}")
                power_play=float(power_play)
                print(f"draw_date,ball1,ball2,ball3,ball4,ball5,powerball,powerplay")
                print(f"{draw_date},{','.join(white_balls)},{powerball},{power_play}")
                break

            else:
                print("Draw date not found in the section.")
                retries -= 1
                time.sleep(1)  # Wait a bit before retrying
        else:
            print("Winning numbers section not found.")
            retries -= 1
            time.sleep(1)  # Wait a bit before retrying
else:
    print(f"Failed to fetch the webpage. HTTP Status code: {response.status_code}")


