"""Test urls.py"""
from backend.config import FRONTEND_ENDPOINT
from backend.urls import agreement_confirmed_url, tenant_signing_url
from backend.utils import generate_uuid


def test_tenant_signing_url() -> None:
    """Test tenant_signing_url."""
    aggreement_id = generate_uuid()
    tenant_id = generate_uuid()
    assert (
        tenant_signing_url(aggreement_id, tenant_id)
        == f"{FRONTEND_ENDPOINT}/sign-agreement/{aggreement_id}/tenant/{tenant_id}"
    )


def test_agreement_confirmed_url() -> None:
    """Test agreement_confirmed_url."""
    aggreement_id = generate_uuid()
    assert (
        agreement_confirmed_url(aggreement_id)
        == f"{FRONTEND_ENDPOINT}/agreement-confirmed/{aggreement_id}"
    )
