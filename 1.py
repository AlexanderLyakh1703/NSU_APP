def get_or_create_eventloop():
    try:
        return ai.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = ai.new_event_loop()
            ai.set_event_loop(loop)
            return ai.get_event_loop()


def get_list_group_names(list_search) -> list[dict]:

    result = []
    urls = [
        f"https://table.nsu.ru/api/groups/search?id={search}" for search in list_search
    ]

    async def get_urls():
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:

            loop = ai.get_event_loop()
            futures = [
                loop.run_in_executor(
                    executor, lambda: requests.get(url, auth=(aconf.TABLE_TOKEN, ""))
                )
                for url in urls
            ]
            for response in await ai.gather(*futures):
                obj = json.loads(response.text)
                result.append(obj)

    loop = get_or_create_eventloop()
    loop.run_until_complete(get_urls())
    return result
