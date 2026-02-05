
import torch
import sys

print(f"Python version: {sys.version}")
print(f"Torch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"Device: {torch.cuda.get_device_name(0)}")

try:
    import flash_attn
    print(f"\nFlash Attention version: {flash_attn.__version__}")
    print(f"Flash Attention file: {flash_attn.__file__}")
except ImportError:
    print("\nFlash Attention not installed")

print("\nChecking specific imports:")

try:
    from flash_attn.flash_attn_interface import flash_attn_kvpacked_func
    print("SUCCESS: from flash_attn.flash_attn_interface import flash_attn_kvpacked_func")
except ImportError as e:
    print(f"FAILED: from flash_attn.flash_attn_interface import flash_attn_kvpacked_func ({e})")

try:
    from flash_attn.flash_attn_interface import flash_attn_func
    print("SUCCESS: from flash_attn.flash_attn_interface import flash_attn_func")
except ImportError as e:
    print(f"FAILED: from flash_attn.flash_attn_interface import flash_attn_func ({e})")

try:
    from flash_attn.flash_attn_interface import flash_attn_unpadded_func
    print("SUCCESS: from flash_attn.flash_attn_interface import flash_attn_unpadded_func")
except ImportError as e:
    print(f"FAILED: from flash_attn.flash_attn_interface import flash_attn_unpadded_func ({e})")

try:
    from flash_attn.bert_padding import pad_input, unpad_input
    print("SUCCESS: from flash_attn.bert_padding import pad_input, unpad_input")
except ImportError as e:
    print(f"FAILED: from flash_attn.bert_padding import pad_input, unpad_input ({e})")

try:
    from flash_attn.layers.rotary import apply_rotary_emb_func
    print("SUCCESS: from flash_attn.layers.rotary import apply_rotary_emb_func")
except ImportError as e:
    print(f"FAILED: from flash_attn.layers.rotary import apply_rotary_emb_func ({e})")
