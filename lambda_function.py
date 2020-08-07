import json
import boto3
from operator import itemgetter
import re
import time
import random
import markovify
#import spacy

models = [{"topic": "america", "count": 0, "file": "markov_america.txt"}, {"topic": "china", "count": 0, "file": "markov_china.txt"},
{"topic": "clinton", "count": 0, "file": "markov_clinton.txt"}, {"topic": "cnn", "count": 0, "file": "markov_cnn.txt"}, {"topic": "covid", "count": 0, "file": "markov_covid.txt"},
{"topic": "dems", "count": 0, "file": "markov_dems.txt"}, {"topic": "elections", "count": 0, "file": "markov_elections.txt"}, {"topic": "fakes", "count": 0, "file": "markov_fakes.txt"},
{"topic": "family", "count": 0, "file": "markov_family.txt"}, {"topic": "fox", "count": 0, "file": "markov_fox.txt"}, {"topic": "germany", "count": 0, "file": "markov_germany.txt"},
{"topic": "guns", "count": 0, "file": "markov_guns.txt"}, {"topic": "healths", "count": 0, "file": "markov_healths.txt"}, {"topic": "industry", "count": 0, "file": "markov_industry.txt"},
{"topic": "interview", "count": 0, "file": "markov_interview.txt"}, {"topic": "iran", "count": 0, "file": "markov_iran.txt"}, {"topic": "jobs", "count": 0, "file": "markov_jobs.txt"},
{"topic": "kag", "count": 0, "file": "markov_kag.txt"},
{"topic": "korea", "count": 0, "file": "markov_korea.txt"}, {"topic": "maga", "count": 0, "file": "markov_maga.txt"}, {"topic": "media", "count": 0, "file": "markov_media.txt"},
{"topic": "military", "count": 0, "file": "markov_military.txt"}, {"topic": "myself", "count": 0, "file": "markov_myself.txt"}, {"topic": "nbc", "count": 0, "file": "markov_nbc.txt"},
{"topic": "obamas", "count": 0, "file": "markov_obamas.txt"}, {"topic": "politics", "count": 0, "file": "markov_politics.txt"}, {"topic": "republican", "count": 0, "file": "markov_republican.txt"},
{"topic": "russia", "count": 0, "file": "markov_russia.txt"}, {"topic": "walls", "count": 0, "file": "markov_walls.txt"}]

