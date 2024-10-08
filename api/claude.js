export default async function handler(req, res) {
  // مدیریت درخواست‌های OPTIONS برای CORS
  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Origin', 'https://sector-profile.vercel.app');  // می‌توانید به جای * دامنه خاصی تنظیم کنید
    res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    res.status(200).end();
    return;
  }

  // فقط متد POST مجاز است
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST, OPTIONS');
    return res.status(405).json({ message: 'Only POST requests are allowed' });
  }

  const apiKey = process.env.API_KEY;  // کلید API از متغیرهای محیطی

  // دریافت محتوای رزومه از بدنه درخواست
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

    const data = await response.json();

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

