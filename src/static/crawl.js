function onChunkedResponseComplete(result) {
    console.log('all done!');
    return result;
}

function onChunkedResponseError(err) {
    console.error(err);
}

function processChunkedResponse(onSection) {
    return (response) => {
        if (response.status != 200) {
            return false;
        }
        var text = '';
        var reader = response.body.getReader();
        var decoder = new TextDecoder();
        let linksAndPlace = null;

        return readChunk();

        function readChunk() {
            return reader.read().then(appendChunks);
        }

        function appendChunks(result) {
            // console.log('chunk', result.value.toString(), typeof result.value);
            var chunk = decoder.decode(result.value || new Uint8Array(), { stream: !result.done });
            console.log('got chunk of', chunk.length, 'bytes');
            console.log(chunk.toString());
            if (chunk.length != 0) {
                if (!linksAndPlace) {
                    linksAndPlace = JSON.parse(chunk.toString());
                    console.log('linksAndPlace', linksAndPlace);
                } else {
                    try {
                        const section = JSON.parse(chunk.toString());
                        console.log('section', section);
                        onSection(section, linksAndPlace);
                    } catch (err) {
                        console.error(err);
                    }
                }
            }

            text += chunk;
            console.log('text so far is', text.length, 'bytes\n');
            if (result.done) {
                console.log('returning');
                return text;
            } else {
                console.log('recursing');
                return readChunk();
            }
        }
    };
}

export function streamCrawl(id, onSection) {
    return fetch('/crawl-stream?id=' + id)
        .then(processChunkedResponse(onSection))
        .then(onChunkedResponseComplete)
        .catch(onChunkedResponseError);
}
