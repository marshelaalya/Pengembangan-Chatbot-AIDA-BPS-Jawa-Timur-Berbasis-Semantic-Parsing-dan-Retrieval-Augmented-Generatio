<script setup>
import { RouterLink, useRouter } from "vue-router";
import { ref, watch, onMounted } from "vue";
import { useWindowsWidth } from "../../assets/js/useWindowsWidth";
import { googleLogout } from "vue3-google-login";
import bootstrap from "bootstrap/dist/js/bootstrap.min.js";

// images
import ArrDark from "@/assets/img/down-arrow-dark.svg";
import DownArrWhite from "@/assets/img/down-arrow-white.svg";
import haloPstBPS from "@/assets/img/halopst-bps.svg";
import haloPST from "@/assets/img/halopst-logo.svg";

const props = defineProps({
  konsultasi: {
    type: Object,
    required: true,
    default: () => ({
      route: "/login",
      color: "bg-gradient-success",
      label: "Login",
    }),
    validator: (value) => {
      return (
        typeof value.route == "string" &&
        typeof value.color == "string" &&
        typeof value.label == "string"
      );
    },
  },
  transparent: {
    type: Boolean,
    default: false,
  },
  light: {
    type: Boolean,
    default: false,
  },
  dark: {
    type: Boolean,
    default: false,
  },
  sticky: {
    type: Boolean,
    default: false,
  },
  darkText: {
    type: Boolean,
    default: false,
  },
});

// set arrow color
function getArrowColor() {
  if (props.transparent && textDark.value) {
    return ArrDark;
  } else if (props.transparent) {
    return DownArrWhite;
  } else {
    return ArrDark;
  }
}

// set text color
const getTextColor = () => {
  let color;
  if (props.transparent && textDark.value) {
    color = "text-dark";
  } else if (props.transparent) {
    color = "text-white";
  } else {
    color = "text-dark";
  }

  return color;
};

// set nav color on mobile && desktop
let textDark = ref(props.darkText);
const { type } = useWindowsWidth();

if (type.value == "mobile") {
  textDark.value = true;
} else if (type.value == "desktop" && textDark.value == false) {
  textDark.value = false;
}

let isLoggedIn = ref(false);
let user = ref(null);
const router = useRouter();

const logout = () => {
  googleLogout();
  Object.keys(user.value).forEach((key) => (user.value[key] = ""));
  isLoggedIn.value = false;
  localStorage.removeItem("user");
  localStorage.setItem("loggedIn", "false");
  localStorage.clear();
  router.push("/login");
};

onMounted(() => {
  const userData = localStorage.getItem("user");
  const loggedIn = localStorage.getItem("loggedIn");
  if (loggedIn == "true" && userData) {
    user.value = JSON.parse(userData);
    isLoggedIn.value = true;
  }
});

watch(
  () => type.value,
  (newValue) => {
    if (newValue == "mobile") {
      textDark.value = true;
    } else {
      textDark.value = false;
    }
  }
);
</script>

