from ath_module import run_ath_update

def refresh_signals():
    ath_events = run_ath_update()
    for token, meta in ath_events.items():
        trigger_strategy(token, meta)
