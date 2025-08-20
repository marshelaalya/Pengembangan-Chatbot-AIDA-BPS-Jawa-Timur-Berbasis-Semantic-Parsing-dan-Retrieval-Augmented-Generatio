<template>
  <div class="card border-0 shadow-sm">
    <div class="card-header px-4 pt-4 pb-2">
      <h4 class="card-title">Notifikasi</h4>
      <p class="card-text">
        <small class="text-muted mb-4">Anda dapat memantau pemberitahuan disini</small>
      </p>
    </div>
    <div class="card-body m-3 py-0 px-1">
      <div v-if="loading" class="text-center">
        <img src="@/assets/loading_2.svg" alt="Loading" />
        <p>Loading...</p>
      </div>
      <div v-else>
        <div class="list-group" v-if="notifs.length > 0">
          <notification-item
            v-for="notif in notifs"
            :key="notif.id"
            :notif="notif"
            @click="showModal(notif.id,notif)"
          />
        </div>
        <div v-else class="text-center">
          <p>Tidak ada Notifikasi yang masuk</p>
        </div>
      </div>
    </div>
    <Modal v-if="isModalVisible" :notif="notif" @close="closeModal" />
  </div>
</template>

<script>
import Modal from "./ModalNotif.vue";
import { apiService } from "@/api/ApiService";
import NotificationItem from "./NotificationItem.vue"; // Tambahkan ini

export default {
  components: { Modal, NotificationItem }, // Tambahkan NotificationItem
  data() {
    return {
      notifs: [],
      loading: true,
      isModalVisible: false,
      notif:[],
    };
  },
  mounted() {
    this.fetchNotifs();
  },
  methods: {
    async fetchNotifs() {
      this.loading = true;
      try {
        const storedUser = localStorage.getItem("user");
        const parsedUser = JSON.parse(storedUser);
        if (parsedUser) {
          const response = await apiService.getNotification(parsedUser.email_google);
          const sortedNotifs = response.data.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
          this.notifs = sortedNotifs;
        } else {
          throw new Error("User tidak ditemukan di localStorage");
        }
      } catch (error) {
        console.error("Error fetching notifications:", error);
      } finally {
        this.loading = false;
      }
    },
    async showModal(notifId,notif) {
      this.notif = notif;
      this.isModalVisible = true;
      try {
        const storedUser = localStorage.getItem("user");
        const parsedUser = JSON.parse(storedUser);
        if (parsedUser) {
          const response = await apiService.setNotificationRead(parsedUser.email_google,notifId);
          console.log(response.data)
        } else {
          throw new Error("User tidak ditemukan di localStorage");
        }
      } catch (error) {
        console.error("Error fetching notifications:", error);
      } finally {
        this.loading = false;
      }
    },
    closeModal() {
      this.isModalVisible = false;
    },
  },
};
</script>

<style scoped>
/* style tetap sama */
.modal-backdrop {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #0000009c;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  box-shadow: 2px 2px 20px 1px;
  overflow-x: auto;
  display: flex;
  flex-direction: column;
}

.modal-header,
.modal-footer {
  padding: 15px;
  display: flex;
}

.modal-header {
  position: relative;
  border-bottom: 1px solid #eeeeee;
  justify-content: space-between;
}

.modal-footer {
  border-top: 1px solid #eeeeee;
  flex-direction: column;
  justify-content: flex-end;
}

.modal-body {
  position: relative;
}

textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: none;
}

.btn-outline-danger:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
