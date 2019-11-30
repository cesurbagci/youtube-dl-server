from api import app
import os
from collections import ChainMap

app_defaults = {
    'YDL_SERVER_HOST': '0.0.0.0',
    'YDL_SERVER_PORT': 3001
}

app_vars = ChainMap(os.environ, app_defaults)

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    # from waitress import serve
    # serve(app, host=app_defaults['YDL_SERVER_HOST'], port=app_defaults['YDL_SERVER_PORT'], debug=True)
    
    app.run(host=app_defaults['YDL_SERVER_HOST'], port=app_defaults['YDL_SERVER_PORT'], debug=False)