import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import asyncio

load_dotenv()

# Configuration from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
SECRET_ROLE_NAME = os.getenv('SECRET_ROLE_NAME', 'SecretRole')  # Default fallback
SOCIALS_YT = os.getenv('SOCIALS_YT', 'https://youtube.com')
SOCIALS_SITE = os.getenv('SOCIALS_SITE', 'https://yourwebsite.com')
BAD_WORDS = ["placeholder1", "placeholder2"]  # Customize in .env or here

# Logging setup
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Colors
TERMINAL_GREEN = 0x00FF00 
CYBER_PURPLE = 0xBC13FE 

@bot.event
async def on_ready():
    print(f'🚀 We are go for lift off, {bot.user.name}')

@bot.event
async def on_member_join(member):
    try:
        await member.send(f"Welcome to the server {member.name}")
    except:
        pass  # User has DMs disabled

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content_lower = message.content.lower()
    clean_content = "".join(char for char in content_lower if char.isalnum())
    
    # HACKER-PROOF FILTER
    if any(word in clean_content for word in BAD_WORDS):
        try:
            await message.delete()
            embed = discord.Embed(
                title="⚠️ SYSTEM ALERT: UPLINK BREACH",
                description=(
                    "```ansi\n"
                    "[2;31m[CRITICAL] Profanity Protocol Violated.[0m\n"
                    "[2;34mSOURCE:[0m User Uplink Identified\n"
                    "[2;34mACTION:[0m Packet Intercepted & Scrubbed\n"
                    "```\n"
                    "**OPERATOR:** Your recent transmission violated server encryption standards. "
                    "WHAT WERE YOU THINKING? NO!"
                ),
                color=discord.Color.red()
            )
            embed.set_image(url="https://media.giphy.com/media/DqiMTFxiXx0VaVZQbF/giphy.gif")
            
            try:
                await message.author.send(embed=embed)
            except:
                await message.channel.send(f"[2;31m[SYSTEM][0m {message.author.mention}, watch your language!", delete_after=5)
            return
        except Exception as e:
            print(f"Filter Error: {e}")

    # Socials trigger
    if any(word in content_lower.split() for word in ["socials", "youtube"]):
        try:
            await message.delete()
            embed = discord.Embed(
                title="📡 DECRYPTING SOCIAL UPLINKS...",
                description=(
                    "```ansi\n"
                    "[2;32m> Initializing Handshake...[0m\n"
                    "[2;32m> Connection Established.[0m\n"
                    "[2;32m> Extracting Platform Data...[0m\n"
                    "```"
                ),
                color=TERMINAL_GREEN
            )
            embed.add_field(name="📺 [VIDEO_FEED]", value=f"`STATUS: ONLINE`\n[Click for YouTube]({SOCIALS_YT})", inline=True)
            embed.add_field(name="💻 [WEB_DATABASE]", value=f"`STATUS: SECURE`\n[Visit Site]({SOCIALS_SITE})", inline=True)
            embed.add_field(name="🔑 [ACCESS_KEY]", value="```fix\n0000\n```", inline=False)
            embed.set_footer(text="WR_OS v2.0.4 | SECURE TRANSMISSION")
            await message.channel.send(embed=embed, delete_after=20)
            return
        except Exception as e:
            print(f"Socials error: {e}")

    # Rules trigger
    if any(word in content_lower.split() for word in ["rules", "help"]):
        try:
            await message.delete()
            embed = discord.Embed(
                title="📂 root/rules/engagement_protocols.sh",
                description=(
                    "```ansi\n"
                    "[2;36m[SYSTEM INFO] Reading field_rules.txt...[0m\n"
                    "```"
                ),
                color=CYBER_PURPLE
            )
            embed.add_field(
                name="01 // NO_TOXICITY", 
                value="```diff\n+ Respect all operators.\n- Toxic behavior = Immediate Kick.\n```", 
                inline=False
            )
            embed.add_field(name="🔗 [EXTERNAL_DOCS]", value="[FULL PROTOCOL HERE](https://discord.com/)", inline=False)
            embed.set_footer(text="EXECUTION SUCCESSFUL | SYSTEM_AUTHORITY")
            await message.channel.send(embed=embed, delete_after=20)
            return
        except Exception as e:
            print(f"Rules error: {e}")

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("```ansi\n[2;31m[ERROR] Access Denied. Insufficient Clearance.[0m\n```", delete_after=5)
    else:
        print(f'Command error: {error}')
        await ctx.send("```ansi\n[2;31m[ERROR] Command failed. Check console logs.[0m\n```", delete_after=5)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=SECRET_ROLE_NAME)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} yooo hey I'm {SECRET_ROLE_NAME}")
    else:
        await ctx.send(f"Role '{SECRET_ROLE_NAME}' doesn't exist")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=SECRET_ROLE_NAME)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {SECRET_ROLE_NAME} removed oof")
    else:
        await ctx.send(f"Role '{SECRET_ROLE_NAME}' doesn't exist")

