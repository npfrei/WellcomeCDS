"""
Utils for Accessing the Wellcome API.

This file contains python implementations of the Wellcome Catalogue API (v2).
This API is documented here: https://developers.wellcomecollection.org/api/catalogue

"""

# from typing import Optional
import requests
from IPython.display import Image, display

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
        BASE_URL + "works/" + f"{work_id}", params=params, timeout=15
    )

    response.raise_for_status()
    return response.json()

def fetch_images(
    query: str = None,
    locations_license: str = None,
    source_contributors_agent_label: str = None,
    source_genres_label: str = None,
    source_subjects_label: str = None,
    sort: str = None,
    sortOrder: str = None,
    source_production_dates_to: str = None,
    source_production_dates_from: str = None,
    colors: str = None,
    include: str = None,
    aggregations: str = None,
    page: int = 1,
    pageSize: int = 10,
) -> dict:
    """
    Fetches a paginated list of images from the Wellcome Collection API.

    Parameters
    ----------
    query : str, optional
        Full-text search query.
    locations_license : str, optional
        License type (e.g., "cc-by", "pdm", "ogl").
    source_contributors_agent_label : str, optional
        Filter images by contributor of the source works.
    source_genres_label : str, optional
        Filter images by genre of the source works.
    source_subjects_label : str, optional
        Filter images by subjects of the source works.
    sort : str, optional
        Sort field, typically "source.production.dates".
    sortOrder : str, optional
        Sort order, either "asc" or "desc".
    source_production_dates_to : str, optional
        Upper bound date for image production (YYYY-MM-DD).
    source_production_dates_from : str, optional
        Lower bound date for image production (YYYY-MM-DD).
    colors : str, optional
        Filter images by colors.
    include : str, optional
        Comma-separated list of extra fields to include (e.g., "source.genres").
    aggregations : str, optional
        Aggregated data to include (e.g., "locations.license").
    page : int, default=1
        Page number to retrieve (>= 1).
    pageSize : int, default=10
        Number of images per page (between 1 and 100).

    Returns
    -------
    dict
        JSON response containing image data and pagination details.

    Raises
    ------
    ValueError
        If `page` is less than 1 or `pageSize` is not between 1 and 100.
    requests.HTTPError
        If the API request returns an unsuccessful status code.
    """
    if not (1 <= pageSize <= 100):
        raise ValueError(f"pageSize must be between 1 and 100, got {pageSize}")
    if page < 1:
        raise ValueError(f"page must be >= 1, got {page}")

    params = {
        "query": query,
        "locations.license": locations_license,
        "source.contributors.agent.label": source_contributors_agent_label,
        "source.genres.label": source_genres_label,
        "source.subjects.label": source_subjects_label,
        "sort": sort,
        "sortOrder": sortOrder,
        "source.production.dates.to": source_production_dates_to,
        "source.production.dates.from": source_production_dates_from,
        "colors": colors,
        "include": include,
        "aggregations": aggregations,
        "page": page,
        "pageSize": pageSize,
    }

    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}

    response = requests.get(BASE_URL + "images", params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_specific_image(image_id: str, include: str = None) -> dict:
    """
    Returns a single image by the `id` of the image from the Wellcome Collection

    Parameters
    ----------
    image_id : str
        The id of the fetched image
	string
        Enum: "visuallySimilar" "withSimilarFeatures" "withSimilarColors" "source.contributors" "source.languages" "source.genres" "source.subjects"
        A comma-separated list of extra fields to include
    """
    params = {"include": include}
    response = requests.get(
        BASE_URL + "images/" + f"{image_id}", params=params, timeout=10
    )

    response.raise_for_status()
    return response.json()


def get_full_res_url(iiif_url:str, resolution="full") -> str:
    """IIIF urls are the following format: {base}/{region}/{resolution}/{rotation}/{quality}.{format}
    example: "https://iiif.wellcomecollection.org/image/V0021817/full/300,/0/default.jpg"
             Here resolution="300,"
    Args:
        iiif_url (str): _description_
        resolution (str, optional): _description_. Defaults to "full".

    Returns:
        str: modified url to get image at expected resolution
    """
    if 'iiif' in iiif_url:
        # split the string at the fifth '/' symbol (right before resolution)
        parts = iiif_url.split('/', 5)
        # Keeps the left part
        left_part = "/".join(parts[:5]) 
        # Manually add the right part depending on expected resolution
        full_res_url = f"{left_part}/full/{resolution}/0/default.jpg"
    else:
        raise Exception("Not a valid IIIF URL.")
    return full_res_url


def display_images_on_query(query: str, nb_imgs=5, resolution="full") -> None:
    """Displays images present in the collection that contain a queried word in their title

    Args:
        query (str): a key word to query the image title on
        resolution (str, optional): the resolution at which we want to display the images. Defaults to "full".
    """
    search_url = f"{BASE_URL}/images"
    
    params = {
        "query": query,
        "pageSize": nb_imgs
    }
    
    response = requests.get(search_url, params=params)
    data = response.json()

    for work in data.get("results", []):
        title = work.get("source").get("title")
        iiif_url = work.get("thumbnail", {}).get("url")
        
        if iiif_url:
            print(title)
            print(iiif_url) # for debugging
            full_res_url = get_full_res_url(iiif_url, resolution=resolution)
            display(Image(url=full_res_url))


def fetch_iiif_images_on_query(image_id: str, include: str= None) -> None:
    """

    Args:
        image_id (str): _description_
        include (str, optional): _description_. Defaults to None.

    Returns:
        : _description_
    """
    params = {"include": include}
    # response = requests.get(
    #     BASE_URL + "images/" + f"{image_id}", params=params, timeout=10
    # )
    # return response.json()