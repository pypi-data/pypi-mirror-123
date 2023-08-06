Object.defineProperty(exports, "__esModule", { value: true });
exports.loadSearchMap = void 0;
const tslib_1 = require("tslib");
const flatMap_1 = (0, tslib_1.__importDefault)(require("lodash/flatMap"));
const flatten_1 = (0, tslib_1.__importDefault)(require("lodash/flatten"));
const formSearchActions_1 = (0, tslib_1.__importDefault)(require("app/actions/formSearchActions"));
/**
 * Creates a list of objects to be injected by a search source
 *
 * @param route The route a form field belongs on
 * @param formGroups An array of `FormGroup: {title: String, fields: [Field]}`
 * @param fields An object whose key is field name and value is a `Field`
 */
const createSearchMap = (_a) => {
    var { route, formGroups, fields } = _a, other = (0, tslib_1.__rest)(_a, ["route", "formGroups", "fields"]);
    // There are currently two ways to define forms (TODO(billy): Turn this into one):
    // If `formGroups` is defined, then return a flattened list of fields in all formGroups
    // Otherwise `fields` is a map of fieldName -> fieldObject -- create a list of fields
    const listOfFields = formGroups
        ? (0, flatMap_1.default)(formGroups, formGroup => formGroup.fields)
        : Object.keys(fields).map(fieldName => fields[fieldName]);
    return listOfFields.map(field => (Object.assign(Object.assign({}, other), { route, title: typeof field !== 'function' ? field.label : undefined, description: typeof field !== 'function' ? field.help : undefined, field })));
};
function loadSearchMap() {
    // Load all form configuration files via webpack that export a named `route`
    // as well as either `fields` or `formGroups`
    // @ts-ignore This fails on cloud builder, but not in CI...
    const context = require.context('../data/forms', true, /\.[tj]sx?$/);
    // Get a list of all form fields defined in `../data/forms`
    const allFormFields = (0, flatten_1.default)(context
        .keys()
        .map(key => {
        const mod = context(key);
        // Since we're dynamically importing an entire directly, there could be malformed modules defined?
        if (!mod) {
            return null;
        }
        // Only look for module that have `route` exported
        if (!mod.route) {
            return null;
        }
        return createSearchMap({
            // `formGroups` can be a default export or a named export :<
            formGroups: mod.default || mod.formGroups,
            fields: mod.fields,
            route: mod.route,
        });
    })
        .filter(i => !!i));
    formSearchActions_1.default.loadSearchMap(allFormFields);
}
exports.loadSearchMap = loadSearchMap;
//# sourceMappingURL=formSearch.jsx.map