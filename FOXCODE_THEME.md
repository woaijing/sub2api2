# sub2api2 的 FoxCode 主题与模型广场移植

完成日期：2026-09-18。

以 `sub2api2` 当前检出的 `871e89c7b`（源码版本 `0.1.326`）为业务底座，从 `sub2apistyle` 的 `e6fe6df` 移植 FoxCode 主题和卡片式模型广场。本次没有升级上游版本，也没有修改后端、数据库迁移、API 定义、路由、状态仓库、依赖锁文件或部署配置。

## 页面变化

- 全局采用陶土橙 `#D97757`、米白底色 `#FAF9F5`，配套暖棕深色模式。主按钮使用同色系的深橙以提高白字对比度。
- 公共按钮、输入框、下拉框、卡片、表格、弹窗、顶栏、侧栏、登录页和首页接入统一主题变量。
- 图表首系列采用品牌色，其他系列保留区分色；趋势图和管理仪表盘的文字、网格颜色随主题切换更新。
- 模型广场采用按模型聚合的卡片布局，桌面三列、平板两列、手机一列，支持模型搜索、分类、分组和倍率筛选。
- 卡片展示基础价格和价格区间，展开显示可用分组及生效倍率；价格详情保留原有实付价格、官方参考价、上下文档位、分时及高峰规则。
- 保留匿名与登录状态、后台 `?embedded=1` 入口，以及后台配置的 Markdown 计费说明和 HTML 清理。

网站名称、Logo 和副标题仍由原有后台品牌设置控制，代码没有固定成 FoxCode。模型和价格仍来自 `/api/v1/model-plaza`，页面没有写死线上价格。

## 保留的 sub2api2 行为

侧栏和顶栏仅合并样式，保留无限画布、访问白名单、充值中心及原有功能开关。密钥多分组智能路由、充值/支付配置、EPUSDT、Codex 配额检测设置、余额结算和渠道监控沿用本分支实现。

管理仪表盘的加载失败与重试逻辑保留；用户仪表盘仍显示本分支的“近 30 天”统计口径。设置页只调整标签页装饰线的颜色。没有带入另一个分支的订阅开关、站点计费模式、OpenCode 平台或批量业务操作。

## 维护入口

| 内容 | 文件 |
| --- | --- |
| 浅深色主题变量 | `frontend/src/styles/foxcode-tokens.css` |
| 品牌色阶、语义颜色与阴影 | `frontend/tailwind.config.js` |
| 公共控件与布局样式 | `frontend/src/style.css`、`frontend/src/components/layout/` |
| 图表配色和主题响应 | `frontend/src/utils/chartColors.ts`、`frontend/src/composables/useChartTheme.ts` |
| 模型广场筛选和详情 | `frontend/src/components/modelPlaza/ModelPlazaContent.vue` |
| 模型卡片和聚合 | `frontend/src/components/modelPlaza/PlazaModelCard.vue`、`catalog.ts` |
| 独立页面和导航 | `frontend/src/views/ModelPlazaView.vue`、`PlazaNavBar.vue` |
| 中英文文案 | `frontend/src/i18n/locales/{zh,en}/dashboard.ts` 的 `modelPlaza` 对象 |

后续调整品牌色时，同时维护 CSS 变量、Tailwind 的 `primary` 色阶及图表首系列颜色。业务状态、模型供应商和支付渠道的识别色仍有独立含义。

## 本地预览

模型广场可以用独立示例接口预览，无需登录。示例模型、价格和分组仅用于展示，不代表线上数据。服务只监听本机，不能完成真实登录、付款或计费。

终端一，在仓库根目录运行：

```powershell
cd D:\github\sub2api2
python analysis/model-plaza-preview.py --serve --port 8082
```

终端二，启动前端：

```powershell
cd D:\github\sub2api2\frontend
corepack pnpm@9.15.5 install --frozen-lockfile
$env:VITE_DEV_PROXY_TARGET = 'http://127.0.0.1:8082'
corepack pnpm@9.15.5 exec vite --host 127.0.0.1 --port 3001 --strictPort
```

访问 <http://127.0.0.1:3001/model-plaza>。连接真实测试后端时，将 `VITE_DEV_PROXY_TARGET` 改成其地址并重启前端；后台需要启用模型广场。

## 验证结果

