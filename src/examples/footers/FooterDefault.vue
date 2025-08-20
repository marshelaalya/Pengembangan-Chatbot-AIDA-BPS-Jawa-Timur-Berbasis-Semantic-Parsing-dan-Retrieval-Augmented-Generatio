<script setup>
import logoDark from "@/assets/img/logo-ct-dark.svg";
defineProps({
  brand: {
    type: Object,
    name: String,
    logo: String,
    route: "",
    default: () => ({
      logo: logoDark,
      route: "/"
    })
  },
  socials: {
    type: Array,
    icon: String,
    link: String,
    default: () => [
      {
        icon: '<i class="fab fa-facebook text-lg opacity-8"></i>',
        link: "https://www.facebook.com/bpsjatim/"
      },
      {
        icon: '<i class="fab fa-twitter text-lg opacity-8"></i>',
        link: "https://twitter.com/bpsjatim"
      },
      {
        icon: '<i class="fab fa-instagram text-lg opacity-8"></i>',
        link: "https://instagram.com/bpsjatim"
      },
      {
        icon: '<i class="fab fa-tiktok text-lg opacity-8"></i>',
        link: "https://www.tiktok.com/@bpsjatim"
      },
      {
        icon: '<i class="fab fa-whatsapp text-lg opacity-8"></i>',
        link: "https://whatsapp.com/channel/0029VaYvI8NFSAtAGl8Whb20"
      },
      {
        icon: '<i class="fab fa-youtube text-lg opacity-8"></i>',
        link: "https://www.youtube.com/@BPSProvinsiJawaTimur"
      }
    ]
  },
  menus: {
    type: Array,
    name: String,
    items: {
      type: Array,
      name: String,
      href: String
    },
    default: () => [
      {
        name: "Tentang BPS",
        items: [
          {
            name: "Informasi Umum",
            href: "https://ppid.bps.go.id/app/konten/3500/Profil-BPS.html#pills-0"
          },
          {
            name: "Visi & Misi",
            href: "https://ppid.bps.go.id/app/konten/3500/Profil-BPS.html#pills-1"
          },
          {
            name: "Tugas & Fungsi",
            href: "https://ppid.bps.go.id/app/konten/3500/Profil-BPS.html#pills-3"
          },
        ]
      },
      {
        name: "Tentang PST",
        items: [
          { 
            name: "Pelayanan Statistik Terpadu", 
            href: "https://ppid.bps.go.id/app/konten/3500/Layanan-BPS.html#pills-0" 
          },
          {
            name: "Standar Pelayanan",
            href: "https://ppid.bps.go.id/app/konten/3500/Layanan-BPS.html#pills-2"
          },
          {
            name: "Maklumat Pelayanan",
            href: "https://ppid.bps.go.id/app/konten/3500/Layanan-BPS.html#pills-2"
          },
          {
            name: "Kompensasi Pelayanan",
            href: "https://ppid.bps.go.id/app/konten/3500/Layanan-BPS.html#pills-3"
          }
        ]
      },
      {
        name: "Bantuan",
        items: [
          {
            name: "Survei Kepuasan",
            href: "https://ppid.bps.go.id/app/konten/3500/Layanan-BPS.html#pills-9"
          },
          {
            name: "Pengaduan",
            href: "https://ppid.bps.go.id/app/konten/3500/Layanan-BPS.html#pills-11"
          },
          {
            name: "Informasi Pelayanan",
            href: "https://ppid.bps.go.id/app/konten/3500/Layanan-BPS.html#pills-12"
          }
        ]
      },
      {
        name: "Website",
        items: [
          {
            name: "BPS",
            href: "https://jatim.bps.go.id"
          },
          {
            name: "PPID",
            href: "https://ppid.bps.go.id/?mfd=3500"
          },
          {
            name: "Pojok Statistik",
            href: "https://pojokstatistik.bps.go.id/page/map"
          }
        ]
      }
    ]
  }
});
</script>
<template>
  <footer class="footer pt-5 mt-5">
    <div class="container">
      <div class="row">
        <div class="col-md-3 mb-4 ms-auto">
          <div>
            <a :href="brand.route">
              <img :src="brand.logo" class="mb-3 footer-logo" width="100%"alt="main_logo" />
            </a>
            <p class="font-weight-normal text-dark text-xs mb-4">
              Jalan Raya Kendangsari Industri No. 43 - 44 Surabaya 60292, 
              Telp. (031) 8439343, Fax (031) 8494007, 8471143, Email : jatim@bps.go.id</p>
          </div>
          <div>
            <ul class="d-flex flex-row ms-n3 nav">
              <li
                class="nav-item"
                v-for="{ icon, link } of socials"
                :key="link"
              >
                <a
                  class="nav-link pe-1"
                  :href="link"
                  target="_blank"
                  v-html="icon"
                >
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div
          class="col-md-2 col-sm-6 col-6 mb-4"
          v-for="{ name, items } of menus"
          :key="name"
        >
          <h6 class="text-sm">{{ name }}</h6>
          <ul class="flex-column ms-n3 nav">
            <li class="nav-item" v-for="item of items" :key="item.name">
              <a class="nav-link" :href="item.href" target="_blank">
                {{ item.name }}
              </a>
            </li>
          </ul>
        </div>

        <div class="col-12">
          <div class="text-center">
            <p class="text-dark my-4 text-sm font-weight-normal">
              Semua Hak Dilindungi ©
              {{ new Date().getFullYear() }},
              <a href="https://jatim.bps.go.id" target="_blank"
                >BPS Provinsi Jawa Timur</a
              >.
            </p>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>
