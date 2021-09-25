if __name__ == '__main__':
    import requests

    cookies = {
        'azkaban.warn.message': '',
        'azkaban.failure.message': '',
        'JSESSIONID': 'o03n192ck6bdwbez3ug1iwk6',
        'azkaban.browser.session.id': '62738959-0c81-40a2-ac7e-45b32f80a3ad',
        'azkaban.success.message': '',
    }

    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://192.168.200.100:8443',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://192.168.200.100:8443/manager?project=aaaa',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    }

    data = {
        'projectId': '1',
        'project': 'aaaa',
        'ajax': 'scheduleCronFlow',
        'flow': 'ORA2PG_DONE',
        'disabled': '[]',
        'failureEmailsOverride': 'false',
        'successEmailsOverride': 'false',
        'failureAction': 'finishCurrent',
        'failureEmails': '',
        'successEmails': '',
        'notifyFailureFirst': 'false',
        'notifyFailureLast': 'false',
        'concurrentOption': 'skip',
        'projectName': 'aaaa',
        'cronExpression': '0 12 12 ? * * '
    }

    response = requests.post('https://192.168.200.100:8443/schedule', headers=headers, cookies=cookies, data=data,
                             verify=False)

    print(response.status_code)
    print(response.json())