<script setup>
import { onMounted } from "vue";

// material-input
import setMaterialInput from "@/assets/js/material-input";
onMounted(() => {
  setMaterialInput();
});
</script>
<template>
  <section class="py-sm-7 py-5 position-relative">
    <div class="container">
      <div class="row">
        <div class="col-12 mx-auto">
          <div class="mt-n8 mt-md-n9 text-center">
          </div>
          <div class="row pt-7">
            <div
              class="col-lg-10 col-md-8 z-index-2 position-relative px-md-2 px-sm-5 mx-auto"
            >
              <div
                class="d-flex justify-content-between align-items-center mb-2"
              >
                <h3 class="mb-0">Apa itu dan Mengapa HaloPST?</h3>
              </div>
              <p class="text-md mb-4">
                Perkembangan teknologi menyebabkan kebutuhan akan pelayanan yang lebih cepat, efisien, dan akurat.
                Digitalisasi di berbagai sektor pelayanan publik yaitu pelayanan statistik menjadi semakin penting. 
                Kebutuhan data statistik yang akurat dan mudah diakses adalah kebutuhan pokok bagi berbagai kalangan, 
                mulai dari pemerintah, akademisi, hingga masyarakat umum.
                <br />
              </p>
              <p class="text-md mb-4">
                <b>HaloPST</b> merupakan sebuah platform digital yang menawarkan Pelayanan Statistik Terpadu secara virtual (online).
                <b>HaloPST</b>  ini dirancang dengan desain antarmuka yang <i>user friendly</i> guna memudahkan pengguna dalam menggunakan 
                berbagai fitur layanan seperti pencarian berbagai data statistik, Chat AI, dan layanan konsultasi. Melalui 
                <b>HaloPST</b> , pengguna dapat mengakses berbagai kebutuhan data statistik pada fitur pencarian data serta fitur 
                Chat AI untuk menjawab pertanyaan terkait insight data secara cepat dan dapat dilakukan kapanpun. Selain itu, pengguna dapat melakukan  
                konsultasi langsung secara online dengan Statistisi dan Tenaga Ahli BPS pada fitur layanan konsultasi. 
                <br />
              </p>
              <p class="text-md mb-4">
                <b>HaloPST</b> juga memberikan kepastian bahwa data yang disajikan adalah data yang aktual dan terpercaya. Melalui 
                website ini, diharapkan pelayanan statistik dapat semakin optimal dan memberikan kontribusi yang signifikan bagi 
                pembangunan serta pengambilan keputusan yang berbasis data. Dengan demikian, <b>HaloPST</b> dapat menjadi langkah maju 
                dalam menghadirkan pelayanan statistik yang modern, terintegrasi, dan dapat diandalkan di era digital ini.
              </p>

              <div
                class="d-flex justify-content-between align-items-center mb-2"
              >
                <h3 class="mb-0">Tujuan HaloPST</h3>
              </div>
              <ol class="numbering">
                <li class="text-md mb-2">
                  Menyediakan platform digital yang memungkinkan pengguna mengakses berbagai data statistik secara cepat 
                  dan mudah, kapan saja dan di mana saja.
                </li>
                <li class="text-md mb-2">Mengintegrasikan berbagai layanan statistik dalam satu platform terpadu.
                </li>
                <li class="text-md mb-2">
                  Membantu pemerintah, lembaga, dan masyarakat dalam pengambilan keputusan yang lebih baik dengan menyediakan 
                  data statistik yang relevan dan mudah diakses.
                </li>
                <li class="text-md mb-2">
                  Menyediakan layanan konsultasi dan edukasi terkait penggunaan data statistik melalui sesi konsultasi 
                  virtual.
                </li>
                <li class="text-md">
                  Mendukung kegiatan penelitian dan inovasi dengan menyediakan data yang terpercaya dan dapat digunakan 
                  oleh peneliti, akademisi, dan inovator. 
                </li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.numbering {
  padding-left: 1.5em; /* Adjust this value as necessary */
  list-style-position: outside;
}
</style>
