**What is MTX :**
MTX Transformation Extender is a powerful, transaction oriented, data integration solution that automates the transformation of high volume complex transactions with functions and no need for hand-coding.

**Architecture:**
REST APIs – To support cloud and web services implementations, all MTX  functions can now be called through REST (Representational State Transfer) APIs. REST APIs allow you to control and configure systems remotely, and deploy artifacts seamlessly across the architecture.
![MapsUsingMTX](images/MapsUsingMTX.png)
**Data supports:**
MTX supporting many types of data, with native support for JSON, XML or any proprietary data format.

**File Manager Structure:**
MTX provides an easy-to-use browser-based development environment and supports centralized team-based collaboration. The integrated design platform makes it easy for your team to create data flows of any complexity, and to deploy these to a runtime server.

**Technology stack:**
MTX framework enables the cutting edge technologies like Java 8, spring boot..

**Build Tool:**
MTX framework was build the artifact using with Maven build tool.

**Deployment:**
MTX using Azure Kubernetes Service (AKS) offers serverless Kubernetes, an integrated continuous integration and continuous delivery (CI/CD) experience and enterprise-grade security and governance. Unite your development and operations teams on a single platform to rapidly build, deliver and scale applications with confidence.

**How MTX Works :**
MTX produces the two services, those are below.
1. Transformation the data using with inputs files.

**EndPoint:**
http://localhost:8080/xml/service/generate/output?mapName={PurchaseOrder}&projectPath={Products}&cacheEnabled=0&flag=false

**Arguments:** mapName paramater is should mandatory and mapname is PurchaseOrder.xml and projectPath paramater is mandatory ,its indicates the directory, flag paramater is either false or true.if true then MTX framewor  build and java classes files and compiled, if false then no need to generate the java class files.
Inorder to mapper file  having XSD inputdefinition , XSD outputdefinition and inoutformat as like below.

       <configuration>
			<inoutformat>{xml2xml}</inoutformat>
			<inputdefinition>{input.orders.xsd}</inputdefinition>
			<outputdefinition>{output.orders.xsd}</outputdefinition>
	</configuration>

**HTTP Method:** POST

**Body:**



2. Rebuilding the Java classes file if any changes in Inputs.







