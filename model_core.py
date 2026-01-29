import torch
import torch.nn as nn
from torch.nn import functional as F

class DAIConfig:
    vocab_size = 262        
    block_size = 1024       
    n_embd = 256            
    n_head = 8              
    n_layer = 6             
    num_experts = 4         
    top_k = 2               
    dropout = 0.1
    device = 'cpu'

class Expert(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(config.n_embd, 4 * config.n_embd),
            nn.GELU(),
            nn.Linear(4 * config.n_embd, config.n_embd),
            nn.Dropout(config.dropout),
        )
    def forward(self, x): return self.net(x)

class MoELayer(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.router = nn.Linear(config.n_embd, config.num_experts)
        self.experts = nn.ModuleList([Expert(config) for _ in range(config.num_experts)])
        self.top_k = config.top_k

    def forward(self, x):
        logits = self.router(x)
        weights, indices = torch.topk(F.softmax(logits, dim=-1), self.top_k, dim=-1)
        B, T, C = x.shape
        out = torch.zeros_like(x)
        flat_x = x.view(-1, C)
        flat_indices = indices.view(-1, self.top_k)
        flat_weights = weights.view(-1, self.top_k)
        for i in range(self.top_k):
            exp_idx = flat_indices[:, i]
            exp_weights = flat_weights[:, i].unsqueeze(1)
            for j, expert in enumerate(self.experts):
                mask = (exp_idx == j)
                if mask.any():
                    out.view(-1, C)[mask] += expert(flat_x[mask]) * exp_weights[mask]
        return out

class Block(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.ln1 = nn.LayerNorm(config.n_embd)
        self.attn = nn.MultiheadAttention(config.n_embd, config.n_head, batch_first=True)
        self.ln2 = nn.LayerNorm(config.n_embd)
        self.moe = MoELayer(config)

    def forward(self, x):
        attn_out, _ = self.attn(self.ln1(x), self.ln1(x), self.ln1(x), need_weights=False)
        x = x + attn_out
        x = x + self.moe(self.ln2(x))
        return x

class DAISentinel(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.token_emb = nn.Embedding(config.vocab_size, config.n_embd)
        self.pos_emb = nn.Embedding(config.block_size, config.n_embd)
        self.blocks = nn.Sequential(*[Block(config) for _ in range(config.n_layer)])
        self.ln_f = nn.LayerNorm(config.n_embd)
        self.head = nn.Linear(config.n_embd, 2)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        x = self.token_emb(idx) + self.pos_emb(torch.arange(T, device=idx.device))
        x = self.blocks(x)
        x = self.ln_f(x)
        logits = self.head(x[:, -1, :])
        return logits, None