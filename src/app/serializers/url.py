"""
    Serializers for url model.
"""
from typing import Any

from flask import url_for

from app.database.models.url import RedirectUrl, PasteUrl
from app.database.mixins import UrlMixin


def serialize_url(
    url: UrlMixin, *, include_stats=False, in_list: bool = False
) -> dict[str, Any]:
    """
    Serializes url object to dict for the response.
    """
    serialized_url = {
        "id": url.id,
        "hash": url.hash,
        "redirect_url": None,
        "text": None,
        "expires_at": url.expiration_date.timestamp(),
        "stats_is_public": url.stats_is_public,
        "is_deleted": url.is_deleted,
        "_links": {
            "qr": {
                "href": url_for(
                    "urls.generate_qr_code_for_url",
                    url_hash=url.hash,
                    _external=True,
                    _scheme="https",
                )
            },
        },
    }
    if isinstance(url, RedirectUrl):
        serialized_url["redirect_url"] = url.redirect
        serialized_url.pop("text")
    if isinstance(url, PasteUrl):
        serialized_url["text"] = url.content
        serialized_url.pop("redirect_url")

    if include_stats:
        serialized_url["_links"]["stats"] = {
            "href": url_for(
                "urls.short_url_stats",
                url_hash=url.hash,
                _external=True,
                _scheme="https",
            )
        }

    if in_list:
        return serialized_url
    if isinstance(url, RedirectUrl):
        return {"url": serialized_url}
    if isinstance(url, PasteUrl):
        return {"paste": serialized_url}


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
