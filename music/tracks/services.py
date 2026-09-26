"""Service-layer operations for track browsing."""

from dataclasses import dataclass
from math import ceil

from music.adapters.repository import AbstractRepository
from music.domainmodel.track import Track


TRACKS_PER_PAGE = 20


@dataclass(frozen=True)
class BrowsePage:
    """Tracks and navigation metadata for one browse page."""

    tracks: list[Track]
    current_page: int
    total_pages: int

    @property
    def has_previous(self) -> bool:
        return self.current_page > 1

    @property
    def has_next(self) -> bool:
        return self.current_page < self.total_pages


def get_tracks_for_browse(
        repository: AbstractRepository,
        limit: int = 20,
) -> list[Track]:
    """Return the first ``limit`` tracks in title order.

    The repository owns data access. This service owns browse-specific
    processing, including sorting and the prototype's fixed result limit.
    """
    tracks = repository.get_all_tracks()
    ordered_tracks = sorted(
        tracks,
        key=lambda track: (track.title.casefold(), track.track_id),
    )
    return ordered_tracks[:limit]


def get_browse_page(
        repository: AbstractRepository,
        requested_page: int,
        per_page: int = TRACKS_PER_PAGE,
) -> BrowsePage:
    """Return one safe page of tracks in a consistent title order.

    Invalid page numbers are treated as page 1. Page numbers beyond the
    available range are clamped to the final page so the route never fails or
    produces an empty page merely because the requested number is too large.
    """
    if per_page < 1:
        raise ValueError("per_page must be at least 1")

    tracks = repository.get_all_tracks()
    ordered_tracks = sorted(
        tracks,
        key=lambda track: (track.title.casefold(), track.track_id),
    )

    total_pages = max(1, ceil(len(ordered_tracks) / per_page))

    if not isinstance(requested_page, int) or isinstance(requested_page, bool):
        current_page = 1
    else:
        current_page = min(max(requested_page, 1), total_pages)

    start_index = (current_page - 1) * per_page
    page_tracks = ordered_tracks[start_index:start_index + per_page]

    return BrowsePage(
        tracks=page_tracks,
        current_page=current_page,
        total_pages=total_pages,
    )


def get_track(track_id: int, repository: AbstractRepository) -> Track | None:
    # Return a track by ID, or None if it does not exist.
    return repository.get_track(track_id)

def search_tracks(query: str,criterion: str,repository: AbstractRepository,) -> list[Track]:
    # Return tracks matching the search query
    valid_criteria = {"title", "artist", "album", "genre"}

    if criterion not in valid_criteria:
        return []
    # reject empty string because it is in anything
    if len(query.strip()) == 0:
        return []

    return repository.search_tracks(query.strip(), criterion)

def get_search_page( query: str,criterion: str,repository: AbstractRepository,requested_page: int,per_page: int = TRACKS_PER_PAGE):
    # return one page of tracks matching the search query, with pagination
    tracks = search_tracks(query, criterion, repository)
    total_tracks = len(tracks)

    if total_tracks == 0:
        total_pages = 1
    else:
        total_pages = (total_tracks + per_page - 1) // per_page

    if requested_page < 1:
        current_page = 1
    elif requested_page > total_pages:
        current_page = total_pages
    else:
        current_page = requested_page

    start_index = (current_page - 1) * per_page
    end_index = start_index + per_page

    page_tracks = tracks[start_index:end_index]

    has_previous = current_page > 1
    has_next = current_page < total_pages

    return page_tracks,current_page,total_pages,has_previous,has_next