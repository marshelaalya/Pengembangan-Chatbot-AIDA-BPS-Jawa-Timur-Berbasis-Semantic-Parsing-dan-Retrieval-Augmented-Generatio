<template>
  <div id="NewsCard" class="">
    <div class="card w-100 mb-3">
      <div class="row g-0">
        <div class="col-md-2 align-self-center">
          <img
            :src="item.thumbnail"
            class="rounded-start card-img-top img-thumbnail"
            alt="publication img"
            height="75"
          />
        </div>
        <div class="col-md-10">
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ item.title }}</h5>
            <small>Subject: {{ item.subj }}</small>
            <div class="row mt-5">
              <div class="col">
                <small>Release: {{ item.rl_date }}</small>
              </div>
              <div class="col d-flex justify-content-end">
                <a
                  :href="item.pdf"
                  class="btn btn-primary mx-1"
                  style="font-size: 14px"
                  target="_blank"
                >
                  Download PDF
                  <i class="bi bi-file-earmark-arrow-down-fill"></i>
                </a>
                <a
                  :href="item.slide"
                  class="btn btn-primary mx-1"
                  style="font-size: 14px"
                  target="_blank"
                >
                  Open Slide
                  <i class="bi bi-file-earmark-arrow-down-fill"></i>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CardNews",
  props: ["item", "keyword"],
};
</script>

<style></style>
