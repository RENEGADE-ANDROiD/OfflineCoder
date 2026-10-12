"""Refresh the compatibility update manifest; website content lives in ../storefront."""
from pathlib import Path
import shutil
root=Path(__file__).resolve().parent
shutil.copy2(root.parent/'storefront/version.json',root/'version.json')
print('GitHub compatibility manifest refreshed. Build the official site with storefront/build_site.py.')