@bot.command(aliases=["clear", "purge"])
@commands.has_permissions(manage_messages=True)
async def wipe(ctx, amount: int = 10):
    await ctx.message.delete()
    status_msg = await ctx.send("```ansi\n[2;31m[!] INITIALIZING SYSTEM WIPE...[0m\n[ ] 0% ░░░░░░░░░░\n```")
    
    await asyncio.sleep(1)
    await status_msg.edit(content="```ansi\n[2;31m[!] PURGING CACHE...[0m\n[■■■] 30% ███░░░░░░░\n```")
    await asyncio.sleep(0.5)
    await status_msg.edit(content="```ansi\n[2;31m[!] SCRUBBING LOGS...[0m\n[■■■■■■■] 70% ███████░░░\n```")
    await asyncio.sleep(0.5)

    deleted = await ctx.channel.purge(limit=amount)
    await status_msg.edit(content=f"```ansi\n[2;32m[SUCCESS] {len(deleted)} logs permanently deleted.[0m\n[■■■■■■■■■■] 100% ██████████\n```")
    
    try:
        dm_embed = discord.Embed(
            title="📂 [WIPE_CONFIRMATION]",
            description=f"```ansi\n[2;32m[REPORT] Data scrub complete.[0m\n[2;34m[TARGET] {ctx.channel.name}[0m\n[2;34m[REMOVED] {len(deleted)} lines.[0m\n```",
            color=TERMINAL_GREEN
        )
        await ctx.author.send(embed=dm_embed)
    except:
        pass

    await asyncio.sleep(3)
    await status_msg.delete()

@bot.command()
async def dm(ctx, *, msg):
    await ctx.message.delete()
    dm_embed = discord.Embed(
        title="🔐 [INCOMING_DATA_BURST]",
        description=f"```ansi\n[2;32m[DECRYPTING]... Source: SERVER_UPLINK[0m\n```\n**DECODED MESSAGE:**\n> {msg}",
        color=CYBER_PURPLE 
    )
    
    try:
        await ctx.author.send(embed=dm_embed)
        confirm = discord.Embed(description="```ansi\n[2;32m[SUCCESS] Private uplink established.[0m\n```", color=TERMINAL_GREEN)
        await ctx.send(embed=confirm, delete_after=5)
    except:
        await ctx.send("```ansi\n[2;31m[ERROR] Uplink Blocked. Check Privacy Settings![0m\n```", delete_after=10)

@bot.command()
@commands.has_permissions(administrator=True)
async def broadcast(ctx, role: discord.Role, *, message_content):
    await ctx.message.delete()
    status_msg = await ctx.send(f"```ansi\n[2;34m[SYSTEM] Initializing broadcast to {role.name}...[0m\n```")
    
    success_count = fail_count = 0
    targets = [m for m in role.members if not m.bot]

    if not targets:
        return await status_msg.edit(content="```ansi\n[2;31m[ERROR] No members found with that role.[0m\n```")

    broadcast_embed = discord.Embed(
        title="🚨 [EMERGENCY_BROADCAST] : LEVEL 5 CLEARANCE",
        description=f"```ansi\n[2;31m[!] PRIORITY MESSAGE FROM COMMAND[0m\n```\n**MESSAGE:**\n> {message_content}",
        color=0xFF0000 
    )
    broadcast_embed.set_footer(text=f"ORIGIN: {ctx.guild.name} | ID: {random.randint(1000, 9999)}")

    for member in targets:
        try:
            await member.send(embed=broadcast_embed)
            success_count += 1
        except:
            fail_count += 1

    report = f"```ansi\n[2;32m[COMPLETE] Broadcast finished.[0m\n[2;34mSUCCESS: {success_count}[0m | [2;31mFAILED: {fail_count}\n```"
    await status_msg.edit(content=report)

bot.remove_command('help')

@bot.command(aliases=["terminal", "help", "h"])
async def commands(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

    embed = discord.Embed(
        title="🖥️ [SYSTEM_DIRECTORY]",
        description="```ansi\n[2;32m> Initializing Handshake...[0m\n[2;34m> Source: /root/bin/commands[0m\n[2;34m> Firewall: ACTIVE[0m\n```",
        color=TERMINAL_GREEN
    )
    embed.add_field(name="📡 [COMMS]", value="`!dm` • Private Echo\n`!broadcast` • Role Broadcast", inline=False)
    embed.add_field(name="📄 [INFO]", value="`rules` • Protocols\n`socials` • External Links", inline=False)
    embed.add_field(name="🧹 [MAINTENANCE]", value="`!wipe` • Clear Logs\n**Filter** • Auto-Moderation", inline=False)
    embed.set_footer(text="WR_OS v2.2 | ALL SYSTEMS NOMINAL")
    await ctx.send(embed=embed, delete_after=60)

@bot.command()
@commands.has_permissions(administrator=True)
async def overdrive(ctx, *, announcement):
    try:
        await ctx.message.delete()
    except:
        pass
    
    warning = await ctx.send("```ansi\n[2;31m[!] CRITICAL: SYSTEM OVERRIDE...[0m\n```")
    await asyncio.sleep(1.5)
    await warning.delete()

    embed = discord.Embed(
        title="⚠️ [GLOBAL_SYSTEM_OVERDRIVE]",
        description=f"```ansi\n[2;31m{'━'*20}\n{announcement.upper()}\n{'━'*20}[0m\n```",
        color=0xFF0000
    )
    embed.set_author(name="SYSTEM AUTHORITY")
    embed.set_footer(text="THREAT_LEVEL: OMEGA")
    
    await ctx.send(content="@everyone", embed=embed)

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("❌ DISCORD_TOKEN not found in .env file!")
        exit(1)
    bot.run(DISCORD_TOKEN, log_handler=handler, log_level=logging.DEBUG)
```](streamdown:incomplete-link)
