# black_house
2017.12.21
之前和群里人跑了一次coc，我当的kp，玩的是《沼泽人》模组，很是欢乐，不过由于第一次做kp还是有点准备不足，有点尬聊团的意味。
用qq跑团，到苹果论坛找了一个骰子娘，在骰子娘罢工的前一天成功结团，可喜可贺。
可能是抛砖引玉，群友表示还想接着跑，于是另一个群友主动来当kp，不过骰子娘已经因为服务器经费问题罢工了。
为此，我找到了一个QQbot的python插件，研究了一下之后自己搭建了一个骰子娘，成功开始了跑团。

2017.12.22
在找到QQbot之前，其实我想的是用Django搭建一个平台来玩coc，不过实在费时费力，自己前端能力又不行，所以应急的用了QQbot。
不过之前的工程还是想开发下去，今天完善了coc6版的人物model，不过职业这块还没想好怎么弄，交互上也似乎有很多问题。

2017.12.24
平安夜开团，唔，怎么说呢，果然还是有些尬，群里有些人并不是跑团老手，时长有些超游，kp也是第一次做，有些细节处理有点不好，不过开心就好了。
平台那边一直没有什么进展，果然coc这种自定义的模组还是有点自由度高的问题，很多突发情况想象不到。
所以今天我准备先把之前买过的《山屋惊魂》这样的有固定规则的游戏试着做出来试试。
其实我买了之后一直也没玩过就是了。。。。

2017.12.25
圣诞节啊，为什么公司楼下的活动是猜字谜。。。。
小黑屋是真的难，本来只是在之前的平台工程里面单独开了个app来编写，结果实际写起来发现问题一堆是一堆的，不得以单独开了一个新的工程给他。
由于自己其实也没实际玩过，所以先从熟悉规则入手，然后就发现里面灵活的东西也是多得一匹，而且很多对人来说很简单的操作要用代码实现也是得绕好大的弯子。
好的，我一度想放弃。不过，最近的确心态比较低落，想做点什么来缓解一下（然后就自己给自己添堵了，难受）
正经的，今天大致做了这么些东西：
·想了想地图版的数据结构实现
·大致设计了一下人物和房间卡的互动
·房间卡44张，今天大约录入了30张，不过房间卡各有各的不同事件，要具体实施起来还是很麻烦的，我本来打算用python的动态绑定方法，然而写起来发现好麻烦！！
我看来得换一个结构了。

2017.12.26
哇，难受，真的想放弃了。
最后还是用写java时面向对象编程，抽取了一个房间卡的超类，然后每一张房间卡写了一个继承类。不过基本属性大致不变昨天录入的数据还是能面前弄一下。
由于每个房间卡一个类了，他们的事件实现起来就相对简单了，不过房间卡涉及到与角色、地图版、事件等的互动，目前还没想到完美的方式，反正之前的互动方式有点问题，某几张卡的事件实现起来有点麻烦。
总而言之，今天把房间卡先勉强实现了，在room_card.py中

2017.12.27
要不要这样啊。。。实在想放弃。
今天开始看物品卡、事件卡、预兆卡，发现里面有太多的改变游戏原本规则的东西存在，哇，这种东西是编程最讨厌的，这意味着之前写好的互动模式应该有所修改了，怎么改。。不知道。
总之今天先把物品卡按着之前房间卡的模式先记录了下来，在item_card.py中，并根据物品卡中的效果，修改了人物对象的方法，虽然如此，物品卡中大多实际效果没有实现。
我觉得，如果就这么一点点的写，不知道哪天我就自动放弃了，所以，我决定把这个放到git上来督促自己，我一定要写出来。
因为，我其实真的就是想和大家一起玩而已。。。。

