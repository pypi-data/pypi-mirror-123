Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const editableText_1 = (0, tslib_1.__importDefault)(require("app/components/editableText"));
const thirds_1 = require("app/components/layouts/thirds");
const locale_1 = require("app/locale");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const utils_1 = require("./savedQuery/utils");
const NAME_DEFAULT = (0, locale_1.t)('Untitled query');
/**
 * Allows user to edit the name of the query.
 * By pressing Enter or clicking outside the component, the changes will be saved, if valid.
 */
function EventInputName({ organization, eventView, savedQuery }) {
    const api = (0, useApi_1.default)();
    function handleChange(nextQueryName) {
        // Do not update automatically if
        // 1) It is a new query
        // 2) The new name is same as the old name
        if (!savedQuery || savedQuery.name === nextQueryName) {
            return;
        }
        // This ensures that we are updating SavedQuery.name only.
        // Changes on QueryBuilder table will not be saved.
        const nextEventView = eventView_1.default.fromSavedQuery(Object.assign(Object.assign({}, savedQuery), { name: nextQueryName }));
        (0, utils_1.handleUpdateQueryName)(api, organization, nextEventView).then((_updatedQuery) => {
            // The current eventview may have changes that are not explicitly saved.
            // So, we just preserve them and change its name
            const renamedEventView = eventView.clone();
            renamedEventView.name = nextQueryName;
            react_router_1.browserHistory.push(renamedEventView.getResultsViewUrlTarget(organization.slug));
        });
    }
    const value = eventView.name || NAME_DEFAULT;
    return (<StyledTitle data-test-id={`discover2-query-name-${value}`}>
      <editableText_1.default value={value} onChange={handleChange} isDisabled={!eventView.id} errorMessage={(0, locale_1.t)('Please set a name for this query')}/>
    </StyledTitle>);
}
const StyledTitle = (0, styled_1.default)(thirds_1.Title) `
  overflow: unset;
`;
exports.default = EventInputName;
//# sourceMappingURL=eventInputName.jsx.map