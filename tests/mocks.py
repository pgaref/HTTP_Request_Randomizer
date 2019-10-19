from httmock import urlmatch


free_proxy_expected = ['138.197.136.46:3128', '177.207.75.227:8080']
proxy_for_eu_expected = ['107.151.136.222:80', '37.187.253.39:8115']
rebro_weebly_expected = ['213.149.105.12:8080', '119.188.46.42:8080']
prem_expected = ['191.252.61.28:80', '167.114.203.141:8080', '152.251.141.93:8080']
sslproxy_expected = ['24.211.89.146:8080', '187.84.222.153:80', '41.193.238.249:8080']

@urlmatch(netloc=r'(.*\.)?sslproxies\.org$')
def sslproxy_mock(url, request):
    return """<table class="table table-striped table-bordered" cellspacing="0" width="100%" id="proxylisttable">
    <thead>
    <tr>
        <th>IP Address</th>
        <th>Port</th>
        <th>Code</th>
        <th class='hm'>Country</th>
        <th>Anonymity</th>
        <th class='hm'>Google</th>
        <th class='hx'>Https</th>
        <th class='hm'>Last Checked</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>24.211.89.146</td>
        <td>8080</td>
        <td>US</td>
        <td class='hm'>United States</td>
        <td>elite proxy</td>
        <td class='hm'>no</td>
        <td class='hx'>yes</td>
        <td class='hm'>8 seconds ago</td>
    </tr>
    <tr>
        <td>187.84.222.153</td>
        <td>80</td>
        <td>BR</td>
        <td class='hm'>Brazil</td>
        <td>anonymous</td>
        <td class='hm'>no</td>
        <td class='hx'>yes</td>
        <td class='hm'>1 minute ago</td>
    </tr>
    <tr>
        <td>41.193.238.249</td>
        <td>8080</td>
        <td>ZA</td>
        <td class='hm'>South Africa</td>
        <td>elite proxy</td>
        <td class='hm'>no</td>
        <td class='hx'>yes</td>
        <td class='hm'>1 minute ago</td>
    </tr>
    </tbody>
    <tfoot>
        <tr>
        <th class="input"><input type="text" /></th>
        <th></th><th></th>
        <th class='hm'></th>
        <th></th>
        <th class='hm'></th>
        <th class='hx'></th>
        <th class='hm'></th>
        </tr>
    </tfoot>
</table>
        """

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
    return """<div class="paragraph" style="text-align:left;"><strong><font color="#3ab890" size="3"><font
        color="#d5d5d5">IP:Port</font></font></strong><br/><font
        size="2"><strong><font color="#33a27f">213.149.105.12:8080<br/>119.188.46.42:8080</font></strong></font><br/><span></span>
</div>


<div class="paragraph" style="text-align:left;"><font size="2"><strong><font size="3"><font color="#3ab890">Country</font></font></strong></font><font size="2">
    <br />Montenegro<br />China<br /></font><br /><span></span>
</div>

<div class="paragraph" style="text-align:left;"><font size="2"><strong><font color="#3ab890" size="3">Status</font></strong></font><br /><font size="2">
    Elite &amp; Anonymous<br />Elite &amp; Anonymous<br /></font><br /><span></span>
</div>

"""


