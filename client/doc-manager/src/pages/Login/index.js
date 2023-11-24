import { useNavigate } from 'react-router-dom'
import { Button, Checkbox, Form, Input, Card, message } from 'antd'
import { LockOutlined, MailOutlined } from '@ant-design/icons'
import { axiosAPI as axios, TOKEN_NAME } from '../../utils'
import styles from './index.module.css'


const Login = () => {
    const navigate = useNavigate()
    const onFinish = async (e) => {
        console.log(`email: ${e.email} password:${e.password}`)
        const result = await axios.post('/api/v1/login/', {
            username: e.email,
            password: e.password
        })

        if (result.status === 200) {
            localStorage.setItem(TOKEN_NAME, result.data.token)
            message.success('Login successed!')
            navigate('/')
        } else {
            message.error(`Log in failed ! Error: ${result.data}`)
        }
    }


    return (<div className={styles.LoginForm}>
        <Card title="LogIn Page" className={styles.LoginCard}>
            <Form
                name="login"
                initialValues={{ remember: true }}
                onFinish={onFinish}
            >
                <Form.Item
                    name="email"
                    rules={[{ required: true, message: 'Email is required!' }]}
                >
                    <Input prefix={<MailOutlined className="site-form-item-icon" />} placeholder="Email" />
                </Form.Item>
                <Form.Item
                    name="password"
                    rules={[{ required: true, message: 'password is required!' }]}
                >
                    <Input
                        prefix={<LockOutlined className="site-form-item-icon" />}
                        type="password"
                        placeholder="Password"
                    />
                </Form.Item>
                <Form.Item>
                    <Form.Item name="remember" valuePropName="checked" noStyle>
                        <Checkbox>Remember me</Checkbox>
                    </Form.Item>

                </Form.Item>

                <Form.Item>
                    <Button type="primary" htmlType="submit" className={styles.login_button}>
                        Log in
                    </Button>
                </Form.Item>
                <div className={styles.RegisterTips} onClick={() => navigate('/register')}>
                    Haven't got an account yet? <span>Sign up </span>
                </div>
            </Form>
        </Card>

    </div >)
}

export default Login

