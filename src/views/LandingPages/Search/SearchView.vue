<template>
  <div>
    <NavbarLogin />
    <!-- SEARCH BAR -->
    <SearchComponent @search-updated="handleSearchUpdate" />

    <!-- FILTER SECTION -->
    <div class="container wrapper">
      <br />
      <div class="row">
        <div class="col-sm-12 col-md-8">
          <ul
            class="nav nav-pills mb-3 align-items-center"
            id="pills-tab"
            role="tablist"
          >
            <li class="nav-item" role="presentation">
              <button
                :class="{ active: activeTab == 'table' }"
                class="btn btn-outline-secondary m-1 rounded rounded-3"
                id="table-search-tab"
                data-bs-toggle="pill"
                @click="handleButtonClick('table')"
                data-bs-target="#table-search"
                type="button"
                role="tab"
                aria-controls="table-search"
                aria-selected="false"
              >
                Tabel
              </button>
            </li>
            <li class="nav-item" role="presentation">
              <button
                :class="{ active: activeTab == 'pub' }"
                class="btn btn-outline-secondary m-1"
                id="pub-search-tab"
                data-bs-toggle="pill"
                data-bs-target="#pub-search"
                type="button"
                role="tab"
                aria-controls="pub-search"
                aria-selected="false"
                @click="handleButtonClick('pub')"
              >
                Publikasi
              </button>
            </li>

            <li class="nav-item" role="presentation">
              <button
                :class="{ active: activeTab == 'news' }"
                class="btn btn-outline-secondary m-1"
                id="news-search-tab"
                data-bs-toggle="pill"
                data-bs-target="#news-search"
                type="button"
                role="tab"
                aria-controls="news-search"
                aria-selected="false"
                @click="handleButtonClick('news')"
              >
                Berita Resmi Statistik
              </button>
            </li>
          </ul>
        </div>
        <div
          class="col d-flex justify-content-start align-items-center mb-3 ms-2"
        >
          <i
            class="bi bi-sliders me-2"
            style="color: rgba(51, 51, 51, 0.692)"
          ></i>

          <!-- FILTER SELECT REGION -->
          <d3>Wilayah:</d3>
          <div class="ms-2 dropdown-center">
            <select
              class="form-select"
              v-model="selectedRegion"
              aria-label="Default select example"
            >
              <option
                v-for="(region, index) in regions"
                :key="index"
                :value="region.value"
              >
                {{ region.label }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <div class="clearfix"></div>
      <hr />

      <!-- LOADING STATE -->
      <div v-if="loading" class="text-center mb-3">
        <p>Loading...</p>
        <img src="/assets/loading_2.svg" height="75" width="75" />
      </div>

      <div v-else>
        <p class="mb-3">Hasil Pencarian : {{ searchResult }}</p>
      </div>

      <!-- HASIL PENCARIAN -->
      <div v-if="noData" class="alert alert-warning" role="alert">
        Maaf, data tidak tersedia.
      </div>

      <div class="tab-content" id="pills-tabContent">
        <div
          class="tab-pane fade"
          :class="{ 'show active': activeTab == 'pub' }"
          id="pub-search"
          role="tabpanel"
          aria-labelledby="pub-search-tab"
          tabindex="0"
        >
          <div v-if="resultPub && resultPub.length > 0">
            <div v-for="pub in resultPub" :key="pub.pub_id">
              <CardPub :item="pub" :keyword="searchResult" />
            </div>
          </div>
        </div>
        <div
          class="tab-pane fade show active"
          :class="{ 'show active': activeTab == 'table' }"
          id="table-search"
          role="tabpanel"
          aria-labelledby="table-search-tab"
          tabindex="0"
        >
          <div v-if="resultTable && resultTable.length > 0">
            <div v-for="table in resultTable" :key="table.table_id">
              <CardTable :item="table" />
            </div>
          </div>
        </div>
        <div
          class="tab-pane fade"
          :class="{ 'show active': activeTab == 'news' }"
          id="news-search"
          role="tabpanel"
          aria-labelledby="news-search-tab"
          tabindex="0"
        >
          <div v-if="resultNews && resultNews.length > 0">
            <div v-for="news in resultNews" :key="news.brs_id">
              <CardNews :item="news" />
            </div>
          </div>
        </div>
      </div>

      <div class="push"></div>

      <div class="container pt-5">
        <div class="row">
          <div class="col-lg-4 mx-auto">
            <div class="pagination-container">
              <MaterialPagination>
                <MaterialPaginationItem
                  prev
                  @click="handlePageChange(currentPage - 1)"
                />
                <MaterialPaginationItem
                  v-for="page in totalPages"
                  :key="page"
                  :label="page"
                  :active="page == currentPage"
                  @click="handlePageChange(page)"
                />
                <MaterialPaginationItem
                  next
                  @click="handlePageChange(currentPage + 1)"
                />
              </MaterialPagination>
            </div>
          </div>
        </div>
      </div>
    </div>
    <DefaultFooter />
  </div>
</template>

<script>
import SearchComponent from "@/views/LandingPages/Search/Component/Search.vue";
import CardTable from "@/views/LandingPages/Search/Component/CardTable.vue";
import CardPub from "@/views/LandingPages/Search/Component/CardPub.vue";
import CardNews from "@/views/LandingPages/Search/Component/CardNews.vue";
import DefaultFooter from "@/examples/footers/FooterDefault.vue";
import NavbarLogin from "@/examples/navbars/NavbarLogin.vue";
import MaterialPagination from "@/components/MaterialPagination.vue";
import MaterialPaginationItem from "@/components/MaterialPaginationItem.vue";
import axios from "axios";

const apiKey = "2ad01e6a21b015ea1ff8805ced02600c/";

export default {
  name: "SearchView",
  components: {
    SearchComponent,
    CardTable,
    CardPub,
    CardNews,
    DefaultFooter,
    NavbarLogin,
    MaterialPagination,
    MaterialPaginationItem,
  },
  props: {
    mfd: {
      type: String,
      default: "3500",
    },
  },
  data() {
    return {
      searchResult: "",
      resultTable: [],
      resultPub: [],
      resultNews: [],
      activeTab: "table",
      key: "",
      resultType: "resultTable",
      selectedRegion: this.mfd,
      currentPage: 1,
      totalPages: 1,
      noData: false,
      regions: [
        { label: "Jawa Timur", value: "3500" },
        { label: "Kab. Bangkalan", value: "3526" },
        { label: "Kab. Banyuwangi", value: "3510" },
        { label: "Kab. Blitar", value: "3505" },
        { label: "Kab. Bojonegoro", value: "3522" },
        { label: "Kab. Bondowoso", value: "3511" },
        { label: "Kab. Gresik", value: "3525" },
        { label: "Kab. Jember", value: "3509" },
        { label: "Kab. Jombang", value: "3517" },
        { label: "Kab. Kediri", value: "3506" },
        { label: "Kab. Lamongan", value: "3524" },
        { label: "Kab. Lumajang", value: "3508" },
        { label: "Kab. Madiun", value: "3519" },
        { label: "Kab. Magetan", value: "3520" },
        { label: "Kab. Malang", value: "3507" },
        { label: "Kab. Mojokerto", value: "3516" },
        { label: "Kab. Nganjuk", value: "3518" },
        { label: "Kab. Ngawi", value: "3521" },
        { label: "Kab. Pacitan", value: "3501" },
        { label: "Kab. Pamekasan", value: "3528" },
        { label: "Kab. Pasuruan", value: "3514" },
        { label: "Kab. Ponorogo", value: "3502" },
        { label: "Kab. Probolinggo", value: "3513" },
        { label: "Kab. Sampang", value: "3527" },
        { label: "Kab. Sidoarjo", value: "3515" },
        { label: "Kab. Situbondo", value: "3512" },
        { label: "Kab. Sumenep", value: "3529" },
        { label: "Kab. Trenggalek", value: "3503" },
        { label: "Kab. Tuban", value: "3523" },
        { label: "Kab. Tulungagung", value: "3504" },
        { label: "Kota Batu", value: "3579" },
        { label: "Kota Blitar", value: "3572" },
        { label: "Kota Kediri", value: "3571" },
        { label: "Kota Madiun", value: "3577" },
        { label: "Kota Malang", value: "3573" },
        { label: "Kota Mojokerto", value: "3576" },
        { label: "Kota Pasuruan", value: "3575" },
        { label: "Kota Probolinggo", value: "3574" },
        { label: "Kota Surabaya", value: "3578" },
      ],
      loading: false,
    };
  },
  created() {
    this.key = this.$route.query.searchQuery || "";
    this.searchResult = this.$route.query.searchQuery || "";

    // // Ambil nilai mfd dari URL dan gunakan sebagai selectedRegion
    // this.selectedRegion = this.$route.query.mfd || "3575"; //SETTING MFD

    if (this.searchResult) {
      this.handleButtonSearch();
    }
  },
  watch: {
    selectedRegion: function (newRegion, oldRegion) {
      this.resultNews = [];
      this.resultPub = [];
      this.resultTable = [];
      this.loading = true;
      this.makeApiCall(this.key, newRegion, 1); // Reset to first page on region change
    },
    "$route.query.mfd": function (newMfd) {
      this.selectedRegion = newMfd || "3500"; // setting MFD
      this.makeApiCall(this.key, this.selectedRegion, this.currentPage);
    },
  },
  methods: {
    async handleSearchUpdate(query) {
      this.searchResult = query.trim();
      if (this.searchResult == "") {
        this.resultNews = [];
        this.resultPub = [];
        this.resultTable = [];
      } else {
        this.handleButtonClick(this.activeTab);
      }
    },
    async handleButtonClick(type) {
      this.activeTab = type;
      // console.log(this.selectedRegion)
      if (this.searchResult) {
        this.resultNews = [];
        this.resultPub = [];
        this.resultTable = [];
        try {
          window.scrollTo(0, 0); // Scroll to top
          if (type == "table") {
            this.key = "statictable";
            this.resultType = "resultTable";
          } else if (type == "pub") {
            this.key = "publication";
            this.resultType = "resultPub";
          } else if (type == "news") {
            this.key = "pressrelease";
            this.resultType = "resultNews";
          }
          this.loading = true;
          this.currentPage = 1; // Reset current page when changing search type
          this.makeApiCall(this.key, this.selectedRegion, this.currentPage);
        } catch (error) {
          this.loading = false;
          console.error("Error during API request:", error);
        }
      }
    },
    async makeApiCall(key, region, page) {
      try {
        const encodedQuery = encodeURIComponent(this.searchResult);
        const response = await axios.get(
          `https://webapi.bps.go.id/v1/api/list/model/${key}/lang/ind/domain/${region}/keyword/${encodedQuery}/key/${apiKey}?page=${page}`
        );

        const paginationInfo = response.data.data[0];
        this.totalPages = paginationInfo.pages;

        const responseData = response.data.data[1];
        if (responseData.length == 0) {
          this.noData = true;
          this[this.resultType] = [];
        } else {
          this.noData = false;
          this[this.resultType] = responseData;
        }
        this.loading = false;
      } catch (error) {
        console.error("Error during API request:", error);
        this.loading = false;
        this.noData = true;
        this.resultNews = [];
        this.resultPub = [];
        this.resultTable = [];
      }
    },
    async handleButtonSearch() {
      this.handleButtonClick("table");
    },
    async handlePageChange(pageNumber) {
      if (pageNumber >= 1 && pageNumber <= this.totalPages) {
        window.scrollTo(0, 0); // Scroll to top
        this.currentPage = pageNumber;
        this.makeApiCall(this.key, this.selectedRegion, pageNumber);
      }
    },
  },
};
</script>

<style scoped>
.pagination-container {
  display: flex;
  justify-content: center;
}

.btn-secondary {
  background-color: #f7f7f7;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

.btn-secondary:hover {
  background-color: #e7e7e7;
}

.current-page {
  font-size: 18px;
  font-weight: bold;
  margin: 0 10px;
}
</style>
