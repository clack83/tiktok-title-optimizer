import { useEffect, useState } from 'react'
import { Table, Button, DatePicker, Space, Tag, Typography, Popconfirm, message, Modal } from 'antd'
import { DeleteOutlined, SwapOutlined, HistoryOutlined } from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import dayjs from 'dayjs'
import api from '../../api/client'

const { Title } = Typography
const { RangePicker } = DatePicker

interface HistoryItem {
  id: string
  original_title: string
  scores: { original_score: number }
  strategy: string
  category: string | null
  created_at: string
}

export default function HistoryPage() {
  const [data, setData] = useState<HistoryItem[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)
  const [dateRange, setDateRange] = useState<[string, string] | null>(null)
  const [compareOpen, setCompareOpen] = useState(false)
  const [selected, setSelected] = useState<string[]>([])
  const [compareResult, setCompareResult] = useState<any>(null)

  const fetchData = async () => {
    setLoading(true)
    try {
      const params: any = { page, page_size: 20 }
      if (dateRange) {
        params.start_date = dateRange[0]
        params.end_date = dateRange[1]
      }
      const { data: res } = await api.get('/history', { params })
      setData(res.items)
      setTotal(res.total)
    } catch { /* ignore */ }
    setLoading(false)
  }

  useEffect(() => {
    fetchData()
  }, [page, dateRange])

  const handleDelete = async (id: string) => {
    await api.delete(`/history/${id}`)
    message.success('已删除')
    fetchData()
  }

  const handleCompare = async () => {
    if (selected.length !== 2) return
    try {
      const { data } = await api.post('/history/compare', { record_id_1: selected[0], record_id_2: selected[1] })
      setCompareResult(data)
      setCompareOpen(true)
    } catch { /* ignore */ }
  }

  const columns: ColumnsType<HistoryItem> = [
    { title: '原标题', dataIndex: 'original_title', ellipsis: true, width: 300 },
    { title: '评分', dataIndex: ['scores', 'original_score'], width: 80 },
    { title: '策略', dataIndex: 'strategy', width: 100, render: (s: string) => <Tag>{s}</Tag> },
    { title: '分类', dataIndex: 'category', width: 80, render: (c: string) => c ? <Tag color="blue">{c}</Tag> : '-' },
    { title: '时间', dataIndex: 'created_at', width: 160, render: (t: string) => dayjs(t).format('YYYY-MM-DD HH:mm') },
    {
      title: '操作', key: 'actions', width: 120,
      render: (_, record) => (
        <Popconfirm title="确认删除？" onConfirm={() => handleDelete(record.id)}>
          <Button size="small" danger icon={<DeleteOutlined />} />
        </Popconfirm>
      ),
    },
  ]

  return (
    <div>
      <Title level={3}><HistoryOutlined /> 优化历史</Title>

      <Space style={{ marginBottom: 16 }}>
        <RangePicker
          onChange={(dates) => {
            if (dates && dates[0] && dates[1]) {
              setDateRange([dates[0].format('YYYY-MM-DD'), dates[1].format('YYYY-MM-DD')])
            } else {
              setDateRange(null)
            }
          }}
        />
        <Button icon={<SwapOutlined />} disabled={selected.length !== 2} onClick={handleCompare}>对比选中</Button>
      </Space>

      <Table
        rowKey="id"
        columns={columns}
        dataSource={data}
        loading={loading}
        rowSelection={{ type: 'checkbox', onChange: (keys) => setSelected(keys as string[]), selectedRowKeys: selected }}
        pagination={{ current: page, total, pageSize: 20, onChange: setPage }}
      />

      <Modal title="对比结果" open={compareOpen} onCancel={() => setCompareOpen(false)} footer={null} width={800}>
        {compareResult && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
            <div>
              <Title level={5}>记录 1</Title>
              <p><strong>原标题:</strong> {compareResult.record_1.original_title}</p>
              <p><strong>评分:</strong> {compareResult.record_1.overall_score}</p>
              <p><strong>策略:</strong> {compareResult.record_1.strategy}</p>
            </div>
            <div>
              <Title level={5}>记录 2</Title>
              <p><strong>原标题:</strong> {compareResult.record_2.original_title}</p>
              <p><strong>评分:</strong> {compareResult.record_2.overall_score}</p>
              <p><strong>策略:</strong> {compareResult.record_2.strategy}</p>
            </div>
          </div>
        )}
      </Modal>
    </div>
  )
}
