# SubDigger

👊 **SubDigger** 是一款强大的子域收集工具

## 🎉 项目简介

在渗透测试中，信息收集至关重要，而子域收集是其中不可或缺的一部分。尽管市面上有许多开源的子域收集工具，但它们普遍存在以下问题：

- **功能不足**：许多工具的接口有限，无法实现批量子域的自动收集，缺乏自动解析、验证、模糊查询及信息扩展等功能。
- **用户体验差**：虽然命令行工具方便，但在参数众多、操作复杂时，使用体验不佳。一个友好的前端界面将大大提升用户体验。
- **缺乏维护**：许多工具长时间未更新，缺乏对问题的响应和修复。
- **效率低下**：未充分利用多进程、多线程和异步协程技术，导致速度较慢。

## 👍 功能特性

### 强大的被动收集能力

1. **证书透明度收集**：支持 `crtsh`、`spyse_api`。
2. **常规检查收集**：支持多种检查方法，包括：
   - 域传送漏洞（`axfr`）
   - 跨域策略文件（`cdx`）
   - HTTPS证书（`cert`）
   - 内容安全策略（`csp`）
   - robots 文件（`robots`）
   - sitemap 文件（`sitemap`）
   - NSEC 记录遍历（`dnssec`）
3. **爬虫收集**：支持`archivecrawl`，`commoncrawl`。
4. **DNS 数据集收集**：支持 `bevigil_api`、`chaziyu` 等。
5. **DNS 查询收集**：通过查询 SRV 记录及其他 DNS 记录（MX, NS, SOA, TXT）收集子域。
6. **威胁情报平台数据收集**：支持 `threatbook_api`、`quake.360` 模块。
7. **搜索引擎发现子域**：支持 `bing`、`google` 全量搜索。

### 强大的主动收集能力

1. **子域爬取**：根据已有子域请求响应体及 JS，从中发现新子域。
2. **子域爆破**：字典爆破模块使用 `ksubdomain`，DNS 解析速度极快且更准确。

### 强大的数据处理功能

- 支持自动去重，筛选有效子域并使用`httpx`扩展域名、ip信息，结果导出为 `json` 格式。

如果您有其他优秀的想法，请随时告诉我！😎

## 🙏 贡献

欢迎各位开发者共同完善本项目！

## 📜 免责声明

本工具仅限于在获得合法授权的企业安全建设中使用。使用本工具时，您应确保遵守当地法律法规。如因使用本工具而产生任何非法行为，您将自行承担后果，所有开发者和贡献者不承担任何法律责任。请在充分阅读、理解并接受本协议条款后再进行安装和使用。您的使用行为即视为您已阅读并同意本协议的约束。
