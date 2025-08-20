<template>
  <div class="card shadow-sm border-0">
    <div class="card-header px-4 pt-4 pb-2">
      <h4 class="card-title mb-3">Lihat/Ubah Data Diri</h4>
      <p class="card-text">
        <small class="text-muted mb-2">Silahkan lengkapi data diri anda!</small>
      </p>
    </div>
    <hr class="hairline" />
    <div class="card-body m-3 mt-0">
      <div v-if="isLoading" class="text-center">
        <img src="/assets/loading_2.svg" alt="Loading..." />
        <p>Loading...</p>
      </div>
      <div v-else>
        <div v-for="(field, key) in userFields" :key="key" class="mb-3">
          <p class="card-text mb-0">{{ field.label }}*</p>
          <p class="card-text">
            <small class="text-muted">{{ field.value || "-" }}</small>
          </p>
        </div>
        <form @submit.prevent="saveData">
          <div v-for="input in formInputs" :key="input.id" class="mb-3">
            <label :for="input.id" class="form-label">{{ input.label }}</label>
            <select
              v-if="input.type == 'select'"
              :class="['form-select', { 'is-invalid': !apiData[input.id] && input.required }]"
              :id="input.id"
              class="pe-2"
              v-model="apiData[input.id]"
              @change="validateField(input.id)"
              :required="input.required"
            >
              <option value="">Pilih {{ input.label }}</option>
              <option
                v-for="option in input.options"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
            <input
              v-else
              :type="input.type"
              :class="['form-control', { 'is-invalid': !apiData[input.id] && input.required }]"
              :id="input.id"
              v-model="apiData[input.id]"
              class="ps-2 pe-2"
              @input="validateField(input.id)"
              :required="input.required"
              style="border: 1px solid #ced4da;"
            />
            <div class="invalid-feedback">{{ input.error }}</div>
          </div>
          <p class="card-text mt-3">
            <small class="text-muted">*) data wajib di isi</small>
          </p>
          <button
            type="submit"
            class="btn btn-success w-100"
            :disabled="!isFormValid"
          >
            Simpan
          </button>
        </form>
      </div>
    </div>

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
                <span class="ms-3">Memproses Perubahan...</span>
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
                <i class="bi bi-check-circle text-success" style="font-size: 2rem"></i>
                <span class="ms-3">Perubahan berhasil dilakukan.</span>
              </div>
              <div class="d-flex justify-content-center mt-3">
                <button type="button" class="btn btn-success" @click="closeSuccessModal">
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
import { reactive, onMounted } from "vue";
import { apiService } from "@/api/ApiService";

