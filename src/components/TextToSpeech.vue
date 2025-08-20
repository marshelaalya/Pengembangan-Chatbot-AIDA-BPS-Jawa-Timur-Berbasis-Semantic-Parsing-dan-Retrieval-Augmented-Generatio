<template>
  <div class="text-to-speech-container">
    <span class="floating-text">Text to Speech</span>
    <button 
      class="text-to-speech-button"
      @click="handleSpeak"
      :aria-label="isSpeaking ? 'Hentikan membaca' : 'Baca halaman'"
    >
      <span class="icon" role="img" :aria-label="isSpeaking ? 'stop' : 'play'">
        <svg viewBox="0 0 24 24" width="24" height="24">
          <path 
            :d="isSpeaking ? mdiStop : mdiVolumeHigh"
            fill="white"
          />
        </svg>
      </span>
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { mdiVolumeHigh, mdiStop } from '@mdi/js'

const isSpeaking = ref(false)

const handleSpeak = () => {
  if (!isSpeaking.value) {
    window.speechSynthesis.cancel()
    const text = document.body.innerText
    
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = 'id-ID'
    
    utterance.onend = () => {
      isSpeaking.value = false
    }

    window.speechSynthesis.speak(utterance)
    isSpeaking.value = true
  } else {
    window.speechSynthesis.cancel()
    isSpeaking.value = false
  }
}
</script>

<style scoped>
.text-to-speech-container {
  position: fixed;
  bottom: 20px;
  left: 70px;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 1000;
}

.floating-text {
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  margin-bottom: 8px;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s ease;
}

.text-to-speech-container:hover .floating-text {
  opacity: 1;
  transform: translateY(0);
}

.text-to-speech-button {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #0066FF; /* Mengubah warna agar sesuai dengan widget Sienna */
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  transition: all 0.3s ease;
  padding: 0;
}

.text-to-speech-button:hover {
  background-color: #0052cc; /* Warna hover yang lebih gelap */
  transform: scale(1.1);
}

.text-to-speech-button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0,123,255,0.5);
}

.icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
}
</style>