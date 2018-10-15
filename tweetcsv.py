from nltk.twitter.common import json2csv

class tweet2csv(object):

    def convert(self,input_file,output_file):
        with open(input_file) as fp:
            json2csv(fp, output_file,
            ['created_at', 'favorite_count', 'id', 'in_reply_to_status_id',
            'in_reply_to_user_id', 'retweet_count', 'retweeted',
            'text', 'truncated', 'user.id'])
        return 1
