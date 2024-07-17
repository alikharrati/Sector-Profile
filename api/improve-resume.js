import { Configuration, OpenAIApi } from "openai";

const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
});

const openai = new OpenAIApi(configuration);

export default async function handler(req, res) {
    const { resume_text } = req.body;

    const response = await openai.createCompletion({
        model: "text-davinci-003",
        prompt: `Improve this resume:\n\n${resume_text}`,
        max_tokens: 500,
    });

    res.status(200).json({ improved_resume: response.data.choices[0].text.trim() });
}
