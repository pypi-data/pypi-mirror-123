import asyncio

from tracardi_url_parser.plugin import ParseURLParameters
from tracardi.domain.session import Session


async def main():
    init = {
        "url": 'session@context.page.url'
    }

    payload = {}

    plugin = ParseURLParameters(**init)
    plugin.session = Session(
        id='1',
        context={
            'page': {
                'url': "http://test.url/path/?param=1#hash"
            }
        }
    )

    return await plugin.run(payload)


result = asyncio.run(main())
print(result)
