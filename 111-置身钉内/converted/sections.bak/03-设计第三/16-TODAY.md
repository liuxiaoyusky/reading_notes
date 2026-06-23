---
chapter: 设计第三
section: TODAY
line_start: 950
---

## TODAY

Hello！以下是你今日需要关注的所有事项，请查收～

日程4

![image](../../images/971726f441cb3a9dcf22657e724c5e6916473023f0777f19be4bcd36215021a2.jpg)

59秒后开始

智能化产品联合验收

$$
0 9: 0 0 - 1 0: 0 0
$$

$$
\mathrm{C6-4-04N}
$$

![image](../../images/ed8968b948575892e4c13531cbedd0f2459e07fac8fe963ed6104ccbf48b64f0.jpg)

③ 未响应，1个日程冲突

智能化产品运营方案

![image](../../images/fac4e20e93c17682a29a9e943a09048690ecb1d20739bef4bae50b26511dd605.jpg)

![image](../../images/24083e490bcd81ef711f03100ed61e7afce58cd683b93643be163e01279f6af8.jpg)

#

它本质上还是卡⽚，只是在⻚眉加了⼀排头像。这样⽤户能提前知道后⾯⼤概是谁的消息，也可以点击跳过某些卡⽚。

横滑结构设计还是想解决两个问题：

1. 给⽤户预告感，缓解「不知道下⼀张是谁、但看⻅就已读」的压⼒；

2. 允许点击头像，主动跳过⼀些卡⽚。

然⽽，交互的底层规则没变，另外还增加了两重隐形⽽严重的麻烦：

1. 相⽐原场域有 last message、有消息发出时间等，⽤户在 ONE 需要依靠更少的信息⸺仅通过头像判断可能需要跳过谁的信息；

2. ⻚眉加了横滑头像之后，压缩了可读空间。在⼀些⼩屏幕机型上，键盘⼀拉起来，甚⾄看不到 IM 消息本身，反⽽更加损失了信息效率，加重了⽤户的阅读负担。

横滑相⽐原场域的好处，仅仅是减少了⽤户⼀进⼀出、点进⼀条消息查看的成本，但这对⽤户来说真的重要吗？假设点进点出需要耗费⽤户 1 秒，⽽判断⼀条消息需不需要跳过需要 10 秒。为了节省 1 秒⽽增加 10 秒的负担，这真的划算吗？

⽆望的补丁2：Peekaboo

Peekaboo 是我提出的。它的原理是，既然必须要标记⽤户已读，那么我们可以在明确标记已读的节点上略施花活。

⽤户在横滑到下⼀张卡⽚时，只要没有完全划到下⼀张、没有松⼿，就还不算正式读到，可以理解为「预读」。这样⽤户可以⽐普通 IM 列表⾥的 last message 看到更多消息内容，⼜暂时不触发已读。

12:29

![image](../../images/d514da5465fa58678c07c7865eb05249a7fa08ac0452a7a7309f2b47d4989a5c.jpg)

![image](../../images/4bcc5b126f892421b393212b3a9469c1ccdb1cab2b5d2064d345040dc4a607d9.jpg)  
幽素

![image](../../images/ddeb9b163cedf990b00525ca95ec1456e9a9ef6a0b16e0350f398b00f5411bdf.jpg)

![image](../../images/ff97d086c92258a1bb664b5e06432ef823dff12bacdde448f58c08b37caa4c37.jpg)

![image](../../images/14d022e8fd987ca4edb040fbc712c33824f51e185101ec519fedbd8fed70b91e.jpg)

![image](../../images/3cad12e640f465114bc1454b0ca2a82036a0dc765f3adb61488eeec7cccd5b8a.jpg)  
Más Ch...

![image](../../images/770cbde3fe139c2cec5bae38c2d28412e3781660fdf729f4599bcff86a43a3de.jpg)

![image](../../images/988ac60f9d19a3be7fbd5d565c341bd38c2ff612aef2503f399bcd74172e7d52.jpg)

![image](../../images/2443bf849c0f49bcd914c418c47bca3bc629804c3a9f43439ac0a005bbf5dc3c.jpg)

![image](../../images/68a45dc517cd50a3c9a663b2b08455ad79b93d74c919949a0ba145f3b046dd14.jpg)
