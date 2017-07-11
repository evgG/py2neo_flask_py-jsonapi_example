#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
My tests on py2neo
'''


from os import getenv
from os.path import dirname
from calendar import month_name
from datetime import date
from flask import Flask, request, redirect, render_template
from py2neo import Graph, watch
from moviegraph.model import Movie, Person, Comment

import jsonapi
import jsonapi.py2neo
import jsonapi.flask

# Create Flask app
app = Flask(__name__)
home = dirname(__file__)

# Set up a link to the local graph database.
graph = Graph(password=getenv("NEO4J_PASSWORD"))
watch("neo4j.bolt")

# Crate api
# py2neo_db = jsonapi.py2neo.Database(graph.begin())
py2neo_db = jsonapi.py2neo.Database(graph)
api = jsonapi.flask.FlaskAPI("/api", db=py2neo_db, flask_app=app)
person_schema = jsonapi.py2neo.Schema(Person)
movie_schema = jsonapi.py2neo.Schema(Movie)
comment_schema = jsonapi.py2neo.Schema(Comment)
api.add_type(movie_schema)
api.add_type(person_schema)
api.add_type(comment_schema)


@app.route("/")
def get_index():
    return render_template("index.html")


@app.route("/person/")
def get_person_list():
    people = Person.select(graph)
    return render_template("person_list.html", people=people)


@app.route("/person/<_id>")
def get_person(_id):
    """ Page with details for a specific person.
    """
    person = Person.select(graph, int(_id)).first()
    movies = sorted([(movie, "Actor") for movie in person.acted_in] +
                    [(movie, "Director") for movie in person.directed])
    return render_template("person.html", person=person, movies=movies)


@app.route("/movie/")
def get_movie_list():
    movies = Movie.select(graph).order_by("_.title")
    return render_template("movie_list.html", movies=movies)


@app.route("/movie/<_id>")
def get_movie(_id):
    movie = Movie.select(graph, int(_id)).first()
    return render_template("movie.html", movie=movie)


@app.route("/movie/comment", methods=["POST"])
def post_movie_comment():
    """ Capture comment and redirect to movie page.
    """
    today = date.today()
    comment_date = "%d %s %d" % (today.day, month_name[today.month],
                                 today.year)
    comment = Comment(comment_date, request.form["name"],
                      request.form["text"])

    title_id = int(request.form["title_id"])
    movie = Movie.select(graph, title_id).first()
    comment.subject.add(movie)
    graph.create(comment)

    return redirect("/movie/%s" % title_id)


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
