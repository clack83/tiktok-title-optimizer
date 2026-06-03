# 🎬 TikTok（抖音）标题优化器

> AI 驱动的抖音视频标题优化工具，输入你的标题，一键生成多个优化版本，附带详细修改理由和评分，帮你提升视频点击率和播放量。

## 📖 目录

- [这是什么？](#这是什么)
- [功能特性](#功能特性)
- [支持的领域分类](#支持的领域分类)
- [小白快速上手（Docker 一键部署）](#小白快速上手docker-一键部署)
- [开发环境部署](#开发环境部署)
- [如何获取 DeepSeek API Key](#如何获取-deepseek-api-key)
- [项目结构](#项目结构)
- [API 接口说明](#api-接口说明)
- [常见问题](#常见问题)
- [技术栈](#技术栈)

---

## 这是什么？

一个帮你**优化抖音标题**的 AI 工具。你输入一个标题，AI 会：

1. **分析你原标题的分数**（从吸引力、信息量、可读性、平台适配四个维度打分）
2. **生成 3-5 个优化版本**，每个版本都有具体评分和提升幅度
3. **告诉你改了什么、为什么改、改了有什么效果**（增加信任感）
4. **提供同领域的爆款标题参考**（帮你找灵感）

### 举个例子

> **你输入：** "分享一个护肤小知识"
>
> **AI 输出：**
> - "后悔没早知道的3个护肤神技巧！第2个太实用了 💡 #护肤干货 #变美小技巧"
>   - 评分：88（+23）✨
>   - 修改理由：增加了后悔体和数字列表，制造认知缺口，预期提升点击率约25%

---

## 功能特性

- ✅ **AI 标题优化** — 基于 DeepSeek 大模型，支持 4 种优化策略（钩子增强、情绪放大、关键词优化、格式润色）
- ✅ **多维度评分** — 从吸引力(40%)、信息量(25%)、可读性(20%)、平台适配(15%)四个维度打分
- ✅ **详细修改理由** — 每条优化建议都告诉你：改了哪里、为什么改、预期效果是什么
- ✅ **10 个垂直领域** — 游戏、生活、旅行、婚恋、美食、科技、职场、美妆、健身、教育
- ✅ **爆款标题参考库** — 每个分类都有 AI 自动生成的高质量参考标题，优化时作为参考
- ✅ **关键词分析** — 提取标题中的关键词，匹配热门话题标签
- ✅ **批量优化** — 一次提交最多 50 条标题，后台异步处理
- ✅ **优化历史** — 保存你的所有优化记录，支持查看和对比
- ✅ **数据看板** — 可视化展示优化趋势、评分分布、高频关键词
- ✅ **用户系统** — 注册登录，每人独立保存数据和偏好

---

## 支持的领域分类

| 分类 | 图标 | 目标受众 | 典型钩子 |
|------|------|----------|----------|
| 🎮 游戏 | gamepad | 18-30岁男性 | "学会这招直接上分" |
| 🏠 生活 | home | 25-45岁女性 | "用了10年的方法竟然是错的" |
| ✈️ 旅行 | compass | 20-40岁 | "人均800玩转XX城市" |
| 💕 婚恋 | heart | 20-35岁 | "TA这样对你说明..." |
| 🍳 美食 | fire | 20-45岁女性 | "学会这道菜家人夸你" |
| 📱 科技 | laptop | 20-40岁男性 | "90%的人不知道的隐藏功能" |
| 💼 职场 | briefcase | 22-35岁 | "领导不会告诉你的晋升秘诀" |
| 💄 美妆 | experiment | 18-35岁女性 | "素颜出门被问用什么粉底" |
| 💪 健身 | dashboard | 18-35岁 | "坚持30天变化惊到我了" |
| 📚 教育 | book | 18-40岁 | "5分钟掌握一个知识点" |

---

## 小白快速上手（Docker 一键部署）

> 💡 **这是最简单的方式，不需要安装 Python 或 Node.js，只要你的电脑能运行 Docker。**

### 第1步：安装 Docker

如果你是 Windows 或 Mac 用户，直接下载 Docker Desktop：

- [Docker Desktop 下载地址](https://www.docker.com/products/docker-desktop/)

下载后双击安装，一路点"下一步"就行。安装完成后打开 Docker Desktop，等它启动完毕（任务栏出现 Docker 图标且显示 "Engine running"）。

### 第2步：获取 DeepSeek API Key

> ⚠️ **这是最关键的一步！没有 API Key 就无法使用 AI 优化功能。**

1. 打开 [platform.deepseek.com](https://platform.deepseek.com/) 注册账号
2. 注册后进入「API Keys」页面，点击「创建 API Key」
3. 复制生成的 key（格式类似 `sk-xxxxxxxxxxxxxxxx`）
4. **充值**：需要充值才能调用 API，充值 10 元就够用很久（优化一次标题大约花费几分钱）

### 第3步：配置 .env 文件

1. 在项目目录下，复制 `.env.example` 文件并重命名为 `.env`：
   - Windows：右键 `.env.example` → 复制 → 粘贴 → 改名为 `.env`
   - Mac：`cp .env.example .env`

2. 用记事本（Windows）或文本编辑（Mac）打开 `.env` 文件，完整的配置内容如下：

```bash
# ========== 数据库配置 ==========
# 以下保持默认值即可，Docker 会自动创建对应的数据库和用户
POSTGRES_USER=tiktok_optimizer
POSTGRES_PASSWORD=tiktok_optimizer
POSTGRES_DB=tiktok_optimizer
DATABASE_URL=postgresql://tiktok_optimizer:tiktok_optimizer@postgres:5432/tiktok_optimizer

# ========== Redis 配置 ==========
# 保持默认值，不需要修改
REDIS_URL=redis://redis:6379/0

# ========== JWT 密钥配置 ==========
# ⚠️ 强烈建议修改！随便打一串乱码，越长越安全
# 这个密钥用于加密用户的登录凭证，泄露后别人可以伪造登录
SECRET_KEY=change-me-to-a-random-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60       # 登录有效时间（分钟），60=1小时后需重新登录
REFRESH_TOKEN_EXPIRE_DAYS=30         # 登录刷新有效期（天），30天内可以自动续登录

# ========== DeepSeek API 配置 ==========
# ⚠️ 必须修改！去 platform.deepseek.com 注册充值后获取
# 不填这一项的话，AI 优化功能无法使用
DEEPSEEK_API_KEY=your-deepseek-api-key    # ← 把这里改成你的真实 Key
DEEPSEEK_BASE_URL=https://api.deepseek.com   # API 地址，不需要改
DEEPSEEK_MODEL=deepseek-chat               # 使用的模型，不需要改

# ========== 应用配置 ==========
# 保持默认值
APP_ENV=development   # 环境：development=开发模式，production=生产模式
DEBUG=true            # 调试开关，开发时保持 true
```

> 📝 **对于小白用户：你只需要改两行——**
> 1. `DEEPSEEK_API_KEY=你的key`（必改）
> 2. `SECRET_KEY=随便打一串乱码`（建议改）

### 第4步：启动项目

打开终端（Windows 按 `Win+R`，输入 `cmd`，回车），进入项目目录，输入：

```bash
docker compose up -d
```

第一次运行会自动下载镜像和依赖，大约需要 5-10 分钟。看到 `✔ Container ... Started` 就说明启动成功了。

### 第5步：打开网页

打开浏览器，访问：

```
http://localhost:5173
```

1. 先点「注册」创建账号
2. 注册后登录，进入「标题优化」页面
3. 输入标题 → 选择分类 → 点击「优化标题」
4. 等待几秒钟，就能看到优化结果了！

### 第6步：停止项目

当你想关闭项目时，在终端按 `Ctrl+C`，或者输入：

```bash
docker compose down
```

---

## 开发环境部署

> 💡 如果你有编程经验，也可以直接在本机运行，不需要 Docker。

### 环境要求

| 工具 | 版本要求 |
|------|---------|
| Python | >= 3.11 |
| Node.js | >= 18 |
| PostgreSQL | >= 14 |
| Redis | >= 6 |

### 1. 克隆项目

```bash
git clone https://github.com/clack83/tiktok-title-optimizer.git
cd tiktok-title-optimizer
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件。完整配置如下，**本地开发只需要改一个地方** —— 把 `DATABASE_URL` 里的 `postgres` 改成 `localhost`：

```bash
# ========== 数据库配置 ==========
POSTGRES_USER=tiktok_optimizer
POSTGRES_PASSWORD=tiktok_optimizer
POSTGRES_DB=tiktok_optimizer
# ⚠️ 注意：本地运行时要把 postgres 改成 localhost
DATABASE_URL=postgresql://tiktok_optimizer:tiktok_optimizer@localhost:5432/tiktok_optimizer

# ========== Redis 配置 ==========
# 本地运行时把 redis 改成 localhost
REDIS_URL=redis://localhost:6379/0

# ========== JWT 密钥配置 ==========
# ⚠️ 建议修改！随便打一串乱码
SECRET_KEY=change-me-to-a-random-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60       # 登录有效时间（分钟）
REFRESH_TOKEN_EXPIRE_DAYS=30         # 登录刷新有效期（天）

# ========== DeepSeek API 配置 ==========
# ⚠️ 必须改成你的真实 Key！去 platform.deepseek.com 申请
DEEPSEEK_API_KEY=your-deepseek-api-key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat

# ========== 应用配置 ==========
APP_ENV=development
DEBUG=true
```

> 📝 **本地开发 vs Docker 部署的区别：**
> - Docker：`DATABASE_URL` 里写 `postgres`，`REDIS_URL` 里写 `redis`
> - 本地：`DATABASE_URL` 里写 `localhost`，`REDIS_URL` 里写 `localhost`

### 3. 启动后端

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 启动数据库迁移（创建表）
alembic upgrade head

# 启动后端服务
uvicorn main:app --reload
```

后端启动后访问 http://localhost:8000/health 能看到 `{"status": "ok"}` 就对了。

### 4. 启动前端

```bash
# 新开一个终端，进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端启动后访问 http://localhost:5173 就能看到页面了。

### 5. 启动 Celery（可选，批量优化需要）

```bash
# 新开终端
cd backend
celery -A app.tasks.celery_app worker --loglevel=info
```

### 快捷命令（Makefile）

项目提供了 Makefile 简化开发流程：

```bash
make dev          # 启动所有 Docker 服务
make dev-down     # 停止所有服务
make dev-logs     # 查看日志
make test         # 运行测试
make lint         # 代码检查
make migrate      # 运行数据库迁移
make clean        # 清理所有容器和数据
```

---

## 如何获取 DeepSeek API Key

> ⚠️ **这是整个项目唯一需要花钱的地方，但非常便宜。**

1. **注册账号**
   - 打开 [platform.deepseek.com](https://platform.deepseek.com/)
   - 点击右上角「注册」，用手机号或邮箱注册

2. **充值（必做）**
   - 登录后进入「费用中心」
   - 点击「充值」，最低充值 10 元
   - **为什么需要充值？** DeepSeek 的 API 是付费的，但价格很低：
     - 优化一次标题大约 0.01-0.03 元
     - 10 元可以优化数百次标题
     - 生成一次种子库大约 0.2-0.5 元

3. **创建 API Key**
   - 进入「API Keys」页面
   - 点击「创建 API Key」
   - 复制生成的 key（格式：`sk-xxxxxxxxxxxxxxxxxxxxxxxx`）
   - ⚠️ **Key 只显示一次，请立即保存！**

4. **填入配置文件**
   - 打开项目中的 `.env` 文件
   - 找到 `DEEPSEEK_API_KEY=` 这一行
   - 在等号后面粘贴你的 key（不要加引号）
   - 例：`DEEPSEEK_API_KEY=sk-abc123def456`

---

## 项目结构

```
tiktok-title-optimizer/
├── backend/                     # 后端代码（Python + FastAPI）
│   ├── main.py                  # 应用入口，注册所有路由
│   ├── requirements.txt         # Python 依赖列表
│   ├── alembic/                 # 数据库迁移文件
│   │   └── env.py
│   ├── alembic.ini
│   └── app/
│       ├── api/v1/              # API 接口
│       │   ├── auth.py          # 注册/登录/刷新token
│       │   ├── optimize.py     # 标题优化/评分/关键词
│       │   ├── categories.py   # 分类列表/提示
│       │   ├── seeds.py        # 爆款种子标题库
│       │   ├── history.py      # 优化历史记录
│       │   ├── dashboard.py    # 数据看板
│       │   └── preferences.py  # 用户偏好设置
│       ├── core/                # 核心模块
│       │   ├── config.py       # 配置管理（读取 .env）
│       │   ├── database.py     # 数据库连接
│       │   ├── security.py     # JWT 认证/密码加密
│       │   └── redis_client.py # Redis 缓存
│       ├── models/              # 数据库模型
│       │   ├── user.py         # 用户表
│       │   ├── optimization.py # 优化记录表
│       │   ├── preference.py   # 用户偏好表
│       │   └── seed_title.py   # 种子标题表
│       ├── schemas/             # 请求/响应格式定义
│       │   ├── auth.py
│       │   ├── optimization.py
│       │   └── seed.py
│       └── tasks/               # 后台任务
│           └── celery_app.py   # Celery 配置和任务
│
├── algorithms/                  # 算法模块（AI 核心逻辑）
│   ├── categories.yaml          # 10个领域的分类配置
│   ├── nlp/
│   │   ├── category_loader.py   # 分类配置加载器（支持热更新）
│   │   ├── keyword_extractor.py # 关键词提取（jieba分词）
│   │   ├── topic_matcher.py     # 热门话题匹配
│   │   └── seed_generator.py    # 种子标题生成
│   ├── optimizer/
│   │   ├── deepseek_client.py   # DeepSeek API 客户端
│   │   ├── strategies.py        # 优化策略和 Prompt 模板
│   │   └── pipeline.py          # 优化流程编排
│   └── scoring/
│       ├── engine.py            # 评分引擎
│       └── rules.py             # 四维评分规则
│
├── frontend/                    # 前端代码（React + TypeScript）
│   ├── package.json             # 前端依赖
│   ├── vite.config.ts           # Vite 构建配置
│   └── src/
│       ├── main.tsx             # 入口文件
│       ├── App.tsx              # 路由配置
│       ├── api/
│       │   └── client.ts        # API 请求客户端（自动处理 token）
│       ├── stores/
│       │   └── auth.ts          # 登录状态管理
│       ├── components/
│       │   └── MainLayout.tsx   # 主布局（侧边栏 + 顶栏）
│       └── pages/
│           ├── Login.tsx        # 登录页
│           ├── Register.tsx     # 注册页
│           ├── Optimizer/       # 标题优化页（核心页面）
│           ├── History/         # 历史记录页
│           └── Dashboard/       # 数据看板页
│
├── tests/                       # 测试代码
│   ├── unit/                    # 单元测试
│   │   ├── test_scoring.py      # 评分引擎测试
│   │   ├── test_optimizer.py    # 优化器测试
│   │   ├── test_keywords.py     # 关键词提取测试
│   │   ├── test_categories.py   # 分类加载测试
│   │   ├── test_deepseek.py     # DeepSeek 客户端测试
│   │   └── test_seed_generator.py # 种子生成测试
│   └── integration/             # 集成测试
│       ├── test_auth_api.py     # 认证接口测试
│       ├── test_categories_api.py
│       └── test_seeds_api.py
│
├── docker-compose.yml           # Docker 编排（一键部署）
├── Dockerfile.backend           # 后端 Docker 镜像
├── Dockerfile.frontend          # 前端 Docker 镜像
├── Makefile                     # 开发快捷命令
├── .env.example                 # 环境变量模板（复制为 .env）
└── README.md                    # 你在看的就是这个文件 📖
```

---

## API 接口说明

所有接口前缀：`http://localhost:8000/api/v1`

### 认证相关

| 方法 | 路径 | 说明 | 需要登录 |
|------|------|------|---------|
| POST | `/auth/register` | 注册账号 | ❌ |
| POST | `/auth/login` | 登录获取 token | ❌ |
| POST | `/auth/refresh` | 刷新 token | ❌ |
| GET | `/auth/me` | 获取当前用户信息 | ✅ |

### 标题优化

| 方法 | 路径 | 说明 | 需要登录 |
|------|------|------|---------|
| POST | `/optimize` | 优化标题（核心接口） | ✅ |
| POST | `/optimize/score` | 给标题评分 | ✅ |
| POST | `/optimize/keywords` | 提取关键词 | ✅ |
| POST | `/optimize/batch` | 批量优化 | ✅ |
| GET | `/optimize/batch/{task_id}` | 查询批量任务状态 | ✅ |

### 分类和种子库

| 方法 | 路径 | 说明 | 需要登录 |
|------|------|------|---------|
| GET | `/categories` | 获取所有分类 | ❌ |
| GET | `/categories/{id}/hints` | 获取分类提示词 | ❌ |
| GET | `/seeds?category=游戏` | 获取种子标题 | ❌ |
| POST | `/seeds/refresh` | 刷新种子库 | ❌ |

### 优化请求示例

```bash
curl -X POST http://localhost:8000/api/v1/optimize \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <你的token>" \
  -d '{
    "title": "分享一个护肤小知识",
    "category": "美妆",
    "strategy": "auto",
    "count": 4
  }'
```

### 优化响应示例

```json
{
  "original_title": "分享一个护肤小知识",
  "original_score": 52,
  "strategy": "auto",
  "category": "美妆",
  "seeds_used": ["uuid-1", "uuid-2", "uuid-3"],
  "variations": [
    {
      "title": "后悔没早知道的3个护肤神技巧！第2个太实用了 💡",
      "score_computed": 88,
      "score_delta": 36,
      "change_reasons": [
        {
          "category": "hook_enhancement",
          "comparison": {
            "before": "分享一个护肤小知识",
            "after": "后悔没早知道的3个护肤神技巧"
          },
          "reason": "原标题缺乏紧迫感和价值感，改用后悔体+数量钩子制造认知缺口",
          "expected_effect": "提升点击率约25%，增加好奇心驱动的完播"
        }
      ]
    }
  ]
}
```

---

## 常见问题

### Q: 需要什么配置的电脑？

> 最低 4GB 内存，推荐 8GB+。项目本身不占用太多资源，AI 计算在云端（DeepSeek 服务器）。

### Q: 免费能用吗？

> 需要给 DeepSeek 充值才能调用 API。但费用很低：优化一次标题约 0.01-0.03 元，10 元能用很久。

### Q: 优化一次标题要多久？

> 通常 3-10 秒，取决于标题长度和 DeepSeek 服务器负载。

### Q: 种子标题是什么？需要手动添加吗？

> 种子标题是 AI 自动生成的高质量参考标题，每个分类 15-20 条。不需要手动添加，系统会每周自动刷新。优化时 AI 会参考这些爆款标题来生成更符合领域特点的版本。

### Q: 为什么要选择分类？不选可以吗？

> 不选也可以。但选了分类后，AI 会针对该领域的受众偏好来优化，效果更好。比如"游戏"分类会用更多挑战性和成就感的话术。

### Q: 四种策略有什么区别？

> - **钩子增强**：专注前8个字的冲击力，制造悬念和好奇
> - **情绪放大**：加强情绪词汇，让人产生共鸣和代入感
> - **关键词优化**：优化关键词位置和密度，提高搜索匹配
> - **格式润色**：优化标点、断句、emoji 和标签
> - **自动选择**：AI 自动判断原标题弱点，选择最佳策略

### Q: 数据安全吗？我的标题会不会被泄露？

> 所有数据存储在你自己的数据库里。AI 调用 DeepSeek 时只发送标题文本和优化指令，不会发送你的个人信息。

### Q: Docker 启动失败怎么办？

> 1. 确保 Docker Desktop 正在运行（任务栏有 Docker 图标）
> 2. 检查 5432（PostgreSQL）、6379（Redis）、8000（后端）、5173（前端）端口是否被占用
> 3. 确保 `.env` 文件已创建且配置正确

### Q: 如何查看后端日志？

```bash
docker compose logs backend -f
```

---

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 后端框架 | FastAPI | 高性能异步 Python Web 框架 |
| 前端框架 | React 18 + TypeScript | 现代前端开发 |
| UI 组件 | Ant Design 5 | 企业级 UI 组件库 |
| 图表 | ECharts | 数据可视化（看板页） |
| 数据库 | PostgreSQL 16 | 主数据存储 |
| 缓存 | Redis 7 | 优化结果缓存、Celery 队列 |
| 任务队列 | Celery | 批量优化异步处理 |
| AI 模型 | DeepSeek-Chat | 标题生成和优化 |
| NLP | jieba + scikit-learn | 中文分词、TF-IDF、关键词提取 |
| 部署 | Docker + Docker Compose | 一键部署 |

---

## 许可证

MIT License

---

**Made with ❤️ for content creators**
