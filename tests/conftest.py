import os
import sys
import warnings

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Suppress known deprecation warnings from dependencies
warnings.filterwarnings("ignore", category=DeprecationWarning, module="strawberry.extensions.*")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="strawberry.fastapi.router")

# Automatically set required environment variables for tests
if not os.environ.get('DEMO'):
    os.environ['DEMO'] = 'True'

if not os.environ.get('GQLUG_ENDPOINT_URL'):
    os.environ['GQLUG_ENDPOINT_URL'] = 'http://localhost:8001'

if not os.environ.get('DEMODATA'):
    os.environ['DEMODATA'] = 'False'

if not os.environ.get('JWTPUBLICKEYURL'):
    os.environ['JWTPUBLICKEYURL'] = 'http://localhost:33001/oauth/publickey'

if not os.environ.get('JWTRESOLVEUSERPATHURL'):
    os.environ['JWTRESOLVEUSERPATHURL'] = 'http://localhost:33001/oauth/userinfo'