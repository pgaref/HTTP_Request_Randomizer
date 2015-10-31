# HTTP Request Randomizer in Python

A convenient way to implement HTTP requests is using Pythons' **requests** library.
One of requests’ most popular features is simple proxying support.
HTTP as a protocol has very well-defined semantics for dealing with proxies, and this contributed to the widespread deployment of HTTP proxies

Proxying is very useful when conducting intensive web crawling/scrapping or when you just want to hide your identity (anomization).

In this project I am using public proxies to randomise over a number of IP addresses and a variety of known user agents to generate requests that look to be produced by different applications and operating systems.


## Proxies

Proxies are a way to tell server P (the middleman) to contact server A and then route the response back to you. In more nefarious circles, it's a prime way to make your presence unknown and pose as many clients to a website instead of just one client.
Often times websites will block IPs that make too many requests, and proxies is a way to get around this. But even for simulating an attack, you should know how it's done.


## User Agent

Surprisingly, the only thing that tells a server the application triggered the request (like browser type or from a script) is a header called a "user agent" which is included in the HTTP request.

## The source code

The project code in this repository is crawling two different public proxy websites http://proxyfor.eu/geo.php and http://free-proxy-list.net.
After collecting the proxy data and filtering the slowest ones it is randomly selecting one of them to query the target url.
The request timeout is configured at 30 seconds and if the proxy fails to return a response it is deleted from the application proxy list.
I have to mention that for each request a different agent header is used. This headers are strong in the **/data/user_agents.txt** file which contains around 900 different agents.
