<template>
  <div v-if="isModalMainVisible">
    <div class="modal-backdrop">
      <div class="modal position-static d-block p-4 py-md-5" tabindex="-1" role="dialog" id="modalSheet">
        <div class="modal-dialog" role="document">
          <div class="modal-content rounded-4 shadow px-2">
            <div class="modal-header border-bottom-0">
              <h4 class="modal-title fw-semibold text-success d-block">RESERVASI KONSULTASI ONLINE</h4>
              <button type="button" class="bi bi-x btn-close-white" @click="close"></button>
            </div>
            <hr class="hairline mt-0" />
            <div class="alert alert-primary modal-body mx-2 p-2" role="alert" id="alert">
              <div class="row">
                <div class="col-auto ms-1">
                  <i class="bi bi-info-circle" style="color: #ffff"></i>
                </div>
                <div class="col p-0">
                  <small style="color: #ffff">
                    Petugas pelayanan bisa saja berganti disesuaikan dengan beban petugas yang ada
                  </small>
                </div>
              </div>
            </div>
            <div class="modal-body py-0">
              <div class="row">
                <div class="col-md-6 d-flex">
                  <i class="bi bi-person-vcard me-2"></i>
                  <div>
                    <p class="fw-semibold mb-0 text-muted">Data Petugas:</p>
                    <p class="mb-0"><small>{{ petugas.nama_petugas }}</small></p>
                    <p><small>{{ petugas.satker.nama_satker }}</small></p>
                  </div>
                </div>
                <div class="col-md-6 d-flex">
                  <i class="bi bi-person-vcard me-2"></i>
                  <div class="pe-2">
                    <p class="fw-semibold mb-0 text-muted">Data Pengguna:</p>
                    <p class="mb-0"><small>{{ pengguna.nama_pengguna }}</small></p>
                    <p><small>{{ pengguna.email_google }}</small></p>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-md-12">
                  <h5>Jadwal Konsultasi:</h5>
                  <div class="form-group d-flex align-items-center">
                    <label for="tanggal" class="me-2">Tanggal:</label>
                    <input type="date" id="tanggal" v-model="tanggal" class="form-control ps-2 pe-2" :min="minDate" :max="maxDate" style="border: 1px solid #ced4da;"/>
                  </div>
                  <small v-if="invalidDate && !isHoliday" class="text-danger">
                    Tanggal yang dipilih tidak valid. Pilih hari Senin hingga Jumat dalam 30 hari ke depan.
                  </small>
                  <small v-if="isHoliday" class="text-danger">
                    Hari yang dipilih tidak valid/hari libur nasional. Pilih hari kerja untuk reservasi konsultasi.
                  </small>
                  <div class="form-group mt-3 d-flex align-items-center">
                    <label for="jam" class="me-2">Jam:</label>
                    <input type="time" id="jam" v-model="jam" class="form-control ps-2 pe-2" style="border: 1px solid #ced4da;" />
                  </div>
                  <small v-if="invalidTime && !invalidTimeToday" class="text-danger">
                    Jam yang dipilih tidak valid. Pilih jam antara 08.00-16.00 WIB.
                  </small>
                  <small v-if="invalidTimeToday" class="text-danger">
                    Jam yang dipilih tidak valid. Pilih jam yang lebih dari 1 jam dari sekarang.
                  </small>
                </div>
              </div>
              <div class="row mt-3">
                <div class="col-md-12">
                  <h5>Topik Konsultasi:</h5>
                  <textarea v-model="topik" rows="5" cols="30" class="w-100 rounded rounded-2 p-2" placeholder="Masukan topik yang ingin Anda diskusikan..."></textarea>
                </div>
              </div>
            </div>
            <div class="modal-footer flex-column align-items-stretch w-100 gap-2 pb-3 border-top-0">
              <button type="button" class="btn btn-success" @click="submitReservation">Kirim!</button>
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
    petugas: {
      type: Object,
      required: true,
    },
    pengguna: {
      type: Object,
      required: true,
    },
    isModalMainVisible: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      tanggal: "",
      minDate: "",
      maxDate:"",
      jam: "",
      topik: "",
      invalidTime: false,
      invalidTimeToday: false,
      invalidDate: false,
      // Menambahkan daftar hari libur nasional dan cuti bersama 2025
      hariLibur: [
        "2025-01-01", // Tahun Baru Masehi
        "2025-01-27", // Isra Mikraj Nabi Muhammad SAW
        "2025-01-28", // Cuti Bersama Tahun Baru Imlek
        "2025-01-29", // Tahun Baru Imlek 2576 Kongzili
        "2025-03-28", // Cuti Bersama Hari Suci Nyepi
        "2025-03-29", // Hari Suci Nyepi (Tahun Baru Saka 1947)
       "2025-03-31", // Hari Raya Idul Fitri 1446 H
       "2025-04-01", // Hari Raya Idul Fitri 1446 H
       "2025-04-02", // Cuti Bersama Idul Fitri
      "2025-04-03", // Cuti Bersama Idul Fitri
      "2025-04-04", // Cuti Bersama Idul Fitri
      "2025-04-07", // Cuti Bersama Idul Fitri
      "2025-04-18", // Wafat Isa Al Masih
      "2025-04-20", // Hari Paskah
      "2025-05-01", // Hari Buruh Internasional
      "2025-05-12", // Hari Raya Waisak 2569 BE
       "2025-05-13", // Cuti Bersama Hari Raya Waisak
       "2025-05-29", // Kenaikan Isa Al Masih
       "2025-05-30", // Cuti Bersama Kenaikan Isa Al Masih
      "2025-06-06", // Hari Raya Idul Adha 1446 H
      "2025-06-09", // Cuti Bersama Idul Adha
      "2025-07-27", // Tahun Baru Islam 1447 H
      "2025-08-17", // Hari Kemerdekaan Republik Indonesia
      "2025-09-05", // Maulid Nabi Muhammad SAW
      "2025-12-25", // Hari Raya Natal
      "2025-12-26",
      ],
    };
  },
  created() {
    this.setMinDate();
    this.loadUser
  },
  methods: {
    setMinDate() {
      const today = new Date();
      const yyyy = today.getFullYear();
      const mm = String(today.getMonth() + 1).padStart(2, "0");
      const dd = String(today.getDate()).padStart(2, "0");
      this.minDate = `${yyyy}-${mm}-${dd}`;

      const maxDateObj = new Date();
      maxDateObj.setDate(today.getDate() + 30);
      const yyyyMax = maxDateObj.getFullYear();
      const mmMax = String(maxDateObj.getMonth() + 1).padStart(2, "0");
      const ddMax = String(maxDateObj.getDate()).padStart(2, "0");
      this.maxDate = `${yyyyMax}-${mmMax}-${ddMax}`;
    },
    close() {
      this.$emit("close");
    },
    validateJam() {
      const [jam, menit] = this.jam.split(":");
      const hour = parseInt(jam, 10);
      const minute = parseInt(menit, 10);

      const validTime =
        (hour >= 8 && hour < 16) ||
        (hour == 16 && minute == 0);

      if (!validTime) {
        this.invalidTime = true;
        this.invalidTimeToday = false;
      } else if (
        this.isToday(this.tanggal) &&
        !this.validateTimeForToday(hour, minute)
      ) {
        this.invalidTimeToday = true;
        this.invalidTime = false;
      } else {
        this.invalidTime = false;
        this.invalidTimeToday = false;
      }
    },
    validateTimeForToday(hour, minute) {
      const now = new Date();
      const selectedTime = new Date();
      selectedTime.setHours(hour);
      selectedTime.setMinutes(minute);
      selectedTime.setSeconds(0);
      selectedTime.setMilliseconds(0);

      const oneHourFromNow = new Date(now.getTime() + 60 * 60 * 1000);

      // Harus lebih dari 1 jam dari sekarang
      return selectedTime > oneHourFromNow;
    },
    validateTanggal() {
      const selectedDate = new Date(this.tanggal);
      const day = selectedDate.getDay();

      const today = new Date();
      today.setHours(0, 0, 0, 0);

      const maxDateObj = new Date();
      maxDateObj.setDate(today.getDate() + 30);
      maxDateObj.setHours(0, 0, 0, 0);

      // Cek apakah tanggal yang dipilih adalah hari libur nasional
      const isHariLibur = this.hariLibur.includes(this.tanggal);

      // Cek apakah tanggal yang dipilih adalah hari Sabtu (6) atau Minggu (0) atau hari libur nasional
      if (day === 0 || day === 6 || isHariLibur) {
        this.invalidDate = true;
        this.isHoliday = true;
      } else if (selectedDate < today || selectedDate > maxDateObj) {
        this.invalidDate = true;
        this.isHoliday = false;
      } else {
        this.invalidDate = false;
        this.isHoliday = false;
      }
    },
    isToday(date) {
      const today = new Date();
      const selectedDate = new Date(date);

      return (
        today.getFullYear() == selectedDate.getFullYear() &&
        today.getMonth() == selectedDate.getMonth() &&
        today.getDate() == selectedDate.getDate()
      );
    },
    loadUser(){
      this.pengguna = JSON.parse(localStorage.getItem("user"))
      console.log(this.pengguna)
    },
    submitReservation() {
      this.validateJam();
      this.validateTanggal();
      this.$emit("loading", true);
      this.$emit("hideMainModal");

      if (
        !this.invalidTime &&
        !this.invalidTimeToday &&
        !this.invalidDate &&
        this.tanggal &&
        this.jam &&
        this.topik
      ) {
        const storedUser = JSON.parse(localStorage.getItem("user"));

        if (storedUser) {
          const dataApi = {
            tanggal_konsultasi: this.tanggal,
            waktu_konsultasi: this.jam,
            topik_diskusi: this.topik,
            id_petugas: this.petugas.id,
            id_pengguna: storedUser.id,
          };

          apiService
            .addConsultation(dataApi)
            .then((response) => {
              console.log("Reservation submitted successfully", response.data);
              this.$emit("loading", false);
              this.$emit("success", true);
            })
            .catch((error) => {
              console.error("Error submitting reservation", error);
              this.$emit("loading", false);
              alert("Terjadi kesalahan saat mengirim reservasi. Silakan Login kembali.");
            });
        } else {
          alert("Pengguna tidak ditemukan. Silakan login kembali.");
        }
      } else {
        alert("Pastikan semua field terisi dengan benar.");
      }
    },
  },
  watch: {
    jam(newVal) {
      if (newVal) {
        this.validateJam();
      }
    },
    tanggal(newVal) {
      if (newVal) {
        this.validateTanggal();
      }
    },
  },
};
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.hairline {
  width: 100%;
  border: 0;
  border-top: 1px solid #141e2a;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.form-group label {
  min-width: 120px; /* Set a fixed width for the label */
  margin-right: 10px;
}

.form-control {
  flex: 1;
}
</style>
