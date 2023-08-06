import psycopg2

from . import fixtures

formation = fixtures.make_formation_fixture('9.5.14')


def test_select(formation):
    """Verify that a SELECT statement can run against the database."""
    connection = psycopg2.connect(formation.connection_string)

    cursor = connection.cursor()
    cursor.execute("SELECT 1;")
    connection.commit()

    assert cursor.fetchone()[0] == 1
