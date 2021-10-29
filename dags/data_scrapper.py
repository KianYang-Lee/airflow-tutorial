import requests
from pymongo import MongoClient
from datetime import datetime
from airflow.providers.mongo.hooks.mongo import MongoHook


def get_raw_joke():
    """Retrieve a joke from 'jokeapi' and return it in dict format."""
    base_url = "https://v2.jokeapi.dev"
    response = requests.get(f"{base_url}/joke/any")
    return response.json()


def preprocess_joke(raw_joke: dict):
    """Perform preprocessing to clean raw jokes."""
    dictObject = {}
    dictObject["type"] = raw_joke.get("type")
    dictObject["category"] = raw_joke.get("category")

    if raw_joke.get("type") == "single":
        dictObject["joke"] = raw_joke.get("joke")
        return dictObject

    elif raw_joke.get("type") == "twopart":
        dictObject["joke"] = {}
        dictObject["joke"]["setup"] = raw_joke.get("setup")
        dictObject["joke"]["delivery"] = raw_joke.get("delivery")
        return dictObject

    else:
        print("Joke is of neither 'single' nor 'twopart' type.")


def serialize_joke(joke: dict):
    """Save jokes into local MongoDB instance."""
    if joke:
        joke["datetime"] = f"{datetime.now():%Y-%m-%d %H:%M:%S%z}"

        # Using PyMongo
        # uri = "mongodb://root:example@mongo:27017"  # this works
        uri = "mongodb://airflow:airflow@mongo:27017"  # this works too
        # uri = "mongodb://airflow:airflow@localhost:3456" # but this does not work
        client = MongoClient(uri)
        db = client.the_database
        collection = db.jokes
        result = collection.insert_one(joke)
        print(f"{result.inserted_id} is inserted!")

        # Using MongoHook wrapper
        # mongo_hook = MongoHook(conn_id="MONGO")
        # client = mongo_hook.get_conn()
        # db = client.the_database
        # collection = db.jokes
        # result = collection.insert_one(joke)
        # print(f"{result.inserted_id} is inserted!")


def scrap_joke():
    raw_joke = get_raw_joke()
    joke = preprocess_joke(raw_joke)
    serialize_joke(joke)


if __name__ == "__main__":
    scrap_joke()
