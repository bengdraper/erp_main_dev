from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import inspect, Table, Column, Integer, String, MetaData
from src.models import db
import os

bp = Blueprint('tables', __name__, url_prefix='/tables')

# Only enable in development
ENABLE_TABLE_API = os.environ.get('FLASK_ENV', 'development') == 'development'

@bp.route('/', methods=['GET'])
def list_tables():
    if not ENABLE_TABLE_API:
        return jsonify({'error': 'Not available in production'}), 403
    inspector = inspect(db.engine)
    details = request.args.get('details', 'false').lower() == 'true'
    table_names = inspector.get_table_names()
    if not details:
        return jsonify({'tables': table_names})
    # Return columns and metadata for each table
    tables_info = {}
    for table in table_names:
        columns = inspector.get_columns(table)
        tables_info[table] = [
            {
                'name': col['name'],
                'type': str(col['type']),
                'nullable': col['nullable'],
                'default': col.get('default'),
                'primary_key': col.get('primary_key', False)
            }
            for col in columns
        ]
    return jsonify({'tables': tables_info})

# @bp.route('/', methods=['POST'])
# def create_table():
#     if not ENABLE_TABLE_API:
#         return jsonify({'error': 'Not available in production'}), 403
#     data = request.get_json()
#     table_name = data.get('table_name')
#     columns = data.get('columns', [])
#     if not table_name or not columns:
#         return jsonify({'error': 'table_name and columns required'}), 400
#     metadata = MetaData(bind=db.engine)
#     cols = [Column(col['name'], getattr(globals(), col['type'], String), primary_key=col.get('primary_key', False)) for col in columns]
#     try:
#         new_table = Table(table_name, metadata, *cols)
#         new_table.create()
#         return jsonify({'status': 'created', 'table': table_name}), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

