<script setup>
import RotatingCard from "../../../examples/cards/rotatingCards/RotatingCard.vue";
import RotatingCardFront from "../../../examples/cards/rotatingCards/RotatingCardFront.vue";
import RotatingCardFrontInfo from "../../../examples/cards/rotatingCards/RotatingCardFrontInfo.vue";
import RotatingCardFrontWarning from "../../../examples/cards/rotatingCards/RotatingCardFrontWarning.vue";
import RotatingCardBack from "../../../examples/cards/rotatingCards/RotatingCardBack.vue";
import RotatingCardBackInfo from "../../../examples/cards/rotatingCards/RotatingCardBackInfo.vue";
import RotatingCardBackWarning from "../../../examples/cards/rotatingCards/RotatingCardBackWarning.vue";

</script>
<template>
  <section class="my-2 py-2">
    <div class="container">
      <div class="row justify-content-center text-center my-sm-3">
          <div class="col-lg-6">
            <h3 class="text-dark mb-0">Masih bingung dengan data BPS?</h3>
          </div>
        </div>
      <div class="row align-items-center">
        <div class="col-md-12 mx-auto">
          <div class="row">
            <div class="col-lg-4 mx-auto p-lg-4 mt-lg-0 mt-2">
              <RotatingCard>
              <RotatingCardFrontInfo
              image="https://res.cloudinary.com/bpsjatim/image/upload/f_auto,q_auto/bmvkoaikysmhrythzdfm"
              title="Konsultasi dengan<br /> Statistisi Ahli BPS"
              description="Konsultasi secara daring langsung bersama Statistisi Ahli dan Analis Data BPS Jawa Timur yang kompeten di bidangnya."
              label="🗓️ Senin-Jumat, 08.00-16.00"
              />

              <RotatingCardBackInfo
              image="https://res.cloudinary.com/bpsjatim/image/upload/f_auto,q_auto/bmvkoaikysmhrythzdfm"
              description="Klik tombol di bawah ini untuk membuat reservasi jadwal konsultasi sesuai dengan kebutuhan Anda"
              :action="[
                {
                  route: '/konsultasi',
                  label: 'Buat Reservasi',
                },
              ]"
              />
              </RotatingCard>
            </div>
            <div class="col-lg-4 mx-auto p-lg-4 mt-lg-0 mt-2">
              <RotatingCard>
              <RotatingCardFront
              image="https://res.cloudinary.com/bpsjatim/image/upload/f_auto,q_auto/o43nykivufzlmudnx4v6"
              title="Ngobrol dengan<br /> Ning AIDA"
              description="Ning AIDA (Artificial Intelligence Data Assistant) akan melayani permintaan data Anda selama 24 jam"
              label="🗓️ Setiap Hari, 24 Jam Non Stop"
              />

              <RotatingCardBack
              image="https://res.cloudinary.com/bpsjatim/image/upload/f_auto,q_auto/o43nykivufzlmudnx4v6"
              description="Harap diingat bahwa meskipun AIDA yang berbasis kecerdasan buatan (AI) berupaya memberikan pelayanan 24 jam non stop, AIDA mungkin saja membuat kesalahan saat memberikan informasi. Tetap merujuk ke website BPS untuk data yang paling akurat."
              :action="[
                {
                  route: '/aida',
                  label: 'Mulai Mengobrol',
                },
              ]"
              />
              </RotatingCard>
            </div>

            <div class="col-lg-4 ms-auto me-auto p-lg-4 mt-lg-0 mt-2">
              <RotatingCard>
              <RotatingCardFrontWarning
              image="https://res.cloudinary.com/bpsjatim/image/upload/f_auto,q_auto/wb88gcfmrrggwhxho4l4"
              title="Baca Koleksi<br />Publikasi BPS"
              description="Anda bisa membaca secara gratis publikasi BPS yang berisi tentang data statistik, ulasan, dan analisis dengan beragam topik."
              label="🗓️ Setiap Saat"
              />

              <RotatingCardBackWarning
              image="https://res.cloudinary.com/bpsjatim/image/upload/f_auto,q_auto/wb88gcfmrrggwhxho4l4"
              description="Temukan publikasi statistik BPS berdasarkan kata kunci topik data sesuai kebutuhan Anda"
              :action="[
                {
                  route: 'https://jatim.bps.go.id/id/publication',
                  label: 'Baca Publikasi',
                },
              ]"
              />
              </RotatingCard>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
