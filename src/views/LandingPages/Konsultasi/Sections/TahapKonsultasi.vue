<!-- src/views/Sections/TahapKonsultasi.vue -->
<template>
  <section class="py-4">
    <div class="container">
      <div class="row align-items-center justify-content-center">
        
          <div class="col-lg-3 row justify-content-center text-center ">
            <DefaultInfoCard
              :image="tahap1"
              class="cursor-pointer"
              description="Pilih ingin dengan siapa Anda berkonsultasi dan buat reservasi konsultasi"
              @click="tahap1Clicked"
            />

        </div>
        <!-- Arrow -->
        <div class="col-lg-1 text-center d-lg-block d-none ">
          <img src="@/assets/img/illustrations/panah-kanan.png" alt="Arrow" class="img-fluid" />
        </div>
        
          <div class="col-lg-3 row justify-content-center text-center">
            <DefaultInfoCard
              :image="tahap2"
              class="cursor-pointer"
              description="Petugas akan mengirimkan jadwal dan link konsultasi melalui email yang terdaftar"
              @click="tahap23Clicked"
            />
          </div>
        
        <!-- Arrow -->
        <div class="col-lg-1 text-center d-lg-block d-none ">
          <img src="@/assets/img/illustrations/panah-kanan.png" alt="Arrow" class="img-fluid" />
        </div>
        
          <div class="col-lg-3 row justify-content-center text-center">
            <DefaultInfoCard
              :image="tahap3"
              class="cursor-pointer"
              description="Silakan jelaskan masalah Anda dan dapatkan solusi dari Statistisi Ahli BPS terpercaya"
              @click="tahap23Clicked"
            />
          </div>
        
      </div>
    </div>
  </section>
</template>

<script setup>
import DefaultInfoCard from '../../../../examples/cards/infoCards/DefaultInfoCard.vue';
import tahap1 from '@/assets/img/illustrations/tahap1.png';
import tahap2 from '@/assets/img/illustrations/tahap2.png';
import tahap3 from '@/assets/img/illustrations/tahap3.png';
import { useRouter } from 'vue-router';
const router = useRouter();


const emit = defineEmits(['tahap1Clicked']);

function tahap1Clicked() {
  emit('tahap1Clicked');
}

function tahap23Clicked(){
  router.push('/settings/booking');
}
</script>

<style scoped>
.row {
    display: flex;
    align-items: center;
  }

  .col-lg-3, .col-lg-1 {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .col-lg-1 img {
    width: 100%;
    max-width: 50px; /* Adjust as necessary */
  }
</style>