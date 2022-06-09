const autocompleteAPI = 'https://api.demo.steller.co/v1/places/autocomplete';
export async function fuzzySearch(generateOptions, handleOptionClick, resetDatalist) {
    const datalist = document.querySelector('#suggestions');
    const searchTerms = document.getElementById('search-box').value;
    if (searchTerms.trim() == '') return resetDatalist();

    const opts = datalist.childNodes;
    for (var i = 0; i < opts.length; i++) {
        if (opts[i].value === searchTerms) {
            handleOptionClick(opts[i].innerHTML.trim());
            return;
        }
    }

    const res = await fetch(`${autocompleteAPI}?text=${searchTerms}`);
    const body = await res.json();

    generateOptions(body.data);
}
