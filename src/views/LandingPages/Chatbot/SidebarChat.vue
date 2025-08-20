<template>
  <div class="sidebar">
    <img class="logo" src="/assets/aida.png" alt="Logo" />
    <hr class="hairline" />
    <div class="note">
      AIDA dapat membuat kesalahan dan memberikan informasi yang kurang akurat. Tetap mengacu pada Website BPS atau gunakan menu Konsultasi untuk informasi yang lebih rinci.
    </div>
    <button class="new-chat-button" @click="startNewChat">Obrolan Baru</button>
    <div class="chat-history">
      <h3>Kenangan bersama AIDA:</h3>
      <ul>
        <li v-for="(chat, index) in chats" :key="index">
          <span @click="loadChat(chat)">{{ chat.summary }}</span>
          <button class="delete-chat-button" @click="deleteChat(chat.id)">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="16px" height="16px">
              <path d="M0 0h24v24H0z" fill="none"/>
              <path d="M16 9v10H8V9h8m-1.5-6h-5l-1 1H5v2h14V4h-4.5l-1-1zM18 9H6v11c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V9z"/>
            </svg>
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SidebarChat',
  props: ['chats'],
  methods: {
    loadChat(chat) {
      this.$emit('load-chat', chat);
    },
    startNewChat() {
      this.$emit('new-chat');
    },
    deleteChat(index) {
      this.$emit('delete-chat', index);
    }
  }
};
</script>

<style scoped>
.sidebar {
  width: 300px;
  background-color: #f1f5f9;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  box-sizing: border-box;
}

.logo {
  width: 100%;
  height: auto;
  margin-bottom: 10px;
}

.hairline {
  width: 100%;
  margin: 5px;
  border: 0;
  border-top: 1px solid #cbd5e1;
}

.note {
  font-size: 12px;
  color: #6b7280;
  text-align: center;
  margin-bottom: 20px;
  padding: 0 10px;
}

.new-chat-button {
  font-size: 11pt;
  margin-bottom: 15px;
  padding: 8px;
  width: 75%;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
}

.new-chat-button:hover {
  background-color: #218838;
}

.chat-history {
  width: 100%;
  overflow-y: auto;
  max-height: 70vh;
}

.chat-history h3 {
  font-size: 12pt;
  font-weight: 500;
  text-align: center;
  margin-bottom: 10px;
}

.chat-history ul {
  font-size: 11pt;
  list-style-type: none;
  padding: 0;
}

.chat-history li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  margin-bottom: 10px;
  padding: 10px;
  background-color: #e2e8f0;
  border-radius: 5px;
}

.chat-history li:hover {
  background-color: #cbd5e1;
}

.delete-chat-button {
  background-color: red;
  border: none;
  border-radius: 5px;
  padding: 5px;
  cursor: pointer;
}

.delete-chat-button svg {
  fill: white;
  width: 16px;
  height: 16px;
}

@media (max-width: 768px) {
  .logo {
    display: none;
  }
  .sidebar {
    width: 100%;
  }
  .chat-history {
    max-height: 50vh;
  }
}
</style>
