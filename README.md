
About: Powerball Winning Numbers
Version: 1.0

# Structure:
  - README.md # this file

  - data
    - Lottery_Powerball_Winning_Numbers_Beginning_2010.csv # old format dataset
    - powerball.csv # new format dataset
    - latest_powerball.csv # latest powerball result
  
  - plots
    - \*.pdf # some plots
    - \*.jpg # some plots
  
  - prepare_powerball_data.py # convert dataset from old format to new format
  - prepare_powerball_data.sh # convert dataset from old format to new format
  - analyze_powerball.py # make some plots from old format dataset
  - analyze_powerball_old_format.py # make some plots from new format dataset
  - get_powerball_result.py # get latest powerball winning numbers
  
  - create_powerball_table.sql # MySQL: create a table
  - load_powerball_data_to_database.sql # MySQL: load data in .csv file into table

  - query_update_powerball_table.py # check latest result and update database table if needed

# Dataset:
  Data file (\*.csv format) can be downloaded from website, i.e., (https://www.kaggle.com/datasets/ulrikthygepedersen/lottery-powerball-winning-numbers?resource=download)

# MySQL:
  ```
  mysql -u user_name -p -D database_name < create_powerball_table.sql
  mysql -u user_name -p database_name < load_powerball_data_to_database.sql
```


# Query and update database through python mysql:
  Define relevant database configuration (credentials as environment variables) in .env file. For example:
  
  ```
   DB_HOST=localhost
   DB_USER=user_name # mysql
   DB_PASSWORD=user_password
   DB_NAME=database_name
```

# Scheduled tasks:
  Using Cron Job (Linux/macOS) to schedule a task:
  From terminal, run:
      ```crontab -e```
  This will open a crontab, add the tasks you want to schedule.
  For example, the following will run query_update_powerball_table.py at midnight every 2 days on the server:
      ```
	  0 0 */2 * * /usr/bin/python3 /path/to/query_update_powerball_table.py
    ```
  To verify the cron job, run:
      ```crontab -l```

# HTML:
  To test locally, you may try to run:
      ```python3 -m http.server 8000```
  then open:
      http://localhost:8000/
   then click and open powerball.html
