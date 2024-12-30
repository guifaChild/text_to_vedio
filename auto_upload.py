# -*- coding:utf-8 -*-
"""
作者：张贵发
日期：2024年12月16日
描述：
"""
from datetime import datetime
from os.path import exists
from pathlib import Path

from conf import BASE_DIR
from uploader.douyin_uploader.main import douyin_setup, DouYinVideo
from uploader.ks_uploader.main import ks_setup, KSVideo
from uploader.tencent_uploader.main import weixin_setup, TencentVideo
from uploader.tk_uploader.main_chrome import tiktok_setup, TiktokVideo
from utils.base_social_media import get_supported_social_media, get_cli_action, SOCIAL_MEDIA_DOUYIN, \
    SOCIAL_MEDIA_TENCENT, SOCIAL_MEDIA_TIKTOK, SOCIAL_MEDIA_KUAISHOU
from utils.constant import TencentZoneTypes
from utils.files_times import get_title_and_hashtags
import asyncio


class TencentZoneTypes:
    LIFESTYLE = "lifestyle"

def parse_schedule(schedule_raw):
    if schedule_raw:
        schedule = datetime.strptime(schedule_raw, '%Y-%m-%d %H:%M')
    else:
        schedule = None
    return schedule

async def main(platform, account_name, action, video_file=None, publish_type=0, schedule=None):
    """
    主函数，通过函数调用执行操作。

    Args:
        platform (str): 选择的平台 ("douyin", "tiktok", "tencent", "kuaishou")。
        account_name (str): 平台上的账户名。
        action (str): 执行动作 ("login" 或 "upload")。
        video_file (str, optional): 视频文件路径，仅在 "upload" 时需要。
        publish_type (int, optional): 发布类型，0为立即发布，1为定时发布。
        schedule (str, optional): 定时发布时间 ("%Y-%m-%d %H:%M" 格式)。仅在 publish_type 为 1 时需要。
    """
    # 参数校验
    if action not in get_cli_action():
        raise ValueError(f"Invalid action: {action}. Choose from {get_cli_action()}.")

    if action == 'upload':
        if not video_file or not exists(video_file):
            raise FileNotFoundError(f"Could not find the video file at {video_file}")
        if publish_type == 1 and not schedule:
            raise ValueError("The schedule must be specified for scheduled publishing.")

    account_file = Path(BASE_DIR / "cookies" / f"{platform}_{account_name}.json")
    account_file.parent.mkdir(exist_ok=True)

    # 根据 action 执行逻辑
    if action == 'login':
        print(f"Logging in with account {account_name} on platform {platform}")
        if platform == SOCIAL_MEDIA_DOUYIN:
            await douyin_setup(str(account_file), handle=True)
        elif platform == SOCIAL_MEDIA_TIKTOK:
            await tiktok_setup(str(account_file), handle=True)
        elif platform == SOCIAL_MEDIA_TENCENT:
            await weixin_setup(str(account_file), handle=True)
        elif platform == SOCIAL_MEDIA_KUAISHOU:
            await ks_setup(str(account_file), handle=True)
        else:
            raise ValueError("Invalid platform")

    elif action == 'upload':
        title, tags = get_title_and_hashtags(video_file)

        if publish_type == 0:
            print("Uploading immediately...")
            publish_date = 0
        else:
            print("Scheduling video...")
            publish_date = parse_schedule(schedule)

        if platform == SOCIAL_MEDIA_DOUYIN:
            await douyin_setup(account_file, handle=False)
            app = DouYinVideo(title, video_file, tags, publish_date, account_file)
        elif platform == SOCIAL_MEDIA_TIKTOK:
            await tiktok_setup(account_file, handle=True)
            app = TiktokVideo(title, video_file, tags, publish_date, account_file)
        elif platform == SOCIAL_MEDIA_TENCENT:
            await weixin_setup(account_file, handle=True)
            category = TencentZoneTypes.LIFESTYLE  # 标记原创需要否则不需要传
            app = TencentVideo(title, video_file, tags, publish_date, account_file, category)

        else:
            raise ValueError("Invalid platform")

        await app.main()


# 示例调用
if __name__ == "__main__":


    asyncio.run(main(platform="douyin", account_name="woai1234A", action="upload", video_file="C:\\Users\\张贵发\\Desktop\\报销\\新建文件夹\\test.mp4", publish_type=0))
