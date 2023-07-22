from django.shortcuts import render

from rest_framework import permissions
from rest_framework.views import APIView

from django.http import HttpResponse

import requests
import json

access_token = "AQXFlC_Md_Whj6LbCGqM9C4niZXNkBZk2y7f12XEN9xeUxZIbT9qXAsHynx3L6LzTP0xAcB4CKzxIaiM9cSNugezfyua9kHAwCbUY9fXcx9v_aMc1ucUM1yIPjallK1xGc4mAm0w5gRC56eiUV-QqpQmUWwXXeJ7U0L0ZXtMDFVkh8UmbztnxAQsVAIdWx_jDJtZb3DR1ut0AvIUKCjrLX0DoSN_FoxfyYVkMWs_2OIdkjjYGUxmJ4qOtV6yyq9GOt-WTonBQyVE6Pv2cMioXErcWBet6vwjnkBlHhr0ShsNbtVwyvmBtK4GjuqMuB_xkHKgqCITYv4OZEshgdctlpPcqd61kw"
linkedin_post_object = {
    "author": "urn:li:person:",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": "post is created from api"
            },
            "shareMediaCategory": "IMAGE",
            "media": [
                {
                    "status": "READY",
                    "description": {
                        "text": "Image through LinkedIn API"
                    },
                    "media": "urn:li:...",
                    "title": {
                        "text": "Test"
                    },
                }
            ]
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}
register_upload_object = {
    "registerUploadRequest": {
        "recipes": [
            "urn:li:digitalmediaRecipe:feedshare-image"
        ],
        "owner": "urn:li:person:",
        "serviceRelationships": [
            {
                "relationshipType": "OWNER",
                "identifier": "urn:li:userGeneratedContent"
            }
        ]
    }
}

# Create your views here.
class PostViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        print("get request")
        data = request.data
        image_file = request.FILES['file']
        heading = data['heading']
        description = data['description']
        print(image_file)
        res = requests.get('https://api.linkedin.com/v2/me', headers={'Authorization': 'Bearer ' + access_token})
        res = res.json()

        print(res['id'])
        obj = linkedin_post_object
        obj['author'] = linkedin_post_object['author'] + res['id']
        # obj["specificContent"]["com.linkedin.ugc.ShareContent"]["media"][0]["originalUrl"] = data['image']
        obj["specificContent"]["com.linkedin.ugc.ShareContent"]["media"][0]["title"]["text"] = heading
        print(obj)
        upload_obj = register_upload_object
        upload_obj['registerUploadRequest']['owner'] = register_upload_object['registerUploadRequest']['owner'] + res['id']
        res = requests.post("https://api.linkedin.com/v2/assets?action=registerUpload", data=json.dumps(upload_obj), headers={'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'})
        res = res.json()

        upload_url = res['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
        asset = res['value']['asset']
        print(upload_url)
        print(asset)
        print(image_file)
        res = requests.put(upload_url, data=image_file, headers={'Authorization': 'Bearer ' + access_token, 'Content-Type': 'image/png'})
        print(res.text)

        obj["specificContent"]["com.linkedin.ugc.ShareContent"]["media"][0]["media"] = asset
        res = requests.post("https://api.linkedin.com/v2/ugcPosts", data=json.dumps(obj), headers={'Authorization': 'Bearer ' + access_token,})
        if(res.status_code == 200):
            print(res.json())
        else:
            print(res.text)

        return HttpResponse("Post Request Called")