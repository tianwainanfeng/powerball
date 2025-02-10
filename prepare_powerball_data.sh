#!/bin/bash

# Input and output file
INPUT="./data/Lottery_Powerball_Winning_Numbers_Beginning_2010.csv"
OUTPUT="./data/powerball.csv"

# Prepare header
echo "draw_date,ball1,ball2,ball3,ball4,ball5,powerball,powerplay" > "$OUTPUT"

# Process each line (skip the header)
tail -n +2 "$INPUT" | while IFS=, read -r date numbers multiplier; do
    # Convert date format (MM/DD/YYYY -> YYYY-MM-DD)
    formatted_date=$(date -d "$date" +"%Y-%m-%d" 2>/dev/null || date -j -f "%m/%d/%Y" "$date" +"%Y-%m-%d")
    
    # Replace spaces in Winning Numbers with commas
    formatted_numbers=$(echo "$numbers" | tr ' ' ',')
    
    # Append to output file
    echo "$formatted_date,$formatted_numbers,$multiplier" >> "$OUTPUT"
done

echo "✅ Data processing complete! File saved as powerball.csv."

