Object.defineProperty(exports, "__esModule", { value: true });
exports.tn = exports.tct = exports.t = exports.gettextComponentTemplate = exports.ngettext = exports.gettext = exports.format = exports.renderTemplate = exports.parseComponentTemplate = exports.setLocale = exports.toggleLocaleDebug = exports.setLocaleDebug = exports.DEFAULT_LOCALE_DATA = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const jed_1 = (0, tslib_1.__importDefault)(require("jed"));
const isArray_1 = (0, tslib_1.__importDefault)(require("lodash/isArray"));
const isObject_1 = (0, tslib_1.__importDefault)(require("lodash/isObject"));
const isString_1 = (0, tslib_1.__importDefault)(require("lodash/isString"));
const sprintf_js_1 = require("sprintf-js");
const localStorage_1 = (0, tslib_1.__importDefault)(require("app/utils/localStorage"));
const markerStyles = {
    background: '#ff801790',
    outline: '2px solid #ff801790',
};
const LOCALE_DEBUG = localStorage_1.default.getItem('localeDebug') === '1';
exports.DEFAULT_LOCALE_DATA = {
    '': {
        domain: 'sentry',
        lang: 'en',
        plural_forms: 'nplurals=2; plural=(n != 1);',
    },
};
function setLocaleDebug(value) {
    localStorage_1.default.setItem('localeDebug', value ? '1' : '0');
    // eslint-disable-next-line no-console
    console.log(`Locale debug is: ${value ? 'on' : 'off'}. Reload page to apply changes!`);
}
exports.setLocaleDebug = setLocaleDebug;
/**
 * Toggles the locale debug flag in local storage, but does _not_ reload the
 * page. The caller should do this.
 */
function toggleLocaleDebug() {
    const currentValue = localStorage_1.default.getItem('localeDebug');
    setLocaleDebug(currentValue !== '1');
}
exports.toggleLocaleDebug = toggleLocaleDebug;
/**
 * Global Jed locale object loaded with translations via setLocale
 */
let i18n = null;
/**
 * Set the current application locale.
 *
 * NOTE: This MUST be called early in the application before calls to any
 * translation functions, as this mutates a singleton translation object used
 * to lookup translations at runtime.
 */
function setLocale(translations) {
    i18n = new jed_1.default({
        domain: 'sentry',
        missing_key_callback: () => { },
        locale_data: {
            sentry: translations,
        },
    });
    return i18n;
}
exports.setLocale = setLocale;
/**
 * Helper to return the i18n client, and initialize for the default locale (English)
 * if it has otherwise not been initialized.
 */
function getClient() {
    if (!i18n) {
        // If this happens, it could mean that an import was added/changed where
        // locale initialization does not happen soon enough.
        const warning = new Error('Locale not set, defaulting to English');
        console.error(warning); // eslint-disable-line no-console
        Sentry.captureException(warning);
        return setLocale(exports.DEFAULT_LOCALE_DATA);
    }
    return i18n;
}
/**
 * printf style string formatting which render as react nodes.
 */
function formatForReact(formatString, args) {
    const nodes = [];
    let cursor = 0;
    // always re-parse, do not cache, because we change the match
    sprintf_js_1.sprintf.parse(formatString).forEach((match, idx) => {
        if ((0, isString_1.default)(match)) {
            nodes.push(match);
            return;
        }
        let arg = null;
        if (match[2]) {
            arg = args[0][match[2][0]];
        }
        else if (match[1]) {
            arg = args[parseInt(match[1], 10) - 1];
        }
        else {
            arg = args[cursor++];
        }
        // this points to a react element!
        if (React.isValidElement(arg)) {
            nodes.push(React.cloneElement(arg, { key: idx }));
        }
        else {
            // not a react element, fuck around with it so that sprintf.format
            // can format it for us.  We make sure match[2] is null so that we
            // do not go down the object path, and we set match[1] to the first
            // index and then pass an array with two items in.
            match[2] = null;
            match[1] = 1;
            nodes.push(<span key={idx++}>{sprintf_js_1.sprintf.format([match], [null, arg])}</span>);
        }
    });
    return nodes;
}
/**
 * Determine if any arguments include React elements.
 */
function argsInvolveReact(args) {
    if (args.some(React.isValidElement)) {
        return true;
    }
    if (args.length !== 1 || !(0, isObject_1.default)(args[0])) {
        return false;
    }
    const componentMap = args[0];
    return Object.keys(componentMap).some(key => React.isValidElement(componentMap[key]));
}
/**
 * Parses a template string into groups.
 *
 * The top level group will be keyed as `root`. All other group names will have
 * been extracted from the template string.
 */
function parseComponentTemplate(template) {
    const parsed = {};
    function process(startPos, group, inGroup) {
        const regex = /\[(.*?)(:|\])|\]/g;
        const buf = [];
        let satisfied = false;
        let match;
        let pos = (regex.lastIndex = startPos);
        // eslint-disable-next-line no-cond-assign
        while ((match = regex.exec(template)) !== null) {
            const substr = template.substr(pos, match.index - pos);
            if (substr !== '') {
                buf.push(substr);
            }
            const [fullMatch, groupName, closeBraceOrValueSeparator] = match;
            if (fullMatch === ']') {
                if (inGroup) {
                    satisfied = true;
                    break;
                }
                else {
                    pos = regex.lastIndex;
                    continue;
                }
            }
            if (closeBraceOrValueSeparator === ']') {
                pos = regex.lastIndex;
            }
            else {
                pos = regex.lastIndex = process(regex.lastIndex, groupName, true);
            }
            buf.push({ group: groupName });
        }
        let endPos = regex.lastIndex;
        if (!satisfied) {
            const rest = template.substr(pos);
            if (rest) {
                buf.push(rest);
            }
            endPos = template.length;
        }
        parsed[group] = buf;
        return endPos;
    }
    process(0, 'root', false);
    return parsed;
}
exports.parseComponentTemplate = parseComponentTemplate;
/**
 * Renders a parsed template into a React tree given a ComponentMap to use for
 * the parsed groups.
 */
