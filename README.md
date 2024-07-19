# 子域名收集方法

## 1. 利用证书透明度收集子域

1. **crtsh**: [https://crt.sh/](https://crt.sh/)
2. **facebook**: [https://developers.facebook.com/tools/ct](https://developers.facebook.com/tools/ct) 需要登录
3. **entrust**: [https://www.entrust.com/ct-search/](https://www.entrust.com/ct-search/)
4. **certspotter**: [https://sslmate.com/certspotter/api/](https://sslmate.com/certspotter/api/)

## 2. 域传送

### 1. 使用 `dig` 命令

```sh
dig +short exampe.com
```

## 3. 利用 DNS 查询收集子域

### SRV 记录

添加服务记录服务器服务记录时会添加此项，SRV 记录了哪台计算机提供了哪个服务。格式为：服务的名字.协议的类型（例如：example-server.tcp）。

### MX 记录

建立电子邮箱服务，将指向邮件服务器地址，需要设置 MX 记录。建立邮箱时，一般会根据邮箱服务商提供的 MX 记录填写此记录。

```sh
nslookup
```

### NS 记录

域名解析服务器记录，如果要将子域名指定某个域名服务器来解析，需要设置 NS 记录。

### SOA 记录

SOA 叫做起始授权机构记录，NS 用于标识多台域名解析服务器，SOA 记录用于在众多 NS 记录中那一台是主服务器。

### TXT 记录

可任意填写，可为空。一般做一些验证记录时会使用此项，如：做 SPF（反垃圾邮件）记录。

## 4. 利用 DNS 数据集收集子域

1. **ip138**: [https://site.ip138.com/{domain}/domain.htm](https://site.ip138.com/{domain}/domain.htm)
2. **百度云观测**: [http://ce.baidu.com/index/getRelatedSites?site_address={domain}](http://ce.baidu.com/index/getRelatedSites?site_address={domain})
3. **hackertarget**: [https://hackertarget.com/find-dns-host-records/](https://hackertarget.com/find-dns-host-records/)
4. **riddler**: [https://riddler.io/search?q=pld:{domain}](https://riddler.io/search?q=pld:{domain})
5. **bufferover**: [https://dns.bufferover.run/dns?q={domain}](https://dns.bufferover.run/dns?q={domain})
6. **dnsdb**: [https://dnsdb.io/zh-cn/search?q={domain}](https://dnsdb.io/zh-cn/search?q={domain})
7. **netcraft**: [https://searchdns.netcraft.com/](https://searchdns.netcraft.com/)
8. **findsubdomains**: [https://findsubdomains.com/](https://findsubdomains.com/)

## 5. 利用威胁情报平台数据收集子域

1. **AlienVault OTX**: [https://otx.alienvault.com/api/v1/indicators/domain/{domain}/{section}](https://otx.alienvault.com/api/v1/indicators/domain/{domain}/{section})
   - `{section}` 指其他指令动作，可参考 [Docs](https://otx.alienvault.com/api/v1/indicators/domain/qq.com/url_list) 关于 API 的使用说明。

2. **RiskIQ**: [https://community.riskiq.com/search/{domain}/subdomains](https://community.riskiq.com/search/{domain}/subdomains)
3. **ThreatBook**: [https://x.threatbook.cn/nodev4/domain/{domain}](https://x.threatbook.cn/nodev4/domain/{domain})
   - API: [https://api.threatbook.cn/v3/domain/sub_domains](https://api.threatbook.cn/v3/domain/sub_domains)
4. **ThreatMiner**: [https://www.threatminer.org/domain.php?q={domain}](https://www.threatminer.org/domain.php?q={domain})
5. **VirusTotal**:
   - [https://www.virustotal.com/ui/domains/{domain}/subdomains](https://www.virustotal.com/ui/domains/{domain}/subdomains)
   - [https://www.virustotal.com/gui/domain/{domain}/relations](https://www.virustotal.com/gui/domain/{domain}/relations)
6. **Pentest-Tools**: [https://pentest-tools.com/information-gathering/find-subdomains-of-domain#](https://pentest-tools.com/information-gathering/find-subdomains-of-domain#)

## 6. 利用搜索引擎发现子域

1. **谷歌搜索语法**: `site`
2. **IP 搜索**: `Site:x.x.x. *(目标IP)`

## 7. 域名备案搜集资产

- [www.beianbeian.com](http://www.beianbeian.com)

## 8. Whois 查询和关联查询

## 9. 域名爆破

爆破的原理是通过枚举的方式实现的，通过不断拼接字典中的内容去枚举域名的 A 记录。该方法一般需要解决泛解析问题。比如开源工具 OneForAll 会首先访问一个随机的并不存在的域，通过返回结果判断是否存在泛解析，确定存在泛解析以后，程序会开始不断循环产生随机域名，去向服务器查询，将每次查询到的 IP 和 TTL 记录下来，直到大部分的 IP 地址出现次数都大于两次，则 IP 黑名单的收集结束。在得到了 IP 黑名单以后，OneForAll 接下来会将自己的字典中的每一项和要指定查询的域名进行拼接。在爆破过程中根据 IP 黑名单进行过滤。但这种宽泛的过滤容易导致漏报，所以 OneForAll 将 TTL 也作为黑名单规则的一部分，评判的依据是：在权威 DNS 中，泛解析记录的 TTL 肯定是相同的，如果子域名记录相同，但 TTL 不同，那这条记录可以说肯定不是泛解析记录。

## 各种细节

1. 网站的 `crossdomain.xml` 文件和返回包中的 `Access-Control-Allow-Origin` 头
2. 返回包中的 `CSP（Content-Security-Policy）` 头
3. 网站 `robots` 文件
4. 网站 `sitemap` 文件
