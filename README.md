# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding

Jaya Jaya Institut merupakan salah satu institusi pendidikan perguruan yang telah berdiri sejak tahun 2000. Hingga saat ini ia telah mencetak banyak lulusan dengan reputasi yang sangat baik. Akan tetapi, terdapat banyak juga siswa yang tidak menyelesaikan pendidikannya alias dropout.

Jumlah dropout yang tinggi ini tentunya menjadi salah satu masalah yang besar untuk sebuah institusi pendidikan. Oleh karena itu, Jaya Jaya Institut ingin mendeteksi secepat mungkin siswa yang mungkin akan melakukan dropout sehingga dapat diberi bimbingan khusus.

### Permasalahan Bisnis

Beberapa permasalahan bisnis yang ingin dijawab antara lain:

1. **Faktor apa saja yang mempengaruhi mahasiwa dropout?**
2. **Bagaimana perusahaan dapat mengidentifikasi karakteristik mahasiswa yang cenderung "graduate" atau "dropout"?**
3. **Insight apa yang dapat diperoleh dari analisis data untuk membantu institut dalam menyusun strategi agar mahasiswa tidak rentan dropout?**

### Cakupan Proyek

Analisis ini bertujuan untuk:

1. Menaganalisa faktor apa saja yang mempengaruhi status kelulusan.
2. Membuat dashboard sederhana yang dapat memprediksi tingkat status kelulusan mahasiswa.
3. Memberikan insight untuk membantu strategi pembelajaran yang efektif

### Persiapan

Sumber data: [Link Dataset](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/README.md)

Setup Environment - Anaconda

```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

Setup Environment - Shell/Terminal

```
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Business Dashboard

Dashboard ini menampilkan gambaran umum (overview) data akademik mahasiswa berdasarkan aktivitas pada Semester 1 dan Semester 2. Pada setiap semester, data dibagi menjadi tiga kategori utama, yaitu jumlah mahasiswa yang melakukan enrollment, mahasiswa dengan evaluasi (with evaluation), serta mahasiswa tanpa evaluasi (without evaluation). Melalui visualisasi ini, pengguna dapat dengan mudah membandingkan tingkat partisipasi dan evaluasi antar semester, melihat proporsi mahasiswa yang aktif dinilai maupun yang belum dievaluasi, serta mengidentifikasi pola atau potensi permasalahan dalam proses pembelajaran. Dashboard ini dirancang untuk memberikan insight yang cepat dan informatif guna mendukung pengambilan keputusan berbasis data di bidang akademik.

Link : [Dashboard](https://lookerstudio.google.com/reporting/586d3422-3677-45f0-8613-52d040561752/page/6iYuF)

## Menjalankan Sistem Machine Learning

Jelaskan cara menjalankan protoype sistem machine learning yang telah dibuat. Selain itu, sertakan juga link untuk mengakses prototype tersebut.

Menjalankan Aplikasi
``conda activate main-ds
streamlit run app.py`

Link : [Streamlit](https://lookerstudio.google.com/reporting/586d3422-3677-45f0-8613-52d040561752/page/6iYuF)

## Conclusion

Berdasarkan hasil analisis korelasi, faktor **akademik** menjadi penentu utama dalam menentukan status mahasiswa. Variabel seperti jumlah mata kuliah yang lulus (_approved_) dan nilai (_grade_) pada Semester 1 dan Semester 2 memiliki pengaruh paling kuat, yang menunjukkan bahwa performa akademik yang baik secara signifikan menurunkan risiko _dropout_. Selain itu, faktor **finansial** seperti status pembayaran kuliah yang lancar (_tuition up to date_) dan kepemilikan beasiswa (_scholarship holder_) juga berkontribusi positif terhadap keberlangsungan studi, sementara kondisi seperti memiliki tunggakan (_debtor_) justru meningkatkan risiko _dropout_. Faktor aktivitas dan _background_ seperti jumlah mata kuliah yang diambil serta nilai masuk juga berpengaruh, namun relatif lebih kecil.

### Rekomendasi Action Items

- Monitoring dini mahasiswa berisiko (berdasarkan nilai & kelulusan)
- Program remedial dan mentoring akademik
- Dukungan finansial (beasiswa / cicilan)
- Tingkatkan keterlibatan (aktif kuliah & evaluasi)
- Pendekatan personal untuk mahasiswa berisiko tinggi
- Gunakan dashboard & model prediksi untuk tracking
