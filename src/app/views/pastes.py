"""
    URL shortener views for text pastes urls.
"""
from flask import Blueprint, request
import pydantic

from app.services.api.errors import ApiErrorException, ApiErrorCode
from app.services.api.response import api_success
from app.serializers.url import serialize_url
from app.services.request.auth import try_query_auth_data_from_request
from app.services.url import is_accessed_to_stats
from app.database import db, crud


bp_pastes = Blueprint("pastes", __name__)


@bp_pastes.route("/", methods=["POST", "GET"])
def pastes_index():
    """
    Pastes index resource.
    Methods:
        POST - Creates paste url and return created url object
        GET - List all urls
    """

    if request.method == "POST":
        if request.is_json:
            text = request.get_json().get("text", "")
        else:
            text = request.form.get("text", "")

        if len(text) < 10:
            raise ApiErrorException(ApiErrorCode.API_INVALID_REQUEST, "Paste text must be at least 10 characters length!")

        stats_is_public = request.form.get(
            "stats_is_public", False, type=lambda i: pydantic.parse_obj_as(bool, i)
        )

        is_authorized, auth_data = try_query_auth_data_from_request(db=db)
        if is_authorized and auth_data:
            owner_id = auth_data.user_id
        else:
            owner_id = None

        url = crud.paste_url.create_url(
            db=db,
            content=text,
            stats_is_public=stats_is_public,
            owner_id=owner_id,
        )

        include_stats = is_accessed_to_stats(url=url, owner_id=owner_id)
        return api_success(serialize_url(url, include_stats=include_stats))

