<template>
  <div>
    <NavbarChat
      :action="{
        route: 'javascript:;',
        label: 'Buy Now',
        color: 'btn-white',
      }"
    />
    <div class="chat-layout">
      <Sidebar
        v-if="isSidebarVisible"
        @suggestion-clicked="sendMessageFromSidebar"
        @load-chat="loadChatFromSidebar"
        @new-chat="startNewChat"
        @delete-chat="deleteChat"
        :chats="chats"
      />
      <div class="chat-window">
        <div class="breadcrumb">
          <button @click="toggleSidebar" class="breadcrumb-toggle">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              width="24px"
              height="24px"
            >
              <path d="M0 0h24v24H0z" fill="none" />
              <path d="M3 7h18v2H3z" />
              <path d="M3 15h13.5v2H3z" />
            </svg>
          </button>
          <span
            v-if="chatSummary"
            class="text-bold"
            style="margin-left: 10px"
            >{{ chatSummary }}</span
          >
        </div>
        <div class="messages">
          <div
            v-for="(message, index) in messages"
            :key="index"
            :class="['message', message.role]"
          >
            <img
              :src="message.role == 'user' ? userAvatar : aiAvatar"
              class="avatar"
            />
            <div class="text" v-html="formatMessage(message.content)"></div>
          </div>
          <div v-if="isLoading" class="message ai">
            <img :src="aiAvatar" class="avatar" />
            <div class="text-italic">
              Tunggu sebentar ya, AIDA sedang mengetik...
            </div>
          </div>
        </div>
        <div class="input-box">
          <input
            v-model="userInput"
            @keyup.enter="sendMessage"
            placeholder="Ketik curhatanmu ke Ning AIDA atau ucapkan 'Halo AIDA' untuk memulai percakapan suara..."
            aria-label="Input pesan"
          />
          <button @click="sendMessage" aria-label="Kirim pesan">Kirim</button>
          
          <!-- Tombol untuk input suara dihapus -->
        </div>
        
        <!-- Status indikator untuk mode aksesibilitas -->
        <div class="accessibility-status">
          <div class="status-indicator">
            <span v-if="isListening">Mendengarkan kata kunci "Halo AIDA"</span>
            <span v-else-if="isRecording">Mendengarkan pesan Anda...</span>
            <span v-else-if="isProcessing">AIDA sedang memproses...</span>
            <span v-else-if="isSpeaking">AIDA sedang berbicara...</span>
            <span v-else>Katakan "Halo AIDA" untuk memulai.</span>
          </div>
          
          <!-- Tombol stop/pause text-to-speech -->
          <button 
            v-if="isSpeaking" 
            @click="stopSpeaking" 
            class="stop-speech-btn"
            aria-label="Hentikan pembacaan"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
              <path d="M5.5 3.5A1.5 1.5 0 0 1 7 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5zm5 0A1.5 1.5 0 0 1 12 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5z"/>
            </svg>
            Hentikan Pembacaan
          </button>
        </div>
        
        <!-- Popup notifikasi untuk stop/pause -->
        <div v-if="showStopNotification" class="stop-notification">
          Pembacaan dihentikan
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavbarChat from "@/examples/navbars/NavbarChat.vue";
import Sidebar from "./SidebarChat.vue";
import { getAiResponse, getChatSummary } from "@/api/RagApi.js";
import { apiService } from "@/api/ApiService.js";

