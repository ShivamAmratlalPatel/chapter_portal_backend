"""URLs for the backend"""
from urllib.parse import urljoin
from uuid import UUID

from backend.config import FRONTEND_ENDPOINT


def tenant_signing_url(agreement_id: UUID, tenant_id: UUID) -> str:
    """Get the URL for the tenant to sign the agreement"""
    return urljoin(
        FRONTEND_ENDPOINT,
        f"/sign-agreement/{agreement_id}/tenant/{tenant_id}",
    )


def agreement_confirmed_url(agreement_id: UUID) -> str:
    """Get the URL for the tenant to sign the agreement"""
    return urljoin(FRONTEND_ENDPOINT, f"/agreement-confirmed/{agreement_id}")
