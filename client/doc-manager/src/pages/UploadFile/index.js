import { useNavigate } from 'react-router-dom'
import { useRef, useState } from 'react'
import { Form, Input, Button, message, Upload, Card } from 'antd'
import { UploadOutlined } from '@ant-design/icons'
import { axiosAPI as axios } from '../../utils'
import styles from './index.module.css'


const UploadFile = () => {
    const { TextArea } = Input

    const specificUrlRef = useRef('')
    const [finalUrlValue, setFinalUrlValue] = useState('/files/')
    const [curfileName, setCurfileName] = useState('')
    const navigate = useNavigate()
    const onFinish = async (values) => {
        console.log('Received values:', values)
        const cur_file_obj = values.files.fileList[0]
        var file_url = ''
        if (values.file_url.startsWith('/')) {
            file_url = `/files${values.file_url}${cur_file_obj.name}`
        }
        else {
            file_url = `/files/${values.file_url}${cur_file_obj.name}`
        }
        const formData = new FormData()
        console.log('values', values)
        formData.append('file_desc', values.file_desc)
        formData.append('file_url', file_url)
        formData.append('file_name', cur_file_obj.name)
        formData.append('file_size', cur_file_obj.size)
        formData.append('file_uid', cur_file_obj.uid)
        formData.append('file_obj', cur_file_obj.originFileObj)
        try {
            const response = await axios.post('/api/v1/files/', formData, {
            })
            message.info('Upload successful!')
            navigate('/')
            console.log('Upload successful:', response.data)
        } catch (error) {
            console.error('Upload failed:', error)
        }

    }

    return (
        <div className={styles.LoginForm}>
            <Card >
                <Form labelCol={{ span: 4 }}
                    wrapperCol={{ span: 14 }}
                    layout="horizontal"
                    style={{ maxWidth: 1200, minWidth: 800 }}
                    onFinish={onFinish}>

                    <Form.Item
                        name="files"
                        label="Upload"
                        rules={[{ required: true, message: 'Please upload a file' }]}
                    >
                        <Upload
                            name="file"
                            multiple={false}
                            maxCount={1}
                            beforeUpload={(e) => {
                                const filename = e.name
                                setCurfileName(filename)
                                return false
                            }} // Prevent automatic upload
                        >
                            <Button icon={<UploadOutlined />}>Click to Upload</Button>
                        </Upload>
                    </Form.Item>
                    <Form.Item label="Specific URL" name="file_url">
                        <Input
                            showCount
                            maxLength={50}
                            ref={specificUrlRef}
                            onChange={() => {
                                const inputValue = specificUrlRef.current.input.value
                                setFinalUrlValue(`/files${inputValue}${curfileName}`)
                            }}
                            placeholder='/xx/xxx/xxx/xxxxx' />
                    </Form.Item>
                    <Form.Item label="Final URL" name="file_final_url">
                        <Input readOnly placeholder={finalUrlValue} />
                    </Form.Item>

                    <Form.Item label="Descript" name="file_desc">
                        <TextArea autoSize showCount
                            maxLength={200} />
                    </Form.Item>

                    <Form.Item className={styles.SummitButton}>
                        <Button type="primary" htmlType="submit">
                            Submit
                        </Button>
                    </Form.Item>
                </Form >
            </Card>

        </div>

    )
}
export default UploadFile;

