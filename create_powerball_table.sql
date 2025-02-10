CREATE TABLE powerball (
    draw_date DATE NOT NULL,         -- Date of the drawing
    ball1 INT NOT NULL,              -- First white ball
    ball2 INT NOT NULL,              -- Second white ball
    ball3 INT NOT NULL,              -- Third white ball
    ball4 INT NOT NULL,              -- Fourth white ball
    ball5 INT NOT NULL,              -- Fifth white ball
    powerball INT NOT NULL,          -- Red Powerball number
    powerplay INT DEFAULT NULL,      -- PowerPlay multiplier (NULL if not available)
    PRIMARY KEY (draw_date)         -- Unique constraint for draw date
);
