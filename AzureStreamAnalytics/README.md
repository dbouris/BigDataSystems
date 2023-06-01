# Assignment Description

In this assignment, the core objective is to create a fully functional Azure Stream Analytics job that will be able to process a stream of data from a simulated data stream. The data will firstly arrive to an Event Hub and then forwarded to the Stream Job to be processed. The data will be processed using SQL Queries and the results will be stored in a Blob Storage. A detailed description of the assignment can be found [here](Proj4_Stream_Analytics.pdf).



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

Comment: The "Sample" option on the input can be utilised to test the incoming data. A JSON file will be returned which is expected to contain the data sent to the Event Hub from the Generator.

4. Add the Blob Storage container specified above (`atmresultscontainer`) as an Output with the following name:
    - `OutputBlob`
5. Add the [sql queries](atmjob_queries.sql) specified in the Query tab of the Stream Analytics Job.

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