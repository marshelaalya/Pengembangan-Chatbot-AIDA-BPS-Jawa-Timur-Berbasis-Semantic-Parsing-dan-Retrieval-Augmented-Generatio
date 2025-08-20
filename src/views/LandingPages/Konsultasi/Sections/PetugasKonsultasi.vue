<script setup>
import { ref, computed, onMounted, watch } from "vue";
import CariWilayah from "./CariWilayahKonsultasi.vue";
import { useRouter } from "vue-router";
import PetugasKonsultasiCard from "@/examples/cards/teamCards/PetugasKonsultasiCard.vue";
import MaterialPagination from "@/components/MaterialPagination.vue";
import MaterialPaginationItem from "@/components/MaterialPaginationItem.vue";
import SpesialisasiKonsultasi from "./SpesialisasiKonsultasi.vue";
import { apiService } from "@/api/ApiService";

const emit = defineEmits(["keahlianClicked"]);
const props = defineProps({
  mfd: {
    type: String,
    required: true,
  },
});

const petugasKonsultasi = ref([]);
const loading = ref(true);
const currentPage = ref(1);
const itemsPerPage = ref(9);
const router = useRouter();

// Tambahkan state untuk filter
const activeFilters = ref({
  wilayah: null,
  keahlian: null,
  originalData: [] // untuk menyimpan data asli
});

// Fungsi untuk mengacak array
const shuffleArray = (array) => {
  return array.sort(() => Math.random() - 0.5);
};

const fetchPetugas = async (mfd) => {
  loading.value = true;
  try {
    const response = await apiService.getOfficersBySatker(mfd);
    if (response.data == 400) {
      router.push({ name: "login" });
    } else {
      activeFilters.value.originalData = response.data.data;
      applyFilters(); // Terapkan filter yang aktif
    }
  } catch (error) {
    console.error("Error fetching petugas konsultasi:", error);
  } finally {
    loading.value = false;
  }
};

// Fungsi untuk menerapkan semua filter aktif
const applyFilters = () => {
  let filteredData = [...activeFilters.value.originalData];
  
  if (activeFilters.value.wilayah) {
    filteredData = filteredData.filter(petugas => {
      // Konversi kedua nilai ke string dan pastikan keduanya ada
      const petugasSatker = petugas.id_satker?.toString() || '';
      const selectedWilayah = activeFilters.value.wilayah?.toString() || '';
      return petugasSatker === selectedWilayah;
    });
  }
  
  if (activeFilters.value.keahlian) {
    filteredData = filteredData.filter(petugas => 
      petugas.keahlian && petugas.keahlian.some(k => k.id.toString() === activeFilters.value.keahlian.toString())
    );
  }
  
  petugasKonsultasi.value = shuffleArray(filteredData);
};

const handleCariWilayahInput = async (satker) => {
  console.log('Wilayah yang dipilih:', satker);
  activeFilters.value.wilayah = satker;
  
  // Update URL dengan mfd baru dan pertahankan filter lainnya
  router.push({
    path: '/konsultasi',
    query: { 
      ...router.currentRoute.value.query,
      mfd: satker 
    }
  });
  
  // Fetch data baru berdasarkan wilayah yang dipilih
  await fetchPetugas(satker);
};

const handleKeahlian = (itemId) => {
  // Jika keahlian yang diklik sama dengan yang aktif, hapus filter
  if (activeFilters.value.keahlian === itemId) {
    activeFilters.value.keahlian = null;
  } else {
    // Jika berbeda, set filter baru
    activeFilters.value.keahlian = itemId;
  }
  applyFilters();
};

const handleHapusFilter = () => {
  activeFilters.value.wilayah = null;
  activeFilters.value.keahlian = null;
  petugasKonsultasi.value = shuffleArray(activeFilters.value.originalData);
};

const paginatedPetugas = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return petugasKonsultasi.value.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(petugasKonsultasi.value.length / itemsPerPage.value);
});

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

onMounted(() => {
  fetchPetugas(props.mfd);
});

