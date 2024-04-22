from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename
import os
import zipfile
import subprocess
import couchdb
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'teste'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'zip'}

couch = couchdb.Server('http://admin:teste@127.0.0.1:5984/')

def get_or_create_database(couch_server, db_name):
    try:
        db = couch_server[db_name]
    except couchdb.http.ResourceNotFound:
        db = couch_server.create(db_name)
    return db

def create_vulnerabilities_view(db):
    view = {
        '_id': '_design/vulnerabilities',
        'views': {
            'all_vulnerabilities': {
                'map': 'function(doc) { if (doc.type === "vulnerability") emit(doc._id, doc); }'
            }
        }
    }
    try:
        db.save(view)
    except couchdb.http.ResourceConflict:
        pass

db = get_or_create_database(couch, 'relatorios')
create_vulnerabilities_view(db)

@app.route('/')
def index():
    return render_template('index.html', title='Melina')

@app.route('/upload_relatorio', methods=['GET', 'POST'])
def upload_relatorio():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return redirect(request.url)
        nome = request.form.get('nome', '')
        clean_nome = secure_filename(nome)
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        folder_name = clean_nome or os.path.splitext(filename)[0]
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
        os.makedirs(folder_path, exist_ok=True)
        create_folder_and_unzip(file_path, folder_path)
        new_path = clean_and_rename_file(file_path, folder_name)
        if new_path:
            os.remove(new_path)
            convert_md_to_pdf(folder_path)
            pdf_path = os.path.join(folder_path, 'result.pdf')
            store_report_metadata(folder_name, pdf_path)
        return redirect(url_for('consulta_relatorios'))
    return render_template('upload_relatorio.html', title='Upload de Relatório')

@app.route('/consulta_relatorios')
def consulta_relatorios():
    reports_list = get_reports_list()
    return render_template('consulta_relatorios.html', title='Relatórios', reports_list=reports_list)

@app.route('/download_relatorio/<report_name>')
def download_relatorio(report_name):
    try:
        doc = next((doc.doc for doc in db.view('_all_docs', include_docs=True) if doc.doc.get('report_name') == report_name), None)
        if not doc:
            raise ValueError("Relatório não encontrado")
        pdf_path = doc['pdf_path']
        return send_file(pdf_path, as_attachment=True, download_name=f"{report_name}_result.pdf")
    except Exception as e:
        print(f"Erro ao fazer download do relatório: {e}")
        return redirect(url_for('consulta_relatorios'))

@app.route('/vulnerabilities')
def vulnerabilities():
    vulnerability_list = [doc.doc for doc in db.view('vulnerabilities/all_vulnerabilities', include_docs=True)]
    return render_template('vulnerabilities.html', title='Banco de Vulnerabilidades', vulnerability_list=vulnerability_list)

@app.route('/add_vulnerability', methods=['GET', 'POST'])
def add_vulnerability():
    if request.method == 'POST':
        save_vulnerability(
            request.form.get('name'),
            request.form.get('owasp_top10'),
            request.form.get('cwe'),
            request.form.get('cve'),
            request.form.get('description'),
            request.form.get('inputs_for_poc'),
            request.form.get('technical_impact'),
            request.form.get('business_impact'),
            request.form.get('correction_recommendation'),
            request.form.get('references')
        )
        return redirect(url_for('vulnerabilities'))
    return render_template('add_vulnerability.html', title='Adicionar Vulnerabilidade')

@app.route('/view_vulnerability/<vulnerability_id>')
def view_vulnerability(vulnerability_id):
    vulnerability = db.get(vulnerability_id)
    return render_template('view_vulnerability.html', vulnerability=vulnerability)