###
### event handler
###
def lambda_handler(event, context):
    user_input = json.loads(event["body"])["user_input"]
    last_tweet = json.loads(event["body"])["last_tweet"]
    fake_tweet = json.loads(event["body"])["fake_tweet"]
    
    #def output of lambda function
    output = {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Credentials': True,
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": ""
    }

    #def client for dynamodb
    client = boto3.resource("dynamodb")
    table = client.Table("trump_data_alt")
    table2 = client.Table("trump_fake_tweet_record_alt")
    
    #if user types !help, return all available topics to the bot
    if (user_input == "!help"):
        
        output["body"] = json.dumps({
                "flavor_text": "I make a very gold conversation on these numerous topics: " + return_topics(),
                "last_tweet": "",
                "fake_tweet": "exit" 
            })
            
        return output
    
    #react to user responding if a tweet is from trump or generated
    elif (user_input == "!fake" and fake_tweet != "exit"):
        
        if (fake_tweet == "true"):

            output["body"] = json.dumps({
                "flavor_text": "This story is just another made up by Fake News tale that is told only to damage me. 100% Correct. Thank you.", #user correct - tweet generated
                "last_tweet": "",
                "fake_tweet": "exit" 
            })

            item = {
                "tweet_id": str(int(round(time.time() * 1000))),
                "user_input": str(user_input),
                "last_tweet": last_tweet,
                "fake_tweet": fake_tweet,
                "result": "user correct -- tweet generated"
            }

            table2.put_item(Item = item)

            return output

        else:

            output["body"] = json.dumps({
                    "flavor_text": "I am full of honesty and sincerity on the other hand you are a total liar. You got it wrong!", #user incorrect - tweet real
                    "last_tweet": "",
                    "fake_tweet": "exit"  
                })

            item = {
                "tweet_id": str(int(round(time.time() * 1000))),
                "user_input": str(user_input),
                "last_tweet": last_tweet,
                "fake_tweet": fake_tweet,
                "result": "user incorrect -- tweet real"
            }

            table2.put_item(Item = item)

            return output
     
    elif (user_input == "!real" and fake_tweet != "exit"):
        
        if (fake_tweet == "true"):

            output["body"] = json.dumps({
                "flavor_text": "Haha, that was a fake tweet! Get this liar out of the White House.", #user incorrect - tweet generated
                "last_tweet": "",
                "fake_tweet": "exit" 
            })

            item = {
                "tweet_id": str(int(round(time.time() * 1000))),
                "user_input": str(user_input),
                "last_tweet": last_tweet,
                "fake_tweet": fake_tweet,
                "result": "user incorrect - tweet generated"
            }

            table2.put_item(Item = item)

            return output

        else:

            output["body"] = json.dumps({
                    "flavor_text": "I dictated this tweet to my executive assistant and she posted it. True!", #user correct - tweet real
                    "last_tweet": "",
                    "fake_tweet": "exit"  
                })

            item = {
                "tweet_id": str(int(round(time.time() * 1000))),
                "user_input": str(user_input),
                "last_tweet": last_tweet,
                "fake_tweet": fake_tweet,
                "result": "user correct - tweet real"
            }

            table2.put_item(Item = item)

            return output
    
    else:
        topics_retrieved = retrieve_topics(user_input)
        
        if (topics_retrieved == None):
            item = {
                "tweet_id": str(int(round(time.time() * 1000))),
                "user_input": str(user_input),
                "tweet": "",
                "fake_tweet": ""
            }

            table.put_item(Item = item)
            
            output["body"] = json.dumps({
                    "flavor_text": "FILE THIS UNDER SH!T you can’t make up YET ITS NOT FAKE NEWS!!!!!! (no valid topic)",
                    "last_tweet": "",
                    "fake_tweet": "exit"                    
            })
            
            return output
            
        else:
            matched_group_topics = matching_group(topics_retrieved)
            
            rnd = random.randint(0,1)
            
            tweet = generate_fake_tweet(matched_group_topics, topics_retrieved) if (rnd > 0.5) else return_real_tweet(matched_group_topics, topics_retrieved)

            item = {
                "tweet_id": str(int(round(time.time() * 1000))),
                "user_input": str(user_input),
                "tweet": tweet["tweet"],
                "fake_tweet": tweet["fake_tweet"]
            }

            table.put_item(Item = item)
 
            output["body"] = json.dumps({
                    "flavor_text": "Some very interesting topics -- here is my tweet:",
                    "last_tweet": tweet["tweet"],
                    "fake_tweet": tweet["fake_tweet"]
            })
            
            return output


def return_topics():
    output = ""
    for x in models:
        if x == models[-1]:
            output += x["topic"]
            
        else:
            output += x["topic"] + ", "
        
    return output


