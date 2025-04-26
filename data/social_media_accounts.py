import numpy as np
import pandas as pd

def social_media_accounts(n_accounts: int = 1_000, misinfo_rate: float = 0.07,seed: int = 2025) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
  
    primary_platform = rng.integers(0, 5, n_accounts, dtype=np.int8)

    account_age_days = rng.exponential(scale=365 * 2, size=n_accounts).astype(np.int32)
    followers_cnt = rng.lognormal(mean=6, sigma=1.3, size=n_accounts).astype(np.int32)
    verified_flag = rng.integers(0, 2, size=n_accounts, dtype=np.int8)  # 0/1


    base_post_rate = rng.gamma(shape=1.8, scale=0.7, size=n_accounts)

    prior_flags_cnt = rng.poisson(lam=0.15, size=n_accounts).astype(np.int8)
    strike_count = rng.poisson(lam=0.05, size=n_accounts).astype(np.int8)


    label = rng.choice([0, 1], size=n_accounts, p=[1.0 - misinfo_rate, misinfo_rate]).astype(
        np.int8
    )

    misinfo_mask = label == 1

    followers_cnt[misinfo_mask] = (followers_cnt[misinfo_mask] * rng.uniform(1.1, 2.0, size=misinfo_mask.sum())).astype(np.int32)
    base_post_rate[misinfo_mask] += rng.gamma(shape=2, scale=1.0, size=misinfo_mask.sum())
    prior_flags_cnt[misinfo_mask] += rng.poisson(lam=2.0, size=misinfo_mask.sum()).astype(np.int8)
    strike_count[misinfo_mask] += rng.poisson(lam=1.0, size=misinfo_mask.sum()).astype(np.int8)


    avg_daily_likes = (base_post_rate * rng.lognormal(mean=3, sigma=1.0, size=n_accounts)).astype(np.int32)
    avg_daily_reshares = (base_post_rate * rng.lognormal(mean=1.8, sigma=0.8, size=n_accounts)).astype(np.int16)
    avg_daily_comments = (base_post_rate * rng.lognormal(mean=2.0, sigma=0.9, size=n_accounts)).astype(np.int16)


    df = pd.DataFrame(
        {
            "account_id": np.arange(1, n_accounts + 1, dtype=np.int32),
            "primary_platform": primary_platform,
            "account_age_days": account_age_days,
            "verified_flag": verified_flag,
            "followers_cnt": followers_cnt,
            "base_post_rate": base_post_rate,
            "prior_flags_cnt": prior_flags_cnt,
            "strike_count": strike_count,
            "avg_daily_likes": avg_daily_likes,
            "avg_daily_reshares": avg_daily_reshares,
            "avg_daily_comments": avg_daily_comments,
            "label": label
        }
    )

    return df

if __name__ == "__main__":
    df = social_media_accounts()
    df.to_csv("social_media_accounts_data.csv", index=False)
    print(df.head().to_markdown())