2017.12.28
先来分析一下，物品卡的类型。
武器类，影响人物的对抗动作时使用的能力值和骰子数目，其中左轮改变了袭击方式。
状态buff类，很简单，持有就加能力，失去就减能力。
特殊能力，这个就很烦了，这个的存在修改了很多游戏规则，比如绳索、钥匙、幸运兔脚、蜡烛。
功能类，一般就是一些回复、攻击，比较容易解决
总之今天就开始从血剑开始实现吧，这个涉及到重新设计人物的袭击动作。

最终还是采用了一个类一个专门的实例来做，这样也方便判断人物是否持有道具或具有buff。
另外，今天看了下FAQ，像塔楼这些地方需要鉴定通过之后才能通过的居然分为了左右两侧，这大大加大了操作难度啊。。。
用户输入也是个问题，总之先定义了一个虚拟类。
大部分物品卡算是做了，接下来就是预兆卡了。
今晚去看《芳华》，恩，又回归一个人看电影的状态。

恩，电影不错。
回家之后，看了下预兆卡，发现基本和物品是一样的存在，所以就依然继承Item类了。明天开始看事件（最麻烦的地方。。。）

2017.12.29
17年最后一个工作日。
看了一遍事件卡，因为事件卡中有太多重复的逻辑调用，所以，觉得重头来理一次游戏中会使用的操作。
移动：
    移动到被门扉相连通的临近房间中；触发房间离开（部分房间的经过事件）；
    每移动一个房间，消耗行动力1；
    同房间敌对势力会干扰移动，每存在一个，行动力下降1；
    人物至少能移动1个房间。
探险：
    进入未知区域；消耗全部行动力；
    抽取房间卡，设置房间卡，触发房间进入事件。
    房间卡设置要求
停留：
    停留在当前位置；触发房间停留事件。
能力挑战：
    通常有一个结果对应表，不同点数对应不同结果，超过最大按最大算；
    以自身能力决定骰数（最大8，最小1）；
    分为“房间”、“物品”、“预兆”、“事件”等不同形式触发；
    【天使的羽毛】可以直接决定点数；
    【肾上腺素】可以在结果加值4；
    【幸运石】可以重骰任意骰；
    【幸运兔脚】可以重骰任一骰；
    【蜡烛】影响‘事件’类能力鉴定；
    “祝福”、“水滴”等房间状态会影响骰子数目；
袭击：
    对另一玩家或怪兽进行攻击；
    通常是以“力量”对抗，会因为道具来影响对抗方式，针对不同的袭击，需要以对应的属性来对抗；
    若抵抗方没有对应属性，则袭击无效；
    “力量”“速度”的袭击造成“肉体伤害”，“意志”“知识”袭击造成“精神伤害”；
    袭击差值为伤害值，值大于2，且位于同一房间，能进行物品偷窃；
偷窃：
    袭击获胜者对袭击落败者，需要在同一房间；
    落败者需要具有可被偷窃的物品（“物品”、“预兆”）；
    进行偷窃说明放弃了伤害；
受伤：
    肉体伤害=力量减值+速度减值；
    精神伤害=意志减值+速度减值；
    【铠甲】能让肉体伤害-1；
    【颅骨】能让精神伤害转为肉体伤害；
    探索阶段，人物不会因为减值而死亡；
能力上升、下降
    探索阶段，人物不会因为减值而死亡；
    超出部分等级记录，在减值时优先减少超出部分；
使用道具、预兆
    部分道具有使用对象；
    部分预兆会查看卡堆；
    使用部分物品会导致角色移动；
    武器类道具使用需要选择对象进行袭击；
给予、丢弃、拾取道具
    一回合一次、一件
    【脏狗】影响动作范围
受困事件
    部分事件会导致人物受困；
    可以通过人物自身能力挑战解脱
    可以通过其他玩家帮忙挑战解脱
    可以放置3回合解脱
    持续时间内可以每回合尝试一次
玩具猴袭击
    进入新房间时，需要判定房间内是否有其他对象，骰攻击骰。
房屋标记
    旋转门、滑道、楼座等可以进行连接的移动
buff房间
    每个玩家能享受一次的buff房间
断层房屋
    需要经过能力挑战才能通行的房屋