def retrieve_topics(user_input):
    array_of_topics = []
    
    if (type(user_input) == str):
        
        user_input = re.sub(r'[^A-Za-z0-9 ]', '', user_input)
        user_input = user_input.lower()
        
        for word in user_input.split():
        
            if (re.search(r'(obama|barack)', word)):
                array_of_topics.append("obamas")
                
            if (re.search(r'(democrat.*|part.*)', word)):
                array_of_topics.append("dems")
                
            if (re.search(r'(china|peking|xi|jinping)', word)):
                array_of_topics.append("china")
    
            if (re.search(r'(media.*|television|tv|radio|news)', word)):
                array_of_topics.append("media")
                
            if (re.search(r'elect.*|ballot.*|poll.*', word)):
                array_of_topics.append("elections")
                
            if (re.search(r'(interview.*|meet.*|press|statement.*)', word)):
                array_of_topics.append("interview")
            
            if (re.search(r'fox', word)):
                array_of_topics.append("fox")
                
            if (re.search(r'(fake.*|hoax|scam.*|trick.*|fraud)', word)):
                array_of_topics.append("fakes")
                
            if (re.search(r'cnn', word)):
                array_of_topics.append("cnn")
                
            if (re.search(r'nbc', word)):
                array_of_topics.append("nbc")
                
            if (re.search(r'(maga|make america great again)', word)):
                array_of_topics.append("maga")
                
            if (re.search(r'(kag.?|keep america great)', word)):
                array_of_topics.append("kag")
                
            if (re.search(r'(hillary|crook.*|clinton)', word)):
                array_of_topics.append("clinton")
                
            if (re.search(r'(usa|america.*|land|states)', word)):
                array_of_topics.append("america")
            
            if (re.search(r'(work|job.*|business|career|office|profession|task.*)', word)):
                array_of_topics.append("jobs")
                
            if (re.search(r'(corona|covid19|covid|.*virus|disease.*|epidemic.*|contag.*)', word)):
                array_of_topics.append("covid")
            
            if (re.search(r'(clan|group|child.*|wife|melania|trump)', word)):
                array_of_topics.append("family")
                
            if (re.search(r'(merkel|german.*|deutsch.*|nazi.*)', word)):
                array_of_topics.append("germany")
                
            if (re.search(r'(gun.*|cannon.*|handgun.*|pistol.*|revolver.*|rifl.*|shotgun.*|firegun.*|weapon.*)', word)):
                array_of_topics.append("guns")            
                
            if (re.search(r'(fitness|strength|health.*|doctor.*|medic.*|hospital.*|obamacare)', word)):
                array_of_topics.append("healths")
                
            if (re.search(r'(busines.*|commerc.*|corporat.*|manage.*|product.*|trad.*|monopol.*)', word)):
                array_of_topics.append("industry")            
                
            if (re.search(r'(iran.*|rohani|hassan|conflict.*|war|terror.*|islam.*|misogyn.*|nuclear.*|persic.*)', word)):
                array_of_topics.append("iran")
                
            if (re.search(r'(korea.*|moon|jae.*|north korea|kim|jong.*|conflict|war|seoul|pyongyang|dictat.*|demilitarized)', word)):
                array_of_topics.append("korea")
                
            if (re.search(r'(milita.*|soldier.*|war|conflict|nuclear.*|attack)', word)):
                array_of_topics.append("military")            
    
            if (re.search(r'(donald|trump|president)', word)):
                array_of_topics.append("myself")
                
            if (re.search(r'(politic.*|senat.*|congres.*|law|decree|rule.*|president)', word)):
                array_of_topics.append("politics")            
                
            if (re.search(r'(republic.*|politic.*)', word)):
                array_of_topics.append("republican")            
                
            if (re.search(r'(putin|russi.*|wodka|cold)', word)):
                array_of_topics.append("russia")            
                
            if (re.search(r'(wall.*|pledg.*|campaign|mexic.*|border)', word)):
                array_of_topics.append("walls")
            
        #return none if no match was found    
        if(len(array_of_topics) == 0):
            return None
        else:       
            return array_of_topics
        
    else:
        return None


def matching_group(topics):
    
    for model in models:
        
        model["count"] = 0
    
    for word in topics:
        
        for model in models:
        
            if (word == model["topic"]):
                model["count"] += 1

    group = max(models, key=itemgetter('count'))
            
    return group


def generate_fake_tweet(matched_group, topics):
    key = "models/" + matched_group["file"]
    
    s3 = boto3.client('s3')
    s3_obj = s3.get_object(Bucket = 'trump-data', Key = key)
    
    model = json.loads(s3_obj["Body"].read())
    model = markovify.Text.from_json(model)

    return {"tweet": model.make_short_sentence(140), "fake_tweet": "true"}


def return_real_tweet(matched_group, topics):
    key = "real_tweets/" + matched_group["file"]
    
    s3 = boto3.client('s3')
    s3_obj = s3.get_object(Bucket = 'trump-data', Key = key)
    
    tweets = s3_obj["Body"].read().decode('utf-8').split("\n")
    
    tweet = random.choice(tweets)

    return {"tweet": tweet, "fake_tweet": "false"}
    
    