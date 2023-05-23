import random, re, os
import markovify

class Tweet:

  CURR_DIR = os.path.dirname(__file__)
  DATA_PATH = "data"
  RETRIES = 2

  def __init__(self) -> None:
    self.models: list[markovify.Text] = []
    self.tweets: list[list[str]] = []

  def train_model(self) -> None:
    '''
      trains markovify models for each group in ./data
    '''
    txt_file_folder = os.path.join(self.CURR_DIR, self.DATA_PATH)
    txt_file_list = os.listdir(txt_file_folder)

    for val in txt_file_list:
      tweets = []
      tweet_file = os.path.join(txt_file_folder, val)

      with open(tweet_file, encoding="utf8") as txt_file:   
          for line in txt_file:
              clean_line = re.sub("\n", "", line)

              tweets.append(clean_line)

      model = markovify.Text(tweets, state_size = 3, well_formed = False)

      self.models.append(model)
      self.tweets.append(tweets)

  def get_fake_tweet(self, group_index: int, topics: dict) -> dict: 
    output = []
    retries = 0

    while (retries < self.RETRIES and len(output) < 1):
        retries += 1
        
        for topic in topics:
            
            if(topic == "media"):
                topic = "the mainstream media"
            if(topic == "maga"):
                topic = "make america great"
            if(topic == "make america great again"):
                topic = "make america great"
            if(topic == "kag2020"):
                topic = "keep america great"
            
            try:
                sentence = self.models[group_index].make_sentence_with_start(topic)
                
                if (sentence != None):
                    output.append(sentence)
                
            except:
                output.append("error")
    
    return {"tweet": random.choice(output), "fake": True}

  def get_real_tweet(self, group_index: int, topics: dict) -> dict:
    possible_tweets = []
    

    for tweet in self.tweets[group_index]:
        for topic in topics:
            
            if(topic == "media"):
                topic = "the mainstream media"
            if(topic == "maga"):
                topic = "make america great"
            if(topic == "make america great again"):
                topic = "make america great"
            if(topic == "kag2020"):
                topic = "keep america great"
            
            if topic in tweet:
                if (re.search(rf'^{topic}', tweet)):
                    possible_tweets.append(tweet)
    
    return {"tweet": random.choice(possible_tweets), "fake": False}
    