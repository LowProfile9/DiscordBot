import discord
from discord.ext import commands
import yt_dlp
import asyncio
from collections import deque
import os
from dotenv import load_dotenv


intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True


FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
    'executable': r'C:\Users\Iwill\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe'
}


YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

class MusicBot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = deque()  
        self.current_title = None

    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("No estás conectado a un canal de voz!")
                raise commands.CommandError("El autor no esta conectado a este canal de voz")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
    
    @commands.command()
    async def play(self, ctx, *, search):
        print("Command working?")           # Print para saber si la funcion se ejecuta correctamente
        try:
            await self.ensure_voice(ctx)
        except Exception as e:
            print(e)
            return
        
        async with ctx.typing():
            try:
                with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                    info = await asyncio.to_thread(ydl.extract_info, f"ytsearch:{search}", download=False)
                    if not info:
                        return await ctx.send("No se encontraron resultados.")
                    
                    entries = info.get('entries', [info])
                    if not entries:
                        return await ctx.send("No se encontró el video.")
                    
                    entry = entries[0]
                    self.queue.append((entry['url'], entry['title']))
                    await ctx.send(f'Añadido a la cola: **{entry["title"]}**')
                    
                    if not ctx.voice_client.is_playing():
                        await self.play_next(ctx)
                        
            except Exception as e:
                await ctx.send(f"Error al procesar la solicitud: {e}")

    async def play_next(self, ctx, error=None):
        if error:
            await ctx.send(f"Error en reproducción: {error}")
        
        if self.queue:
            url, title = self.queue.popleft()
            self.current_title = title
            source = discord.FFmpegOpusAudio(url, **FFMPEG_OPTIONS)
            ctx.voice_client.play(
                source, 
                after=lambda e: asyncio.run_coroutine_threadsafe(
                    self.play_next(ctx, e), 
                    self.client.loop
                )
            )
            await ctx.send(f'Reproduciendo ahora: **{title}**')
        else:
            self.current_title = None
            
            await asyncio.sleep(60)
            if not ctx.voice_client.is_playing() and not self.queue:
                await ctx.voice_client.disconnect()

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Canción saltada")

    @commands.command()
    async def stop(self, ctx):
        self.queue.clear()
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Bot detenido")

    @commands.command()
    async def queue_list(self, ctx):
        if not self.queue:
            return await ctx.send("La cola está vacía!")
        
        queue_list = "\n".join([f"{i+1}. {title}" for i, (_, title) in enumerate(self.queue)])
        await ctx.send(f"**Cola de reproducción:**\n{queue_list}")

load_dotenv()
TOKEN = os.getenv('DiscordToken')

client = commands.Bot(command_prefix="!", intents=intents)

async def main():
    await client.add_cog(MusicBot(client))
    await client.start(TOKEN)

asyncio.run(main())