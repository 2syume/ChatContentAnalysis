#coding=utf8
import operator
import re
import sys

PATTERN_SINGLE_MESSAGE_RECORD = '(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}), ([^:]+): (.*)'
PATTERN_NON_TEXT_CONTENT = '\[\[.*\]\]'
PATTERN_STICKER_AND_GIF = '\[\[.*[Sticker|GIF].*\]\]'

def extract_usernames_and_messages(filename):
  message_tuple_list = []
  lines = open(filename, 'r').readlines()
  for line in lines:
    matchObj = re.match(PATTERN_SINGLE_MESSAGE_RECORD, line)
    if (matchObj):
      time = matchObj.group(1)
      username = matchObj.group(2)
      message = matchObj.group(3)
      message_tuple_list.append((time, username, message))
  return message_tuple_list

def count_num_messages_per_user(message_tuple_list):
  username_num_messages_pairs = {}
  for message_tuple in message_tuple_list:
    username = message_tuple[1]
    if not username in username_num_messages_pairs:
      username_num_messages_pairs[username] = 1
    else:
      username_num_messages_pairs[username] += 1
  return username_num_messages_pairs

def count_text_length_per_user(message_tuple_list):
  username_text_length_pairs = {}
  p = re.compile(PATTERN_NON_TEXT_CONTENT)
  for message_tuple in message_tuple_list:
    username = message_tuple[1]
    message = p.sub('', message_tuple[2])
    if not username in username_text_length_pairs:
      username_text_length_pairs[username] = len(message)
    else:
      username_text_length_pairs[username] += len(message)
  return username_text_length_pairs

def count_num_stickers_per_user(message_tuple_list):
  username_num_stickers_pairs = {}
  for message_tuple in message_tuple_list:
    username = message_tuple[1]
    matchObj = re.match(PATTERN_STICKER_AND_GIF, message_tuple[2])
    if matchObj:
      if not username in username_num_stickers_pairs:
        username_num_stickers_pairs[username] = 1
      else:
        username_num_stickers_pairs[username] += 1
  return username_num_stickers_pairs

def sort_dict_by_value(dict, reverse):
  sorted_list = sorted(dict.items(), key=operator.itemgetter(1), reverse=reverse)
  return sorted_list

if __name__ == '__main__':
  chat_history_file_path = sys.argv[1]
  message_tuple_list = extract_usernames_and_messages(chat_history_file_path)

  # Rank of message number
  print 'Rank of message number ============================================\n'
  username_num_messages_pairs = count_num_messages_per_user(message_tuple_list)
  sorted_username_num_messages_pairs = sort_dict_by_value(username_num_messages_pairs, True)
  for username_num_messages_pair in sorted_username_num_messages_pairs:
    print '%s: %d' % (username_num_messages_pair[0], username_num_messages_pair[1])
  print '\n'

  # Rank of message length
  print 'Rank of message length ============================================\n'
  username_text_length_pairs = count_text_length_per_user(message_tuple_list)
  sorted_username_text_length_pairs = sort_dict_by_value(username_text_length_pairs, True)
  for username_text_length_pair in sorted_username_text_length_pairs:
    print '%s: %d' % (username_text_length_pair[0], username_text_length_pair[1])
  print '\n'

  # Rank of stickers and GIF number
  print 'Rank of stickers and GIF number ===================================\n'
  username_num_stickers_pairs = count_num_stickers_per_user(message_tuple_list)
  sorted_username_num_stickers_pairs = sort_dict_by_value(username_num_stickers_pairs, True)
  for username_num_stickers_pair in sorted_username_num_stickers_pairs:
    print '%s: %d' % (username_num_stickers_pair[0], username_num_stickers_pair[1])
  print '\n'
