<template>
  <div class="modal-backdrop" v-if="isModalMainVisible">
    <div
      class="modal position-static d-block p-4 py-md-5"
      id="ratingModal"
      tabindex="-1"
      aria-labelledby="ratingModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content rounded-4 shadow px-2">
          <div class="modal-header border-bottom-0">
            <h5
              class="modal-title fs-4 fw-semibold text-success"
              id="ratingModalLabel"
            >
              Nilai dan Ulasan
            </h5>
            <button
              type="button"
              class="btn-close-white"
              data-bs-dismiss="modal"
              aria-label="Close"
              @click="close"
            >
              <i class="bi bi-x"></i>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="sendReview">
              <div class="mb-3 text-center">
                <label for="review" class="form-label">
                  Berikan Nilai dan Ulasan terkait pelayanan kami
                </label>
                <div class="rating">
                  <input
                    type="radio"
                    name="rating"
                    value="10"
                    id="10"
                    class="star"
                    v-model="rating"
                  /><label for="10" class="star">☆</label>
                  <input
                    type="radio"
                    name="rating"
                    value="9"
                    id="9"
                    class="star"
                    v-model="rating"
                  /><label for="9" class="star">☆</label>
                  <input
                    type="radio"
                    name="rating"
                    value="8"
                    id="8"
                    class="star"
                    v-model="rating"
                  /><label for="8" class="star">☆</label>
                  <input
                    type="radio"
                    name="rating"
                    value="7"
                    id="7"
                    class="star"
                    v-model="rating"
                  /><label for="7" class="star">☆</label>
                  <input
                    type="radio"
                    name="rating"
                    value="6"
                    id="6"
                    class="star"
                    v-model="rating"
                  /><label for="6" class="star">☆</label>
                  <input
                    type="radio"
                    name="rating"
                    value="5"
                    id="5"
                    class="star"
                    v-model="rating"
                  /><label for="5" class="star">☆</label>
                  <input
                    type="radio"
                    name="rating"
                    value="4"
                    id="4"
                    class="star"
                    v-model="rating"
                  /><label for="4" class="star">☆</label>
                  <input
                    type="radio"
                    name="rating"
                    value="3"
                    id="3"
                    class="star"
                    v-model="rating"
                  /><label for="3" class="star">☆</label>
                  <input
                    type="radio"
                    name="rating"
                    value="2"
                    id="2"
                    class="star"
                    v-model="rating"
                  /><label for="2" class="star">☆</label>
                  <input
                    type="radio"
                    name="rating"
                    value="1"
                    id="1"
                    class="star"
                    v-model="rating"
                  /><label for="1" class="star">☆</label>
                </div>
                <textarea
                  v-model="review"
                  class="form-control mt-3 ps-2"
                  id="review"
                  rows="3"
                  placeholder="Silahkan masukan saran"
                  style="border: 1px solid #ced4da;"
                ></textarea>
                <p class="mt-3">
                  <small>
                    Penilaian dan ulasan Anda sangat penting bagi kami untuk
                    meningkatkan kualitas layanan Konsultasi Online BPS Provinsi
                    Jawa Timur.
                  </small>
                </p>
                <button
                  type="submit"
                  class="btn btn-success py-1 rounded rounded-4"
                  :disabled="!isFormValid"
                >
                  Submit
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from "@/api/ApiService";

export default {
  name: "ModalUlasan",
  props: {
    historyId: {
      required: true,
    },
    isModalMainVisible: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      review: "",
      rating: "",
    };
  },
  computed: {
    isFormValid() {
      return this.review.trim() && this.rating;
    },
  },
  methods: {
    async sendReview() {
      if (!this.isFormValid) {
        throw new Error(
          "Harap isi semua bagian ulasan dan pilih nilai rating."
        );
      }

      this.$emit("loading", true);
      this.$emit("hideMainModal");
      try {
        const data = {
          rating: this.rating,
          kritik_saran: this.review,
        };
        await apiService.giveFeedback(this.historyId, data);
        console.log(`History ID ${this.historyId} sudah di review.`);
        this.$emit("loading", false);
        this.$emit("success", true);
      } catch (error) {
        this.$emit("loading", false);
        console.error("Error saat melakukan review:", error.message);
        alert("Gagal mengirim ulasan. Silakan coba lagi.");
      }
    },
    close() {
      this.$emit("close");
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
  border-bottom: 1px solid #eeeeee;
  justify-content: space-between;
  color: #4aae9b;
}

.modal-body {
  position: relative;
}

.rating {
  display: flex;
  flex-direction: row-reverse;
  justify-content: center;
}

.rating > input {
  display: none;
}

.rating > label {
  position: relative;
  width: 1em;
  font-size: 30px;
  font-weight: 300;
  color: #ffd600;
  cursor: pointer;
}

.rating > label::before {
  content: "\2605";
  position: absolute;
  opacity: 0;
}

.rating > label:hover:before,
.rating > label:hover ~ label:before {
  opacity: 1 !important;
}

.rating > input:checked ~ label:before {
  opacity: 1;
}

.rating:hover > input:checked ~ label:before {
  opacity: 0.4;
}
</style>
