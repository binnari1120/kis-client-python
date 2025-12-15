def kis_spot_inter_process_rate_limited(func):
    async def wrapper(self, *args, **kwargs):
        limiter = getattr(self, "_spot_inter_process_rate_limiter", None)
        if limiter:
            await limiter.acquire()
        return await func(self, *args, **kwargs)

    return wrapper
