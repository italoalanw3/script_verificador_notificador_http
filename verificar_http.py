
import requests, time, subprocess, smtplib

class Verificador(object):
	__caiu = 0
	__QUANTIDADE_QUEDAS_PARA_REINICIAR = 3
	__COMANDO_REINICIAR_SERVICO = "/etc/init.d/tomcat7 restart"

	def __init__(self):
		self.__caiu = 0		

	def __enviar_email(self, mensagem):
		try:
			print('enviando e-mail')

			fromaddr = 'seuemail@gmail.com'
			toaddrs = ['email_a_ser_avisado_01@gmail.com', 'email_a_ser_avisado_02@gmail.com', 'email_a_ser_avisado_03@gmail.com']
			username = 'seuemail'
			password = 'senha_seuemail'
			server = smtplib.SMTP('smtp.gmail.com:587')
			server.starttls()
			server.login(username,password)
			server.sendmail(fromaddr, toaddrs, mensagem)
			server.quit()
			print('e-mail enviado com sucesso')
		except Exception as e:
			print('e-mail nao enviado: {0}'.format(str(e)))

	def __restart_servico(self):
		try:
			print('reiniciando tomcat...')
			subprocess.call(self.__COMANDO_REINICIAR_SERVICO, shell=True)
			print('tomcat reiniciado!')
		except Exception as e:
			print('erro ao reiniciar tomcat: '.format(str(e)))

	def __tratar_queda_servico(self):
		self.__caiu = self.__caiu + 1
		print('servico caiu {0} vezes'.format(self.__caiu))
		if self.__caiu == self.__QUANTIDADE_QUEDAS_PARA_REINICIAR:
			self.__enviar_email('Subject: {0}\n\n{0}'.format('caiu :('))
			self.__restart_servico()			

	def __servico_caiu_e_voltou_ao_normal(self):
		if self.__caiu >= self.__QUANTIDADE_QUEDAS_PARA_REINICIAR:
			self.__enviar_email('Subject: {0}\n\n{0}'.format('voltou \o/!'))
			self.__caiu = 0

	def verificar_servico(self):
		
		try: 
			r = requests.get('http://url/')
			if r.status_code == 200:
				print('no ar')
				self.__servico_caiu_e_voltou_ao_normal()			
			else:
				self.__tratar_queda_servico()				

		except Exception as e:
			self.__tratar_queda_servico()

if __name__ == '__main__':
	
	print('iniciou main')

	INTERVALO_EM_SEGUNDOS_VERIFICAR_SERVICO = 10
	verificador = Verificador()
	while True:
		try:
			verificador.verificar_servico()			
		except Exception as e:
			print('Erro ao verificar api: {0}'.format(str(e)))

		print('aguardando {0} segundos para verificar novamente'.format(INTERVALO_EM_SEGUNDOS_VERIFICAR_SERVICO))			
		time.sleep(INTERVALO_EM_SEGUNDOS_VERIFICAR_SERVICO)
