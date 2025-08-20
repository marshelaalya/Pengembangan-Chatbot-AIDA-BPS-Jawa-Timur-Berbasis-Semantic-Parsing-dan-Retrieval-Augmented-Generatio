<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import Typed from 'typed.js';
import { useRouter } from 'vue-router';

// Example components
import NavbarDefault from '../../examples/navbars/NavbarDefault.vue';
import DefaultFooter from '../../examples/footers/FooterDefault.vue';
import Header from '../../examples/Header.vue';

// Sections
import LayananKhusus from './Components/LayananKhusus.vue';
import JenisLayanan from './Components/JenisLayanan.vue';

// Images
import bg0 from '@/assets/img/bg9.jpg';
import misterj from '@/assets/img/misterj.svg';

// State
const searchQuery = ref('');
const router = useRouter();

// Hooks
const body = document.getElementsByTagName('body')[0];

onMounted(() => {
  body.classList.add('presentation-page', 'bg-gray-200');

  if (document.getElementById('typed')) {
    new Typed('#typed', {
      stringsElement: '#typed-strings',
      typeSpeed: 90,
      backSpeed: 90,
      backDelay: 200,
      startDelay: 500,
      loop: true,
    });
  }
  
  // Tampilkan popup setelah 3 detik
  setTimeout(() => {
    showPopup.value = true;
    // Hapus baris ini karena sudah tidak digunakan
    popupType.value = 'image'; // atau 'video'
  }, 3000);
});

onUnmounted(() => {
  body.classList.remove('presentation-page', 'bg-gray-200');
});

// Methods
const search = () => {
  if (searchQuery.value.trim()) {
    router.push({ name: 'search', query: { searchQuery: searchQuery.value.trim() } });
  }
};

// State untuk popup
const showPopup = ref(false);
const currentPopupIndex = ref(0);

// Data popup
const popupContents = [
  {
    type: 'video',
    content: 'https://www.youtube.com/embed/tgDOmtPniiA'
  },
  {
    type: 'image',
    content: '/assets/popup1.webp'
  }
];

// Method untuk menutup popup
const closePopup = () => {
  showPopup.value = false;
};

// Method untuk slide berikutnya
const nextSlide = () => {
  currentPopupIndex.value = (currentPopupIndex.value + 1) % popupContents.length;
};

// Method untuk slide sebelumnya
const prevSlide = () => {
  currentPopupIndex.value = currentPopupIndex.value === 0 
    ? popupContents.length - 1 
    : currentPopupIndex.value - 1;
};

// Modifikasi onMounted
onMounted(() => {
  body.classList.add('presentation-page', 'bg-gray-200');

  if (document.getElementById('typed')) {
    new Typed('#typed', {
      stringsElement: '#typed-strings',
      typeSpeed: 90,
      backSpeed: 90,
      backDelay: 200,
      startDelay: 500,
      loop: true,
    });
  }
  
  // Tampilkan popup setelah 3 detik
  setTimeout(() => {
    showPopup.value = true;
  }, 3000);
});

// Method untuk menutup popup saat klik di luar konten
const handleOverlayClick = (event) => {
  // Pastikan klik terjadi di overlay, bukan di konten popup
  if (event.target.classList.contains('popup-overlay')) {
    closePopup();
  }
};
</script>

