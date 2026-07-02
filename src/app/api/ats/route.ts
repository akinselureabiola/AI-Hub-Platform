import { OpenAI } from "openai";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function POST(req: Request) {
  try {
    const { resumeText, jobDescription } = await req.json();

    const prompt = `
      You are an ATS optimization specialist. 
      Analyze this resume against the job description and return the output in this EXACT format:
      ===FINAL_RESUME===
      [Optimized Resume Here]
      ===FINAL_COVER_LETTER===
      [Optimized Cover Letter Here]

      CANDIDATE RESUME: ${resumeText}
      JOB DESCRIPTION: ${jobDescription}
    `;

    const completion = await openai.chat.completions.create({
      model: "gpt-4o-mini", // Using the efficient, high-performance model
      messages: [{ role: "user", content: prompt }],
      temperature: 0.7,
    });

    const fullResponse = completion.choices[0].message.content || "";
    
    // Simple parser to split the AI response
    const parts = fullResponse.split("===FINAL_COVER_LETTER===");
    const finalResume = parts[0].replace("===FINAL_RESUME===", "").trim();
    const finalCoverLetter = parts[1]?.trim() || "";

    return Response.json({ resume: finalResume, coverLetter: finalCoverLetter });
  } catch (error) {
    return Response.json({ error: "Failed to generate documents" }, { status: 500 });
  }
}