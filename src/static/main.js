import { randomIDs } from './ids.js';
import { fuzzySearch } from './steller.js';

async function getInfoByID(id) {
    const res = await fetch(`https://api.demo.steller.co/v1/places/internal/${id}`);
    return res.json();
}
async function handleOptionClick(id) {
    const res2 = await fetch(`/crawl?id=${id}`);
    const arr = await res2.json();
    showResults(arr);

    // "establishment" -> business result
}

async function generateOptionsFromIDs(ids) {
    console.log('ids', ids);
    const arr = ids.map(
        (id, i) =>
            new Promise((resolve) => {
                setTimeout(async () => {
                    resolve(await getInfoByID(id));
                }, i * 200);
            })
    );
    const places = await Promise.all(arr);
    generateOptions(places);
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

function resetDatalist(dataListID) {
    document.querySelector('#suggestions').innerHTML = document.querySelector(`#${dataListID}`).innerHTML;
}

function showResults(arr) {
    const section = document.querySelector('#results-section');
    section.textContent = '';
    arr.forEach((item) => {
        const h2 = document.createElement('h1');
        h2.innerHTML = item.heading;
        section.appendChild(h2);

        item.paragraphs.forEach((text) => {
            const p = document.createElement('p');
            p.innerHTML = text;
            section.appendChild(p);
        });
    });
}

let timeout = null;
window.addEventListener('load', function () {
    this.document.addEventListener('keyup', function (e) {
        clearTimeout(timeout);
        timeout = setTimeout(fuzzySearch.bind(null, generateOptions, handleOptionClick, resetDatalist), 300);
    });

    resetDatalist('random-list');
    // generateOptions(internalIDs.slice(100).map((id) => ({ id, data: { address: id } })));
});
