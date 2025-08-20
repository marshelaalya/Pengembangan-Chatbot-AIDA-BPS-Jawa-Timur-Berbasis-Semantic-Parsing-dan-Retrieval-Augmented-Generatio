
import apiClient from './ApiConfig.js';

export const apiService = {
  addUser(data) {
    return apiClient.post("pengguna", data);
  },

  updateUser(id, data) {
    return apiClient.put(`pengguna/${id}`, data);
  },

  addConsultation(data) {
    return apiClient.post("konsultasi", data);
  },

  getConsultationsByUser(idPengguna) {
    return apiClient.get(`konsultasi-by-pengguna/${idPengguna}`);
  },

  getReservationsByUser(idPengguna) {
    return apiClient.get(`reservasi-by-pengguna/${idPengguna}`);
  },

  getHistoryByUser(idPengguna) {
    return apiClient.get(`histori-by-pengguna/${idPengguna}`);
  },

  getConsultation(idKonsultasi) {
    return apiClient.get(`konsultasi/${idKonsultasi}`);
  },

  cancelConsultation(idKonsultasi, data) {
    return apiClient.put(`konsultasi/${idKonsultasi}/batal`, data);
  },

  giveFeedback(idKonsultasi, data) {
    return apiClient.put(`konsultasi/${idKonsultasi}/feedback`, data);
  },

  getAllOfficers() {
    return apiClient.get('petugas');
  },

  getOfficersBySatker(idSatker) {
    return apiClient.get(`petugas-by-satker/${idSatker}`);
  },

  getOfficer(idPetugas) {
    return apiClient.get(`petugas/${idPetugas}`);
  },

  getAllKabupaten() {
    return apiClient.get('kabupaten');
  },

  getKabupatenByProvinsi(idProv) {
    return apiClient.get(`kabupaten-by-prov/${idProv}`);
  },

  getAllProvinces() {
    return apiClient.get('provinsi');
  },

  getAllUsers() {
    return apiClient.get('pengguna');
  },

  getUser(idPengguna) {
    return apiClient.get(`pengguna/${idPengguna}`);
  },

  getAllConsultations() {
    return apiClient.get('konsultasi');
  },

  getAllSatker() {
    return apiClient.get('satker');
  },

  getNotification(email_user) {
    return apiClient.get(`notifikasi/${email_user}`);
  },

  setNotificationRead(email_user, id_notif) {
    return apiClient.get(`notifikasi/${email_user}/mark-as-read/${id_notif}`);
  },

  getKeahlian() {
    return apiClient.get('keahlian');
  },

  getPetugasByKeahlian(id_keahlian) {
    return apiClient.get(`petugas-by-keahlian/${id_keahlian}`);
  },

  getVerify() {
    return apiClient.post('verify-google-token');
  },

  // New AIDA API methods
  addAida(data) {
    return apiClient.post('aida', data);
  },

  getAidaByUser(idPengguna) {
    return apiClient.get(`aida-by-pengguna/${idPengguna}`);
  },

  updateAidaConversation(idAida, data) {
    return apiClient.put(`aida-update-conv/${idAida}/update`, data);
  },

  deleteAidaConversation(idAida) {
    return apiClient.put(`aida-hapus-conv/${idAida}`);
  },
};
