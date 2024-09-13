export default async function handler(req, res) {
  // چک کنید که درخواست POST باشد
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Only POST requests are allowed' });
  }

  const apiKey = process.env.API_KEY;  // کلید API مخفی‌شده در Vercel

  // محتوای رزومه ارسال‌شده از طریق بدنه درخواست (request body)
  const { resume } = req.body;

  if (!resume) {
    return res.status(400).json({ message: 'Resume content is required' });
  }

  try {
    // ارسال درخواست به API Claude
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
        messages: [
          { role: "user", content: `Please improve this resume:\n\n${resume}` }
        ]
      })
    });

    // پردازش پاسخ از API Claude
    const data = await response.json();

    // چک کردن وضعیت موفقیت آمیز درخواست
    if (!response.ok) {
      throw new Error(`Error: ${response.status} - ${response.statusText}`);
    }

    // ارسال پاسخ به کاربر
    res.status(200).json(data);
  } catch (error) {
    console.error('Error occurred:', error);
    res.status(500).json({ message: 'Error processing resume', error: error.message });
  }
}

