import React, { useRef, useState } from 'react';
import { Tabs, ConfigProvider, Button, Tooltip } from 'antd';
import { CaretRightOutlined, FileOutlined } from '@ant-design/icons';
import EditorCodigo from './EditorCodigo.jsx';
import './Tab.css';

const operations = <Tooltip title="Compilar"><Button type="primary" shape="circle" icon={<CaretRightOutlined />} className='mr-12' /></Tooltip>

const initialItems = [
  {
    label: 'Sin-Título',
    children: <EditorCodigo />,
    key: '1',
    closable: false,
    icon: <FileOutlined />
  },
];

const Tab = () => {
  const [activeKey, setActiveKey] = useState(initialItems[0].key);
  const [items, setItems] = useState(initialItems);
  const newTabIndex = useRef(0);
  const onChange = (newActiveKey) => {
    setActiveKey(newActiveKey);
  };
  const add = () => {
    const newActiveKey = `newTab${newTabIndex.current++}`;
    const newPanes = [...items];
    newPanes.push({
      label: 'Nueva pestaña',
      children: <EditorCodigo />,
      key: newActiveKey,
      icon: <FileOutlined />
    });
    setItems(newPanes);
    setActiveKey(newActiveKey);
  };
  const remove = (targetKey) => {
    let newActiveKey = activeKey;
    let lastIndex = -1;
    items.forEach((item, i) => {
      if (item.key === targetKey) {
        lastIndex = i - 1;
      }
    });
    const newPanes = items.filter((item) => item.key !== targetKey);
    if (newPanes.length && newActiveKey === targetKey) {
      if (lastIndex >= 0) {
        newActiveKey = newPanes[lastIndex].key;
      } else {
        newActiveKey = newPanes[0].key;
      }
    }
    setItems(newPanes);
    setActiveKey(newActiveKey);
  };
  const onEdit = (targetKey, action) => {
    if (action === 'add') {
      add();
    } else {
      remove(targetKey);
    }
  };

  return (
    <ConfigProvider
      theme={{
        components: {
          Tabs: {
            colorBgContainer: '#1e1e1e',
            colorBorderSecondary: '#10B73B',
            borderRadiusLG: 0,
            lineType: '',
            itemColor: '#ACACAC',
            itemHoverColor: '#40BE20',
            itemSelectedColor: '#41DC27',
            colorText: '#fff',
            colorTextHeading: '#fff',
            colorTextDescription: '#ACACAC',
            itemActiveColor: '#fff'
            //algorithm:true
          },
          Button: {
            colorPrimary: '#0D931F',
            colorPrimaryHover: '#13C12A',
            algorithm: true
          }
        }
      }}

    >
      <div className="border border-green-900" >
        <Tabs
          type="editable-card"
          onChange={onChange}
          activeKey={activeKey}
          onEdit={onEdit}
          items={items}
          tabBarExtraContent={operations}
        ></Tabs>
      </div>

    </ConfigProvider>
  );
};
export default Tab;