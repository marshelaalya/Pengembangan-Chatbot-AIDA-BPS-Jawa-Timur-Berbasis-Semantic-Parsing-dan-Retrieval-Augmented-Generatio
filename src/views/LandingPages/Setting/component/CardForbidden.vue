<template>
  <div class="card border-0 shadow-sm">
    <div class="card-header px-4 pt-4 pb-2">
      <h4 class="card-title text-center">Forbidden</h4>
      <p class="card-text text-center">
        <small class="text-muted mb-4">Anda tidak dapat mengakses data ini</small>
      </p>
    </div>
    <div class="card-body m-3 py-0 px-1">
      <div  class="text-center">
        <img src="@/assets/img/404-error.png" alt="Loading" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
  },
  mounted() {
  },
  methods: {
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
