# KYD

It is important to be clear about your processing requirements, and to understand what you want MINTS to do for your business.

In a typical IT environment there are many interacting components, each with a role to play, and it is important that you are able to clearly define the role of MINTS in the broader environment. A key design decision is how much business logic to implement within your Integrations. MINTS enables you to implement large amounts of processing within an Integration, and implementations can vary significantly from the simple routing of messages to complex validation and transformation. Some implementations also read data from a database and use that data to populate messages. Regardless of the amount of function that you decide to implement in a Integration, it is important to have clear boundaries between pieces of application processing.

Several different processing styles are commonly used with MINTS, and it is important to understand the ones that are most relevant to you, such as:

**Request Reply**

This is the most common type of processing, and enables two applications to communicate, even if they use different data formats. For example, an Integration transforms a request message from Application 1 into a format that Application 2 can understand. The output of the first Integration is then sent to Application 2, which processes the request and issues a reply. The reply is processed in a second Integration, which converts the response message into a format that Application 1 can understand.

**Aggregation**

This type of processing is often used to invoke one or more back-end systems and coordinate replies. It is a more complex form of a Request Reply case, in which all the replies from the intermediate applications must be collected together before the reply message for the original request can be sent. For example, this type of processing could be used to book a holiday, in which a flight, hotel, and a car are required, and all must be successfully processed before the holiday confirmation can be sent.

**Routing**

Routing is used to redirect messages, and one or more copies of a message can be sent to one or more destinations.

**Transformation**

This type of processing involves the use of one or more transformation technologies such as MINTS MTX, IBM ITX, XSLT Nodelets. In this type of processing the input message is processed according to some business rules, and there might also be a change of message format or protocol.

**File processing**

The use of files is one of the most common methods of storing data. You can create Integrations to process data in files, accepting data in files as input message data, and producing output message data for file-based destinations.

**Database handling**

You can configure your Integrations to access and manipulate business data in databases.

**REST services**

MINTS Service Hub can be used as both a consumer and provider of services. You can publish and subscribe the services and manage the services using MINTS Service Hub.

**Transport switching**

You can use this type of processing to switch between transports such as HTTP and JMS.
