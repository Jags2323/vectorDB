In general, every application has some resource configurations. Some of the applications will provide the less results due to lack of resources or **lack of resource planning strategies**. 

The **MINTS Infra Estimate application** will provide the exact configuration based on the application behavior. It’s also predicted the expected resources in the **cluster** such as **Memory CPU, Nodes, Storage devices** based on the expected **TPS (Transaction per second).**

The advantages of using the **MINTS Infra Estimate application** are used provides the exact configuration and provide stability to the applications. It also provides **cost-saving** to the customers who are planning to perform **Infrastructure as a Service configuration(IaaS)**.


**Complete the following steps to get started:**
1.	Log on to MINTS and click on the tab **MINTS Infra Estimate** after you will redirect to the MINTS Infra Estimate tab.
2.	In this Mints Infra estimate page, you will be able to get the Cluster Spec by providing the expected **TPS (Transactions per second)**. On this page, users need to select the Cloud vendor such as **Azure, AWS, GCP, IBM.**
3.	Now you can bale to select the Load properties such as the **Pattern, Protocol, Msg Size, Msg Volume Pattern Count**. Below is one of the examples of Load properties. 

**Example 1:**

| Pattern               | Protocol           | Msg Size    | Msg Volume | Pattern Count |
|-----------------------|--------------------|-------------|------------|---------------|
| Simple/Medium/complex | AMQ/WMQ/Kafka/REST | 1kb to 10MB | 100K to 5M | 10            |

4. Now you can provide the expected TPS score and click on the Go button to get the cluster specification based on your TPS.
5. Below is the sample example cluster specs.

**Cluster Specification's**

**Example 2:**

| Primary Services(1 Node) |        |         |
|---------------------------|--------|---------|
| CPU                       | Memory | Storage |
| 2 Cores                   | 8 GB   | 1TB     |

| Secondary Services (1 Node) |        |         |
|------------------------------|--------|---------|
| CPU                          | Memory | Storage |
| 2 Cores                      | 8 GB   | 500 GB  |
