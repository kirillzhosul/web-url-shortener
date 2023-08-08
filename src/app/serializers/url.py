"""
    Serializers for url model.
"""
from typing import Any

from flask import url_for, current_app

from app.database.models.url import RedirectUrl


def serialize_url(
    url: RedirectUrl, *, include_stats=False, in_list: bool = False
) -> dict[str, Any]:
    """
    Serializes url object to dict for the response.
    """
    API_SCHEME = current_app.config["API_SCHEME"]
    API_HOSTNAME = current_app.config["API_HOSTNAME"]
    QR_PATH = url_for("urls.generate_qr_code_for_url", url_hash=url.hash)
    STATS_PATH = url_for("urls.short_url_stats", url_hash=url.hash)

    serialized_url = {
        "id": url.id,
        "redirect_url": url.redirect,
        "hash": url.hash,
        "expires_at": url.expiration_date.timestamp(),
        "is_expired": url.is_expired(),
        "stats_is_public": url.stats_is_public,
        "is_deleted": url.is_deleted,
        "_links": {
            "qr": {
                "href": f"{API_SCHEME}://{API_HOSTNAME}{QR_PATH}",
            },
        },
    }

    if include_stats:
        serialized_url["_links"]["stats"] = {
            "href": f"{API_SCHEME}://{API_HOSTNAME}{STATS_PATH}"
        }

    if in_list:
        return serialized_url

    return {"url": serialized_url}


def serialize_urls(
    urls: list[RedirectUrl],
    *,
    include_stats: bool = False,
) -> dict[str, Any]:
    """
    Serializes list of urls objects to dict for the response.
    """
    return {
        "urls": [
            serialize_url(
                url,
                include_stats=include_stats,
                in_list=True,
            )
            for url in urls
        ]
    }
