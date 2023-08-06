"""
Conftest module.

This module contains pytest fixtures.
"""
import datetime

import pytest


@pytest.fixture(scope="session")
def comic_list_response():
    """Comic list response fixture."""
    return {
        "comics": [
            {
                "publisher": "IMAGE COMICS",
                "description": '"LEGACY," Part Five-The third arc of the Eisner Award-winning BITTER ROOT comes to an epic conclusion that will decide the fate of humanity. For the Sangerye family, it means making another sacrifice while searching for hope during hopeless times.',  # noqa : E501
                "title": "BITTER ROOT #15 CVR A GREENE (MR)",
                "price": "$3.99",
                "creators": "(W) David Walker, Chuck Brown (A/CA) Sanford Greene",
                "release_date": "2021-08-11",
                "diamond_id": "MAY210139",
            },
            {
                "publisher": "IMAGE COMICS",
                "description": '"LEGACY," Part Five-The third arc of the Eisner Award-winning BITTER ROOT comes to an epic conclusion that will decide the fate of humanity. For the Sangerye family, it means making another sacrifice while searching for hope during hopeless times.',  # noqa : E501
                "title": "BITTER ROOT #15 CVR B CONLEY CURIEL (MR)",
                "price": "$3.99",
                "creators": "(W) David Walker, Chuck Brown (A) Sanford Greene (CA) Chase Conley, Charissa Curiel",  # noqa : E501
                "release_date": "2021-08-11",
                "diamond_id": "MAY210140",
            },
            {
                "publisher": "MARVEL COMICS",
                "description": "A NEW DAREDEVIL RISES TO PROTECT HELL'S KITCHEN! Matt Murdock is a killer - but while he's serving his time as the masked vigilante called Daredevil, Hell's Kitchen has suddenly been left without a guardian devil. Or it was, until ELEKTRA NATCHIOS took it upon herself to protect Murdock's neighborhood and his legacy as the NEW DAREDEVIL! But she's already got her work cut out for her: WILSON FISK remains seated as New York's mayor, with TYPHOID MARY, THE OWL, HAMMERHEAD and other lethal - and FAMILIAR - foes at his beck and call...  Rated T+",  # noqa : E501
                "title": "DAREDEVIL #1 HALLOWEEN COMIC EXTRAVAGANZA 2021",
                "price": "$PI",
                "creators": "(W) Chip Zdarsky (A/CA) Marco Checchetto",
                "release_date": "2021-10-20",
                "diamond_id": "JUL219364",
            },
        ]
    }


@pytest.fixture(scope="session")
def sb_dates_response():
    """Fixture of date strings."""
    return {
        "dates": [
            "2021-07-29.",
            "2021-08-04",
            "2021-08-11",
            "2021-08-18",
            "2021-08-25",
        ]
    }


@pytest.fixture(scope="session")
def sb_cleaned_dates():
    """Fixture of date objects."""
    return [
        datetime.date(2021, 8, 4),
        datetime.date(2021, 8, 11),
        datetime.date(2021, 8, 18),
        datetime.date(2021, 8, 25),
    ]
