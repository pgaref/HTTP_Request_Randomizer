from httmock import urlmatch


free_proxy_expected = ['http://138.197.136.46:3128', 'http://177.207.75.227:8080']
proxy_for_eu_expected = ['http://107.151.136.222:80', 'http://37.187.253.39:8115']
rebro_weebly_expected = ['http://213.149.105.12:8080', 'http://119.188.46.42:8080']
samair_expected = ['http://191.252.61.28:80', 'http://167.114.203.141:8080']

@urlmatch(netloc=r'(.*\.)?free-proxy-list\.net$')
def free_proxy_mock(url, request):
    return """<table border="0" cellpadding="0" cellspacing="0" id="proxylisttable"
id="proxylisttable">\n
<thead>\n
<tr>\n
    <th>IP Address</th>
    \n
    <th>Port</th>
    \n
    <th>Code</th>
    \n
    <th>Country</th>
    \n
    <th>Anonymity</th>
    \n
    <th>Google</th>
    \n
    <th>Https</th>
    \n
    <th>Last Checked</th>
    \n
</tr>
\n
</thead>
\n
<tbody>
<tr>
    <td>138.197.136.46</td>
    <td>3128</td>
    <td>CA</td>
    <td>Canada</td>
    <td>anonymous</td>
    <td>no</td>
    <td>no</td>
    <td>7 seconds ago</td>
</tr>
\n
<tr>
    <td>177.207.75.227</td>
    <td>8080</td>
    <td>BR</td>
    <td>Brazil</td>
    <td>transparent</td>
    <td>no</td>
    <td>no</td>
    <td>2 hours 21 minutes ago</td>
</tr>
\n
</tbody>
\n
<tfoot>\n
<tr>\n
    <th class="input"><input type="text"/></th>
    \n
    <th></th>
    \n
    <th></th>
    \n
    <th></th>
    \n
    <th></th>
    \n
    <th></th>
    \n
    <th></th>
    \n
    <th></th>
    \n
</tr>
\n
</tfoot>
\n
</table>"""


@urlmatch(netloc=r'(.*\.)?proxyfor\.eu')
def proxy_for_eu_mock(url, request):
    return """<table class="proxy_list">
    <tr>
        <th>IP</th>
        <th>Port</th>
        <th>Country</th>
        <th>Anon</th>
        <th>Speed</th>
        <th> Check</th>
        <th>Cookie/POST</th>
    </tr>
    <tr>
        <td>107.151.136.222</td>
        <td>80</td>
        <td>United States</td>
        <td>HIGH</td>
        <td>1.643</td>
        <td>2016-04-12 17:02:43</td>
        <td>Yes/Yes</td>
    </tr>
    <tr>
        <td>37.187.253.39</td>
        <td>8115</td>
        <td>France</td>
        <td>HIGH</td>
        <td>12.779</td>
        <td>2016-04-12 14:36:18</td>
        <td>Yes/Yes</td>
    </tr>
</table>"""


@urlmatch(netloc=r'(.*\.)?rebro\.weebly\.com$')
def rebro_weebly_mock(url, request):
    return """<div class="paragraph" style="text-align:left;"><strong><font color="#3ab890"
                                                              size="3"><font
        color="#d5d5d5">IP:Port</font></font></strong><br/><font
        size="2"><strong><font color="#33a27f">213.149.105.12:8080<br/>119.188.46.42:8080</font></strong></font><br/><span></span>
</div>"""


@urlmatch(netloc=r'(.*\.)?www.samair.ru')
def samair_mock(url, request):
    return """<table id="proxylist">\n
    <tr class="list_sorted">\n
        <th><a href="http://samair.ru/proxy/ip-address-01.htm"
               title="Proxy List sorted by ip address">IP address</a></th>
        \n
        <th><a href="http://samair.ru/proxy/proxy-01.htm"
               title="Proxy List sorted by anonymity level">Anonymity level</a>
        </th>
        \n
        <th><a href="http://samair.ru/proxy/time-01.htm"
               title="Proxy List sorted by updated time">Checked time</a></th>
        \n
        <th><a href="http://samair.ru/proxy/type-01.htm"
               title="Proxy list sorted by country">Country</a></th>
        \n
        <th><dfn title="City or State\\Region ">City</dfn></th>
        \n
        <th><dfn title="Internet Service Provider">ISP</dfn></th>
        \n
    </tr>
    \n
    <tr class="elite">
        <td>191.252.61.28:80</td>
        <td>high-anonymous</td>
        <td>Apr-18, 17:18</td>
        <td>Brazil</td>
        <td>S\xe3o Jos\xe9 Dos Campos</td>
        <td><dfn title="Locaweb Servi\xe7os de Internet S/A">Locaweb
            Servi\xe7o...</dfn></td>
    </tr>
    \n
    <tr class="transp">
        <td>167.114.203.141:8080</td>
        <td>transparent</td>
        <td>Apr-18, 13:22</td>
        <td>Canada</td>
        <td>Montr\xe9al (QC)</td>
        <td>OVH Hosting</td>
    </tr>
    \n
</table>"""
