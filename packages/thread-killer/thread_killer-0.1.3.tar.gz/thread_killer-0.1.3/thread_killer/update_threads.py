from datetime import datetime, timedelta
from typing import Callable


def update_alive_threads(all_threads: dict, running_wallets: list,
                         thread_lifetime: int, set_run_status: Callable[[int, bool], None], logger) -> dict:
    """
    method kills zombie threads and return only actual threads
    """
    if not running_wallets:
        return {}

    running_wallets_ids = [wallet.id for wallet in running_wallets]
    alive_threads_only = {run_wallet: all_threads[run_wallet] for run_wallet
                          in running_wallets_ids if run_wallet in all_threads}

    for wallet_id, thread in list(alive_threads_only.items()):
        if datetime.now() - thread.start_time > timedelta(seconds=thread_lifetime):
            thread.thread.kill()
            set_run_status(wallet_id, False)
            logger.info(f"--INFO Kill thread with wallet_id: {wallet_id}")
            del alive_threads_only[wallet_id]

    return alive_threads_only
