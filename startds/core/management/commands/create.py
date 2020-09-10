from startds.core.management.template import TemplateCommand


class Command(TemplateCommand):
	help = (
		'Creates a Dolphyn experiment directory structure for the '
		'given experiment name in the current directory.'
	)

	missing_args_message = 'You must provide an experiment name.'

	def handle(self, *args, **options):
		exp_name = args[0]
		super().handle(exp_name, options)