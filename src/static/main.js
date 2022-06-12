import { randomIDs } from './ids.js';
import { fuzzySearch } from './steller.js';

function showLoader() {
    document.querySelector('.loader').classList.remove('hidden');
}
function hideLoader() {
    document.querySelector('.loader').classList.add('hidden');
}

async function getInfoByID(id) {
    const res = await fetch(`https://api.demo.steller.co/v1/places/internal/${id}`);
    return res.json();
}

async function handleOptionClick(id) {
    showLoader();
    try {
        clearResults();

        const res2 = await fetch(`/crawl?id=${id}`);
        const arr = await res2.json();
        showResults(arr);
    } catch (err) {
        console.error(err);
    }

    hideLoader();
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

function clearResults() {
    const section = document.querySelector('#results-section');
    section.textContent = '';
}

function showResults(arr) {
    clearResults();

    const section = document.querySelector('#results-section');
    arr.forEach((item) => {
        const sectionContainer = document.createElement('div');
        const h2 = document.createElement('h1');
        h2.innerHTML = item.heading;

        const link = document.createElement('a');
        link.setAttribute('href', item.link);
        link.innerHTML = new URL(item.link).hostname;

        sectionContainer.appendChild(h2);
        sectionContainer.appendChild(link);

        item.paragraphs.forEach((text) => {
            const p = document.createElement('p');
            p.innerHTML = text;
            sectionContainer.appendChild(p);
        });
        section.appendChild(sectionContainer);
    });
}

let timeout = null;
window.addEventListener('load', function () {
    this.document.addEventListener('keyup', function (e) {
        clearTimeout(timeout);
        timeout = setTimeout(
            fuzzySearch.bind(null, generateOptions, handleOptionClick, resetDatalist.bind(null, 'random-list')),
            300
        );
    });

    resetDatalist('random-list');
    // generateOptions(internalIDs.slice(100).map((id) => ({ id, data: { address: id } })));
});
