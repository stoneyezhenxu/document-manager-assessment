import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Layout, Menu, theme, message, Table, Button } from 'antd'
import { FileOutlined, FolderOpenOutlined, CustomerServiceOutlined, PictureOutlined, LaptopOutlined } from '@ant-design/icons'
import { axiosAPI as axios, removeToken } from '../../utils'
import styles from './index.module.css'


const { Header, Content, Footer, Sider } = Layout




const Home = () => {
  const navigate = useNavigate()
  const [files, setFiles] = useState([])  // all files
  const [curfiles, setCurfiles] = useState([]) // type files
  const [isLoaded, setIsLoaded] = useState(false)

  useEffect(() => {
    const getUserFiles = async () => {
      try {
        const result = await axios.get('/api/v1/files')
        console.log(result.data)
        if (result.status === 200) {
          setFiles(result.data)
          setCurfiles(result.data)
          setIsLoaded(true)
        }

      } catch (error) {
        message.info('please login first!')
      }

    }
    getUserFiles()
  }, [])
  return (isLoaded && (<MyLayout files={files} curfiles={curfiles} setCurfiles={setCurfiles} navigate={navigate} />)
  )
}





const MainContentTable = ({ curfiles, navigate }) => {
  const columns = [

    {
      title: 'FileName',
      dataIndex: 'file_name',
      key: 'file_name'
    },

    {
      title: 'Versions',
      dataIndex: 'file_version',
      key: 'file_version'
    },

    {
      title: 'FileUrl',
      dataIndex: 'file_url',
      key: 'file_url',
      render: (text) => <a onClick={() => {
        navigate(text)
      }
      }>{text}</a>,
    },


    {
      title: 'Size',
      dataIndex: 'file_size',
      key: 'file_size',
    },

    {
      title: 'FileType',
      dataIndex: 'file_type',
      key: 'file_type'
    },
    {
      title: 'CreateTime',
      dataIndex: 'create_at',
      key: 'create_at'
    },

    {
      title: 'Desc',
      dataIndex: 'file_desc',
      key: 'file_desc'
    },
  ]

  return <Table columns={columns} dataSource={curfiles} />
}





const LayoutSide = ({ files, setCurfiles }) => {
  const [collapsed, setCollapsed] = useState(false)
  const getItem = (label, key, icon, children) => {
    return { key, icon, children, label }
  }
  const fileTypeList = ['Images', 'Docs', 'Videos', 'Procedures', 'Others']
  const fileType = [
    {
      key: 0,
      icon: <PictureOutlined />

    }, {
      key: 1,
      icon: <FileOutlined />,

    },
    {
      key: 2,
      icon: <CustomerServiceOutlined />,

    },
    {
      key: 3,
      icon: <LaptopOutlined />,

    },
    {
      key: 4,
      icon: <FolderOpenOutlined />,
    }
  ]
  const sider_items = [
    getItem('All Files', 's2', <FolderOpenOutlined />,
      fileType.map((item, index) => getItem(fileTypeList[index], item.key, item.icon)))
  ]
  const SideItemsOnClick = (e) => {
    var typeFilesData = files.filter((items) => items.file_type == fileTypeList[e.key])
    setCurfiles(typeFilesData)
  }

  return <Sider collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}>
    <div className="demo-logo-vertical" />
    <Menu onClick={SideItemsOnClick} theme="dark" defaultSelectedKeys={['1']} mode="inline" items={sider_items} />

  </Sider>

}

const MyLayout = ({ files, curfiles, setCurfiles, navigate }) => {

  const LogoutClick = async () => {

    const result = await axios.get('/api/v1/logout/')
    console.log('LogoutClick result', result.data)
    if (result.status === 200) {
      message.success('Logout successed!')
      removeToken()
      navigate('/login')

    } else {
      message.error(`Logout failed ! Error: ${result.data}`)
    }
  }


  const { token: { colorBgContainer } } = theme.useToken()
  return (<div>
    <Layout style={{ minHeight: '100vh' }}>
      <LayoutSide files={files} setCurfiles={setCurfiles} />
      <Layout >
        <Header style={{ padding: 0, background: colorBgContainer }} />
        <Content style={{ margin: '0 16px' }}>
          <div className={styles.ContentHeader}>
            <div> <Button type='primary' onClick={() => navigate('/upload')}>Upload File </Button></div>
            <div>Welcome to Propylon Document Management:  stoneye</div>
            <div> <Button type='primary' onClick={LogoutClick}>Logout </Button>
            </div>
          </div>
          <div className={styles.ContentMain}>
            <MainContentTable curfiles={curfiles} navigate={navigate} />
          </div>
        </Content>

        <Footer style={{ textAlign: 'center' }}>
          Document Management ©2023 Created by Propylon
        </Footer>
      </Layout>
    </Layout>
  </div>)
}
export default Home