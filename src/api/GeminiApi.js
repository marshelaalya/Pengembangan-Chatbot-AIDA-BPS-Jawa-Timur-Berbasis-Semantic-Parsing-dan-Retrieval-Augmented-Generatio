import { GoogleGenerativeAI } from '@google/generative-ai';


const apiKey = 'AIzaSyDxLpZKmepLUUu8oYuJfzvg3I4wv2p9G1U';
const genAI = new GoogleGenerativeAI(apiKey);

const model = genAI.getGenerativeModel({
  model: 'gemini-1.5-flash',
});

const generationConfig = {
  temperature: 1,
  topP: 0.95,
  topK: 64,
  maxOutputTokens: 8192,
  responseMimeType: 'text/plain',
};

const websites = ["https://jatim.bps.go.id","https://pacitankab.bps.go.id","https://ponorogokab.bps.go.id","https://trenggalekkab.bps.go.id","https://tulungagungkab.bps.go.id","https://blitarkab.bps.go.id","https://kedirikab.bps.go.id","https://malangkab.bps.go.id","https://lumajangkab.bps.go.id","https://jemberkab.bps.go.id","https://banyuwangikab.bps.go.id","https://bondowosokab.bps.go.id","https://situbondokab.bps.go.id","https://probolinggokab.bps.go.id","https://pasuruankab.bps.go.id","https://sidoarjokab.bps.go.id","https://mojokertokab.bps.go.id","https://jombangkab.bps.go.id","https://nganjukkab.bps.go.id","https://madiunkab.bps.go.id","https://magetankab.bps.go.id","https://ngawikab.bps.go.id","https://bojonegorokab.bps.go.id","https://tubankab.bps.go.id","https://lamongankab.bps.go.id","https://gresikkab.bps.go.id","https://bangkalankab.bps.go.id","https://sampangkab.bps.go.id","https://pamekasankab.bps.go.id","https://sumenepkab.bps.go.id","https://kedirikota.bps.go.id","https://blitarkota.bps.go.id","https://malangkota.bps.go.id","https://probolinggokota.bps.go.id","https://pasuruankota.bps.go.id","https://mojokertokota.bps.go.id","https://madiunkota.bps.go.id","https://surabayakota.bps.go.id","https://batukota.bps.go.id"];
const subjectTable = ["/id/statistics-table?subject=519", "/id/statistics-table?subject=520", "/id/statistics-table?subject=521",
                      "/id/statistics-table?subject=522", "/id/statistics-table?subject=523", "/id/statistics-table?subject=524",
                      "/id/statistics-table?subject=525", "/id/statistics-table?subject=526", "/id/statistics-table?subject=527",
                      "/id/statistics-table?subject=528", "/id/statistics-table?subject=529", "/id/statistics-table?subject=530",
                      "/id/statistics-table?subject=531", "/id/statistics-table?subject=532", "/id/statistics-table?subject=533",
                      "/id/statistics-table?subject=534", "/id/statistics-table?subject=535", "/id/statistics-table?subject=536",
                      "/id/statistics-table?subject=537", "/id/statistics-table?subject=538", "/id/statistics-table?subject=557",
                      "/id/statistics-table?subject=558", "/id/statistics-table?subject=559", "/id/statistics-table?subject=560",
                      "/id/statistics-table?subject=561", "/id/statistics-table?subject=562", "/id/statistics-table?subject=539",
                      "/id/statistics-table?subject=540", "/id/statistics-table?subject=541", "/id/statistics-table?subject=542",
                      "/id/statistics-table?subject=563", "/id/statistics-table?subject=564", "/id/statistics-table?subject=565",
                      "/id/statistics-table?subject=566", "/id/statistics-table?subject=567", "/id/statistics-table?subject=568",
                      "/id/statistics-table?subject=569"
                      ]

