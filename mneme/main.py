import discord
import niquests

from mneme.logger import log
from mneme.config import CONFIG

intents = discord.Intents.default()
bot  = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)


@bot.event
async def on_ready():
    try:
        await tree.sync()
    except Exception as e:
        log.error(f"Failed to sync commands", exc_info=e)

    log.info(f'Logged in as {bot.user}')


@tree.command(name="ping", description="Replies with a Pong!")
async def ping_command(ctx: discord.Interaction):
    await ctx.response.send_message(f"Pong! ({round(bot.latency * 1000)}ms)")


@tree.command(name="channel_status_history", description="Prints the status history of the current voice channel from the last 100 stauts changes")
async def channel_status_history_command(ctx: discord.Interaction):
    log.debug("Command executed")

    if not ctx.guild:
        raise ValueError("Command must be run on a Sever")
    if not ctx.channel:
        raise ValueError("Command must be run on a Channel")

    url = f"https://discord.com/api/v10/guilds/{ctx.guild.id}/audit-logs?action_type=192&limit=100"
    async with niquests.AsyncSession() as session:
        request = await session.get(url, headers={"Authorization": f"Bot {CONFIG.DISCORD_BOT_TOKEN}"})
        response = request.json()

    raw_audit_logs: list[dict] = response["audit_log_entries"]
    status_change_logs = [map_audit_log_to_status_change_log(raw_audit_log) for raw_audit_log in raw_audit_logs]

    channel_id = ctx.channel.id
    channel_status_changes = [change_log for change_log in status_change_logs if change_log["channel_id"] == channel_id]

    message = generate_message_from_channel_status_changes(channel_status_changes)
    await ctx.response.send_message(message)


def generate_message_from_channel_status_changes(channel_status_changes: list[dict]) -> str:
    message = ""
    for change_log in channel_status_changes:
        message += f"- <t:{change_log['time']}:d>: {change_log['status']}\n"
    return message


def map_audit_log_to_status_change_log(audit_log: dict) -> dict:
    channel_id = int(audit_log["options"]["channel_id"])
    status = audit_log["options"]["status"]
    timestamp = int(get_timestamp_from_snowflake(audit_log["id"]))

    return {"channel_id": channel_id, "status": status, "time": timestamp,}


def get_timestamp_from_snowflake(snowflake: int):
    return ((int(snowflake) >> 22) + 1420070400000) / 1000


def main():
    log.info("Starting Mneme")
    bot.run(CONFIG.DISCORD_BOT_TOKEN, log_handler=None)


if __name__ == "__main__":
    main()