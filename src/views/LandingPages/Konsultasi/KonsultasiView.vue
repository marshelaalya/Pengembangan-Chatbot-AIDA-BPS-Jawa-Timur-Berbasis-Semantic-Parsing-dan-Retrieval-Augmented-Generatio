<!-- src/views/KonsultasiView.vue -->
<template>
  <div>
    <NavbarKonsultasi />
    <header class="bg-gradient-dark">
      <div class="page-header min-vh-70" :style="{ backgroundImage: `url(${bg0})` }">
        <span class="mask bg-gradient-dark opacity-4"></span>
        <div class="container">
          <div class="row justify-content-center">
            <div class="col-lg-8 text-center mx-auto my-auto">
              <h1 class="text-white">
                Konsultasikan Masalah Data Statistik dengan Ahlinya
              </h1>
              <p class="mb-4 text-white text-dark">
                Layanan konsultasi langsung secara daring dengan Statistisi Ahli
                dan Analis Data Profesional dari BPS Jawa Timur
              </p>
            </div>
          </div>
        </div>
      </div>
    </header>
    <div class="card card-body shadow-xl mx-3 mx-md-4 mt-n6 pb-0">
      <Tahapan @tahap1Clicked="scrollToPetugasKonsultasi" />
      <div ref="petugasSection">
        <PetugasKonsultasi :mfd="mfd" @keahlianClicked="scrollToPetugasKonsultasi"/>
      </div>
    </div>
    <DefaultFooter />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import NavbarKonsultasi from '../../../examples/navbars/NavbarKonsultasi.vue';
import DefaultFooter from '../../../examples/footers/FooterDefault.vue';
import bg0 from '@/assets/img/bg9.jpg';
import Tahapan from './Sections/TahapKonsultasi.vue';
import PetugasKonsultasi from './Sections/PetugasKonsultasi.vue';

const petugasSection = ref(null);
const route = useRoute();

const mfd = ref(route.query.mfd);

function scrollToPetugasKonsultasi() {
  petugasSection.value.scrollIntoView({ behavior: 'smooth' });
}

const body = document.getElementsByTagName('body')[0];
onMounted(() => {
  body.classList.add('konsultasi-page');
  body.classList.add('bg-gray-200');
  const isAuthenticated = localStorage.getItem('loggedIn') === 'true'
  if (!isAuthenticated) {
    router.push({ name: 'login' })
  }
});
onUnmounted(() => {
  body.classList.remove('konsultasi-page');
  body.classList.remove('bg-gray-200');
});
</script>
