import discord
from discord.ext import commands
from discord.ui import View, Button
import asyncio

TOKEN = "YOUR_TOKEN_BOT"
GUILD_ID = 1419282589105000541          # ไอดีเซิร์ฟเวอ
ADMIN_ROLE_ID = 1421730357991968818     # ไอดียศแอดมิน (ดูห้องตั๋วได้)
ADMIN_CHANNEL_ID = 1422224061819256883 # ช่องแอดมิน (รับแจ้งเตือน/สรุปตั๋ว)
CATEGORY_ID = 1421731612881846355                     # ไอดีหมวดหมู่ (ถ้าไม่ใส่ บอทสร้างห้องนอกหมวด)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

TICKET_OPTIONS = {
    "buy1": ("🛒", "ซื้อสินค้า", "โปรดระบุสินค้าที่ต้องการ"),
    "buy2": ("🛍️", "ซื้อสินค้า", "โปรดระบุสินค้าที่ต้องการ"),
    "admin": ("🛡️", "ติดต่อแอดมิน", "โปรดแจ้งเรื่องที่ต้องการติดต่อ"),
}

# ---------------- ปิดตั๋ว ----------------
class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)----------------

    @discord.ui.button(label="🔒 Close", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close(self, interaction: discord.Interaction, button: Button):
        channel = interaction.channel
        if not channel.name.startswith("ticket-"):
            return await interaction.response.send_message("❌ นี่ไม่ใช่ห้องตั๋ว", ephemeral=True)

        await interaction.response.send_message("🔒 กำลังปิดตั๋วและบันทึกข้อมูล...", ephemeral=True)
        await asyncio.sleep(2)

        # สรุปข้อความเข้าช่องแอดมิน
        admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
        if admin_channel:
            owner = channel.topic or "ไม่ทราบ"
            async for msg in channel.history(limit=200, oldest_first=True):
                pass  # ต้องการเฉพาะนับจำนวน/เก็บ transcript สั้น ๆ
            messages = [m async for m in channel.history(limit=500, oldest_first=True)]
            transcript = "\n".join(f"[{m.created_at.strftime('%H:%M')}] {m.author}: {m.content}" for m in messages if m.content)
            if len(transcript) > 3900:
                transcript = transcript[-3900:]

            embed = discord.Embed(title=f"📋 ตั๋วถูกปิด: {channel.name}", color=discord.Color.red())
            embed.add_field(name="ปิดโดย", value=interaction.user.mention, inline=True)
            embed.add_field(name="เจ้าของตั๋ว", value=owner, inline=True)
            embed.add_field(name="ข้อความ", value=f"```{transcript}```", inline=False)
            await admin_channel.send(embed=embed)

        await channel.delete(reason=f"Closed by {interaction.user}")

# ---------------- ปุ่มเปิดตั๋ว 3 ปุ่ม ----------------
class TicketPanelView(View):
    def __init__(self):
        super().__init__(timeout=None)

    async def create_ticket(self, interaction: discord.Interaction, key: str):
        guild = interaction.guild
        user = interaction.user
        emoji, title, hint = TICKET_OPTIONS[key]

        # เช็คว่ามีห้องตั๋วอยู่แล้วหรือไม่
        existing = discord.utils.get(guild.channels, name=f"ticket-{user.name.lower()}")
        if existing:
            return await interaction.response.send_message(
                f"❌ คุณมีตั๋วเปิดอยู่แล้ว: {existing.mention}", ephemeral=True)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        }
        admin_role = guild.get_role(ADMIN_ROLE_ID)
        if admin_role:
            overwrites[admin_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)

        category = guild.get_channel(CATEGORY_ID) if CATEGORY_ID else None
        channel = await guild.create_text_channel(
            name=f"ticket-{user.name}",
            category=category if isinstance(category, discord.CategoryChannel) else None,
            overwrites=overwrites,
            topic=f"เจ้าของตั๋ว: {user.mention} | ประเภท: {title}"
        )

        await interaction.response.send_message(f"✅ สร้างตั๋วแล้ว: {channel.mention}", ephemeral=True)

        embed = discord.Embed(
            title=f"{emoji} ยินดีต้อนรับเข้าสู่ตั๋ว ({title})",
            description=f"{user.mention} {hint}\n\nเจ้าหน้าที่จะมาตอบโดยเร็วที่สุด",
            color=discord.Color.green()
        )
        await channel.send(embed=embed, view=CloseTicketView())

        # แจ้งเตือนช่องแอดมิน
        admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
        if admin_channel:
            await admin_channel.send(f"🎫 มีตั๋วใหม่ {channel.mention} โดย {user.mention} ประเภท: **{title}**")

    @discord.ui.button(label="1) ซื้อสินค้า", style=discord.ButtonStyle.primary, custom_id="ticket_buy1", emoji="🔵")
    async def buy1(self, interaction: discord.Interaction, button: Button):
        await self.create_ticket(interaction, "buy1")

    @discord.ui.button(label="2) ซื้อสินค้า", style=discord.ButtonStyle.success, custom_id="ticket_buy2", emoji="🟢")
    async def buy2(self, interaction: discord.Interaction, button: Button):
        await self.create_ticket(interaction, "buy2")

    @discord.ui.button(label="3) ติดต่อแอดมิน", style=discord.ButtonStyle.danger, custom_id="ticket_admin", emoji="🔴")
    async def admin(self, interaction: discord.Interaction, button: Button):
        await self.create_ticket(interaction, "admin")

@bot.event
async def on_ready():
    bot.add_view(TicketPanelView())
    bot.add_view(CloseTicketView())
    print(f"✅ บอทออนไลน์: {bot.user}")

@bot.command(name="setup")
@commands.has_permissions(administrator=True)
async def setup(ctx):
    embed = discord.Embed(
        title="🎫 เปิดตั๋วซัพพอร์ต",
        description="เลือกหัวข้อด้านล่างเพื่อเปิดตั๋ว",
        color=discord.Color.blurple()
    )
    await ctx.send(embed=embed, view=TicketPanelView())

@setup.error
async def setup_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ ต้องเป็นแอดมินเท่านั้น")

bot.run(TOKEN)

