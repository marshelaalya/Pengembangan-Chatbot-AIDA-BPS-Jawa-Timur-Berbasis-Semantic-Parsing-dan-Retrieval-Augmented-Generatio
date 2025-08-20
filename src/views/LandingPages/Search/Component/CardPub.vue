<template>
  <div id="PubCard" class="">
    <div class="card w-100 mb-3">
      <div class="row g-0">
        <div class="col-md-2 align-self-center">
          <img
            :src="item.cover"
            class="img-fluid rounded-start card-img-top "
            alt="publication img"
          />
        </div>
        <div class="col-md-10">
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ item.title }}</h5>
            <small>ISSN: {{ item.issn }}</small>
            <br />
            <p class="card-text">{{ truncateAbstract(item.abstract, 20) }}</p>
            <!-- Truncate abstract -->
            <div class="row mt-5">
              <div class="col">
                <small>Release: {{ item.rl_date }}</small>
              </div>
              <div class="col d-flex justify-content-end">
                <a
                  :href="item.pdf"
                  class="btn btn-primary"
                  style="font-size: 14px"
                  target="_blank"
                >
                  Open PDF
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
  name: "CardPub",
  props: ["item", "keyword"],
  methods: {
    truncateAbstract(abstract, maxLength) {
      if (!abstract) return ""; // Handle case when abstract is not provided
      const words = abstract.split(" ");
      if (words.length <= maxLength) return abstract; // Return the full abstract if it contains less than or equal to maxLength words
      const truncated = words.slice(0, maxLength).join(" ");
      return truncated + "..."; // Append ellipsis
    },
  },
};
</script>

<style></style>
