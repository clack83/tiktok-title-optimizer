import { useEffect, useState } from 'react'
import { Card, Row, Col, Statistic, Typography, Spin } from 'antd'
import { RiseOutlined, ThunderboltOutlined, StarOutlined, DashboardOutlined } from '@ant-design/icons'
import ReactEChartsCore from 'echarts-for-react/lib/core'
import * as echarts from 'echarts/core'
import { LineChart, BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, TitleComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import api from '../../api/client'

echarts.use([LineChart, BarChart, GridComponent, TooltipComponent, TitleComponent, LegendComponent, CanvasRenderer])

const { Title } = Typography

export default function DashboardPage() {
  const [overview, setOverview] = useState<any>(null)
  const [trends, setTrends] = useState<any>(null)
  const [keywords, setKeywords] = useState<any>(null)
  const [distribution, setDistribution] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      try {
        const [ov, tr, kw, dist] = await Promise.all([
          api.get('/dashboard/overview'),
          api.get('/dashboard/trends'),
          api.get('/dashboard/keywords-cloud'),
          api.get('/dashboard/score-distribution'),
        ])
        setOverview(ov.data)
        setTrends(tr.data)
        setKeywords(kw.data)
        setDistribution(dist.data)
      } catch { /* ignore */ }
      setLoading(false)
    }
    load()
  }, [])

  if (loading) return <Spin size="large" style={{ display: 'block', margin: '100px auto' }} />

  const trendOption = {
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: trends?.trend?.map((t: any) => t.date) || [] },
    yAxis: { type: 'value', name: '平均评分' },
    series: [
      { name: '平均评分', type: 'line', data: trends?.trend?.map((t: any) => t.avg_score) || [], smooth: true },
    ],
  }

  const distOption = {
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: distribution?.distribution?.map((d: any) => d.range) || [] },
    yAxis: { type: 'value', name: '数量' },
    series: [
      { name: '标题数量', type: 'bar', data: distribution?.distribution?.map((d: any) => d.count) || [] },
    ],
  }

  return (
    <div>
      <Title level={3}><DashboardOutlined /> 数据看板</Title>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card><Statistic title="总优化次数" value={overview?.total_optimizations || 0} prefix={<ThunderboltOutlined />} /></Card>
        </Col>
        <Col span={6}>
          <Card><Statistic title="平均评分提升" value={overview?.avg_score_improvement || 0} suffix="分" prefix={<RiseOutlined />} /></Card>
        </Col>
        <Col span={12}>
          <Card title="常用策略">
            {overview?.top_strategies?.map(([s, c]: [string, number]) => (
              <span key={s} style={{ marginRight: 16 }}><strong>{s}</strong>: {c}次</span>
            ))}
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={12}>
          <Card title="评分趋势（近30天）">
            <ReactEChartsCore echarts={echarts} option={trendOption} style={{ height: 300 }} />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="评分分布">
            <ReactEChartsCore echarts={echarts} option={distOption} style={{ height: 300 }} />
          </Card>
        </Col>
      </Row>

      <Card title="关键词云">
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
          {keywords?.keywords?.slice(0, 30).map((kw: any) => (
            <span key={kw.word} style={{
              fontSize: Math.max(12, Math.min(36, kw.count * 3)),
              color: `hsl(${Math.random() * 360}, 70%, 50%)`,
              padding: '2px 6px',
            }}>
              {kw.word}({kw.count})
            </span>
          ))}
        </div>
      </Card>
    </div>
  )
}
