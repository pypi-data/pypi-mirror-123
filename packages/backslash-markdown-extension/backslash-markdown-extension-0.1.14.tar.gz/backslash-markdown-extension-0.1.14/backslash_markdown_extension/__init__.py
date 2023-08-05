from markdown.extensions import Extension
from backslash_markdown_extension import processors

class BackslashMarkdownExtension(Extension):

	def extendMarkdown(self, md):
		md.preprocessors.register(processors.BackslashPreProcessor(md), 'backslash', 1)
		md.treeprocessors.register(processors.BackslashTreeProcessor(md), 'backslash', 2)
		md.postprocessors.register(processors.BackslashPostProcessor(), 'backslash', 3)
