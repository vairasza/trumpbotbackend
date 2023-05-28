import re
from operator import itemgetter
from typing import Union

from Config import Config

class Topics:

  TOPICS = Config.TOPICS

  @staticmethod
  def to_string() -> str:
    return Config.HELP_TEXT + ", ".join(Topics.TOPICS)

  @staticmethod
  def retrieve_topics(user_input: str) -> Union[list[str], None]:
    array_of_topics = []

    if (type(user_input) is not str):
      return None

    #remove characters that are not alphabetic or numeric
    user_input = re.sub(r'[^A-Za-z0-9 ]', '', user_input)
    user_input = user_input.lower()
    
    if (re.search(r'(obama|barack.?obama|barack)', user_input)):
      array_of_topics.append("barack obama")
        
    if (re.search(r'(democrat.*|part(y|ies))', user_input)):
      array_of_topics.append("democrats")
        
    if (re.search(r'(china|peking|xi( jinping)?)', user_input)):
      array_of_topics.append("china")
        
    if (re.search(r'(deals?|trade deal|contract)', user_input)):
      array_of_topics.append("deal")
        
    if (re.search(r'(medias?|television|tv|radio|news)', user_input)):
      array_of_topics.append("media")
        
    if (re.search(r'elections?|ballot.*|polls?', user_input)):
      array_of_topics.append("election")
    
    if (re.search(r'campaign.*', user_input)):
      array_of_topics.append("campaign")
        
    if (re.search(r'(interview.?|meet.*|press( conference)?|statements?)', user_input)):
      array_of_topics.append("interview")
    
    if (re.search(r'fox( news)?', user_input)):
      array_of_topics.append("fox")
        
    if (re.search(r'(fake( news)?|hoax|scam.*|trick.*|fraud)', user_input)):
      array_of_topics.append("fake")
        
    if (re.search(r'(news|report.*|state(ment)?|rumor.*|report.*)', user_input)):
      array_of_topics.append("news")
        
    if (re.search(r'cnn', user_input)):
      array_of_topics.append("cnn")
        
    if (re.search(r'nbc', user_input)):
      array_of_topics.append("nbc")
        
    if (re.search(r'obamagate', user_input)):
      array_of_topics.append("obamagate")
        
    if (re.search(r'(provocat.*|affront|insult.*)', user_input)):
      array_of_topics.append("provocation")
        
    if (re.search(r'(maga|make america great again)', user_input)):
      array_of_topics.append("make america great again")
        
    if (re.search(r'(kag(2020)?|keep america great)', user_input)):
      array_of_topics.append("keep america great")
        
    if (re.search(r'(thanks?(you)?|prais.*|grateful|appreciat.*)', user_input)):
      array_of_topics.append("thank you")
        
    if (re.search(r'(congrat.*|compliments?|bless.*)', user_input)):
      array_of_topics.append("congrats")
        
    if (re.search(r'(hillary|crook.*|clinton)', user_input)):
      array_of_topics.append("hillary")
        
    if (re.search(r'(usa|america.*|land|states)', user_input)):
      array_of_topics.append("america")
    
    if (re.search(r'(work|job.*|business|career|office|profession|task.*)', user_input)):
      array_of_topics.append("jobs")
      
    if (re.search(r'state of the union', user_input)):
      array_of_topics.append("state of the union")
        
    if (re.search(r'(announc.*|advertis.*|messag.*|publica.*)', user_input)):
      array_of_topics.append("announcement")
        
    if (re.search(r'congress.*', user_input)):
      array_of_topics.append("congress")
        
    if (re.search(r'senat.*', user_input)):
      array_of_topics.append("senator")
        
        
    #return none if no match was found    
    if(len(array_of_topics) == 0):
      return None

    else:       
      return array_of_topics
  
  @staticmethod
  def get_matching_group(topics: list) -> int:
    groups = [
      { "count": 0, "index": 0},
      { "count": 0, "index": 1},
      { "count": 0, "index": 2},
      { "count": 0, "index": 3}
    ]
      
    for word in topics:
        
      if (word in Config.GROUP_1["subtopics"]):
        groups[0]["count"] += 1
      
      elif (word in Config.GROUP_2["subtopics"]):
        groups[1]["count"] += 1
          
      elif (word in Config.GROUP_3["subtopics"]):
        groups[2]["count"] += 1
          
      elif (word in Config.GROUP_4["subtopics"]):
        groups[3]["count"] += 1

    group = max(groups, key=itemgetter('count'))
            
    return group["index"]