# Assignment Description

In this assignment, the core objective is to create a fully functional Azure Stream Analytics job that will be able to process a stream of ATM data from a simulated data stream. The data will firstly arrive to an Event Hub and then forwarded to the Stream Job to be processed. The data will be processed using SQL Queries and the results will be stored in a Blob Storage. A detailed description of the assignment can be found [here](Proj4_Stream_Analytics.pdf).


## ATM Data
The Data Generator creates ATM data in JSON format. <br>
Example ATM event: `{ "ATMCode": 10 , "CardNumber": 4026567514157759, "Type": 1 , "Amount": 42 }`

A set of reference files are provided to the Stream Analytics Job. These files contain the following information:
- Area.json: Contains the area code and the corresponding area name (area_country, area_city)
- Atm.json: Contains the ATM code and the corresponding area code (area_code).
- Customer.json: Contains personal information of the customer (first_name, last_name, age etc).

## Queries 

A set of queries should be modelled to process the incoming data. The queries asked are the following:
1. Show the total `Amount` of `Type = 0` transactions at `ATM Code = 21` of the last 10 minutes. Repeat as new events keep flowing in (use a sliding window).
2. Show the total `Amount` of `Type = 1` transactions at `ATM Code = 21` of the last hour. Repeat once every hour
(use a tumbling window).
3. Show the total `Amount` of `Type = 1` transactions at `ATM Code = 21` of the last hour. Repeat once every 30 minutes (use a hopping window).
4. Show the total `Amount` of `Type = 1` transactions per `ATM Code` of the last one hour (use a sliding window).
5. Show the total `Amount` of `Type = 1` transactions per `Area Code` of the last hour. Repeat once every hour (use a tumbling window).
6. Show the total `Amount` per ATM’s `City` and Customer’s `Gender` of the last hour. Repeat once every hour (use a tumbling window).
7. Alert (SELECT “1”) if a Customer has performed two transactions of `Type = 1` in a window of an hour (use a sliding window).
8. Alert (SELECT “1”) if the `Area Code` of the ATM of the transaction is not the same as the “Area Code” of the `Card Number` (Customer’s Area Code) - (use a sliding window)


# Azure Stream Analytics Configuration

## Event Hub Configuration

1. Create a new Event Hub Namespace (`AuebNamespace`)
2. Create a new Event Hub (`bdmshub`)
3. Create a new Shared Access Policy
    - SendPolicy
    - ReceivePolicy

View the Event Hub setup screenshots [here](Setup_Screenshots/EventHub/).

## Data Generator Configuration

1. Download the [Security Access Signature (SAS) Generator](https://github.com/sandrinodimattia/RedDog/releases).
2. Fill the required fields to generate the SAS Token. 
    - Namespace: `AuebNamespace`
    - Event Hub: `bdmshub`
    - Publisher: `Laptop`
    - SenderKeyName: `SendPolicy`
    - Sender Key: The `primary key` of the SendPolicy created
    - Token TTL (minutes): `7200`
3. Download the [Data Generator](https://edu.dmst.aueb.gr/mod/resource/view.php?id=2535)
4. Replace the Config variables to match the Event Hub created.
5. Recplace the SAS key with the one generated above.
6. Open the DataGenerator in a browser and press `SEND DATA`

To verify the Data Ingestion process, monitor the Event Hub's `Metrics` tab. The "Incoming Requests" and "Incoming Messages" metrics should be increasing. Any errors are captured in the "User Errors" metric which means that the request was not succesfull.

View the Data Generator Configuration screenshots [here](DataIngestionScreenshots).

## Blob Storage Configuration

1. Create a new Blob Storage Namespace (`auebstorage`)
2. Create a new Container to store the results of the job (`atmresultscontainer`)
3. Create a new Container to store the reference files (`atmrefcontainer`)
    - Upload the reference files 

View the Blob Storage setup screenshots [here](Setup_Screenshots/BlobStorage/).

## Stream Analytics Configuration

1. Create a new Stream Analytics Job (`bdmsjob`)
2. Add the Event Hub specified above as an Input
3. Add the Blob Storage reference specified above (`atmrefcontainer`) as Input. Each reference file is added as a separate Input with the following names:
    - `InputAreaRef` : The reference Blob storage with the `Area.json` file specified in the path.
    - `InputAtmRef` : The reference Blob storage with the `Atm.json` file specified in the path.
    - `InputCustomerRef` : The reference Blob storage with the `Customer.json` file specified in the path.  
4. Add the Blob Storage container specified above (`atmresultscontainer`) as an Output with the following name:
    - `OutputBlob`
5. Add the [sql queries](atmjob_queries.sql) specified in the Query tab of the Stream Analytics Job.

The "Sample" option on the input can be utilised to test the incoming data. A JSON file will be returned which is expected to contain the data produced from the Generator and some attributes added by the Event Hub: `EventProcessedUtcTime`, `PartitionId` and `EventEnqueuedUtcTime`.


View the Stream Analytics setup screenshots [here](Setup_Screenshots/StreamAnalyticsJob/).

# Running the Azure Stream Analytics Job

1. Start the Data Generator
2. Start the Stream Analytics Job
    - Monitor the Stream Analytics Job's `Monitoring` tab. 
3. After some minutes stop the Generator and the Stream Analytics Job.
4. The output of the Stream Analytics Job can be found in the Blob Storage container specified above (`atmresultscontainer`). 


# Results
The results of the job can be found [here](StreamJobResults/). <br>
Each file contains the results of the corresponding query. The results are stored in JSON format.