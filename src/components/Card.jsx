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
      <p>Error 1</p>
      <p>Error 2</p>
      <p>Error 3</p>
    </Card>
  </ConfigProvider>
);
export default CardComponent;