export default {
  name: "ChatbotView",
  components: {
    NavbarChat,
    Sidebar,
  },
  data() {
    return {
      userInput: "",
      messages: [],
      chats: [],
      userAvatar: "",
      aiAvatar: "https://res.cloudinary.com/bpsjatim/image/upload/f_auto,q_auto/tzpygq8dcjgr6phg4ny0",
      chatSummary: null,
      isSidebarVisible: true,
      isLoading: false,
      userId: "",
      currentChatId: null,
      isListening: false,
      isRecording: false,
      recognition: null,
      synthesis: null,
      triggerRecognition: null,
      notificationSound: null,
      audioContext: null,
      isProcessing: false,
      isSpacePressed: false,
      accessibilityMode: true, // Mode aksesibilitas selalu aktif
      isSpeaking: false, // Status berbicara
      lastSpokenMessage: null, // Menyimpan pesan terakhir yang dibacakan
      showStopNotification: false, // Status notifikasi pemberhentian pembacaan
    };
  },
  created() {
    this.loadUserFromLocalStorage();
    this.loadChatsFromApi();
    this.initializeAudioContext();
    this.initializeSpeechRecognition();
    this.synthesis = window.speechSynthesis;
    
    // Mulai mendengarkan trigger suara secara otomatis
    this.startListeningForTrigger();
    
    // Tambahkan event listener untuk keyboard shortcuts
    window.addEventListener('keydown', this.handleKeyboardShortcuts);
    
    // Beri tahu pengguna bahwa sistem siap mendengarkan
    setTimeout(() => {
      this.announceAccessibility("AIDA siap mendengarkan");
    }, 2000);
  },
  beforeUnmount() {
    // Hapus event listener saat komponen dihapus
    window.removeEventListener('keydown', this.handleKeyboardShortcuts);
  },
  methods: {
    initializeAudioContext() {
      try {
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        
        // Membuat suara notifikasi yang lebih ramah
        this.notificationSound = {
          play: () => {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            // Membuat nada yang lebih lembut
            oscillator.type = 'sine';
            oscillator.frequency.setValueAtTime(1200, this.audioContext.currentTime);
            oscillator.frequency.setValueAtTime(800, this.audioContext.currentTime + 0.2);
            
            gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
            gainNode.gain.linearRampToValueAtTime(0.3, this.audioContext.currentTime + 0.1);
            gainNode.gain.linearRampToValueAtTime(0, this.audioContext.currentTime + 0.3);
            
            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 0.3);
          }
        };
      } catch (error) {
        console.error('Error initializing audio context:', error);
      }
    },
    async initializeSpeechRecognition() {
      if ('webkitSpeechRecognition' in window) {
        // Recognition untuk trigger kata kunci
        this.triggerRecognition = new webkitSpeechRecognition();
        this.triggerRecognition.continuous = true;
        this.triggerRecognition.interimResults = false;
        this.triggerRecognition.lang = 'id-ID';
    
        this.triggerRecognition.onstart = () => {
          this.isListening = true;
          console.log('Mendengarkan trigger kata kunci...');
          
          // Beri tahu pengguna tuna netra bahwa sistem sedang mendengarkan
          if (!this.isSpeaking) {
            this.announceAccessibility("Mode mendengarkan aktif. Katakan Halo AIDA untuk memulai percakapan.");
          }
        };
    
        this.triggerRecognition.onresult = async (event) => {
          const transcript = event.results[event.results.length - 1][0].transcript.toLowerCase();
          console.log('Trigger terdeteksi:', transcript);
          
          if (transcript.includes('halo aida')) {
            this.triggerRecognition.stop();
            this.notificationSound.play();
            
            // Beri tahu pengguna tuna netra bahwa trigger terdeteksi
            this.announceAccessibility(" ");
            
            // Tambahkan input pengguna ke riwayat chat
            this.messages.push({ role: "user", content: "Halo AIDA" });
            this.isLoading = true;
            this.isProcessing = true;
    
            try {
              // Gunakan getAiResponse dari GeminiApi.js
              const aiResponse = await getAiResponse(this.messages);
              this.messages.push({ role: "ai", content: aiResponse });
              
              // Nonaktifkan recognition sementara saat berbicara
              await this.speakText(aiResponse);
              
              this.isLoading = false;
              this.isProcessing = false;
              this.saveMessages();
              
              // Mulai mode percakapan setelah respons selesai
              console.log("Memulai input suara setelah respons AI...");
              setTimeout(() => {
                this.startVoiceInput();
              }, 1000);
            } catch (error) {
              console.error("Error mendapatkan respons AI:", error);
              this.messages.push({
                role: "ai",
                content: "Maaf, terjadi kesalahan saat mendapatkan respons.",
              });
              this.isLoading = false;
              this.isProcessing = false;
              this.startVoiceInput(); // Langsung mulai input suara, bukan kembali ke trigger
            }
          }
        };

        // Recognition untuk input pesan
        this.recognition = new webkitSpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.lang = 'id-ID';
    
        this.recognition.onstart = () => {
          this.isRecording = true;
          
          // Beri tahu pengguna tuna netra bahwa sistem siap menerima input suara
          this.announceAccessibility("Silakan bicara sekarang.");
        };
    
        this.recognition.onresult = async (event) => {
          const transcript = event.results[0][0].transcript;
          console.log('Pesan yang diterima:', transcript);
          
          // Tambahkan pesan ke riwayat chat
          this.messages.push({ role: "user", content: transcript });
          this.isLoading = true;
          this.isProcessing = true;
          
          try {
            // Gunakan getAiResponse dari GeminiApi.js
            const aiResponse = await getAiResponse(this.messages);
            this.messages.push({ role: "ai", content: aiResponse });
            
            // Selesaikan proses loading dan simpan pesan terlebih dahulu
            this.isLoading = false;
            this.saveMessages();
            
            // Nonaktifkan recognition sementara saat berbicara
            // Pastikan text-to-speech hanya bekerja setelah respons AI selesai dihasilkan
            await this.speakText(aiResponse);
            
            this.isProcessing = false;
            
            // Mulai mendengarkan lagi setelah selesai berbicara
            console.log("Memulai input suara setelah respons AI...");
            setTimeout(() => {
              this.startVoiceInput();
            }, 1000);
          } catch (error) {
            console.error("Error mendapatkan respons AI:", error);
            this.messages.push({
              role: "ai",
              content: "Maaf, terjadi kesalahan saat mendapatkan respons.",
            });
            this.isLoading = false;
            this.isProcessing = false;
            this.startVoiceInput();
          }
        };
    
        this.recognition.onend = () => {
          this.isRecording = false;
          if (!this.isProcessing) {
            this.startVoiceInput();
          }
        };
      }
    },

    async speakText(text) {
      if (this.synthesis && this.audioContext) {
        return new Promise((resolve) => {
          // Set flag bahwa sedang berbicara
          this.isSpeaking = true;
          
          // Matikan mikrofon sebelum berbicara
          if (this.recognition) {
            this.recognition.abort();
            this.recognition.stop();
          }
          if (this.triggerRecognition) {
            this.triggerRecognition.abort();
            this.triggerRecognition.stop();
          }

          // Hitung delay berdasarkan panjang teks
          const charPerSecond = 15;
          const minDelay = 2;
          const calculatedDelay = Math.max(minDelay, Math.ceil(text.length / charPerSecond));
          
          // Buat audio context baru untuk routing audio
          const audioContext = new (window.AudioContext || window.webkitAudioContext)();
          const destination = audioContext.createMediaStreamDestination();
          
          // Buat gain node untuk mengontrol volume
          const gainNode = audioContext.createGain();
          gainNode.gain.value = 1.0; // Volume maksimal
          
          // Sambungkan ke output speaker
          gainNode.connect(audioContext.destination);
          
          this.isProcessing = true;
          this.synthesis.cancel();
          
          const cleanText = this.cleanTextForSpeech(text);
          this.lastSpokenMessage = cleanText; // Simpan pesan terakhir yang dibacakan
          
          const utterance = new SpeechSynthesisUtterance(cleanText);
          utterance.lang = 'id-ID';
          utterance.rate = 0.9; // Sedikit lebih lambat untuk mode aksesibilitas
          utterance.pitch = 1.0;
          utterance.volume = 1.0;
          
          // Pilih suara wanita Indonesia jika tersedia
          const voices = this.synthesis.getVoices();
          const indonesianVoice = voices.find(voice => 
            voice.lang.includes('id-ID') && voice.name.includes('Female')
          );
          
          if (indonesianVoice) {
            utterance.voice = indonesianVoice;
          }
          
          // Tambahkan audio processing
          utterance.onstart = () => {
            this.isProcessing = true;
            this.isRecording = false;
            this.isSpeaking = true;
            
            // Pastikan mikrofon benar-benar mati
            if (this.recognition) this.recognition.abort();
            if (this.triggerRecognition) this.triggerRecognition.abort();
          };
          
          utterance.onend = () => {
            console.log('Selesai berbicara');
            
            // Bersihkan resources audio
            audioContext.close();
            
            setTimeout(() => {
              this.isProcessing = false;
              this.isSpeaking = false;
              
              // Dalam mode aksesibilitas, selalu kembali ke mode mendengarkan
              this.startListeningForTrigger();
            }, calculatedDelay * 1000);
            
            resolve();
          };

          utterance.onerror = (event) => {
            console.error('Error saat berbicara:', event);
            audioContext.close();
            this.isProcessing = false;
            this.isSpeaking = false;
            resolve();
          };
          
          // Tambahkan event listener untuk memastikan suara dimuat
          window.speechSynthesis.onvoiceschanged = () => {
            const voices = window.speechSynthesis.getVoices();
            const indonesianVoice = voices.find(voice => 
              voice.lang.includes('id-ID') && voice.name.includes('Female')
            );
            if (indonesianVoice) {
              utterance.voice = indonesianVoice;
            }
          };
          
          this.synthesis.speak(utterance);
        });
      }
    },
    
    // Fungsi untuk membersihkan teks sebelum dibacakan
    cleanTextForSpeech(text) {
      if (!text) return "";
      
      // Hapus markdown dan kode
      let cleanText = text
        .replace(/```[\s\S]*?```/g, "Terdapat blok kode di sini.") // Ganti code blocks
        .replace(/`([^`]+)`/g, "$1") // Hapus inline code formatting
        .replace(/\*\*([^*]+)\*\*/g, "$1") // Hapus bold formatting
        .replace(/\*([^*]+)\*/g, "$1") // Hapus italic formatting
        .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1") // Ganti links dengan teks saja
        // Hapus semua tag HTML
        .replace(/<\/?(?:ol|ul|li|a|p|strong|em|div|span|br|hr|h[1-6]|table|tr|td|th|thead|tbody|code|pre|blockquote|img|figure|figcaption|video|audio|source|iframe)[^>]*>/gi, "") 
        // Hapus atribut HTML seperti href, class, id, dll
        .replace(/ [a-z\-]+="[^"]*"/gi, "")
        // Hapus tag HTML yang tersisa
        .replace(/<[^>]*>/g, "")
        // Hapus entitas HTML
        .replace(/&[a-z]+;/gi, " ")
        .replace(/\n\n/g, ". ") // Ganti double newlines dengan titik dan spasi
        .replace(/\n/g, ". ") // Ganti single newlines dengan titik dan spasi
        .replace(/\s+/g, " ") // Hapus multiple spaces
        .trim();
      
      return cleanText;
    },
    
    // Fungsi untuk mengumumkan pesan aksesibilitas tanpa mengganggu percakapan
    announceAccessibility(message) {
      // Jangan mengumumkan jika sedang berbicara
      if (this.isSpeaking) return;
      
      const utterance = new SpeechSynthesisUtterance(message);
      utterance.lang = 'id-ID';
      utterance.rate = 1.0;
      utterance.volume = 0.8; // Sedikit lebih pelan dari pesan utama
      
      // Pilih suara wanita Indonesia jika tersedia
      const voices = this.synthesis.getVoices();
      const indonesianVoice = voices.find(voice => 
        voice.lang.includes('id-ID') && voice.name.includes('Female')
      );
      
      if (indonesianVoice) {
        utterance.voice = indonesianVoice;
      }
      
      this.synthesis.speak(utterance);
    },
    
    startListeningForTrigger() {
      if (this.triggerRecognition && !this.isProcessing && !this.isSpeaking) {
        this.isListening = true;
        try {
          this.triggerRecognition.start();
          console.log('Mendengarkan trigger kata kunci...');
        } catch (error) {
          console.error('Error starting trigger recognition:', error);
          setTimeout(() => this.startListeningForTrigger(), 1000);
        }
      } else {
        console.log('Tidak dapat memulai pengenalan suara: sedang memproses atau berbicara');
        // Coba lagi setelah beberapa detik jika sedang memproses atau berbicara
        if (this.isProcessing || this.isSpeaking) {
          setTimeout(() => this.startListeningForTrigger(), 3000);
        }
      }
    },
    
    startVoiceInput() {
      if (this.recognition && !this.isProcessing && !this.isSpeaking) {
        setTimeout(() => {
          this.isRecording = true;
          try {
            this.recognition.start();
            console.log('Mikrofon aktif, silakan bicara...');
            // Tambahkan notifikasi suara untuk memberi tahu pengguna
            this.notificationSound.play();
            this.announceAccessibility("Silakan bicara sekarang.");
          } catch (error) {
            console.error('Error starting voice input:', error);
            this.isRecording = false;
            
            // Coba lagi memulai input suara setelah beberapa saat
            setTimeout(() => this.startVoiceInput(), 1000);
          }
        }, 1000); // Kurangi delay menjadi 1 detik agar lebih responsif
      } else {
        console.log('Tidak dapat memulai input suara: sedang memproses atau berbicara');
        // Coba lagi memulai input suara setelah beberapa saat
        setTimeout(() => this.startVoiceInput(), 2000);
      }
    },
    
    // Ulangi pesan terakhir
    repeatLastMessage() {
      if (this.lastSpokenMessage && !this.isSpeaking) {
        this.speakText(this.lastSpokenMessage);
      }
    },
    
    // Fungsi untuk menghentikan pembacaan text-to-speech
    stopSpeaking() {
      if (this.synthesis) {
        this.synthesis.cancel();
        this.isSpeaking = false;
        this.isProcessing = false;
        
        // Tampilkan notifikasi pemberhentian
        this.showStopNotification = true;
        setTimeout(() => {
          this.showStopNotification = false;
        }, 2000);
        
        // Mulai mendengarkan lagi dalam mode percakapan, bukan mode trigger
        setTimeout(() => {
          this.startVoiceInput();
        }, 1000);
      }
    },
    
    // Keyboard shortcuts
    handleKeyboardShortcuts(event) {
      // Alt+R untuk mengulang pesan terakhir
      if (event.altKey && event.key === 'r') {
        this.repeatLastMessage();
      }
    },
    
    async sendMessage() {
      const message = this.userInput.trim();
      if (!message) return;

      this.messages.push({ role: "user", content: message });
      this.userInput = "";
      this.isLoading = true;
      this.isProcessing = true;
      
      // Membacakan pesan proses
      this.speakText("Jawaban sedang diproses mohon tunggu sebentar");
      
      try {
        const aiResponse = await getAiResponse(this.messages);
        this.messages.push({ role: "ai", content: aiResponse });
        this.isLoading = false;
        this.isProcessing = false;
        
        // Membacakan respons AI
        this.speakText(aiResponse);
        
        this.saveMessages();
      } catch (error) {
        console.error("Error fetching AI response:", error);
        this.messages.push({
          role: "ai",
          content: "Maaf, terjadi kesalahan dalam mendapatkan respons.",
        });
        this.isLoading = false;
        this.isProcessing = false;
        
        this.speakText("Maaf, terjadi kesalahan dalam mendapatkan respons.");
        this.startListeningForTrigger();
        
        this.saveMessages();
      }
    },
    
    loadUserFromLocalStorage() {
      const storedUser = localStorage.getItem("user");
      const storedLoggedIn = localStorage.getItem("loggedIn");

      if (storedUser && storedLoggedIn) {
        const parsedUser = JSON.parse(storedUser);
        this.userAvatar = parsedUser.foto;
        this.userId = parsedUser.id;
      }
    },
    async loadChatsFromApi() {
      try {
        const response = await apiService.getAidaByUser(this.userId);
        if (Array.isArray(response.data.data)) {
          this.chats = response.data.data.map((chat) => ({
            id: chat.id,
            summary: chat.resume,
            messages: JSON.parse(chat.conversation),
          }));
          if (this.chats.length > 0) {
            this.loadChatFromSidebar(this.chats[0]);
          }
        } else {
          console.error("Unexpected response format:", response.data);
        }
      } catch (error) {
        console.error("Error fetching chats:", error);
      }
    },
    toggleSidebar() {
      this.isSidebarVisible = !this.isSidebarVisible;
    },
    async sendMessageFromSidebar(message) {
      this.messages.push({ role: "user", content: message });
      this.isLoading = true;
      try {
        const aiResponse = await getAiResponse(this.messages);
        this.messages.push({ role: "ai", content: aiResponse });
        this.isLoading = false;
        
        // Membacakan respons
        this.speakText(aiResponse);
        
        this.saveMessages();
      } catch (error) {
        console.error("Error fetching AI response:", error);
        this.messages.push({
          role: "ai",
          content: "Sorry, there was an error getting the response.",
        });
        this.isLoading = false;
        
        this.speakText("Maaf, terjadi kesalahan dalam mendapatkan respons.");
        
        this.saveMessages();
      }
    },
    async saveMessages() {
      try {
        const chatSummary = await this.getChatSummaryIfNotExists();
        const conversation = {
          resume: chatSummary,
          conversation: JSON.stringify(this.messages),
          id_pengguna: this.userId,
        };
        if (this.currentChatId) {
          await apiService.updateAidaConversation(this.currentChatId, conversation);
        } else {
          const response = await apiService.addAida(conversation);
          this.currentChatId = response.data.id;
        }
        await this.updateChatHistories(chatSummary);
      } catch (error) {
        console.error("Error saving messages:", error);
      }
    },
    async getChatSummaryIfNotExists() {
      if (!this.chatSummary && this.messages.length > 0) {
        try {
          this.chatSummary = await getChatSummary(this.messages);
        } catch (error) {
          console.error("Error fetching chat summary:", error);
          this.chatSummary = "Conversation Summary";
        }
      }
      return this.chatSummary;
    },
    loadChatFromSidebar(chat) {
      this.messages = chat.messages;
      this.chatSummary = chat.summary;
      this.currentChatId = chat.id; // Set current chat ID
      
      // Beri tahu pengguna tentang chat yang dimuat
      const announcement = `Chat dimuat: ${this.chatSummary || 'Percakapan baru'}`;
      this.announceAccessibility(announcement);
    },
    async startNewChat() {
      // Hentikan text-to-speech jika sedang berbicara
      if (this.isSpeaking) {
        this.stopSpeaking();
      }
      
      this.messages = [];
      this.chatSummary = null;
      this.currentChatId = null; // Reset current chat ID for new chat
      
      // Beri tahu pengguna tentang chat baru
      this.announceAccessibility("Percakapan baru dimulai. Katakan Halo AIDA untuk memulai.");
    },
    async deleteChat(chatId) {
      try {
        // Hentikan text-to-speech jika sedang berbicara
        if (this.isSpeaking) {
          this.stopSpeaking();
        }
        
        await apiService.deleteAidaConversation(chatId);
        this.chats = this.chats.filter((chat) => chat.id !== chatId);
        
        // Beri tahu pengguna tentang penghapusan chat
        this.announceAccessibility("Chat berhasil dihapus.");
        
        if (this.chats.length == 0) {
          this.startNewChat();
        } else {
          this.loadChatFromSidebar(this.chats[0]);
        }
      } catch (error) {
        console.error("Error deleting chat:", error);
        
        this.announceAccessibility("Terjadi kesalahan saat menghapus chat.");
      }
    },
    async updateChatHistories(chatSummary) {
      const newChat = { summary: chatSummary, messages: this.messages, id: this.currentChatId };
      this.chats = [
        newChat,
        ...this.chats.filter((chat) => chat.id !== this.currentChatId),
      ];
    },
    formatMessage(message) {
      if (typeof message !== 'string') {
        return '';
      }
      
      // Handle code blocks dengan syntax highlighting
      message = message.replace(/```(\w+)?\n([\s\S]*?)```/g, function(match, language, code) {
        const lang = language || 'plaintext';
        const escapedCode = code
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          .trim();
        
        return `<div class="code-block"><div class="code-header">${lang}</div><pre><code class="language-${lang}">${escapedCode}</code></pre></div>`;
      });
      
      // Handle inline code
      message = message.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
      
      // Handle markdown formatting
      message = message.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
      message = message.replace(/\*(.*?)\*/g, "<em>$1</em>");
      message = message.replace(/\n/g, "<br>");
      
      // Handle links
      message = message.replace(
        /\[([^\]]+)\]\(([^)]+)\)/g,
        '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>'
      );
      
      // Handle numbered lists
      message = message.replace(/^\d+\.\s/gm, (match) => `<br>${match}`);
      
      return message;
    }
  },
};
</script>


<style scoped>

.chat-layout {
  display: flex;
  height: 100vh;
}

.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: white;
  height: 100vh;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  box-sizing: border-box;
}

.message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
}

.message.user {
  justify-content: flex-end;
}

.message.ai {
  justify-content: flex-start;
}

.message.user .avatar {
  order: 2;
  margin-left: 10px;
}

.message.ai .avatar {
  margin-right: 10px;
}

.message.user .text {
  background-color: #1a73e8;  /* Ganti dengan warna biru yang lebih kontras */
  color: #ffffff; /* Teks putih untuk kontras lebih baik */
}

.message.ai .text {
  background-color: #f8f9fa; /* Background lebih terang */
  color: #202124; /* Teks hitam untuk kontras lebih baik */
  border: 1px solid #dadce0;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.text {
  max-width: 70%;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  white-space: pre-wrap;
}

.input-box {
  display: flex;
  padding: 10px;
  background-color: #f1f5f9;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
  position: sticky;
  bottom: 0;
}

input {
  flex: 1;
  padding: 10px;
  border: 1px solid #cbd5e1;
  border-radius: 5px;
  margin-right: 10px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.breadcrumb {
  display: flex;
  align-items: center;
  padding: 4px;
  background-color: #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.breadcrumb-toggle {
  background: #007bff;
  border: none;
  cursor: pointer;
}

/* Status indikator untuk mode aksesibilitas */
.accessibility-status {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 16px;
  background-color: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  margin-top: 10px;
}

.status-indicator {
  font-size: 14px;
  color: #666;
}

.stop-speech-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.stop-speech-btn:hover {
  background-color: #c0392b;
}

.stop-notification {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 14px;
  z-index: 1000;
  animation: fadeInOut 2s ease-in-out;
}

@keyframes fadeInOut {
  0% { opacity: 0; }
  20% { opacity: 1; }
  80% { opacity: 1; }
  100% { opacity: 0; }
}

.status-indicator {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 4px;
  background-color: #e0f2fe;
  color: #0369a1;
}

@media (max-width: 768px) {
  .chat-layout {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
  }

  .chat-window {
    height: calc(100vh - 50px);
  }

  .loading-spinner {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}

/* Perbaikan untuk heading dan teks */
.message .text {
  max-width: 70%;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  white-space: pre-wrap;
  font-size: 14px;
  line-height: 1.6;
}

.message .text h1,
.message .text h2,
.message .text h3,
.message .text h4,
.message .text h5,
.message .text h6 {
  color: #1a1a1a;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
  line-height: 1.3;
}

.message .text h1 { font-size: 1.75em; }
.message .text h2 { font-size: 1.5em; }
.message .text h3 { font-size: 1.25em; }
.message .text h4 { font-size: 1.1em; }
.message .text h5,
.message .text h6 { font-size: 1em; }

/* Perbaikan untuk code block dan syntax highlighting */
.code-block {
  background: #282a36; /* Background Dracula theme */
  border-radius: 8px;
  margin: 1rem 0;
  overflow: hidden;
  font-family: 'Fira Code', monospace;
}

.code-header {
  background: #44475a;
  color: #f8f8f2;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  border-bottom: 1px solid #6272a4;
  font-weight: 500;
}

.code-block pre {
  margin: 0;
  padding: 1rem;
  overflow-x: auto;
  background: inherit;
}

.code-block code {
  font-family: 'Fira Code', monospace;
  font-size: 14px;
  line-height: 1.6;
  color: #f8f8f2; /* Warna teks terang */
  white-space: pre-wrap;
  word-wrap: break-word;
  text-shadow: none;
}

/* Universal syntax highlighting untuk semua bahasa */
.code-block .language-r,
.code-block .language-python,
.code-block .language-javascript,
.code-block .language-java,
.code-block .language-cpp,
.code-block .language-php,
.code-block .language-sql,
.code-block .language-plaintext {
  display: block;
  color: #f8f8f2; /* Warna teks dasar terang */
  background: transparent!important;
}

/* Syntax highlighting universal */
.code-block {
  /* Keywords, Control Flow, Built-in */
  .keyword,
  .control-flow,
  .builtin { 
    color: #ff79c6 !important; /* Pink terang */
  }
  
  /* String, Text */
  .string,
  .char { 
    color: #f1fa8c !important; /* Kuning terang */
  }
  
  /* Numbers, Values */
  .number,
  .boolean,
  .constant { 
    color: #bd93f9 !important; /* Ungu terang */
  }
  
  /* Comments */
  .comment { 
    color: #6272a4 !important; /* Biru keabu-abuan */
  }
  
  /* Functions, Methods */
  .function,
  .method { 
    color: #50fa7b !important; /* Hijau terang */
  }
  
  /* Operators, Symbols */
  .operator,
  .punctuation { 
    color: #ff79c6 !important; /* Pink terang */
  }
  
  /* Variables, Parameters */
  .variable,
  .parameter { 
    color: #8be9fd !important; /* Cyan terang */
  }
  
  /* Classes, Types */
  .class-name,
  .type { 
    color: #ffb86c !important; /* Orange terang */
  }
}

/* Inline code */
.inline-code {
  background: #282a36;
  color: #f8f8f2;
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-family: 'Fira Code', monospace;
  font-size: 0.9em;
}

/* Scrollbar */
.code-block pre::-webkit-scrollbar {
  height: 8px;
  width: 8px;
}

.code-block pre::-webkit-scrollbar-track {
  background: #282a36;
  border-radius: 4px;
}

.code-block pre::-webkit-scrollbar-thumb {
  background: #6272a4;
  border-radius: 4px;
}

.code-block pre::-webkit-scrollbar-thumb:hover {
  background: #44475a;
}
</style>