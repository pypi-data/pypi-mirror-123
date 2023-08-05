#import ibm_db
#import ibm_db_dbi as db
from typing import Any, Dict, Optional

from airflow.hooks.dbapi_hook import DbApiHook
from airflow.models.connection import Connection


class DB2Hook(DbApiHook):
    """
    General hook for DB2 access.
    """
    conn_name_attr = 'db2_conn_id'
    default_conn_name = 'db2_default'
    conn_type = 'DB2'
    hook_name = 'DB2 Connection'

    @staticmethod
    def get_connection_form_widgets() -> Dict[str, Any]:
        """Returns connection widgets to add to connection form"""
        from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
        from flask_babel import lazy_gettext
        from wtforms import StringField

        return {
            "security_mechanism": StringField(lazy_gettext('Security Mechanism'), widget=BS3TextFieldWidget())
        }
    
    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        """Returns custom field behaviour"""
        return {
            "hidden_fields": ['schema', 'extra'],
            "relabeling": {'schema': 'database'}
        }

    def get_conn(self):
        conn: Connection = self.get_connection(getattr(self, self.conn_name_attr))
        host: str = conn.host
        login: str = conn.login
        psw: str = conn.password
        port: str = conn.port
        database: str = conn.schema
        security_mechanism: Optional[str] = conn.extra_dejson.get('security_mechanism')
    
        # conn = conn = db.Connection(
        #     ibm_db.connect(
        #         f'''
        #         DATABASE={database};\
        #         HOSTNAME={host};\
        #         PORT={port};\
        #         PROTOCOL=TCPIP;\
        #         SECURITYMECHANISM={security_mechanism};\
        #         UID={login};\
        #         PWD={psw};\
        #         ''', '', ''))
        
        return conn
        

