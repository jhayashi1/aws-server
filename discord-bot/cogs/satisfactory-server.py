from discord.ext import commands
import boto3
import os

ERROR_MESSAGE = 'Usage: ,server [start|stop|status]'
INSTANCE_ID = os.getenv('INSTANCE_ID')
APPROVED_USERS = ['__jared__', 'hotwire12', 'pizzacat.rar']


class SatisfactoryServerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Start, stop, or get server status')
    async def server(self, ctx, *args):
        if str(ctx.message.author) not in APPROVED_USERS:
            await ctx.send(content='Eat my ass')
            return
        # Check the args
        check = error_check(args)

        # Initalize response variables
        response = ERROR_MESSAGE

        # Start command
        if (check == 0):
            response = start_server()
            await ctx.send(content=response)
            response = wait_for_server_start()
        # Stop command
        elif (check == 1):
            response = stop_server()
        # Status command
        elif (check == 2):
            response = get_server_status()

        await ctx.send(content=response)


def error_check(args):
    if args[0] == 'start':
            return 0
    elif args[0] == 'stop':
            return 1
    elif args[0] == 'status':
        return 2

    return -1


def start_server():
    ec2 = boto3.client('ec2', 'us-east-1')
    try:
        # Get instance from boto3
        response = ec2.describe_instances(
            InstanceIds=[
                INSTANCE_ID
            ]
        )

        # Get instance info
        instance = response['Reservations'][0]['Instances'][0]
        instance_state = instance['State']['Name']

        # Check server status
        if instance_state == 'running':
            instance_ip = instance['PublicIpAddress']
            return 'Server is running with ip: ' + instance_ip
        if instance_state != 'stopped':
            return 'Server is unavailable. Try again later'

        # Start instance
        start_response = ec2.start_instances(
            InstanceIds=[
                INSTANCE_ID,
            ]
        )
    except Exception as e:
        return e

    return 'Starting server...'

def wait_for_server_start():
    ec2 = boto3.client('ec2', 'us-east-1')
    try:
        # Wait for instance to start
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[INSTANCE_ID])

        # Get instance info again
        response = ec2.describe_instances(
            InstanceIds=[
                INSTANCE_ID
            ]
        )

        # Get instance ip
        instance = response['Reservations'][0]['Instances'][0]
        instance_ip = instance['PublicIpAddress']
    except Exception as e:
        return e

    return 'Successfully started server with ip: ' + instance_ip
def stop_server():
    ec2 = boto3.client('ec2', 'us-east-1')
    try:
        instance_state = get_instance_status()

        if instance_state != 'running':
            return 'Server is not currently running'

        stop_response = ec2.stop_instances(
            InstanceIds=[
                INSTANCE_ID
            ]
        )

        return "Stopping server"
    except Exception as e:
        return e


def get_server_status():
    ec2 = boto3.client('ec2', 'us-east-1')
    try:
        response = ec2.describe_instances(
            InstanceIds=[
                INSTANCE_ID
            ]
        )

        # Get instance info
        instance = response['Reservations'][0]['Instances'][0]
        instance_state = instance['State']['Name']

        if instance_state != 'running':
            return 'Server is not currently running'

        instance_ip = instance['PublicIpAddress']

        return 'Server with ip ' + instance_ip + ' is online'

    except Exception as e:
        return e

def get_instance_status():
    ec2 = boto3.client('ec2', 'us-east-1')
    try:
        response = ec2.describe_instances(
            InstanceIds=[
                INSTANCE_ID
            ]
        )

        # Get instance info
        instance = response['Reservations'][0]['Instances'][0]
        instance_state = instance['State']['Name']

        return instance_state
    except Exception as e:
        return e

async def setup(bot):
    await bot.add_cog(SatisfactoryServerCog(bot))
