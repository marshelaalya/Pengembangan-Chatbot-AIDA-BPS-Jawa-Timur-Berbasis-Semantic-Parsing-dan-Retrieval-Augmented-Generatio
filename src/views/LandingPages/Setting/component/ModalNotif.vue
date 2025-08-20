<template>
  <div class="modal-backdrop">
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
              Notification
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
            <div class="d-flex main-content align-items-start">
              <img
                src="@/assets/img/mail.png"
                alt="Image"
                class="img-fluid w-25 h-25 mr-3 "
              />
              <div class="content-text px-4 pe-0">
                <h3 class="mb-4">Informasi Konsultasi</h3>
                <p class="mb-4">
                  {{ notif.data.message }}
                </p>
                <div class="d-flex">  
                  <div class="ml-auto" v-if="notif.data.action != null">
                    <a
                      class="btn btn-primary px-4"
                      :href="notif.data.action"
                      target="_blank"
                    >
                      <span>Link Meeting</span>
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import { defineComponent } from 'vue';
const router = useRouter();

export default defineComponent({
  name: "ModalNotif",
  props: {
    notif: {
      type: Object,
      required: true,
    },
  },
  setup() {
    

    const navigateToSettings = () => {
      router.push({ name: "CardNotif" });
      // this.$router.go(0);
    };

    return {
      navigateToSettings,
    };
  },
  methods: {
    close() {
      this.$emit("close");
      // Refresh the page after closing the modal
      // router.push({ name: "CardProfil" });
      this.$router.go(0);
    },
  },
});
</script>

<style>
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
  color: #4aae9b;
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


.buttons {
  position: relative;
  top: 36px;
}
</style>
