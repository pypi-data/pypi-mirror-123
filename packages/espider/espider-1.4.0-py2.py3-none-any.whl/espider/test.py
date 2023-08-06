from espider import Spider
import time


async def print_url(u):
    print(u.url)
    return u


class Wall(Spider):
    def prepare(self):
        self.REQUEST_BATCH_SIZE = 10
        self.RESPONSE_MIDDLEWARES = print_url
        pass

    def start_requests(self):
        url = 'https://desk.zol.com.cn/fengjing/weimeiyijing/{}.html'

        for i in range(1, 10):
            yield self.request(url.format(i))

    def parse(self, response, *args, **kwargs):

        urls = response.xpath('//a/img/@src').getall()

        for i in urls:
            yield self.request(i, callback=self.level_1)

    def level_1(self, response, *args, **kwargs):
        yield response


W = Wall()
W.start()
