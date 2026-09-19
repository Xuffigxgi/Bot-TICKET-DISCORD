import discord
from discord.ext import commands
from discord.ui import View, Button
import asyncio

TOKEN = "YOUR_TOKEN_BOT"
GUILD_ID = 1419282589105000541          # Server ID
ADMIN_ROLE_ID = 1421730357991968818     # Admin Role ID (can view tickets)
ADMIN_CHANNEL_ID = 1422224061819256883 # Admin Channel (for alerts/ticket summaries)
CATEGORY_ID = 1421731612881846355       # Category ID (if not set, bot creates channels outside categories)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

TICKET_OPTIONS = {
    "buy1": ("🛒", "Buy Products", "Please specify the product you need."),
    "buy2": ("🛍️", "Buy Products", "Please specify the product you need."),
    "admin": ("🛡️", "Contact Admin", "Please describe the issue you need help with."),
}

# ---------------- Close Ticket ----------------
class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Close", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close(self, interaction: discord.Interaction, button: Button):
        channel = interaction.channel
        if not channel.name.startswith("ticket-"):
            return await interaction.response.send_message("❌ This is not a ticket channel.", ephemeral=True)

        await interaction.response.send_message("🔒 Closing ticket and saving data...", ephemeral=True)
        await asyncio.sleep(2)

        # Send transcript summary to admin channel
        admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
        if admin_channel:
            owner = channel.topic or "Unknown"
            messages = [m async for m in channel.history(limit=500, oldest_first=True)]
            transcript = "\n".join(f"[{m.created_at.strftime('%H:%M')}] {m.author}: {m.content}" for m in messages if m.content)
            if len(transcript) > 3900:
                transcript = transcript[-3900:]

            embed = discord.Embed(title=f"📋 Ticket Closed: {channel.name}", color=discord.Color.red())
            embed.add_field(name="Closed By", value=interaction.user.mention, inline=True)
            embed.add_field(name="Ticket Owner", value=owner, inline=True)
            embed.add_field(name="Transcript", value=f"```{transcript}```", inline=False)
            await admin_channel.send(embed=embed)

        await channel.delete(reason=f"Closed by {interaction.user}")

# ---------------- Ticket Panel 3 Buttons ----------------
class TicketPanelView(View):
    def __init__(self):
        super().__init__(timeout=None)

    async def create_ticket(self, interaction: discord.Interaction, key: str):
        guild = interaction.guild
        user = interaction.user
        emoji, title, hint = TICKET_OPTIONS[key]

        # Check if user already has an open ticket
        existing = discord.utils.get(guild.channels, name=f"ticket-{user.name.lower()}")
        if existing:
            return await interaction.response.send_message(
                f"❌ You already have an open ticket: {existing.mention}", ephemeral=True)

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
            topic=f"Ticket Owner: {user.mention} | Type: {title}"
        )

        await interaction.response.send_message(f"✅ Ticket created: {channel.mention}", ephemeral=True)

        embed = discord.Embed(
            title=f"{emoji} Welcome to Support Ticket ({title})",
            description=f"{user.mention} {hint}\n\nStaff will respond as soon as possible.",
            color=discord.Color.green()
        )
        await channel.send(embed=embed, view=CloseTicketView())

        # Notify admin channel
        admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
        if admin_channel:
            await admin_channel.send(f"🎫 New ticket {channel.mention} created by {user.mention} | Type: **{title}**")

    @discord.ui.button(label="1) Buy Products", style=discord.ButtonStyle.primary, custom_id="ticket_buy1", emoji="🔵")
    async def buy1(self, interaction: discord.Interaction, button: Button):
        await self.create_ticket(interaction, "buy1")

    @discord.ui.button(label="2) Buy Products", style=discord.ButtonStyle.success, custom_id="ticket_buy2", emoji="🟢")
    async def buy2(self, interaction: discord.Interaction, button: Button):
        await self.create_ticket(interaction, "buy2")

    @discord.ui.button(label="3) Contact Admin", style=discord.ButtonStyle.danger, custom_id="ticket_admin", emoji="🔴")
    async def admin(self, interaction: discord.Interaction, button: Button):
        await self.create_ticket(interaction, "admin")

@bot.event
async def on_ready():
    bot.add_view(TicketPanelView())
    bot.add_view(CloseTicketView())
    print(f"✅ Bot is online: {bot.user}")

@bot.command(name="setup")
@commands.has_permissions(administrator=True)
async def setup(ctx):
    embed = discord.Embed(
        title="🎫 Support Ticket",
        description="Select a category below to open a ticket.",
        color=discord.Color.blurple()
    )
    await ctx.send(embed=embed, view=TicketPanelView())

@setup.error
async def setup_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You must be an administrator to use this command.")

bot.run(TOKEN)
