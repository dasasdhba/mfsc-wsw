# 说明

## 本地测试

请配置环境变量 `SILICONFLOW_API_KEY` 用于文字识别，然后运行 `python draw_local.py`

## GitHub Action

GitHub Action 需要配置如下环境变量：

1. `MY_TOKEN`：即 `GITHUB_TOKEN`，可在 GitHub Developer setting 中设置，用于 commit repo
2. `SILICONFLOW_API_KEY`：可在硅基流动申请，用于文字识别

此外，由于 GitHub Action 的 CronJob 无法正常工作，推荐使用 Cloudflare Worker 部署自动化触发 Action，具体来说：

1. 将 `worker.js` 部署到 Cloudflare Worker
2. 在 setting 中填入环境变量 `GITHUB_TOKEN`、`GITHUB_OWNER`、`GITHUB_REPO`，这里的 token 要确保有 `repo` 权限（用于提交代码）
3. 在 setting 中设定好 CronJob 间隔，设定为每小时一次就好

## 已收集的节气挂命图

- Aggressive Dance-59-Difficulty 11
- 夜空のPスイッチロマン-128-Difficulty 11
- Aggressive Dance-54-Difficulty 11
- Aggressive Dance-17-Difficulty 11
- Aggressive Dance-88-Difficulty 11
- Aggressive Dance-39-Difficulty 11
- Aggressive Dance-109-Difficulty 11
