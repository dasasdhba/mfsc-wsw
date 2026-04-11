# 说明

## 本地测试

请配置环境变量 `SILICONFLOW_API_KEY` 用于文字识别，然后运行 `python draw_local.py`

## GitHub Action

请打开 repo Action 的读写权限，并配置 repo secret `SILICONFLOW_API_KEY`；此外，由于 GitHub Action 的 CronJob 无法正常工作，推荐使用 Cloudflare Worker 部署自动化触发 Action，具体来说：

1. 将 `worker.js` 部署到 Cloudflare Worker
2. 在 setting 中填入环境变量 `GITHUB_TOKEN`、`GITHUB_OWNER`、`GITHUB_REPO`，这里的 token 要确保有 `repo` 权限（用于提交代码）
3. 在 setting 中设定好 CronJob 间隔，设定为每小时一次就好

## 已收集的节气挂命图

- Aggressive Dance-113-Difficulty 11
- Aggressive Dance-89-Difficulty 11
- Aggressive Dance-2-Difficulty 11
- Aggressive Dance-97-Difficulty 11
- Weather Insurrection-124-Difficulty 12
- Aggressive Dance-62-Difficulty 11
- Aggressive Dance-111-Difficulty 11
- Aggressive Dance-105-Difficulty 11
- 夜空のPスイッチロマンス38-Difficulty H
- Aggressive Dance-131-Difficulty 11
- 夜空のPスイッチロマン-130-Difficulty 11
- Aggressive Dance-33-Difficulty 11
- 夜空のPスイッチロマン-64-Difficulty 11
- Aggressive Dance-4-Difficulty 11
- Aggressive Dance-99-Difficulty 11
- 夜空のPスイッチロマン-131-Difficulty 11
- 夜空のPスイッチロマン-138-Difficulty 11
- 夜空のPスイッチロマン-54-Difficulty 11
- 夜空のPスイッチロマン-69-Difficulty 11
- 夜空のPスイッチロマン-101P-Difficulty 11
- Aggressive Dance-127-Difficulty 11
- 夜空のPスイッチロマンス39-Difficulty 11
- Aggressive Dance-53-Difficulty 11
- Aggressive Dance-114-Difficulty 11
- Aggressive Dance-25-Difficulty 11
- 夜空のPスイッチロマン-51-Difficulty 11
- Aggressive Dance-128-Difficulty 11
- Aggressive Dance-47-Difficulty 11
- 夜空のPスイッチロマン-106-Difficulty 11
- 夜空のPスイッチロマン-67-Difficulty 11
- Aggressive Dance-40-Difficulty 11
- Weather Insurrection-112-Difficulty 12
- 夜空のPスイッチロマン-72-Difficulty 11
- Aggressive Dance-50-Difficulty 11
- Aggressive Dance-87-Difficulty 11
- Aggressive Dance-63-Difficulty 11
- Aggressive Dance-34-Difficulty 11
- Aggressive Dance-59-Difficulty 11
- 夜空のPスイッチロマン-128-Difficulty 11
- Aggressive Dance-54-Difficulty 11
- Aggressive Dance-17-Difficulty 11
- Aggressive Dance-88-Difficulty 11
- Aggressive Dance-39-Difficulty 11
- Aggressive Dance-109-Difficulty 11
- Scourge of Depravity-16-Difficulty 11
- Aggressive Dance-90-Difficulty 11
- Aggressive Dance-157-Difficulty 11
- Aggressive Dance-215-Difficulty 11
- Scourage of Depravity-53-Difficulty 11
- Aggressive Dance-191-Difficulty 11
- Scourge of Depravity-68-Difficulty 11
- Aggressive Dance-224-Difficulty 11
- Aggressive Dance-219-Difficulty 11
- Scourge of Depravity-62-Difficulty 11
- Scourge of Depravity-42-Difficulty 11
- Scourge of Depravity-32-Difficulty 11
- Scourge of Depravity-3-Difficulty 11
- Scourage of Depravity-12-Difficulty 11
- Aggressive Dance-181-Difficulty 11
- Scourge of Depravity-33-Difficulty 11
- Scourge of Depravity-39-Difficulty 11
- Aggressive Dance-201-Difficulty 11
- Aggressive Dance-138-Difficulty 11
- Scourage of Depravity-40-Difficulty 11
- Scourge of Depravity-27-Difficulty 11
- Scourge of Depravity-13-Difficulty 11
- Aggressive Dance-182-Difficulty 11
- Scourge of Depravity-57-Difficulty 11
- Aggressive Dance-193-Difficulty 11
- Scourge of Depravity-51-Difficulty 11
- Aggressive Dance-218-Difficulty 11
- Scourge of Depravity-58-Difficulty 11
- Scourge of Depravity-26-Difficulty 11
- Scourge of Depravity-65-Difficulty 11
- Aggressive Dance-96-Difficulty 11
- Scourge of Depravity-79-Difficulty 11
- Scourge of Depravity-22-Difficulty 11
- Aggressive Dance-214-Difficulty 11
- Scourge of Depravity-76-Difficulty 11
- Scourge of Depravity-85-Difficulty 11
- Scourge of Depravity-31-Difficulty 11
- Scourage of Depravity-5-Difficulty 11
- Scourge of Depravity-10-Difficulty 11
- Aggressive Dance-202-Difficulty 11
- Aggressive Dance-223-Difficulty 11
- Aggressive Dance-137-Difficulty 11
- Scourge of Depravity-43-Difficulty 11
- Aggressive Dance-162-Difficulty 11
- Scourage of Depravity-86-Difficulty 11
- Aggressive Dance-135-Difficulty 11
- Scourage of Depravity-69-Difficulty 11
- Scourge of Depravity-25-Difficulty 11
- Aggressive Dance-206-Difficulty 11
- Scourge of Depravity-1-Difficulty 11
- Scourge of Depravity-38-Difficulty 11
- Scourge of Depravity-48-Difficulty 11
- Scourage of Depravity-11-Difficulty 11
- Scourge of Depravity-23-Difficulty 11
- Scourge of Depravity-80-Difficulty 11
- Scourge of Depravity-21-Difficulty 11
- Scourge of Depravity-35-Difficulty 11
- Aggressive Dance-117-Difficulty 11
