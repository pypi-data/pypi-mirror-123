Object.defineProperty(exports, "__esModule", { value: true });
exports.SmartSearchBar = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_autosize_textarea_1 = (0, tslib_1.__importDefault)(require("react-autosize-textarea"));
const react_router_1 = require("react-router");
const is_prop_valid_1 = (0, tslib_1.__importDefault)(require("@emotion/is-prop-valid"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const indicator_1 = require("app/actionCreators/indicator");
const savedSearches_1 = require("app/actionCreators/savedSearches");
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const dropdownLink_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownLink"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const parser_1 = require("app/components/searchSyntax/parser");
const renderer_1 = (0, tslib_1.__importDefault)(require("app/components/searchSyntax/renderer"));
const utils_1 = require("app/components/searchSyntax/utils");
const constants_1 = require("app/constants");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const memberListStore_1 = (0, tslib_1.__importDefault)(require("app/stores/memberListStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
const utils_2 = require("app/utils");
const analytics_1 = require("app/utils/analytics");
const callIfFunction_1 = require("app/utils/callIfFunction");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const actions_1 = require("./actions");
const searchDropdown_1 = (0, tslib_1.__importDefault)(require("./searchDropdown"));
const types_2 = require("./types");
const utils_3 = require("./utils");
const DROPDOWN_BLUR_DURATION = 200;
/**
 * The max width in pixels of the search bar at which the buttons will
 * have overflowed into the dropdown.
 */
const ACTION_OVERFLOW_WIDTH = 400;
/**
 * Actions are moved to the overflow dropdown after each pixel step is reached.
 */
const ACTION_OVERFLOW_STEPS = 75;
const makeQueryState = (query) => ({
    query,
    parsedQuery: (0, parser_1.parseSearch)(query),
});
const generateOpAutocompleteGroup = (validOps, tagName) => {
    const operatorMap = (0, utils_3.generateOperatorEntryMap)(tagName);
    const operatorItems = validOps.map(op => operatorMap[op]);
    return {
        searchItems: operatorItems,
        recentSearchItems: undefined,
        tagName: '',
        type: types_2.ItemType.TAG_OPERATOR,
    };
};
class SmartSearchBar extends React.Component {
    constructor() {
        var _a, _b;
        super(...arguments);
        this.state = {
            query: this.initialQuery,
            parsedQuery: (0, parser_1.parseSearch)(this.initialQuery),
            searchTerm: '',
            searchGroups: [],
            flatSearchItems: [],
            activeSearchItem: -1,
            tags: {},
            inputHasFocus: false,
            loading: false,
            numActionsVisible: (_b = (_a = this.props.actionBarItems) === null || _a === void 0 ? void 0 : _a.length) !== null && _b !== void 0 ? _b : 0,
        };
        /**
         * Ref to the search element itself
         */
        this.searchInput = React.createRef();
        /**
         * Ref to the search container
         */
        this.containerRef = React.createRef();
        /**
         * Used to determine when actions should be moved to the action overflow menu
         */
        this.inputResizeObserver = null;
        /**
         * Updates the numActionsVisible count as the search bar is resized
         */
        this.updateActionsVisible = (entries) => {
            var _a, _b;
            if (entries.length === 0) {
                return;
            }
            const entry = entries[0];
            const { width } = entry.contentRect;
            const actionCount = (_b = (_a = this.props.actionBarItems) === null || _a === void 0 ? void 0 : _a.length) !== null && _b !== void 0 ? _b : 0;
            const numActionsVisible = Math.min(actionCount, Math.floor(Math.max(0, width - ACTION_OVERFLOW_WIDTH) / ACTION_OVERFLOW_STEPS));
            if (this.state.numActionsVisible === numActionsVisible) {
                return;
            }
            this.setState({ numActionsVisible });
        };
        this.onSubmit = (evt) => {
            evt.preventDefault();
            this.doSearch();
        };
        this.clearSearch = () => this.setState(makeQueryState(''), () => (0, callIfFunction_1.callIfFunction)(this.props.onSearch, this.state.query));
        this.onQueryFocus = () => this.setState({ inputHasFocus: true });
        this.onQueryBlur = (e) => {
            // wait before closing dropdown in case blur was a result of clicking a
            // menu option
            const value = e.target.value;
            const blurHandler = () => {
                this.blurTimeout = undefined;
                this.setState({ inputHasFocus: false });
                (0, callIfFunction_1.callIfFunction)(this.props.onBlur, value);
            };
            this.blurTimeout = window.setTimeout(blurHandler, DROPDOWN_BLUR_DURATION);
        };
        this.onQueryChange = (evt) => {
            const query = evt.target.value.replace('\n', '');
            this.setState(makeQueryState(query), this.updateAutoCompleteItems);
            (0, callIfFunction_1.callIfFunction)(this.props.onChange, evt.target.value, evt);
        };
        this.onInputClick = () => this.updateAutoCompleteItems();
        /**
         * Handle keyboard navigation
         */
        this.onKeyDown = (evt) => {
            var _a, _b, _c;
            const { onKeyDown } = this.props;
            const { key } = evt;
            (0, callIfFunction_1.callIfFunction)(onKeyDown, evt);
            const hasSearchGroups = this.state.searchGroups.length > 0;
            const isSelectingDropdownItems = this.state.activeSearchItem !== -1;
            if ((key === 'ArrowDown' || key === 'ArrowUp') && hasSearchGroups) {
                evt.preventDefault();
                const { flatSearchItems, activeSearchItem } = this.state;
                const searchGroups = [...this.state.searchGroups];
                const [groupIndex, childrenIndex] = isSelectingDropdownItems
                    ? (0, utils_3.filterSearchGroupsByIndex)(searchGroups, activeSearchItem)
                    : [];
                // Remove the previous 'active' property
                if (typeof groupIndex !== 'undefined') {
                    if (childrenIndex !== undefined &&
                        ((_b = (_a = searchGroups[groupIndex]) === null || _a === void 0 ? void 0 : _a.children) === null || _b === void 0 ? void 0 : _b[childrenIndex])) {
                        delete searchGroups[groupIndex].children[childrenIndex].active;
                    }
                }
                const currIndex = isSelectingDropdownItems ? activeSearchItem : 0;
                const totalItems = flatSearchItems.length;
                // Move the selected index up/down
                const nextActiveSearchItem = key === 'ArrowUp'
                    ? (currIndex - 1 + totalItems) % totalItems
                    : isSelectingDropdownItems
                        ? (currIndex + 1) % totalItems
                        : 0;
                const [nextGroupIndex, nextChildrenIndex] = (0, utils_3.filterSearchGroupsByIndex)(searchGroups, nextActiveSearchItem);
                // Make sure search items exist (e.g. both groups could be empty) and
                // attach the 'active' property to the item
                if (nextGroupIndex !== undefined &&
                    nextChildrenIndex !== undefined &&
                    ((_c = searchGroups[nextGroupIndex]) === null || _c === void 0 ? void 0 : _c.children)) {
                    searchGroups[nextGroupIndex].children[nextChildrenIndex] = Object.assign(Object.assign({}, searchGroups[nextGroupIndex].children[nextChildrenIndex]), { active: true });
                }
                this.setState({ searchGroups, activeSearchItem: nextActiveSearchItem });
            }
            if ((key === 'Tab' || key === 'Enter') &&
                isSelectingDropdownItems &&
                hasSearchGroups) {
                evt.preventDefault();
                const { activeSearchItem, searchGroups } = this.state;
                const [groupIndex, childrenIndex] = (0, utils_3.filterSearchGroupsByIndex)(searchGroups, activeSearchItem);
                const item = groupIndex !== undefined &&
                    childrenIndex !== undefined &&
                    searchGroups[groupIndex].children[childrenIndex];
                if (item) {
                    this.onAutoComplete(item.value, item);
                }
                return;
            }
            if (key === 'Enter' && !isSelectingDropdownItems) {
                this.doSearch();
                return;
            }
            const cursorToken = this.cursorToken;
            if (key === '[' &&
                (cursorToken === null || cursorToken === void 0 ? void 0 : cursorToken.type) === parser_1.Token.Filter &&
                cursorToken.value.text.length === 0 &&
                (0, utils_1.isWithinToken)(cursorToken.value, this.cursorPosition)) {
                const { query } = this.state;
                evt.preventDefault();
                let clauseStart = null;
                let clauseEnd = null;
                // the new text that will exist between clauseStart and clauseEnd
                const replaceToken = '[]';
                const location = cursorToken.value.location;
                const keyLocation = cursorToken.key.location;
                // Include everything after the ':'
                clauseStart = keyLocation.end.offset + 1;
                clauseEnd = location.end.offset + 1;
                const beforeClause = query.substring(0, clauseStart);
                let endClause = query.substring(clauseEnd);
                // Add space before next clause if it exists
                if (endClause) {
                    endClause = ` ${endClause}`;
                }
                const newQuery = `${beforeClause}${replaceToken}${endClause}`;
                // Place cursor between inserted brackets
                this.updateQuery(newQuery, beforeClause.length + replaceToken.length - 1);
                return;
            }
        };
        this.onKeyUp = (evt) => {
            if (evt.key === 'ArrowLeft' || evt.key === 'ArrowRight') {
                this.updateAutoCompleteItems();
            }
            // Other keys are managed at onKeyDown function
            if (evt.key !== 'Escape') {
                return;
            }
            evt.preventDefault();
            const isSelectingDropdownItems = this.state.activeSearchItem > -1;
            if (!isSelectingDropdownItems) {
                this.blur();
                return;
            }
            const { searchGroups, activeSearchItem } = this.state;
            const [groupIndex, childrenIndex] = isSelectingDropdownItems
                ? (0, utils_3.filterSearchGroupsByIndex)(searchGroups, activeSearchItem)
                : [];
            if (groupIndex !== undefined && childrenIndex !== undefined) {
                delete searchGroups[groupIndex].children[childrenIndex].active;
            }
            this.setState({
                activeSearchItem: -1,
                searchGroups: [...this.state.searchGroups],
            });
        };
        /**
         * Returns array of tag values that substring match `query`; invokes `callback`
         * with data when ready
         */
        this.getTagValues = (0, debounce_1.default)((tag, query) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            // Strip double quotes if there are any
            query = query.replace(/"/g, '').trim();
            if (!this.props.onGetTagValues) {
                return [];
            }
            if (this.state.noValueQuery !== undefined &&
                query.startsWith(this.state.noValueQuery)) {
                return [];
            }
            const { location } = this.props;
            const endpointParams = (0, getParams_1.getParams)(location.query);
            this.setState({ loading: true });
            let values = [];
            try {
                values = yield this.props.onGetTagValues(tag, query, endpointParams);
                this.setState({ loading: false });
            }
            catch (err) {
                this.setState({ loading: false });
                Sentry.captureException(err);
                return [];
            }
            if (tag.key === 'release:' && !values.includes('latest')) {
                values.unshift('latest');
            }
            const noValueQuery = values.length === 0 && query.length > 0 ? query : undefined;
            this.setState({ noValueQuery });
            return values.map(value => {
                // Wrap in quotes if there is a space
                const escapedValue = value.includes(' ') || value.includes('"')
                    ? `"${value.replace(/"/g, '\\"')}"`
                    : value;
                return { value: escapedValue, desc: escapedValue, type: types_2.ItemType.TAG_VALUE };
            });
        }), constants_1.DEFAULT_DEBOUNCE_DURATION, { leading: true });
        /**
         * Returns array of tag values that substring match `query`; invokes `callback`
         * with results
         */
        this.getPredefinedTagValues = (tag, query) => {
            var _a;
            return ((_a = tag.values) !== null && _a !== void 0 ? _a : [])
                .filter(value => value.indexOf(query) > -1)
                .map((value, i) => ({
                value,
                desc: value,
                type: types_2.ItemType.TAG_VALUE,
                ignoreMaxSearchItems: tag.maxSuggestedValues ? i < tag.maxSuggestedValues : false,
            }));
        };
        /**
         * Get recent searches
         */
        this.getRecentSearches = (0, debounce_1.default)(() => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { savedSearchType, hasRecentSearches, onGetRecentSearches } = this.props;
            // `savedSearchType` can be 0
            if (!(0, utils_2.defined)(savedSearchType) || !hasRecentSearches) {
                return [];
            }
            const fetchFn = onGetRecentSearches || this.fetchRecentSearches;
            return yield fetchFn(this.state.query);
        }), constants_1.DEFAULT_DEBOUNCE_DURATION, { leading: true });
        this.fetchRecentSearches = (fullQuery) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization, savedSearchType } = this.props;
            if (savedSearchType === undefined) {
                return [];
            }
            try {
                const recentSearches = yield (0, savedSearches_1.fetchRecentSearches)(api, organization.slug, savedSearchType, fullQuery);
                // If `recentSearches` is undefined or not an array, the function will
                // return an array anyway
                return recentSearches.map(searches => ({
                    desc: searches.query,
                    value: searches.query,
                    type: types_2.ItemType.RECENT_SEARCH,
                }));
            }
            catch (e) {
                Sentry.captureException(e);
            }
            return [];
        });
        this.getReleases = (0, debounce_1.default)((tag, query) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const releasePromise = this.fetchReleases(query);
            const tags = this.getPredefinedTagValues(tag, query);
            const tagValues = tags.map(v => (Object.assign(Object.assign({}, v), { type: types_2.ItemType.FIRST_RELEASE })));
            const releases = yield releasePromise;
            const releaseValues = releases.map((r) => ({
                value: r.shortVersion,
                desc: r.shortVersion,
                type: types_2.ItemType.FIRST_RELEASE,
            }));
            return [...tagValues, ...releaseValues];
        }), constants_1.DEFAULT_DEBOUNCE_DURATION, { leading: true });
        /**
         * Fetches latest releases from a organization/project. Returns an empty array
         * if an error is encountered.
         */
        this.fetchReleases = (releaseVersion) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, location, organization } = this.props;
            const project = location && location.query ? location.query.projectId : undefined;
            const url = `/organizations/${organization.slug}/releases/`;
            const fetchQuery = {
                per_page: constants_1.MAX_AUTOCOMPLETE_RELEASES,
            };
            if (releaseVersion) {
                fetchQuery.query = releaseVersion;
            }
            if (project) {
                fetchQuery.project = project;
            }
            try {
                return yield api.requestPromise(url, {
                    method: 'GET',
                    query: fetchQuery,
                });
            }
            catch (e) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to fetch releases'));
                Sentry.captureException(e);
            }
            return [];
        });
        this.generateValueAutocompleteGroup = (tagName, query) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _c;
            const { prepareQuery, excludeEnvironment } = this.props;
            const supportedTags = (_c = this.props.supportedTags) !== null && _c !== void 0 ? _c : {};
            const preparedQuery = typeof prepareQuery === 'function' ? prepareQuery(query) : query;
            // filter existing items immediately, until API can return
            // with actual tag value results
            const filteredSearchGroups = !preparedQuery
                ? this.state.searchGroups
                : this.state.searchGroups.filter(item => item.value && item.value.indexOf(preparedQuery) !== -1);
            this.setState({
                searchTerm: query,
                searchGroups: filteredSearchGroups,
            });
            const tag = supportedTags[tagName];
            if (!tag) {
                return {
                    searchItems: [],
                    recentSearchItems: [],
                    tagName,
                    type: types_2.ItemType.INVALID_TAG,
                };
            }
            // Ignore the environment tag if the feature is active and
            // excludeEnvironment = true
            if (excludeEnvironment && tagName === 'environment') {
                return null;
            }
            const fetchTagValuesFn = tag.key === 'firstRelease'
                ? this.getReleases
                : tag.predefined
                    ? this.getPredefinedTagValues
                    : this.getTagValues;
            const [tagValues, recentSearches] = yield Promise.all([
                fetchTagValuesFn(tag, preparedQuery),
                this.getRecentSearches(),
            ]);
            return {
                searchItems: tagValues !== null && tagValues !== void 0 ? tagValues : [],
                recentSearchItems: recentSearches !== null && recentSearches !== void 0 ? recentSearches : [],
                tagName: tag.key,
                type: types_2.ItemType.TAG_VALUE,
            };
        });
        this.showDefaultSearches = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { query } = this.state;
            const [defaultSearchItems, defaultRecentItems] = this.props.defaultSearchItems;
            if (!defaultSearchItems.length) {
                // Update searchTerm, otherwise <SearchDropdown> will have wrong state
                // (e.g. if you delete a query, the last letter will be highlighted if `searchTerm`
                // does not get updated)
                this.setState({ searchTerm: query });
                const tagKeys = this.getTagKeys('');
                const recentSearches = yield this.getRecentSearches();
                this.updateAutoCompleteState(tagKeys, recentSearches !== null && recentSearches !== void 0 ? recentSearches : [], '', types_2.ItemType.TAG_KEY);
                return;
            }
            // cursor on whitespace show default "help" search terms
            this.setState({ searchTerm: '' });
            this.updateAutoCompleteState(defaultSearchItems, defaultRecentItems, '', types_2.ItemType.DEFAULT);
            return;
        });
        this.updateAutoCompleteFromAst = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _d, _e;
            const cursor = this.cursorPosition;
            const cursorToken = this.cursorToken;
            if (!cursorToken) {
                this.showDefaultSearches();
                return;
            }
            if (cursorToken.type === parser_1.Token.Filter) {
                const tagName = (0, utils_1.getKeyName)(cursorToken.key, { aggregateWithArgs: true });
                // check if we are on the tag, value, or operator
                if ((0, utils_1.isWithinToken)(cursorToken.value, cursor)) {
                    const node = cursorToken.value;
                    const cursorValue = this.cursorValue;
                    let searchText = (_d = cursorValue === null || cursorValue === void 0 ? void 0 : cursorValue.text) !== null && _d !== void 0 ? _d : node.text;
                    if (searchText === '[]' || cursorValue === null) {
                        searchText = '';
                    }
                    const valueGroup = yield this.generateValueAutocompleteGroup(tagName, searchText);
                    const autocompleteGroups = valueGroup ? [valueGroup] : [];
                    // show operator group if at beginning of value
                    if (cursor === node.location.start.offset) {
                        const opGroup = generateOpAutocompleteGroup((0, utils_3.getValidOps)(cursorToken), tagName);
                        autocompleteGroups.unshift(opGroup);
                    }
                    this.updateAutoCompleteStateMultiHeader(autocompleteGroups);
                    return;
                }
                if ((0, utils_1.isWithinToken)(cursorToken.key, cursor)) {
                    const node = cursorToken.key;
                    const autocompleteGroups = [yield this.generateTagAutocompleteGroup(tagName)];
                    // show operator group if at end of key
                    if (cursor === node.location.end.offset) {
                        const opGroup = generateOpAutocompleteGroup((0, utils_3.getValidOps)(cursorToken), tagName);
                        autocompleteGroups.unshift(opGroup);
                    }
                    this.setState({ searchTerm: tagName });
                    this.updateAutoCompleteStateMultiHeader(autocompleteGroups);
                    return;
                }
                // show operator autocomplete group
                const opGroup = generateOpAutocompleteGroup((0, utils_3.getValidOps)(cursorToken), tagName);
                this.updateAutoCompleteStateMultiHeader([opGroup]);
                return;
            }
            if (cursorToken.type === parser_1.Token.FreeText) {
                const lastToken = (_e = cursorToken.text.trim().split(' ').pop()) !== null && _e !== void 0 ? _e : '';
                const keyText = lastToken.replace(new RegExp(`^${constants_1.NEGATION_OPERATOR}`), '');
                const autocompleteGroups = [yield this.generateTagAutocompleteGroup(keyText)];
                this.setState({ searchTerm: keyText });
                this.updateAutoCompleteStateMultiHeader(autocompleteGroups);
                return;
            }
        });
        this.updateAutoCompleteItems = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (this.blurTimeout) {
                clearTimeout(this.blurTimeout);
                this.blurTimeout = undefined;
            }
            this.updateAutoCompleteFromAst();
        });
        /**
         * Updates autocomplete dropdown items and autocomplete index state
         *
         * @param groups Groups that will be used to populate the autocomplete dropdown
         */
        this.updateAutoCompleteStateMultiHeader = (groups) => {
            const { hasRecentSearches, maxSearchItems, maxQueryLength } = this.props;
            const { query } = this.state;
            const queryCharsLeft = maxQueryLength && query ? maxQueryLength - query.length : undefined;
            const searchGroups = groups
                .map(({ searchItems, recentSearchItems, tagName, type }) => (0, utils_3.createSearchGroups)(searchItems, hasRecentSearches ? recentSearchItems : undefined, tagName, type, maxSearchItems, queryCharsLeft))
                .reduce((acc, item) => ({
                searchGroups: [...acc.searchGroups, ...item.searchGroups],
                flatSearchItems: [...acc.flatSearchItems, ...item.flatSearchItems],
                activeSearchItem: -1,
            }), {
                searchGroups: [],
                flatSearchItems: [],
                activeSearchItem: -1,
            });
            this.setState(searchGroups);
        };
        this.updateQuery = (newQuery, cursorPosition) => this.setState(makeQueryState(newQuery), () => {
            var _a, _b;
            // setting a new input value will lose focus; restore it
            if (this.searchInput.current) {
                this.searchInput.current.focus();
                if (cursorPosition) {
                    this.searchInput.current.selectionStart = cursorPosition;
                    this.searchInput.current.selectionEnd = cursorPosition;
                }
            }
            // then update the autocomplete box with new items
            this.updateAutoCompleteItems();
            (_b = (_a = this.props).onChange) === null || _b === void 0 ? void 0 : _b.call(_a, newQuery, new MouseEvent('click'));
        });
        this.onAutoCompleteFromAst = (replaceText, item) => {
            var _a;
            const cursor = this.cursorPosition;
            const { query } = this.state;
            const cursorToken = this.cursorToken;
            if (!cursorToken) {
                this.updateQuery(`${query}${replaceText}`);
                return;
            }
            // the start and end of what to replace
            let clauseStart = null;
            let clauseEnd = null;
            // the new text that will exist between clauseStart and clauseEnd
            let replaceToken = replaceText;
            if (cursorToken.type === parser_1.Token.Filter) {
                if (item.type === types_2.ItemType.TAG_OPERATOR) {
                    (0, analytics_1.trackAnalyticsEvent)({
                        eventKey: 'search.operator_autocompleted',
                        eventName: 'Search: Operator Autocompleted',
                        organization_id: this.props.organization.id,
                        query: (0, utils_3.removeSpace)(query),
                        search_operator: replaceText,
                        search_type: this.props.savedSearchType === 0 ? 'issues' : 'events',
                    });
                    const valueLocation = cursorToken.value.location;
                    clauseStart = cursorToken.location.start.offset;
                    clauseEnd = valueLocation.start.offset;
                    if (replaceText === '!:') {
                        replaceToken = `!${cursorToken.key.text}:`;
                    }
                    else {
                        replaceToken = `${cursorToken.key.text}${replaceText}`;
                    }
                }
                else if ((0, utils_1.isWithinToken)(cursorToken.value, cursor)) {
                    const valueToken = (_a = this.cursorValue) !== null && _a !== void 0 ? _a : cursorToken.value;
                    const location = valueToken.location;
                    if (cursorToken.filter === parser_1.FilterType.TextIn) {
                        // Current value can be null when adding a 2nd value
                        //             ▼ cursor
                        // key:[value1, ]
                        const currentValueNull = this.cursorValue === null;
                        clauseStart = currentValueNull
                            ? this.cursorPosition
                            : valueToken.location.start.offset;
                        clauseEnd = currentValueNull
                            ? this.cursorPosition
                            : valueToken.location.end.offset;
                    }
                    else {
                        const keyLocation = cursorToken.key.location;
                        clauseStart = keyLocation.end.offset + 1;
                        clauseEnd = location.end.offset + 1;
                        // The user tag often contains : within its value and we need to quote it.
                        if ((0, utils_1.getKeyName)(cursorToken.key) === 'user') {
                            replaceToken = `"${replaceText.trim()}"`;
                        }
                        // handle using autocomplete with key:[]
                        if (valueToken.text === '[]') {
                            clauseStart += 1;
                            clauseEnd -= 2;
                        }
                        else {
                            replaceToken += ' ';
                        }
                    }
                }
                else if ((0, utils_1.isWithinToken)(cursorToken.key, cursor)) {
                    const location = cursorToken.key.location;
                    clauseStart = location.start.offset;
                    // If the token is a key, then trim off the end to avoid duplicate ':'
                    clauseEnd = location.end.offset + 1;
                }
            }
            if (cursorToken.type === parser_1.Token.FreeText) {
                const startPos = cursorToken.location.start.offset;
                clauseStart = cursorToken.text.startsWith(constants_1.NEGATION_OPERATOR)
                    ? startPos + 1
                    : startPos;
                clauseEnd = cursorToken.location.end.offset;
            }
            if (clauseStart !== null && clauseEnd !== null) {
                const beforeClause = query.substring(0, clauseStart);
                const endClause = query.substring(clauseEnd);
                const newQuery = `${beforeClause}${replaceToken}${endClause}`;
                this.updateQuery(newQuery, beforeClause.length + replaceToken.length);
            }
        };
        this.onAutoComplete = (replaceText, item) => {
            if (item.type === types_2.ItemType.RECENT_SEARCH) {
                (0, analytics_1.trackAnalyticsEvent)({
                    eventKey: 'search.searched',
                    eventName: 'Search: Performed search',
                    organization_id: this.props.organization.id,
                    query: replaceText,
                    source: this.props.savedSearchType === 0 ? 'issues' : 'events',
                    search_source: 'recent_search',
                });
                this.setState(makeQueryState(replaceText), () => {
                    // Propagate onSearch and save to recent searches
                    this.doSearch();
                });
                return;
            }
            this.onAutoCompleteFromAst(replaceText, item);
        };
    }
    componentDidMount() {
        if (!window.ResizeObserver) {
            return;
        }
        if (this.containerRef.current === null) {
            return;
        }
        this.inputResizeObserver = new ResizeObserver(this.updateActionsVisible);
        this.inputResizeObserver.observe(this.containerRef.current);
    }
    componentDidUpdate(prevProps) {
        const { query } = this.props;
        const { query: lastQuery } = prevProps;
        if (query !== lastQuery && ((0, utils_2.defined)(query) || (0, utils_2.defined)(lastQuery))) {
            // eslint-disable-next-line react/no-did-update-set-state
            this.setState(makeQueryState((0, utils_3.addSpace)(query !== null && query !== void 0 ? query : undefined)));
        }
    }
    componentWillUnmount() {
        var _a;
        (_a = this.inputResizeObserver) === null || _a === void 0 ? void 0 : _a.disconnect();
        if (this.blurTimeout) {
            clearTimeout(this.blurTimeout);
        }
    }
    get initialQuery() {
        const { query, defaultQuery } = this.props;
        return query !== null ? (0, utils_3.addSpace)(query) : defaultQuery !== null && defaultQuery !== void 0 ? defaultQuery : '';
    }
    blur() {
        if (!this.searchInput.current) {
            return;
        }
        this.searchInput.current.blur();
    }
    doSearch() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            this.blur();
            if (!this.hasValidSearch) {
                return;
            }
            const query = (0, utils_3.removeSpace)(this.state.query);
            const { onSearch, onSavedRecentSearch, api, organization, savedSearchType, searchSource, } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'search.searched',
                eventName: 'Search: Performed search',
                organization_id: organization.id,
                query,
                search_type: savedSearchType === 0 ? 'issues' : 'events',
                search_source: searchSource,
            });
            (0, callIfFunction_1.callIfFunction)(onSearch, query);
            // Only save recent search query if we have a savedSearchType (also 0 is a valid value)
            // Do not save empty string queries (i.e. if they clear search)
            if (typeof savedSearchType === 'undefined' || !query) {
                return;
            }
            try {
                yield (0, savedSearches_1.saveRecentSearch)(api, organization.slug, savedSearchType, query);
                if (onSavedRecentSearch) {
                    onSavedRecentSearch(query);
                }
            }
            catch (err) {
                // Silently capture errors if it fails to save
                Sentry.captureException(err);
            }
        });
    }
    /**
     * Check if any filters are invalid within the search query
     */
    get hasValidSearch() {
        const { parsedQuery } = this.state;
        // If we fail to parse be optimistic that it's valid
        if (parsedQuery === null) {
            return true;
        }
        return (0, utils_1.treeResultLocator)({
            tree: parsedQuery,
            noResultValue: true,
            visitorTest: ({ token, returnResult, skipToken }) => token.type !== parser_1.Token.Filter
                ? null
                : token.invalid
                    ? returnResult(false)
                    : skipToken,
        });
    }
    /**
     * Get the active filter or free text actively focused.
     */
    get cursorToken() {
        const matchedTokens = [parser_1.Token.Filter, parser_1.Token.FreeText];
        return this.findTokensAtCursor(matchedTokens);
    }
    /**
     * Get the active parsed text value
     */
    get cursorValue() {
        const matchedTokens = [parser_1.Token.ValueText];
        return this.findTokensAtCursor(matchedTokens);
    }
    /**
     * Get the current cursor position within the input
     */
    get cursorPosition() {
        var _a;
        if (!this.searchInput.current) {
            return -1;
        }
        // No cursor position when the input loses focus. This is important for
        // updating the search highlighters active state
        if (!this.state.inputHasFocus) {
            return -1;
        }
        return (_a = this.searchInput.current.selectionStart) !== null && _a !== void 0 ? _a : -1;
    }
    /**
     * Finds tokens that exist at the current cursor position
     * @param matchedTokens acceptable list of tokens
     */
    findTokensAtCursor(matchedTokens) {
        const { parsedQuery } = this.state;
        if (parsedQuery === null) {
            return null;
        }
        const cursor = this.cursorPosition;
        return (0, utils_1.treeResultLocator)({
            tree: parsedQuery,
            noResultValue: null,
            visitorTest: ({ token, returnResult, skipToken }) => !matchedTokens.includes(token.type)
                ? null
                : (0, utils_1.isWithinToken)(token, cursor)
                    ? returnResult(token)
                    : skipToken,
        });
    }
    /**
     * Returns array of possible key values that substring match `query`
     */
    getTagKeys(query) {
        var _a;
        const { prepareQuery } = this.props;
        const supportedTags = (_a = this.props.supportedTags) !== null && _a !== void 0 ? _a : {};
        // Return all if query is empty
        let tagKeys = Object.keys(supportedTags).map(key => `${key}:`);
        if (query) {
            const preparedQuery = typeof prepareQuery === 'function' ? prepareQuery(query) : query;
            tagKeys = tagKeys.filter(key => key.indexOf(preparedQuery) > -1);
        }
        // If the environment feature is active and excludeEnvironment = true
        // then remove the environment key
        if (this.props.excludeEnvironment) {
            tagKeys = tagKeys.filter(key => key !== 'environment:');
        }
        return tagKeys.map(value => ({ value, desc: value }));
    }
    generateTagAutocompleteGroup(tagName) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const tagKeys = this.getTagKeys(tagName);
            const recentSearches = yield this.getRecentSearches();
            return {
                searchItems: tagKeys,
                recentSearchItems: recentSearches !== null && recentSearches !== void 0 ? recentSearches : [],
                tagName,
                type: types_2.ItemType.TAG_KEY,
            };
        });
    }
    /**
     * Updates autocomplete dropdown items and autocomplete index state
     *
     * @param searchItems List of search item objects with keys: title, desc, value
     * @param recentSearchItems List of recent search items, same format as searchItem
     * @param tagName The current tag name in scope
     * @param type Defines the type/state of the dropdown menu items
     */
    updateAutoCompleteState(searchItems, recentSearchItems, tagName, type) {
        const { hasRecentSearches, maxSearchItems, maxQueryLength } = this.props;
        const { query } = this.state;
        const queryCharsLeft = maxQueryLength && query ? maxQueryLength - query.length : undefined;
        this.setState((0, utils_3.createSearchGroups)(searchItems, hasRecentSearches ? recentSearchItems : undefined, tagName, type, maxSearchItems, queryCharsLeft));
    }
    render() {
        const { api, className, savedSearchType, dropdownClassName, actionBarItems, organization, placeholder, disabled, useFormWrapper, inlineLabel, maxQueryLength, } = this.props;
        const { query, parsedQuery, searchGroups, searchTerm, inputHasFocus, numActionsVisible, loading, } = this.state;
        const input = (<SearchInput type="text" placeholder={placeholder} id="smart-search-input" name="query" ref={this.searchInput} autoComplete="off" value={query} onFocus={this.onQueryFocus} onBlur={this.onQueryBlur} onKeyUp={this.onKeyUp} onKeyDown={this.onKeyDown} onChange={this.onQueryChange} onClick={this.onInputClick} disabled={disabled} maxLength={maxQueryLength} spellCheck={false}/>);
        // Segment actions into visible and overflowed groups
        const actionItems = actionBarItems !== null && actionBarItems !== void 0 ? actionBarItems : [];
        const actionProps = {
            api,
            organization,
            query,
            savedSearchType,
        };
        const visibleActions = actionItems
            .slice(0, numActionsVisible)
            .map(({ key, Action }) => <Action key={key} {...actionProps}/>);
        const overflowedActions = actionItems
            .slice(numActionsVisible)
            .map(({ key, Action }) => <Action key={key} {...actionProps} menuItemVariant/>);
        const cursor = this.cursorPosition;
        return (<Container ref={this.containerRef} className={className} isOpen={inputHasFocus}>
        <SearchLabel htmlFor="smart-search-input" aria-label={(0, locale_1.t)('Search events')}>
          <icons_1.IconSearch />
          {inlineLabel}
        </SearchLabel>

        <InputWrapper>
          <Highlight>
            {parsedQuery !== null ? (<renderer_1.default parsedQuery={parsedQuery} cursorPosition={cursor === -1 ? undefined : cursor}/>) : (query)}
          </Highlight>
          {useFormWrapper ? <form onSubmit={this.onSubmit}>{input}</form> : input}
        </InputWrapper>

        <ActionsBar gap={0.5}>
          {query !== '' && (<actions_1.ActionButton onClick={this.clearSearch} icon={<icons_1.IconClose size="xs"/>} title={(0, locale_1.t)('Clear search')} aria-label={(0, locale_1.t)('Clear search')}/>)}
          {visibleActions}
          {overflowedActions.length > 0 && (<dropdownLink_1.default anchorRight caret={false} title={<actions_1.ActionButton aria-label={(0, locale_1.t)('Show more')} icon={<VerticalEllipsisIcon size="xs"/>}/>}>
              {overflowedActions}
            </dropdownLink_1.default>)}
        </ActionsBar>

        {(loading || searchGroups.length > 0) && (<searchDropdown_1.default css={{ display: inputHasFocus ? 'block' : 'none' }} className={dropdownClassName} items={searchGroups} onClick={this.onAutoComplete} loading={loading} searchSubstring={searchTerm}/>)}
      </Container>);
    }
}
exports.SmartSearchBar = SmartSearchBar;
SmartSearchBar.defaultProps = {
    defaultQuery: '',
    query: null,
    onSearch: function () { },
    excludeEnvironment: false,
    placeholder: (0, locale_1.t)('Search for events, users, tags, and more'),
    supportedTags: {},
    defaultSearchItems: [[], []],
    useFormWrapper: true,
    savedSearchType: types_1.SavedSearchType.ISSUE,
};
class SmartSearchBarContainer extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            members: memberListStore_1.default.getAll(),
        };
        this.unsubscribe = memberListStore_1.default.listen((members) => this.setState({ members }), undefined);
    }
    componentWillUnmount() {
        this.unsubscribe();
    }
    render() {
        // SmartSearchBar doesn't use members, but we forward it to cause a re-render.
        return <SmartSearchBar {...this.props} members={this.state.members}/>;
    }
}
exports.default = (0, withApi_1.default)((0, react_router_1.withRouter)((0, withOrganization_1.default)(SmartSearchBarContainer)));
const Container = (0, styled_1.default)('div') `
  border: 1px solid ${p => p.theme.border};
  box-shadow: inset ${p => p.theme.dropShadowLight};
  background: ${p => p.theme.background};
  padding: 7px ${(0, space_1.default)(1)};
  position: relative;
  display: grid;
  grid-template-columns: max-content 1fr max-content;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: start;

  border-radius: ${p => p.isOpen
    ? `${p.theme.borderRadius} ${p.theme.borderRadius} 0 0`
    : p.theme.borderRadius};

  .show-sidebar & {
    background: ${p => p.theme.backgroundSecondary};
  }
`;
const SearchLabel = (0, styled_1.default)('label') `
  display: flex;
  padding: ${(0, space_1.default)(0.5)} 0;
  margin: 0;
  color: ${p => p.theme.gray300};
`;
const InputWrapper = (0, styled_1.default)('div') `
  position: relative;
`;
const Highlight = (0, styled_1.default)('div') `
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  user-select: none;
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 25px;
  font-size: ${p => p.theme.fontSizeSmall};
  font-family: ${p => p.theme.text.familyMono};
`;
const SearchInput = (0, styled_1.default)(react_autosize_textarea_1.default, {
    shouldForwardProp: prop => typeof prop === 'string' && (0, is_prop_valid_1.default)(prop),
}) `
  position: relative;
  display: flex;
  resize: none;
  outline: none;
  border: 0;
  width: 100%;
  padding: 0;
  line-height: 25px;
  margin-bottom: -1px;
  background: transparent;
  font-size: ${p => p.theme.fontSizeSmall};
  font-family: ${p => p.theme.text.familyMono};
  caret-color: ${p => p.theme.subText};
  color: transparent;

  &::selection {
    background: rgba(0, 0, 0, 0.2);
  }
  &::placeholder {
    color: ${p => p.theme.formPlaceholder};
  }

  [disabled] {
    color: ${p => p.theme.disabled};
  }
`;
const ActionsBar = (0, styled_1.default)(buttonBar_1.default) `
  height: ${(0, space_1.default)(2)};
  margin: ${(0, space_1.default)(0.5)} 0;
`;
const VerticalEllipsisIcon = (0, styled_1.default)(icons_1.IconEllipsis) `
  transform: rotate(90deg);
`;
//# sourceMappingURL=index.jsx.map