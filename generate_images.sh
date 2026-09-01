#!/bin/bash
# 批量生成记忆编码配图
# 使用Pollinations AI免费API

IMG_DIR="/home/work/.openclaw/workspace/memory-guide/images"
mkdir -p "$IMG_DIR"

# 编码列表：数字|英文关键词|中文描述
declare -a ENCODINGS=(
  "00|golden bell ringing|金色铃铛叮当响"
  "01|magic pill glowing|一颗发光的仙丹灵药"
  "02|small bell tinkling|小铃铛叮当响"
  "03|mountain with giant Buddha|灵山大佛"
  "04|pile of snacks and chips|一堆零食"
  "05|magic talisman with symbols|一道符咒"
  "06|guide leading the way|导游带路"
  "07|general waving command flag|将军挥令旗"
  "08|roller skates gliding|穿溜溜鞋滑行"
  "09|water chestnut being peeled|剥菱角"
  "10|shirt collar closeup|衣服领子特写"
  "11|pair of chopsticks|两根筷子"
  "12|cute baby learning to walk|婴儿学步"
  "13|doctor in white coat with stethoscope|白大褂听诊的医生"
  "14|golden key unlocking|金色钥匙开锁"
  "15|colorful parrot talking|会说话的彩色鹦鹉"
  "16|pomegranate split open red seeds|石榴掰开红籽"
  "17|test tube with bubbles|试管冒泡泡"
  "18|waist bag with money|腰包装钱"
  "19|medicinal wine being poured|倒药酒"
  "20|golden earring sparkling|金耳环闪闪发光"
  "21|big mouth crocodile|大嘴鳄鱼"
  "22|cute duck flapping wings|鸭子拍翅膀"
  "23|Buddhist monk chanting|和尚念经"
  "24|alarm clock ringing|闹钟叮铃铃响"
  "25|erhu Chinese violin being played|拉二胡"
  "26|flowing river with rocks|河流流淌"
  "27|headphones playing music|戴耳机听歌"
  "28|bully slamming table|恶霸拍桌子"
  "29|donkey hide gelatin simmering|熬阿胶"
  "30|tricycle loaded with goods|三轮车装满货"
  "31|great white shark|大白鲨"
  "32|folding fan opening|折扇打开"
  "33|bright shining star|一颗亮星星"
  "34|ancient temple in deep mountain|深山古寺钟声"
  "35|underwater coral reef|海底珊瑚"
  "36|mountain path with trees|山路"
  "37|wild pheasant in mountain|山里扑棱的野鸡"
  "38|woman cooking in kitchen|妇女做饭"
  "39|triangle ruler and protractor|三角尺"
  "40|military commander giving orders|司令指挥"
  "41|wedding emcee with microphone|婚礼司仪"
  "42|persimmon split open juicy|掰开红柿子汁水"
  "43|stone mountain with trees|石头山"
  "44|stone lion at temple gate|门口大石狮子"
  "45|martial arts master teaching|师父教导"
  "46|animal feed being scattered|撒饲料"
  "47|taxi driver driving|开车的司机"
  "48|stone slab path|石板路"
  "49|stone mortar and pestle|石臼捣药"
  "50|ancient martial arts book|泛黄武功秘籍"
  "51|construction worker with helmet|戴安全帽工人"
  "52|drum being beaten|敲鼓"
  "53|lunch meat being sliced|切午餐肉"
  "54|samurai drawing sword|武士拔刀"
  "55|steam train moving|火车呜呜叫"
  "56|Chinese parasol tree shade|梧桐树下乘凉"
  "57|weapons on display|武器展示"
  "58|fox tail wagging|狐狸尾巴摇啊摇"
  "59|five pointed star shining|五角星闪闪"
  "60|durian fruit thorny|榴莲"
  "61|child with backpack jumping|小朋友背书包蹦跳"
  "62|cow eating grass|牛吃草"
  "63|quicksand sinking|陷入流沙"
  "64|screw being tightened|拧螺丝"
  "65|gong and drum being beaten|敲锣打鼓"
  "66|yo-yo spinning|溜溜球甩出去弹回"
  "67|green flag waving|绿色旗帜飘扬"
  "68|steak sizzling on pan|煎牛排滋滋响"
  "69|deer antler velvet slices|鹿茸切片"
  "70|Chinese qilin mythical beast|麒麟奔跑"
  "71|washing clothes on washboard|搓衣板搓衣服"
  "72|penguin waddling|企鹅摇摆走"
  "73|egg being cracked open|一巴掌拍碎鸡蛋"
  "74|knight on horse charging|骑士冲锋"
  "75|colorful building blocks stacked|堆积木"
  "76|rhinoceros charging|犀牛冲撞"
  "77|crickets fighting in jar|斗蛐蛐"
  "78|watermelon being sliced|切西瓜"
  "79|colorful balloon flying up|气球飞上天"
  "80|double decker bus|双层巴士"
  "81|ants carrying food|蚂蚁搬食物"
  "82|archery target with arrow|射箭中靶"
  "83|peanuts being shelled|剥花生"
  "84|pulled candy floss golden|拔丝地瓜拉金丝"
  "85|white fox with fluffy tail|白狐甩尾巴"
  "86|Eighth Route Army marching|八路军行军"
  "87|white chess piece on board|白棋落子"
  "88|father carrying child|爸爸背孩子"
  "89|banana being peeled|芭蕉扇风"
  "90|fairy casting magic spell|精灵施魔法"
  "91|sports jersey number|穿球衣"
  "92|soccer ball being kicked|踢球"
  "93|old umbrella being opened|撑旧伞"
  "94|classroom with blackboard|教室上课"
  "95|ambulance with sirens|救护车呼啸"
  "96|deer antlers in forest|梅花鹿大角"
  "97|old faded flag waving|褪色旧旗迎风飘"
  "98|bar counter with cocktails|酒吧吧台调酒"
  "99|uncle holding nephew|舅舅抱外甥"
)

# 计数器
count=0
total=${#ENCODINGS[@]}

echo "开始生成 $total 张记忆编码配图..."
echo "================================"

for entry in "${ENCODINGS[@]}"; do
  IFS='|' read -r num keyword desc <<< "$entry"
  count=$((count + 1))
  
  outfile="$IMG_DIR/${num}.jpg"
  
  # 跳过已存在的文件
  if [ -f "$outfile" ] && [ -s "$outfile" ]; then
    echo "[$count/$total] $num - 已存在，跳过"
    continue
  fi
  
  # 构建提示词：简单卡通风格，白色背景，记忆编码插画
  prompt="simple cute cartoon illustration, $keyword, white background, clean lines, memorable, educational style"
  
  # URL编码
  encoded_prompt=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$prompt'))")
  
  # 调用Pollinations API
  url="https://image.pollinations.ai/prompt/${encoded_prompt}?width=256&height=256&nologo=true&seed=${num}"
  
  echo "[$count/$total] $num - $desc"
  curl -s -L -o "$outfile" "$url" 2>/dev/null
  
  # 检查文件大小（至少5KB才算成功）
  filesize=$(stat -c%s "$outfile" 2>/dev/null || echo 0)
  if [ "$filesize" -lt 5000 ]; then
    echo "  ⚠️  文件太小($filesize bytes)，可能生成失败"
    rm -f "$outfile"
  else
    echo "  ✅ 生成成功 ($filesize bytes)"
  fi
  
  # 间隔2秒避免频率限制
  sleep 2
done

echo ""
echo "================================"
echo "生成完成！"
ls -la "$IMG_DIR"/*.jpg 2>/dev/null | wc -l
echo "张图片已生成到 $IMG_DIR"
