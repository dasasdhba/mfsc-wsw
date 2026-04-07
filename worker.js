export default {
  async scheduled(event, env, ctx) {
    const GITHUB_TOKEN = env.GITHUB_TOKEN;
    const OWNER = env.GITHUB_OWNER;
    const REPO = env.GITHUB_REPO;
    const response = await fetch(`https://api.github.com/repos/${OWNER}/${REPO}/dispatches`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${GITHUB_TOKEN}`,
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "Cloudflare-Worker"
      },
      body: JSON.stringify({
        event_type: "mfsc-draw-trigger"
      })
    });
    console.log("Status:", response.status);
    if (response.ok) {
      console.log("GitHub Action triggered successfully");
    } else {
      console.error("Failed to trigger GitHub Action");
    }
  }
};