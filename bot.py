import discord
from discord.ext import commands
import os
from moviepy.editor import VideoFileClip

TOKEN = "여기에_디스코드_봇_토큰"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -------------------------------
# !사용법 — Sora 안내 메시지
# -------------------------------
@bot.command()
async def 사용법(ctx):
    message = (
        "🎬 **Sora 영상 GIF 변환봇 사용법 안내**\n\n"
        "1️⃣ **Sora 앱을 설치하거나 웹 버전에 접속하세요.**\n"
        "    - *(예: sora.com 또는 OpenAI 앱)*\n\n"
        "2️⃣ 원하는 프롬프트로 **영상을 생성하세요.**\n\n"
        "3️⃣ 생성된 영상을 이 채널에 **그냥 업로드하면**,\n"
        "   제가 자동으로 **GIF로 변환**해드립니다!\n\n"
        "💡 변환 후, 디스코드에서 바로 다운로드 가능합니다."
    )
    await ctx.send(message)

# -------------------------------
# 영상 업로드 → 자동 GIF 변환
# -------------------------------
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # 첨부파일이 있을 때만 처리
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith(".mp4") or attachment.filename.endswith(".mov"):
                
                await message.channel.send("📥 영상 다운로드 중...")

                video_path = f"temp_video_{attachment.filename}"
                gif_path = video_path.replace(".mp4", ".gif").replace(".mov", ".gif")

                # 다운로드
                await attachment.save(video_path)

                await message.channel.send("🎞 변환 중... (조금 걸릴 수 있어요)")

                try:
                    clip = VideoFileClip(video_path)
                    clip.write_gif(gif_path)

                    # GIF 업로드
                    await message.channel.send("✨ 변환 완료! 아래 GIF를 저장하세요:")
                    await message.channel.send(file=discord.File(gif_path))

                except Exception as e:
                    await message.channel.send(f"❌ 변환 실패: {e}")

                # 파일 삭제
                try:
                    os.remove(video_path)
                    os.remove(gif_path)
                except:
                    pass

    # 명령어도 작동하도록 유지
    await bot.process_commands(message)


bot.run(MTQwMzM0NTYzNTEwNDc4ODU3MA.Gqzd0n.vbklmilwXwFGc-iCP4mVZf9fkbMaenZ67j7PIk)
