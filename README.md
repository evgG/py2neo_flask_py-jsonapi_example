This is an example of my tests on flask, py-jsonapi and py2neo
==========

Based on [Nigel Small's Demo](https://github.com/nigelsmall/py2neo/demo)

I change Bottle to Flask, and remove __primarykey__ on py2neo ogm models

License
-------

This library is licensed under the `MIT License <./LICENSE>`_.

Install
-------

pip:

pip install -r requirements.txt

pip install git+https://github.com/evgG/py-jsonapi.git@py2neo#egg=py-jsonapi

neo4j server:
- Running Neo4j server, i prefer [docker image](https://github.com/neo4j/docker-neo4j)
- Movie data set (`:play movies` in browser)

Usage
-----

To run from the root of the source tree:
```
PYTHONPATH=. NEO4J_PASSWORD="password" python -m moviegraph.flask_server
```

Here you have 2 options:
- Use web-app on http://localhost:8080/
- Use jsonapi for models Person, Movie and Comment:
```
http://localhost:8080/api/Person
http://localhost:8080/api/Movie
http://localhost:8080/api/Comment
```

Using curl to get jsonapi response
----------------------------------
- Get full Person output:
```
curl -i -H "Accept: application/vnd.api+json" -H 'Content-Type:application/vnd.api+json' 'http://localhost:8080/api/Person'
```

- Get Person with id = 56
```
curl -i -H "Accept: application/vnd.api+json" -H 'Content-Type:application/vnd.api+json' 'http://localhost:8080/api/Person/56'
```