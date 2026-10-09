"""Retain the output of one development compilation; not a final proof receipt."""
import sys
from datetime import datetime, timezone
import verify

stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
directory = verify.AREA / 'development' / stamp
directory.mkdir(parents=True)
module = sys.argv[1]
result = verify.run([verify.LAKE, 'env', 'lean', verify.ROOT / 'Experiments' / (module + '.lean')], directory, module)
verify.write(directory / 'command.json', result)
print((verify.ROOT / result['stdout']).read_text(encoding='utf-8'))
print((verify.ROOT / result['stderr']).read_text(encoding='utf-8'))
print('DEVELOPMENT_EXIT', result['exit_code'], 'LOG', directory)
raise SystemExit(result['exit_code'])
