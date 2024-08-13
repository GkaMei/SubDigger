# SubDigger

👊 **SubDigger** 是一款强大的子域收集工具

## 🎉 项目简介

在渗透测试中，信息收集是成功的关键环节，而子域名收集则是这一过程中的重要组成部分。本插件旨在提供一种高效、准确的方式来进行被动和主动的子域名收集，帮助安全研究人员和渗透测试人员更好地识别目标的潜在攻击面。

本插件支持快速的被动子域名收集，同时也支持主动收集和字典爆破，以满足不同场景下的需求。

### 功能特点

- **被动扫描**：通过分析公共数据源，快速收集目标域名的子域名信息，无需直接与目标交互。
- **主动扫描**：通过直接查询 DNS 记录，获取更全面的子域名信息。
- **字典爆破**：使用内置字典或自定义字典进行子域名爆破，发现隐藏的子域名。

### 使用方式

以下是本插件的基本使用命令：

```bash
# 被动扫描
python3 main.py -passive example.com 

# 主动扫描
python3 main.py -active example.com 

# 使用工具自带字典进行扫描
python3 main.py -dict example.com 

# 使用个性化字典进行扫描
python3 main.py -dict /path/subdomain.txt example.com 
```

### 注意事项

- 请确保在进行主动扫描和字典爆破时遵循相关法律法规，并获得目标网站的授权。
- 被动扫描通常是最安全的选择，建议优先使用。

## 👍 功能模块

### 强大的被动收集能力

1. **常规检查收集**：支持多种检查方法，包括：
   - 域传送漏洞（`axfr`）
   - 跨域策略文件（`cdx`）
   - HTTPS证书（`cert`）
   - 内容安全策略（`csp`）
   - robots 文件（`robots`）
   - sitemap 文件（`sitemap`）
   - NSEC 记录遍历（`dnssec`）
2. **DNS 查询收集**：通过查询 SRV 记录及其他 DNS 记录（MX, NS, SOA, TXT）收集子域。
3. **证书透明度收集**：支持 `crtsh`、`censys_api`。
4. **DNS 数据集收集**：支持 `bevigil_api`、`chaziyu` 等。
5. **威胁情报平台数据收集**：支持 `threatbook_api`、`quake.360` 模块。
6. **搜索引擎发现子域**：支持 `bing`、`google`、`baidu` 全量搜索。

### 强大的主动收集能力

1. **子域爆破**：字典爆破模块使用 `ksubdomain`，DNS 解析速度极快且更准确(需要root权限启动)。
2. **爬虫收集**：支持`async_link_harvester`，`web_depth_explorer`。
3. **子域爬取**：根据已有子域请求响应体及 JS，从中发现新子域。

### 强大的数据处理功能

- 支持自动去重，筛选有效子域并使用`httpx`扩展更多子域信息，结果导出为 `json` 格式。

如果您有其他优秀的想法，请随时告诉我！😎

## 🙏 贡献

欢迎各位开发者共同完善本项目！

## 📜 免责声明

本工具仅限于在获得合法授权的企业安全建设中使用。使用本工具时，您应确保遵守当地法律法规。如因使用本工具而产生任何非法行为，您将自行承担后果，所有开发者和贡献者不承担任何法律责任。请在充分阅读、理解并接受本协议条款后再进行安装和使用。您的使用行为即视为您已阅读并同意本协议的约束。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=GkaMei/SubDigger&type=Date)](https://star-history.com/#GkaMei/SubDigger&Date)