@urlmatch(netloc=r'(.*\.)?www\.premproxy\.com')
def prem_mock(url, request):
    return """
    <head>
        <script src="/js/test.js"></script>
    </head>
    <div id="proxylist">\n
    <tr class="anon">\n
        <th><a href="/list/ip-address-01.htm" title="Proxy List sorted by ip address">IP address</a></th>
        \n
        <th><a href="/list/" title="Proxy List sorted by anonymity level">Anonymity</a></th>
        \n
        <th><a href="/list/time-01.htm" title="Proxy List sorted by updated time">Checked</a></th>
        \n
        <th><a href="/list/type-01.htm" title="Proxy list sorted by country">Country</a></th>
        \n
        <th><dfn title="City or State\\Region ">City</dfn></th>
        \n
        <th><dfn title="Internet Service Provider">ISP</dfn></th>
        \n
    </tr>
    \n
    <div id="navbar">
        <ul class="pagination"><li class="active"><a href="/list/">1</a></li><li><a href="02.htm">2</a></li></ul>
    </div>
    \n
    <tr class="anon">
        <td data-label="IP:port "><span><input type="checkbox" name="proxyIp[]" value="191.252.61.28|r60e6"></span>191.252.61.28:<span class="r60e6"></span></td>
        <td data-label="Anonymity Type: ">high-anonymous</td>
        <td data-label="Checked: ">Apr-18, 17:18</td>
        <td data-label="Country: ">Brazil</td>
        <td data-label="City: ">S\xe3o Jos\xe9 Dos Campos</td>
        <td data-label="ISP: "><dfn title="Locaweb Servi\xe7os de Internet S/A">Locaweb
            Servi\xe7o...</dfn></td>
    </tr>
    \n
    <tr class="anon">
        <td data-label="IP:port "><span><input type="checkbox" name="proxyIp[]" value="167.114.203.141|r63c5"></span>167.114.203.141:<span class="r63c5"></span></td>
        <td data-label="Anonymity Type: ">transparent</td>
        <td data-label="Checked: ">Apr-18, 13:22</td>
        <td data-label="Country: ">Canada</td>
        <td data-label="City: ">Montr\xe9al (QC)</td>
        <td data-label="ISP: ">OVH Hosting</td>
    </tr>
    \n
    <tr class="anon">
        <td data-label="IP:port "><span><input type="checkbox" name="proxyIp[]" value="152.251.141.93|r63c5"></span>152.251.141.93:<span class="r63c5"></span></td>
        <td data-label="Anonymity Type: ">elite </td>
        <td data-label="Checked: ">Jul-16, 04:39</td>
        <td data-label="Country: ">Brazil</td>
        <td data-label="City: ">&nbsp;</td>
        <td data-label="ISP: ">Vivo</td>
    </tr>
    \n
    <tr><td colspan="6"><span><input type="checkbox" name="" value="" onclick="checkAll(this)"></span>Select All Proxies</td></tr>
</div>"""


@urlmatch(netloc=r'(.*\.)?www\.premproxy\.com', path='/js/test.js', method='get', scheme='https')
def prem_js_mock(url, request):
    return b"eval(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};" \
           b"if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\\\w+'};c=1};" \
           b"while(c--){if(k[c]){p=p.replace(new RegExp('\\\\b'+e(c)+'\\\\b','g'),k[c])}}return p}('$(t).u(v(){$(\\'.s\\').0(r);" \
           b"$(\\'.n\\').0(o);$(\\'.p\\').0(q);$(\\'.w\\').0(x);$(\\'.D\\').0(E);$(\\'.F\\').0(C);$(\\'.B\\').0(y);$(\\'.z\\').0(A);" \
           b"$(\\'.m\\').0(i);$(\\'.7\\').0(8);$(\\'.9\\').0(6);$(\\'.4\\').0(1);$(\\'.2\\').0(5);$(\\'.3\\').0(a);$(\\'.l\\').0(b);" \
           b"$(\\'.j\\').0(k);$(\\'.h\\').0(g);$(\\'.c\\').0(d);$(\\'.e\\').0(f);$(\\'.G\\').0(1n);$(\\'.H\\').0(1b);$(\\'.1c\\').0(19);" \
           b"$(\\'.18\\').0(14);$(\\'.15\\').0(16);$(\\'.17\\').0(1d);$(\\'.1e\\').0(1k);$(\\'.1l\\').0(1m);$(\\'.1j\\').0(1i);$(\\'.1f\\').0(1g);" \
           b"$(\\'.1h\\').0(13);$(\\'.12\\').0(O);$(\\'.P\\').0(Q);$(\\'.N\\').0(M);$(\\'.I\\').0(J);$(\\'.K\\').0(L);$(\\'.R\\').0(S);$(\\'.Z\\').0(10)" \
           b";$(\\'.11\\').0(Y);$(\\'.X\\').0(T);$(\\'.U\\').0(V);$(\\'.W\\').0(1a)});',62,86,'html|20183|r97e1|rff0a|r117f|65103|65205|r76d3|52335|r21e1|" \
           b"62225|9000|r2e7b|81|r0d8a|9797|6666|r1f9b|28080|rdde2|31773|rf51a|rd687|r1c53|53281|raceb|3128|8080|r63c5|document|ready|function|r60e6|80|8888|" \
           b"r6ec1|8181|rb058|8197|r40ed|8081|re3f0|r28a8|r55d0|ra6df|8090|r4381|8000|53282|r125a|8082|r2f55|2016|r6714|47753|55012|rb59a|9090|ra346|r4b77|54214|" \
           b"rd762|1080|rc6d0|r9946|60088|9999|r3e10|8118|r7f82|r371f|54314|63909|41258|r8065|8380|rf914|r9e8e|8088|r3c82|808|r3165|8383|r6643|555|3130'.split('|'),0,{}))\n"
