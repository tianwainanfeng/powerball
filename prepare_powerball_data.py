import six
import pandas as pd

# Load the original CSV
df = pd.read_csv("./data/Lottery_Powerball_Winning_Numbers_Beginning_2010.csv")

# Convert date format (MM/DD/YYYY -> YYYY-MM-DD)
df["Draw Date"] = pd.to_datetime(df["Draw Date"], format="%m/%d/%Y").dt.strftime("%Y-%m-%d")

# Split the "Winning Numbers" into separate columns
df[["ball1", "ball2", "ball3", "ball4", "ball5", "powerball"]] = df["Winning Numbers"].str.split(" ", expand=True)

# Select and rename columns
df = df.rename(columns={"Draw Date": "draw_date", "Multiplier": "powerplay"})

# Save the new CSV with correct formatting
df[["draw_date", "ball1", "ball2", "ball3", "ball4", "ball5", "powerball", "powerplay"]].to_csv("./data/powerball.csv", index=False)

print("✅ Data processing complete! File saved as powerball.csv.")
