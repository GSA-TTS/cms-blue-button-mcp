import httpx
from fastmcp.server.dependencies import get_access_token
from fastmcp.server.auth import AccessToken

BASE_URL = "https://sandbox.bluebutton.cms.gov/v2/"


def register_tools(mcp):

    @mcp.tool()
    async def get_fhir_capability_statement() -> dict:
        """Get the FHIR CapabilityStatement from the CMS Blue Button API."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}fhir/metadata",
                headers={"Accept": "application/fhir+json"},
            )
            response.raise_for_status()
            return response.json()

    @mcp.tool()
    async def get_user_info() -> dict:
        """
        Get information about the authenticated Medicare beneficiary.

        Returns user profile data including name and FHIR patient ID.
        Requires the user to have completed OAuth authorization.
        """
        token: AccessToken | None = get_access_token()
        if token is None:
            raise ValueError("Not authenticated. Please complete OAuth authorization first.")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}connect/userinfo",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {token.token}",
                },
            )
            response.raise_for_status()
            return response.json()