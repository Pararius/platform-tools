def split_into_chunks(iterator, chunksize=100):
    chunk = []

    for i, line in enumerate(iterator):
        if i % chunksize == 0 and i > 0:
            yield chunk
            chunk = []
        chunk.append(line)

    yield chunk
