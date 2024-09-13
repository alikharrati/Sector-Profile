export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');  // یا دامنه خاص مانند 'https://your-github-page-url'
  res.setHeader('Access-Control-Allow-Methods', 'POST');
  
  const apiKey = process.env.API_KEY;

  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "x-api-key": apiKey,
      "content-type": "application/json",
      "anthropic-version": "2023-06-01"
    },
    body: JSON.stringify({
      model: "claude-3-5-sonnet-20240620",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Please improve this resume." }]
    })
  });

  const data = await response.json();
  res.status(200).json(data);
}
