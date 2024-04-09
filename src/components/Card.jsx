import React from 'react';
import { Card, ConfigProvider } from 'antd';
const CardComponent = () => (
  <ConfigProvider
    theme={{
      components:{
        Card:{
          borderRadiusLG:0,
          colorBorderSecondary:'#14532D',
          colorText:'#fff'
        }
      }
    }}
  >
    <Card
      style={{
        width: '100%',
        backgroundColor: '#2e2e2e'
        
      }}
    >
      <p>Card content</p>
      <p>Card content</p>
      <p>Card content</p>
    </Card>
  </ConfigProvider>
);
export default CardComponent;