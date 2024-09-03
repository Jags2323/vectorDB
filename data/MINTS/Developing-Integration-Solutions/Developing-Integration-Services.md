# Developing Integration Services

**MINTS App** will Connect Enterprise provides a **flexible environment** in which you can develop **integrated solutions** to **transform, enrich, route**, and process your business messages and data. You can integrate client applications that use different protocols and different message formats.

In MINTS App will connect the Enterprise, you develop an **integration solution** by using a MINTS integration service application.

MINTS integration service is the container for the resources that you develop to **process your business messages and data**. MINTS App connect Enterprise manages three sets of resources to **integrate your applications, messages, and data**.

In MINTS integration service message flow is a **sequence of processing steps** that run in an integration service when an input message is received from the target. An integration will perform a **set of execution processes** that host one or more message flows to **route**, **transform**, and **enrich in-flight messages**.

**Complete the following steps to develop an Integration:**
1.	Log on to MINTS Integration Service.
2.	Click on the **create button** to create an Integration with **Source** system and **Destination** system.
3.	Enter the Integration details such as** Integration Name, Source (AMQ), Destination (WMQ), Keys, Integration description**.
4.	After you provided the basic Integration details. Click on the continue button to proceed further.
5.	Select the **categories** such as **Basic, Transformations, File I/O, FTP, etc…** in the template section.
6.	After selecting the category. Select the required pattern based on your requirement such as **INLET > OUTLET, INLET>PGP Security>Outlet,**, etc…

7.	Provide the properties in the properties section such as Source queue name, Encoding, Thread Count, Target queue name. Click on the continue button to proceed further.
8.	Now you will see the all properties of your Integration.
9.	Click on save to save the Integration. After that, You will get the message as integration saved successfully with **Integration Id ex:(I0007)**. Click on **publish integration button** to publish the integration in MINTS App.
10.	After publishing the integration service. MINTS XML route will build and save in the MINTS integration folder with the file name ex: **I0007.xml**
11.	Here is the sample **MINTS XML route** 

## Simple Route

`<route id="I0001">
<from uri="CustomerInteract:queue:INLET?selector=MINTID%3D'I0001'" />
		<to uri="audit:Inlet?level=info" />
		<to uri="CustomerInteract:queue:OUTLET" />
		<to uri="audit:Outlet?level=info" />
</route>`


## MINTS Transformation Architecture

![AltText](images/TransformationArch.png)