watch(
  () => props.mfd,
  (newMfd) => {
    fetchPetugas(newMfd);
  }
);

// Tambahkan ref untuk daftar wilayah
const wilayahList = ref([
  { id: '3500', name: 'Provinsi Jawa Timur' },
  { id: '3501', name: 'Kabupaten Pacitan' },
  { id: '3502', name: 'Kabupaten Ponorogo' },
  { id: '3503', name: 'Kabupaten Trenggalek' },
  { id: '3504', name: 'Kabupaten Tulungagung' },
  { id: '3505', name: 'Kabupaten Blitar' },
  { id: '3506', name: 'Kabupaten Kediri' },
  { id: '3507', name: 'Kabupaten Malang' },
  { id: '3508', name: 'Kabupaten Lumajang' },
  { id: '3509', name: 'Kabupaten Jember' },
  { id: '3510', name: 'Kabupaten Banyuwangi' },
  { id: '3511', name: 'Kabupaten Bondowoso' },
  { id: '3512', name: 'Kabupaten Situbondo' },
  { id: '3513', name: 'Kabupaten Probolinggo' },
  { id: '3514', name: 'Kabupaten Pasuruan' },
  { id: '3515', name: 'Kabupaten Sidoarjo' },
  { id: '3516', name: 'Kabupaten Mojokerto' },
  { id: '3517', name: 'Kabupaten Jombang' },
  { id: '3518', name: 'Kabupaten Nganjuk' },
  { id: '3519', name: 'Kabupaten Madiun' },
  { id: '3520', name: 'Kabupaten Magetan' },
  { id: '3521', name: 'Kabupaten Ngawi' },
  { id: '3522', name: 'Kabupaten Bojonegoro' },
  { id: '3523', name: 'Kabupaten Tuban' },
  { id: '3524', name: 'Kabupaten Lamongan' },
  { id: '3525', name: 'Kabupaten Gresik' },
  { id: '3526', name: 'Kabupaten Bangkalan' },
  { id: '3527', name: 'Kabupaten Sampang' },
  { id: '3528', name: 'Kabupaten Pamekasan' },
  { id: '3529', name: 'Kabupaten Sumenep' },
  { id: '3571', name: 'Kota Kediri' },
  { id: '3572', name: 'Kota Blitar' },
  { id: '3573', name: 'Kota Malang' },
  { id: '3574', name: 'Kota Probolinggo' },
  { id: '3575', name: 'Kota Pasuruan' },
  { id: '3576', name: 'Kota Mojokerto' },
  { id: '3577', name: 'Kota Madiun' },
  { id: '3578', name: 'Kota Surabaya' },
  { id: '3579', name: 'Kota Batu' }
]);

// Ganti fungsi handleCariWilayahInput menjadi handleWilayahChange
const handleWilayahChange = async (event) => {
  const selectedValue = event.target.value;
  if (selectedValue) {
    await handleCariWilayahInput(selectedValue);
  }
};
const keahlianList = ref([]);

onMounted(async () => {
  fetchPetugas(props.mfd);
  try {
    const response = await apiService.getKeahlian();
    keahlianList.value = response.data.data;
  } catch (error) {
    console.error("Error fetching keahlian:", error);
  }
});

const getKeahlianName = (keahlianId) => {
  const keahlian = keahlianList.value.find(k => k.id.toString() === keahlianId.toString());
  return keahlian ? keahlian.nama_keahlian : keahlianId;
};
</script>

