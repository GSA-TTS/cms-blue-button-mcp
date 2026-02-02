import httpx

BASE_URL = "https://sandbox.bluebutton.cms.gov/v2/fhir"


def register_tools(mcp):

    @mcp.tool()
    async def get_fhir_capability_statement() -> dict:
        """Get the FHIR CapabilityStatement from the CMS Blue Button API."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/metadata",
                headers={"Accept": "application/fhir+json"},
            )
            response.raise_for_status()
            return response.json()