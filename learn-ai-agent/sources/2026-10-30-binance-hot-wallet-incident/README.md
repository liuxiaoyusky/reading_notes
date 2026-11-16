# 币安热钱包安全事件｜官方原帖与热门帖

收录香港时间 2026 年 10 月 30 日至 11 月 13 日可通过 X 检索核对的 152 条官方及事件相关机构通报，另收录第三方热门帖 5 条，其中 17 篇为 X Articles。官方组按时间排列，热门组按本次检索快照的点赞数排列。

官方组覆盖币安全球及华语账号、币安负责人、执法机构和参与冻结的发行方。按原帖 ID 去重，保留不同语言和不同发布账号的版本。X 搜索的可见范围受索引及结果限制。热门报道的早期金额为当时口径，后续以币安公告及执法机关通报为准。

## 档案内容

- [逐帖原文](posts/)按 X 帖子 ID 保存 Markdown 和采集到的 JSON。
- [图片](media/)可在目录内查看，5 段[原视频](https://github.com/liuxiaoyusky/reading_notes/releases/tag/binance-incident-source-media-2026-11-13)可从同仓库附件下载。[媒体清单](媒体清单.json)记录采集来源、下载地址和 SHA-256。
- [来源清单](来源信息.json)记录发布主体、UTC 发布时间、原帖地址、采集时点赞数及 X Article 标记。采集日期按香港时间记为 2026-11-13。
- [图文阅读版](原文阅读版.md)和 [EPUB 阅读副本](LW-471-reading-copy.epub)由采集材料生成。视频在 EPUB 中用静态预览和原帖链接呈现。
- [视频转写](transcripts/)含 4 段本地自动字幕和转写稿，供检索，尚未逐字校对。另一段视频无音轨。

以下列表的发帖日期按 UTC 显示。官方组收录机构公告和发言，具体主张以发帖主体和时间为准。修订信息见原帖及链接页面。热门帖保留传播时的表述及点赞数。

## 下载原视频

[GitHub 附件](https://github.com/liuxiaoyusky/reading_notes/releases/tag/binance-incident-source-media-2026-11-13)提供两段可直接下载的 MP4。其余三段保留原始字节，下载同名的全部分片后按编号合并。用 GitHub CLI 可一次下载全部分片。

```sh
gh release download binance-incident-source-media-2026-11-13 \
  --repo liuxiaoyusky/reading_notes --pattern '*.part-*' --dir binance-video-parts
cd binance-video-parts
for video in GNuBqRMDboUgby5i.mp4 oYgDWqo7I59XbCoS.mp4 Q1c2gF4eOdduWjjb.mp4; do
  cat "$video".part-* > "$video"
done
shasum -a 256 *.mp4
```

合并后的文件可对照[媒体清单](媒体清单.json)中对应原视频的 SHA-256。

## 优先阅读

[币安初步调查（中文）](https://x.com/binancezh/status/2117632624651125019) · [FBI 归因通报](https://x.com/FBICyberBranch/status/2116660730745299426) · [币安 100% 资产回填](https://x.com/binance/status/2120921979226329504)

## 第三方热门帖

1. [BREAKING: World's largest crypto exchange Binance hacked with over $5.6 billion stolen:](https://x.com/WatcherGuru/status/2115922259739349132) · @WatcherGuru · 2026-10-29 · 43,326 赞
2. [JUST IN: 🇰🇵 North Korea's $6,300,000,000 Binance crypto hack is the largest heist in human history.](https://x.com/WatcherGuru/status/2116175386916897161) · @WatcherGuru · 2026-10-30 · 40,205 赞
3. [JUST IN: 🇰🇵 North Korea responsible for $6 billion Binance hack, CNN reports.](https://x.com/WatcherGuru/status/2116035434681634857) · @WatcherGuru · 2026-10-30 · 37,137 赞
4. [BREAKING: Binance has been hacked with wallets across the Ethereum, Bitcoin, and TRON networks seein](https://x.com/KobeissiLetter/status/2115926246916038921) · @KobeissiLetter · 2026-10-29 · 36,938 赞
5. [BREAKING: 🇺🇸🇰🇵 FBI confirms North Korea is responsible for the $6,300,000,000 Binance crypto hack.](https://x.com/WatcherGuru/status/2116644116872519909) · @WatcherGuru · 2026-10-31 · 24,417 赞

## 官方与机构通报

1. [User funds are safe!](https://x.com/cz_binance/status/2115915423174853077) · @cz_binance · 2026-10-29 · 36,222 赞
2. [Circle is closely tracking reports of a potential exploit involving Binance. In coordination with la](https://x.com/jerallaire/status/2115916207463481846) · @jerallaire · 2026-10-29 · 4,472 赞
3. [Tether froze more than 1.567B USDT related to a potential Binance exchange hack.](https://x.com/paoloardoino/status/2115918000373346709) · @paoloardoino · 2026-10-29 · 13,120 赞
4. [Our teams are aware of reports of a potential security issue and are actively investigating. User fu](https://x.com/binance/status/2115918888429133902) · @binance · 2026-10-29 · 7,135 赞
5. [Our team is conducting security checks. Withdrawals will resume as soon as the security issue is ful](https://x.com/binance/status/2115930656589119995) · @binance · 2026-10-29 · 1,703 赞
6. [Our team is conducting security checks. Withdrawals will resume as soon as the security issue is ful](https://x.com/binance/status/2115935002139742437) · @binance · 2026-10-29 · 4,002 赞
7. [As part of our ongoing security measures, Binance Alpha trading has been temporarily suspended - CEX](https://x.com/binance/status/2115943482204574108) · @binance · 2026-10-29 · 1,683 赞
8. [User funds are safe.](https://x.com/heyibinance/status/2115958049244631357) · @heyibinance · 2026-10-30 · 8,044 赞
9. [币安团队正在持续与执法部门、资产发行方、区块链情报机构及行业合作伙伴密切协作，追踪并冻结更多相关资产，累计冻结金额有望进一步提升。](https://x.com/binancezh/status/2115958108090782075) · @binancezh · 2026-10-30 · 53 赞
10. [We are working non-stop to resolve this issue. Binance will cover all losses.](https://x.com/binance/status/2115960292115124558) · @binance · 2026-10-30 · 6,974 赞
11. [我们正在全力推进问题解决，币安将承担因此产生的全部损失。](https://x.com/binancezh/status/2115962419159986521) · @binancezh · 2026-10-30 · 205 赞
12. [Our teams are aware of reports regarding a potential security issue and are actively investigating.](https://x.com/_RichardTeng/status/2115962445584081395) · @_RichardTeng · 2026-10-30 · 1,072 赞
13. [Arbitrum Security Council has executed a transaction to freeze ~$30.5M from the Binance Exploit.](https://x.com/heyibinance/status/2115962957880602653) · @heyibinance · 2026-10-30 · 1,903 赞
14. [截至目前，相关资金已冻结近 30 亿美元。](https://x.com/binancezh/status/2115971910370746783) · @binancezh · 2026-10-30 · 193 赞
15. [Thank you for the collective support from the community.💛](https://x.com/heyibinance/status/2115977844224565522) · @heyibinance · 2026-10-30 · 2,037 赞
16. [Binance will cover all losses.](https://x.com/binance/status/2115981055043981791) · @binance · 2026-10-30 · 10,870 赞
17. [User funds are SAFU!](https://x.com/cz_binance/status/2115993068507897936) · @cz_binance · 2026-10-30 · 13,743 赞
18. [Binance's initial investigation suggests that the security incident may involve a compromised DevOps](https://x.com/binance/status/2115993361517891592) · @binance · 2026-10-30 · 29,565 赞
19. [Thank you all in the community for your support. We will enable withdrawals as soon as the security](https://x.com/heyibinance/status/2115995324825370777) · @heyibinance · 2026-10-30 · 1,663 赞
20. [安全事件进展通报](https://x.com/binancezh/status/2115999785400598801) · @binancezh · 2026-10-30 · 323 赞
21. [**Service Update**](https://x.com/heyibinance/status/2116021551262740985) · @heyibinance · 2026-10-30 · 3,023 赞
22. [Service Update](https://x.com/binance/status/2116026356740034858) · @binance · 2026-10-30 · 3,996 赞
23. [服务更新](https://x.com/binancezh/status/2116027164139442335) · @binancezh · 2026-10-30 · 148 赞
24. [I want to speak to you directly about what happened.](https://x.com/_RichardTeng/status/2116072080525656150) · @_RichardTeng · 2026-10-30 · 6,152 赞
25. [Investigation update: Our initial investigation suggested that the security incident may have involv](https://x.com/binance/status/2116089661408108712) · @binance · 2026-10-30 · 5,531 赞
26. [调查进展更新：根据此前的初步调查显示，此次安全事件可能涉及一台被入侵的笔记本电脑。但在后续调查中，我们发现了其他可能的入侵点。](https://x.com/binancezh/status/2116093801592959262) · @binancezh · 2026-10-30 · 151 赞
27. [Binance has begun recovering affected assets for users and continues to work with law enforcement, i](https://x.com/binance/status/2116121748555153621) · @binance · 2026-10-30 · 11,390 赞
28. [Binance’s SAFU fund and Binance’s holdings include a large amount of assets such as BTC and ETH. We](https://x.com/heyibinance/status/2116124832584904742) · @heyibinance · 2026-10-30 · 2,045 赞
29. [币安已开始回填此次事件中被盗的资产，并将继续与执法部门、资产发行方、区块链情报机构及行业合作伙伴密切协作，追踪、冻结并追回更多相关资金。](https://x.com/binancezh/status/2116127613009687035) · @binancezh · 2026-10-30 · 339 赞
30. [Seems token recovery already began.](https://x.com/cz_binance/status/2116137390180065546) · @cz_binance · 2026-10-30 · 8,114 赞
31. [An update on the security incident.](https://x.com/_RichardTeng/status/2116176335722913865) · @_RichardTeng · 2026-10-30 · 4,278 赞
32. [User funds are SAFU.](https://x.com/heyibinance/status/2116189354418897261) · @heyibinance · 2026-10-30 · 11,267 赞
33. [Saw a few discussions about size of hack, why impact to bitcoin price is small, etc. 👇](https://x.com/cz_binance/status/2116198836729520420) · @cz_binance · 2026-10-30 · 11,543 赞
34. [Security Incident | Recovery Update #2](https://x.com/binance/status/2116258356109496479) · @binance · 2026-10-30 · 4,929 赞
35. [Over the past 24 hours, our teams have been working around the clock to respond to a serious securit](https://x.com/_RichardTeng/status/2116259036903669855) · @_RichardTeng · 2026-10-30 · 893 赞
36. [安全事件进展公告#2（2026-10-30）](https://x.com/binancezh/status/2116259997449589155) · @binancezh · 2026-10-30 · 452 赞
37. [Security Incident | Update #3: 90% of Stolen Assets Replenished; Proof of Reserves Snapshot Provided](https://x.com/binance/status/2116538196259684457) · @binance · 2026-10-31 · 6,413 赞
38. [We know how important trust is, especially in moments like this.](https://x.com/_RichardTeng/status/2116538946188726474) · @_RichardTeng · 2026-10-31 · 1,764 赞
39. [安全事件资产回填进展：已完成约 90% 受影响资产回填并公布储备金证明快照（2026-10-31）](https://x.com/binancezh/status/2116541711149334707) · @binancezh · 2026-10-31 · 170 赞
40. [Binance has allocated US$6.34 billion of its own corporate funds to the User Fund. In the current Us](https://x.com/heyibinance/status/2116545162818318487) · @heyibinance · 2026-10-31 · 3,856 赞
41. [Update: SAFU fund transfer is complete - this was the large 7,499 $BTC transfer visible here:](https://x.com/binance/status/2116564794094559407) · @binance · 2026-10-31 · 3,156 赞
42. [@whale_alert Update: SAFU fund transfer is complete - this was the large 7,499 $BTC transfer visible](https://x.com/binance/status/2116565273520279817) · @binance · 2026-10-31 · 440 赞
43. [Detailed FAQ 👇](https://x.com/cz_binance/status/2116565758058885138) · @cz_binance · 2026-10-31 · 3,722 赞
44. [The FBI is releasing information advising the Democratic People's Republic of Korea (North Korea) wa](https://x.com/FBICyberBranch/status/2116660730745299426) · @FBICyberBranch · 2026-10-31 · 13,721 赞
45. [Update: We had already covered $6B of the impacted amount of the hacked loss.](https://x.com/binance/status/2116713972779126822) · @binance · 2026-11-01 · 2,546 赞
46. [Update: We have already covered $6B of the impacted amount of the hacked loss.](https://x.com/binance/status/2116728061765034338) · @binance · 2026-11-01 · 3,896 赞
47. [Security Incident | Recovery Update #4: Withdrawals Resume in Phases (2026-11-01)](https://x.com/binance/status/2116744986096292263) · @binance · 2026-11-01 · 1,986 赞
48. [安全事件恢复进展公告#4：分阶段恢复提现服务（2026-11-01）](https://x.com/binancezh/status/2116745976446956000) · @binancezh · 2026-11-01 · 204 赞
49. [@FBICyberBranch We sincerely thank you for your strong support during this challenging time.](https://x.com/binance/status/2116755967417442715) · @binance · 2026-11-01 · 2,762 赞
50. [We sincerely thank @FBICyberBranch for their strong support during this challenging time.](https://x.com/binance/status/2116758629634478111) · @binance · 2026-11-01 · 1,894 赞
51. [Today, we're beginning the phased resumption of withdrawals, taking a careful approach to ensure ser](https://x.com/_RichardTeng/status/2116760027570864240) · @_RichardTeng · 2026-11-01 · 590 赞
52. [US Law Enforcement agencies (FBI, USSS, IRS and more) provided vital help in this incident, includin](https://x.com/cz_binance/status/2116768459451469945) · @cz_binance · 2026-11-01 · 11,600 赞
53. [Update: First batch network now opened in phase one of withdrawals is $BTC bitcoin network](https://x.com/binance/status/2116777408074600621) · @binance · 2026-11-01 · 1,617 赞
54. [BTC withdrawal is live.](https://x.com/cz_binance/status/2116778339918877033) · @cz_binance · 2026-11-01 · 10,230 赞
55. [最新进展：第一阶段提现服务已开始恢复，首批开放的是 BTC 网络提现。](https://x.com/binancezh/status/2116781786533654572) · @binancezh · 2026-11-01 · 58 赞
56. [As part of our ongoing security response, we have updated our list of Proof of Reserves addresses to](https://x.com/binance/status/2116785774540787920) · @binance · 2026-11-01 · 893 赞
57. [New withdraw addresses already added into PoR.](https://x.com/heyibinance/status/2116786769148682276) · @heyibinance · 2026-11-01 · 507 赞
58. [作为持续安全应对措施的一部分，我们已更新储备金证明（PoR）地址列表，新增了一批新生成的钱包地址。](https://x.com/binancezh/status/2116789937626632660) · @binancezh · 2026-11-01 · 44 赞
59. [Things are currently running fairly smoothly. If there are many withdrawal requests, congestion cann](https://x.com/heyibinance/status/2116791881057354102) · @heyibinance · 2026-11-01 · 1,458 赞
60. [Withdrawal Update](https://x.com/binance/status/2116799757507305516) · @binance · 2026-11-01 · 4,734 赞
61. [目前，以下资产及网络的提现服务已恢复：](https://x.com/binancezh/status/2116800772725981513) · @binancezh · 2026-11-01 · 104 赞
62. [Withdrawals restored for:](https://x.com/cz_binance/status/2116801935953285223) · @cz_binance · 2026-11-01 · 7,201 赞
63. [Withdrawals have now been restored for the following assets and networks:](https://x.com/heyibinance/status/2116805144771703169) · @heyibinance · 2026-11-01 · 1,174 赞
64. [Latest Withdrawal Update](https://x.com/binance/status/2116827310229967326) · @binance · 2026-11-01 · 1,647 赞
65. [Withdrawals re-enabled for:](https://x.com/cz_binance/status/2116827778545033429) · @cz_binance · 2026-11-01 · 9,864 赞
66. [提现服务最新进展](https://x.com/binancezh/status/2116828876282466737) · @binancezh · 2026-11-01 · 70 赞
67. [Withdrawals have now been re-enabled for the following networks and assets:](https://x.com/heyibinance/status/2116829548708856199) · @heyibinance · 2026-11-01 · 721 赞
68. [Latest Withdrawal Update](https://x.com/binance/status/2116833451949306221) · @binance · 2026-11-01 · 1,003 赞
69. [Withdrawals have now been re-enabled for the following networks and assets:](https://x.com/heyibinance/status/2116835604046729648) · @heyibinance · 2026-11-01 · 695 赞
70. [Latest Withdrawal Update](https://x.com/binance/status/2116844881448743094) · @binance · 2026-11-01 · 1,075 赞
71. [Withdrawals have now been re-enabled for the following networks and assets:](https://x.com/heyibinance/status/2116846750304731336) · @heyibinance · 2026-11-01 · 676 赞
72. [提现服务最新进展](https://x.com/binancezh/status/2116846782982541318) · @binancezh · 2026-11-01 · 37 赞
73. [Latest Withdrawal Update](https://x.com/binance/status/2116851716448718901) · @binance · 2026-11-01 · 1,123 赞
74. [Withdrawals have now been re-enabled for the following networks and assets:](https://x.com/heyibinance/status/2116852768677978149) · @heyibinance · 2026-11-01 · 541 赞
75. [Latest Withdrawal Update](https://x.com/binance/status/2116855614634852611) · @binance · 2026-11-01 · 931 赞
76. [Withdrawals have now been re-enabled for the following networks and assets:](https://x.com/heyibinance/status/2116856295051386904) · @heyibinance · 2026-11-01 · 682 赞
77. [提现服务最新进展](https://x.com/binancezh/status/2116857687027707929) · @binancezh · 2026-11-01 · 37 赞
78. [Latest Withdrawal Update](https://x.com/binance/status/2116871932075516174) · @binance · 2026-11-01 · 1,709 赞
79. [提现服务最新进展](https://x.com/binancezh/status/2116874155983524286) · @binancezh · 2026-11-01 · 41 赞
80. [Withdrawals have now been re-enabled for the following networks and assets:](https://x.com/heyibinance/status/2116886884043636880) · @heyibinance · 2026-11-01 · 871 赞
81. [Binance began restoring withdrawals in phases at 06:00 UTC on November 1, 2026. By 12:36 UTC, withdr](https://x.com/binance/status/2116926305254133892) · @binance · 2026-11-01 · 2,693 赞
82. [币安已于 2026 年 11 月 1 日 14:00（东八区时间）起分阶段恢复提现服务。截至 20:36（东八区时间），首批涵盖的全部 15 个网络与资产均已恢复提现。提现量在最初短暂激增后已回落，并](https://x.com/binancezh/status/2116929784194400705) · @binancezh · 2026-11-01 · 93 赞
83. [12 hours after withdrawals resumed: 2.1% net outflow, with most occurring in the first couple of hou](https://x.com/cz_binance/status/2116954044988354798) · @cz_binance · 2026-11-01 · 15,268 赞
84. [The U.S. Secret Service continues to investigate the theft of more than $6 billion in cryptocurrency](https://x.com/SecretService/status/2116956218887389218) · @SecretService · 2026-11-01 · 1,850 赞
85. [Thank you, @SecretService, and all the agencies and industry partners involved. You acted within min](https://x.com/cz_binance/status/2116977683393618404) · @cz_binance · 2026-11-01 · 5,726 赞
86. [Our top priority right now is to ensure the environment is secure, after which users can withdraw th](https://x.com/heyibinance/status/2117155170568253732) · @heyibinance · 2026-11-02 · 1,158 赞
87. [Fiat Withdrawal Update](https://x.com/binance/status/2117164969582330063) · @binance · 2026-11-02 · 1,462 赞
88. [💁🏻‍♀️Fiat withdrawals are now available for the following currencies:](https://x.com/heyibinance/status/2117166103369814235) · @heyibinance · 2026-11-02 · 548 赞
89. [法币提现服务最新进展](https://x.com/binancezh/status/2117166231564562475) · @binancezh · 2026-11-02 · 63 赞
90. [Security Incident | Recovery Update #5: October 31st PoR Snapshot Now Fully Verifiable by Users](https://x.com/binance/status/2117237539098521938) · @binance · 2026-11-02 · 969 赞
91. [安全事件恢复进展公告 #5：10月31储备金证明快照的零知识证明已生成，用户现可完成独立验证（2026-11-02）](https://x.com/binancezh/status/2117238337039978847) · @binancezh · 2026-11-02 · 47 赞
92. [New update, seems mostly PoR (proof-of-reserve) related.](https://x.com/cz_binance/status/2117240423576162481) · @cz_binance · 2026-11-02 · 1,981 赞
93. [The full zero-knowledge proof for the proof-of-reserves snapshot completed by Binance at 08:00 on Oc](https://x.com/heyibinance/status/2117246543019528463) · @heyibinance · 2026-11-02 · 576 赞
94. [⚠️安全提醒：提现服务恢复期间，请警惕诈骗](https://x.com/binancezh/status/2117263082762482143) · @binancezh · 2026-11-02 · 31 赞
95. [Security Reminder: Stay Alert to Scams as Withdrawals Resume](https://x.com/binance/status/2117264311953563781) · @binance · 2026-11-02 · 1,009 赞
96. [As withdrawals resume, impersonators are offering "priority processing," "compensation claims," and](https://x.com/_RichardTeng/status/2117271494208225735) · @_RichardTeng · 2026-11-02 · 239 赞
97. [Security Incident | Recovery Update #6: Withdrawals Reopen for More Assets (2026-11-03)](https://x.com/binance/status/2117444179630707088) · @binance · 2026-11-03 · 667 赞
98. [安全事件恢复进展更新 #6：更多资产开放提现 (2026-11-03)](https://x.com/binancezh/status/2117448637127233906) · @binancezh · 2026-11-03 · 62 赞
99. [Withdrawal Update](https://x.com/binance/status/2117468922647818652) · @binance · 2026-11-03 · 1,024 赞
100. [Binance will reopen withdrawals for the assets listed below, beginning at 04:00 (UTC) on 2026-11-03.](https://x.com/heyibinance/status/2117469491156435236) · @heyibinance · 2026-11-03 · 384 赞
101. [提现服务最新进展](https://x.com/binancezh/status/2117469578603507937) · @binancezh · 2026-11-03 · 19 赞
102. [💁🏻‍♀️Withdrawals have now been restored for the following assets and networks:](https://x.com/heyibinance/status/2117469655296266577) · @heyibinance · 2026-11-03 · 498 赞
103. [Withdrawal data update](https://x.com/binance/status/2117494793446298084) · @binance · 2026-11-03 · 1,351 赞
104. [By 03:00 UTC, we are seeing hourly deposits exceed withdrawals, reflecting improving user activity a](https://x.com/heyibinance/status/2117495470310490140) · @heyibinance · 2026-11-03 · 568 赞
105. [提现数据更新](https://x.com/binancezh/status/2117502782781698239) · @binancezh · 2026-11-03 · 61 赞
106. [Latest Withdrawal Update](https://x.com/binance/status/2117514123089231963) · @binance · 2026-11-03 · 1,158 赞
107. [💁🏻‍♀️Withdrawals have now been re-enabled for the following networks and assets:](https://x.com/heyibinance/status/2117515821132218502) · @heyibinance · 2026-11-03 · 722 赞
108. [提现服务最新进展](https://x.com/binancezh/status/2117520084948472170) · @binancezh · 2026-11-03 · 33 赞
109. [The trend is starting to show more positive inflows with hourly deposits exceeding withdrawals.](https://x.com/_RichardTeng/status/2117525035619606718) · @_RichardTeng · 2026-11-03 · 229 赞
110. [Binance hourly deposits EXCEED withdrawals. 👀](https://x.com/cz_binance/status/2117532388641136767) · @cz_binance · 2026-11-03 · 5,534 赞
111. [In 10 minutes I'm live on @SquawkStreet as we publish the full report on the 29 October incident. We](https://x.com/_RichardTeng/status/2117626084636405889) · @_RichardTeng · 2026-11-03 · 152 赞
112. [29 October Binance Security Incident: Initial Findings and Response Update](https://x.com/binance/status/2117626126214504729) · @binance · 2026-11-03 · 9,295 赞
113. [On 29 October, Binance was the target of one of the most sophisticated attacks the digital asset ind](https://x.com/_RichardTeng/status/2117626871445921884) · @_RichardTeng · 2026-11-03 · 344 赞
114. [In a few minutes, I'll be live on @FoxBusiness to discuss our initial findings on the 29 October inc](https://x.com/_RichardTeng/status/2117631277050585186) · @_RichardTeng · 2026-11-03 · 153 赞
115. [2026年10月30日币安安全事件：调查初步发现与应对进展更新](https://x.com/binancezh/status/2117632624651125019) · @binancezh · 2026-11-03 · 807 赞
116. [Binance Co-CEO Richard Teng: “We now are operating, we are protecting every user, and we are extreme](https://x.com/binance/status/2117660904833835490) · @binance · 2026-11-03 · 1,353 赞
117. [“The difference is verification, not just promises.”](https://x.com/_RichardTeng/status/2117674232780070977) · @_RichardTeng · 2026-11-03 · 286 赞
118. [A hack of this scale means serious security failures occurred. No platform is unhackable, but that c](https://x.com/cz_binance/status/2117846768666755491) · @cz_binance · 2026-11-04 · 6,293 赞
119. [Security Incident | Recovery Update #7: 98% of Stolen Assets Covered; New & Expanded PoR Snapshot](https://x.com/binance/status/2118001921252347938) · @binance · 2026-11-04 · 1,050 赞
120. [Our latest Proof of Reserves snapshot now covers 44 tokens, up from 10, expanding the range of asset](https://x.com/_RichardTeng/status/2118002177285530100) · @_RichardTeng · 2026-11-04 · 193 赞
121. [安全事件恢复进展更新 #7：98%的被盗资产已完成回填；新一轮储备金证明快照覆盖范围扩大（2026-11-04）](https://x.com/binancezh/status/2118003199332553156) · @binancezh · 2026-11-04 · 50 赞
122. [We have also taken a new Proof of Reserves (PoR) snapshot at 2026-11-04 00:00 (UTC). It now covers 4](https://x.com/heyibinance/status/2118024848803057670) · @heyibinance · 2026-11-04 · 765 赞
123. [安全事件恢复进展更新 #8：更多资产开放提现（2026-11-05）](https://x.com/binancezh/status/2118183176472514793) · @binancezh · 2026-11-05 · 74 赞
124. [💁🏻‍♀️We continue to make progress restoring the withdrawal services and will reopen withdrawals for](https://x.com/heyibinance/status/2118188155769893035) · @heyibinance · 2026-11-05 · 398 赞
125. [Security Incident | Recovery Update #8: Withdrawals for More Assets to Reopen (2026-11-05)](https://x.com/binance/status/2118189091279995327) · @binance · 2026-11-05 · 563 赞
126. [💁🏻‍♀️We continue to make progress restoring the withdrawal services and will reopen withdrawals for](https://x.com/heyibinance/status/2118193327581639096) · @heyibinance · 2026-11-05 · 427 赞
127. [Collective defense is now an operational requirement. In a new post,](https://x.com/circle/status/2118342575631323323) · @circle · 2026-11-05 · 115 赞
128. [Recovery Update #9: Withdrawals for More Assets to Reopen (2026-11-06)](https://x.com/binance/status/2118541594358104469) · @binance · 2026-11-06 · 498 赞
129. [恢复进展更新 #9：更多资产开放提现（2026-11-06）](https://x.com/binancezh/status/2118544228930469888) · @binancezh · 2026-11-06 · 30 赞
130. [💁🏻‍♀️We continue to make progress restoring the withdrawal services and will reopen withdrawals for](https://x.com/heyibinance/status/2118547409441829016) · @heyibinance · 2026-11-06 · 498 赞
131. [A Special Thank You to Our Binance Alpha Community](https://x.com/BinanceWallet/status/2118607986298167510) · @BinanceWallet · 2026-11-06 · 873 赞
132. [ZKProof for the latest PoR is ready, users can verify their balances on Binance are backed at a mini](https://x.com/binance/status/2118631544038580248) · @binance · 2026-11-06 · 562 赞
133. [最新一期储备金证明（PoR）的零知识证明（ZKProof）现已生成，用户可自行验证其在币安平台上的资产均有至少 1:1 的储备金支持。](https://x.com/binancezh/status/2118633902042706293) · @binancezh · 2026-11-06 · 21 赞
134. [Our latest PoR ZKProof is ready, allowing you to independently verify that your Binance balances are](https://x.com/_RichardTeng/status/2118644319255179727) · @_RichardTeng · 2026-11-06 · 141 赞
135. [Update: We’re working to reopen withdrawals for HYPE, INJ, APT, PLASMA, NEAR, LTC by end of next wee](https://x.com/binance/status/2118657118014496819) · @binance · 2026-11-06 · 1,386 赞
136. [最新进展：](https://x.com/binancezh/status/2118660855609061572) · @binancezh · 2026-11-06 · 72 赞
137. [Our next priority is to reopen withdrawals for HYPE, INJ, APT, PLASMA, NEAR, and LTC by the end of n](https://x.com/_RichardTeng/status/2118667958939693265) · @_RichardTeng · 2026-11-06 · 169 赞
138. [💁🏻‍♀️ZKProof for the latest PoR is ready, users can verify their balances on Binance are backed at a](https://x.com/heyibinance/status/2118698626520346871) · @heyibinance · 2026-11-06 · 509 赞
139. [Latest Withdrawal Update](https://x.com/binance/status/2119352231732580574) · @binance · 2026-11-08 · 1,238 赞
140. [💁🏻‍♀️](https://x.com/heyibinance/status/2119353313145799153) · @heyibinance · 2026-11-08 · 648 赞
141. [提现服务最新进展](https://x.com/binancezh/status/2119356820183486661) · @binancezh · 2026-11-08 · 67 赞
142. [Have questions for them?](https://x.com/binance/status/2119423524834316442) · @binance · 2026-11-08 · 77 赞
143. [Join Binance Co-CEOs @_RichardTeng and @heyibinance, alongside Chief Security Officer Jimmy Su, for](https://x.com/binance/status/2119423521516560738) · @binance · 2026-11-08 · 777 赞
144. [Latest Withdrawal Update](https://x.com/binance/status/2119655363385659500) · @binance · 2026-11-09 · 793 赞
145. [提现服务最新进展](https://x.com/binancezh/status/2119662445446979813) · @binancezh · 2026-11-09 · 68 赞
146. [@bc1qDave 也不一定是你们协会成员。](https://x.com/heyibinance/status/2120797853866234333) · @heyibinance · 2026-11-12 · 120 赞
147. [Binance Alpha Appreciation Airdrop & Service Updates](https://x.com/BinanceWallet/status/2120801480106181050) · @BinanceWallet · 2026-11-12 · 260 赞
148. [Binance has completed coverage of assets impacted in the security incident and we have published a n](https://x.com/binance/status/2120921979226329504) · @binance · 2026-11-12 · 2,664 赞
149. [币安已完成对本次安全事件中受影响资产的资金回填，并发布了新一轮储备金证明快照。](https://x.com/binancezh/status/2120925031790502362) · @binancezh · 2026-11-12 · 49 赞
150. [Transparency should go beyond statements. It should be something users can independently verify.](https://x.com/_RichardTeng/status/2120931658224570652) · @_RichardTeng · 2026-11-12 · 136 赞
151. [💁‍♀️ 100%](https://x.com/heyibinance/status/2120933032265957697) · @heyibinance · 2026-11-12 · 800 赞
152. [100% 1:1 backing. Funds are SAFU!](https://x.com/cz_binance/status/2120944565448548658) · @cz_binance · 2026-11-12 · 7,108 赞
