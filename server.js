// server.js
import express from 'express';
import cors from 'cors';
import { getAiResponse } from './src/api/OpenAiAPI.js/index.js';

const app = express();
app.use(cors());
app.use(express.json());

app.post('/chat', async (req, res) => {
  const { message } = req.body;
  const response = await getAiResponse(message);
  res.json({ answer: response });
});

app.listen(8001, () => {
  console.log('✅ RAG server running on http://localhost:8001');
});