const systemPrompt = {
  role: 'system',
  content: 
  `Kamu adalah Ning Aida, AI Data Assistant BPS Provinsi Jawa Timur yang siap membantu Anda menyediakan data dan informasi statistik seputar BPS.

  BPS membuka pelayanan konsultasi data dari hari Senin s.d. Kamis, pukul 08.00-15.30 dan hari Jumat, pukul 08.00–16.00

  Produk statistik BPS meliputi tabel data statistik, data mikro, publikasi statistik, dan Berita Resmi Statistik.

  Jika ada yang meminta insight, berikan insight terkait fenomena data, intepretasi data, dan rekomendasi kebijakan untuk pemerintah.

  Jika ada yang meminta data:
  - Kependudukan dan Migrasi ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[0]}`).join('\n')}
  - Tenaga Kerja ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[1]}`).join('\n')}
  - Pendidikan ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[2]}`).join('\n')}
  - Kesehatan ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[3]}`).join('\n')}
  - Konsumsi dan Pendapatan ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[4]}`).join('\n')}
  - Perlindungan Sosial ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[5]}`).join('\n')}
  - Pemukiman dan Perumahan ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[6]}`).join('\n')}
  - Hukum dan Kriminal ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[7]}`).join('\n')}
  - Budaya ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[8]}`).join('\n')}
  - Aktivitas Politik dan Komunitas Lainnya ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[9]}`).join('\n')}
  - Penggunaan Waktu ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[10]}`).join('\n')}
  - Statistik Makroekonomi ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[11]}`).join('\n')}
  - Neraca Ekonomi ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[12]}`).join('\n')}
  - Statistik Bisnis ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[13]}`).join('\n')}
  - Statistik Sektoral ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[14]}`).join('\n')}
  - Keuangan Pemerintah, Fiskal dan Statistik Sektor Publik ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[15]}`).join('\n')}
  - Perdagangan Internasional dan Neraca Pembayaran, Ekspor, Impor ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[16]}`).join('\n')}
  - Harga-Harga, Nilai Tukar Petani/Nelayan, dan Inflasi ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[17]}`).join('\n')}
  - Biaya Tenaga Kerja, Upah/Gaji ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[18]}`).join('\n')}
  - Ilmu Pengetahuan, Teknologi, dan Inovasi (Internet, Telepon Seluler, Media Sosial) ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[19]}`).join('\n')}
  - Pertanian, Kehutanan, Perikanan, Peternakan, Perkebunan ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[20]}`).join('\n')}
  - Energi ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[21]}`).join('\n')}
  - Pertambangan, Manufaktur, Konstruksi ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[22]}`).join('\n')}
  - Transportasi ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[23]}`).join('\n')}
  - Pariwisata ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[24]}`).join('\n')}
  - Perbankan, Asuransi, Saham, dan Finansial ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[25]}`).join('\n')}
  - Lingkungan, Iklim, Bencana ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[26]}`).join('\n')}
  - Statistik Regional, Statistik Area Kecil, Desa/Kecamatan/Wilayah ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[27]}`).join('\n')}
  - Statistik dan Indikator Multi-Domain ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[28]}`).join('\n')}
  - Buku Tahunan dan Ringkasan Sejenis ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[29]}`).join('\n')}
  - Kondisi Tempat Tinggal, Kemiskinan, dan Permasalahan Sosial Lintas Sektor ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[30]}`).join('\n')}
  - Gender dan Kelompok Populasi Khusus ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[31]}`).join('\n')}
  - Masyarakat Informasi ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[32]}`).join('\n')}
  - Globalisasi ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[33]}`).join('\n')}
  - Indikator Millenium Development Goals (MDGs) ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[34]}`).join('\n')}
  - Perkembangan Berkelanjutan ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[35]}`).join('\n')}
  - Kewiraswastaan ${websites.map((url) => `- ${url.match(/https:\/\/(\w+)\.bps\.go\.id/)[1]}: ${url}${subjectTable[36]}`).join('\n')}
  
  Khusus untuk data eskpor impor, jika ada yang memita data ekspor impor Kabupaten atau Kota, arahkan ke https://jatim.bps.go.id/id/exim 
  
  Setelah memberikan informasi tentang data, jangan lupa tawarkan pelayanan data BPS lainnya
  Setelah memberi data, arahkan pengunjung untuk konsultasi dengan Statistisi Ahli dari BPS melalui link: https://halopst.web.bps.go.id/konsultasi 
  
  Tidak semua data merupakan data mikro, kebanyakan bisa diakses di https://jatim.bps.go.id/id/query-builder.

  Jika ada yang minta data atau minta diberikan data, arahkan ke:
  - Data secara umum arahkan ke: https://jatim.bps.go.id/id/statistics-table?subject=519
  - Tabel lainnya arahkan ke: https://jatim.bps.go.id/id/query-builder
  - Publikasi statistik arahkan ke: https://jatim.bps.go.id/id/publication
  - Berita Resmi Statistik arahkan ke: https://jatim.bps.go.id/id/pressrelease
  - Data sensus arahkan ke: https://sensus.bps.go.id/
  - Data ekspor impor arahkan ke: https://jatim.bps.go.id/id/exim
  - Konsep definisi dan metadata arahkan ke: https://sirusa.web.bps.go.id/metadata/
  - Pembelian Data mikro arahkan ke: https://silastik.bps.go.id/v3/index.php/site/index_internal/#tta dengan harga https://ppid.bps.go.id/upload/img/standar_biaya5.png
  - Mengajukan rekomendasi statistik arahkan ke https://romantik.web.bps.go.id
  - Informasi tentang Pojok Statistik arahkan ke https://pojokstatistik.bps.go.id/
  
  Berikut website BPS di Jawa Timur yang bisa menjadi rujukan dalam memperoleh produk statistik BPS:
  ${websites.map((url, index) => `${index + 1}. ${url}`).join('\n')}

  Jika ada yang meminta data di luar wilayah Jawa Timur, arahkan ke https://bps.go.id

  Selain website, data BPS Jawa Timur dapat diperoleh melalui aplikasi Mister J-Statistik Jatim yang dapat didownload melalui Google Playstore di https://play.google.com/store/apps/details?id=com.bps_jatim_3500.statistik_jatim&hl=id

  di akhir percakapan, tawarkan pengunjung untuk mengisi Survei Kebutuhan Data sebagai bentuk peningkatan layanan BPS Jawa Timur di link: https://skd.bps.go.id/SKD2024/web/entri/responden/blok1?token=D8vpKU5RZ2XIjNgKS03zSuCnQ_wL8Sd-9jXKDkMNkDaSDytXhq7WHxZUtD5xCgfykodltGTsKC0g6zS5XqIKF2SF3PY-HctaucbQ
  
  Berikan link url yang dapat diklik/dibuka.
  `
};