export default {
  props: {
    user: {
      type: Object,
      required: true,
    },
    cardApiUrl: {
      type: String,
    },
  },
  data() {
    return {
      apiData: {
        pekerjaan: "",
        jenis_kelamin: "",
        tanggal_lahir: "",
        id_prov: "",
        id_kab: "",
        nmr_telp: "",
        pendidikan: "",
      },
      formInputs: [
        {
          id: "pekerjaan",
          label: "Pekerjaan",
          type: "select",
          required: true,
          options: [
            { label: "Pelajar/Mahasiswa", value: "Pelajar/Mahasiswa" },
            { label: "Peneliti/Dosen", value: "Peneliti/Dosen" },
            { label: "Pegawai Swasta", value: "Pegawai Swasta" },
            { label: "Pegawai BUMN/BUMD", value: "Pegawai BUMN/BUMD" },
            { label: "Wiraswasta", value: "Wiraswasta" },
            { label: "ASN/TNI/Polri", value: "ASN/TNI/Polri" },
          ],
          error: "",
        },
        {
          id: "jenis_kelamin",
          label: "Jenis Kelamin",
          type: "select",
          required: true,
          options: [
            { label: "Perempuan", value: "Perempuan" },
            { label: "Laki-laki", value: "Laki-Laki" },
          ],
          error: "",
        },
        {
          id: "tanggal_lahir",
          label: "Tanggal Lahir",
          type: "date",
          required: true,
          error: "",
        },
        {
          id: "id_prov",
          label: "Asal Provinsi",
          type: "select",
          required: true,
          options: [],
          error: "",
        },
        {
          id: "id_kab",
          label: "Asal Kabupaten/Kota",
          type: "select",
          required: true,
          options: [],
          error: "",
        },
        {
          id: "nmr_telp",
          label: "Nomor Handphone",
          type: "tel",
          required: true,
          error: "",
        },
        {
          id: "pendidikan",
          label: "Pendidikan Terakhir",
          type: "select",
          required: true,
          options: [
            { label: "<= SLTA Sederajat", value: "<= SLTA Sederajat" },
            { label: "D1/D2/D3", value: "D1/D2/D3" },
            { label: "D4/S1", value: "D4/S1" },
            { label: "S2", value: "S2" },
            { label: "S3", value: "S3" },
          ],
          error: "",
        },
      ],
      userFields: [
        { label: "Nama Panjang", value: this.user.nama_pengguna },
        { label: "Email", value: this.user.email_google },
        { label: "Nama Depan", value: this.user.given_name },
        { label: "Nama Belakang", value: this.user.family_name },
      ],
      isLoading: false,
      isSuccess: false,
    };
  },
  computed: {
    isFormValid() {
      return this.formInputs.every(
        (input) => !input.required || (this.apiData[input.id] && !input.error)
      );
    },
  },
  created() {
    this.fetchProvinces();
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.isLoading = true;
      const storedUser = localStorage.getItem("user");
      const storedLoggedIn = localStorage.getItem("loggedIn");

      if (storedUser && storedLoggedIn) {
        const parsedUser = JSON.parse(storedUser);

        this.apiData.pekerjaan = parsedUser.pekerjaan ?? "";
        this.apiData.jenis_kelamin = parsedUser.jenis_kelamin ?? "";
        this.apiData.tanggal_lahir = parsedUser.tanggal_lahir ?? "";
        this.apiData.id_prov = parsedUser.id_prov ?? "";
        this.apiData.id_kab = parsedUser.id_kab ?? "";
        this.apiData.nmr_telp = parsedUser.nmr_telp ?? "";
        this.apiData.pendidikan = parsedUser.pendidikan ?? "";

        this.user.nama_pengguna = parsedUser.nama_pengguna ?? "-";
        this.user.email_google = parsedUser.email_google ?? "-";
        this.user.given_name = parsedUser.given_name ?? "-";
        this.user.family_name = parsedUser.family_name ?? "-";
      }
      this.isLoading = false;
    },
    saveData() {
      this.isLoading = true;
      try {
        const storedUser = localStorage.getItem("user");
        if (!storedUser) {
          throw new Error("No user data found in local storage");
        }
        const parsedUser = JSON.parse(storedUser);

        apiService
          .updateUser(parsedUser.id, this.apiData)
          .then((response) => {
            this.isSuccess = true;
            setTimeout(() => {
              this.isSuccess = false;
            }, 2000);

            const updatedUser = response.data.data;
            localStorage.setItem("user", JSON.stringify(updatedUser));
            this.fetchData();
          })
          .catch((error) => {
            console.error("Error:", error.message);
          })
          .finally(() => {
            this.isLoading = false;
          });
      } catch (error) {
        console.error("Error:", error.message);
        this.isLoading = false;
      }
    },
    validateField(field) {
      const input = this.formInputs.find((input) => input.id === field);

      if (field === "nmr_telp") {
        const phoneRegex = /^08[0-9]{7,11}$/;
        input.error = phoneRegex.test(this.apiData[field])
          ? ""
          : "Nomor HP harus diawali 08 dan terdiri dari 9-12 angka tanpa simbol atau huruf";
      } else {
        input.error =
          this.apiData[field] || !input.required
            ? ""
            : "Kolom ini harus diisi.";
      }
    },
    fetchProvinces() {
      apiService
        .getAllProvinces()
        .then((response) => {
          const provinces = response.data.data;
          const provinceInput = this.formInputs.find(
            (input) => input.id === "id_prov"
          );
          if (provinceInput) {
            provinceInput.options = provinces.map((province) => ({
              label: province.nama_prov,
              value: province.id_prov,
            }));
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    fetchCities(provinceId) {
      apiService
        .getKabupatenByProvinsi(provinceId)
        .then((response) => {
          const cities = response.data.data;
          const cityInput = this.formInputs.find(
            (input) => input.id === "id_kab"
          );
          if (cityInput) {
            cityInput.options = cities.map((city) => ({
              label: city.nama_kab,
              value: city.id_kab,
            }));
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  watch: {
    "apiData.id_prov"(newProvinceId) {
      if (newProvinceId) {
        this.fetchCities(newProvinceId);
      } else {
        const cityInput = this.formInputs.find((input) => input.id === "id_kab");
        if (cityInput) {
          cityInput.options = [];
        }
      }
    },
  },
};
</script>

<style scoped>
.card-header {
  border-bottom: none;
}

.card-body {
  padding: 1rem;
}

.form-control.is-invalid {
  border-color: #dc3545;
}

.form-select {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  line-height: 1.5;
  color: #495057;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  transition:
    border-color 0.15s ease-in-out,
    box-shadow 0.15s ease-in-out;
}

.form-select:focus {
  color: #495057;
  background-color: #fff;
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.invalid-feedback {
  display: block;
}

.hairline {
  width: 100%;
  border: 0;
  border-top: 1px solid #141e2a;
  margin-bottom: 20px;
}

/* Modal styles */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.modal-content {
  background: #fff;
  padding: 1rem 1.5rem;
  border-radius: 0.3rem;
  text-align: center;
}
</style>
