import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Form, Input, Button, Card, Typography, message } from 'antd'
import { MailOutlined, LockOutlined } from '@ant-design/icons'
import api from '../api/client'
import { useAuthStore } from '../stores/auth'

export default function LoginPage() {
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const setTokens = useAuthStore((s) => s.setTokens)

  const onFinish = async (values: { email: string; password: string }) => {
    setLoading(true)
    try {
      const { data } = await api.post('/auth/login', values)
      setTokens(data.access_token, data.refresh_token)
      message.success('登录成功')
      navigate('/optimizer')
    } catch {
      message.error('邮箱或密码错误')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', background: '#f0f2f5' }}>
      <Card style={{ width: 400 }} title={<div style={{ textAlign: 'center', fontSize: 20 }}>抖音标题优化器</div>}>
        <Form onFinish={onFinish} layout="vertical">
          <Form.Item name="email" rules={[{ required: true, type: 'email', message: '请输入有效邮箱' }]}>
            <Input prefix={<MailOutlined />} placeholder="邮箱" size="large" />
          </Form.Item>
          <Form.Item name="password" rules={[{ required: true, message: '请输入密码' }]}>
            <Input.Password prefix={<LockOutlined />} placeholder="密码" size="large" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block size="large" loading={loading}>登录</Button>
          </Form.Item>
        </Form>
        <div style={{ textAlign: 'center' }}>
          没有账号？<Link to="/register">立即注册</Link>
        </div>
      </Card>
    </div>
  )
}
