Object.defineProperty(exports, "__esModule", { value: true });
exports.getValidOps = exports.generateOperatorEntryMap = exports.filterSearchGroupsByIndex = exports.createSearchGroups = exports.getQueryTerms = exports.getLastTermIndex = exports.removeSpace = exports.addSpace = void 0;
const parser_1 = require("app/components/searchSyntax/parser");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const types_1 = require("./types");
function addSpace(query = '') {
    if (query.length !== 0 && query[query.length - 1] !== ' ') {
        return query + ' ';
    }
    return query;
}
exports.addSpace = addSpace;
function removeSpace(query = '') {
    if (query[query.length - 1] === ' ') {
        return query.slice(0, query.length - 1);
    }
    return query;
}
exports.removeSpace = removeSpace;
/**
 * Given a query, and the current cursor position, return the string-delimiting
 * index of the search term designated by the cursor.
 */
function getLastTermIndex(query, cursor) {
    // TODO: work with quoted-terms
    const cursorOffset = query.slice(cursor).search(/\s|$/);
    return cursor + (cursorOffset === -1 ? 0 : cursorOffset);
}
exports.getLastTermIndex = getLastTermIndex;
/**
 * Returns an array of query terms, including incomplete terms
 *
 * e.g. ["is:unassigned", "browser:\"Chrome 33.0\"", "assigned"]
 */
function getQueryTerms(query, cursor) {
    return query.slice(0, cursor).match(/\S+:"[^"]*"?|\S+/g);
}
exports.getQueryTerms = getQueryTerms;
function getTitleForType(type) {
    if (type === types_1.ItemType.TAG_VALUE) {
        return (0, locale_1.t)('Tag Values');
    }
    if (type === types_1.ItemType.RECENT_SEARCH) {
        return (0, locale_1.t)('Recent Searches');
    }
    if (type === types_1.ItemType.DEFAULT) {
        return (0, locale_1.t)('Common Search Terms');
    }
    if (type === types_1.ItemType.TAG_OPERATOR) {
        return (0, locale_1.t)('Operator Helpers');
    }
    return (0, locale_1.t)('Tags');
}
function getIconForTypeAndTag(type, tagName) {
    if (type === types_1.ItemType.RECENT_SEARCH) {
        return <icons_1.IconClock size="xs"/>;
    }
    if (type === types_1.ItemType.DEFAULT) {
        return <icons_1.IconStar size="xs"/>;
    }
    // Change based on tagName and default to "icon-tag"
    switch (tagName) {
        case 'is':
            return <icons_1.IconToggle size="xs"/>;
        case 'assigned':
        case 'bookmarks':
            return <icons_1.IconUser size="xs"/>;
        case 'firstSeen':
        case 'lastSeen':
        case 'event.timestamp':
            return <icons_1.IconClock size="xs"/>;
        default:
            return <icons_1.IconTag size="xs"/>;
    }
}
function createSearchGroups(searchItems, recentSearchItems, tagName, type, maxSearchItems, queryCharsLeft) {
    const activeSearchItem = 0;
    if (maxSearchItems && maxSearchItems > 0) {
        searchItems = searchItems.filter((value, index) => index < maxSearchItems || value.ignoreMaxSearchItems);
    }
    if (queryCharsLeft || queryCharsLeft === 0) {
        searchItems = searchItems.filter((value) => value.value.length <= queryCharsLeft);
        if (recentSearchItems) {
            recentSearchItems = recentSearchItems.filter((value) => value.value.length <= queryCharsLeft);
        }
    }
    const searchGroup = {
        title: getTitleForType(type),
        type: type === types_1.ItemType.INVALID_TAG ? type : 'header',
        icon: getIconForTypeAndTag(type, tagName),
        children: [...searchItems],
    };
    const recentSearchGroup = recentSearchItems && {
        title: (0, locale_1.t)('Recent Searches'),
        type: 'header',
        icon: <icons_1.IconClock size="xs"/>,
        children: [...recentSearchItems],
    };
    if (searchGroup.children && !!searchGroup.children.length) {
        searchGroup.children[activeSearchItem] = Object.assign({}, searchGroup.children[activeSearchItem]);
    }
    return {
        searchGroups: [searchGroup, ...(recentSearchGroup ? [recentSearchGroup] : [])],
        flatSearchItems: [...searchItems, ...(recentSearchItems ? recentSearchItems : [])],
        activeSearchItem: -1,
    };
}
exports.createSearchGroups = createSearchGroups;
/**
 * Items is a list of dropdown groups that have a `children` field. Only the
 * `children` are selectable, so we need to find which child is selected given
 * an index that is in range of the sum of all `children` lengths
 *
 * @return Returns a tuple of [groupIndex, childrenIndex]
 */
