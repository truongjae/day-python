import requests
import base64
import threading
from time import sleep as sl
import io
from PIL import Image
import json
def convert_string_to_json_cookies(cookies):
	cookies = cookies.replace(" ","")
	list_cookies = cookies.split(";")
	

	json_cookies = dict()

	for cookie in list_cookies:
		if cookie != '':
			cut_cookie = cookie.split("=")
			key = cut_cookie[0]
			value = cut_cookie[1]
			json_cookies[key] = value
	return json_cookies
def get_fb_dtsg(cookies):
	url = "https://facebook.com"
	p = requests.get(url,cookies=cookies)
	data = p.text
	key = '["DTSGInitialData",[],{"token":"'
	data = cut_string('["DTSGInitialData",[],{"token":"',data,True)
	data = cut_string('"',data,False)
	return data

def cut_string(key,data,option):
	if option:
		index = data.find(key)
		data = data[index+len(key):]
		return data
	else:
		index = data.find(key)
		return data[:index]
def get_post_id_from_url(url,cookies):
	p = requests.get(url,cookies=cookies)
	data = p.text
	arrKey = ['"params":{"story_fbid":"','"params":{"fbid":"','"story_token":"']
	for key in arrKey:
		if data.find(key) != -1:
			result = cut_string(key,data,True)
			result = cut_string('"',result,False)
			return result
	return None

def spam_comment(text,post_id,cookies):
	url = "https://www.facebook.com/api/graphql/"
	fb_dtsg = get_fb_dtsg(cookies)
	post_id_encode = base64.b64encode(("feedback:"+post_id).encode()).decode()
	actor_id = cookies['c_user']
	# print(post_id_encode)
	data = {
		'fb_dtsg': fb_dtsg,
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
		    "feedback_id": "'''+post_id_encode+'''",
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
		    "actor_id": "'''+actor_id+'''",
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


def post_newfeed(cookies,fb_dtsg,image_id,content):
	user_id = cookies['c_user']
	url = 'https://www.facebook.com/api/graphql/'
	data = {
		'fb_dtsg': fb_dtsg,
		'variables': '''{
			  "input": {
			    "composer_entry_point": "inline_composer",
			    "composer_source_surface": "newsfeed",
			    "composer_type": "feed",
			    "source": "WWW",
			    "attachments": [
			      {
			        "photo": {
			          "id": "'''+image_id+'''"
			        }
			      }
			    ],
			    "audience": {
			      "privacy": {
			        "allow": [],
			        "base_state": "SELF",
			        "deny": [],
			        "tag_expansion_state": "UNSPECIFIED"
			      }
			    },
			    "message": {
			      "ranges": [],
			      "text": "'''+content+'''"
			    },
			    "with_tags_ids": [],
			    "inline_activities": [],
			    "explicit_place_id": "0",
			    "text_format_preset_id": "0",
			    "logging": {
			      "composer_session_id": ""
			    },
			    "navigation_data": {
			      "attribution_id_v2": "CometHomeRoot.react,comet.home,tap_tabbar,1666883493754,714515,4748854339,"
			    },
			    "tracking": [
			      null
			    ],
			    "actor_id": "'''+user_id+'''",
			    "client_mutation_id": "2"
			  },
			  "displayCommentsFeedbackContext": null,
			  "displayCommentsContextEnableComment": null,
			  "displayCommentsContextIsAdPreview": null,
			  "displayCommentsContextIsAggregatedShare": null,
			  "displayCommentsContextIsStorySet": null,
			  "feedLocation": "NEWSFEED",
			  "feedbackSource": 1,
			  "focusCommentID": null,
			  "gridMediaWidth": null,
			  "groupID": null,
			  "scale": 1,
			  "privacySelectorRenderLocation": "COMET_STREAM",
			  "renderLocation": "homepage_stream",
			  "useDefaultActor": false,
			  "inviteShortLinkKey": null,
			  "isFeed": true,
			  "isFundraiser": false,
			  "isFunFactPost": false,
			  "isGroup": false,
			  "isEvent": false,
			  "isTimeline": false,
			  "isSocialLearning": false,
			  "isPageNewsFeed": false,
			  "isProfileReviews": false,
			  "isWorkSharedDraft": false,
			  "UFI2CommentsProvider_commentsKey": "CometModernHomeFeedQuery",
			  "hashtag": null,
			  "canUserManageOffers": false
			}''',
			'doc_id': '5737011653023776'
	}
	p = requests.post(url,data=data,cookies=cookies)
	# print(p.text)

def image_to_byte_array(image:Image):
	imgByteArr = io.BytesIO()
	image.save(imgByteArr, format=image.format)
	imgByteArr = imgByteArr.getvalue()
	return imgByteArr

def upload_image(cookies,fb_dtsg,filename):
	user_id = cookies['c_user']
	img = Image.open(filename)
	img_arr = image_to_byte_array(img)
	url = "https://upload.facebook.com/ajax/react_composer/attachments/photo/upload?av="+user_id+"&__user="+user_id+"&__a=1&fb_dtsg="+fb_dtsg
	data = {
		'source': '8',
		'profile_id': user_id,
		'waterfallxapp': 'comet',
		'upload_id': 'jsc_c_18m',
	}
	files = {
		'farr': img_arr
	}
	p = requests.post(url,data=data,files=files,cookies=cookies)
	resp = p.text
	resp = resp[9:]
	resp_json = json.loads(resp)
	return resp_json['payload']['photoID']


cookies = "sb=-ZhVYhyKeolDfKxOOXwyllD-;datr=-ZhVYuRotzANNQY6XRJjZ4NF;locale=vi_VN;c_user=100029031824085;m_page_voice=100029031824085;xs=50%3AVvUa4-zZhKw55Q%3A2%3A1666623371%3A-1%3A6328%3A%3AAcVsw6w8Ie4n1o2bCfci1Mi-00eekHkKiQOZjCccTqU;fr=0b4emdyTjzK3FApiu.AWW-wp_ffRALObr9nVF8XJI6x48.BjWoZ7.Iy.AAA.0.0.BjWo5E.AWVnk1PcWas;presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1666879328226%2C%22v%22%3A1%7D;wd=998x874;"
cookies = convert_string_to_json_cookies(cookies)

user_id = cookies['c_user']

fb_dtsg = get_fb_dtsg(cookies)
print(fb_dtsg)

image_id = upload_image(cookies,fb_dtsg,'thiennhien.jpg')
print(image_id)
content = "day la noi dung dang bai"

post_newfeed(cookies,fb_dtsg,image_id,content)