<template>
  <section class="pb-5 satker-relative bg-gradient-dark mx-n3">
    <div class="container">
      <div class="row">
        <div class="col-md-3 text-start mb-3 mt-5">
          <select 
            class="form-select" 
            @change="handleWilayahChange"
            aria-label="Pilih Wilayah"
          >
            <option value="">Pilih Wilayah</option>
            <option 
              v-for="wilayah in wilayahList" 
              :key="wilayah.id" 
              :value="wilayah.id"
            >
              {{ wilayah.name }}
            </option>
          </select>
        </div>
        <div class="col-md-7 text-start mb-3 mt-5">
          <div class="filter-tags" v-if="activeFilters.keahlian">
            <button class="btn btn-success" @click="handleHapusKeahlian">
              {{ getKeahlianName(activeFilters.keahlian) }}
              <span class="ms-2">×</span>
            </button>
          </div>
        </div>
        <div class="col-md-2 text-end mb-3 mt-5">
          <button class="btn btn-danger" @click="handleHapusFilter">Hapus Filter</button>
        </div>
        <div class="col-md-12 text-start mb-5">
          <h3 class="text-white z-index-1 satker-relative">Reservasi Konsultasi</h3>
          <p class="text-white text-dark mb-0">
            Pilih petugas konsultasi berdasarkan bidang keahlian yang sesuai dengan topik konsultasi Anda:
          </p>
        </div>
      </div>
      <div class="row">
        <div v-if="loading" class="text-center">
          <img src="/assets/loading_2.svg" alt="Loading..." />
          <p class="fw-bold fs-3 text-light">Loading...</p>
        </div>
        <div v-else-if="petugasKonsultasi.length == 0" class="text-center">
          <p>Tidak ada petugas ditemukan.</p>
        </div>
        <div v-else class="col-lg-4 col-12 mb-6" v-for="petugas in paginatedPetugas" :key="petugas.id">
            <PetugasKonsultasiCard style="height: 100%;" class="mt-4" :petugas="petugas" />
        </div>
      </div>
      <div class="container pt-5">
        <div class="row justify-content-center">
          <div class="col-lg-4">
            <div class="pagination-container">
              <MaterialPagination>
                <MaterialPaginationItem prev @click="changePage(currentPage - 1)" />
                <MaterialPaginationItem
                  v-for="page in totalPages"
                  :key="page"
                  :label="page"
                  :active="page == currentPage"
                  @click="changePage(page)"
                />
                <MaterialPaginationItem next @click="changePage(currentPage + 1)" />
              </MaterialPagination>
            </div>
          </div>
        </div>
      </div>
      <div class="row pt-3">
        <div class="col-md-8 text-start mb-5 mt-2">
          <h3 class="text-white z-index-1 satker-relative">Cari Statistisi Ahli atau Spesialisasi</h3>
          <p class="text-white text-dark mb-0">
            Pilih kategori yang tersedia sesuai masalah Anda
          </p>
        </div>
      </div>
      <SpesialisasiKonsultasi @item="handleKeahlian" @click="keahlianClicked" />
    </div>
  </section>
</template>

<style scoped>
.pagination-container {
  display: flex;
  justify-content: center;
}

.form-select {
  background-color: white;
  color: #344767;
  border: 1px solid #d2d6da;
  border-radius: 0.5rem;
  padding: 0.625rem 0.75rem;
  font-size: 0.875rem;
  font-weight: 400;
  line-height: 1.4rem;
}

.form-select:focus {
  border-color: #35D28A;
  box-shadow: 0 0 0 2px rgba(53, 210, 138, 0.25);
}

.filter-tags {
  display: flex;
  gap: 0.5rem;
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  background: rgba(53, 210, 138, 0.2);
  color: #fff;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  border: 1px solid rgba(53, 210, 138, 0.5);
  cursor: pointer;
}

.filter-tag:hover {
  background: rgba(53, 210, 138, 0.3);
}

.tag-close {
  background: none;
  border: none;
  color: #fff;
  margin-left: 0.5rem;
  padding: 0 0.25rem;
  font-size: 1.25rem;
  line-height: 1;
}

.tag-close:hover {
  color: #ff4444;
}

.btn-success {
  background-color: #35D28A;
  border-color: #35D28A;
  color: #fff;
}

.btn-success:hover {
  background-color: #2bb674;
  border-color: #2bb674;
}

/* Hapus style yang tidak digunakan */
.filter-tags {
  display: flex;
  gap: 0.5rem;
}

</style>
