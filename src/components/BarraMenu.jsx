import React from 'react';
import { Dropdown, message, Space, ConfigProvider } from 'antd';

const onClick = ({ key }) => {
  message.info(`Click on item ${key}`);
};

const itemsArchivo = [
  {
    label: 'Nuevo archivo',
    key: '1',
  },
  {
    label: 'Abrir',
    key: '2',
  },
  {
    label: 'Guardar',
    key: '3',
  },
  {
    label: 'Guardar como',
    key: '4',
  },
];

const itemsEditar = [
  {
    label: 'Copiar',
    key: '1',
  },
  {
    label: 'Cortar',
    key: '2',
  },
  {
    label: 'Pegar',
    key: '3',
  },
];

const itemsVer = [
  {
    label: 'Vista previa',
    key: '1',
  },
  {
    label: 'Opciones de visualización',
    key: '2',
  },
];

const itemsAyuda = [
  {
    label: 'Documentación',
    key: '1',
  },
  {
    label: 'Soporte',
    key: '2',
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

const BarraMenu = () => (
  <ConfigProvider theme={{
    components:{
      Dropdown:{
        colorBgElevated:'#C9FFB6',
        borderRadiusLG:2,
        colorText:'#000'
      }
    }
  }}>
    <MenuDropdown label="Archivo" items={itemsArchivo} />
    <MenuDropdown label="Editar" items={itemsEditar} />
    <MenuDropdown label="Ver" items={itemsVer} />
    <MenuDropdown label="Ayuda" items={itemsAyuda} />
  </ConfigProvider>
);

export default BarraMenu;
