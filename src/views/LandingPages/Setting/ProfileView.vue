<template>
  <div>
    <NavbarDefault />
    <div class=" container-fluid py-2 px-5" id="background">
      <div class="row mt-lg-5 mt-md-3">
        <div class="col-md-4 col-sm-6 position-sticky top-0">
          <!-- User info card -->
          <UserInfoCard :user="user" />

          <!-- Button list -->
          <ButtonList @select-card="$router.push({ name: $event })" />
        </div>
        <div class="col-md-8 col-sm-12">
          <!-- Card router view -->
          <router-view :api-url="cardApiUrl" :user="user" />
        </div>
      </div>
    </div>
    <DefaultFooter />
  </div>
</template>

<script>
import UserInfoCard from "@/views/LandingPages/Setting/component/UserInfoCard.vue";
import ButtonList from "@/views/LandingPages/Setting/component/ButtonList.vue";
import NavbarDefault from "@/examples/navbars/NavbarDefault.vue";
import DefaultFooter from "@/examples/footers/FooterDefault.vue";

export default {
  name: "ProfileView",
  components: { UserInfoCard, ButtonList, NavbarDefault, DefaultFooter },
  data() {
    return {
      user: {},
      cardApiUrl: {
        profil: '-',
        booking: '-',
        history: '-',
      },
    };
  },
};
</script>

<style scoped>
#background{
  background-color: #F5FDEC;
  min-height: 100vh;
}
</style>
