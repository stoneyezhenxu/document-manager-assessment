import React, { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { Button, Divider, Table, message, Card } from 'antd'
import { DownloadOutlined, UploadOutlined } from '@ant-design/icons'

import { axiosAPI as axios, getFileHashCode } from '../../utils'
import styles from './index.module.css'

const VersionsTable = ({ fileVersionsData, setfileVersionsData }) => {
    const columns = [{
        title: 'Versions',
        dataIndex: 'file_version',
        key: 'file_version',
        render: (version_id) => <a onClick={() => {

            setfileVersionsData([fileVersionsData[fileVersionsData.length - 1 - version_id]])
        }
        }>{version_id}</a>,
    },

    {
        title: 'Name',
        dataIndex: 'file_name',
        key: 'file_name'
    },

    {
        title: 'Size',
        dataIndex: 'file_size',
        key: 'file_size',
    },
    {
        title: 'Url',
        dataIndex: 'file_url',
        key: 'file_url'
    },
    {
        title: 'Type',
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

    return <div className={styles.TableContent}>
        <Table style={{ margin: 30 }} columns={columns} dataSource={fileVersionsData} />
    </div>


}



const CurFileInfos = ({ navigate, file_info }) => {
    const downloadClick = async (file_info) => {
        try {
            const result = await axios.get(`/api/v1/files/content?file_uuid=${file_info.file_uuid.replace('-', '')}&file_type=${file_info.file_type}&file_name=${file_info.file_name}`, {
                responseType: 'blob'
            })
            console.log("file_uuid: ", file_info.file_uuid)
            console.log(result)
            var filename = file_info.name

            if (result.status === 200) {
                message.success('Download successed!')
                const blob = new Blob([result.data], { type: result.headers['content-type'] })
                const url = window.URL.createObjectURL(blob)
                const link = document.createElement('a')
                link.href = url
                var filename = `revision_${file_info.file_version}_${file_info.file_name}`
                link.setAttribute('download', filename)
                document.body.appendChild(link)
                link.click()
                document.body.removeChild(link)
            } else {
                message.error(' Download Failed!')
            }
        } catch (error) {
            console.error('Download Failed')
        }
    }





    return (<>

        <div className={styles.Card}>
            <Card
                title={`Current Version:  ${file_info.file_version}`}
                bordered={true}
                headStyle={{ backgroundColor: 'skyblue' }}
                hoverable={true}
                style={{
                    width: 600,
                    margin: 20,
                    backgroundColor: "whitesmoke"
                }}
            >
                <div className={styles.CardInfos}>
                    <div>Name: <span>{file_info.file_name}</span></div>
                    <div>Size: <span>{file_info.file_size}</span></div>
                    <div>URL: <span>{file_info.file_url}</span></div>
                    <div>Type: <span>{file_info.file_type}</span></div>
                    <div>Desc: <span>{file_info.file_desc}</span></div>
                </div>

            </Card>

            <div className={styles.CardButtons}>
                <div><Button type="primary" icon={<UploadOutlined />} onClick={() => { navigate('/upload') }}>Upload New Version</Button></div>
                <div><Button type="primary" icon={<DownloadOutlined />} onClick={() => downloadClick(file_info)}>Download</Button></div>

            </div >

        </div >


    </>)


}


const FileVersionDetails = () => {

    const navigate = useNavigate()
    const [fileVersionsData, setfileVersionsData] = useState([])
    const [curfileVersion, setCurFileVersion] = useState(0)
    const [isLoaded, setIsLoaded] = useState(false)
    const location = useLocation()
    const searchParams = new URLSearchParams(location.search)
    console.log('location.pathname', location.pathname)
    const file_url = location.pathname
    const revision = searchParams.get('revision')
    const fileUrlHashcode = getFileHashCode(`${file_url}`)
    console.log('fileUrlHashcode', fileUrlHashcode)
    useEffect(() => {
        const getfileVersionsData = async () => {
            try {
                const result = await axios.get(`/api/v1/files/${fileUrlHashcode}?revision=${revision}`)
                console.log(result)
                if (result.status === 200) {
                    console.log(result.data)
                    setfileVersionsData(result.data)
                    setCurFileVersion(revision)
                    setIsLoaded(true)
                }
                else {
                    message.info('No file exist, error!')
                    navigate('/error')
                }
            } catch (error) {
                message.info('please login first!')
                // navigate('/login')
            }
        }
        getfileVersionsData()
    }, [location])






    return (isLoaded && <div>

        <CurFileInfos navigate={navigate} file_info={fileVersionsData[fileVersionsData.length === 1 ? 0 : fileVersionsData.length - 1 - curfileVersion]} />
        {
            fileVersionsData.length > 1 ? (
                <>
                    <Divider />
                    <VersionsTable fileVersionsData={fileVersionsData} setfileVersionsData={setfileVersionsData} />
                </>
            ) : <></>
        }
    </div >)

}

export default FileVersionDetails