function renderTemplate(template, components) {
    let idx = 0;
    function renderGroup(groupKey) {
        var _a;
        const children = [];
        const group = template[groupKey] || [];
        for (const item of group) {
            if ((0, isString_1.default)(item)) {
                children.push(<span key={idx++}>{item}</span>);
            }
            else {
                children.push(renderGroup(item.group));
            }
        }
        // In case we cannot find our component, we call back to an empty
        // span so that stuff shows up at least.
        let reference = (_a = components[groupKey]) !== null && _a !== void 0 ? _a : <span key={idx++}/>;
        if (!React.isValidElement(reference)) {
            reference = <span key={idx++}>{reference}</span>;
        }
        const element = reference;
        return children.length === 0
            ? React.cloneElement(element, { key: idx++ })
            : React.cloneElement(element, { key: idx++ }, children);
    }
    return <React.Fragment>{renderGroup('root')}</React.Fragment>;
}
exports.renderTemplate = renderTemplate;
/**
 * mark is used to debug translations by visually marking translated strings.
 *
 * NOTE: This is a no-op and will return the node if LOCALE_DEBUG is not
 * currently enabled. See setLocaleDebug and toggleLocaleDebug.
 */
function mark(node) {
    if (!LOCALE_DEBUG) {
        return node;
    }
    // TODO(epurkhiser): Explain why we manually create a react node and assign
    // the toString function. This could likely also use better typing, but will
    // require some understanding of reacts internal types.
    const proxy = {
        $$typeof: Symbol.for('react.element'),
        type: 'span',
        key: null,
        ref: null,
        props: {
            style: markerStyles,
            children: (0, isArray_1.default)(node) ? node : [node],
        },
        _owner: null,
        _store: {},
    };
    proxy.toString = () => '✅' + node + '✅';
    return proxy;
}
/**
 * sprintf style string formatting. Does not handle translations.
 *
 * See the sprintf-js library [0] for specifics on the argument
 * parameterization format.
 *
 * [0]: https://github.com/alexei/sprintf.js
 */
function format(formatString, args) {
    if (argsInvolveReact(args)) {
        return formatForReact(formatString, args);
    }
    return (0, sprintf_js_1.sprintf)(formatString, ...args);
}
exports.format = format;
/**
 * Translates a string to the current locale.
 *
 * See the sprintf-js library [0] for specifics on the argument
 * parameterization format.
 *
 * [0]: https://github.com/alexei/sprintf.js
 */
function gettext(string, ...args) {
    const val = getClient().gettext(string);
    if (args.length === 0) {
        return mark(val);
    }
    // XXX(ts): It IS possible to use gettext in such a way that it will return a
    // React.ReactNodeArray, however we currently rarely (if at all) use it in
    // this way, and usually just expect strings back.
    return mark(format(val, args));
}
exports.gettext = gettext;
exports.t = gettext;
/**
 * Translates a singular and plural string to the current locale. Supports
 * argument parameterization, and will use the first argument as the counter to
 * determine which message to use.
 *
 * See the sprintf-js library [0] for specifics on the argument
 * parameterization format.
 *
 * [0]: https://github.com/alexei/sprintf.js
 */
function ngettext(singular, plural, ...args) {
    let countArg = 0;
    if (args.length > 0) {
        countArg = Math.abs(args[0]) || 0;
        // `toLocaleString` will render `999` as `"999"` but `9999` as `"9,999"`. This means that any call with `tn` or `ngettext` cannot use `%d` in the codebase but has to use `%s`.
        // This means a string is always being passed in as an argument, but `sprintf-js` implicitly coerces strings that can be parsed as integers into an integer.
        // This would break under any locale that used different formatting and other undesirable behaviors.
        if ((singular + plural).includes('%d')) {
            // eslint-disable-next-line no-console
            console.error(new Error('You should not use %d within tn(), use %s instead'));
        }
        else {
            args = [countArg.toLocaleString(), ...args.slice(1)];
        }
    }
    // XXX(ts): See XXX in gettext.
    return mark(format(getClient().ngettext(singular, plural, countArg), args));
}
exports.ngettext = ngettext;
exports.tn = ngettext;
/**
 * special form of gettext where you can render nested react components in
 * template strings.
 *
 * ```jsx
 * gettextComponentTemplate('Welcome. Click [link:here]', {
 *   root: <p/>,
 *   link: <a href="#" />,
 * });
 * ```
 *
 * The root string is always called "root", the rest is prefixed with the name
 * in the brackets
 *
 * You may recursively nest additional groups within the grouped string values.
 */
function gettextComponentTemplate(template, components) {
    const tmpl = parseComponentTemplate(getClient().gettext(template));
    return mark(renderTemplate(tmpl, components));
}
exports.gettextComponentTemplate = gettextComponentTemplate;
exports.tct = gettextComponentTemplate;
//# sourceMappingURL=locale.jsx.map