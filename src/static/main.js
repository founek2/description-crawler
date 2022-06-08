let places = [];
const internalAPI = 'https://api.demo.steller.co/v1/places/internal';
async function handleOptionClick(id) {
    // const place = places.find((place) => place.id == id);
    // const placeTypes = place.data.types;
    // console.log('placeTypes', placeTypes);

    const res = await fetch(`${internalAPI}/${id}`);
    const placeMoreInfo = await res.json();
    console.log(
        'place',
        placeMoreInfo.data.types.map((p) => p.id),
        placeMoreInfo.data.website_url
    );

    // "establishment" -> business result
}

async function generateOptions(places) {
    const datalist = document.querySelector('#suggestions');
    const options = places.map((place) => {
        const el = document.createElement('option');
        el.setAttribute('value', `${place.data.name} (${place.data.address})`);
        el.innerHTML = place.id;

        return el;
    });

    datalist.replaceChildren(...options);
}

const autocompleteAPI = 'https://api.demo.steller.co/v1/places/autocomplete';
async function fuzzySearch() {
    const datalist = document.querySelector('#suggestions');
    const searchTerms = document.getElementById('search-box').value;

    const opts = datalist.childNodes;
    for (var i = 0; i < opts.length; i++) {
        if (opts[i].value === searchTerms) {
            handleOptionClick(opts[i].innerHTML);
            return;
        }
    }

    const res = await fetch(`${autocompleteAPI}?text=${searchTerms}`);
    const body = await res.json();
    places = body.data;

    generateOptions(places);
}
function resetDatalist() {
    document.querySelector('#suggestions').innerHTML = document.querySelector('#default-list').innerHTML;
}

let timeout = null;
window.addEventListener('load', function () {
    this.document.addEventListener('keyup', function (e) {
        clearTimeout(timeout);
        timeout = setTimeout(fuzzySearch, 300);
    });

    resetDatalist();
    // generateOptions(internalIDs.slice(100).map((id) => ({ id, data: { address: id } })));
});
