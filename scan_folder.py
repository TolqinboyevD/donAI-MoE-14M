import os
import sys
import time
import argparse
import torch
import torch.nn.functional as F
from tqdm import tqdm

# Ranglar
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

try:
    from model_core import DAISentinel, DAIConfig
except ImportError:
    print(f"{Colors.FAIL}⚠️  XATOLIK: 'model_core.py' fayli topilmadi!{Colors.ENDC}")
    print("Dastur ishlashi uchun model yadrosi (model_core.py) kerak.")
    sys.exit()

def print_banner():
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print(r"""
     _              _    ___ 
  __| | ___  _ __  / \  |_ _|
 / _` |/ _ \| '_ \/ _ \  | | 
| (_| | (_) | | |/ ___ \ | | 
 \__,_|\___/|_| /_/   \_\___|
                             
  donAI-MoE-14M (Mass Scanner)
    """)
    print(f"{Colors.ENDC}")

def scan_directory(folder_path, model_path="dai_moe_100.pth"):
    if not os.path.exists(folder_path):
        print(f"{Colors.FAIL}❌ Xatolik: Papka topilmadi: {folder_path}{Colors.ENDC}")
        return

    print(f"{Colors.HEADER}📂 PAPKANI TEKSHIRISH BOSHLANDI: {folder_path}{Colors.ENDC}")
    
    # 1. Konfiguratsiya va Modelni yuklash
    config = DAIConfig()
    model = DAISentinel(config)
    
    if not os.path.exists(model_path):
        if os.path.exists(os.path.join("models", model_path)):
            model_path = os.path.join("models", model_path)
        else:
            print(f"{Colors.FAIL}❌ Model fayli topilmadi: {model_path}{Colors.ENDC}")
            return

    try:
        checkpoint = torch.load(model_path, map_location='cpu')
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        else:
            model.load_state_dict(checkpoint)
        model.eval()
    except Exception as e:
        print(f"{Colors.FAIL}❌ Model xatoligi: {e}{Colors.ENDC}")
        return

    # 2. Fayllarni yig'ish
    files_to_scan = []
    print(f"{Colors.BLUE}⏳ Fayllar ro'yxati tuzilmoqda...{Colors.ENDC}")
    
    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                files_to_scan.append(os.path.join(root, file))
    except Exception as e:
        print(f"❌ Fayllarni o'qishda xatolik: {e}")
        return
            
    if not files_to_scan:
        print("❌ Papka bo'sh!")
        return

    print(f"🔍 Jami fayllar: {len(files_to_scan)} ta")
    
    # 3. Skanerlash jarayoni
    infected_files = []
    clean_count = 0
    start_time = time.time()

    try:
        # TQDM progress bar
        for file_path in tqdm(files_to_scan, unit="fayl", desc="Skanerlanmoqda", leave=True):
            try:
                # Faylni o'qish
                with open(file_path, "rb") as f:
                    file_bytes = list(f.read(config.block_size))
                
                # Padding
                if len(file_bytes) < config.block_size:
                    file_bytes += [0] * (config.block_size - len(file_bytes))
                else:
                    file_bytes = file_bytes[:config.block_size]
                
                input_tensor = torch.tensor([file_bytes], dtype=torch.long)
                
                # Inference
                with torch.no_grad():
                    logits, _ = model(input_tensor)
                    probs = F.softmax(logits, dim=-1)
                    virus_score = probs[0][1].item() * 100
                    
                if virus_score > 50:
                    infected_files.append((file_path, virus_score))
                else:
                    clean_count += 1
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}⚠️  Jarayon foydalanuvchi tomonidan to'xtatildi!{Colors.ENDC}")
                break
            except Exception:
                # O'qib bo'lmaydigan fayllar tashlab ketiladi
                pass 

    except KeyboardInterrupt:
        print("\nTo'xtatilmoqda...")

    # 4. Yakuniy hisobot
    duration = time.time() - start_time
    
    print("\n" + "="*50)
    print(f"📊 YAKUNIY HISOBOT ({duration:.2f} soniya)")
    print("="*50)
    print(f"🟢 Toza fayllar: {clean_count} ta")
    
    if infected_files:
        print(f"{Colors.FAIL}🔴 Viruslar:      {len(infected_files)} ta{Colors.ENDC}")
        print("-" * 50)
        print(f"{Colors.FAIL}{Colors.BOLD}🚨 TOPILGAN XAVFLAR:{Colors.ENDC}")
        
        # Ro'yxatni chiroyli chiqarish
        for i, (fpath, score) in enumerate(infected_files):
            if i >= 20:
                print(f"   ... va yana {len(infected_files) - 20} ta fayl.")
                break
            short_name = os.path.basename(fpath)
            # Agar fayl nomi juda uzun bo'lsa qisqartirish
            if len(short_name) > 40: short_name = short_name[:37] + "..."
            
            # Xavf darajasiga qarab belgi
            icon = "💀" if score > 80 else "⚠️ "
            print(f"  {icon} [{score:.1f}%] {short_name}")
    else:
        print(f"🔴 Viruslar:      0 ta")
        print("-" * 50)
        print(f"{Colors.GREEN}{Colors.BOLD}✅ Tizim toza! Virus topilmadi.{Colors.ENDC}")
    print("="*50)

if __name__ == "__main__":
    print_banner()
    
    parser = argparse.ArgumentParser(description='donAI-MoE-14M Mass Scanner')
    parser.add_argument("folder", nargs="?", help="Tekshiriladigan papka manzili")
    args = parser.parse_args()
    
    if args.folder:
        scan_directory(args.folder)
    else:
        try:
            target = input(f"{Colors.BLUE}Qaysi papkani tekshiramiz? manzili: {Colors.ENDC}")
            if target.strip():
                scan_directory(target.strip())
            else:
                print("❌ Papka kiritilmadi.")
        except KeyboardInterrupt:
            print("\nChiqilmoqda...")
