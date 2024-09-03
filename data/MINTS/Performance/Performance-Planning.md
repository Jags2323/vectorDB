
**Why we required performance testing for application?**

Performance testing is a type of testing performed to check how the application performs under workload in **terms of responsiveness and stability.**

The Performance Test goal is to identify and **remove performance bottlenecks from an application**.
This test is mainly performed to check whether the software meets the expected requirements for **application speed, scalability, and stability**. 

In the **Mints performance testing framework** LOAD test plays a key role to test the application performance. Load Testing is a type of performance test where the application is tested for its performance on normal and peak usage. The performance of an application is checked with respect to its response to the user request and its ability to respond consistently within an accepted tolerance on **different user loads**.

In the MINTS testing framework performance tests can be done with multiple applications such as **AMQ, WMQ,** etc… So, we can able to estimate the **TPS (Transaction Per Second)** score for the application. 

The TPS score will help to estimate the **source or target application performance**. This performance test is also called as **BENCHMARK test**.


**Complete the following steps to get started:**

1.	Log on to MINTS and click on the **Designer tab** and select **Test Case Designer** after you will redirect to the **MINTS Integration testing framework module**.
2.	Now need to add the source and target connections by clicking on Add Connection and need to select the connection type AMQ, WMQ based on the connection type need to provide connection configuration details such as **Connection name, HOST, PORT, Channel, Username, Password, Queue manager** etc…
3.	A new performance test can be added by clicking the **Add** button and specifying the performance test details such **Country Name, Scenario Id, Integration ID** details etc… After you will redirect to your performance test project.
4.	A test case can be added by clicking on **Add Test Case** button. Provide the test case name. Now you will need to add test case steps by clicking on **Add Step**. Select the appropriate performance step action based on your requirement such as **LOAD TEST**, etc… After selecting the action select the source connection and provide the **source queue name [INLET]**. Choose the test file from the GIT storage directory and also provide the **target queue name [OUTLET]**.
5.	Select the Input load such as **1k,2k,3k,4k…….5M** and click on save button to save the performance test case.
6.	Test case execution can be done by clicking on the **Initiate Test** button. Now you will able to see your test cases which you are configured earlier.
7.	Select the checkbox on test case to test the performance load.
8.	Click on the **test button** to execute the test cases. Now you will be able to see some processing state for your test case wait until the performance tests completes.
9.	After performance test executed in MINTS Testing framework. It will provide the **performance results report with TPS score**.
10.	Below is sample result report format of performance testing

| Performance Results |                                   |
|---------------------|-----------------------------------|
| Start time          | Test Starting time (HH:MM:SS)     |
| Endtime             | Test Ending time (HH:MM:SS)       |
| Duration            | Total Duration of time (HH:MM:SS) |
| Load Applied        | Total load applied (1k/10k,100k..etc)  |
| Overall TPS Score   | TPS score                         |
