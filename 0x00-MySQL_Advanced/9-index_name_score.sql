-- Import the table dump
-- Assuming the table name is 'names' and it has columns 'name' and 'score'

-- Create the index
CREATE INDEX idx_name_first_score ON names (SUBSTRING(name, 1, 1), LEFT(score::text, 1));
