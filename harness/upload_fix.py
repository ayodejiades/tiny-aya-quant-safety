from huggingface_hub import HfApi
a = HfApi()
a.upload_file(path_or_fileobj="models/ours/tiny-aya-global-Q3_K_S-protected.gguf", path_in_repo="tiny-aya-global-Q3_K_S-protected.gguf", repo_id="ayodejiades/tiny-aya-global-safety-protected-GGUF", repo_type="model"); print("F1 uploaded", flush=True)
a.upload_file(path_or_fileobj="models/ours/tiny-aya-global-Q3_K_S-decoy.gguf", path_in_repo="tiny-aya-global-Q3_K_S-decoy.gguf", repo_id="ayodejiades/tiny-aya-global-lowbit-GGUF", repo_type="model"); print("F2 uploaded", flush=True)
