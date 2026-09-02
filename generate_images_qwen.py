#!/usr/bin/env python3
"""
记忆编码配图生成器（Qwen-Image版，低显存优化）
使用disk offload + float8减少显存占用

依赖安装：
pip install diffsynth torch safetensors

使用方式：
python generate_images_qwen.py
"""

import os
import torch
from diffsynth.pipelines.qwen_image import QwenImagePipeline, ModelConfig

# 低显存配置：disk offload + float8
vram_config = {
    "offload_dtype": "disk",
    "offload_device": "disk",
    "onload_dtype": torch.float8_e4m3fn,
    "onload_device": "cpu",
    "preparing_dtype": torch.float8_e4m3fn,
    "preparing_device": "cuda",
    "computation_dtype": torch.bfloat16,
    "computation_device": "cuda",
}

# 图片输出目录
IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(IMG_DIR, exist_ok=True)

# 00-99编码表：(数字, 英文关键词, 中文描述, 画面风格)
ENCODINGS = [
    ("00", "old telephone ringing", "老式电话铃铃铃响", "cute cartoon"),
    ("01", "glowing magic pill elixir", "发光的仙丹灵药", "fantasy illustration"),
    ("02", "wind chime tinkling", "风铃叮当响", "cute cartoon"),
    ("03", "giant Buddha on mountain", "灵山大佛", "Chinese landscape"),
    ("04", "pile of snacks chips", "一堆零食", "colorful illustration"),
    ("05", "magic talisman with symbols", "一道符咒", "Chinese fantasy"),
    ("06", "tourist guide leading way", "导游带路", "cute cartoon"),
    ("07", "general waving command flag", "将军挥令旗发令", "Chinese historical"),
    ("08", "roller skates gliding", "穿溜溜鞋滑行", "cute cartoon"),
    ("09", "water chestnut being peeled", "剥菱角吃", "food illustration"),
    ("10", "shirt collar closeup", "衣服领子特写", "fashion illustration"),
    ("11", "pair of chopsticks", "两根筷子", "minimalist"),
    ("12", "cute baby learning to walk", "婴儿学步", "cute cartoon"),
    ("13", "doctor white coat stethoscope", "白大褂听诊医生", "cute cartoon"),
    ("14", "golden key unlocking door", "金色钥匙开锁", "fantasy illustration"),
    ("15", "colorful parrot talking", "会说话彩色鹦鹉", "cute cartoon"),
    ("16", "pomegranate split red seeds", "石榴掰开红籽", "food illustration"),
    ("17", "test tube with bubbles", "试管冒泡泡", "science illustration"),
    ("18", "waist bag with coins", "腰包装钱", "cute cartoon"),
    ("19", "medicinal wine pouring", "倒药酒喝", "Chinese medicine"),
    ("20", "golden earring sparkling", "金耳环闪闪发光", "jewelry illustration"),
    ("21", "big mouth crocodile", "大嘴鳄鱼张嘴", "cute cartoon"),
    ("22", "cute duck flapping wings", "嘎嘎叫鸭子拍翅膀", "cute cartoon"),
    ("23", "Buddhist monk chanting", "和尚念经打坐", "cute cartoon"),
    ("24", "alarm clock ringing", "闹钟叮铃铃响", "cute cartoon"),
    ("25", "erhu Chinese violin playing", "拉二胡演奏", "Chinese culture"),
    ("26", "flowing river with rocks", "河流流淌", "landscape"),
    ("27", "headphones playing music", "戴耳机听歌", "cute cartoon"),
    ("28", "bully slamming table", "恶霸拍桌子", "cute cartoon"),
    ("29", "donkey hide gelatin simmering", "熬阿胶", "Chinese medicine"),
    ("30", "tricycle loaded goods", "三轮车装满货", "cute cartoon"),
    ("31", "great white shark", "大白鲨", "ocean illustration"),
    ("32", "folding fan opening", "折扇打开", "Chinese culture"),
    ("33", "bright shining star", "一颗亮星星", "cute cartoon"),
    ("34", "ancient temple deep mountain", "深山古寺钟声", "Chinese landscape"),
    ("35", "underwater coral reef", "海底珊瑚", "ocean illustration"),
    ("36", "mountain path with trees", "山路崎岖", "landscape"),
    ("37", "wild pheasant mountain", "山里扑棱野鸡", "cute cartoon"),
    ("38", "woman cooking kitchen", "妇女在做饭", "cute cartoon"),
    ("39", "triangle ruler protractor", "三角尺量角器", "education"),
    ("40", "military commander orders", "司令指挥", "cute cartoon"),
    ("41", "wedding emcee microphone", "婚礼司仪主持", "cute cartoon"),
    ("42", "persimmon split juicy", "掰开红柿子汁水四溅", "food illustration"),
    ("43", "stone mountain with trees", "石头山", "landscape"),
    ("44", "stone lion temple gate", "门口大石狮子", "Chinese culture"),
    ("45", "martial arts master teaching", "师父教导", "Chinese culture"),
    ("46", "animal feed scattered", "撒饲料喂鸡", "cute cartoon"),
    ("47", "taxi driver driving", "开车的司机", "cute cartoon"),
    ("48", "stone slab path", "石板路", "landscape"),
    ("49", "stone mortar pestle grinding", "石臼捣药", "Chinese medicine"),
    ("50", "ancient martial arts book", "泛黄武功秘籍", "Chinese fantasy"),
    ("51", "construction worker helmet", "戴安全帽工人", "cute cartoon"),
    ("52", "drum being beaten", "敲鼓", "cute cartoon"),
    ("53", "lunch meat being sliced", "切午餐肉", "food illustration"),
    ("54", "samurai drawing sword", "武士拔刀", "Japanese style"),
    ("55", "steam train moving", "火车呜呜叫", "cute cartoon"),
    ("56", "Chinese parasol tree shade", "梧桐树下乘凉", "landscape"),
    ("57", "weapons on display rack", "武器展示架", "fantasy illustration"),
    ("58", "fox tail wagging", "狐狸尾巴摇啊摇", "cute cartoon"),
    ("59", "five pointed star shining", "五角星闪闪发光", "cute cartoon"),
    ("60", "durian fruit thorny", "榴莲带刺", "food illustration"),
    ("61", "child backpack jumping", "小朋友背书包蹦跳", "cute cartoon"),
    ("62", "cow eating grass", "牛吃草", "cute cartoon"),
    ("63", "quicksand sinking", "陷入流沙", "adventure"),
    ("64", "screw being tightened", "拧螺丝", "cute cartoon"),
    ("65", "gong drum beaten", "敲锣打鼓", "Chinese culture"),
    ("66", "yo-yo spinning back", "溜溜球甩出去弹回", "cute cartoon"),
    ("67", "green flag waving", "绿色旗帜飘扬", "cute cartoon"),
    ("68", "steak sizzling pan", "煎牛排滋滋响", "food illustration"),
    ("69", "deer antler velvet slices", "鹿茸切片泡酒", "Chinese medicine"),
    ("70", "Chinese qilin mythical", "麒麟奔跑", "Chinese fantasy"),
    ("71", "washing clothes washboard", "搓衣板搓衣服泡沫", "cute cartoon"),
    ("72", "penguin waddling", "企鹅摇摆走", "cute cartoon"),
    ("73", "egg cracked open yolk", "一巴掌拍碎鸡蛋", "food illustration"),
    ("74", "knight horse charging", "骑士冲锋", "fantasy illustration"),
    ("75", "colorful blocks stacked", "堆积木", "cute cartoon"),
    ("76", "rhinoceros charging", "犀牛冲撞", "cute cartoon"),
    ("77", "crickets fighting jar", "斗蛐蛐罐子里打架", "cute cartoon"),
    ("78", "watermelon being sliced", "切西瓜", "food illustration"),
    ("79", "colorful balloon flying", "气球飞上天", "cute cartoon"),
    ("80", "double decker bus", "双层巴士急刹车", "cute cartoon"),
    ("81", "ants carrying food", "蚂蚁搬食物", "cute cartoon"),
    ("82", "archery target arrow", "射箭中靶", "cute cartoon"),
    ("83", "peanuts being shelled", "剥花生", "food illustration"),
    ("84", "pulled candy floss golden", "拔丝地瓜拉金丝", "food illustration"),
    ("85", "white fox fluffy tail", "白狐甩尾巴", "cute cartoon"),
    ("86", "Eighth Route Army marching", "八路军行军", "Chinese historical"),
    ("87", "white chess piece board", "白棋落子", "minimalist"),
    ("88", "father carrying child", "爸爸背孩子", "cute cartoon"),
    ("89", "banana fan waving", "芭蕉扇风", "cute cartoon"),
    ("90", "fairy casting magic", "精灵施魔法", "fantasy illustration"),
    ("91", "sports jersey number", "穿球衣运动", "cute cartoon"),
    ("92", "soccer ball kicked", "踢球", "cute cartoon"),
    ("93", "old umbrella opened", "撑旧伞", "cute cartoon"),
    ("94", "classroom blackboard", "教室上课", "cute cartoon"),
    ("95", "ambulance with sirens", "救护车呼啸", "cute cartoon"),
    ("96", "deer antlers forest", "梅花鹿大角", "cute cartoon"),
    ("97", "old faded flag waving", "褪色旧旗迎风飘", "cute cartoon"),
    ("98", "bar counter cocktails", "酒吧吧台调酒", "cute cartoon"),
    ("99", "uncle holding nephew", "舅舅抱外甥", "cute cartoon"),
]

