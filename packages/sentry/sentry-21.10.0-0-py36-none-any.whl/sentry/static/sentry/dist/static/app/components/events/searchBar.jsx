Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const assign_1 = (0, tslib_1.__importDefault)(require("lodash/assign"));
const flatten_1 = (0, tslib_1.__importDefault)(require("lodash/flatten"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const memoize_1 = (0, tslib_1.__importDefault)(require("lodash/memoize"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const tags_1 = require("app/actionCreators/tags");
const smartSearchBar_1 = (0, tslib_1.__importDefault)(require("app/components/smartSearchBar"));
const constants_1 = require("app/constants");
const types_1 = require("app/types");
const utils_1 = require("app/utils");
const fields_1 = require("app/utils/discover/fields");
const measurements_1 = (0, tslib_1.__importDefault)(require("app/utils/measurements/measurements"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withTags_1 = (0, tslib_1.__importDefault)(require("app/utils/withTags"));
const SEARCH_SPECIAL_CHARS_REGEXP = new RegExp(`^${constants_1.NEGATION_OPERATOR}|\\${constants_1.SEARCH_WILDCARD}`, 'g');
class SearchBar extends React.PureComponent {
    constructor() {
        super(...arguments);
        /**
         * Returns array of tag values that substring match `query`; invokes `callback`
         * with data when ready
         */
        this.getEventFieldValues = (0, memoize_1.default)((tag, query, endpointParams) => {
            var _a;
            const { api, organization, projectIds } = this.props;
            const projectIdStrings = (_a = projectIds) === null || _a === void 0 ? void 0 : _a.map(String);
            if ((0, fields_1.isAggregateField)(tag.key) || (0, fields_1.isMeasurement)(tag.key)) {
                // We can't really auto suggest values for aggregate fields
                // or measurements, so we simply don't
                return Promise.resolve([]);
            }
            return (0, tags_1.fetchTagValues)(api, organization.slug, tag.key, query, projectIdStrings, endpointParams, 
            // allows searching for tags on transactions as well
            true).then(results => (0, flatten_1.default)(results.filter(({ name }) => (0, utils_1.defined)(name)).map(({ name }) => name)), () => {
                throw new Error('Unable to fetch event field values');
            });
        }, ({ key }, query) => `${key}-${query}`);
        /**
         * Prepare query string (e.g. strip special characters like negation operator)
         */
        this.prepareQuery = query => query.replace(SEARCH_SPECIAL_CHARS_REGEXP, '');
    }
    componentDidMount() {
        var _a, _b;
        // Clear memoized data on mount to make tests more consistent.
        (_b = (_a = this.getEventFieldValues.cache).clear) === null || _b === void 0 ? void 0 : _b.call(_a);
    }
    componentDidUpdate(prevProps) {
        var _a, _b;
        if (!(0, isEqual_1.default)(this.props.projectIds, prevProps.projectIds)) {
            // Clear memoized data when projects change.
            (_b = (_a = this.getEventFieldValues.cache).clear) === null || _b === void 0 ? void 0 : _b.call(_a);
        }
    }
    getTagList(measurements) {
        const { fields, organization, tags, omitTags } = this.props;
        const functionTags = fields
            ? Object.fromEntries(fields
                .filter(item => !Object.keys(fields_1.FIELD_TAGS).includes(item.field) && !(0, fields_1.isEquation)(item.field))
                .map(item => [item.field, { key: item.field, name: item.field }]))
            : {};
        const fieldTags = organization.features.includes('performance-view')
            ? Object.assign({}, measurements, fields_1.FIELD_TAGS, functionTags)
            : (0, omit_1.default)(fields_1.FIELD_TAGS, fields_1.TRACING_FIELDS);
        const semverTags = organization.features.includes('semver')
            ? Object.assign({}, fields_1.SEMVER_TAGS, fieldTags)
            : fieldTags;
        const combined = (0, assign_1.default)({}, tags, semverTags);
        combined.has = {
            key: 'has',
            name: 'Has property',
            values: Object.keys(combined),
            predefined: true,
        };
        return (0, omit_1.default)(combined, omitTags !== null && omitTags !== void 0 ? omitTags : []);
    }
    render() {
        const { organization } = this.props;
        return (<measurements_1.default organization={organization}>
        {({ measurements }) => {
                const tags = this.getTagList(measurements);
                return (<react_1.ClassNames>
              {({ css }) => (<smartSearchBar_1.default hasRecentSearches savedSearchType={types_1.SavedSearchType.EVENT} onGetTagValues={this.getEventFieldValues} supportedTags={tags} prepareQuery={this.prepareQuery} excludeEnvironment dropdownClassName={css `
                    max-height: 300px;
                    overflow-y: auto;
                  `} {...this.props}/>)}
            </react_1.ClassNames>);
            }}
      </measurements_1.default>);
    }
}
exports.default = (0, withApi_1.default)((0, withTags_1.default)(SearchBar));
//# sourceMappingURL=searchBar.jsx.map