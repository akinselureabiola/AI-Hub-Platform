"use client";
import { useState } from "react";

export default function DashboardPage() {
  const [input, setInput] = useState("");

  const actionCards = [
    "Ask your AI agent anything", 
    "Review agent responses", 
    "Route workflows automatically", 
    "Tune prompts for precision"
  ];

  return (
    <main className="min-h-screen bg-gray-950 text-white font-sans w-full overflow-x-hidden">
      <div className="mx-auto w-full max-w-7xl px-3 py-4 sm:px-6 lg:px-8">
        
        {/* Header - Stacks on mobile, side-by-side on desktop */}
        <header className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold">Your AI Cockpit</h1>
            <p className="text-sm text-gray-400 mt-1">Welcome back, WA³S Dashboard</p>
          </div>
          <div className="rounded-full bg-gray-900 px-4 py-2 text-sm text-gray-300 break-all border border-gray-800">
            daizsign@gmail.com
          </div>
        </header>

        {/* Layout - Horizontal scroll sidebar on mobile, fixed column on desktop */}
        <div className="grid gap-6 lg:grid-cols-[240px_1fr]">
          
          <aside className="overflow-x-auto lg:overflow-visible pb-2 lg:pb-0">
            <div className="flex gap-2 lg:flex-col">
              <button className="whitespace-nowrap rounded-lg bg-blue-600 px-4 py-3 font-medium">Home</button>
              <button className="whitespace-nowrap rounded-lg bg-gray-900 px-4 py-3 text-gray-300 hover:bg-gray-800">AI Agents</button>
              <button className="whitespace-nowrap rounded-lg bg-gray-900 px-4 py-3 text-gray-300 hover:bg-gray-800">Settings</button>
            </div>
          </aside>

          {/* Main Content Area */}
          <section className="rounded-xl border border-gray-800 bg-gray-900 p-4 sm:p-6 shadow-xl">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold">WA³S Assistant</h2>
              <span className="rounded bg-green-900/30 px-3 py-1 text-xs font-semibold text-green-400 border border-green-900">
                LIVE BETA
              </span>
            </div>
            
            <p className="text-green-400 font-semibold text-sm mb-6">AGENT STATUS: READY</p>

            {/* Responsive Action Cards - 1 col mobile, 2 col desktop */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {actionCards.map((text) => (
                <button 
                  key={text}
                  className="rounded-xl border border-gray-700 bg-gray-950 p-5 text-left text-gray-300 hover:border-blue-500 transition-all"
                >
                  {text}
                </button>
              ))}
            </div>

            {/* Responsive Input Section */}
            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <input
                className="h-12 flex-1 rounded-lg border border-gray-700 bg-gray-950 px-4 text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none"
                placeholder="Ask your AI agent anything..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
              />
              <button className="h-12 rounded-lg bg-blue-600 px-8 font-medium text-white hover:bg-blue-700">
                Send
              </button>
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}