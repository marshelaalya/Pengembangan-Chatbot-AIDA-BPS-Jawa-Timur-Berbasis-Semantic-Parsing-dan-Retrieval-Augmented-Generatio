<template>
  <div v-if="isModalMainVisible">
    <!-- Modal Backdrop -->
    <div class="modal-backdrop">
      <div
        class="modal position-static d-block p-4 py-md-5"
        tabindex="-1"
        role="dialog"
        id="modalSheet"
      >
        <div class="modal-dialog" role="document">
          <div class="modal-content rounded-4 shadow px-2">
            <div class="modal-header border-bottom-0">
              <h1 class="modal-title fs-5 fw-semibold text-danger">
                Ingin membatalkan Reservasi?
              </h1>
              <button
                type="button"
                class="btn-close-white"
                aria-label="Close"
                @click="close"
              >
                <i class="bi bi-x"></i>
              </button>
            </div>
            <div class="modal-body py-0">
              <p>
                Apakah Anda yakin ingin
                <strong>membatalkan reservasi</strong> yang telah dibuat? Harap
                dicatat bahwa Anda mungkin harus mengatur ulang seluruh proses
                reservasi jika Anda memutuskan untuk membatalkan.
              </p>
            </div>
            <div class="modal-body py-0">
              <p>
                Harap berikan <strong>Alasan</strong> mengapa Anda ingin
                membatalkan reservasi Anda.
              </p>
              <textarea
                v-model="cancelReason"
                class="w-100 p-2"
                rows="4"
                placeholder="Harap isikan minimal 30 kata."
              ></textarea>
            </div>
            <div
              class="modal-footer flex-column align-items-stretch w-100 gap-2 pb-3 border-top-0"
            >
              <button
                type="button"
                class="btn btn-outline-danger"
                @click="cancelReservation"
                :disabled="cancelReason.length < 30"
              >
                Batalkan Reservasi
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from "@/api/ApiService";

export default {
  name: "Modal",
  props: {
    bookingId: {
      type: String,
      required: true,
    },
    isModalMainVisible: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      cancelReason: "",
    };
  },
  methods: {
    close() {
      this.$emit("close");
    },
    async cancelReservation() {
      if (this.cancelReason.length < 10) {
        alert("Harap isikan minimal 10 kata untuk alasan pembatalan.");
        return;
      }
      this.$emit("loading", true);
      this.$emit("hideMainModal");
      try {
        const data = {
          alasan_pembatalan: this.cancelReason,
        };
        await apiService.cancelConsultation(this.bookingId, data);
        console.log(`Booking ID ${this.bookingId} dibatalkan.`);
        this.$emit("loading", false);
        this.$emit("success", true);
      } catch (error) {
        console.error("Error cancelling reservation:", error);
        this.$emit("loading", false);
        alert(
          "Terjadi kesalahan saat membatalkan reservasi. Silakan coba lagi."
        );
      }
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

.btn-outline-danger:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
