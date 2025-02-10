LOAD DATA INFILE '/var/lib/mysql-files/powerball.csv'
INTO TABLE powerball
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@draw_date, @ball1, @ball2, @ball3, @ball4, @ball5, @powerball, @powerplay)
SET 
    draw_date = STR_TO_DATE(@draw_date, '%Y-%m-%d'),
    ball1 = @ball1,
    ball2 = @ball2,
    ball3 = @ball3,
    ball4 = @ball4,
    ball5 = @ball5,
    powerball = @powerball,
    powerplay = NULLIF(@powerplay, '');
