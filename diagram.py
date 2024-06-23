import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.lines as mlines

pd.set_option('display.max_columns', None)  

# Read the CSV file
date_column = ['datetime']
df = pd.read_csv('/Users/ahmetcol/Desktop/epilepsy_ml_project/epilepsy_ml_project/data.csv', parse_dates=date_column, dayfirst=True)

# Ensure the datetime column is in datetime format
df['datetime'] = pd.to_datetime(df['datetime'])

# Extract date and time
df['date'] = df['datetime'].dt.date
df['time'] = df['datetime'].dt.time

# Convert time to a datetime object with only the time component
df['time'] = pd.to_datetime(df['time'].astype(str), format='%H:%M:%S')
print(df)

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

ax.scatter(df['date'], df['time'], c='blue', alpha=0.5)

# Set the labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Time (24-hour format)')
ax.set_title('Date vs Time Scatter Plot')

# Format the x-axis to display dates in dd-mm-yyyy format
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))

# Format the y-axis to display time in 24-hour format
ax.yaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# Rotate the x-axis labels for better readability
plt.xticks(rotation=45)

# Add doses lines
nine_pm = pd.to_datetime('21:00:00', format='%H:%M:%S')
nine_am = pd.to_datetime('09:00:00', format='%H:%M:%S')
ax.axhline(nine_pm, color='red', linestyle='-', linewidth=1, label='9 PM')
ax.axhline(nine_am, color='red', linestyle='-', linewidth=1, label='9 AM')

# Add shaded region between 3 PM and 5 PM
three_pm = pd.to_datetime('15:00:00', format='%H:%M:%S')
five_pm = pd.to_datetime('17:00:00', format='%H:%M:%S')
ax.fill_between(df['date'].unique(), three_pm, five_pm, color='gray', alpha=0.3, hatch='//', label='15:00 - 17:00')


# Show the plot
plt.tight_layout()
plt.show()