# 通用画面描述后缀（统一风格）
STYLE_SUFFIX = "simple cute cartoon illustration, white background, clean lines, memorable, educational style, high quality"


def load_pipeline():
    """加载Qwen-Image管道（低显存模式）"""
    print("正在加载Qwen-Image模型（低显存模式）...")
    print("首次运行需要下载模型，请耐心等待...")

    pipe = QwenImagePipeline.from_pretrained(
        torch_dtype=torch.bfloat16,
        device="cuda",
        model_configs=[
            ModelConfig(
                model_id="Qwen/Qwen-Image",
                origin_file_pattern="transformer/diffusion_pytorch_model*.safetensors",
                **vram_config,
            ),
            ModelConfig(
                model_id="Qwen/Qwen-Image",
                origin_file_pattern="text_encoder/model*.safetensors",
                **vram_config,
            ),
            ModelConfig(
                model_id="Qwen/Qwen-Image",
                origin_file_pattern="vae/diffusion_pytorch_model.safetensors",
                **vram_config,
            ),
        ],
        tokenizer_config=ModelConfig(
            model_id="Qwen/Qwen-Image",
            origin_file_pattern="tokenizer/"
        ),
        vram_limit=torch.cuda.mem_get_info("cuda")[1] / (1024 ** 3) - 0.5,
    )

    print("模型加载完成！")
    return pipe


