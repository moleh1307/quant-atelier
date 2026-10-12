# Local CodeMirror Python editor

CodeMirror 6 and its Python grammar are bundled into `python-editor.js` for offline use. No CDN, account, API or language server. Exact versions and transitive integrity hashes are pinned in `../../../editor/package-lock.json`. `LICENSES.txt` preserves the licenses of all 14 bundled dependency packages.

Canonical configuration: `editor/editor.mjs` in the project root. Uses Python syntax highlighting, line numbers, bracket/quote closing, bracket matching, four-space indentation, folding and undo history. The autocompletion extension, completion keymap and completion UI are deliberately excluded. The autocomplete package contributes only its bracket-closing exports.

Rebuild from the project root:

```sh
cd editor
npm ci
npm run build
```

Node/npm are build tools only; opening the website still requires only the Python launcher. The server provides a style nonce so CodeMirror's generated styles can load under the existing Content Security Policy; inline scripts remain disallowed.

Primary upstream sources: [CodeMirror reference](https://codemirror.net/docs/ref/), [Python language package](https://github.com/codemirror/lang-python), [keyboard Tab handling](https://codemirror.net/examples/tab/).
