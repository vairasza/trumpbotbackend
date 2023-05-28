from Topics import Topics

def T_get_matching_group():
  topic_list = ['barack obama', 'make america great again']

  index = Topics.get_matching_group(topic_list)

  assert type(index) is not None, "index is type None"

def T_retrieve_topics_1():
  user_input = None
  output = Topics.retrieve_topics(user_input)

  assert type(output) is not list, "none input, output no list"
  assert output == None, "None input, output is None"

def T_retrieve_topics_2():
  user_input = "test"
  output = Topics.retrieve_topics(user_input)
  
  assert type(output) is not list, "input without topic match, output no list"
  assert output == None, "input without topic match, output is None"

def T_retrieve_topics_3():
  user_input = "obama"
  output = Topics.retrieve_topics(user_input)
  
  assert type(output) is list, "input with topic match, output list"
  assert len(output) == 1, "input with topic match, output is list with length 1"

def T_to_string():
  output = Topics.to_string()
  
  assert type(output) is str, "wrong datatype"

if __name__ == "__main__":
  T_get_matching_group()
  T_retrieve_topics_1()
  T_retrieve_topics_2()
  T_retrieve_topics_3()
  T_to_string()