def generate_image(pipe, num, keyword_cn, style, seed):
    """生成单张图片"""
    prompt = f"{keyword_cn}，{style}，{STYLE_SUFFIX}"
    image = pipe(prompt, seed=seed, num_inference_steps=40)
    return image


def main():
    """主函数"""
    print("=" * 60)
    print("记忆编码配图生成器（Qwen-Image版·低显存优化）")
    print("=" * 60)
    print(f"输出目录：{IMG_DIR}")
    print(f"待生成：{len(ENCODINGS)} 张图片")
    print(f"显存优化：disk offload + float8")
    print()

    # 加载模型
    pipe = load_pipeline()
    print()

    # 统计
    success_count = 0
    skip_count = 0
    fail_count = 0

    # 逐个生成
    for i, (num, keyword_en, keyword_cn, style) in enumerate(ENCODINGS, 1):
        outfile = os.path.join(IMG_DIR, f"{num}.jpg")

        # 跳过已存在的文件
        if os.path.exists(outfile) and os.path.getsize(outfile) > 5000:
            print(f"[{i}/{len(ENCODINGS)}] {num} - 已存在，跳过")
            skip_count += 1
            continue

        print(f"[{i}/{len(ENCODINGS)}] {num} - {keyword_cn} ...", end=" ", flush=True)

        try:
            seed = int(num) + 42
            image = generate_image(pipe, num, keyword_cn, style, seed)
            image.save(outfile)

            filesize = os.path.getsize(outfile)
            if filesize < 5000:
                print(f"⚠️ 文件太小({filesize} bytes)，可能生成失败")
                os.remove(outfile)
                fail_count += 1
            else:
                print(f"✅ 成功 ({filesize} bytes)")
                success_count += 1

        except Exception as e:
            print(f"❌ 失败: {e}")
            fail_count += 1

    # 输出统计
    print()
    print("=" * 60)
    print("生成完成！")
    print(f"  成功：{success_count}")
    print(f"  跳过：{skip_count}")
    print(f"  失败：{fail_count}")
    print(f"  总计：{len(ENCODINGS)}")
    print("=" * 60)

    # 列出失败的编码
    if fail_count > 0:
        print()
        print("失败的编码：")
        for num, _, keyword_cn, _ in ENCODINGS:
            outfile = os.path.join(IMG_DIR, f"{num}.jpg")
            if not os.path.exists(outfile) or os.path.getsize(outfile) < 5000:
                print(f"  {num} - {keyword_cn}")


if __name__ == "__main__":
    main()
