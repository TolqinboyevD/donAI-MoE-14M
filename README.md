# donAI-MoE-14M (Beta) 🛡️

**donAI-MoE-14M** — bu **Mixture of Experts (MoE)** arxitekturasiga asoslangan ilg'or sun'iy intellekt quvvatli zararli dasturlarni aniqlash tizimi. U an'anaviy imzo usullari o'rniga bayt darajasidagi strukturaviy tahlil orqali ko'p platformalarda (Windows, Linux, Android) tahdidlarni aniqlash uchun mo'ljallangan.

---

## 🌟 Asosiy Xususiyatlar

* **Ko'p Platformali Intellekt:** Yagona birlashtirilgan model yordamida `.exe`, `.so`, `.apk` va `.dex` formatlaridagi tahdidlarni aniqlaydi.
* **Samarali Arxitektura:** 14.5M parametrli MoE Transformer arxitekturasidan foydalanadi, har bir xulosada atigi ~8.2M faol parametr bilan standart protsessorlarda yuqori samaradorlikni ta'minlaydi.
* **Maxfiylik Birinchi O'rinda:** Barcha tahlillar mahalliy darajada amalga oshiriladi. Fayllaringiz hech qachon qurilmangizdan chiqmaydi.
* **Real Vaqtda Himoya:** Maxsus kataloglarni doimiy kuzatish uchun watchdog modulini o'z ichiga oladi.

---

## 🧠 Model Arxitekturasi va Statistikasi

Asosiy qism siyrak shlyuzli MoE qatlamlari bilan 6 qatlamli Transformer hisoblanadi.

| Ko'rsatkich | Qiymat |
| :--- | :--- |
| **Jami Parametrlar** | 14,535,194 (14.5M) |
| **Faol Parametrlar** | 8,230,000 (~8.2M) |
| **Kontekst Oynasi** | 1024 Bayt (Sarlavhaga yo'naltirilgan tahlil) |
| **Xulosa Kechikishi** | ~200ms - 300ms (standart CPU da) |
| **Siyraklik (Samaradorlik)** | Hisoblashda 43.4% qisqarish |

---

## 📊 Ishlash Ko'rsatkichlari

Model toza va zararli fayllarning muvozanatli ma'lumotlar to'plamida sinovdan o'tkazildi.

* **Aniqlash Aniqligi:** ~80-88% (Joriy Beta)
* **Noto'g'ri Ijobiy Natija Darajasi:** Tizim fayllari bilan minimal aralashish uchun optimallashtirilgan (masalan, Rufus kabi murakkab vositalarni to'g'ri tasniflaydi).

---

## 🚀 O'rnatish va Sozlash

### 1. Repozitoriyani klonlash

```bash
git clone https://github.com/TolqinboyevD/donAI-MoE-14M.git
cd donAI-MoE-14M
```

### 2. Bog'liqliklarni o'rnatish

```bash
pip install -r requirements.txt
```

---

## 🔍 Foydalanish Bo'yicha Qo'llanma

### Bitta Faylni Skanerlash

Muayyan shubhali faylni tahlil qilish:

```bash
python scan.py path/to/suspicious_file.exe
```

### Katalogni Ommaviy Skanerlash

Potentsial tahdidlar uchun butun papkani skanerlash:

```bash
python scan_folder.py path/to/folder
```

---

## 📁 Repozitoriya Tuzilishi

```text
donAI-MoE-14M/
│── dai_moe_100.pth            # Oldindan o'qitilgan MoE og'irliklari (14.5M params)
├── model_core.py              # Neyron tarmoq arxitekturasi ta'riflari
├── scan.py                    # Bitta fayl tahlili uchun CLI vositasi
├── scan_folder.py             # Ommaviy katalog skaneri
├── requirements.txt           # Loyiha bog'liqliklari
└── README.md                  # Hujjatlar
```

---

## 🛡️ Ogohlantirish va Litsenziya

**Ogohlantirish:** Ushbu loyiha faqat ta'lim va tadqiqot maqsadlarida mo'ljallangan. U professional, tijorat antivirus yechimlarini almashtirish uchun mo'ljallanmagan.

**Litsenziya:** Ushbu loyiha MIT litsenziyasi ostida litsenziyalangan.

---

**Muallif:** Doniyorbek  
**Aloqa:** janobdtd@gmail.com
**Telegram:** @TolqinboyevD 
**Yaratilgan:** PyTorch, Mixture of Experts (MoE) Arxitekturasi yordamida

---

## 📚 Qo'shimcha Ma'lumot

### Texnik Tafsilotlar

Ushbu model **bayt darajasidagi tahlil** usulidan foydalanadi, bu degani u fayllarning ichki tuzilishini va strukturaviy xususiyatlarini o'rganadi. An'anaviy antivirus yechimlari ma'lum imzolarni qidiradi, donAI esa zararli naqshlarni tanib olish uchun chuqur o'rganish texnologiyasidan foydalanadi.

### Kelajak Rejalari

* Aniqlash aniqligini 95%+ ga oshirish
* Qo'shimcha fayl formatlarini qo'llab-quvvatlash
* GUI interfeysi qo'shish
* Cloud-based havo tahlili imkoniyatlari

### Hissa Qo'shish

Loyihaga hissa qo'shmoqchimisiz? Pull request yuboring yoki issue oching!

---

**© 2026 Doniyorbek. Barcha huquqlar himoyalangan.**