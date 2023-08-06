from espider import Spider


def response_filter(response):
    print('{}'.format(response.url))
    return response


def request_filter(req):
    print('222: {}'.format(req.url))
    return req


def pi(r):
    # print(r)
    return r


def pi2(r):
    # print(f'22:{r}')
    return r


class Wall(Spider):

    def prepare(self):
        # self.RESPONSE_MIDDLEWARES =
        # self.REQUEST_MIDDLEWARES = [response_filter, request_filter]
        self.ITEM_PIPELINES.extend([pi, pi2])
        # self.RESPONSE_MIDDLEWARES = []
        pass

    def start_requests(self):
        url = 'https://desk.zol.com.cn/fengjing/weimeiyijing/{}.html'
        for i in range(1, 20):
            yield self.request(url.format(i) + 'dawd')

    def parse(self, response, *args, **kwargs):
        urls = response.xpath('//a[@class="pic"]/img/@src').getall()
        for i in urls:
            yield self.request(i, callback=self.level_2)

    def level_2(self, response, *args, **kwargs):
        yield response
        yield response

    def close(self):
        pass


W = Wall()
W.start()
