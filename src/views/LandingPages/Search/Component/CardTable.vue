<template>
  <div id="TableCard">
    <div class="card w-100 mb-3">
      <div class="card-body d-flex flex-column">
        <h5 class="card-title">{{ item.title }}</h5>
        <p class="card-text">Subject: {{ item.subj }}</p>
        <div class="row">
          <div class="col">
            <small>Update: {{ item.updt_date }}</small>
          </div>
          <div class="col d-flex justify-content-end">
            <a
              :href="item.excel"
              class="btn btn-primary"
              style="font-size: 14px"
              >Download Excel <i class="bi bi-file-earmark-arrow-down-fill"></i
            ></a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CardTable",
  props: ["item"],
};
</script>

<style>
/* Add any custom styles if needed */
</style>
