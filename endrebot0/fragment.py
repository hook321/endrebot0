import re

__all__ = ['fragment']

_pattern = re.compile(r'(\{\{[^\}]*\}\})|(\{\[[^\]]*\]\})')

def fragment(content):
	code_fragments = _pattern.findall(content)
	idx = 0
	for frag in code_fragments:
		frag_content = frag[0] or frag[1]
		frag_start = content.find(frag_content, idx)
		if frag_start != idx: yield TextFragment(content[idx:frag_start])
		yield CommandFragment(frag[0]) if frag[0] else FlagFragment(frag[1])
		idx = frag_start + len(frag_content)
	if idx < len(content):
		yield TextFragment(content[idx:]) # This will only be text

class Fragment:
	def __init__(self, content):
		self.content = content
	
	def __str__(self):
		return '%s[%s]' % (self.__class__.__name__, self.content)
	
	def __repr__(self):
		return '%s[%s]' % (self.__class__.__name__, repr(self.content))

class TextFragment(Fragment):
	async def invoke(self, ctx):
		return self.content

class CommandFragment(Fragment):
	async def invoke(self, ctx):
		cmd = self.content[2:-2].strip()
		command = ctx.bot.commands[cmd]
		return await command.invoke(ctx)

class FlagFragment(Fragment):
	async def invoke(self, ctx):
		flags = self.content[2:-2].strip()
		return flags