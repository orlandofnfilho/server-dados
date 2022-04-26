import sys
import cgi
from http.server import HTTPServer, SimpleHTTPRequestHandler
from database.database import create_table, delete_record, insert_record, fetch_records, delete_record, update_record

HOST_NAME = "localhost"
PORT = 8080


def read_html_template(path):
    """funcao para ler arquivo HTML"""
    try:
        with open(path) as f:
            file = f.read()
    except Exception as e:
        file = e
    return file


def show_records(self):
    """funcao para mostrar registros no modelo"""
    file = read_html_template(self.path)

    # buscar registros do banco de dados
    table_data = fetch_records()

    table_row = ""
    for data in table_data:
        table_row += "<tr>"
        for item in data:
            table_row += "<td>"
            table_row += item
            table_row += "</td>"
        table_row += "</tr>"
    # substitua {{user_records}} no modelo por table_row
    file = file.replace("{{user_records}}", table_row)
    self.send_response(200, "OK")
    self.end_headers()
    self.wfile.write(bytes(file, "utf-8"))


class PythonServer(SimpleHTTPRequestHandler):
    """Servidor HTTP Python que lida com solicitacoes GET e POST"""

    def do_GET(self):
        if self.path == '/':
            self.path = './templates/form.html'
            file = read_html_template(self.path)
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(bytes(file, "utf-8"))

        if self.path == '/show_records':
            self.path = './templates/show_records.html'

            # chame a funcao show_records para mostrar os usuarios inseridos
            show_records(self)

    def do_POST(self):
        if self.path == '/success':

            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                full_name = fields.get("full_name")[0]
                country = fields.get("country")[0]

                # crie a tabela Usuario se for executado pela primeira vez, senao nao
                create_table()

                # inserir registro na tabela User
                insert_record(full_name, country)

                # obs tudo em uma unica linha
                html = f"<html><head></head><body><h1>Dados do formulario gravados com sucesso!!!</h1><br><a href='/'>Dados Cadastrados</a></body></html>"

                self.send_response(200, "OK")
                self.end_headers()
                self.wfile.write(bytes(html, "utf-8"))

        if self.path == '/remove':

            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                full_name = fields.get("full_name")[0]

                # deletar registro na tabela User
                delete_record(full_name)
                
                html = f"<html><head></head><body><h1>Dados deletados com sucesso!!!</h1><br><a href='/'>Dados Cadastrados</a></body></html>"

                self.send_response(200, "OK")
                self.end_headers()
                self.wfile.write(bytes(html, "utf-8"))
       
        if self.path == '/update':

            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                full_name = fields.get("full_name")[0]
                country = fields.get("country")[0]

                 # atualiza registro na tabela User
                update_record(full_name, country)

                
                html = f"<html><head></head><body><h1>Dados do formulario atualizados!!!</h1><br><a href='/'>Dados Cadastrados</a></body></html>"

                self.send_response(200, "OK")
                self.end_headers()
                self.wfile.write(bytes(html, "utf-8"))


if __name__ == "__main__":
    server = HTTPServer((HOST_NAME, PORT), PythonServer)
    print(f"Servidor iniciado http://{HOST_NAME}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Servidor parado com sucesso")
        sys.exit(0)