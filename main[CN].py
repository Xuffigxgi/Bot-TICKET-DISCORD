import discord
from discord.ext import commands
from discord.ui import View, Button
import asyncio

TOKEN = "YOUR_TOKEN_BOT"
GUILD_ID = 1419282589105000541          # 服务器ID
ADMIN_ROLE_ID = 1421730357991968818     # 管理员身份组ID（可查看工单频道）
ADMIN_CHANNEL_ID = 1422224061819256883  # 管理员频道（接收通知/工单摘要）
CATEGORY_ID = 1421731612881846355       # 分类ID（不填则机器人在分类外创建频道）

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

TICKET_OPTIONS = {
    "buy1": ("🛒", "购买商品", "请说明您想购买的商品"),
    "buy2": ("🛍️", "购买商品", "请说明您想购买的商品"),
    "admin": ("🛡️", "联系管理员", "请说明您要联系管理员的事项"),
}

# ---------------- 关闭工单 ----------------
class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 关闭", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close(self, interaction: discord.Interaction, button: Button):
        channel = interaction.channel
        if not channel.name.startswith("ticket-"):
            return await interaction.response.send_message("❌ 这不是工单频道", ephemeral=True)

        await interaction.response.send_message("🔒 正在关闭工单并保存记录...", ephemeral=True)
        await asyncio.sleep(2)

        # 将聊天摘要发送到管理员频道
        admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
        if admin_channel:
            owner = channel.topic or "未知"
            messages = [m async for m in channel.history(limit=500, oldest_first=True)]
            transcript = "\n".join(
                f"[{m.created_at.strftime('%H:%M')}] {m.author}: {m.content}"
                for m in messages if m.content
            )
            if len(transcript) > 900:
                transcript = transcript[-900:]

            embed = discord.Embed(title=f"📋 工单已关闭：{channel.name}", color=discord.Color.red())
            embed.add_field(name="关闭者", value=interaction.user.mention, inline=True)
            embed.add_field(name="工单所有者", value=owner, inline=True)
            embed.add_field(name="聊天记录", value=f"```{transcript or '无'}```", inline=False)
            await admin_channel.send(embed=embed)

        await channel.delete(reason=f"Closed by {interaction.user}")

# ---------------- 三个开单按钮 ----------------
class TicketPanelView(View):
    def __init__(self):
        super().__init__(timeout=None)

    async def create_ticket(self, interaction: discord.Interaction, key: str):
        guild = interaction.guild
        user = interaction.user
        emoji, title, hint = TICKET_OPTIONS[key]

        # 检查是否已有工单
        existing = discord.utils.get(guild.channels, name=f"ticket-{user.name.lower()}")
        if existing:
            return await interaction.response.send_message(
                f"❌ 您已有一个未关闭的工单：{existing.mention}", ephemeral=True)

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
            topic=f"工单所有者：{user.mention} | 类型：{title}"
        )

        await interaction.response.send_message(f"✅ 工单已创建：{channel.mention}", ephemeral=True)

        embed = discord.Embed(
            title=f"{emoji} 欢迎来到工单（{title}）",
            description=f"{user.mention} {hint}\n\n工作人员将尽快回复您",
            color=discord.Color.green()
        )
        await channel.send(embed=embed, view=CloseTicketView())

        # 通知管理员频道
        admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
        if admin_channel:
            await admin_channel.send(f"🎫 新工单 {channel.mention}，创建者 {user.mention}，类型：**{title}**")

    @discord.ui.button(label="1) 购买商品", style=discord.ButtonStyle.primary, custom_id="ticket_buy1", emoji="🔵")
    async def buy1(self, interaction: discord.Interaction, button: Button):
        await self.create_ticket(interaction, "buy1")

    @discord.ui.button(label="2) 购买商品", style=discord.ButtonStyle.success, custom_id="ticket_buy2", emoji="🟢")
    async def buy2(self, interaction: discord.Interaction, button: Button):
        await self.create_ticket(interaction, "buy2")

    @discord.ui.button(label="3) 联系管理员", style=discord.ButtonStyle.danger, custom_id="ticket_admin", emoji="🔴")
    async def admin(self, interaction: discord.Interaction, button: Button):
        await self.create_ticket(interaction, "admin")

@bot.event
async def on_ready():
    bot.add_view(TicketPanelView())
    bot.add_view(CloseTicketView())
    print(f"✅ 机器人已上线：{bot.user}")

@bot.command(name="setup")
@commands.has_permissions(administrator=True)
async def setup(ctx):
    embed = discord.Embed(
        title="🎫 开启客服工单",
        description="请选择下方主题以开启工单",
        color=discord.Color.blurple()
    )
    await ctx.send(embed=embed, view=TicketPanelView())

@setup.error
async def setup_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ 仅限管理员使用")

bot.run(TOKEN)
