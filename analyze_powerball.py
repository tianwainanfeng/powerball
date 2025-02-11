import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations

# ======= Global Controls ========

do_print = False
plot_path = './plots/'

sns.set_style("darkgrid") # note: all "seaborn-darkgrid" changed to "seaborn-v0_8-darkgrid"

colors = ["blue", "green", "red", "purple", "orange", "brown", "pink"]
markers = ["o", "s", "D", "^", "v", "P", "*"]

# ========  Read the data (if stored as a CSV file) ========

df = pd.read_csv("./data/powerball.csv")

# names of columns
if do_print:
    print(df.columns)

# number of rows (first value of shape)
if do_print:
    print(f"Number of rows: {df.shape[0]}")

# ======== Sort ========

# sort by date
df["draw_date"] = pd.to_datetime(df["draw_date"])
df = df.sort_values("draw_date")

# print out first 10 rows
if do_print:
    print(df.head(10))

df["weekday"] = df["draw_date"].dt.day_name()

# print out first 3 rows
if do_print:
    print()
    print(df.head(3))

# ========  Plots ========

# ==== Powerball numbers ====

# -- powerball distribution --

powerball_counts = df["powerball"].value_counts().sort_index()

jpg_filename_powerball = "powerball_distribution.jpg"
with plt.style.context('seaborn-v0_8-darkgrid'):
    plt.figure(figsize=(10, 5))
    plt.bar(powerball_counts.index, powerball_counts.values, color='red')
    plt.xlabel("Powerball Number")
    plt.ylabel("Frequency")
    plt.title("Distribution of Powerball Numbers")
    plt.xticks(range(min(powerball_counts.index), max(powerball_counts.index) + 1))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.subplots_adjust(left=0.07, right=0.95, top=0.92, bottom=0.1)
    # Save plot as a PDF file
    plt.savefig(plot_path + jpg_filename_powerball, format="jpg")
    #plt.show()

if do_print:
    print(f"Powerball distribution plot saved as '{jpg_filename_powerball}'.")

# -- powerball vs weekday --

valid_weekdays = df["weekday"].unique()
if do_print:
    print("Valid draw weekdays in the dataset:", valid_weekdays)

num_days = len(valid_weekdays)
fig_p_w, axes_p_w = plt.subplots(num_days, 1, figsize=(10, 4 * num_days), sharex=True)

bins = range(min(powerball_counts.index), max(powerball_counts.index) + 2)
bin_centers = np.array([(b + 0.5) for b in bins[:-1]])
if do_print:
    print(bin_centers)

jpg_filename_powerball_weekday = "powerball_vs_weekday.jpg"
with plt.style.context('seaborn-v0_8-darkgrid'):
    plt.figure(figsize=(12, 6))

    for idx, day in enumerate(valid_weekdays):
        subset = df[df["weekday"] == day]
        
        # Histogram for frequency count
        #plt.hist(subset["Powerball"], bins=bins, alpha=0.5, color=colors[idx % len(colors)], label=day, edgecolor="black")

        # Scatter plot to indicate peak values
        counts, bin_edges = np.histogram(subset["powerball"], bins=bins)
        plt.scatter(bin_centers, counts, color=colors[idx % len(colors)], marker=markers[idx % len(markers)], label=f"{day}")
        # Line plot to connect the scatter points
        plt.plot(bin_centers, counts, color=colors[idx % len(colors)], linestyle="-", alpha=0.7)

    plt.title("Powerball Number Distribution by Weekday")
    plt.xlabel("Powerball Number")
    plt.ylabel("Frequency")

    #plt.xlim(bins[0] - 0.5, bins[-1] + 0.5) # Set x-axis limits to reduce empty margins
    plt.xticks(bin_centers, labels=[str(int(x)) for x in bin_centers])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(fontsize=16)
    plt.subplots_adjust(left=0.07, right=0.95, top=0.92, bottom=0.1)

    plt.savefig(plot_path + jpg_filename_powerball_weekday, format="jpg")
    #plt.show()

if do_print:
    print(f"Powerball vs. Weekday plot saved as '{jpg_filename_powerball_weekday}'.")

# ==== White Balls ====

# ---- white ball distribution ----

# flatten the list to get all white ball numbers
all_white_balls = df[["ball1", "ball2", "ball3", "ball4", "ball5"]].stack().reset_index(drop=True)

# count occurrences of each white ball number
white_ball_counts = all_white_balls.value_counts().sort_index()

# Create a figure and save to PDF
jpg_filename_whiteballs = "white_ball_distribution.jpg"
with plt.style.context('seaborn-v0_8-darkgrid'):
    plt.figure(figsize=(15, 5))
    plt.bar(white_ball_counts.index, white_ball_counts.values, color='blue')
    plt.xlabel("White Ball Number")
    plt.ylabel("Frequency")
    plt.title("Distribution of White Ball Numbers")
    plt.xticks(range(min(white_ball_counts.index), max(white_ball_counts.index) + 1))
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.subplots_adjust(left=0.06, right=0.96, top=0.92, bottom=0.1)
    # Save plot as a PDF file
    plt.savefig(plot_path + jpg_filename_whiteballs, format="jpg")
    #plt.show()