<template>
  <nav
    class="navbar navbar-expand-lg top-0"
    :class="{
      'z-index-3 w-100 shadow-none navbar-transparent position-absolute my-3':
        props.transparent,
      'my-3 blur border-radius-lg z-index-3 py-2 shadow py-2 start-0 end-0 mx-4 position-absolute mt-4':
        props.sticky,
      'navbar-light bg-white py-3': props.light,
      'navbar-dark bg-gradient-dark z-index-3 py-3': props.dark,
    }"
  >
    <div
      :class="
        props.transparent || props.light || props.dark
          ? 'container'
          : 'container-fluid px-0'
      "
    >
      <RouterLink
        class="navbar-brand d-none d-md-block"
        :class="[
          (props.transparent && textDark.value) || !props.transparent
            ? 'text-dark font-weight-bolder ms-sm-3'
            : 'text-white font-weight-bolder ms-sm-3',
        ]"
        :to="{ name: 'presentation' }"
        rel="tooltip"
        title="Halo PST BPS Jawa Timur"
        data-placement="bottom"
      >
        <img :src="haloPstBPS" alt="Halo PST BPS Jawa Timur" class="arrow" />
      </RouterLink>
      <RouterLink
        class="navbar-brand d-block d-md-none"
        :class="
          props.transparent || props.dark
            ? 'text-white'
            : 'font-weight-bolder ms-sm-3'
        "
        to="/"
        rel="tooltip"
        title="Halo PST BPS Jawa Timur"
        data-placement="bottom"
      >
        <img :src="haloPST" alt="Halo PST BPS Jawa Timur" class="arrow" />
      </RouterLink>
      <template v-if="!isLoggedIn">
        <RouterLink
          :to="{ name: 'login' }"
          class="btn btn-sm bg-gradient-success mb-0 ms-auto d-lg-none d-block"
          >Login</RouterLink
        >
      </template>
      <template v-else>
        <RouterLink
          to="/settings/profil"
          class="btn btn-sm bg-gradient-info mb-0 ms-auto d-lg-none d-block"
        >
          Akun
        </RouterLink>
      </template>
      <button
        class="navbar-toggler shadow-none ms-2"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navigation"
        aria-controls="navigation"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon mt-2">
          <span class="navbar-toggler-bar bar1"></span>
          <span class="navbar-toggler-bar bar2"></span>
          <span class="navbar-toggler-bar bar3"></span>
        </span>
      </button>
      <div
        class="collapse navbar-collapse w-100 pt-3 pb-2 py-lg-0"
        id="navigation"
      >
        <ul class="navbar-nav navbar-nav-hover ms-auto">
          <li class="nav-item dropdown dropdown-hover mx-2">
            <RouterLink
              :to="{ name: 'tentang' }"
              class="nav-link ps-2 d-flex cursor-pointer align-items-center"
            >
              <span>Tentang</span>
            </RouterLink>
          </li>
          <li class="nav-item dropdown dropdown-hover mx-2">
            <RouterLink
              :to="{ name: 'presentation' }"
              class="nav-link ps-2 d-flex cursor-pointer align-items-center"
            >
              <span>Layanan</span>
            </RouterLink>
          </li>
          <li class="nav-item dropdown dropdown-hover mx-2">
            <RouterLink
              :to="{ name: 'konsultasi' }"
              class="nav-link ps-2 d-flex cursor-pointer align-items-center"
            >
              <span>Konsultasi</span>
            </RouterLink>
          </li>
        </ul>
        <ul class="navbar-nav d-lg-block d-none">
          <li class="nav-item mx-2">
            <template v-if="!isLoggedIn">
              <RouterLink
                :to="konsultasi.route"
                class="btn btn-sm mb-0"
                :class="konsultasi.color"
                @click.native="smoothToPricing('pricing-soft-ui')"
                >{{ konsultasi.label }}</RouterLink
              >
            </template>
            <template v-else>
              <div
                class="dropdown text-end badge d-flex align-items-center p-1 pe-2 text-info bg-info-subtle border border-info rounded-pill"
              >
                <a
                  href="#"
                  class="d-block link-body-emphasis text-decoration-none dropdown-toggle me-2"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  <img
                    :src="
                      user.foto ||
                      'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'
                    "
                    width="32"
                    height="32"
                    class="rounded-circle me-1"
                  />
                </a>
                <ul class="dropdown-menu dropdown-menu-end text-small">
                  <li>
                    <RouterLink
                      to="/settings/profil"
                      class="nav-link ps-2 d-flex cursor-pointer align-items-center"
                    >
                      <span>Settings</span>
                    </RouterLink>
                  </li>
                  <li>
                    <RouterLink
                      to="/settings/booking"
                      class="nav-link ps-2 d-flex cursor-pointer align-items-center"
                    >
                      <span>Reservasi</span>
                    </RouterLink>
                  </li>
                  <li>
                    <RouterLink
                      to="/settings/notif"
                      class="nav-link ps-2 d-flex cursor-pointer align-items-center"
                    >
                      <span>Notifikasi</span>
                    </RouterLink>
                  </li>
                  <li><hr class="dropdown-divider" /></li>
                  <li><a class="dropdown-item" @click="logout">Sign out</a></li>
                </ul>
              </div>
            </template>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <!-- End Navbar -->
</template>
