import { randomIDs } from './ids.js';
import { fuzzySearch } from './steller.js';
import japanResponse from './japan.js';
import { buildResult, buildResults, buildSelectionForm } from './builder.js';
import { buildTag } from './generator.js';
import { streamCrawl } from './crawl.js';

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

async function crawlID(id) {
    return fetch(`/crawl?id=${id}`).then((res) => res.json());
}

async function handleOptionClick(id) {
    showLoader();
    try {
        clearResults();
        await streamCrawl(id, handleStreamSection);
        // const { data } = await crawlID(id);
        // showResults(data);
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

function showResult(section) {
    const tag = buildResult(section);
    const sectionElement = document.querySelector('#results-section');
    sectionElement.appendChild(tag);
}

function showResults(sections) {
    const tag = buildResults(sections);
    const sectionElement = document.querySelector('#results-section');
    sectionElement.appendChild(tag);
}

async function processIDs(ids) {
    showLoader();
    clearResults();
    try {
        const sectionElement = document.querySelector('#results-section');
        for (const id of ids) {
            // const json = await crawlID(id);
            // results.push(json);
            let showHeader = true;

            await streamCrawl(id, (section, { place }) => {
                if (showHeader) {
                    showHeader = false;
                    const addr = place.data.address.split(', ');
                    sectionElement.appendChild(buildTag('h1', place.data.name + ' -  ' + addr[addr.length - 1]));
                }
                handleStreamSection(section);
            });
        }

        // results.forEach(({ data, place }) => {

        //     const addr = place.data.address.split(', ');
        //     sectionElement.appendChild(buildTag('h1', place.data.name + ' -  ' + addr[addr.length - 1]));
        //     showResults(data);
        // });
    } catch (err) {
        console.error(err);
    }

    hideLoader();
}

async function handleStreamSection(section) {
    console.log('handle', section);
    showResult(section);
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

    // resetDatalist('random-list');

    const randomList = document.querySelector('#random-list');
    const form = buildSelectionForm(randomList, processIDs);
    const section = this.document.querySelector('#results-section');
    section.replaceChildren(form);

    // streamCrawl('3e5fa772-b720-4a89-9aac-a4c9149bca7c', handleStreamSection);

    // showResults(japanResponse);
    // generateOptions(internalIDs.slice(100).map((id) => ({ id, data: { address: id } })));
});