function formatToHtml(text) {
  let formattedText = text;

  // Convert headers (Markdown syntax) to <h1>, <h2>, etc.
  formattedText = formattedText.replace(/^###### (.*$)/gim, '<h6>$1</h6>');
  formattedText = formattedText.replace(/^##### (.*$)/gim, '<h5>$1</h5>');
  formattedText = formattedText.replace(/^#### (.*$)/gim, '<h4>$1</h4>');
  formattedText = formattedText.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  formattedText = formattedText.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  formattedText = formattedText.replace(/^# (.*$)/gim, '<h1>$1</h1>');

  // Convert **bold** to <strong>
  formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

  // Convert *italic* to <em>
  formattedText = formattedText.replace(/\*(.*?)\*/g, '<em>$1</em>');

  // Convert numbered list to <ol><li>
  formattedText = formattedText.replace(/^\d+\.\s+(.*)$/gm, '<li>$1</li>');
  if (formattedText.includes('<li>')) {
    formattedText = formattedText.replace(/(<li>.*<\/li>)/gs, '<ol>$1</ol>');
  }

  // Convert bullet list to <ul><li>
  formattedText = formattedText.replace(/^\*\s+(.*)$/gm, '<li>$1</li>');
  if (formattedText.includes('<li>')) {
    formattedText = '<ul>' + formattedText.replace(/(<li>.*<\/li>)/gs, '$1') + '</ul>';
  }

  // Convert URLs to <a href="...">...</a>
  formattedText = formattedText.replace(/\bhttps?:\/\/[^\s<]+(^\s.,)<]/g, function(url) {
    return '<a href="' + url + '" target="_blank" rel="noopener noreferrer">' + url + '</a>';
  });
  
  return formattedText;
}

export async function getAiResponse(messages) {
  const parts = [{ role: 'system', content: 'Gunakan informasi berikut sebagai konteks:\n'}, 
    systemPrompt, ...messages].map(message => ({ text: message.content }));

  try {
    const result = await model.generateContent({
      contents: [{ role: 'user', parts }],
      generationConfig,
    });

    const formattedResponse = formatToHtml(result.response.text());
    return formattedResponse;
  } catch (error) {
    console.error('Error fetching AI response:', error);
    return 'Maaf, saya sudah mencapai limit. Ulangi kembali permintaan Anda.';
  }
}

export async function getChatSummary(messages) {
  const summaryPrompt = {
    role: 'system',
    content: 'Buat ringkasan judul dari topik yang dibahas. Judul harus singkat, jelas, dan tepat sasaran. Hanya 7 kata, tidak boleh lebih dari 7 kata. Kurang dari 7 kata diutamakan'
  };

  const parts = [{ role: 'system', content: 'Berikan ringkasan yang sangat singkat dan tepat.' }, ...messages, summaryPrompt].map(message => ({ text: message.content }));

  try {
    const result = await model.generateContent({
      contents: [{ role: 'user', parts }],
      generationConfig,
    });

    let summary = result.response.text().trim();

    // Validate and truncate the summary to 7 words if necessary
    const words = summary.split(' ');
    if (words.length > 7) {
      summary = words.slice(0, 7).join(' ') + '...';
    }

    return summary;
  } catch (error) {
    console.error('Error fetching chat summary:', error);
    return 'Ringkasan Percakapan';
  }
}
