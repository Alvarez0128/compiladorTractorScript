import React, { useRef, useState } from 'react';
import { Layout, Card, ConfigProvider, Button, Tooltip, Tabs, Table, message, Dropdown, Space, Tree, Modal, Image } from 'antd';
import { DownOutlined } from '@ant-design/icons';
import Editor from '@monaco-editor/react';
import { writeFile, readTextFile } from '@tauri-apps/api/fs';
import { open, save } from '@tauri-apps/api/dialog';
import './App.css'

const { Header, Content, Footer } = Layout;

const columns = [
  {
    title: 'Token',
    dataIndex: 'type',
    key: 'type',
  },
  {
    title: 'Lexema',
    dataIndex: 'value',
    key: 'value',
    render: (text) => <a>{text}</a>,
  },
  {
    title: 'Linea',
    dataIndex: 'line',
    key: 'line',
  },
  {
    title: 'Columna',
    key: 'column',
    dataIndex: 'column',
  },
];

function App() {
  const [tokens, setTokens] = useState([]);
  const [errors, setErrors] = useState([]);
  const [compilationMessage, setCompilationMessage] = useState('');
  const [codigo, setCodigo] = useState('');
  const [arbol, setArbol] = useState([]);
  const [modalVisible, setModalVisible] = useState(false);

  let table = <ConfigProvider theme={{
    components: {
      Table: {
        colorBgContainer: '#303030',
        algorithm: true,
        borderColor: '#282828',
        colorText: '#dcdcdc',
        rowHoverBg: '#353535',
        colorTextHeading: '#fff',
        stickyScrollBarBg: '#365d34',
      }
    }
  }}>
    <Table pagination={false} columns={columns} dataSource={tokens} id='tabla' />
  </ConfigProvider>

  let tree = <div className='font-mono font-bold rounded-lg p-5 text-lg overflow-auto' id='arbol'>
    <pre className='font-mono font-bold text-lg p-2'>
      Gramatica generada:<br />
      <ConfigProvider theme={{
        components: {
          Tree: {
            colorBgContainer: '#404040',
            algorithm: true,
            colorText: '#dcdcdc',
            nodeSelectedBg: '#606060',
            nodeHoverBg: '#505050'
          }
        }
      }}
      >
        <Tree
          showLine
          switcherIcon={<DownOutlined />}
          defaultExpandedKeys={['0-0-0']}
          // onSelect={onSelect}
          treeData={arbol}
          style={{ overflow: "auto", padding: "10px" }}
        />
      </ConfigProvider>
    </pre>
  </div>

  const itemsTabs = [
    {
      key: '1',
      label: 'Componentes Léxicos',
      children: table,
    },
    {
      key: '2',
      label: 'Análisis Sintáctico',
      children: tree,
    },
    {
      key: '3',
      label: 'Análisis Semántico',
      children: 'Content of Tab Pane 2',
    },
    {
      key: '4',
      label: 'Codigo Intermedio',
      children: 'Content of Tab Pane 3',
    },
    {
      key: '5',
      label: 'Codigo Optimizado',
      children: 'Content of Tab Pane 4',
    },
    {
      key: '6',
      label: 'Codigo Objeto',
      children: 'Content of Tab Pane 5',
    },
  ];

  const editorRef = useRef(null);

  function handleEditorDidMount(editor, monaco) {
    editorRef.current = editor;
  }
  const goToLineAndColumn = (line, column, text) => {
    if (editorRef.current) {
      const model = editorRef.current.getModel();
      const position = { lineNumber: line, column: column };
      const startOffset = model.getOffsetAt(position);
      const textLength = text.length;
      let endOffset = startOffset + textLength;
      let endPosition = model.getPositionAt(endOffset);

      // Check if the text exists at the position
      const currentText = model.getValueInRange({
        startLineNumber: line,
        startColumn: column,
        endLineNumber: endPosition.lineNumber,
        endColumn: endPosition.column,
      });

      if (currentText !== text) {
        // If text not found, select only one character
        endOffset = startOffset + 1;
        endPosition = model.getPositionAt(endOffset);
      }

      editorRef.current.revealPositionInCenter(position);
      editorRef.current.setPosition(position);
      editorRef.current.setSelection({
        startLineNumber: line,
        startColumn: column,
        endLineNumber: endPosition.lineNumber,
        endColumn: endPosition.column,
      });
      editorRef.current.focus();
    }
  };

  const compileCode = () => {
    fetch('http://localhost:5000/compile', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code: editorRef.current.getValue() }),
    })
      .then(response => response.json())
      .then(data => {
        //console.log(data[0].errors);
        console.log(data[1].title);
        if (data[0].tokens) {
          setTokens(data[0].tokens);
          if (data[1].title === "Producción detenida") {
            setArbol([{ title: "Árbol no generado" }])
          } else {
            setArbol([data[1]])
          }
          setErrors([]);
        }
        if (data[0].errors) {
          setErrors(data[0].errors);
          setCompilationMessage('Compilación exitosa');
        }
        editorRef.current.setPosition({ lineNumber: 1, column: 1 });

      })
      .catch(error => console.error('Error:', error));
  };

  const guardarArchivo = async () => {
    const codigo = editorRef.current.getValue();
    try {
      const result = await save({
        defaultPath: 'code.tsp',
        filters: [{
          name: 'TractorScript',
          extensions: ['tsp']
        }]
      });
      if (result) {
        await writeFile(result, codigo);
        message.success('Archivo guardado correctamente');
      } else {
        message.info('Guardado cancelado por el usuario');
      }
    } catch (error) {
      console.error('Error al guardar el archivo:', error);
      message.error('Error al guardar el archivo');
    }
  };

  const nuevoArchivo = () => {
    setCodigo('');
  }
  const abrirArchivo = async () => {
    try {
      const result = await open({

        filters: [{
          name: 'TractorScript',
          extensions: ['tsp']
        }]
      });
      if (result) {
        const codigo = await readTextFile(result);
        setCodigo(codigo);
        message.success('Abierto');
      } else {
        message.info('No abierto');
      }
    } catch (error) {
      console.error('Error al abrir el archivo:', error);
      message.error('Error al abrir el archivo');
    }
  };
  const onClick = ({ key }) => { }

  // Función para mostrar el modal
  const showModalInfoErrores = () => {
    setModalVisible(true);
  };

  // Función para ocultar el modal
  const handleCancel = () => {
    setModalVisible(false);
  };

  const itemsArchivo = [
    {
      label: 'Nuevo archivo',
      key: 'nuevo',
      onClick: () => {
        nuevoArchivo();
      },
    },
    {
      label: 'Abrir',
      key: 'abrir',
      onClick: () => {
        abrirArchivo();
      },
    },
    {
      label: 'Guardar',
      key: 'guardarc',
      onClick: () => {
        guardarArchivo();
      },
    },
  ];

  const itemsEditar = [
    {
      label: 'Copiar',
      key: 'copiar',
    },
    {
      label: 'Cortar',
      key: 'cortar',
    },
    {
      label: 'Pegar',
      key: 'pegar',
    },
  ];

  const itemsVer = [
    {
      label: 'Panel derecho',
      key: 'pander',
    },
    {
      label: 'Salida',
      key: 'salida',
    },
  ];

  const itemsAyuda = [
    {
      label: 'Documentación',
      key: 'documentacion',
    },
    {
      label: 'Soporte',
      key: 'soporte',
    },
  ];


  const MenuDropdown = ({ label, items }) => (
    <Dropdown menu={{ items, onClick }} trigger={['click']}>
      <a onClick={(e) => e.preventDefault()} className="cursor-default">
        <Space className=' text-white hover:bg-green-600 px-3 py-0.5 hover:text-white'>
          {label}
        </Space>
      </a>
    </Dropdown>
  );

  return (
    <Layout>
      <Header className='bg-zinc-900 text-sm text-white h-fit pl-0'>
        <ConfigProvider theme={{
          components: {
            Dropdown: {
              colorBgElevated: '#C9FFB6',
              borderRadiusLG: 2,
              colorText: '#000'
            }
          }
        }}>
          <MenuDropdown label="Archivo" items={itemsArchivo} />
          <MenuDropdown label="Editar" items={itemsEditar} />
          <MenuDropdown label="Ver" items={itemsVer} />
          <MenuDropdown label="Ayuda" items={itemsAyuda} />
        </ConfigProvider>

        <ConfigProvider theme={{
          components: {
            Button: {
              textHoverBg: 'rgba(22, 163, 74, 0)',
              colorText: '#fff',
              colorBgTextActive: 'rgba(22, 163, 74, 0.28)'
            }
          }
        }}>
          <Tooltip title="Compilar">
            <Button type='text' onClick={compileCode}>▶</Button>
          </Tooltip>
        </ConfigProvider>

      </Header>

      <Content id='content' className='border border-green-900 grid grid-cols-2'>
        <div>
          <Editor
            theme='vs-dark'
            height='100%'
            width='100%'
            options={{
              fontSize: '18',
            }}
            value={`${codigo}` ?? ""}
            onChange={(value) => setCodigo(value)}
            onMount={handleEditorDidMount}
            className='border-e border-green-900 pt-3 relative'
          />
        </div>
        <div className='px-6 '>
          <ConfigProvider
            theme={{
              components: {
                Tabs: {
                  itemSelectedColor: '#43BC4C',
                  algorithm: true,
                  inkBarColor: '#43BC4C',
                  itemColor: '#fff',
                  itemHoverColor: '#47AB4E',
                  colorText: '#fff',
                  colorBorderSecondary: '#8b8b8b',
                  colorBgContainer: '#282828'
                }
              }
            }}
          >
            <Tabs defaultActiveKey="1" items={itemsTabs} />
          </ConfigProvider>
        </div>
      </Content>

      <Footer className='bg-slate-800 h-60 m-0 p-0'>
        <ConfigProvider theme={{
          components: {
            Card: {
              headerHeight: 0,
              colorText: '#CCCCCC',
              colorBorderSecondary: '#14532D',
              paddingLG: 10,
              algorithm: true
            }
          }
        }}>
          <Card
            title="Salida ↴"
            bordered={false}
            style={{
              width: '100%',
              height: '35vh',
              borderRadius: 0,
              overflow: 'auto',
              backgroundColor: '#2e2e2e',
            }}
          >
            <div className='px-5 '>
              {errors.length === 0 && <p>{compilationMessage}</p>}
              {errors.map((error, index) => (
                <li key={index} onClick={showModalInfoErrores} className='hover:text-green-600 cursor-pointer transition'>
                  Error {error.type} - {error.description} en la <a onClick={(e) => { e.stopPropagation(); goToLineAndColumn(error.line, error.column, error.value); }} className="font-bold hover:underline"> línea {error.line}, columna {error.column}</a> lexema: {error.value}
                </li>
              ))}

              <Modal
                title="Gramatica de validación para el error"
                open={modalVisible}
                onCancel={handleCancel}
                footer={null}
              >
                foto de ejemplo de las gramaticas que quiere el fic
                <Image
                  width="90%"
                  src="../public/example.jpg"
                />
              </Modal>
            </div>
          </Card>
        </ConfigProvider>
      </Footer>
    </Layout>
  );
}

export default App;