升降梯
    随时移动的房间卡
另外还有就是游戏后半段和前半段的分别。

2017.12.31
    昨天去重庆了一天，导致中断，今天回来继续，已经是17年最后一天了，新的一年要加油啊！
    继续吧，由上文可知，数据对象设计大致如下：
    人物：
    ·姓名、性别、年龄
    ·力量/速度/意志/知识条、初始力量/速度/意志/知识级别、当前力量/速度/意志/知识级别、超出力量/速度/意志/知识级别
    ·所在楼层、房间（坐标x，坐标y）
    ·行动力
    ·物品栏
    ·预兆栏
    ·事件栏
    ·buff栏
    ·标志物
    ·方法：增减能力等级（级别，超出级别）
    ·方法：复原能力（级别、原本级别）
    ·方法：移动（标志物，房间（标记），地图）
    ·方法：探险（标志物，房间（标记），地图，房间卡堆）
    ·方法：能力挑战（能力，加值，buff，目标值）
    ·方法：房间互动（房间(标记)，buff）
    ·方法：抽物品卡（数量）
    ·方法：抽预兆卡（房间，揭示真相）
    ·方法：抽事件卡（buff，房间）
    ·方法：袭击（武器（物品+预兆），对象（对象列表））
    ·方法：反击（能力，对象）
    ·方法：偷窃（对象（物品+预兆可偷窃列表））
    ·方法：受伤（类型，数值，buff）
    ·方法：给予物品（物品栏，对象）
    ·方法：物品互动（物品栏、预兆栏）->调用物品的使用/丢弃方法
    ·方法：死亡（物品栏、预兆栏）
    房间：
    ·名称、楼层、门、窗、抽卡标志
    ·标志物
    ·物品栏、预兆栏
    ·对象列表【断层房间分两列】
    ·方法：进入事件（角色）【断层房间通行事件由进入事件修改“门”数值实现】
    ·方法：离开事件（角色）
    ·方法：停留事件（角色）
    物品、预兆
    ·名称、是否消耗、可否转交、可否偷窃
    ·所有者
    ·方法：获取事件（角色）
    ·方法：互动事件（角色、是否消耗）
    ·方法：失去事件（角色、角色2、可否转交、可否偷窃）

2018.1.2
    昨天忘写日志了，主要是按着之前总结的改了一下人物类和房间类。
    今天准备把之前录的房间卡按着现在的结构修改一下，然后发现隔断的房间的确有点难处理，需要再想想。
    恩，没想出来怎么做。
    决定先做游戏前期流程吧，然后边做边改了。
    整体修改了一下，然后跑了一下，之后边跑边改吧。
    明天开始调试+写事件吧

2018.1.3
    今天开始写事件。
    写到[自由的呼唤]时，玩家可能会跃至[天井]，虽然之前也有优点类似的[崩塌的房间]，但是这个事件要求目的地必须为天井，天井不存在时，可以按照之前的随机选取处理，但天井若存在，则需要移动至天井，那么就需要获取天井所在的地图坐标。
    由此，有两个预想的方法，一个是保留现在的状态，通过查地图版来找到坐标；另一个是给房间卡添加xy属性记录坐标。
    思考一下怎么做。
    另外，这种事件移动，我认为不应该触发房间特效。

2018.1.8
    工作一忙起来居然就鸽了这么久。。。
    从明天开始继续开始写吧，今天先回忆一下之前写到哪了。。。

    恩，结果又去忙其他事了。。。。好吧。。。

2018.1.9
    异常记录：
    ·进入、离开、停留、跨越房间事件没有触发
    ·抽卡没有触发
    ·房间挑战骰子结果没有输出
    ·地图边界判断
    ·隔断地图处理
    ·升降梯移动处理
    ·探险导致地图封闭问题
    ·莫名其妙的卡死
    ·“迷失神志”事件处理
    ·受困buff处理

    恩，今天略有进展。
    白天以前大学同学邀我继续考高级，想想也的确该捡起来了，本来去年下半年就打算考一次试试的，结果人事考试网上一直异常，甚至一度认为要取消考试了。
    总之，的确需要让自己忙起来了。
    下班时发现同事报了个阿里云的机器学习挑战项目，我也想去试试。
    18年了，加油，奋斗！

