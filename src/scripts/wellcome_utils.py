"""
Utils for Accessing the Wellcome API.

This file contains python implementations of the Wellcome Catalogue API (v2).
This API is documented here: https://developers.wellcomecollection.org/api/catalogue

"""

# from typing import Optional
import requests

BASE_URL = "https://api.wellcomecollection.org/catalogue/v2/"


def fetch_works(
    query: str = None,
    include: str = None,
    items_locations_locationType: str = None,
    workType: str = None,
    type: str = None,
    aggregations: str = None,
    languages: str = None,
    genres_label: str = None,
    genres: str = None,
    subjects_label: str = None,
    subjects: str = None,
    contributors_agent_label: str = None,
    contributors_agent: str = None,
    identifiers: str = None,
    items: str = None,
    items_identifiers: str = None,
    partOf: str = None,
    partOf_title: str = None,
    availabilities: str = None,
    items_locations_accessConditions_status: str = None,
    items_locations_license: str = None,
    sort: str = None,
    sortOrder: str = None,
    production_dates_from: str = None,
    production_dates_to: str = None,
    page: int = 1,
    pageSize: int = 10,
) -> dict:
    """
    Fetches a paginated list of works from the Wellcome Collection API, with optional filters and query parameters.

    Parameters
    ----------
    query : str, optional
        Full-text search query.
    include : str, optional
        Comma-separated list of extra fields to include in the response.
    items_locations_locationType : str, optional
        Filter by the location type of items.
    workType : str, optional
        Filter by the format of the works.
    type : str, optional
        Filter by the type of works ("Collection", "Series", "Section").
    aggregations : str, optional
        Aggregated data to include in the response.
    languages : str, optional
        Filter by language code (e.g., "eng" for English).
    genres_label : str, optional
        Filter works by genre label.
    genres : str, optional
        Filter works by canonical genre concept IDs.
    subjects_label : str, optional
        Filter works by subject label.
    subjects : str, optional
        Filter works by canonical subject concept IDs.
    contributors_agent_label : str, optional
        Filter works by contributor label.
    contributors_agent : str, optional
        Filter works by canonical contributor concept IDs.
    identifiers : str, optional
        Filter by identifiers.
    items : str, optional
        Filter by item canonical IDs.
    items_identifiers : str, optional
        Filter by item identifiers.
    partOf : str, optional
        Filter by partOf relation.
    partOf_title : str, optional
        Filter by title of a partOf relation.
    availabilities : str, optional
        Filter by availability.
    items_locations_accessConditions_status : str, optional
        Filter by access status (e.g., "open", "restricted").
    items_locations_license : str, optional
        Filter by license (e.g., "cc-by", "pdm").
    sort : str, optional
        Field to sort results by (e.g., "production.dates").
    sortOrder : str, optional
        Order to sort results in ("asc" or "desc").
    production_dates_from : str, optional
        Start date for production date filter (YYYY-MM-DD).
    production_dates_to : str, optional
        End date for production date filter (YYYY-MM-DD).
    page : int, optional, default=1
        Page number to retrieve.
    pageSize : int, optional, default=10
        Number of results per page. Must be between 1 and 100 inclusive.

    Returns
    -------
    list of dict
        A JSON-parsed dictionary containing the results, pagination metadata, and (optionally) aggregations.

    Raises
    ------
    ValueError
        If `pageSize` is not between 1 and 100 or if `page` is less than 1.
    requests.HTTPError
        If the API request fails.
    """
    if not (1 <= pageSize <= 100):
        raise ValueError(f"pageSize must be between 1 and 100, got {pageSize}")
    if page < 1:
        raise ValueError(f"page must be >= 1, got {page}")

    params = {
        "query": query,
        "include": include,
        "items.locations.locationType": items_locations_locationType,
        "workType": workType,
        "type": type,
        "aggregations": aggregations,
        "languages": languages,
        "genres.label": genres_label,
        "genres": genres,
        "subjects.label": subjects_label,
        "subjects": subjects,
        "contributors.agent.label": contributors_agent_label,
        "contributors.agent": contributors_agent,
        "identifiers": identifiers,
        "items": items,
        "items.identifiers": items_identifiers,
        "partOf": partOf,
        "partOf.title": partOf_title,
        "availabilities": availabilities,
        "items.locations.accessConditions.status": items_locations_accessConditions_status,
        "items.locations.license": items_locations_license,
        "sort": sort,
        "sortOrder": sortOrder,
        "production.dates.from": production_dates_from,
        "production.dates.to": production_dates_to,
        "page": page,
        "pageSize": pageSize,
    }

    # Remove keys with None values
    params = {k: v for k, v in params.items() if v is not None}

    response = requests.get(BASE_URL + "works", params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_specific_work(work_id: str, include: str = None) -> dict:
    """
    Returns a single work by the `id` of the work from the Wellcome Collection

    Parameters
    ----------
    work_id : str
        The id of the fetched work
    include : str, optional
        Enum: "identifiers" "items" "holdings" "subjects" "genres" "contributors" "production" "languages" "notes" "images" "succeededBy" "precededBy" "partOf" "parts"
        A comma-separated list of extra fields to include
    """
    params = {"include": include}
    response = requests.get(
        BASE_URL + "works/" + f"{work_id}", params=params, timeout=10
    )

    response.raise_for_status()
    return response.json()
