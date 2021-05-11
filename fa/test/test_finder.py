"""
Tests module
"""

from unittest import mock
import pytest
from fa.containers import Container

@pytest.fixture
def container():
    container = Container()
    container.config.from_dict({
        'finder': {
            'type': 'csv',
            'csv': {
                'path': '/fake-movies.csv',
                'delimiter': ',',
            },
            'sqlite': {
                'path': '/fake-movies.db',
            },
        },
    })
    return container

def test_flights_depart_from(container):
    finder_mock = mock.Mock()
    finder_mock.find_all.return_value = [
        container.flight('xyz', 'KIAH', 'KAUS'),
        container.flight('123', 'KHOU', 'KEFD'),
    ]

    with container.finder.override(finder_mock):
        lister = container.lister()
        flights = lister.flights_depart_from('KIAH')

    assert len(flights) == 1
    assert flights[0].flight_id == 'xyz'

def test_movies_released_in(container):
    finder_mock = mock.Mock()
    finder_mock.find_all.return_value = [
        container.flight('xyz', 'KIAH', 'KAUS'),
        container.flight('123', 'KHOU', 'KEFD'),
    ]

    with container.finder.override(finder_mock):
        lister = container.lister()
        flights = lister.flights_arrive_at('KEFD')

    assert len(flights) == 1
    assert flights[0].flight_id == '123'
