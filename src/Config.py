class Config:
  TOPICS = ["obama", "democrats", "china", "deal", "the mainstream media", "election", "campaign", "interview", "fox", "fake", "news", "fake news", "make america great", "keep america great", "@ cnn", "#", "thank you", "congratulations", "hillary", "america", "jobs", "congress", "senator"]

  #these groups are a reprensentation for our clusters
  GROUP_1 = {"index": 0, "overtopic": "election", "count": 0, "subtopics": TOPICS[:7], "file": "data/gruppe1.txt"}
  GROUP_2 = {"index": 1, "overtopic": "news", "count": 0, "subtopics": TOPICS[7:14], "file": "data/gruppe2.txt"}
  GROUP_3 = {"index": 2, "overtopic": "people", "count": 0, "subtopics": TOPICS[14:18], "file": "data/gruppe3.txt"}
  GROUP_4 = {"index": 3, "overtopic": "politics", "count": 0, "subtopics": TOPICS[18:], "file": "data/gruppe4.txt"}

  HELP_TEXT = "I make a very gold conversation on these numerous topics: "