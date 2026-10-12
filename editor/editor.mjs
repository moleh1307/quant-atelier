import {EditorState, EditorSelection, StateEffect} from '@codemirror/state';
import {EditorView, keymap, lineNumbers, highlightActiveLine, highlightActiveLineGutter,
  drawSelection, highlightSpecialChars, dropCursor} from '@codemirror/view';
import {python} from '@codemirror/lang-python';
import {syntaxHighlighting, HighlightStyle, indentUnit, indentOnInput, bracketMatching,
  foldGutter, foldKeymap} from '@codemirror/language';
import {defaultKeymap, history, historyKeymap, indentWithTab} from '@codemirror/commands';
// Only bracket closing is used from this package. No autocompletion extension or keymap.
import {closeBrackets, closeBracketsKeymap} from '@codemirror/autocomplete';
import {tags} from '@lezer/highlight';

const sessions = new Map();
const colours = HighlightStyle.define([
  {tag: tags.keyword, color: '#934b72'},
  {tag: [tags.string, tags.special(tags.string)], color: '#54713c'},
  {tag: [tags.number, tags.bool, tags.null], color: '#ad5027'},
  {tag: tags.comment, color: '#64705e', fontStyle: 'italic'},
  {tag: [tags.function(tags.variableName), tags.definition(tags.variableName)], color: '#2e6d8a'},
  {tag: [tags.className, tags.typeName], color: '#84622e'},
  {tag: [tags.operator, tags.punctuation], color: '#596655'},
  {tag: tags.invalid, color: '#b23f2c'}
]);

export function exitKeys(onExit) {
  let armed = false;
  return {
    keydown(event) {
      if (event.key === 'Escape') { armed = true; event.preventDefault(); return true; }
      if (event.key === 'Tab' && armed) {
        armed = false;
        if (typeof onExit === 'function' && onExit(event.shiftKey) !== false) { event.preventDefault(); return true; }
      }
      armed = false;
      return false;
    },
    blur() { armed = false; }
  };
}

export function mount({parent, id, value, onChange, status, onExit}) {
  // Preserve selection and undo history across app renders, independently per exercise.
  const cached = sessions.get(id);
  const nonce = document.querySelector('meta[name="editor-style-nonce"]')?.content || '';
  const extensions = [
    python(), lineNumbers(), highlightSpecialChars(), history(), drawSelection(), dropCursor(),
    indentUnit.of('    '), EditorState.tabSize.of(4), indentOnInput(), bracketMatching(),
    closeBrackets(), foldGutter(), highlightActiveLine(), highlightActiveLineGutter(),
    syntaxHighlighting(colours), EditorView.cspNonce.of(nonce),
    EditorView.domEventHandlers(exitKeys(onExit)),
    EditorView.contentAttributes.of({
      'aria-label': 'Python solution', 'aria-describedby': 'editor-help',
      spellcheck: 'false', autocorrect: 'off', autocapitalize: 'off',
      autocomplete: 'off', 'data-testid': 'python-editor'
    }),
    keymap.of([...closeBracketsKeymap, ...defaultKeymap, ...historyKeymap, ...foldKeymap, indentWithTab]),
    EditorView.updateListener.of(update => {
      sessions.set(id, update.state);
      if (update.docChanged) onChange(update.state.doc.toString());
      if (update.docChanged || update.selectionSet) showPosition(update.state);
    })
  ];
  function showPosition(state) {
    const cursor = state.selection.main.head, line = state.doc.lineAt(cursor);
    if (status) status.textContent = `Ln ${line.number}, Col ${cursor-line.from+1}`;
  }
  // Reconfigure cached extensions: callbacks/status refer to this fresh render's nodes.
  const state = cached && cached.doc.toString() === value
    ? cached.update({effects: StateEffect.reconfigure.of(extensions)}).state
    : EditorState.create({doc: value, extensions});
  parent.replaceChildren();
  const view = new EditorView({parent, state});
  sessions.set(id, state);
  showPosition(state);
  return {
    getValue: () => view.state.doc.toString(),
    goToLine(number) {
      const line = view.state.doc.line(Math.max(1, Math.min(view.state.doc.lines, number)));
      view.dispatch({selection: EditorSelection.cursor(line.from),
        effects: EditorView.scrollIntoView(line.from, {y: 'center'})});
      view.focus();
    },
    replace(value) {
      view.dispatch({changes: {from: 0, to: view.state.doc.length, insert: value},
        selection: EditorSelection.cursor(0), userEvent: 'input'});
      view.focus();
    },
    destroy() {sessions.set(id, view.state); view.destroy();}
  };
}
