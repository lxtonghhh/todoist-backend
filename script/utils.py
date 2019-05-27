import asyncio, aiohttp


async def download_one_image(item):
    # print('生成一个协程', ip)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
        'Accept': '*/*',
    }
    async with aiohttp.ClientSession() as session:
        try:
            url, image_id, dirpath = item['url'], item['image_id'], item['dirpath']

            async with session.get(url, headers=headers, timeout=100,
                                   proxy_auth=aiohttp.BasicAuth('user', 'pass')) as res:
                c = res.status
                if c == 200:
                    # 逻辑
                    print("download ", dirpath + str(image_id) + '.jpg')
                    content = await res.read()
                    # print('content', content)
                    with open(dirpath + str(image_id) + '.jpg', 'wb') as f:
                        f.write(content)
                        print(image_id, "完成", url)

                else:
                    raise Exception
                    # print(ip, 'Unavailable,不可用')
        except asyncio.TimeoutError as e:
            print(image_id, "超时", url)
            raise Exception


def get_tasks(get_one_task_func, todolist):
    """

    :param get_one_task_func:异步函数
    :param todolist: [
        {"url":"xxx","image_id":"xxx","dirpath":"xxx"
    ]
    :return:
    """
    return [asyncio.ensure_future(get_one_task_func(item)) for item in todolist]


def async_download(todolist):
    print("开始异步下载：", todolist)
    loop = asyncio.get_event_loop()
    tasks = get_tasks(get_one_task_func=download_one_image, todolist=todolist)
    loop.run_until_complete(asyncio.wait(tasks))

