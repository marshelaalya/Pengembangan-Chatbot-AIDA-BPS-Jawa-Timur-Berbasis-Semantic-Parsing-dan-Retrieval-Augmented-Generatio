<template>
  <div class="card border-0 shadow-sm rounded-4">
    <div class="card-body">
      <ul class="list-group list-group-flush text-start">
        <li
          v-for="card in cards"
          :key="card.id"
          class="list-group-item btn btn-outline-dark bg-outline-dark text-start"
          :class="{ active: $route.name == card.id }"
          @click="$emit('select-card', card.id)"
        >
          <i :class="card.icon"></i> {{ card.title }}
        </li>
        <li
          class="list-group-item btn btn-outline-dark bg-outline-dark text-start"
          @click="logout"
        >
          <i class="bi bi-box-arrow-right"></i> Logout
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { googleLogout } from "vue3-google-login";
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      cards: [
        {
          id: "CardProfil",
          title: "Profil Setting",
          icon: "bi bi-person-fill-gear",
        },
        {
          id: "CardBooking",
          title: "Reservasi Konsultasi",
          icon: "bi bi-journal-bookmark-fill",
        },
        {
          id: "CardHistory",
          title: "Riwayat Konsultasi",
          icon: "bi bi-clock-history",
        },
        {
          id: "CardNotif",
          title: "Notifikasi",
          icon: "bi bi-bell-fill",
        },
      ],
    };
  },
  methods: {
    logout() {
      googleLogout();
      localStorage.clear();
      this.$router.push("/konsultasi");
    },
  },
};
</script>

<style scoped>
.list-group-item-divider {
  border-bottom: 1px solid #191313; /* Warna dan ketebalan garis pemisah */
}

.list-group-item-divider:last-child {
  border-bottom: none; /* Hilangkan garis pemisah pada item terakhir */
}
</style>
