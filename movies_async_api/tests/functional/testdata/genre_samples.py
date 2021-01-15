from tests.functional.testdata.models.film import Film
from tests.functional.testdata.models.genre import Genre, NestedGenre
from tests.functional.testdata.models.person import NestedPerson

GENRE_ES_DATA_1 = Genre(
    id='edba9556-2c18-46a2-bb5e-f071af502989',
    name='Fantasy')
GENRE_ES_DATA_2 = Genre(
    id='7fbd8d35-7f0d-4141-b6f6-74e9088c366b',
    name='Sci-Fi')

FILM_ES_DATA_1 = Film(
    id='aec4b240-39d4-495c-b303-451097bdaa6d',
    imdb_rating=7.6,
    genre=[NestedGenre(g_id, g_name) for g_id, g_name in (
        ('7fbd8d35-7f0d-4141-b6f6-74e9088c366b', 'Sci-Fi'),
    )],
    title='Star Trek: First Contact',
    description='In the 24th century, the crew of the Enterprise-E has been ordered to patrol the Romulan Neutral.',
    directors_names=[
        'Jonathan Frakes'
    ],
    actors_names=[
        'Brent Spiner',
        'LeVar Burton',
        'Patrick Stewart',
        'Jonathan Frakes'],
    writers_names=[
        'Gene Roddenberry'],
    actors=[NestedPerson(p_id, p_name) for p_id, p_name in (
        ('fb04f296-2240-4f94-9c83-518a413c3ee9', 'Brent Spiner'),
        ('cfe6b5c1-8f75-448b-a70e-d94956b89d39', 'LeVar Burton'),
        ('ff42a473-d1d7-477a-b1b1-48c629a97814', 'Patrick Stewart'),
        ('33ca493b-0201-4df4-a8e9-3cdf445b3477', 'Jonathan Frakes')
    )],
    writers=[NestedPerson(p_id, p_name) for p_id, p_name in (
        ('9e0e32dd-d5b3-4ef9-a8bc-0ea63682a380', 'Gene Roddenberry'),
    )],
    directors=[NestedPerson(p_id, p_name) for p_id, p_name in (
        ('33ca493b-0201-4df4-a8e9-3cdf445b3477', 'Jonathan Frakes'),
    )]
)
FILM_ES_DATA_2 = Film(
    id='378aa679-5646-4884-bfdd-de299e2c2b5c',
    imdb_rating=6.7,
    genre=[NestedGenre(g_id, g_name) for g_id, g_name in (
        ('edba9556-2c18-46a2-bb5e-f071af502989', 'Fantasy'),
    )],
    title='Star Wars: Episode IX - The Rise of Skywalker',
    description='The surviving members of the resistance face the First Order once again.',
    directors_names=[
        'J.J. Abrams'],
    actors_names=[
        'Mark Hamill',
        'Adam Driver',
        'Carrie Fisher',
        'Daisy Ridley'],
    writers_names=[
        'Chris Terrio'],
    actors=[NestedPerson(p_id, p_name) for p_id, p_name in (
        ('2b9aaf72-86fa-4e7d-8f97-4d1731e69b7f', 'Mark Hamill'),
        ('876dd623-ab44-4c12-b2d3-bec99ed417fe', 'Adam Driver'),
        ('9623439e-7ce2-4855-9b0d-d2db10f60e42', 'Carrie Fisher'),
        ('5e4f1319-d8d4-42bf-8c9a-22b7a431034e', 'Daisy Ridley')
    )],
    writers=[NestedPerson(p_id, p_name) for p_id, p_name in (
        ('d89f7beb-fa49-4f4f-a0a7-1f0066be5f78', 'Chris Terrio'),
    )],
    directors=[NestedPerson(p_id, p_name) for p_id, p_name in (
        ('5b48ff69-3e4b-4f1f-a1e7-8b015cf94be2', 'J.J. Abrams'),
    )]
)

GENRE_SAMPLES_1 = [GENRE_ES_DATA_1, GENRE_ES_DATA_2]
RELATED_FILM_SAMPLES_1 = [FILM_ES_DATA_1, FILM_ES_DATA_2]
