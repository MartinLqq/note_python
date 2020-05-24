def simple_middleware(get_response):
    print('第一次配置和初始化的时候执行一次')
    print(get_response)

    def middleware(request):
        print('每个请求处理视图前被执行')

        response = get_response(request)

        # 此处代码会在每个请求处理视图之后被执行
        print('每个请求处理视图之后被执行')

        return response

    return middleware
