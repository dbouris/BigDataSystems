SELECT -- Q1
    sum(CAST([input].[Amount] AS BIGINT)) as Total_Amount, 
    System.Timestamp() AS Event_Time
INTO [q1output]
FROM
    [input] 
WHERE [input].[Type] = 0 and [input].[ATMCode] = 21
GROUP BY SlidingWindow(minute, 10)
SELECT -- Q2
    sum(CAST([input].[Amount] AS BIGINT)) as Total_Amount, 
    System.Timestamp() AS Time
INTO [q2output]
FROM
    [input]
WHERE [input].[Type] = 1 and [input].[ATMCode] = 21
GROUP BY TumblingWindow(hour, 1)
SELECT -- Q3 
    sum(CAST([input].[Amount] AS BIGINT)) as Total_Amount, 
    System.Timestamp() AS Time
INTO [q3output]
FROM
    [input]
WHERE [input].[Type] = 1 and [input].[ATMCode] = 21
GROUP BY HoppingWindow(minute, 60, 30)
SELECT -- Q4
    [input].[ATMCode],
    sum(CAST([input].[Amount] AS BIGINT)) as Total_Amount, 
    System.Timestamp() AS Time
INTO [q4output]
FROM
    [input]
WHERE Type = 1
GROUP BY [input].[ATMCode],
         SlidingWindow(hour, 1)
SELECT -- Q5
    [inputAtmRef].[area_code],
    sum(CAST([input].[Amount] AS BIGINT)) as Total_Amount, 
    System.Timestamp() AS Time
INTO [q5output]
FROM
    [input]
INNER JOIN [inputAtmRef] 
    ON [input].[ATMCode] = [inputAtmRef].[atm_code] 
WHERE [input].[Type] = 1
GROUP BY [inputAtmRef].[area_code],
         TumblingWindow(hour, 1)
SELECT -- Q6
    [inputAreaRef].[area_city],
    [inputCustomerRef].[gender],
    sum(CAST([input].[Amount] AS BIGINT)) as Total_Amount, 
    System.Timestamp() AS Time
INTO [q6output]
FROM
    [input]
INNER JOIN [inputAtmRef]
    ON [input].[ATMCode] = [inputAtmRef].[atm_code] 
INNER JOIN [inputAreaRef]
    ON [inputAtmRef].[area_code] = [inputAreaRef].[area_code]
INNER JOIN [inputCustomerRef]
    ON [input].[CardNumber] = [inputCustomerRef].[card_number]
GROUP BY [inputAreaRef].[area_city],
         [inputCustomerRef].[gender], 
         TumblingWindow(hour, 1)
SELECT -- Q7
    [inputCustomerRef].[first_name],
    [inputCustomerRef].[last_name],
    [input].[CardNumber] AS Card_Number,
    COUNT (*) AS Transactions,
    System.Timestamp AS Time
INTO
    [q7output]
FROM
    [input]
INNER JOIN [inputCustomerRef]
    ON [inputCustomerRef].[card_number] = [input].[CardNumber]
WHERE [input].[Type] = 1
GROUP BY [inputCustomerRef].[first_name],
         [inputCustomerRef].[last_name],
         [input].[CardNumber],
         SlidingWindow(hour, 1)
HAVING Transactions = 2
SELECT -- Q8
    [inputAtmRef].[area_code] AS Atm_Area_Code,
    [inputCustomerRef].[area_code] AS Customer_Area_Code,
    COUNT (*),
    System.Timestamp AS Time
INTO
    [q8output]
FROM
    [input]
INNER JOIN [inputCustomerRef]
    ON [inputCustomerRef].[card_number] = [input].[CardNumber]
INNER JOIN [inputAtmRef]
    ON [inputAtmRef].[atm_code] = [input].[ATMCode]
WHERE [inputAtmRef].[area_code] != [inputCustomerRef].[area_code]
GROUP BY [inputAtmRef].[area_code],
         [inputCustomerRef].[area_code], 
         SlidingWindow(hour, 1)