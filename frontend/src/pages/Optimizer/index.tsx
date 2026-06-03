import { useState, useEffect } from 'react'
import { Tabs, Input, Select, Button, Card, Tag, Typography, Space, Collapse, message, Tooltip, Empty, Spin } from 'antd'
import { ThunderboltOutlined, SendOutlined, BulbOutlined, RiseOutlined, FireOutlined } from '@ant-design/icons'
import api from '../../api/client'

const { TextArea } = Input
const { Title, Text } = Typography

const ICON_MAP: Record<string, string> = {
  gamepad: '🎮', home: '🏠', compass: '✈️', heart: '💕',
  fire: '🍳', laptop: '📱', briefcase: '💼', experiment: '💄',
  dashboard: '💪', book: '📚',
}

const REASON_LABELS: Record<string, string> = {
  hook_enhancement: '钩子增强', emotional: '情绪放大',
  keyword: '关键词优化', formatting: '格式润色',
  emotional_amplification: '情绪放大', keyword_optimization: '关键词优化',
  formatting_polish: '格式润色', hook: '钩子',
}

const HOOK_TYPE_LABELS: Record<string, string> = {
  question: '疑问式', number_list: '数字列表式', controversy: '争议式',
  emotional_story: '情感故事式', cognitive_gap: '认知缺口式',
  general: '通用',
}

const STRATEGIES = [
  { value: 'auto', label: '自动选择' },
  { value: 'hook_enhancement', label: '钩子增强' },
  { value: 'emotional_amplification', label: '情绪放大' },
  { value: 'keyword_optimization', label: '关键词优化' },
  { value: 'formatting_polish', label: '格式润色' },
]

