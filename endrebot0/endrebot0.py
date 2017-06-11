import discord
from . import log

class EndreBot(discord.Client):
	modules = {}
	commands = {}
	
	def __init__(self):
		super().__init__()
		log.info('endrebot0 v0.4.0')
	
	def add_module(self, module):
		self.modules[module.__name__] = module
		self.commands.update(module.commands)
	
	async def on_ready(self):
		log.info('Logged in as %s (%s)' % (self.user, self.user.id))
	
	async def on_message(self, message):
		if message.author != self.user: return
		if message.content.startswith('{{') and message.content.endswith('}}'):
			cmd, *args = message.content[2:-2].strip().split()
			command = self.commands.get(cmd)
			if command:
				await command.invoke(self, message)
	
	def run(self, token):
		super().run(token, bot=False)
