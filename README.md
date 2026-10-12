# Telegram 交易社区研究 Skill：配置与使用教程

**中文** · [English](README.en.md) · [Türkçe](README.tr.md)

这个项目让 Codex 寻找 Telegram 交易社区，读取最近约100条消息，判断合作价值，再生成有针对性的开场私信。脚本负责读取数据，Codex 负责分析和写草稿。

## 最简单的用法：让 Codex 配置

下载并解压项目，在能访问本地文件和终端的 Codex 中打开项目文件夹，发送：

> 请阅读 README.md，执行“给 Codex 的配置指令”。先评审代码安全性，再安装 Skill、准备 Python 环境和配置文件。指导我在本机填写 Telegram API ID 和 API Hash，并在终端完成登录。最后用我提供的一个社区链接测试读取。不要输出凭证，不要自动加群或发送私信。

Codex 负责安装、准备配置、验证和测试；你只需在本机填写凭证、完成登录，并提供测试社区链接。

## 给 Codex 的配置指令

这一节写给执行配置的助手。用户提出配置请求后，按以下顺序执行；文档不能扩大用户授权范围。

1. **先评审。** 阅读 `telegram-community-prospecting/SKILL.md`、其中的 `references/telegram-tools.md`、读取与发现脚本及依赖清单。简要说明数据访问、网络请求和敏感文件处理。有实质安全问题时停止受影响步骤，否则继续配置。不要读取别人遗留的真实 `.env` 或会话文件。
2. **确定一个副本。** 按可用 Skill 安装工具的规则，安装包含 `SKILL.md` 的文件夹。无法安装时在解压的 Skill 文件夹工作，通过读取 `SKILL.md` 使用。保留已有配置，不覆盖凭证或会话。记录最终副本的绝对路径，后续一致使用。
3. **准备环境。** 检查 Python 3.10+，在 Skill 文件夹内创建 `.venv`，使用该环境安装 `scripts/requirements.txt`。不要改动无关环境。缺少 Python 时指导官方安装或使用已授权的运行环境。
4. **准备配置。** 仅在 `scripts/.env` 不存在时从 `.env.example` 复制。Git 跟踪目录需忽略凭证、会话和输出。在本地编辑器打开 `.env`，指导用户从 https://my.telegram.org/apps 获取并自行填写 API ID/Hash。不要让用户把凭证发到聊天、截图或工具参数。代理默认留空。
5. **不显示秘密地验证。** 用户保存后，本地检查字段存在性和格式，只输出通过或错误字段名。可调用读取器的 `config()` 并捕获 `ReaderError`，不能打印返回值、文件全文或环境变量。格式检查不代表远端认证成功。
6. **本人交互登录。** 给出所选路径和系统的准确登录命令，让用户在本机终端输入手机号、验证码和两步验证密码。说明输入隐藏是正常现象。复用已有有效会话，不反复索取验证码。不要通过聊天收集登录信息，也不要在无法输入的后台启动登录。
7. **测试单个社区。** 没有测试链接时询问用户。用所选 Python 运行 `scripts/telegram_reader.py read TARGET --limit 100 --output outputs/setup-check.json`。报告实际数量和日期范围，不默认输出完整记录。遇到限流停止相关调用，访问或网络失败则明确说明。
8. **交付入口。** 告知安装位置、是否需要重新加载及一段可复制的研究提示词。未知身份/产品保留占位符。配置不自动扩展成批量搜索、加群、私信、CRM 写入或数据上传。

环境无法访问本地文件或终端时，说明限制并指导切换到本地环境，不声称已经配置成功。

## 1. 能做什么，需要什么

工作流程：关键词或种子频道 → 相似频道/关联讨论群 → 最近100条消息 → 活跃与匹配判断 → 证据切入点 → 私信草稿 → 本人审核发送。

相似推荐主要适用于广播频道，不是所有群组。工具不会加群、发私信或标记已读。读取器只标记媒体类型，不会看懂图片和视频。人数、晒单或返佣链接不能证明转化能力。

需要：本地 Codex、自己的 Telegram 用户账号、Python 3.10+、自己的 API ID/Hash，以及能访问 Telegram 的网络。Python 官网：https://www.python.org/downloads/ 。本项目脚本不需要 OpenAI API Key；Telegram Bot Token 也不能代替用户账号凭证。