export default function OptimizerPage() {
  const [activeTab, setActiveTab] = useState('single')
  const [title, setTitle] = useState('')
  const [batchTitles, setBatchTitles] = useState('')
  const [category, setCategory] = useState('')
  const [categoryHints, setCategoryHints] = useState<any>(null)
  const [categories, setCategories] = useState<any[]>([])
  const [categoriesRaw, setCategoriesRaw] = useState<any[]>([])
  const [strategy, setStrategy] = useState('auto')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [scoreResult, setScoreResult] = useState<any>(null)
  const [keywordResult, setKeywordResult] = useState<any>(null)
  const [batchTaskId, setBatchTaskId] = useState('')
  const [seeds, setSeeds] = useState<any[]>([])
  const [seedsLoading, setSeedsLoading] = useState(false)

  useEffect(() => {
    api.get('/categories').then(({ data }) => {
      setCategoriesRaw(data)
      const opts = [{ value: '', label: '不选择分类' }]
      data.forEach((c: any) => {
        const icon = ICON_MAP[c.icon] || '📌'
        const seedInfo = c.seed_count > 0 ? ` [${c.seed_count}条参考]` : ''
        opts.push({ value: c.id, label: `${icon} ${c.name}${seedInfo}`, seedCount: c.seed_count, seedPreview: c.seed_preview })
      })
      setCategories(opts)
    }).catch(() => {
      setCategories([{ value: '', label: '不选择分类' }])
    })
  }, [])

  const fetchSeeds = async (catId: string) => {
    if (!catId) {
      setSeeds([])
      return
    }
    setSeedsLoading(true)
    try {
      const { data } = await api.get(`/seeds?category=${encodeURIComponent(catId)}`)
      setSeeds(data)
    } catch {
      setSeeds([])
    } finally {
      setSeedsLoading(false)
    }
  }

  const handleCategoryChange = async (val: string) => {
    setCategory(val)
    setCategoryHints(null)
    if (val) {
      try {
        const { data } = await api.get(`/categories/${val}/hints`)
        setCategoryHints(data)
      } catch { /* ignore */ }
      fetchSeeds(val)
    } else {
      setSeeds([])
    }
  }

  const handleOptimize = async () => {
    if (!title.trim()) return
    setLoading(true)
    setResult(null)
    try {
      const { data } = await api.post('/optimize', { title: title.trim(), strategy, category: category || undefined })
      setResult(data)
    } catch (err: any) {
      setResult({ error: err.response?.data?.detail || '优化失败' })
    } finally {
      setLoading(false)
    }
  }

  const handleScore = async () => {
    if (!title.trim()) return
    try {
      const { data } = await api.post('/optimize/score', { title: title.trim() })
      setScoreResult(data)
    } catch { /* ignore */ }
  }

  const handleKeywords = async () => {
    if (!title.trim()) return
    try {
      const { data } = await api.post('/optimize/keywords', { title: title.trim() })
      setKeywordResult(data)
    } catch { /* ignore */ }
  }

  const handleBatchOptimize = async () => {
    const titles = batchTitles.split('\n').filter((t: string) => t.trim())
    if (!titles.length) return
    setLoading(true)
    try {
      const { data } = await api.post('/optimize/batch', { titles, strategy, category: category || undefined })
      setBatchTaskId(data.task_id)
      message.success(`批量任务已提交 (ID: ${data.task_id})`)
    } catch (err: any) {
      message.error(err.response?.data?.detail || '提交失败')
    }
    setLoading(false)
  }

  const renderChangeReasons = (v: any) => {
    if (!v.change_reasons?.length) return null
    return (
      <Collapse size="small" ghost items={[{
        key: 'reasons',
        label: <Text type="secondary">查看修改理由 ({v.change_reasons.length}条)</Text>,
        children: v.change_reasons.map((r: any, j: number) => (
          <div key={j} style={{ marginBottom: 10, padding: 8, background: '#fafafa', borderRadius: 6 }}>
            <Tag color="blue">{REASON_LABELS[r.category] || r.category}</Tag>
            <div style={{ margin: '4px 0' }}>
              <Text delete type="secondary">"{r.comparison?.before}"</Text>
              {' → '}
              <Text strong>"{r.comparison?.after}"</Text>
            </div>
            <Text>{r.reason}</Text>
            <br /><Text type="success">📈 {r.expected_effect}</Text>
          </div>
        )),
      }]} />
    )
  }

  const renderSeedsPanel = () => {
    if (!category) return null

    if (seedsLoading) {
      return (
        <Card size="small" title={<span><FireOutlined /> 爆款参考</span>} style={{ marginTop: 16 }}>
          <div style={{ textAlign: 'center', padding: 20 }}><Spin /> 加载中...</div>
        </Card>
      )
    }

    if (!seeds.length) {
      return (
        <Card size="small" title={<span><FireOutlined /> 爆款参考</span>} style={{ marginTop: 16 }}>
          <Empty description="该分类暂无种子标题" image={Empty.PRESENTED_IMAGE_SIMPLE}>
            <Text type="secondary">种子生成中，请稍后再试或点击刷新</Text>
          </Empty>
        </Card>
      )
    }

    return (
      <Card size="small" title={<span><FireOutlined /> 爆款参考 ({seeds.length}条)</span>} style={{ marginTop: 16 }}>
        <div style={{ maxHeight: 400, overflowY: 'auto' }}>
          {seeds.map((s: any, i: number) => (
            <div key={s.id || i} style={{
              padding: '8px 0',
              borderBottom: i < seeds.length - 1 ? '1px solid #f0f0f0' : 'none',
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 4 }}>
                <Text style={{ flex: 1, marginRight: 8 }}>{s.title}</Text>
                <Tag color="blue" style={{ flexShrink: 0 }}>{s.score}</Tag>
              </div>
              <Tag color="purple">{HOOK_TYPE_LABELS[s.hook_type] || s.hook_type}</Tag>
            </div>
          ))}
        </div>
      </Card>
    )
  }

  const renderCategoryOption = (opt: any) => {
    if (!opt.value || !opt.seedPreview?.length) return null
    return (
      <Tooltip
        title={
          <div>
            <div style={{ fontWeight: 'bold', marginBottom: 4 }}>Top 参考标题:</div>
            {opt.seedPreview.map((t: string, i: number) => (
              <div key={i} style={{ fontSize: 12, marginBottom: 2 }}>{i + 1}. {t}</div>
            ))}
          </div>
        }
        placement="right"
      >
        <span>{opt.label}</span>
      </Tooltip>
    )
  }

  const selectOptions = categories.map((opt: any) => ({
    ...opt,
    label: opt.value && opt.seedPreview?.length ? (
      <Tooltip
        key={opt.value}
        title={
          <div>
            <div style={{ fontWeight: 'bold', marginBottom: 4 }}>Top 参考标题:</div>
            {opt.seedPreview.map((t: string, i: number) => (
              <div key={i} style={{ fontSize: 12, marginBottom: 2 }}>{i + 1}. {t}</div>
            ))}
          </div>
        }
        placement="right"
      >
        <span>{opt.label}</span>
      </Tooltip>
    ) : opt.label,
  }))

  return (
    <div style={{ maxWidth: 900, margin: '0 auto' }}>
      <Title level={3}><ThunderboltOutlined /> 标题优化</Title>

      <Tabs activeKey={activeTab} onChange={setActiveTab} items={[
        {
          key: 'single',
          label: '单条优化',
          children: (
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              <Card size="small" title="输入设置">
                <Space wrap>
                  <Select value={category} onChange={handleCategoryChange} options={selectOptions} style={{ width: 200 }} placeholder="选择分类" />
                  <Select value={strategy} onChange={setStrategy} options={STRATEGIES} style={{ width: 140 }} />
                </Space>
              </Card>

              {categoryHints && (
                <Card size="small" type="inner">
                  <Text strong>{categoryHints.name} 领域关键词：</Text>
                  <div style={{ marginTop: 4 }}>
                    {categoryHints.context_keywords?.map((k: string) => <Tag key={k}>{k}</Tag>)}
                  </div>
                </Card>
              )}

              <TextArea value={title} onChange={(e) => setTitle(e.target.value)} rows={3} placeholder="输入你的抖音标题..." maxLength={200} showCount />
              <Space>
                <Button type="primary" icon={<SendOutlined />} onClick={handleOptimize} loading={loading}>优化标题</Button>
                <Button icon={<RiseOutlined />} onClick={handleScore}>评分</Button>
                <Button icon={<BulbOutlined />} onClick={handleKeywords}>关键词分析</Button>
              </Space>

              {result && !result.error && (
                <Card title={`优化结果（原标题评分: ${result.original_score}）`}>
                  {result.warnings?.map((w: string, i: number) => (
                    <Tag color="orange" key={i} style={{ marginBottom: 8 }}>{w}</Tag>
                  ))}
                  {result.seeds_used?.length > 0 && (
                    <Text type="secondary" style={{ display: 'block', marginBottom: 12 }}>
                      参考种子: {result.seeds_used.length} 条
                    </Text>
                  )}
                  {result.variations?.map((v: any, i: number) => (
                    <Card key={i} size="small" style={{ marginBottom: 12 }} type="inner"
                      title={<Space><Text strong>{v.title}</Text><Tag color="blue">评分 {v.score_computed}</Tag><Tag color="green">+{v.score_delta}</Tag></Space>}>
                      {renderChangeReasons(v)}
                    </Card>
                  ))}
                </Card>
              )}

              {result?.error && <Card><Text type="danger">{result.error}</Text></Card>}

              {scoreResult && (
                <Card title="评分详情" size="small">
                  <Title level={4}>综合评分: {scoreResult.overall_score}</Title>
                  <Collapse size="small" items={Object.entries(scoreResult.explanations || {}).map(([dim, exp]: [string, any]) => ({
                    key: dim,
                    label: <Space><Text strong>{dim}</Text><Tag color={exp.score >= 70 ? 'green' : exp.score >= 50 ? 'orange' : 'red'}>{exp.score}</Tag></Space>,
                    children: (
                      <div>
                        <Text>🔍 诊断: {exp.diagnosis}</Text><br />
                        <Text type="warning">💡 改进: {exp.improvement}</Text><br />
                        <Text type="success">📈 效果: {exp.expected_effect}</Text>
                      </div>
                    ),
                  }))} />
                </Card>
              )}

              {keywordResult && (
                <Card title="关键词分析" size="small">
                  <div style={{ marginBottom: 12 }}>
                    <Text strong>关键词: </Text>
                    {keywordResult.keywords?.map((k: any) => <Tag key={k.keyword}>{k.keyword} ({k.weight})</Tag>)}
                  </div>
                  {keywordResult.matched_topics?.length > 0 && (
                    <div>
                      <Text strong>匹配热门话题: </Text>
                      {keywordResult.matched_topics?.map((t: any) =>
                        <Tag key={t.topic} color="red">{t.topic} {t.hashtags?.join(' ')}</Tag>
                      )}
                    </div>
                  )}
                </Card>
              )}

              {renderSeedsPanel()}
            </Space>
          ),
        },
        {
          key: 'batch',
          label: '批量优化',
          children: (
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              <Card size="small" title="批量设置">
                <Space wrap>
                  <Select value={category} onChange={handleCategoryChange} options={selectOptions} style={{ width: 200 }} placeholder="选择分类（所有标题共享）" />
                  <Select value={strategy} onChange={setStrategy} options={STRATEGIES} style={{ width: 140 }} />
                </Space>
              </Card>
              <TextArea value={batchTitles} onChange={(e) => setBatchTitles(e.target.value)} rows={8} placeholder="每行一个标题，最多50条..." />
              <Button type="primary" onClick={handleBatchOptimize} loading={loading}>提交批量优化</Button>
              {batchTaskId && (
                <Card size="small">
                  <Text>任务ID: {batchTaskId}</Text>
                  <br /><Text type="secondary">任务已提交，可在历史记录中查看结果</Text>
                </Card>
              )}
              {renderSeedsPanel()}
            </Space>
          ),
        },
      ]} />
    </div>
  )
}
