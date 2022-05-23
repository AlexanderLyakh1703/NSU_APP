import asyncio as ai
import requests
import concurrent.futures
import json

import timeit
import sys


def timer(function):
    def new_function(*args, **kwargs):
        start_time = timeit.default_timer()
        res = function(*args, **kwargs)
        elapsed = timeit.default_timer() - start_time
        print(
            'Function "{name}" took {time} seconds to complete.'.format(
                name=function.__name__, time=elapsed
            )
        )
        return res

    return new_function


def get_or_create_eventloop():
    try:
        return ai.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = ai.new_event_loop()
            ai.set_event_loop(loop)
            return ai.get_event_loop()


@timer
def async_get_jsons(urls, max_workers=100, **kwargs):

    result = []

    async def get_urls():
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:

            loop = ai.get_event_loop()
            futures = [
                loop.run_in_executor(executor, lambda: requests.get(url, **kwargs))
                for url in urls
            ]
            for response in await ai.gather(*futures):
                obj = json.loads(response.text)
                print(response, file=sys.stderr)
                result.append(obj)

    loop = get_or_create_eventloop()
    loop.run_until_complete(get_urls())
    return result


@timer
def get_jsons(urls, **kwargs):
    result = []
    for url in urls:
        response = requests.get(url, **kwargs)
        result.append(json.loads(response.text))
        print(response, file=sys.stderr)
    return result
