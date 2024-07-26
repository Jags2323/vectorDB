# MINTS API

MINTS product internally interacts with multiple REST APIs that might need to set integrations up and maintain the stable architecture in the microservices applications are connected with multiple target systems.

MINTS API needs authentication of signature to access multiple internal services. Below is the API’s list of MINTS Integration service product.

## List of MINTS API:
1. MTX API
2. Authorization API
3. Signature Generation API
4. Integration Testing API
5. REST-ENTRY API
6. Service Invoker API
7. Data Mapper (X-Ref API)

## 1.MTX API:
In this MTX API users can access their MTX maps and mapping can be done with the required fields.
Using MTX functions is used to perform all aggregation operations such sum,avg, max, min, for applied filed and get the data as per the client's business requirements.

Below is the sample REST API from the MTX framework

 `http://<MINTS-HOST>:<MINTS-PORT>/xml/service/generate/output?mapName={PurchaseOrder}&projectPath={Products}&cacheEnabled=0&flag=false`

## 2.Authorization API
In this MINTS product, all the services can be accessed only for the granted roles of users and granted groups, administrators,MINTS-super-users.
We are using token based authentication to acess the MINTS services.

Below is the sample Token Generation API REST API

`http://<MINTS-HOST>:<MINTS-PORT>/AuthService/VerifyToken`


## 3.Signature Generation API
Signature Generation API is used to generate the signature using users PRIVATE_KEY which can access the REST services in the MINTS.

Below is the sample Token Generation API REST API

`http://<MINTS-HOST>:<MINTS-PORT>/AuthService/GenerateToken`

## 4.Integration Testing API
MINTS Integration Testing API is used to test all the integrations which are created by users. This API automated integration testing where we can simply create the test cases in step by step process to perform integration testing and this API will provide the detailed test results report.

Below is the sameple Integration Testing API

`http://<MINTS-HOST>:<PORT>/Testcases?FeatureFileName=<YOUR_FEATURE_FILE_NAME>.feature&featureId=<YOUR_FEATURE_ID>`

## 5.REST-ENTRY API:
REST-ENTRY API will be able to access specific integrations based on the keys with  single REST call and get the response of your integrations.

Below is the sample REST-ENTRY API

`http://<MINTS-HOST>:<PORT>/MINTS-APP/<INTEGRATION-ID>`

## Service Invoker:
In MINTS Service Invoker API used to invoke the any REST service and performs user defined operations and sends the REST response to the destinations.

## Data Mapper:
Data Mapper API is used to map the fields in the OUTPUT based on the INPUT and META-DATA provided by the user.
It will update the values at specific target path in the OUTPUT fetching from the data store using key: value pair combinations.

Below is the sample DATA Mapper API

`http://<MINTS-HOST>:<PORT>/processPayload`