- pnpm `9.15.5` 冻结锁文件安装通过，没有新增运行时依赖。
- 全量 ESLint、`vue-tsc -b` 和 Vite 生产构建通过。
- 15 个相关测试文件、145 项测试通过，覆盖模型广场及定价、图表、侧栏、设置页、管理仪表盘、密钥、画布、支付、路由访问、密钥用量查询和国际化。
- 模型广场在 1440、768、390、320 像素宽度检查浅深主题、搜索、分类、分组和图片独立倍率筛选、展开、详情弹窗、Esc 关闭及焦点返回、空结果、失败重试、后台内嵌入口和长名称。
- 登录页、用户仪表盘、用量页、首页及密钥查询页检查桌面和手机布局；同时检查画布及白名单侧栏入口存在、图表已绘制且包含品牌色。
- 共生成 28 张模型广场截图及 16 张全站主题截图；检查未发现页面横向溢出、坏图或页面运行异常，并人工查看了代表性的浅深主题、手机详情和仪表盘截图。手机价格详情表保留内部横向滚动。

构建仍提示 Browserslist 数据较旧、混用动态/静态导入及部分分包超过 500 KB；未阻止构建。部分原有测试会输出 mock 导出缺失或 `router-link` stub 的日志，相关测试均通过。

浏览器检查使用独立 Playwright 上下文和示例数据；尚未联调真实登录、网关请求、支付或余额结算，没有部署到服务器。

复现源码检查，在 `frontend` 目录运行：

```powershell
corepack pnpm@9.15.5 run lint:check
corepack pnpm@9.15.5 exec vue-tsc -b
corepack pnpm@9.15.5 exec vitest run src/components/modelPlaza/__tests__ src/components/charts/__tests__ src/components/layout/__tests__/AppSidebar.spec.ts src/views/admin/__tests__/DashboardView.spec.ts src/views/admin/__tests__/SettingsView.spec.ts src/views/user/__tests__/KeysView.spec.ts src/views/user/__tests__/InfiniteCanvasView.spec.ts src/views/user/__tests__/PaymentView.spec.ts src/router/__tests__/feature-access.spec.ts src/views/__tests__/KeyUsageView.spec.ts src/i18n/__tests__/localeKeyCompleteness.spec.ts --maxWorkers=4 --minWorkers=1
corepack pnpm@9.15.5 exec vite build
```

浏览器检查需要本机安装 Python Playwright 和 Microsoft Edge。在上述两个预览服务启动后，从仓库根目录运行：

```powershell
python analysis/model-plaza-preview.py
python analysis/foxcode-visual-check.py
```

可通过环境变量 `FOXCODE_PREVIEW_URL` 更换被测前端地址，默认 `http://127.0.0.1:3001`。截图与报告生成至已忽略的 `output/model-plaza-qa/` 和 `output/foxcode-qa/`，不进入应用构建或 Git 提交。

## 部署衔接

Vite 产物位于 `backend/internal/web/dist`。要部署这份定制界面，需要用本目录源码重新构建项目 Docker 镜像，或重新构建带 `embed` 标签的 Go 二进制，再通过现有部署流程替换应用。

现有 Compose 和在线更新仍指向原上游，直接拉取上游镜像或使用原上游在线更新会覆盖定制界面。正式发布时应明确使用自己的构建产物和镜像标签。本次没有更改部署来源，也没有增加数据库迁移。

## 首页、登录页与注册页设计（2026-09-18）

通过 camoufox-reverse MCP 实际查看了 Fluxion 的首页、登录页和注册页。参考其明确的入口、模型浏览和接入步骤，采用适合 FoxCode 暖色系的“创作工作台”方向：以“少一点配置，多一点创造”为首页主题，用非对称排版、连接线和陶土橙图形建立页面识别。

### 首页

首屏左侧为产品说明与开始入口，右侧为原创 SVG/CSS 绘制的“灵感接入台”。编程、写作、图像三个按钮切换场景文案和 API 路径示意，不会发起模型请求。下方依次展示模型生态、选模型/管密钥/查用量三个功能入口、三步接入说明及开始按钮。

没有使用参考站的图片、Logo、价格、承诺指标或在线状态。模型图标复用项目原有组件。站名、Logo、文档地址继续读取本系统设置；开始按钮根据登录状态和注册开关跳转；模型广场入口仍遵守开关及登录要求。

**自定义首页 HTML/URL 和简洁首页模式保留原有优先级。** 若线上配置了这些选项，默认新首页不会覆盖它们；展示本次完整首页需在后台使用默认首页模式。

### 账号入口

