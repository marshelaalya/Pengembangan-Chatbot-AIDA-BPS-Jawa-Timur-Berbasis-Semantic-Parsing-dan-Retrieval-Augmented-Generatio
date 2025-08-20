<script setup>
// card components
import BackgroundBlogCard from "../../../examples/cards/blogCards/BackgroundBlogCard.vue";

// icon layanan
import silastik from "@/assets/img/icon/silastik.png";
import romantik from "@/assets/img/icon/romantik.png";
import perpustakaan from "@/assets/img/icon/opac.png";
import api from "@/assets/img/icon/api.png";

</script>
<template>
  <section class="py-3">
    <div class="container">
      <div class="row justify-content-center text-center my-sm-3">
        <div class="col-lg-6">
          <h4 class="font-weight-normal mb-2">Layanan Lainnya</h4>
        </div>
      </div>
      <div class="row">
        <div class="col-lg-3 col-md-12 col-12 mb-2">
          <BackgroundBlogCard
            :image="perpustakaan"
            title="Perpustakaan Digital"
            description="Publikasi statistik terbitan BPS dari berbagai kategori."
            url="https://perpustakaan.bps.go.id/opac/"
          />
        </div>
        <div class="col-lg-3 col-md-12 col-12 mb-2">
          <BackgroundBlogCard
            :image="silastik"
            title="SILASTIK"
            description="Layanan penjualan data mikro, publikasi, dan peta digital wilkerstat."
            url="https://silastik.bps.go.id/v3/index.php/site/index_internal/#tta"
          />
        </div>
        <div class="col-lg-3 col-md-12 col-12 mb-2">
          <BackgroundBlogCard
            :image="romantik"
            title="ROMANTIK"
            description="Layanan bagi instansi pemerintah yang akan melakukan survei dan mengajukan rekomendasi kegiatan statistik."
            url="https://romantik.web.bps.go.id/"
          />
        </div>
        <div class="col-lg-3 col-md-12 col-12 mb-2">
          <BackgroundBlogCard
            :image="api"
            title="WebAPI BPS"
            description="API data statistik BPS yang dapat digunakan untuk mengintegrasikan data BPS ke aplikasi lain."
            url="https://webapi.bps.go.id/developer/"
          />
        </div>
      </div>
    </div>
  </section>
</template>