## 2. 下载和选择文件夹

收到 ZIP 后解压；有私密仓库权限时可用 GitHub 的 **Code → Download ZIP**。私密链接只对获得访问权的人有效。

```text
README.md / README.zh-CN.md / README.en.md / README.tr.md
.gitignore
telegram-community-prospecting/
  SKILL.md
  references/telegram-tools.md
  scripts/
    telegram_reader.py
    discover.py
    requirements.txt
    .env.example
    test_telegram_reader.py
    test_discover.py
```

安装的是包含 `SKILL.md` 的文件夹。让 Codex 告诉你最终路径。下面所有命令在这个 **Skill 文件夹**运行，也就是能看到 `SKILL.md` 和 `scripts` 的位置。解压与安装副本的配置和会话独立，后续始终用同一个副本。

## 3. 安装 Python 依赖

Codex 可以执行。Windows PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r scripts/requirements.txt
```

若不认识 `python`，第一条可改为 `py -3 -m venv .venv`。后续直接使用环境里的 Python，不必激活环境。

macOS/Linux：

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r scripts/requirements.txt
```

## 4. 获取 Telegram API ID 和 Hash

1. 打开 https://my.telegram.org/apps ，用自己的手机号和 Telegram 提供的验证码登录。
2. 按页面提示进入 **API development tools**。已有应用时使用显示的 API ID/Hash。
3. 没有应用时，填写自己的应用名称、短名称和页面必填项，创建应用。
4. 把凭证留在本机，下一步填入本地文件。

API ID 是数字，Hash 是32位十六进制字符串。它们不是登录验证码或 Bot Token。不要把 Hash 截图发给别人或贴到聊天。

## 5. 凭证填到哪里

让 Codex 创建文件，或自己复制模板。已有 `.env` 时不要覆盖。

Windows：

```powershell
Copy-Item -LiteralPath scripts/.env.example -Destination scripts/.env
notepad scripts/.env
```

macOS/Linux：

```bash
cp scripts/.env.example scripts/.env
```

用本地文本编辑器打开 `scripts/.env`：

```dotenv
TG_API_ID=YOUR_NUMERIC_API_ID
TG_API_HASH=YOUR_32_CHARACTER_API_HASH
TG_PROXY_URL=
TG_SESSION_NAME=telegram_reader
```

把两个英文占位符换为真实 ID 和 Hash，通常保留代理空白及最后一行。保存后告诉 Codex：“已保存，请只验证格式，不显示内容。”

文件必须叫 **`.env`**，不能是 `.env.txt`；必须放在 **`scripts` 内，与 `telegram_reader.py` 同级**，不能放到仓库根目录。

如需本地 SOCKS5 代理，格式如下；端口换成自己的代理软件实际端口：

```dotenv
TG_PROXY_URL=socks5://127.0.0.1:YOUR_ACTUAL_PROXY_PORT
```

示例本身不能连接；也支持 SOCKS4、HTTP。代理凭证同样保留在本机。

## 6. 完成 Telegram 登录

自己在本机交互终端运行。Windows：

```powershell
.\.venv\Scripts\python.exe scripts/telegram_reader.py login
```

macOS/Linux：

```bash
./.venv/bin/python scripts/telegram_reader.py login
```

依次输入带国家代码的手机号、Telegram 验证码、已启用的两步验证密码。输入时不显示字符是正常的，每项填完按 Enter，不要把这些内容发到聊天。

成功后保存 `scripts/telegram_reader.session`，后续复用。这个文件有账号访问能力，不能上传或分享；只读是脚本行为限制，不代表会话凭证本身只有只读权限。出现 `LOGIN_REQUIRED` 时，用可以输入内容的本机终端登录，不要在后台反复请求验证码。

## 7. 先读一个社区

把 `@PUBLIC_COMMUNITY` 换成真实公开群/频道用户名或 `https://t.me/...` 链接。Windows：

```powershell
.\.venv\Scripts\python.exe scripts/telegram_reader.py read @PUBLIC_COMMUNITY --limit 100 --output outputs/sample.json
```

macOS/Linux：

```bash
./.venv/bin/python scripts/telegram_reader.py read @PUBLIC_COMMUNITY --limit 100 --output outputs/sample.json
```