function filterSearchGroupsByIndex(items, index) {
    let _index = index;
    let foundSearchItem = [undefined, undefined];
    items.find(({ children }, i) => {
        if (!children || !children.length) {
            return false;
        }
        if (_index < children.length) {
            foundSearchItem = [i, _index];
            return true;
        }
        _index -= children.length;
        return false;
    });
    return foundSearchItem;
}
exports.filterSearchGroupsByIndex = filterSearchGroupsByIndex;
function generateOperatorEntryMap(tag) {
    return {
        [parser_1.TermOperator.Default]: {
            type: types_1.ItemType.TAG_OPERATOR,
            value: ':',
            desc: `${tag}:${(0, locale_1.t)('[value] is equal to')}`,
        },
        [parser_1.TermOperator.GreaterThanEqual]: {
            type: types_1.ItemType.TAG_OPERATOR,
            value: ':>=',
            desc: `${tag}:${(0, locale_1.t)('>=[value] is greater than or equal to')}`,
        },
        [parser_1.TermOperator.LessThanEqual]: {
            type: types_1.ItemType.TAG_OPERATOR,
            value: ':<=',
            desc: `${tag}:${(0, locale_1.t)('<=[value] is less than or equal to')}`,
        },
        [parser_1.TermOperator.GreaterThan]: {
            type: types_1.ItemType.TAG_OPERATOR,
            value: ':>',
            desc: `${tag}:${(0, locale_1.t)('>[value] is greater than')}`,
        },
        [parser_1.TermOperator.LessThan]: {
            type: types_1.ItemType.TAG_OPERATOR,
            value: ':<',
            desc: `${tag}:${(0, locale_1.t)('<[value] is less than')}`,
        },
        [parser_1.TermOperator.Equal]: {
            type: types_1.ItemType.TAG_OPERATOR,
            value: ':=',
            desc: `${tag}:${(0, locale_1.t)('=[value] is equal to')}`,
        },
        [parser_1.TermOperator.NotEqual]: {
            type: types_1.ItemType.TAG_OPERATOR,
            value: '!:',
            desc: `!${tag}:${(0, locale_1.t)('[value] is not equal to')}`,
        },
    };
}
exports.generateOperatorEntryMap = generateOperatorEntryMap;
function getValidOps(filterToken) {
    var _a, _b;
    // If the token is invalid we want to use the possible expected types as our filter type
    const validTypes = (_b = (_a = filterToken.invalid) === null || _a === void 0 ? void 0 : _a.expectedType) !== null && _b !== void 0 ? _b : [filterToken.filter];
    // Determine any interchangable filter types for our valid types
    const interchangeableTypes = validTypes.map(type => { var _a; return (_a = parser_1.interchangeableFilterOperators[type]) !== null && _a !== void 0 ? _a : []; });
    // Combine all types
    const allValidTypes = [...new Set([...validTypes, ...interchangeableTypes.flat()])];
    // Find all valid operations
    const validOps = new Set(allValidTypes.map(type => parser_1.filterTypeConfig[type].validOps).flat());
    return [...validOps];
}
exports.getValidOps = getValidOps;
//# sourceMappingURL=utils.jsx.map