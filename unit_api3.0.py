import urllib.request as urllib2
import json

class baidu_unit():
    token = ''

    # service_id: 机器人id
    # session_id: 实现多轮对话                  
    # log_id: AppID? 技能ID?                        # ,\"skill_ids\":[\"1188690\"]
    post_data_prefix = "{\"version\":\"3.0\",\"service_id\":\"S69358\",\"session_id\":\"\",\"log_id\":\"26227257\",\"request\":{\"terminal_id\":\"88888\",\"query\":\""

    def fetch_token(self):
        API_Key = ''
        Secret_Key = ''

        host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_Key}&client_secret={Secret_Key}'
        request = urllib2.Request(host)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        content = urllib2.urlopen(request).read()
        my_json = content.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        if data:
            self.token = data['access_token']
        else:
            print("[ERROR]: 调用unit时获取token失败")

    def get_unit_reply(self, user_text):
        url = 'https://aip.baidubce.com/rpc/2.0/unit/service/v3/chat?access_token=' + self.token

        post_data = self.post_data_prefix + user_text + "\"}}"
        # print(post_data)

        request = urllib2.Request(url, bytearray(post_data, 'utf8'))
        request.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(request)

        content_json = json.loads(response.read().decode('utf8'))  # 转为dict

        # 处理session_id：第一次请求是，session_id 值为空，以后应该填上返回的值，如此才能实现多轮会话
        if self.post_data_prefix[53] == '"':
            self.post_data_prefix = self.post_data_prefix[:53] + content_json['result']['session_id'] + self.post_data_prefix[53:]

        reply = content_json['result']['responses'][0]['actions'][0]['say']  # 提取回答
        print(f"[Bot]: {reply}")

        return reply