import torch
import torch.nn.functional as F
import sys
import os
import argparse
import time

# Ranglar (ANSI Escape Codes)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# MUHIM O'ZGARISH: train.py dan emas, model_core.py dan olamiz!
try:
    from model_core import DAISentinel, DAIConfig
except ImportError:
    print(f"{Colors.FAIL}⚠️  XATOLIK: 'model_core.py' fayli topilmadi!{Colors.ENDC}")
    print("Dastur ishlashi uchun model yadrosi (model_core.py) kerak.")
    sys.exit()

def print_banner():
    print(f"{Colors.CYAN}{Colors.BOLD}")
    # Yangi "donAI" ASCII Art
    print(r"""
     _              _    ___ 
  __| | ___  _ __  / \  |_ _|
 / _` |/ _ \| '_ \/ _ \  | | 
| (_| | (_) | | |/ ___ \ | | 
 \__,_|\___/|_| /_/   \_\___|
                             
  donAI-MoE-14M (Beta)
    """)
    print(f"{Colors.ENDC}")

def scan_file(file_path, model_path="dai_moe_100.pth"):
    if not os.path.exists(file_path):
        print(f"{Colors.FAIL}❌ Xatolik: '{file_path}' fayli topilmadi.{Colors.ENDC}")
        return

    print(f"{Colors.BLUE}🔍 Tizim ishga tushdi...{Colors.ENDC}")
    print(f"📁 Tekshirilayotgan fayl: {Colors.BOLD}{file_path}{Colors.ENDC}")
    
    # 1. Konfiguratsiya va Model
    config = DAIConfig()
    model = DAISentinel(config)
    
    # 2. Modelni yuklash
    # Agar model models/ papkasida bo'lsa, yo'lni tekshiramiz
    if not os.path.exists(model_path):
        # Ehtimol model 'models' papkasidadir?
        if os.path.exists(os.path.join("models", model_path)):
            model_path = os.path.join("models", model_path)
        else:
            print(f"{Colors.FAIL}❌ Model fayli topilmadi: {model_path}{Colors.ENDC}")
            print("Iltimos, dai_moe_100.pth faylini shu yerga qo'ying.")
            return

    try:
        checkpoint = torch.load(model_path, map_location='cpu')
        
        # Checkpoint strukturasi har xil bo'lishi mumkinligini hisobga olish
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        else:
            model.load_state_dict(checkpoint)
            
        model.eval() # Inference Mode
    except Exception as e:
        print(f"{Colors.FAIL}❌ Model buzilgan yoki mos emas: {e}{Colors.ENDC}")
        return

    # 3. Faylni o'qish va tahlil qilish
    start_time = time.time()
    try:
        with open(file_path, "rb") as f:
            file_bytes = list(f.read(config.block_size))
            
        # Padding
        if len(file_bytes) < config.block_size:
            file_bytes += [0] * (config.block_size - len(file_bytes))
        else:
            file_bytes = file_bytes[:config.block_size]
            
        input_tensor = torch.tensor([file_bytes], dtype=torch.long)

        # 4. Hukm (Inference)
        with torch.no_grad():
            logits, _ = model(input_tensor)
            probs = F.softmax(logits, dim=-1)
            
            clean_score = probs[0][0].item() * 100
            virus_score = probs[0][1].item() * 100

        # 5. Natijani chiqarish
        duration = (time.time() - start_time) * 1000 # ms
        
        print("\n" + "-" * 40)
        print(f"📊 TAHLIL NATIJASI ({duration:.1f} ms):")
        print("-" * 40)
        
        print(f"🟢 Toza fayl ehtimoli: {clean_score:.2f}%")
        
        # Xavf darajasiga qarab rang o'zgaradi
        if virus_score > 50:
            virus_color = Colors.FAIL
        else:
            virus_color = Colors.GREEN
            
        print(f"{virus_color}🔴 Virus ehtimoli:     {virus_score:.2f}%{Colors.ENDC}")
        print("-" * 40)
        
        if virus_score > 80:
            print(f"\n{Colors.FAIL}{Colors.BOLD}🚨 KRITIK XAVF: BU FAYL ANIQP VIRUS! ({virus_score:.1f}%){Colors.ENDC}")
            print(f"{Colors.FAIL}🚫 Tizim tomonidan bloklandi!{Colors.ENDC}")
        elif virus_score > 50:
             print(f"\n{Colors.WARNING}{Colors.BOLD}⚠️  SHUBHALI FAYL: Ehtiyot bo'ling!{Colors.ENDC}")
        else:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ XAVFSIZ: Hech qanday tahdid topilmadi.{Colors.ENDC}")

    except Exception as e:
        print(f"{Colors.FAIL}❌ Tahlil jarayonida xatolik: {e}{Colors.ENDC}")

if __name__ == "__main__":
    print_banner()
    
    # Argumentlarni qabul qilish (Nomi ham o'zgardi)
    parser = argparse.ArgumentParser(description='donAI-MoE-14M (Beta) - AI Antivirus Scanner')
    parser.add_argument('file', nargs='?', help='Tekshiriladigan fayl manzili')
    args = parser.parse_args()
    
    if args.file:
        scan_file(args.file)
    else:
        # Agar argument berilmasa, so'raymiz
        try:
            target = input(f"{Colors.BLUE}Fayl manzilini kiriting: {Colors.ENDC}")
            if target.strip():
                scan_file(target.strip())
            else:
                print("❌ Fayl kiritilmadi.")
        except KeyboardInterrupt:
            print("\nChiqilmoqda...")