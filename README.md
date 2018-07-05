# HTTP Request Randomizer  [![Build Status](https://travis-ci.org/pgaref/HTTP_Request_Randomizer.svg?branch=master)](https://travis-ci.org/pgaref/HTTP_Request_Randomizer) [![Coverage Status](https://coveralls.io/repos/github/pgaref/HTTP_Request_Randomizer/badge.svg?branch=master)](https://coveralls.io/github/pgaref/HTTP_Request_Randomizer?branch=master) [![Requirements Status](https://requires.io/github/pgaref/HTTP_Request_Randomizer/requirements.svg?branch=la55u-master)](https://requires.io/github/pgaref/HTTP_Request_Randomizer/requirements/?branch=la55u-master) [![PyPI version](https://badge.fury.io/py/http-request-randomizer.svg)](https://badge.fury.io/py/http-request-randomizer)

[Vietnamese version](README-vi.md)

A convenient way to implement HTTP requests is using Pythons' **requests** library.
One of requests’ most popular features is simple proxying support.
HTTP as a protocol has very well-defined semantics for dealing with proxies, and this contributed to the widespread deployment of HTTP proxies

Proxying is very useful when conducting intensive web crawling/scrapping or when you just want to hide your identity (anonymization).

In this project I am using public proxies to randomise http requests over a number of IP addresses and using a variety of known user agent headers these requests look to have been produced by different applications and operating systems.


## Proxies

Proxies provide a way to use server P (the middleman) to contact server A and then route the response back to you. In more nefarious circles, it's a prime way to make your presence unknown and pose as many clients to a website instead of just one client.
Often times websites will block IPs that make too many requests, and proxies is a way to get around this. But even for simulating an attack, you should know how it's done.


## User Agent

Surprisingly, the only thing that tells a server the application triggered the request (like browser type or from a script) is a header called a "user agent" which is included in the HTTP request.

## The source code

The project code in this repository is crawling **four** different public proxy websites:
* http://proxyfor.eu/geo.php
* http://free-proxy-list.net
* http://rebro.weebly.com/proxy-list.html
* http://www.samair.ru/proxy/time-01.htm 

After collecting the proxy data and filtering the slowest ones it is randomly selecting one of them to query the target url.
The request timeout is configured at 30 seconds and if the proxy fails to return a response it is deleted from the application proxy list.
I have to mention that for each request a different agent header is used. The different headers are stored in the **/data/user_agents.txt** file which contains around 900 different agents.

## Installation
If you wish to use this module as a [CLI tool](#command-line-interface), install it globally via pip:
```
  pip install http-request-randomizer
```
   
Otherwise, you can clone the repository and use setup tools:
```
python setup.py install
```


## How to use

* [Command-line interface](#command-line-interface)
* [Library API](#api)

## Command-line interface

Assuming that you have **http-request-randomizer** installed, you can use the commands below:

show help message:
```
proxyList   -h, --help
```
specify proxy provider(s) (required):
```
  -s {proxyforeu,rebro,samair,freeproxy,all} 
```
Specify output stream (default: sys.stdout), could also be a file:
```
  -o, --outfile
```
specify provider timeout threshold in seconds:
```
  -t, --timeout
```
specify proxy bandwidth threshold in KBs:
```                        
  -bw, --bandwidth
```
show program's version number:
```                        
  -v, --version
```

## API


To use **http-request-randomizer** as a library, include it in your requirements.txt file.
Then you can simply generate a proxied request using a method call:

````python
import time
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

if __name__ == '__main__':

    start = time.time()
    req_proxy = RequestProxy()
    print("Initialization took: {0} sec".format((time.time() - start)))
    print("Size: {0}".format(len(req_proxy.get_proxy_list())))
    print("ALL = {0} ".format(list(map(lambda x: x.get_address(), req_proxy.get_proxy_list()))))

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

## Documentation 

[http-request-randomizer documentation](http://pythonhosted.org/http-request-randomizer)


## Contributing

Many thanks to the open-source community for
 [contributing](https://github.com/pgaref/HTTP_Request_Randomizer/blob/master/CONTRIBUTORS.md) to this project!


## Faced an issue?

Open an issue [here](https://github.com/pgaref/HTTP_Request_Randomizer/issues), and be as detailed as possible :)

## Feels like a feature is missing?

Feel free to open a ticket! PRs are always welcome!

## License

This project is licensed under the terms of the MIT license.
