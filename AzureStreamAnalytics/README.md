# Assignment Description

In this assignment, the core objective is to create a fully functional Azure Stream Analytics job that will be able to process a stream of data from a simulated data stream. The data will firstly arrive to an Event Hub and then forwarded to the Stream Job to be processed. The data will be processed using SQL Queries and the results will be stored in a Blob Storage. A detailed description of the assignment can be found [here](Proj4_Stream_Analytics.pdf).



# Azure Stream Analytics Configuration

## Event Hub Configuration

Steps: 
- Create a new Event Hub Namespace (`AuebNamespace`)
- Create a new Event Hub (`bdmshub`)
- Create a new Shared Access Policy
    - SendPolicy
    - ReceivePolicy

## Data Generator Configuration

Steps:
- Download the [Security Access Signature (SAS) Generator](https://github.com/sandrinodimattia/RedDog/releases).
- Fill the required fields to generate the SAS Token. 
    - Namespace: `AuebNamespace`
    - Event Hub: `bdmshub`
    - Publisher: `Laptop`
    - SenderKeyName: `SendPolicy`
    - Sender Key: The `primary key` of the SendPolicy created
    - Token TTL (minutes): `7200`
- Download the [Data Generator](https://edu.dmst.aueb.gr/mod/resource/view.php?id=2535)
- Replace the Config variables to match the Event Hub created.
- Recplace the SAS key with the one generated above.
- Open the DataGenerator in a browser and press `SEND DATA`

To verify the Data Ingestion process, monitor the Event Hub's `Metrics` tab. The "Incoming Requests" and "Incoming Messages" metrics should be increasing. Any errors are captured in the "User Errors" metric which means that the request was not succesfull.


## Blob Storage Configuration

Steps:
- Create a new Blob Storage Namespace (`auebstorage`)
- Create a new Container to store the results of the job (`atmresultscontainer`)
- Create a new Container to store the reference files (`atmrefcontainer`)
    - Upload the reference files 

## Stream Analytics Configuration

Steps:
- Create a new Stream Analytics Job (`bdmsjob`)
- Add the Event Hub specified above as an Input
- Add the Blob Storage reference specified above (`atmrefcontainer`) as Input. Each reference file is added as a separate Input.
    - `InputAreaRef` : The reference Blob storage with the `Area.json` file specified in the path.
    - `InputAtmRef` : The reference Blob storage with the `Atm.json` file specified in the path.
    - `InputCustomerRef` : The reference Blob storage with the `Customer.json` file specified in the path.  
- Add the Blob Storage container specified above (`atmresultscontainer`) as an Output 
- Add the [sql queries](atmjob_queries.sql) specified in the Query tab of the Stream Analytics Job.