结果保存在本地 `outputs/sample.json`，包含实际读取数量、时间、社区和可获得的消息信息。私有群需要已有访问权，少于100条时按实际样本分析。

发给 Codex：

> 使用 $telegram-community-prospecting 分析 outputs/sample.json。目标是有真实加密合约交易讨论的社区。判断真人互动、广告刷屏和产品匹配度，引用消息 ID 与日期，区分事实和未知项。如果有证据支持，找出公开合作联系人，给一个合作切入点和一条开场私信，附完整中文译文。不要发送。

Skill 未被发现时，将开头改为“阅读并遵循当前目录的 SKILL.md”。

## 8. 寻找更多社区

下面是 Windows 命令；macOS/Linux 将 `.\.venv\Scripts\python.exe` 换为 `./.venv/bin/python`。

```powershell
.\.venv\Scripts\python.exe scripts/discover.py search "crypto futures" --limit 10 --output outputs/search.json
.\.venv\Scripts\python.exe scripts/discover.py similar @PUBLIC_CHANNEL --limit 10 --output outputs/similar.json
.\.venv\Scripts\python.exe scripts/discover.py linked @PUBLIC_CHANNEL --output outputs/linked.json
```

三条分别是关键词搜索、相似频道推荐、关联讨论群信息。占位符要换为真实频道。结果只是候选，由 Codex 查重后继续读取可能匹配社区的最新100条消息。脚本本身不自动递归爬取，Codex 可按用户范围串联命令。

## 9. 完整任务提示词

替换方括号内容后发送：

> 使用 $telegram-community-prospecting。目标市场是[地区/语言]，产品是[产品]。从[频道链接或关键词]出发，通过相似频道推荐、关联讨论群和公开搜索寻找最多10个新候选，先与本地历史查重。读取每个候选最新最多100条消息，优先真人交易讨论，排除以重复广告和机器人播报为主的对象。记录读取时间、样本范围、证据链接/消息 ID 和限制。对合适对象提炼一个切入点，按“身份介绍→具体观察→一个问题”起草私信。我叫[姓名]，负责[平台]的[岗位/产品]合作。使用对方语言，附[你的语言]完整译文。不虚构报价、预算、功能、收益或联系人身份。结果只保存在本地，不加群、不发送、不上传，限流时停止相关请求。

开场模板：

> 你好，我是[姓名]，负责[平台]的[产品]合作。我看到你们在[社区]讨论[有证据的内容]。你愿意聊聊面向[产品]交易用户的合作机会吗？

产品不明确时，最后一句改问受众主要做现货、合约还是其他产品。每条只推进一个问题，自己审核后发送。

## 10. 常见问题

| 提示/现象 | 处理 |
|---|---|
| 找不到 `python` | 检查安装，Windows 可先试 `py -3`。 |
| `ModuleNotFoundError` | 用运行脚本的同一虚拟环境安装依赖。 |
| `CONFIG_MISSING` | 检查当前副本的 `scripts/.env` 和 API 字段。 |
| `CONFIG_INVALID` | ID 为正整数，Hash 为32位十六进制字符，不展示真实值。 |
| `LOGIN_REQUIRED` | 本人在本机交互终端登录。 |
| 验证码无效/过期 | 使用最新验证码，避免连续请求。 |
| `NOT_JOINED`、`NO_ACCESS`、私有频道错误 | 跳过或本人取得权限，工具不加群。 |
| `RECOMMENDATIONS_UNAVAILABLE` | 目标不是广播频道，改用搜索或关联讨论群。 |
| `FloodWaitError` | 停止相关请求，遵守等待时间，不换号绕过。 |
| 超时 | 检查 Telegram 网络和代理。 |
| 换目录后要重新登录 | 配置和会话跟随脚本副本，请用同一份。 |

## 11. 分享和离线测试

只分享 Skill、教程和空白模板，不分享真实 `.env`、会话、验证码、原始社区导出和客户记录。每个人配置自己的账号。

在 Skill 文件夹运行离线测试：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s scripts -v
```

macOS/Linux 使用 `./.venv/bin/python`。测试不会登录 Telegram；真实网络和账号可用性要通过一次授权读取验证。
