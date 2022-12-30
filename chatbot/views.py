import os

from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from campusdiscount import settings
from chatbot.forms import UserForm
from chatbot.models import User_Model, Store_Model


# Create your views here.
def keyboard(request):
    return JsonResponse({
        'type': 'text'
    })


@csrf_exempt
def message(request):
    answer = ((request.body).decode('utf-8'))
    userRequest_Json = json.loads(answer)
    userRequest_Block = userRequest_Json['userRequest']['block']['name']
    userRequest_Text = userRequest_Json['userRequest']['utterance']
    userRequest_User_ID = userRequest_Json['userRequest']['user']['id']
    User_Vaild = User_Model.objects.filter(user_id=userRequest_User_ID)

    if (userRequest_Block == "setup"):  # 블록 이름 확인
        if request.method == 'POST':
            if (User_Vaild == False):  # 이미 있는 유저인지 확인
                obj = User_Model(department=userRequest_Text, user_id=userRequest_User_ID)
                obj.save()
                User_Vaild = User_Model.objects.filter(user_id=userRequest_User_ID)
                if (User_Vaild == True):
                    return JsonResponse({
                        'version': "2.0",
                        'template': {
                            'outputs': [{
                                'simpleText': {
                                    'text': "초기세팅 성공"
                                }
                            }],
                        }
                    })
                else:
                    return JsonResponse({
                        'version': "2.0",
                        'template': {
                            'outputs': [{
                                'simpleText': {
                                    'text': "이미 세팅이 되어있습니다"
                                }
                            }],
                        }
                    })

    elif userRequest_Block == 'search':
        return JsonResponse({
            'version': "2.0",
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': "테스트 성공입니다."
                    }
                }],
            }
        })
    elif userRequest_Block == 'restaurant':
        User_Vaild = User_Model.objects.filter(user_id=userRequest_User_ID)
        if(User_Vaild):
            for store in Store_Model.objects.filter(favorite=True):
                fileDir = os.path.join(settings.MEDIA_ROOT, 'json')
                print(fileDir)
                fileName = "restaurant.json"
                with open(os.path.join(fileDir, fileName), 'r') as file:
                    json_res = json.load(file)
                data = json_res["template"]["outputs"][0]
                for i in data.values():
                    for j in i["items"]:
                        print(j)
                        if store.contents:
                            j["title"] = "제휴)" + store.store_name + " " + store.first_menu_name  # 메세지 제목 가게이름+메뉴
                        else:
                            j["title"] = store.store_name + " " + store.first_menu_name  # 메세지 제목 가게이름+메뉴

                        j["description"] = store.contents  # 메세지 본문
                        j["thumbnail"]["imageUrl"] = "https://campusdiscount.azurewebsites.net/media/" + str(store.first_menu_image)  # 메세지 이미지
                        for k in j["buttons"]:
                            k["webLinkUrl"] = store.naver_map_URL  # 네이버지도 URL버튼


                return JsonResponse(json_res)
        else:
            return JsonResponse({
                'version': "2.0",
                'template': {
                    'outputs': [{
                        'simpleText': {
                            'text': "단과대를 먼저 입력해주세요. ex 공대 공학대학"
                        }
                    }],
                }
            })

    else:
        return JsonResponse({
            'version': "2.0",
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': "테스트 실패입니다."
                    }
                }],
            }
        })
