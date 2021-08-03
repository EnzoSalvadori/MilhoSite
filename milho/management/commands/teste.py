from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class Command(BaseCommand):
	help = 'Command Customizado Teste'

	def handle(self, *args, **options):
		subject, from_email, to = 'hello', 'from@example.com', 'enzosalvadori17@gmail.com'
		text_content = 'This is an important message.'
		ctx = { 'username': "enzo" }
		html_content = render_to_string('lala.html', ctx)
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()