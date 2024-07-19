﻿# Bilibili_scraper
## 简介：

## 试验记录：

### 流程记录
![图1 七月四日之前的工作](https://github.com/kem190/Bilibili_scraper/blob/main/mindmap.png)
### **20240626**
关键字相关视频信息抓取，998条。存于jiangping_metadata2024_06_26.csv。以它们为seed，抓取了供4107条推荐视频，有19606条seed-related的相关关系。
### **20240628**
重写了相关视频抓取逻辑，用26号查询的关键视频重新抓取了相关视频。存于related_video_data_2.csv，这是后几日社会网络分析（SNA）和文本分析（CTA）的基础。
### **20240702**
终于靠b站教程完成了评论区翻页的抓取代码，抓取了seed视频的评论。这里犯的错误是限制了评论最大抓取数量到200条左右，导致相当数量的视频评论只有200条，而看不出评论变化的趋势。目前看来，在抓到评论的x条视频中，大部分只有少于十条评论，尔后评论数量开始均匀分布，直到200附近出现一个峰值。有理由怀疑后续也会均匀分布？或者评论数量干脆就是双峰分布的。
### **20240702**
痛定思痛，开始抓取全部4107条视频的评论（因为998条“似乎”只有标题包含姜萍这个关键字的），并且不设抓取上限。截至目前，程序已经跑了134593秒，仍然不知道它抓到了多少以及什么时候会停下。————我在写这个文档的时候突然发现了问题所在，这程序跑下来会比我想得长上百倍，故放弃。
### **20240703**
1. 对998-8031（6月26日的种子，7月2日的相关视频）的第一次相关视频数据，和4107-yy的第二次相关视频数据分别做了SNA，第一组数据分成明显的四个社区（见图2），第二组数据则非常散乱。
![图2 4107个视频的SNA分析](/jiangping_2_SNA.png)
1.1. 首先有趣的是时隔几天得到的related_vids 有巨大区别。这几个rel_vids 都标注了date of excecution，值得玩味一下。 （补充，这个不存在，看错了）<br />
1.2. 关于第一组数据分成的社区，还有待进一步探索，但在分析数据的过程中我发现我自己的bias，我还是太想看到“挺姜”和“反姜”了，这纯preconceived idea。当然，我也没找到这个。<br />
1.3. 目前需要的：对方法论内涵和外延的了解，内涵：它基于什么模型？我们做了哪些假设？外延：在什么场景下使用这种方法？能达到什么效果？<br />
   
3. 对998个跟姜萍最高相关度的视频下的评论做了WordFish估计，结果如图3。
![图3 对998个搜索得来的视频评论区的留言的WordFish估计](https://github.com/kem190/Bilibili_scraper/blob/main/jiangping_wordfish_community.jpeg)
2.1. 结果就是并没有得到我认为有意义的数据，还需要进一步的探索。这包含建立意义层面的理解和进一步的整理和把玩数据。比如做关键词清理、对视频的分类和筛选之类的。<br />
2.1.1. 假设要对视频进行筛选，我们可能需要一个明确的pipeline还有主旨。主旨是尽可能全、快，并且在单位时间内完整的收集数据并且完整的分析。在这个主旨下我选择了用“推荐视频”来做迭代的方式。所以说，选这种数据收集方式的原因是突出它的便利性，而不是我想把b站推送算法当作客体来分析。而如何筛选才能最终得到和主题相关的视频，或者说尽量全的得到视频，这我不得而知。<br />
3. 对998个最高相关度视频下的评论做了topic modelling，结果就是没产生有意义的结果（图4）。同时，用CaoJuan2009的方法来估计K值，结论是从5-50随着K增加结果越来越好，这不太真实。我知道不应该只依赖算法，我认为应该人为筛选一下相关数据。<br />
![图4 k=30时首当其冲的998个视频的主题建模结果](https://github.com/kem190/Bilibili_scraper/blob/main/jiangping_LDA_k%3D30.jpeg)
3.1. 主题建模同样没什么收获，并且不知道为什么。again，这需要一些对模型和方法的再认识。<br />


## 其他想法：
如果我把多次相关视频的seed-result联系起来，相当于人为施加权重。感觉不合理。但如果不这么相关，又能意味着什么呢？把程序当主体？<br />
切入的视角：related video只是收集数据的方式，我们用这个方法收集数据只是为了更快地获得更全面的数据，而并非要像很多研究Youtube的文章一样研究b站的推送算法。所以，我们的切入点应该仍然是网络情绪，舆论之类的。现在需要一些关于情绪的理论，比如造神毁神这种假设。<br />

## 注：
改代码确实有趣，但也确实效率低下。我因为脑子没在R和Python间切换过来，导致python中一处把 = 写成了 <- 而得不到正确的结果，这一个问题，我到处追查，花了一个多小时解决。<br />
