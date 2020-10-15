import praw
import os



# Variables
subreddit = "musicbottesting"
target_flair = "ExampleFlair"

reddit = praw.Reddit(client_id='####',
                client_secret='####',
                user_agent='Enoctis r_RequestABot Request',
                username='####',
                password='####')

waiting_list = []

if os.path.isfile('processed_submissions.txt'):
	with open('processed_submissions.txt', 'r') as file:
		processed_submissions = [line.rstrip('\n') for line in file]

for flair in reddit.subreddit(subreddit).flair(limit=None):
    user = flair['user'].name
    flair_text = flair['flair_text']
    if flair_text == str(target_flair):
        for submission in reddit.redditor(user).submissions.new(limit=None):
            if submission.subreddit == str(subreddit):
                if submission.id not in processed_submissions:
                    for top_level_comment in submission.comments:
                        if top_level_comment.author == "AutoModerator":
                            top_level_comment.mod.remove(mod_note="User is now verified")
                            print("Deleted Automoderator Comment {} on post {}".format(top_level_comment.id, submission.id))
                            waiting_list.append(submission.id)
            else:
                break
            
with open('processed_submissions.txt','a') as file:
	for item in waiting_list:
		file.write('{}\n'.format(item))