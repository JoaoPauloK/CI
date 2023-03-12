import datetime
import os
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from reptile.bands import Report


class TestReport:
    content: str = None
    has_errors: bool = False
    html_content: str = None

    def add_report(self, result):
        if not self.content:
            self.content = self._prepare_plain()
        if not self.html_content:
            self.html_content = self._prepare_html()
        self.content += f"Resultado de testes para app {result['appname']}\n"
        self._insert_into_html(f"<h3>Resultado de testes para o app {result['appname']}</h3>\n")
        if result['nerrors'] > 0 or result['nfailures'] > 0:
            self.has_errors = True 

        if result['nerrors'] > 0:
            self._update_content('-- ERROS\n')
        for error in result['errors']:
            for line in error:
                self._update_content(f'{line}\n')

        if result['nfailures'] > 0:
            self._update_content('-- FALHAS\n')
        for failure in result['failures']:
            for line in failure:
                self._update_content(f'{line}\n')

        self._update_content(f"\nTotal Erros: {result['nerrors']} ---- Total Falhas: {result['nfailures']}")

    def _update_content(self, text):
        self.content += text
        self._insert_into_html(text)

    def _insert_into_html(self, text):
        index = self.html_content.find('</div>')
        self.html_content = self.html_content[:index] + f'<p style="margin: 0">{text}</p>' + self.html_content[index:]
    
    def _finalize_html(self):
        html = MIMEMultipart('alternative')
        html['Subject'] = 'Relatório de Testes'
        html.attach(MIMEText(self.html_content, 'html'))
        return html

    def _prepare_html(self):        
        html_text = f'''
        <html>
            <head></head>
            <body>
                <h2>{self.content}</h2>
                <div class="content"></div>
            </body>
        </html>
        '''
        return html_text

    def _prepare_plain(self):
        content = f'''
            RELATÓRIO DE TESTES AUTOMÁTICOS - {datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}\n
        '''
        return content

    def _export(self):
        from reptile.exports.pdf import PDF
        filename = uuid.uuid4().hex + '.pdf'
        rep = Report(self.content)
        doc = rep.prepare()
        PDF(doc).export(filename)
        return os.path.basename(filename)

    def export(self):
        return self._export()

    def send_mail(self):
        import smtplib
        from base.setup import EMAILS, SENDER, SENDER_PASSWORD
        assert self.content, 'Nao ha resultado disponivel.'
        mail_content = self._finalize_html()
        print(self.html_content)
        for email in EMAILS:
            instance = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            instance.login(SENDER, SENDER_PASSWORD)
            for email in EMAILS:
                instance.sendmail(SENDER, email, mail_content.as_string())
                instance.quit()

    def send_result(self, result, appname: str):
        if len(result.errors) == 0 and len(result.failures) == 0:
            return
        errors = [error[1].split('\n') for error in result.errors]
        failures = [failure[1].split('\n') for failure in result.failures]
        self.add_report({
            'appname': appname,
            'errors': errors, 
            'failures': failures, 
            'nerrors': len(result.errors), 
            'nfailures': len(result.failures)
        })