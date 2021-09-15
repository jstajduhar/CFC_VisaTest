# CFC_VisaTest
This repo is meant to hold files related to Visa API testing and integration for the Code for Charlottesville Credit Score Management project.

Visa Developer Account

  If you want to create your own project for testing the Visa API, you first need to sign up for a Visa Developer account

    https://developer.visa.com/

Create Project 

  After creating an account, you can create a project from your account dashboard.  This link walks you through the process.
    
    https://developer.visa.com/pages/working-with-visa-apis/create-project

  When creating a project you will have to create keys for authentication. This code has initially used the mutual authentication option.  You will get a user_id and password and be able to download cert and key PEM files.
	
  You can also add APIs during project creation.  This code used the FundsTransferAPI.  Much of the sample code in this repo was pulled from the FundsTransferAPI sample code.
	
Mutual Authentication Test

  The /hello_world/mutual_auth directory tests mutual authentication.  The Jupyter Notebook runs the helloworld.py Python file which reaches out and hits the Visa sandbox.  The helloworld.py file needs to be updated to contain a real user_id and password and also paths to valid cert and key PEM files.

Funds Transfer Test

  In the main directory, the CFC_Test.py files contains methods that reach out the the Visa API sandbox to makes pull and push funds transfer requests.  The POST methods actually perform the transfers, the GET methods provide status.  Canned values are used that are accepted by the sandbox.  The CFC_FundsTransferTest.ipynb Notebook has commands to import CFC_Test and run each of the 4 funds transfer methods.
	
  The CFC_FundsTransferTest.ipynb also contains commands to try to setup and run all of the test files that came out of the box with the Visa sample code.  These are not currently working.  It could be due to permissions restrictions in the Code for Charlottesville environment or issues with restructuring the directories.
 
API Test

  This directory is intended to teste hosting an API from the CFC JupyterHub environment using Kernel Gateway.  The API can be launched but is currently just accessible internally.  This is the site I used as a guide:
  
    https://ndres.me/post/jupyter-notebook-rest-api/
    
  After editing the Kernel Gateway config I used this command in a terminal to start the notebook API:
  
    jupyter kernelgateway --KernelGatewayApp.api='kernel_gateway.notebook_http' --KernelGatewayApp.seed_uri='CFC_VisaTest/API_test/API_Endpoint_Test.ipynb'
  
  

