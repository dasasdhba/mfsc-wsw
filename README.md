# 说明

由于 GitHub Action 的 CronJob 无法正常工作，推荐使用 Cloudflare Worker 部署自动化触发 Action，具体来说：

1. 将 `worker.js` 部署到 Cloudflare Worker
2. 在 setting 中填入环境变量 `GITHUB_TOKEN`、`GITHUB_OWNER`、`GITHUB_REPO`，这里的 token 要确保有触发 Action 的权限
3. 在 setting 中设定好 CronJob 间隔，设定为每小时一次就好
