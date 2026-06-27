"use client";
import { useState } from "react";

type Message = { role: 'user' | 'bot'; text: string };

export default function DashboardPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");

  const handleSend = (text: string) => {
    const messageText = text || input;
    if (!messageText.trim()) return;
    
    const newMessages: Message[] = [...messages, { role: 'user', text: messageText }];
    setMessages(newMessages);
    
    setTimeout(() => {
      setMessages([...newMessages, { 
        role: 'bot', 
        text: `[MOCK MODE ACTIVE] The bridge is perfectly wired! I received your message: "${messageText}". Your frontend is ready for the real Brain.` 
      }]);
    }, 600);
    
    setInput("");
  };

  const actionCards = [
    "Ask your AI agent anything", 
    "Review agent responses", 
    "Route workflows automatically", 
    "Tune prompts for precision"
  ];

  return (
    <main className="min-h-screen bg-[#020617] text-white p-4 font-sans">
      <nav className="flex justify-between items-center py-4 mb-6">
        <h1 className="text-xl font-bold">AI Hub</h1>
        <div className="flex gap-6 text-sm text-slate-400">
          <span className="text-white">Home</span>
          <span>Features</span>
          <span>Docs</span>
        </div>
      </nav>

      <div className="bg-[#0b1120] border border-slate-800 rounded-2xl p-6 shadow-xl">
        <div className="flex justify-between items-start mb-8">
          <div className="flex items-center gap-4">
            <div className="bg-blue-600 p-3 rounded-lg font-bold">W</div>
            <div>
              <p className="text-[10px] uppercase text-slate-400 tracking-wider">WA³S</p>
              <h2 className="font-bold text-lg">Dashboard</h2>
            </div>
          </div>
          <div className="flex-1 mx-8">
            <p className="text-slate-400 text-xs uppercase tracking-widest">Welcome back</p>
            <h1 className="text-3xl font-bold">Your AI cockpit</h1>
          </div>
          <div className="bg-[#1e293b] px-4 py-2 rounded-full flex items-center gap-3">
            <div className="bg-blue-500 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold">DA</div>
            <div>
              <p className="text-xs font-medium">daizsign@gmail.com</p>
              <p className="text-[10px] text-green-400 flex items-center gap-1">
                <span className="w-1.5 h-1.5 bg-green-400 rounded-full"></span> Online - Active now
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-4 gap-6">
          <div className="col-span-1 space-y-4">
            <div className="bg-[#1e293b] p-3 rounded-xl font-medium border-l-2 border-blue-500">Home</div>
            <div className="p-3 text-slate-400">AI Agents</div>
            <div className="p-3 text-slate-400">Settings</div>
            <div className="mt-8 p-4 bg-[#020617] rounded-xl border border-slate-800">
              <p className="text-xs uppercase text-slate-500 mb-2">Workspace</p>
              <div className="flex items-center gap-3 bg-[#1e293b] p-2 rounded-lg">
                <div className="bg-slate-700 p-2 rounded">AI</div>
                <div>
                  <p className="text-sm font-bold">Agent Lab</p>
                  <p className="text-[10px] text-slate-400">Build and run your AI agents</p>
                </div>
              </div>
            </div>
          </div>

          <div className="col-span-3">
            <div className="flex justify-between items-center mb-4">
              <p className="text-[10px] uppercase text-slate-500">AI CHAT</p>
              <span className="text-[10px] bg-green-900/30 text-green-400 px-2 py-0.5 rounded border border-green-900">LIVE BETA</span>
            </div>
            <h2 className="text-2xl font-bold mb-2">WA³S Assistant</h2>
            <p className="text-green-400 font-bold text-sm mb-6">AGENT STATUS: READY</p>

            {/* Interactive Action Cards */}
            <div className="grid grid-cols-2 gap-4 mb-6">
              {actionCards.map((text) => (
                <button 
                  key={text} 
                  onClick={() => handleSend(text)}
                  className="border border-slate-800 p-4 rounded-xl text-sm text-slate-300 hover:border-blue-500 transition-all text-left"
                >
                  {text}
                </button>
              ))}
            </div>

            {/* Chat History */}
            <div className="bg-[#020617] border border-slate-800 rounded-xl p-4 h-[250px] overflow-y-auto mb-4 flex flex-col gap-3">
              {messages.map((m, i) => (
                <div key={i} className={`p-3 rounded-lg text-sm max-w-[80%] ${m.role === 'user' ? 'bg-blue-600 self-end' : 'bg-[#1e293b] self-start'}`}>
                  {m.text}
                </div>
              ))}
            </div>

            <div className="flex gap-2">
              <input 
                className="flex-1 bg-[#020617] border border-slate-800 p-3 rounded-xl text-sm"
                placeholder="Ask your AI agent anything..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend(input)}
              />
              <button onClick={() => handleSend(input)} className="bg-blue-600 px-6 rounded-xl text-sm font-bold">Send</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}