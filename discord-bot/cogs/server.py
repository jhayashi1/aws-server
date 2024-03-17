from discord.ext import commands
import boto3
import os
from enum import Enum

ERROR_MESSAGE = 'Usage: ,server [factorio|minecraft] [start|stop|status]'
APPROVED_USERS = ['__jared__', 'hotwire12', 'pizzacat.rar', 'legionous', 'shnooker94']
SERVER_INSTANCES = {
    'factorio': {
        'instance_id': os.getenv('FACTORIO_INSTANCE'),
        'port': '34197'
    },
    'minecraft': {
        'instance_id': os.getenv('MINECRAFT_INSTANCE'),
        'port': '25565'
    }
}
ACTIONS = Enum('Action', ['START', 'STOP', 'STATUS'])

class ServerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Start, stop, or get server status')
    async def server(self, ctx, *args):
        server_type = args[1]

        if str(ctx.message.author) not in APPROVED_USERS:
            await ctx.send(content='Eat my ass')
            return
        
        if server_type not in SERVER_INSTANCES.keys():
            await ctx.send(content=f'server named "{server_type}" not found')
            return
        
        action = get_action(args)
        server_info = SERVER_INSTANCES[server_type]
        response = ERROR_MESSAGE

        # Start command
        if (action == ACTIONS.START):
            response = start_server(server_info)
            await ctx.send(content=response)
            response = wait_for_server_start(server_info)
        # Stop command
        elif (action == ACTIONS.STOP):
            response = stop_server(server_info['instance_id'])
        # Status command
        elif (action == ACTIONS.STATUS):
            response = get_server_status(server_info)

        await ctx.send(content=response)


def get_action(args):
    if args[0] == 'start': return ACTIONS.START
    if args[0] == 'stop': return ACTIONS.STOP
    if args[0] == 'status': return ACTIONS.STATUS

    return -1


def start_server(server_info):
    ec2 = boto3.client('ec2', 'us-east-1')
    instance_id, port = server_info.values()

    try:
        # Get instance from boto3
        response = ec2.describe_instances(
            InstanceIds=[
                instance_id
            ]
        )

        # Get instance info
        instance = response['Reservations'][0]['Instances'][0]
        instance_state = instance['State']['Name']

        # Check server status
        if instance_state == 'running':
            instance_ip = instance['PublicIpAddress']
            return f'Server is running with ip: {instance_ip}:{port}'
        if instance_state != 'stopped':
            return 'Server is unavailable. Try again later'

        # Start instance
        start_response = ec2.start_instances(
            InstanceIds=[
                instance_id,
            ]
        )
    except Exception as e:
        return e

    return 'Starting server...'

def wait_for_server_start(server_info):
    ec2 = boto3.client('ec2', 'us-east-1')
    instance_id, port = server_info.values()

    try:
        # Wait for instance to start
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])

        # Get instance info again
        response = ec2.describe_instances(
            InstanceIds=[
                instance_id
            ]
        )

        # Get instance ip
        instance = response['Reservations'][0]['Instances'][0]
        instance_ip = instance['PublicIpAddress']
    except Exception as e:
        return e

    return f'Successfully started server with ip: {instance_ip}:{port}'

def stop_server(instance_id):
    ec2 = boto3.client('ec2', 'us-east-1')
    try:
        instance_state = get_instance_status()

        if instance_state != 'running':
            return 'Server is not currently running'

        stop_response = ec2.stop_instances(
            InstanceIds=[
                instance_id
            ]
        )

        return "Stopping server"
    except Exception as e:
        return e


def get_server_status(server_info):
    ec2 = boto3.client('ec2', 'us-east-1')
    instance_id, port = server_info.values()

    try:
        response = ec2.describe_instances(
            InstanceIds=[
                instance_id
            ]
        )

        # Get instance info
        instance = response['Reservations'][0]['Instances'][0]
        instance_state = instance['State']['Name']

        if instance_state != 'running':
            return 'Server is not currently running'

        instance_ip = instance['PublicIpAddress']

        return f'Server with ip {instance_ip}:{port} is online'

    except Exception as e:
        return e

def get_instance_status(instance_id):
    ec2 = boto3.client('ec2', 'us-east-1')
    try:
        response = ec2.describe_instances(
            InstanceIds=[
                instance_id
            ]
        )

        # Get instance info
        instance = response['Reservations'][0]['Instances'][0]
        instance_state = instance['State']['Name']

        return instance_state
    except Exception as e:
        return e

async def setup(bot):
    await bot.add_cog(ServerCog(bot))
