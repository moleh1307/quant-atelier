import {build} from 'esbuild';
import {mkdir, readFile, writeFile} from 'node:fs/promises';
const output = new URL('../static/vendor/codemirror/', import.meta.url);
await mkdir(output, {recursive: true});
const result = await build({
  entryPoints: [new URL('editor.mjs', import.meta.url).pathname],
  outfile: new URL('python-editor.js', output).pathname,
  bundle: true, minify: true, format: 'iife', globalName: 'QuantPythonEditor',
  target: ['es2020'], legalComments: 'eof', metafile: true
});
const packages = new Set(Object.keys(result.metafile.inputs)
  .filter(path => path.includes('node_modules/'))
  .map(path => path.split('node_modules/')[1].split('/').slice(0, path.split('node_modules/')[1].startsWith('@') ? 2 : 1).join('/')));
const licenses = [];
for (const name of [...packages].sort()) {
  const root = new URL(`node_modules/${name}/`, import.meta.url);
  const pkg = JSON.parse(await readFile(new URL('package.json', root), 'utf8'));
  let license;
  for (const filename of ['LICENSE', 'LICENSE.txt', 'LICENSE.md']) {
    try {license = await readFile(new URL(filename, root), 'utf8'); break;} catch {}
  }
  if (!license) throw new Error(`Missing license for ${name}`);
  licenses.push(`${name}@${pkg.version}\n${license.trim()}`);
}
await writeFile(new URL('LICENSES.txt', output), licenses.join('\n\n----------------------------------------\n\n')+'\n');
console.log(`Built offline Python editor; ${packages.size} dependency licenses retained.`);