2018.1.11
    昨天看了一天的阿里云项目。
    基本是从头开始看，才发现是真的不懂，照着baseline逐行debug了一下，大致弄清了前后顺序，找到了核心训练方法，今天准备继续debug。

    核心算法果然还是c啊，不过本来也是windows弄的东西，不用c才奇怪。算是理清了运作流程，然后发现流程上能改动的地方似乎不多。
    而对于训练参数上面，也不太明白各个参数对模型训练的影响。现在的想法是还是按着baseline来，不过对数据进行一个删选和预处理，提交一次看看结果。

    处理数据的事先放一遍慢慢来，今天解决一下隔断房间的问题吧
    ·由于需求是隔断房间左右分割，对于不同方向进入的角色，其实是相当于进入了两个房间中，只有挑战通过才能到对面房间。

    大致实现。。测试了一下似乎没什么问题，今天先这样了~

2018.1.12
    居然都周五了。。。过得好快。
    上午看了的DataFrame的api，做了个数据预处理，x.apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=1)，已比值关系来削减部分属性的差异值。
    当然还有很多异常数据，所以还需要做一个数据清洗，目前还没有什么想法，大致是x[x.notna[x[(x<x.mean()*2)&(x>x.mean()*0.5)]].all()]

    小黑屋这边的打算是，处理一下房间标签互动、道具处理部分事务。另外，随着程序的运行（恩，崩掉的时间少了些），又出现了之前设计上忽略的一些问题，果然还是要想办法去解决啊。

2018.1.16
    周末贪玩中。。恩，不是贪玩蓝月。
    昨天处理了一下袭击行动，不过还没考虑特殊的手枪远程袭击情况。
    房间的互动和人物buff处理做了一些。

    尝试了处理手枪的远程攻击对象列表获取，本来想和脏狗判断一起做的，然而。。。。子弹是直线，残念。
    （/扶额）然后晚上又沉迷游戏一晚上。。。。神™，负罪感好强。

2018.1.17
    今天开会+3个新需求，忙了一天。。。。又要鸽了。咕咕咕。
    另外，DataFrame看来在机器学习的数据预处理上面还是弱了些，不如from sklearn import preprocessing那么强，不过在数据筛选清洗筛选上面功能不错。

2018.1.18
    用递归的方法单独写了枪械的远程袭击判断。准备照样吧脏狗的判断写了。
    照例把脏狗的范围房间获取写了。

2018.1.21
    周末回家，听闻高中语文老师早晨因病去世，很是难过。

2018.1.24
    最近繁杂的事情很多，昨天回去参加了老师的告别会，非常难受。。。哎。。

    今天重新开始鸽了很久的工程，游戏第一部分的机制大部分弄好了（其实事件都没写完。。。），开始跳入后半段的大坑——50个剧本的代码化
    因为真相表是一个二维矩阵，所以为了方便查询，使用了pandas的DataFrame（你看，之前偶然间学到的东西就有用了）来生成真相表，然后逐一研究剧本，途中抽时间把奸徒表也写了吧。
    第一剧本：木乃伊归来~

2018.1.25
    修修补补，整整改改。
    今天在弄一些第一个剧本相关的设定，然后在跑程序的过程中对出现的bug进行处理，有些bug先打了断点，还不清楚成因，记录一下：
    ·"究竟怎么回事？"，事件异常
    ·升降梯事件异常
    今天在山屋惊魂吧看到了用unity3d做的pc版和手机版，果然很厉害啊，希望能借鉴一些东西。

2018.1.31
    又鸽了很久，应该说不知道怎么继续做。当然另外的原因就是怪物猎人世界了。。。（捂脸）