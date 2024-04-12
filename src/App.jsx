import Tab from './components/Tab.jsx';
import BarraMenu from './components/BarraMenu.jsx';
import { Layout, Card, ConfigProvider } from 'antd';
import './App.css'
const { Header, Content, Footer } = Layout;

function App() {
  return (
    <Layout>
      <Header className='bg-zinc-900 text-sm space-x-0.5 text-white h-fit pl-0'>
        <BarraMenu />
      </Header>

      <Content>
        <Tab />
      </Content>

      <Footer className='bg-slate-800 h-60 m-0 p-0'>
        <ConfigProvider theme={{
          components:{
            Card:{
              headerHeight:0,
              colorText:'#CCCCCC',
              colorBorderSecondary:'#14532D',
              algorithm:true,
              paddingLG:10
            }
          }
        }}>
          <Card
            title="Salida"
            bordered={false}
            style={{
              width: '100%',
              height: '100%',
              borderRadius: 0,
              backgroundColor: '#2e2e2e',
            }}
          >
            <p>Error...</p>
            <p>Error...</p>
            <p>Error...</p>
          </Card>
        </ConfigProvider>
      </Footer>
    </Layout>
  )

}

export default App;
