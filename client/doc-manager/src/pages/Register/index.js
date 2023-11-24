import { useNavigate } from 'react-router-dom'
import { Button, Form, Input, Card, message } from 'antd'
import { UserOutlined, LockOutlined, MailOutlined } from '@ant-design/icons'
import { axiosAPI as axios } from '../../utils'
import styles from './index.module.css'


const Register = () => {
  const navigate = useNavigate()
  const onFinish = async (e) => {
    console.log(`username:${e.username}; email: ${e.email}; password:${e.password}`)
    const result = await axios.post('/api/v1/register/', {
      username: e.username,
      email: e.email,
      password: e.password
    })

    if (result.status === 200) {
      message.success('Register successed! Jump to Login page!')
      navigate('/login')
    } else {
      message.error(`Register failed ! Error: result ${result.data}`)
    }
  }

  return (<div className={styles.LoginForm}>

    <Card title="Register Page" className={styles.LoginCard}>
      <Form
        name="register"
        initialValues={{ remember: true }}
        onFinish={onFinish}
      >
        <Form.Item
          name="username"
          rules={[{ required: true, message: 'Username is required!' }]}
        >
          <Input prefix={<UserOutlined className="site-form-item-icon" />} placeholder="Username" />
        </Form.Item>

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
          <Button type="primary" htmlType="submit" className={styles.register_button}>
            Register
          </Button>
        </Form.Item>

        <div className={styles.loginTips} onClick={() => navigate('/login')}>
          Already have an account? <span>Sign in</span>
        </div>
      </Form>
    </Card>

  </div>)
}

export default Register

