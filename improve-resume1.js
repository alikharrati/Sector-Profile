import { Configuration, OpenAIApi } from "openai";

const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
});

const openai = new OpenAIApi(configuration);

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        res.setHeader('Allow', ['POST']);
        return res.status(405).end(`Method ${req.method} Not Allowed`);
    }

    const { resume_text } = req.body;

    if (!resume_text) {
        return res.status(400).json({ error: 'Resume text is required' });
    }

    try {
        const response = await openai.createCompletion({
            model: "davinci-002",
            prompt: `Improve this resume:\n\n${resume_text}`,
            max_tokens: 150,
        });

        // اضافه کردن console.log برای بررسی پاسخ
        console.log('OpenAI response:', response);

        res.status(200).json({ improved_resume: response.data.choices[0].text.trim() });
    } catch (error) {
        console.error('OpenAI API error:', error);
        res.status(500).json({ error: 'Failed to improve resume' });
    }
}
