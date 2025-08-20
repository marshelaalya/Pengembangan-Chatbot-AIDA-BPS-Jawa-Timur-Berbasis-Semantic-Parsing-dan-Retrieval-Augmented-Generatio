<script setup>
// example components
import DefaultNavbar from "../../../examples/navbars/NavbarDefault.vue";
import Header from "../../../examples/Header.vue";
import DefaultFooter from "../../../examples/footers/FooterDefault.vue";

// sections
import Profile from "./Sections/TentangProfil.vue";
import Mutu from "./Sections/TentangMutu.vue";

// image
import image from "@/assets/img/bg9.jpg";
</script>
<template>
  <DefaultNavbar />
  <Header>
    <div
      class="page-header min-height-300"
      :style="{ backgroundImage: `url(${image})` }"
      loading="lazy"
    >
    </div>
  </Header>
  <div class="card card-body blur shadow-blur mx-3 mx-md-4 mt-n6">
    <Profile />
    <Mutu />
  </div>
  <DefaultFooter />
</template>
