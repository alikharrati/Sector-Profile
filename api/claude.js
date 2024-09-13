export default async function handler(req, res) {
  const apiKey = process.env.API_KEY;  // کلید API از متغیر محیطی خوانده می‌شود

  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "x-api-key": apiKey,  // کلید API از متغیر محیطی گرفته می‌شود
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

