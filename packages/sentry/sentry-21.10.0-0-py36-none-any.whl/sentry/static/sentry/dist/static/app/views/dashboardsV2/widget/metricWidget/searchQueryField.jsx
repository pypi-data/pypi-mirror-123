Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const memoize_1 = (0, tslib_1.__importDefault)(require("lodash/memoize"));
const smartSearchBar_1 = (0, tslib_1.__importDefault)(require("app/components/smartSearchBar"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const SEARCH_SPECIAL_CHARS_REGEXP = new RegExp(`^${constants_1.NEGATION_OPERATOR}|\\${constants_1.SEARCH_WILDCARD}`, 'g');
function SearchQueryField({ api, orgSlug, projectSlug, tags, onSearch, onBlur }) {
    /**
     * Prepare query string (e.g. strip special characters like negation operator)
     */
    function prepareQuery(query) {
        return query.replace(SEARCH_SPECIAL_CHARS_REGEXP, '');
    }
    function fetchTagValues(tagKey) {
        return api.requestPromise(`/projects/${orgSlug}/${projectSlug}/metrics/tags/${tagKey}/`, {
            method: 'GET',
        });
    }
    function getTagValues(tag, _query) {
        return fetchTagValues(tag.key).then(tagValues => tagValues, () => {
            throw new Error('Unable to fetch tag values');
        });
    }
    const supportedTags = tags.reduce((acc, tag) => {
        acc[tag] = { key: tag, name: tag };
        return acc;
    }, {});
    return (<react_1.ClassNames>
      {({ css }) => (<smartSearchBar_1.default placeholder={(0, locale_1.t)('Search for tag')} onGetTagValues={(0, memoize_1.default)(getTagValues, ({ key }, query) => `${key}-${query}`)} supportedTags={supportedTags} prepareQuery={prepareQuery} onSearch={onSearch} onBlur={onBlur} useFormWrapper={false} excludeEnvironment dropdownClassName={css `
            max-height: 300px;
            overflow-y: auto;
          `}/>)}
    </react_1.ClassNames>);
}
exports.default = SearchQueryField;
//# sourceMappingURL=searchQueryField.jsx.map