@app.route('/update_vulnerability/<vulnerability_id>', methods=['GET', 'POST'])
def update_vulnerability(vulnerability_id):
    vulnerability = db.get(vulnerability_id)
    if not vulnerability:
        return "Vulnerabilidade não encontrada", 404

    if request.method == 'POST':
        vulnerability.update({
            'name': request.form['name'],
            'owasp_top10': request.form['owasp_top10'],
            'cwe': request.form['cwe'],
            'cve': request.form['cve'],
            'description': request.form['description'],
            'inputs_for_poc': request.form['inputs_for_poc'],
            'technical_impact': request.form['technical_impact'],
            'business_impact': request.form['business_impact'],
            'correction_recommendation': request.form['correction_recommendation'],
            'references': request.form['references']
        })
        db.save(vulnerability)
        return redirect(url_for('vulnerabilities'))

    return render_template('update_vulnerability.html', vulnerability=vulnerability)

@app.route('/delete_vulnerability/<vulnerability_id>', methods=['POST'])
def delete_vulnerability(vulnerability_id):
    try:
        doc = db[vulnerability_id]
        db.delete(doc)
        flash('Vulnerabilidade deletada com sucesso.', 'success')
    except Exception as e:
        flash(f'Erro ao deletar vulnerabilidade: {e}', 'error')
    return redirect(url_for('vulnerabilities'))

@app.errorhandler(404)
def page_not_found(e):
    app.logger.error('Página 404 acionada', exc_info=e)
    return render_template('404.html'), 404

@app.route('/delete_relatorio/<report_name>', methods=['POST'])
def delete_relatorio(report_name):
    try:
        doc = next((doc.doc for doc in db.view('_all_docs', include_docs=True) if doc.doc.get('report_name') == report_name), None)
        if doc:
            pdf_path = doc.get('pdf_path')
            if pdf_path and os.path.exists(pdf_path):
                os.remove(pdf_path)
            db.delete(doc)
            flash(f'Relatório {report_name} deletado com sucesso.', 'success')
        else:
            flash(f'Relatório {report_name} não encontrado.', 'error')
    except Exception as e:
        flash(f'Erro ao deletar relatório: {e}', 'error')
    return redirect(url_for('consulta_relatorios'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_folder_and_unzip(zip_path, extract_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    except Exception as e:
        print(f"Erro ao extrair arquivo ZIP: {e}")

def clean_and_rename_file(file_path, new_filename):
    try:
        directory, old_filename = os.path.split(file_path)
        old_filename_without_extension = os.path.splitext(old_filename)[0]
        new_filename_with_extension = f"{new_filename}.zip"
        new_path = os.path.join(directory, new_filename_with_extension)
        os.rename(file_path, new_path)
        return new_path
    except Exception as e:
        print(f"Erro ao renomear arquivo: {e}")

def convert_md_to_pdf(extract_path):
    try:
        os.chdir(extract_path)
        md_files = [f for f in os.listdir('.') if f.endswith('.md')]
        if not md_files:
            print("Nenhum arquivo .md encontrado.")
            return
        subprocess.run([
            'pandoc'] + md_files + [
            '-o', 'result.pdf',
            '--from', 'markdown', '--template', 'eisvogel.tex',
            '--highlight-style', 'breezedark', '--toc', '-N',
            '--top-level-division=chapter',
            '--pdf-engine=xelatex'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar pandoc: {e}")
    finally:
        os.chdir(os.getcwd())

def store_report_metadata(report_name, pdf_path):
    doc = {
        'report_name': report_name,
        'pdf_path': pdf_path,
        'creation_date': str(datetime.now()),
        'status': 'completed'
    }
    db.save(doc)

def get_reports_list():
    return [doc.doc['report_name'] for doc in db.view('_all_docs', include_docs=True) if 'report_name' in doc.doc]

def save_vulnerability(name, owasp_top10, cwe, cve, description, inputs_for_poc, technical_impact, business_impact, correction_recommendation, references):
    doc = {
        'type': 'vulnerability',
        'name': name,
        'owasp_top10': owasp_top10,
        'cwe': cwe,
        'cve': cve,
        'description': description,
        'inputs_for_poc': inputs_for_poc,
        'technical_impact': technical_impact,
        'business_impact': business_impact,
        'correction_recommendation': correction_recommendation,
        'references': references
    }
    db.save(doc)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0', port=80)
