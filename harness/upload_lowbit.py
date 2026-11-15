import sys
from huggingface_hub import HfApi
api = HfApi(); rid = "ayodejiades/tiny-aya-global-lowbit-GGUF"
for f in sys.argv[1:]:
    api.upload_file(path_or_fileobj=f"models/ours/{f}", path_in_repo=f, repo_id=rid, repo_type="model"); print("uploaded", f, flush=True)
