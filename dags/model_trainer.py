from typing import Tuple
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import pickle
from pymongo import MongoClient

# Classes for jokes
classes = ["Programming", "Misc", "Dark", "Pun", "Spooky", "Christmas"]


def retrieve_jokes():
    """Retrieve all jokes in MongoDB and return it as DataFrame object."""
    uri = "mongodb://airflow:airflow@mongo:27017"
    # uri = "mongodb://airflow:airflow@localhost:3456"

    client = MongoClient(uri)
    db = client.the_database
    collection = db.jokes
    cursor = collection.find({})
    jokes = list(cursor)
    jokes_df = DataFrame(jokes)
    return jokes_df


def preprocess_data(raw_data: DataFrame) -> DataFrame:
    """
    Perform preprocessing by:
    1. Extracting only the relevant columns.
    2. Fill up 'joke' column by concatenating 'setup' and
    'delivery' values for jokes with type 'twopart'.
    3. Create new column "class" by encoding "category".

    """
    columns = ["type", "joke", "category"]
    data = raw_data[columns].copy()

    data.loc[data["type"] == "twopart", "joke"] = data[
        data["type"] == "twopart"
    ].joke.map(lambda x: x.get("setup") + " " + x.get("delivery"))

    data["class"] = data.category.map(lambda x: classes.index(x))

    return data


def train_model(data: DataFrame) -> Tuple:
    """
    Train the model by performing the following:
    1. Splitting data into train and test dataset,
    2. Perform count vectorizing and tf-idf transformation on features,
    3. Fit the model on train dataset,
    4. Evaluate the model on both train and test set, and
    5. Serialize the model, count vectorizer and tf-idf transformer.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        data["joke"], data["class"], random_state=0
    )
    vectorizer = CountVectorizer()
    X_train_count_vec = vectorizer.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_count_vec)

    model = MultinomialNB().fit(X_train_tfidf, y_train)
    train_acc_score = accuracy_score(y_train, model.predict(X_train_tfidf))
    print("Train accuracy score: ", train_acc_score)

    X_test_tfidf = tfidf_transformer.transform(vectorizer.transform(X_test))
    test_acc_score = accuracy_score(y_test, model.predict(X_test_tfidf))
    print("Test accuracy score: ", test_acc_score)

    # Serialize
    pickle.dump(
        vectorizer.vocabulary_, open("/opt/airflow/dags/files/vectorizer.pkl", "wb")
    )
    pickle.dump(
        tfidf_transformer, open("/opt/airflow/dags/files/tfidf_transformer.pkl", "wb")
    )
    pickle.dump(model, open("/opt/airflow/dags/files/model.pkl", "wb"))


def inference():
    """
    Load binary files and perform model inference on one feature.
    """
    vectorizer = CountVectorizer(
        vocabulary=pickle.load(open("/opt/airflow/dags/files/vectorizer.pkl", "rb"))
    )
    tfidf_transformer = pickle.load(
        open("/opt/airflow/dags/files/tfidf_transformer.pkl", "rb")
    )
    model = pickle.load(open("/opt/airflow/dags/files/model.pkl", "rb"))

    vectorized_feature = vectorizer.transform(
        [
            "I was reading a great book about an immortal dog the other day. It was impossible to put down."
        ]
    )
    feature = tfidf_transformer.transform(vectorized_feature)
    result = classes[model.predict(feature).item()]
    print(
        f"With a given input, the model predicts: '{result}' when the right label is 'Pun'"
    )
    return result


def generate_model():
    raw_data = retrieve_jokes()
    data = preprocess_data(raw_data)
    train_model(data)


if __name__ == "__main__":
    generate_model()
    inference()
