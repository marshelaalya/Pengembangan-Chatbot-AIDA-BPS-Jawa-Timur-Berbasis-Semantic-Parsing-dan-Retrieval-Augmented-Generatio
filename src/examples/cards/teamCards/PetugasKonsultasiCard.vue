<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { GoogleGenerativeAI } from '@google/generative-ai';
import MaterialBadge from "../../../components/MaterialBadge.vue";
import Modal from "../../../views/LandingPages/Konsultasi/Sections/RsvpModal.vue";
import { marked } from 'marked';

// Mendefinisikan props
const props = defineProps({
  petugas: {
    type: Object,
    required: true,
    id: Number,
    nama_panggilan: String,
    email_bps: String,
    id_satker: String,
    jabatan: String,
    foto: String,
    satker: Object,
    keahlian: Array,
    jenis_kelamin: Number,
  },
});

// Mendefinisikan data dan methods
const isModalVisible = ref(false);
const isLoading = ref(false);
const isSuccess = ref(false);
const isModalMainVisible = ref(true);
const user = ref(JSON.parse(localStorage.getItem("user")) || {});
const router = useRouter();

// Tambahan untuk tooltip
const showTooltip = ref(false);
const tooltipText = ref('');
const isLoadingTooltip = ref(false);

// Fungsi untuk mendapatkan rekomendasi dari Gemini API
async function getRecommendation() {
  if (!props.petugas.keahlian.length) return;
  
  isLoadingTooltip.value = true;
  showTooltip.value = true;
  
  try {
    const keahlianList = props.petugas.keahlian.map(k => k.nama_keahlian).join(', ');
    const prompt = `Berdasarkan keahlian berikut: ${keahlianList}, buatkan rekomendasi singkat (maksimal 50 kata) untuk memilih petugas ini dengan format "Pilih saya jika Anda butuh data/informasi tentang..." Sertakan juga potensi topik penelitian terkait bidang tersebut.`;
    
    const genAI = new GoogleGenerativeAI('AIzaSyClh5eZ4Q-NBMFia1tbDv_ob3ewbs66N2U');
    const model = genAI.getGenerativeModel({ model: 'gemini-2.0-flash' });
    
    const result = await model.generateContent(prompt);
    const response = await result.response;
    const markdownText = response.text();
    tooltipText.value = marked(markdownText);
  } catch (error) {
    console.error('Error getting recommendation:', error);
    tooltipText.value = 'Maaf, terjadi kesalahan saat memuat rekomendasi.';
  } finally {
    isLoadingTooltip.value = false;
  }
}

// Computed property untuk menambahkan 'cak' atau 'ning' berdasarkan jenis kelamin
const namaLengkap = computed(() => {
  if (props.petugas.jenis_kelamin == 1) {
    return `Cak ${props.petugas.nama_panggilan}`;
  } else if (props.petugas.jenis_kelamin == 2) {
    return `Ning ${props.petugas.nama_panggilan}`;
  }
  return props.petugas.nama_panggilan;
});

function showModal() {
  const isLogin = localStorage.getItem("loggedIn");
  if (isLogin == "true") {
    isModalVisible.value = true;
    isModalMainVisible.value = true;
  } else {
    router.push({ name: "login" });
  }
}

function closeModal() {
  isModalVisible.value = false;
}

function setLoading(value) {
  isLoading.value = value;
}

function setSuccess(value) {
  isSuccess.value = value;
}

function hideMainModal() {
  isModalMainVisible.value = false;
}

function closeSuccessModal() {
  isSuccess.value = false;
  router.push({ name: "CardBooking" });
}
</script>

