"""
ComicsList module.

This module provides the following classes:

- ComicsList
"""
from marshmallow import ValidationError

from serifan import comic, exceptions


class ComicsList:
    """The ComicsList object contains a list of `Comic` objects."""

    def __init__(self, response):
        """Initialize a new ComicsList."""
        self.comics = []

        schema = comic.ComicSchema()
        for issue_dict in response["comics"]:
            try:
                result = schema.load(issue_dict)
            except ValidationError as error:
                raise exceptions.ApiError(error)

            self.comics.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.comics)

    def __len__(self):
        """Return the length of the object."""
        return len(self.comics)

    def __getitem__(self, index: int):
        """Return the object of a at index."""
        return self.comics[index]
