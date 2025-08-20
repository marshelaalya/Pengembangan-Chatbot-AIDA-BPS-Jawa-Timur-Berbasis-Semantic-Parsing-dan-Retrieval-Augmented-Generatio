<template>
  <div class="card border-0 shadow-sm">
    <div class="card-header p-4 d-flex align-items-center pb-0">
      <button class="btn m-0" @click="goBack">
        <h5 class="mb-0 bi bi-arrow-left"></h5>
      </button>
      <h4 class="card-title ms-3">Detail Reservasi</h4>
    </div>
    
    <div class="card-body p-4">
      <div v-if="loading" class="text-center">
        <img src="/assets/loading_2.svg" alt="Loading..." />
        <p>Loading...</p>
      </div>
      <div v-else class="container">
        <div v-if="booking.status == 'Diajukan'">
          <h5 class="fw-semibold text-warning mb-0">
            <i class="bi bi-hourglass-split me-2"></i> Reservasi Konsultasi Sedang Diajukan
          </h5>
          <small class="mb-4 text-muted">Anda akan segera menerima email konfirmasi.</small>
        </div>
        <div v-else-if="booking.status == 'Disetujui'">
          <h5 class="fw-semibold text-info mb-0">
            <i class="bi bi-check-circle-fill me-2"></i> Reservasi Konsultasi Sudah Disetujui
          </h5>
          <small class="mb-4 text-muted">Mohon lihat email Anda untuk detail konfirmasi.</small>
        </div>
        <div class="mt-4">
          <h4 class="fw-semibold">Tentang Konsultasi</h4>
          <div class="mt-3">
            <p class="text-muted mb-1 fw-semibold">
              <i class="bi bi-camera-video-fill me-2"></i> Link Pertemuan:
            </p>
            <span class="ms-4" v-if="booking.status == 'Diajukan'">
              Link akan diberitahukan setelah reservasi disetujui.
            </span>
            <span class="ms-4" v-else-if="booking.status == 'Disetujui'">
              <a :href="booking.link_meeting" target="_blank">{{ booking.link_meeting }}</a>
            </span>
          </div>
          <div class="mt-3">
            <p class="text-muted mb-1 fw-semibold">
              <i class="bi bi-chat-left-quote-fill me-2"></i> Topik Konsultasi:
            </p>
            <span class="ms-4">{{ booking.topik_diskusi }}</span>
          </div>
        </div>
        <div class="row mt-4">
          <div class="col-6">
            <p class="fw-semibold text-muted mb-2">
              <i class="bi bi-person-fill me-2"></i> Informasi Petugas:
            </p>
            <p class="mb-0 ms-4">{{ booking.petugas.nama_petugas }}</p>
            <p class="mb-0 ms-4">{{ booking.satker_agen }}</p>
          </div>
          <div class="col-6">
            <p class="fw-semibold text-muted mb-2">
              <i class="bi bi-calendar2-week-fill me-2"></i> Jadwal Konsultasi:
            </p>
            <p class="mb-0 ms-4">{{ booking.tanggal_konsultasi }}</p>
            <p class="mb-0 ms-4">{{ booking.waktu_konsultasi }}</p>
          </div>
        </div>
        <hr />
        <div class="d-block">
          <p class="mb-0">
            <small class="mb-2 fw-semibold">Tanggal Pembuatan Reservasi</small>
          </p>
          <p>
            <small>{{ booking.created_at }}</small>
          </p>
          <button class="btn btn-danger w-100 mt-4" type="button" @click="showModal">
            Batalkan
          </button>
        </div>
      </div>
    </div>
    <Modal
      v-if="isModalVisible"
      @close="closeModal"
      @loading="setLoading"
      @success="setSuccess"
      @hideMainModal="hideMainModal"
      :bookingId="bookingId"
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
                <span class="ms-3">Memproses pembatalan...</span>
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
                <span class="ms-3">Reservasi berhasil dibatalkan.</span>
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
import { apiService } from "@/api/ApiService";
import Modal from "./Modal.vue";

export default {
  name: "CardDetailBooking",
  components: { Modal },
  data() {
    return {
      booking: {},
      loading: true,
      isModalVisible: false,
      isLoading: false,
      isSuccess: false,
      isModalMainVisible: true,
      bookingId: this.$route.params.uuid, // Ambil parameter dari route
    };
  },
  created() {
    this.fetchBookingDetails(this.bookingId);
  },
  methods: {
    async fetchBookingDetails(bookingId) {
      this.loading=true
      try {
        const response = await apiService.getConsultation(bookingId);
        this.booking = response.data.data;
        if(response.data==404){
          this.$router.push({
            name: "CardForbidden"
          });
        }
        // console.log(response);
      } catch (error) {
        console.error("Error fetching booking details:", error);
      } finally {
        this.loading = false;
      }
    },
    goBack() {
      this.$router.go(-1);
    },
    showModal() {
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
      window.location.href = "/settings/booking";
    },
  },
};
</script>

<style scoped>
.card-body {
  padding: 2rem;
}

.list-group-item {
  padding: 0.5rem 1rem;
  border: none;
}

.list-group-item strong {
  font-weight: 500;
}

.btn-danger {
  width: 100%;
  margin-top: 1rem;
}

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
