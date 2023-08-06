"""
Comic module.

This module provides the following classes:

- Comic
- ComicSchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load

from .utils import is_decimal


class Comic:
    """
    The Comic object contains information for an issue.

    :param `**kwargs`: The keyword arguments is used for setting comic data.
    """

    def __init__(self, **kwargs):
        """Intialize a new Comic."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class ComicSchema(Schema):
    """
    Schema for Comic api.

    .. versionchanged:: 1.0.0
        Changed ``price`` field to a ``Decimal`` type.
    """

    publisher = fields.Str()
    description = fields.Str()
    title = fields.Str()
    price = fields.Decimal(places=2)
    creators = fields.Str()
    release_date = fields.Date(format="%Y-%m-%d")
    diamond_id = fields.Str()

    class Meta:
        """Any unknown fields will be included."""

        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        """Strip the dollar sign from the price before loading the data."""
        new_data = data

        if "price" in new_data:
            new_data["price"] = new_data["price"].strip("$")
            if not is_decimal(new_data["price"]):
                new_data["price"] = "0.00"

        return new_data

    @post_load
    def make_object(self, data, **kwargs):
        """
        Make the comic object.

        :param data: Data from Shortboxed response.
        :return: :class:`Comic` object
        :rtype: Comic
        """
        return Comic(**data)