<template>
  <div class="card card-profile">
    <div 
      class="helper-icon"
      @mouseenter="getRecommendation()"
    >
      <i class="material-icons">help_outline</i>
    </div>

    <!-- Tooltip content -->
    <div v-if="showTooltip || isLoadingTooltip" class="helper-tooltip">
      <div class="helper-tooltip-header">
        <h6 class="mb-0">Rekomendasi Petugas</h6>
        <button class="close-button" @click="showTooltip = false">
          <i class="material-icons">close</i>
        </button>
      </div>
      <div class="helper-tooltip-body">
        <div v-if="isLoadingTooltip" class="d-flex justify-content-center p-2">
          <div class="spinner-border spinner-border-sm text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        <p v-else class="recommendation-text" style="font-size:small" v-html="tooltipText"></p>
      </div>
    </div>

    <div class="row">
      <div class="col-lg-4 col-md-6 col-12 mt-n5">
        <div class="p-3 pe-md-0">
          <img class="w-100 border-radius-md shadow-lg" :src="petugas.foto" :alt="namaLengkap" />
        </div>
      </div>
      <div class="col-lg-8 col-md-6 col-12 my-auto">
        <div class="card-body ps-lg-0">
          <h6 class="mb-0">{{ namaLengkap }}</h6>
          <p class="text-weight-bold text-sm mb-0 text-success">{{ petugas.satker.nama_satker }}</p>
          <p class="mb-2 text-xs">
            <i class="fa fa-briefcase text-xs margin-right-4"></i>
            {{ petugas.jabatan }}
          </p>
          <div class="col-lg-12">
            <MaterialBadge
              color="gray-300"
              class="mb-1 text-dark opacity-6"
              style="margin-right: 2px; text-transform: none"
              v-for="topik in petugas.keahlian"
              :key="topik.id"
            >
              {{ topik.nama_keahlian }}
            </MaterialBadge>
          </div>
          <div class="col-lg-12">
            <a @click="showModal" class="btn btn-sm bg-gradient-danger mt-2 mb-0" style="text-transform: none">
              Buat Reservasi
            </a>
          </div>
        </div>
      </div>
    </div>
    <Modal
      v-if="isModalVisible"
      @close="closeModal"
      @loading="setLoading"
      @success="setSuccess"
      @hideMainModal="hideMainModal"
      :petugas="petugas"
      :pengguna="user"
      :isModalMainVisible="isModalMainVisible"
    />
    <!-- Modal Loading -->
    <div v-if="isLoading" class="modal-backdrop">
      <div class="modal position-static d-block p-4 py-md-5">
        <div class="modal-dialog" role="document">
          <div class="modal-content rounded-4 shadow px-2">
            <div class="modal-body py-5">
              <div class="d-flex justify-content-center align-items-center">
                <div class="spinner-border text-success" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <span class="ms-3">Mengirim reservasi...</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Success -->
    <div v-if="isSuccess" class="modal-backdrop">
      <div class="modal position-static d-block p-4 py-md-5">
        <div class="modal-dialog" role="document">
          <div class="modal-content rounded-4 shadow px-2">
            <div class="modal-body py-5">
              <div class="d-flex justify-content-center align-items-center">
                <i class="bi bi-check-circle text-success" style="font-size: 2rem"></i>
                <span class="ms-3 fs-5">Reservasi berhasil dikirim.</span>
              </div>
              <div class="d-flex justify-content-center mt-1">
                <span class="fw-semibold text-center">Dimohon untuk memeriksa inbox email anda secara berkala</span>
              </div>
              <div class="d-flex justify-content-center mt-3">
                <button type="button" class="btn btn-success" @click="closeSuccessModal">
                  Tutup
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.helper-icon {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 10;
  cursor: pointer;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  transition: color 0.3s ease;
}

.helper-icon:hover {
  color: #000;
}

.helper-tooltip {
  position: absolute;
  top: 40px;
  right: 10px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  width: 280px;
  z-index: 1000;
  overflow: hidden;
  max-height: 400px;
}

.helper-tooltip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-bottom: 1px solid #eee;
  background: #008cff;
}

.helper-tooltip-header h6 {
  font-size: 0.875rem;
  color: #ffffff;
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  padding: 4px;
  cursor: pointer;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.close-button:hover {
  color: #000;
  background: rgba(0, 0, 0, 0.05);
}

.close-button i {
  font-size: 18px;
}

.helper-tooltip-body {
  padding: 12px;
  font-size: 10px;
  line-height: 1.4;
  color: #333;
  max-height: 300px;
  overflow-y: auto;
}

/* Styling scrollbar */
.helper-tooltip-body::-webkit-scrollbar {
  width: 6px;
}

.helper-tooltip-body::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.helper-tooltip-body::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.helper-tooltip-body::-webkit-scrollbar-thumb:hover {
  background: #555;
}
.recommendation-text :deep(strong) {
  font-weight: bold;
}
</style>

<style scoped>
.recommendation-text :deep(p) {
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.recommendation-text :deep(strong) {
  font-weight: bold;
}

.recommendation-text :deep(ul) {
  font-size: 0.875rem;
  padding-left: 1.25rem;
  margin-bottom: 0.5rem;
}

.recommendation-text :deep(li) {
  margin-bottom: 0.25rem;
}
</style>