import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage, SystemMessage } from "@langchain/core/messages";

export const generateResumeNode = async (resume: string, jd: string) => {
  const model = new ChatOpenAI({ modelName: "gpt-4-turbo" });
  
  const response = await model.invoke([
    new SystemMessage("You are an experienced IT recruiter, ATS specialist... (insert full prompt here)"),
    new HumanMessage(`Analyze this resume: ${resume} against this job description: ${jd}`)
  ]);

  return { result: response.content };
};