import math
from dataclasses import dataclass
from typing import Union

import torch
from aislib.misc_utils import get_logger
from torch import nn, Tensor
from torch.nn import TransformerEncoder, TransformerEncoderLayer

logger = get_logger(name=__name__, tqdm_compatible=True)


@dataclass
class BasicTransformerModelConfig:
    """
    :param embedding_dim:
        Which dimension to use for the embeddings. If ``None``, will autoamtically set
        this value based on the number of tokens and attention heads.

    :param num_heads:
        The number of heads in the multi-head attention models

    :param num_layers:
        The number of encoder blocks in the transformer model.

    :param dropout:
        Common dropout value to use in (a) the positional encoding and (b) the encoder
        layers.
    """

    embedding_dim: Union[int, None] = None
    num_heads: int = 8
    num_layers: int = 2
    dropout: float = 0.10


class TransformerModel(nn.Module):
    def __init__(
        self,
        model_config: BasicTransformerModelConfig,
        num_tokens: int,
        max_length: int,
    ) -> None:
        super().__init__()

        self.model_config = model_config
        self.num_tokens = num_tokens
        self.max_length = max_length

        self.embedding_dim = model_config.embedding_dim
        if self.model_config.embedding_dim is None:
            auto_emb_dim = (
                math.ceil((int(num_tokens ** 0.25) / self.model_config.num_heads))
                * self.model_config.num_heads
            )
            logger.info(
                "Setting up automatic embedding dimension of %d based on %d "
                "tokens and %d attention heads.",
                auto_emb_dim,
                self.num_tokens,
                self.model_config.num_heads,
            )
            self.embedding_dim = auto_emb_dim

        self.pos_encoder = PositionalEncoding(
            embedding_dim=self.embedding_dim, dropout=model_config.dropout
        )
        encoder_layers = TransformerEncoderLayer(
            d_model=self.embedding_dim,
            nhead=model_config.num_heads,
            dim_feedforward=self.max_length,
            dropout=model_config.dropout,
        )
        self.transformer_encoder = TransformerEncoder(
            encoder_layer=encoder_layers, num_layers=model_config.num_layers
        )
        self.embedding = nn.Embedding(
            num_embeddings=self.num_tokens, embedding_dim=self.embedding_dim
        )

        self.init_weights()

    @property
    def num_out_features(self) -> int:
        return self.max_length * self.embedding_dim

    def embed_tokens(self, input: torch.Tensor) -> torch.Tensor:
        return self.embedding(input)

    def init_weights(self) -> None:
        init_range = 0.1
        self.embedding.weight.data.uniform_(-init_range, init_range)

    def forward(self, input: Tensor) -> Tensor:

        out = input * math.sqrt(self.embedding_dim)
        out = self.pos_encoder(out)
        out = self.transformer_encoder(out)
        return out.flatten(1)


def next_power_of_2(x: int) -> int:
    if x == 0:
        return 1

    return 2 ** math.ceil(math.log2(x))


class PositionalEncoding(nn.Module):
    def __init__(
        self, embedding_dim: int, dropout: float = 0.1, max_len: int = 5000
    ) -> None:
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, embedding_dim, 2) * (-math.log(10000.0) / embedding_dim)
        )
        pe = torch.zeros(max_len, 1, embedding_dim)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer("pe", pe)

    def forward(self, x: Tensor) -> Tensor:
        x = x + self.pe[: x.size(0)]
        return self.dropout(x)
