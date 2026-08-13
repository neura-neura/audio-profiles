import base64, json, pathlib, sys
payload = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
for path, encoded in payload.items():
    target = pathlib.Path(path)
    target.write_text(base64.b64decode(encoded).decode('utf-8'), encoding='utf-8', newline='\n')
    print(f'wrote {target} {target.stat().st_size}')
