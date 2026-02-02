"""
Blue Button OAuth Provider for FastMCP.

Implements OAuth 2.0 Authorization Code flow with PKCE as required by CMS Blue Button API.
"""
import os
from fastmcp.server.auth import OAuthProxy
from fastmcp.server.auth.providers.introspection import IntrospectionTokenVerifier


def create_bluebutton_auth():
    """
    Create a Blue Button OAuth provider for FastMCP.

    Required environment variables:
        BLUEBUTTON_CLIENT_ID: Your registered application client ID
        BLUEBUTTON_CLIENT_SECRET: Your application client secret
        BLUEBUTTON_BASE_URL: Your MCP server's base URL (for callbacks)
        BLUEBUTTON_SANDBOX: Set to "false" for production (default: true)
    """
    is_sandbox = os.getenv("BLUEBUTTON_SANDBOX", "true").lower() == "true"

    if is_sandbox:
        base = "https://sandbox.bluebutton.cms.gov"
    else:
        base = "https://api.bluebutton.cms.gov"

    client_id = os.environ["BLUEBUTTON_CLIENT_ID"]
    client_secret = os.environ["BLUEBUTTON_CLIENT_SECRET"]
    base_url = os.environ["BLUEBUTTON_BASE_URL"]

    # Token verifier using OAuth 2.0 introspection
    token_verifier = IntrospectionTokenVerifier(
        introspection_url=f"{base}/v2/o/introspect/",
        client_id=client_id,
        client_secret=client_secret,
        base_url=base_url,
    )

    return OAuthProxy(
        # Upstream Blue Button OAuth endpoints
        upstream_authorization_endpoint=f"{base}/v2/o/authorize/",
        upstream_token_endpoint=f"{base}/v2/o/token/",
        upstream_client_id=client_id,
        upstream_client_secret=client_secret,

        # Token validation
        token_verifier=token_verifier,

        # Your MCP server's public URL (where OAuth callbacks will be received)
        base_url=base_url,

        # Blue Button FHIR scopes
        valid_scopes=[
            "openid",
            "profile",
            "patient/Patient.rs",
            "patient/Coverage.rs",
            "patient/ExplanationOfBenefit.rs",
        ],

        # Forward PKCE to upstream (Blue Button requires PKCE)
        forward_pkce=True,
    )
