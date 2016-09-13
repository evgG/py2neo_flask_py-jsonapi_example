# Py2neo Demo: The Movie Graph

Prerequisites:
- Running Neo4j server
- Movie data set (`:play movies` in browser)
- The Flask web framework (`pip install flask`)

To run from the root of the py2neo source tree:
```
PYTHONPATH=. NEO4J_PASSWORD="password" python -m moviegraph.flask_server
```