if do_print:
    print(f"White ball distribution plot saved as '{jpg_filename_whiteballs}'.")

# ---- pairwise correlation heatmap ----

white_balls = df[["ball1", "ball2", "ball3", "ball4", "ball5"]]
plt.figure(figsize=(7, 6))
sns.heatmap(white_balls.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Pairwise Correlation of White Balls")
plt.subplots_adjust(left=0.1, right=1, top=0.9, bottom=0.12)
plt.savefig(plot_path + "white_ball_correlation.jpg")
#plt.show()

if do_print:
    print(f"White ball correlation plot saved as 'white_ball_correlation.jpg'")

# ---- distribution of number gaps ----

white_ball_df = df[["ball1", "ball2", "ball3", "ball4", "ball5"]]
gap_df = white_ball_df.diff(axis=1).iloc[:, 1:]  # Compute gaps between consecutive white balls

plt.figure(figsize=(7, 5))
for i, col in enumerate(gap_df.columns):
    sns.histplot(gap_df[col], bins=20, kde=False, label=f"Gap {i+1}-{i+2}", alpha=0.4)

plt.xlabel("Gap Size")
plt.ylabel("Frequency")
plt.title("Distribution of White Ball Gaps")
plt.legend(fontsize=14)
plt.xlim(-10, 60)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.12)
plt.savefig(plot_path + "white_ball_gaps.jpg")
#plt.show()

if do_print:
    print(f"White ball gap plot saved as 'white_ball_gaps.jpg'")

# ---- co-occurrence of number pairs ----

# Extract white balls as lists
white_balls_list = df[["ball1", "ball2", "ball3", "ball4", "ball5"]].values.tolist()

pair_counts = {}

# Count occurrences of number pairs
for balls in white_balls_list:
    for pair in combinations(sorted(balls), 2):  # Ensure consistent order
        pair_counts[pair] = pair_counts.get(pair, 0) + 1

# Convert to DataFrame
pair_df = pd.DataFrame(list(pair_counts.items()), columns=["Pair", "Count"])
pair_df[["Num1", "Num2"]] = pd.DataFrame(pair_df["Pair"].tolist(), index=pair_df.index)
pair_df = pair_df.pivot(index="Num1", columns="Num2", values="Count").fillna(0)

# Heatmap for pair occurrences
plt.figure(figsize=(9, 8))
sns.heatmap(pair_df, cmap="Blues", annot=False)
plt.xlabel("White Ball Number")
plt.ylabel("White Ball Number")
plt.title("Co-occurrence Heatmap of White Ball Pairs")
plt.subplots_adjust(left=0.1, right=0.98, top=0.9, bottom=0.12)
plt.savefig(plot_path + "white_ball_pairs.jpg")
#plt.show()

if do_print:
    print(f"White ball pair plot saved as 'white_ball_pairs.jpg'")

"""
# ---- each draw's white balls ----

plt.figure(figsize=(10, 6))
for i, balls in enumerate(white_balls_list):
    plt.scatter(balls, [i] * 5, label=f"Draw {i+1}" if i < 1 else "", alpha=0.7)

plt.xlabel("White Ball Number")
plt.ylabel("Draw Index")
plt.title("White Ball Selections Over Time")
plt.xticks(range(1, 70, 2))  # Adjust for clarity
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.12)
plt.savefig(plot_path + "white_ball_draws.jpg")
#plt.show()

if do_print:
    print(f"White ball draw plot saved as 'white_ball_draws.jpg'")
"""

# ---- distributions of each white ball ----

plt.figure(figsize=(10, 6))

# Count occurrences of each number in each position
white_ball_counts = {i: df[f'ball{i}'].value_counts().sort_index() for i in range(1, 6)}

labels = [f'White Ball {i}' for i in range(1, 6)]

for i in range(1, 6):
    x_vals = white_ball_counts[i].index
    y_vals = white_ball_counts[i].values
    plt.plot(x_vals, y_vals, color=colors[i-1], marker=markers[i-1], label=labels[i-1], linestyle='-', linewidth=1)

# Formatting
plt.xlabel("White Ball Number")
plt.ylabel("Frequency")
plt.title("Distribution of Each White Ball Position")
plt.xticks(np.arange(1, 70, step=2))  # Adjust as needed
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=12, loc='upper center')  # Increase legend size

# Show plot
plt.tight_layout()
plt.savefig(plot_path + "white_ball_each_distribution.jpg")
#plt.show()

if do_print:
    print(f"White ball each distribution plot saved as 'white_ball_each_distribution.jpg'")
