Object.defineProperty(exports, "__esModule", { value: true });
exports.ActionButton = exports.makeSearchBuilderAction = exports.makeSaveSearchAction = exports.makePinSearchAction = void 0;
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const modal_1 = require("app/actionCreators/modal");
const savedSearches_1 = require("app/actionCreators/savedSearches");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const types_1 = require("app/types");
const analytics_1 = require("app/utils/analytics");
const createSavedSearchModal_1 = (0, tslib_1.__importDefault)(require("app/views/issueList/createSavedSearchModal"));
const utils_1 = require("./utils");
/**
 * The Pin Search action toggles the current as a pinned search
 */
function makePinSearchAction({ pinnedSearch, sort }) {
    const PinSearchAction = ({ menuItemVariant, savedSearchType, organization, api, query, location, }) => {
        const onTogglePinnedSearch = (evt) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a;
            evt.preventDefault();
            evt.stopPropagation();
            if (savedSearchType === undefined) {
                return;
            }
            const _b = location.query, { cursor: _cursor, page: _page } = _b, currentQuery = (0, tslib_1.__rest)(_b, ["cursor", "page"]);
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'search.pin',
                eventName: 'Search: Pin',
                organization_id: organization.id,
                action: !!pinnedSearch ? 'unpin' : 'pin',
                search_type: savedSearchType === types_1.SavedSearchType.ISSUE ? 'issues' : 'events',
                query: (_a = pinnedSearch === null || pinnedSearch === void 0 ? void 0 : pinnedSearch.query) !== null && _a !== void 0 ? _a : query,
            });
            if (!!pinnedSearch) {
                (0, savedSearches_1.unpinSearch)(api, organization.slug, savedSearchType, pinnedSearch).then(() => {
                    react_router_1.browserHistory.push(Object.assign(Object.assign({}, location), { pathname: `/organizations/${organization.slug}/issues/`, query: Object.assign(Object.assign({}, currentQuery), { query: pinnedSearch.query, sort: pinnedSearch.sort }) }));
                });
                return;
            }
            const resp = yield (0, savedSearches_1.pinSearch)(api, organization.slug, savedSearchType, (0, utils_1.removeSpace)(query), sort);
            if (!resp || !resp.id) {
                return;
            }
            react_router_1.browserHistory.push(Object.assign(Object.assign({}, location), { pathname: `/organizations/${organization.slug}/issues/searches/${resp.id}/`, query: currentQuery }));
        });
        const pinTooltip = !!pinnedSearch ? (0, locale_1.t)('Unpin this search') : (0, locale_1.t)('Pin this search');
        return menuItemVariant ? (<menuItem_1.default withBorder data-test-id="pin-icon" icon={<icons_1.IconPin isSolid={!!pinnedSearch} size="xs"/>} onClick={onTogglePinnedSearch}>
        {!!pinnedSearch ? (0, locale_1.t)('Unpin Search') : (0, locale_1.t)('Pin Search')}
      </menuItem_1.default>) : (<exports.ActionButton title={pinTooltip} disabled={!query} aria-label={pinTooltip} onClick={onTogglePinnedSearch} isActive={!!pinnedSearch} data-test-id="pin-icon" icon={<icons_1.IconPin isSolid={!!pinnedSearch} size="xs"/>}/>);
    };
    return { key: 'pinSearch', Action: (0, react_router_1.withRouter)(PinSearchAction) };
}
exports.makePinSearchAction = makePinSearchAction;
/**
 * The Save Search action triggers the create saved search modal from the
 * current query.
 */
function makeSaveSearchAction({ sort }) {
    const SavedSearchAction = ({ menuItemVariant, query, organization }) => {
        const onClick = () => (0, modal_1.openModal)(deps => (<createSavedSearchModal_1.default {...deps} {...{ organization, query, sort }}/>));
        return (<access_1.default organization={organization} access={['org:write']}>
        {menuItemVariant ? (<menuItem_1.default withBorder icon={<icons_1.IconAdd size="xs"/>} onClick={onClick}>
            {(0, locale_1.t)('Create Saved Search')}
          </menuItem_1.default>) : (<exports.ActionButton onClick={onClick} data-test-id="save-current-search" icon={<icons_1.IconAdd size="xs"/>} title={(0, locale_1.t)('Add to organization saved searches')} aria-label={(0, locale_1.t)('Add to organization saved searches')}/>)}
      </access_1.default>);
    };
    return { key: 'saveSearch', Action: SavedSearchAction };
}
exports.makeSaveSearchAction = makeSaveSearchAction;
/**
 * The Search Builder action toggles the Issue Stream search builder
 */
function makeSearchBuilderAction({ onSidebarToggle }) {
    const SearchBuilderAction = ({ menuItemVariant }) => menuItemVariant ? (<menuItem_1.default withBorder icon={<icons_1.IconSliders size="xs"/>} onClick={onSidebarToggle}>
        {(0, locale_1.t)('Toggle sidebar')}
      </menuItem_1.default>) : (<exports.ActionButton title={(0, locale_1.t)('Toggle search builder')} tooltipProps={{ containerDisplayMode: 'inline-flex' }} aria-label={(0, locale_1.t)('Toggle search builder')} onClick={onSidebarToggle} icon={<icons_1.IconSliders size="xs"/>}/>);
    return { key: 'searchBuilder', Action: SearchBuilderAction };
}
exports.makeSearchBuilderAction = makeSearchBuilderAction;
exports.ActionButton = (0, styled_1.default)(button_1.default) `
  color: ${p => (p.isActive ? p.theme.blue300 : p.theme.gray300)};
  width: 18px;

  &,
  &:hover,
  &:focus {
    background: transparent;
  }

  &:hover {
    color: ${p => p.theme.gray400};
  }
`;
exports.ActionButton.defaultProps = {
    type: 'button',
    borderless: true,
    size: 'zero',
};
//# sourceMappingURL=actions.jsx.map