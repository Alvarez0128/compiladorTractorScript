import React from 'react';
import { Dropdown, message, Space,ConfigProvider } from 'antd';

const onClick = ({ key }) => {
  message.info(`Click on item ${key}`);
};

const items = [
  {
    label: '1st menu item',
    key: '1',
  },
  {
    label: '2nd menu item',
    key: '2',
  },
  {
    label: '3rd menu item',
    key: '3',
  },
];

const MenuDropdown = ({ label }) => (
  <Dropdown menu={{ items, onClick }} trigger={['click']}>
    <a onClick={(e) => e.preventDefault()} className="cursor-default">
      <Space className='hover:bg-green-600 px-3 py-0.5'>
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
    <MenuDropdown label="Archivo" />
    <MenuDropdown label="Editar" />
    <MenuDropdown label="Ver" />
    <MenuDropdown label="Ayuda" />
  </ConfigProvider>
);

export default BarraMenu;
