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

            text += chunk.toString();
            console.log('text so far is', text.length, 'bytes\n');

            if (chunk.length != 0 && text.includes('///')) {
                const parts = text.split('///');
                const toProcess = parts.slice(0, -1);
                toProcess.forEach((part) => {
                    if (!linksAndPlace) {
                        linksAndPlace = JSON.parse(part);
                        console.log('linksAndPlace', linksAndPlace);
                    } else {
                        try {
                            const section = JSON.parse(part);
                            console.log('section', section);
                            onSection(section, linksAndPlace);
                        } catch (err) {
                            console.error(err);
                        }
                    }
                });
                if (toProcess.length < parts.length) {
                    text = parts.slice(-1);
                }
            }

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
