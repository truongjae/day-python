import requests
def convert_string_to_json_cookies(cookies):
	cookies = cookies.replace(" ","")
	list_cookies = cookies.split(";")

	json_cookies = dict()

	for cookie in list_cookies:
		cut_cookie = cookie.split("=")
		key = cut_cookie[0]
		value = cut_cookie[1]
		json_cookies[key] = value
	return json_cookies

def spam_comment(text,cookies):
	url = "https://www.facebook.com/api/graphql/"

	data = {
		'fb_dtsg': 'NAcM1Mc49Q5uGlHvJxIho28Uz__mGiYIG1drnoTeoE-jXqpnzrORV6Q:27:1665755271',
		'variables': '''{
		  "displayCommentsFeedbackContext": null,
		  "displayCommentsContextEnableComment": null,
		  "displayCommentsContextIsAdPreview": null,
		  "displayCommentsContextIsAggregatedShare": null,
		  "displayCommentsContextIsStorySet": null,
		  "feedLocation": "PERMALINK",
		  "feedbackSource": 2,
		  "focusCommentID": null,
		  "groupID": null,
		  "includeNestedComments": false,
		  "input": {
		    "attachments": null,
		    "feedback_id": "ZmVlZGJhY2s6ODQ3NDkwNjUyOTQ3ODE1",
		    "formatting_style": null,
		    "message": {
		      "ranges": [],
		      "text": "'''+text+'''"
		    },
		    "attribution_id_v2": "CometSinglePostRoot.react,comet.post.single,via_cold_start,1666278871161,362633,,",
		    "is_tracking_encrypted": true,
		    "tracking": [
		      
		    ],
		    "feedback_source": "OBJECT",
		    "idempotence_token": null,
		    "actor_id": "100029031824085",
		    "client_mutation_id": "3"
		  },
		  "inviteShortLinkKey": null,
		  "renderLocation": null,
		  "scale": 1,
		  "useDefaultActor": false,
		  "UFI2CommentsProvider_commentsKey": "CometSinglePostRoute"
		}''' ,
		'doc_id': '5619117208110871'
	}
	p = requests.post(url,cookies = cookies,data = data)
	print("done")
def spam_mess(content,cookies):
	url = "https://m.facebook.com/messages/send/?icm=1&entrypoint=jewel&surface_hierarchy=unknown&eav=AfaxC2cSbKhrrWECjlwnLyc8qZPdaH8sGmVhLFYQfjDMc32FhIB2r7nJ53YhEoNuvZ4&paipv=0&refid=12"
	data = {
		'tids': 'cid.c.100015464351734:100029031824085',
		'wwwupp': 'C3',
		'ids[100015464351734]': 'ids[100015464351734]',
		'body': content,
		'fb_dtsg': 'NAcNHfAp0sc9C5VQJeZKkQYARbZTrE006C8Sy4HYz_InjyeGHUsTJ1A:27:1665755271',
		'__user': '100029031824085'
	}
	p = requests.post(url,data=data,cookies = cookies)

cookies = 'sb=-ZhVYhyKeolDfKxOOXwyllD-; datr=-ZhVYuRotzANNQY6XRJjZ4NF; locale=vi_VN; c_user=100029031824085; xs=27:F8VHuEEqJOB-Yg:2:1665755271:-1:6328::AcWC-aIlScKqX5pk7ZyT3dxflfgqg9oUtDAfLvlrzeM; wd=1876x935; fr=0iiuIdO2XVOXS4RqM.AWWO0jc0bYk1rmc8hfO1b6uIBIU.BjUVpo.Iy.AAA.0.0.BjUWLe.AWWt6LpzzIc; presence=C{"t3":[],"utc3":1666278133450,"v":1}'
cookies = convert_string_to_json_cookies(cookies)

# list_comment = 'ANHYEUEM'
# for cmt in list_comment:
# 	spam_mess(cmt,cookies)

from collections import deque

q = deque()
q.append(1)
q.append(2)
q.append(3)
print(q.popleft())
print(q.popleft())
print(q.popleft())
print(q)