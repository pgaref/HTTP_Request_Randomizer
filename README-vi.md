# HTTP Request Randomizer  [![Build Status](https://travis-ci.org/pgaref/HTTP_Request_Randomizer.svg?branch=master)](https://travis-ci.org/pgaref/HTTP_Request_Randomizer) [![Coverage Status](https://coveralls.io/repos/github/pgaref/HTTP_Request_Randomizer/badge.svg?branch=master)](https://coveralls.io/github/pgaref/HTTP_Request_Randomizer?branch=master) [![Dependency Status](https://gemnasium.com/badges/github.com/pgaref/HTTP_Request_Randomizer.svg)](https://gemnasium.com/github.com/pgaref/HTTP_Request_Randomizer) [![PyPI version](https://badge.fury.io/py/http-request-randomizer.svg)](https://badge.fury.io/py/http-request-randomizer)

[View English version of this file here](README.md)

Thư viện này cung cấp để cải tiến cách thực thi các request HTTP của thư viện **requests** trong Python. Một trong những tính năng rất cần thiết đó là hỗ trợ proxy. HTTP được thiết kế rất tốt để làm việc với proxy.

Proxy rất hữu ích khi làm các công việc liên quan đến thu thập dữ liệu web hoặc đơn giản là khi bạn muốn ẩn danh (anomization).

Trong dự án này tôi sử dụng các proxy được cung cấp trên mạng và sử dụng nhiều user-agent khác nhau để gửi các request http bằng những IP ngẫu nhiên.

## Proxy là gì

Proxy cho phép sử dụng máy chủ P (trung gian) để liên lạc với máy chủ A và sau đó phản hồi lại cho bạn kết quả. Một cách nói khác, việc này giúp ẩn đi sự hiện diện của bạn khi truy cập vào một trang web, website sẽ hiểu đây là truy cập từ nhiều người thay vì chỉ một người duy nhất.

Thông thường, các trang web sẽ chặn các địa chỉ IP gửi quá nhiều request, và proxy là một cách để giải quyết vấn đề này. Bạn có thể lợi dụng proxy để thực hiện tấn công một website, nhưng tốt hơn bạn nên hiểu cách proxy hoạt động như thế nào ;)

## User-Agent là gì

User-agent chỉ là một giá trị gửi kèm trong HTTP request để giúp máy chủ web có thể giả lập trình duyệt và gửi yêu cầu đến một website bất kỳ.

## Mã nguồn

Mã nguồn trong repository này sẽ thực hiện lấy proxy từ **bốn** website khác nhau:
* http://proxyfor.eu/geo.php
* http://free-proxy-list.net
* http://rebro.weebly.com/proxy-list.html
* http://www.samair.ru/proxy/time-01.htm 

Sau khi thu thập danh sách các proxy và loại bỏ những proxy chậm nó sẽ lấy ngẫu nhiên một proxy để gửi request đến url được chỉ định.
Thời gian chờ được thiết lập là 30 giây và nếu proxy không phản hồi kết quả nó sẽ được xóa bỏ trong danh sách proxy.
Tôi phải nhắc lại rằng mỗi request được gửi bằng một user-agent khác nhau, danh sách user-agent (khoảng 900 chuỗi khác nhau) được lưu trong file **/data/user_agents.txt**

## Làm sao để sử dụng?

Project này đã được phân phối như là một thư viện PyPI!
Đây là phần source code mẫu cho việc sử dụng thư viện này. Bạn chỉ cần thêm **http-request-randomizer** vào file requirements.txt và chạy đoạn code dưới đây:

````python
import time
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

if __name__ == '__main__':

    start = time.time()
    req_proxy = RequestProxy()
    print("Initialization took: {0} sec".format((time.time() - start)))
    print("Size: {0}".format(len(req_proxy.get_proxy_list())))
    print("ALL = {0} ".format(req_proxy.get_proxy_list()))

    test_url = 'http://ipv4.icanhazip.com'

    while True:
        start = time.time()
        request = req_proxy.generate_proxied_request(test_url)
        print("Proxied Request Took: {0} sec => Status: {1}".format((time.time() - start), request.__str__()))
        if request is not None:
            print("\t Response: ip={0}".format(u''.join(request.text).encode('utf-8')))
        print("Proxy List Size: {0}".format(len(req_proxy.get_proxy_list())))

        print("-> Going to sleep..")
        time.sleep(10)
````

## Tài liệu 

[http-request-randomizer documentation](http://pythonhosted.org/http-request-randomizer)


## Đóng góp

Mọi đóng góp của bạn luôn được trân trọng. Đừng ngần ngại gửi pull request cho chúng tôi.

## Bạn gặp vấn đề với thư viện này?

Hãy nêu lên vấn đề của bạn [tại đây](https://github.com/pgaref/HTTP_Request_Randomizer/issues), và càng chi tiết càng tốt. Chúng tôi sẽ hỗ trợ bạn trong sớm nhất có thể :)

## Giấy phép

Dự án này được cấp phép theo các điều khoản của giấy phép MIT.
