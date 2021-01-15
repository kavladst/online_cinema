from tests.functional.testdata.models.film import Film
from tests.functional.testdata.models.genre import NestedGenre
from tests.functional.testdata.models.person import Person, NestedPerson

PERSON_ES_DATA_1 = Person(
    id='488d9f93-e547-477e-bc0d-190de4ad4462',
    full_name='Harrison Ford'
)
PERSON_ES_DATA_2 = Person(
    id='2b9aaf72-86fa-4e7d-8f97-4d1731e69b7f',
    full_name='Mark Hamill'
)

FILM_ES_DATA_1 = Film(
    id='378aa679-5646-4884-bfdd-de299e2c2b5c',
    imdb_rating=6.7,
    genre=[NestedGenre(g_id, g_name) for g_id, g_name in (
        ('7fbd8d35-7f0d-4141-b6f6-74e9088c366b', 'Sci-Fi'),
        ('6135a119-5a44-4269-a4e2-f5bf6a5c8487', 'Action'),
        ('c354e2ee-3708-49ec-8497-1b04aa3a7cb7', 'Adventure'),
        ('edba9556-2c18-46a2-bb5e-f071af502989', 'Fantasy')
    )],
    title='Star Wars: Episode IX - The Rise of Skywalker',
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
        ('5b48ff69-3e4b-4f1f-a1e7-8b015cf94be2', 'J.J. Abrams')
    )]
)
FILM_ES_DATA_2 = Film(
    id='90199510-1cb1-4fca-b75d-01c7590f02da',
    imdb_rating=8.7,
    genre=[NestedGenre(g_id, g_name) for g_id, g_name in (
        ('7fbd8d35-7f0d-4141-b6f6-74e9088c366b', 'Sci-Fi'),
        ('6135a119-5a44-4269-a4e2-f5bf6a5c8487', 'Action'),
        ('c354e2ee-3708-49ec-8497-1b04aa3a7cb7', 'Adventure'),
        ('edba9556-2c18-46a2-bb5e-f071af502989', 'Fantasy')
    )],
    title='Star Wars: Episode V - The Empire Strikes Back',
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
        ('efaad97f-3aa7-4f33-ae97-4326ddc73196', 'Billy Dee Williams'),
    )],
    writers=[NestedPerson(p_id, p_name) for p_id, p_name in (
        ('c54e0d2f-8ee9-4e04-8ff6-e92f33dbd183', 'Leigh Brackett'),
    )],
    directors=[NestedPerson(p_id, p_name) for p_id, p_name in (
        ('d5e46652-0c3f-4b2a-be2e-6a1d60f89260', 'Irvin Kershner'),
    )]
)

PERSON_SAMPLES_1 = [PERSON_ES_DATA_1, PERSON_ES_DATA_2]
RELATED_FILM_SAMPLES_1 = [FILM_ES_DATA_1, FILM_ES_DATA_2]
