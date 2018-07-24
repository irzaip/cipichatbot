
#WHY?

Apa gunanya program ini.
Program ini dibuat untuk kita bisa menggunakan suara dalam mengoperasikan komputer.
Program ini didesain agar input yang dilakukan oleh user sangat fleksibel. Kadang Untuk memberikan instruksi kita harus mengingat 1 kata dengan tepat, tetapi dengan program ini kita usahakan agar bermacam-macam teknik input bisa dapat dilakukan.
Program ini menggunakan neural Network agar bisa mengenali perintah yang dilakukan oleh user. Cara menggunakan neural Network ini berbeda dengan pemrograman yang sangat struktural.
Neural Network yang digunakan diharapkan dapat mengenali flow pembicaraan, app ini menggunakan tensorflow dan keras.
Program ini dibagi tiga tahap yaitu pengenalan Hot Word (kata panas).
Lalu pindah ke pengenalan instruksi awal, hal ini memisahkan antara percakapan biasa dengan sebuah instruksi yang spesifik. Hal ini memisahkan antara percakapan biasa dengan sebuah instruksi yang spesifik.
Instruksi yang spesifik menggunakan script tambahan seperti add-on yang di letakkan di direktori data.
Anda bisa menemukan bermacam-macam instruksi yang berkaitan dalam folder tersebut.

##FILE PENTING dalam direktori DATA

input.txt - macam-macam input pengenalan dalam bentuk susunan kata-kata
sinonim.txt - Untuk membuat permutasi dari instruksi

___instruksi.py  - berisi skrip python sebagai ADD-ON


##PROSES TRAINING
sekarang ini masih menggunakan jupyter. nanti akan dibuatkan script langsung.


####Trainer-Word2Vec-Builder1.ipynb
Jantung dari chatting, berupa trainer untuk membentuk seluruh VECTOR dari setiap kata yang bisa di kenali oleh bot.


####Trainer-WordRecognizer.ipynb

####Trainer-Intent-classifier.ipynb
Trainer untuk membuat klasifikasi intent menjadi sebuah database prediksi.

####Trainer-BasicChitchat.ipynb
Trainer untuk membuat chitchat yang sederhana, apabila tidak dikenali sebuah intent, maka 
akan masuk ke chit-chat umum. dan disini bisa di tuliskan script pembicaraan.
dialog akan masuk di direktori dialog dgn extention .TXT
dgn format A: Pertanyaan  B: Jawaban bot

####Trainer-TheMiddleBot.ipynb
di harapkan bisa Generate kalimat dari sebuah vektor kecil.  -> tidak sempurna

####file BASICSCRAPER-xxx.ipynb
file kumpulan scraping, website berisi text2 indonesia, kamus dll.

####Cipi-theChatbot.ipynb
File untuk jalan apps dalam betuk Jupyter

####Cipi-theChatbot.py
File untuk jalan apps dalam betuk Python asli.
gunakan file .cmd sebagai batch file

####Debugger-Chat.ipynb
untuk keperluan logging dan debugger dari chat secara mengetik, gunakan app ini.

####chat_iface.py  
Berisi rutin interface ke selenium

####chat_proc.py
Berisi rutin interface process sebuah input menjadi output Reply.

####chat_wordvec.py
Berisi rutin mengkonversi text menjadi vektor

####chitchat.py
Rutin untuk chitchat saja.

####intent_builder.py
Rutin untuk loading intent sebagai Add ON

####preprocess.py
Merubah audio signal menjadi class yang bisa di kenali.

