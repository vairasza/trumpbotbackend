import random

from flask import Flask, request

from Tweet import Tweet
from Topics import Topics


app = Flask(__name__)
tweet = Tweet()
tweet.train_model()


@app.route("/tweet", methods=["POST"])
def hello_world():
  user_request = request.get_json()
  user_text = user_request["text"]
  
  topic_list = Topics.retrieve_topics(user_text)
  if topic_list is None:
    return {
      "body": {
        "text": "FILE THIS UNDER SH!T you can't make up YET ITS NOT FAKE NEWS!!!!!! (no valid topic)"
      }
    }

  else:
    group = Topics.get_matching_group(topic_list)

    real_or_fake = [tweet.get_real_tweet, tweet.get_fake_tweet]
    rnd_func = random.choice(real_or_fake)
    trump_tweet = rnd_func(group, topic_list)

    return {
      "body": trump_tweet
    }


@app.route("/help", methods=["GET"])
def get_help():
  return {
    "body": {
      "text": Topics.to_string()
    }
  }


if __name__ == "__main__":
  app.run(port=5037)