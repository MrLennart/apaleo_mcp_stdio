# requirements: requests fastmcp
from mcp.server.fastmcp import FastMCP
import base64
import requests
import os
from typing import List

# Instantiates an MCP server client
mcp = FastMCP("Apaleo")

#Generates a request token
def token():
    creds=os.getenv("APALEO_CREDENTIALS").encode("ascii")
    creds=base64.b64encode(creds)
    creds=creds.decode("ascii")
    headers = {
        "Authorization": f"Basic {creds}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    params = {"grant_type": "client_credentials"}
    response = requests.post("https://identity.apaleo.com/connect/token", data=params, headers=headers)
    token = response.json()['access_token']
    authorization = f'Bearer {token}'
    return authorization 

#HTTP Get Request
def get(content):
    authorization = token()
    headers = {"Authorization": authorization}
    response = requests.get(content, headers=headers)

    try:
        return response.json()
    except Exception as e:
        return {"error": str(e), "status_code": response.status_code}
    
#HTTP Post Request 
def post(content,params):
    authorization=token()
    headers = {"Authorization": authorization}
    response = requests.post(content,json=params, headers=headers)
    try:
        return response.json()
    except Exception as e:
        return {"error": str(e), "status_code": response.status_code}



#Tools go here
@mcp.tool()
def TestTool() -> dict:
    """gives back important information"""
    result = get('https://api.apaleo.com/inventory/v1/properties')
    r={"tool_use_id": "TestTool", "result": {"Information":"The Test has worked"}}
    return r


@mcp.tool()
async def InventoryPropertiesGet(pageNumber:int=1,pageSize:int=10) -> dict:
    """Get a properties list 
"""
    result = get("https://api.apaleo.com/inventory/v1/properties?pageNumber={pageNumber}}&pageSize={pageSize}}}") 
    return {'tool_use_id': 'InventoryPropertiesGet', 'result': result}

@mcp.tool()
async def InventoryProperties_countGet() -> dict:
    """Return total count of properties 

"""
    result = get("https://api.apaleo.com/inventory/v1/properties/$count") 
    return {'tool_use_id': 'InventoryProperties_countGet', 'result': result}


@mcp.tool()
async def InventoryTypesCountriesGet() -> dict:
    """Returns a list of supported countries. 

"""
    result = get("https://api.apaleo.com/inventory/v1/types/countries") 
    return {'tool_use_id': 'InventoryTypesCountriesGet', 'result': result}



#Starts the server
if __name__ == "__main__":
    mcp.run(transport="stdio")