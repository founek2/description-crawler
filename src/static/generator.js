export const $ = document.querySelectorAll.bind(document);
export const $1 = document.querySelector.bind(document);

export function buildTag(tagName, children, options = {}) {
    if (!Array.isArray(children)) children = [children];

    const tag = document.createElement(tagName);
    Object.entries(options).forEach(([key, val]) => {
        if (key === 'actions') {
            Object.entries(val).forEach(([event, fn]) => {
                tag.addEventListener(event, fn);
            });
        } else if (val !== null) tag.setAttribute(key, val);
    });
    flatten(children)
        .map((el) => (typeof el === 'string' ? document.createTextNode(el) : el))
        .forEach(tag.appendChild.bind(tag));
    return tag;
}

function buildMultiple({ answers, question, result }, idx) {
    return buildTag('div', [
        buildRow(
            'Otázka',
            buildTag('input', [], {
                value: question,
                type: 'text',
                class: 'form-control-plaintext',
                name: `Multiple.${idx}.question`,
            })
        ),
        buildRow(
            'Typ',
            buildTag('label', ['Multiple'], {
                class: 'form-control-plaintext',
            })
        ),

        Object.entries(answers).map(([k, val]) =>
            buildRow(
                `Odpověď ${k}`,
                //val
                buildTag('input', [], {
                    value: val,
                    type: 'text',
                    class: 'form-control-plaintext',
                    name: `Multiple.${idx}.answers.${k}`,
                })
            )
        ),
        buildRow(
            'Odpověď - správně',
            buildTag(
                'select',
                Object.keys(answers).map((k) =>
                    buildTag('option', [k], { selected: k === result ? 'selected' : null })
                ),
                { class: 'form-control', name: `Multiple.${idx}.result` }
            )
        ),
        buildTag('button', ['Smazat'], { class: 'btn btn-secondary', actions: { click: () => removeMultiple(idx) } }),
    ]);
}

function buildTF({ question, result }, idx) {
    return buildTag('div', [
        buildRow(
            'Otázka',
            buildTag('input', [], {
                value: question,
                type: 'text',
                class: 'form-control-plaintext',
                name: `TF.${idx}.question`,
            })
        ),
        buildRow(
            'Typ',
            buildTag('label', ['True/False'], {
                class: 'form-control-plaintext',
            })
        ),
        buildRow('Odpověď - správně', [
            buildTag('input', [], {
                checked: result === 'false' ? 'checked' : null,
                value: 'false',
                type: 'radio',
                name: `TF.${idx}.result`,
            }),
            buildTag('label', ['Nepravda'], {}),
            buildTag('input', [], {
                checked: result === 'true' ? 'checked' : null,
                value: 'true',
                type: 'radio',
                name: `TF.${idx}.result`,
            }),
            buildTag('label', ['Pravda'], {}),
        ]),
        buildTag('button', ['Smazat'], { class: 'btn btn-secondary', actions: { click: () => removeTF(idx) } }),
    ]);
}

function buildRow(labelName, inputValue) {
    return buildTag(
        'div',
        [
            buildTag('label', [labelName], { class: 'col-sm-2 col-form-label' }),
            buildTag(
                'div',
                [
                    typeof inputValue === 'string'
                        ? buildTag('input', [], { value: inputValue, type: 'text', class: 'form-control-plaintext' })
                        : inputValue,
                ],
                { class: 'col-sm-8' }
            ),
        ],
        { class: 'form-group row' }
    );
}

function head(arr) {
    return arr[0];
}
function key(obj) {
    return head(Object.keys(obj));
}
function value(obj) {
    return head(Object.values(obj));
}

function concat(arr1, arr2) {
    return arr1.concat(arr2);
}
function flatten(arr) {
    return arr.flat(10);
}

console.log('test', deepen({ 'a.4.c': 4, 'a.1.s': 4 }));

function deepen(obj) {
    const result = {};

    // For each object path (property key) in the object
    for (const objectPath in obj) {
        // Split path into component parts
        const parts = objectPath.split('.');

        // Create sub-objects along path as needed
        let target = result;
        while (parts.length > 1) {
            const part = parts.shift();
            if (target[part]) {
                target = target[part] = target[part];
            } else target = target[part] = isNaN(parts[0]) ? {} : [];
        }

        // Set value at end of path
        target[parts[0]] = obj[objectPath];
    }

    return result;
}
