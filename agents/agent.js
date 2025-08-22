// agents/agent.js
import express from 'express';
import fetch from 'node-fetch';
import { RealtimeAgent, tool } from '@openai/agents/realtime';
import { z } from 'zod';

const app = express();
app.use(express.json());

// Tool to call Django supervisor endpoint
const supervisorAgent = tool({
  name: 'supervisorAgent',
  description: 'Passes a case to your supervisor for approval.',
  parameters: z.object({ caseDetails: z.string() }),
  execute: async ({ caseDetails }, details) => {
    const history = details.context.history || [];
    const res = await fetch('http://localhost:8000/chat/supervisor-check/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ caseDetails, history }),
    });
    const data = await res.json();
    return data.message;
  },
});

// Main RealtimeAgent
const returnsAgent = new RealtimeAgent({
  name: 'Returns Agent',
  instructions: `
    You are a returns agent. Handle requests and always check with your supervisor before responding.
  `,
  tools: [supervisorAgent],
});

app.get('/', (req, res) => {
  res.send('RealtimeAgent is running! Use POST /chat to interact.');
});

// Endpoint for frontend chat
app.post('/chat', async (req, res) => {
  const { message } = req.body;
  if (!message) return res.status(400).json({ error: 'Message is required' });

  try {
    const response = await returnsAgent.run({
      input: message,
      context: { history: [] }
    });
    res.json({ response: response.output_text });
  } catch (err) {
    console.error(err);
    res.status(500).json({ response: '⚠️ Agent error occurred' });
  }
});

// Start server
const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Node RealtimeAgent running at http://localhost:${PORT}`);
});
