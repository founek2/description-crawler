import { buildTag, $1, $ } from './generator.js';

export function buildResult(section) {
    const maxScore = Math.max(...section.keywords.map((item) => item.distance.score));
    const paragraphs = section.paragraphs.map((text) => buildTag('p', [text]));
    const kws = section.keywords.map((item) =>
        buildTag('span', [
            buildTag('b', item.kw),
            ` (score: ${item.score.toFixed(3)}, distance: ${item.distance.score.toFixed(3)} (${item.distance.alg})) `,
        ])
    );
    return buildTag(
        'div',
        [
            buildTag('h2', [section.heading]),
            buildTag(
                'span',
                [
                    buildTag('a', [new URL(section.link).hostname], { href: section.link, target: '_blank' }),
                    ` [${maxScore.toFixed(3)}]`,
                ],
                { class: 'link-container' }
            ),

            ...paragraphs,
            ...kws,
        ],
        { class: 'section' }
    );
}

export function buildResults(sections) {
    return buildTag('div', sections.map(buildResult));
}

function handleSubmit(cb) {
    return (e) => {
        e.preventDefault();
        const form = $1('form');
        const data = new FormData(form);
        const obj = Object.fromEntries(data.entries());

        cb(Object.values(obj));
    };
}

export function buildSelectionForm(dataListContainer, onSubmit) {
    const options = dataListContainer.children;
    const checkboxes = [...options].map((option, i) => {
        return buildTag('div', [
            buildTag('input', [], {
                type: 'checkbox',
                name: `id-selection-${i}`,
                value: option.innerHTML.trim(),
            }),
            buildTag('label', option.getAttribute('value')),
        ]);
    });

    return buildTag('form', [
        ...checkboxes,
        buildTag('button', 'Makej!', { actions: { click: handleSubmit(onSubmit) } }),
    ]);
}
