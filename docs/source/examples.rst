Examples
========

.. _examples:

Getting a user's bio.
#####################

An example that showcases how to fetch an account by username and acquire its bio.

.. code-block:: Python

    from recnetpy import Client
    from asyncio import get_event_loop

    async def main():
        RecNet = Client()
        user = await RecNet.accounts.get("ColinXYZ")
        bio = await user.get_bio()
        print(bio)
        await RecNet.close()

    loop = get_event_loop()
    loop.run_until_complete(main())

Calculating self cheers.
########################

An example showcasing how to fetch an account, acquire its RecNet images and handle a large amount of requests for cheers.

.. code-block:: Python

    import time
    import asyncio
    from recnetpy import Client

    async def main():
        RecNet = Client()
        user = await RecNet.accounts.get("Meriesa")
        images = await user.get_images(take=100_000)  # 100,000 to make sure ALL posts are included
        
        start_time = time.perf_counter()
        
        # Filter out images that have no cheers since they can't possibly be self-cheered
        cheered_images = list(filter(lambda image: image.cheer_count, images))
        
        # Create co-routines for fetching the cheers of the images
        coroutines = map(lambda image: image.get_cheers(), cheered_images)
        
        # Fetch the cheers
        cheered_player_ids = await asyncio.gather(*coroutines)
        
        # Exclude images that are self-cheered
        self_cheered_images = list(filter(lambda image: user.id in image, cheered_player_ids))
        
        end_time = time.perf_counter()
        
        # Print results
        print(
            f"Self-cheers: {len(self_cheered_images):,}",
            f"Images checked: {len(images):,}",
            f"Time elapsed: {round(end_time-start_time, 2)} seconds",
            sep="\n"
        )
        
        await RecNet.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())