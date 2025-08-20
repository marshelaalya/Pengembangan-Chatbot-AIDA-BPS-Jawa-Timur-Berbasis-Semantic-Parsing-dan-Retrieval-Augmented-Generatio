// root/src/api/RagApi.js
import axios from 'axios';

const API_URL = 'http://localhost:8000';

/**
 * Mengirim pesan ke RAG chatbot dan mendapatkan respons
 * @param {Array} messages - Array berisi history messages
 * @returns {Promise<string>} - Respons dari RAG chatbot
 */
export async function getAiResponse(messages) {
  try {
    // Ambil pesan terakhir dari user
    const lastUserMessage = messages
      .filter(msg => msg.role === 'user')
      .pop();
    
    if (!lastUserMessage) {
      throw new Error('No user message found');
    }

    // Kirim request ke backend RAG
    const response = await axios.post(`${API_URL}/chat`, {
      message: lastUserMessage.content
    });

    // Return hasil dari RAG
    return response.data.result || 'Maaf, tidak ada respons dari server.';
    
  } catch (error) {
    console.error('Error calling RAG API:', error);
    
    // Handle different error types
    if (error.response) {
      // Server responded with error
      throw new Error(`Server error: ${error.response.status}`);
    } else if (error.request) {
      // No response from server
      throw new Error('Tidak dapat terhubung ke server. Pastikan backend berjalan di http://localhost:8000');
    } else {
      // Other errors
      throw error;
    }
  }
}

/**
 * Mendapatkan ringkasan chat (optional - jika Anda ingin implementasi)
 * @param {Array} messages - Array berisi history messages
 * @returns {Promise<string>} - Ringkasan chat
 */
export async function getChatSummary(messages) {
  try {
    // Jika Anda ingin implementasi summary, bisa tambahkan endpoint di backend
    // Untuk sementara, return summary sederhana
    if (messages.length === 0) {
      return 'Belum ada percakapan';
    }
    
    const messageCount = messages.filter(m => m.role === 'user').length;
    return `${messageCount} pesan dalam percakapan`;
    
  } catch (error) {
    console.error('Error getting chat summary:', error);
    return 'Ringkasan tidak tersedia';
  }
}

/**
 * Test koneksi ke backend
 * @returns {Promise<boolean>} - True jika koneksi berhasil
 */
export async function testConnection() {
  try {
    // Anda bisa tambahkan endpoint /health di backend untuk test
    await axios.get(`${API_URL}/`);
    return true;
  } catch (error) {
    return false;
  }
}