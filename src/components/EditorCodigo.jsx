import Editor from '@monaco-editor/react'

function EditorCodigo() {
  return (
    <Editor
      theme='vs-dark'
      height='70vh'
      options={{
        fontSize: '18'
      }}
    />
  )
}

export default EditorCodigo

