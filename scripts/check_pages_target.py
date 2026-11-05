"""Prevent publishing the new atlas build under the legacy Pages URL."""
import json
import os
from pathlib import Path

root = Path(__file__).resolve().parents[1]
site = json.loads((root / 'website/site.config.json').read_text())
actual = os.environ.get('GITHUB_REPOSITORY', '')
expected = site['publicationRepository']
if actual != expected:
    raise SystemExit(
        f'Pages target mismatch: {actual or "unset"}; expected {expected}. '
        'The URL migration has not been performed. Keep the legacy public site intact.'
    )
print(f'Pages publication target verified: {expected}')