<template>
  <div>
    <div class="container position-sticky z-index-sticky top-0">
      <div class="row">
        <div class="col-12">
          <NavbarDefault :sticky="true" />
        </div>
      </div>
    </div>
    <Header>
      <div
        class="page-header min-vh-75"
        :style="`background-image: url(${bg0})`"
        loading="lazy"
      >
        <span class="mask bg-gradient-dark opacity-2"></span>
        <div class="container">
          <div class="row">
            <div class="col-lg-7 text-center mx-auto position-relative">
              <h1 class="text-white pt-3 mt-n5 me-2" :style="{ display: 'inline-block' }">
                Halo PST BPS Jatim!
              </h1>
              <p class="text-white px-5 mt-1" :style="{ fontWeight: '500' }">
                <i>Saya lagi butuh <span class="text-white" id="typed"></span>, nih </i>🥺 <br />
                <h4 class="text-white font-weight-normal">
                  Tenang! Kami Ada untuk Solusi Data Anda
                </h4>
              </p>
              <div id="typed-strings">
                <h1>data statistik</h1>
                <h1>konsultasi data</h1>
                <h1><s>jodoh</s> ide skripsi</h1>
              </div>
            </div>
            <div class="col-lg-6 mx-auto position-relative">
              <div class="input-group mt-3">
                <input
                  type="text"
                  class="form-control bg-white px-3"
                  placeholder="Cari Data Apa?"
                  aria-label="Recipient's username"
                  aria-describedby="button-addon2"
                  v-model="searchQuery"
                  @keyup.enter="search"
                />
                <button class="btn btn-success" style="margin-bottom: 0;" type="button-lg" id="button-addon2" @click="search">
                  Cari
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Header>

    <div class="card card-body blur shadow-blur mx-3 mx-md-4 mt-n6">
      <JenisLayanan />
      <LayananKhusus />

      <div
        class="container-fluid mt-sm-5 border-radius-xl"
        :style="{ background: 'linear-gradient(195deg, rgb(66, 66, 74), rgb(25, 25, 25))' }"
      >
        <div
          class="page-header py-6 py-md-5 my-sm-3 mb-3 border-radius-xl"
          :style="{ backgroundImage: `url(${misterj})` }"
          loading="lazy"
        >
          <span class="mask bg-gradient-dark" style="opacity: 0;"></span>
          <div class="container">
            <div class="row">
              <div class="d-flex justify-content-center p-5">
                <div class="col-lg-8 ms-lg-5 text-center">
                  <h2 class="text-white">
                    Mister J-Statistik Jatim
                  </h2>
                  <h3 class="text-white text-xl font-weight-normal">
                    Akses berbagai Data Statistik Jawa Timur semudah sentuhan jari
                  </h3>

                  <a
                    href="https://play.google.com/store/search?q=statistik+jatim&c=apps&hl=en&pli=1"
                    class="btn btn-sm mb-0 bg-gradient-success px-3 py-3 mt-4"
                  ><i class="fab fa-google-play text-lg" style="margin-right: 4px;"></i>Download Sekarang</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <DefaultFooter />
  
  <!-- Popup Modal -->
  <div v-if="showPopup" class="popup-overlay" @click="handleOverlayClick">
    <div class="popup-content">
      <button class="popup-close" @click="closePopup">
        <i class="fas fa-times"></i>
      </button>
      
      <!-- Konten Popup -->
      <div v-if="popupContents[currentPopupIndex].type === 'image'" class="popup-image">
        <img :src="popupContents[currentPopupIndex].content" alt="Popup Image">
      </div>
      
      <div v-else-if="popupContents[currentPopupIndex].type === 'video'" class="popup-video">
        <iframe 
          :src="popupContents[currentPopupIndex].content"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen>
        </iframe>
      </div>
  
      <!-- Navigation Buttons -->
      <button class="nav-button prev" @click="prevSlide">
        <i class="fas fa-chevron-left"></i>
      </button>
      <button class="nav-button next" @click="nextSlide">
        <i class="fas fa-chevron-right"></i>
      </button>
    </div>
  </div>

  </div>
</template>

<style scoped>
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  cursor: pointer; /* Tambahkan cursor pointer untuk indikasi bisa diklik */
}

.popup-content {
  position: relative;
  width: 90%;
  max-width: 800px; /* Tambahkan max-width */
  background: white;
  padding: 20px;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-video {
  width: 100%;
  aspect-ratio: 16/9; /* Gunakan aspect ratio untuk menjaga proporsi video */
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  background: #000; /* Tambahkan background hitam */
}

.popup-video iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
}

.popup-image {
  width: 100%;
  height: auto;
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-image img {
  max-width: 100%;
  max-height: 80vh;
  object-fit: contain;
  border-radius: 8px;
}

.popup-close {
  position: absolute;
  top: -15px;
  right: -15px;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #dc3545;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  z-index: 10000;
}

.nav-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.8);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  transition: background-color 0.3s;
}

.nav-button:hover {
  background: rgba(255, 255, 255, 1);
}

.nav-button.prev {
  left: -50px;
}

.nav-button.next {
  right: -50px;
}

.nav-button i {
  color: #000;
  font-size: 20px;
}
</style>
