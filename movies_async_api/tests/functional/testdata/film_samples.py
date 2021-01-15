from tests.functional.testdata.models.film import Film, NestedGenre, NestedPerson
from tests.functional.testdata.models.person import Person

FILM_ES_DATA_1 = Film(
    id='aec4b240-39d4-495c-b303-451097bdaa6d',
    title='Star Trek: First Contact',
    imdb_rating=7.6,
    description='In the 24th century, the crew of the Enterprise-E has been ordered to patrol the Romulan Neutral '
                'Zone by the Federation to avoid interference with their battle against the insidious Borg. '
                'Witnessing the loss of the battle, Captain Jean-Luc Picard ignores orders and takes command of '
                'the fleet engaging the Borg. But the Borg plan to travel back into the 21st century through a '
                'vortex with the intention to stop Earth\'s first contact with an alien race (the Vulcans). '
                'Following the Borg sphere, Picard and his crew realize that they have taken over the Enterprise '
                'in order to carry out their mission. Their only chance to do away with the Borg and their '
                'seductive queen is to make sure that Zefram Cochrane makes his famous faster-than-light travel '
                'to the stars.',
    directors_names=[
        'Jonathan Frakes'
    ],
    actors_names=[
        'Brent Spiner',
        'LeVar Burton',
        'Patrick Stewart',
        'Jonathan Frakes'
    ],
    writers_names=[
        'Gene Roddenberry'
    ],
    genre=[NestedGenre(g_id, g_name) for g_id, g_name in (
        ('c354e2ee-3708-49ec-8497-1b04aa3a7cb7', 'Adventure'),
        ('7fbd8d35-7f0d-4141-b6f6-74e9088c366b', 'Sci-Fi'),
        ('f03b109e-18fc-493a-aa9b-8f79def687e6', 'Drama'),
        ('5d13c978-a535-4e58-8f71-8bf84f87f0f2', 'Thriller'),
        ('6135a119-5a44-4269-a4e2-f5bf6a5c8487', 'Action'),
    )],
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
    title='Star Wars: Episode IX - The Rise of Skywalker',
    imdb_rating=6.7,
    genre=[NestedGenre(g_id, g_name) for g_id, g_name in (
        ('7fbd8d35-7f0d-4141-b6f6-74e9088c366b', 'Sci-Fi'),
        ('6135a119-5a44-4269-a4e2-f5bf6a5c8487', 'Action'),
        ('c354e2ee-3708-49ec-8497-1b04aa3a7cb7', 'Adventure'),
        ('edba9556-2c18-46a2-bb5e-f071af502989', 'Fantasy')
    )],
    description='The surviving members of the resistance face the First Order once again, and the legendary '
                'conflict between the Jedi and the Sith reaches its peak bringing the Skywalker saga to its end.',
    directors_names=[
        'J.J. Abrams'
    ],
    actors_names=[
        'Mark Hamill',
        'Adam Driver',
        'Carrie Fisher',
        'Daisy Ridley'
    ],
    writers_names=[
        'Chris Terrio'
    ],
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
FILM_ES_DATA_3 = Film(
    id='90199510-1cb1-4fca-b75d-01c7590f02da',
    title='Star Wars: Episode V - The Empire Strikes Back',
    imdb_rating=8.7,
    genre=[NestedGenre(g_id, g_name) for g_id, g_name in (
        ('7fbd8d35-7f0d-4141-b6f6-74e9088c366b', 'Sci-Fi'),
        ('6135a119-5a44-4269-a4e2-f5bf6a5c8487', 'Action'),
        ('c354e2ee-3708-49ec-8497-1b04aa3a7cb7', 'Adventure'),
        ('edba9556-2c18-46a2-bb5e-f071af502989', 'Fantasy')
    )],
    description='Luke Skywalker, Han Solo, Princess Leia and Chewbacca face attack by the Imperial forces and its '
                'AT-AT walkers on the ice planet Hoth. While Han and Leia escape in the Millennium Falcon, '
                'Luke travels to Dagobah in search of Yoda. Only with the Jedi master\'s help will Luke survive '
                'when the dark side of the Force beckons him into the ultimate duel with Darth Vader.',
    directors_names=[
        'Irvin Kershner'
    ],
    actors_names=[
        'Harrison Ford',
        'Mark Hamill',
        'Carrie Fisher',
        'Billy Dee Williams'
    ],
    writers_names=[
        'Leigh Brackett'
    ],
    actors=[NestedPerson(p_id, p_name) for p_id, p_name in (
        ('488d9f93-e547-477e-bc0d-190de4ad4462', 'Harrison Ford'),
        ('2b9aaf72-86fa-4e7d-8f97-4d1731e69b7f', 'Mark Hamill'),
        ('9623439e-7ce2-4855-9b0d-d2db10f60e42', 'Carrie Fisher'),
        ('efaad97f-3aa7-4f33-ae97-4326ddc73196', 'Billy Dee Williams')
    )],
    writers=[NestedPerson(p_id, p_name) for p_id, p_name in (
        ('c54e0d2f-8ee9-4e04-8ff6-e92f33dbd183', 'Leigh Brackett'),
    )],
    directors=[NestedPerson(p_id, p_name) for p_id, p_name in (
        ('d5e46652-0c3f-4b2a-be2e-6a1d60f89260', 'Irvin Kershner'),
    )]
)

RELATED_PERSON_ES_DATA_1 = Person(
    id='488d9f93-e547-477e-bc0d-190de4ad4462',
    full_name='Harrison Ford'
)
RELATED_PERSON_ES_DATA_2 = Person(
    id='2b9aaf72-86fa-4e7d-8f97-4d1731e69b7f',
    full_name='Mark Hamill'
)

FILM_SAMPLES_1 = [FILM_ES_DATA_1, FILM_ES_DATA_2, FILM_ES_DATA_3]
FILM_SEARCH_SAMPLES_EXPECTED_1 = [
    {
        'uuid': '378aa679-5646-4884-bfdd-de299e2c2b5c',
        'title': 'Star Wars: Episode IX - The Rise of Skywalker',
        'imdb_rating': 6.7
    }
]
FILM_SEARCH_QUERY_FOR_SAMPLES_1 = 'Rise'

RELATED_PERSON_SAMPLES_1 = [RELATED_PERSON_ES_DATA_1, RELATED_PERSON_ES_DATA_2]

FILM_AGE_LIMIT_ES_DATA = Film(
    id='c1262097-2f4f-4f93-8e75-b3c8ca1d01a7',
    title='Deadpool',
    imdb_rating=8.0,
    age_limit=True,
)