登录和注册使用公共导航及桌面双栏布局：左侧为品牌文案和原创连接线图形，右侧为表单。手机屏幕收起装饰区域，突出表单。两页各自设置标题和说明，支持中英文与浅深主题。

本次仅修改登录/注册模板与布局，两个页面的认证脚本保持不变。注册关闭、邀请码、优惠码、验证码、OAuth、Passkey、协议确认、邮件验证、两步验证和错误处理沿用原有流程。密码显隐按钮补充了无障碍名称与状态。找回密码、邮箱验证和 OAuth 回调继续使用原有单栏 AuthLayout 分支。

### 新增维护入口

| 文件 | 用途 |
| --- | --- |
| `frontend/src/components/layout/PublicHeader.vue` | 公共页品牌导航、主题切换和手机菜单 |
| `frontend/src/composables/usePublicBrand.ts` | 公共导航的品牌设置、功能入口及主题状态 |
| `frontend/src/components/common/ConnectionStudio.vue` | 首页三种场景的交互示意 |
| `frontend/src/views/HomeView.vue` | 默认首页结构与样式 |
| `frontend/src/components/layout/AuthLayout.vue` | 登录/注册品牌布局；其他账号页面的原布局 |
| `frontend/src/i18n/locales/{zh,en}/brand.ts` | 本轮新增的中英文品牌文案 |
| `analysis/public-pages-visual-check.py` | 公共页面浏览器验证脚本 |

### 本轮验证与预览

全量 ESLint、TypeScript 和生产构建通过；11 个相关测试文件的 77 项用例通过（原 73 项加 4 项首页入口开关回归），包含认证、验证码动作门控、OAuth、两步验证、原简洁首页行为及国际化。

浏览器检查覆盖中文 1440/1024/768/390/320 像素和英文 1440/390 像素下的三个页面、浅深两种主题，以及注册关闭、OAuth/邀请码/优惠码、协议展示状态，共生成 45 张截图。检查密码显隐、导航、场景切换以及本地模拟拒绝响应的登录/注册提交；未发现横向溢出、缺失翻译、坏图或主流程页面运行异常。桌面、手机、中英文及深色代表截图已人工查看。

该验证使用隔离浏览器上下文、虚构邮箱和本地拦截的接口，未操作真实账户、未调用模型，也未执行真实 OAuth 或验证码服务。构建提示与上轮相同，尚未部署到服务器。

沿用前文两个本地预览服务：

- 首页：<http://127.0.0.1:3001/home>
- 登录页：<http://127.0.0.1:3001/login>
- 注册页：<http://127.0.0.1:3001/register>

运行 `python analysis/public-pages-visual-check.py` 可重新生成 `output/public-pages-qa/` 内的截图和报告。普通预览服务仅返回公开配置和示例模型列表，不提供真实登录/注册服务。

## 用户控制台改版（2026-09-18）

仪表盘、API 密钥和使用记录页采用更紧凑的统计与工作区布局，增加初次加载失败重试、手机筛选/菜单适配和减少动态效果支持。
所有新增配色来自现有 FoxCode 变量；按钮使用 `--ui-action`，图表保留品牌首色与分类色。
原提供商选择、智能路由、平台配额、近 30 天统计、批量图像权限及导航功能继续保留。

维护入口为 `frontend/src/styles/console-shell.css`、`console-workspace.css`、
`frontend/src/composables/useConsoleWorkspace.ts` 和 `frontend/src/components/user/dashboard/`。
样式由路由限定到 `/dashboard`、`/keys`、`/usage`；切换到其他页面后不继续覆盖其布局。
手机日期弹层输入框纵向排列，避免窄屏时右侧日期被挤住。

新增独立预览：在 `frontend` 下运行 `corepack pnpm@9.15.5 run dev:console`，打开
<http://127.0.0.1:4317/dashboard>。默认端口 4317，可用 `--port` 指定其他端口。
该预览提供三个用户控制台页面的模拟数据和演示密钥操作，不连接真实后端，重启清空操作结果。
生产构建禁止使用此模式，预览代码与生产 Vite 配置隔离。

本轮通过全量 ESLint、应用/预览 TypeScript 检查、生产构建及 341 项相关测试。
48 组浏览器页面检查及三种宽度的交互检查通过；截图和报告见本机 `output/console-qa/`。
来源、范围及验证细节记录于 `UPSTREAM_UPDATES.md`。前文公共页/模型广场预览脚本是此前验证记录，
当前工作区已删除这些脚本；本轮新增控制台预览不依赖它们。
