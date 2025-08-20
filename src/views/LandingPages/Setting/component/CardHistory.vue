<template>
  <div class="card border-0 shadow-sm">
    <div class="card-header px-4 pt-4 pb-2">
      <h4 class="card-title">Daftar History</h4>
      <p class="card-text">
        <small class="text-muted mb-4">
          Anda dapat melihat daftar history konsultasi anda disini!
        </small>
      </p>
    </div>
    <hr class="hairline mb-0" />
    <div class="card-body m-3">
      <div v-if="loading" class="text-center">
        <img src="@/assets/loading_2.svg" alt="Loading" />
        <p>Loading...</p>
      </div>
      <div v-else>
        <table class="table table-bordered" v-if="histories.length > 0">
          <thead>
            <tr>
              <th scope="col" class="text-center">Tanggal</th>
              <th scope="col" class="text-center">Nama Petugas</th>
              <th scope="col" class="text-center">Status</th>
              <th scope="col" class="text-center">Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(history, index) in histories" :key="index">
              <td>
                <small>{{ history.tanggal_konsultasi }}</small>
              </td>
              <td>
                <small>{{ history.petugas.nama_petugas }}</small>
              </td>
              <td>
                <span
                  class="badge bg-success"
                  v-if="history.status == 'Selesai'"
                  >Selesai</span
                >
                <span
                  class="badge bg-danger"
                  v-else-if="history.status == 'Dibatalkan'"
                  >Dibatalkan</span
                >
              </td>
              <td class="d-flex justify-content-center align-items-center">
                <button
                  class="btn btn-info me-2 btn-sm"
                  v-if="history.status == 'Selesai' && history.rating == null"
                  @click="showModal(history.id)"
                >
                  Ulasan
                </button>
                <button
                  class="btn btn-warning me-2 btn-sm"
                  v-if="history.status == 'Selesai'"
                  @click="showDetail(history.uuid)"
                >
                  Detail
                </button>
                <button
                  class="btn btn-warning btn-sm"
                  v-else-if="history.status == 'Dibatalkan'"
                  @click="showDetail(history.uuid)"
                >
                  Detail
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="text-center">
          <p>Tidak ada History Ditemukan</p>
        </div>
      </div>
    </div>
    <ModalUlasan
      v-if="isModalVisible"
      :historyId="historyId"
      @close="closeModal"
      @loading="setLoading"
      @hideMainModal="hideMainModal"
      @success="setSuccess"
      :isModalMainVisible="isModalMainVisible"
    />

    <!-- Modal Loading -->
    <div v-if="isLoading" class="modal-backdrop">
      <div class="modal position-static d-block p-4 py-md-5">
        <div class="modal-dialog" role="document">
          <div class="modal-content rounded-4 shadow px-2">
            <div class="modal-body py-5">
              <div class="d-flex justify-content-center align-items-center">
                <div class="spinner-border text-success" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <span class="ms-3">Memproses ulasan...</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Success -->
    <div v-if="isSuccess" class="modal-backdrop">
      <div class="modal position-static d-block p-4 py-md-5">
        <div class="modal-dialog" role="document">
          <div class="modal-content rounded-4 shadow px-2">
            <div class="modal-body py-5">
              <div class="d-flex justify-content-center align-items-center">
                <i
                  class="bi bi-check-circle text-success"
                  style="font-size: 2rem"
                ></i>
                <span class="ms-3">Ulasan berhasil dikirim.</span>
              </div>
              <div class="d-flex justify-content-center mt-3">
                <button
                  type="button"
                  class="btn btn-success"
                  @click="closeSuccessModal"
                >
                  Tutup
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ModalUlasan from "./ModalUlasan.vue";
import { apiService } from "@/api/ApiService";

export default {
  components: { ModalUlasan },
  data() {
    return {
      histories: [],
      loading: true,
      isModalVisible: false,
      historyId: "",
      isLoading: false,
      isSuccess: false,
      isModalMainVisible: true,
    };
  },
  mounted() {
    this.fetchHistories();
  },
  methods: {
    async fetchHistories() {
      this.loading = true;
      try {
        const storedUser = localStorage.getItem("user");
        const parsedUser = JSON.parse(storedUser);
        if (parsedUser) {
          const response = await apiService.getHistoryByUser(parsedUser.id);
          const sortedHistory = response.data.data.sort((a, b) => {
            return (
              new Date(b.tanggal_konsultasi) - new Date(a.tanggal_konsultasi)
            );
          });
          this.histories = sortedHistory;
        } else {
          throw new Error("User tidak ditemukan di localStorage");
        }
      } catch (error) {
        console.error("Error fetching bookings:", error);
      } finally {
        this.loading = false;
      }
    },
    showDetail(historyId) {
      this.$router.push({
        name: "CardDetailHistory",
        params: { uuid: historyId },
      });
    },
    showModal(historyId) {
      this.historyId = historyId;
      this.isModalVisible = true;
      this.isModalMainVisible = true;
    },
    closeModal() {
      this.isModalVisible = false;
    },
    setLoading(isLoading) {
      this.isLoading = isLoading;
    },
    setSuccess(isSuccess) {
      this.isSuccess = isSuccess;
    },
    hideMainModal() {
      this.isModalMainVisible = false;
    },
    closeSuccessModal() {
      this.isSuccess = false;
      window.location.href = "/settings/history";
    },
  },
};
</script>

<style scoped>
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

.hairline {
  width: 100%;
  border: 0;
  border-top: 1px solid #141e2a;
  margin-bottom: 20px;
}

.btn-outline-danger:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
