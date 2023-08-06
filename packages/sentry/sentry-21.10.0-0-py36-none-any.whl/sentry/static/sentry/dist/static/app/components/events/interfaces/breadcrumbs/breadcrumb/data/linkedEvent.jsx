Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const indicator_1 = require("app/actionCreators/indicator");
const projectBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/projectBadge"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const shortId_1 = (0, tslib_1.__importDefault)(require("app/components/shortId"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const useSessionStorage_1 = (0, tslib_1.__importDefault)(require("app/utils/useSessionStorage"));
function LinkedEvent({ orgSlug, eventId, route, router }) {
    const [storedLinkedEvent, setStoredLinkedEvent, removeStoredLinkedEvent] = (0, useSessionStorage_1.default)(eventId);
    const [eventIdLookup, setEventIdLookup] = (0, react_1.useState)();
    const [hasError, setHasError] = (0, react_1.useState)(false);
    const api = (0, useApi_1.default)();
    (0, react_1.useEffect)(() => {
        fetchEventById();
        router.setRouteLeaveHook(route, onRouteLeave);
    }, []);
    (0, react_1.useEffect)(() => {
        fetchIssueByGroupId();
    }, [eventIdLookup]);
    function onRouteLeave() {
        removeStoredLinkedEvent();
    }
    function fetchEventById() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (!!storedLinkedEvent) {
                return;
            }
            try {
                const response = yield api.requestPromise(`/organizations/${orgSlug}/eventids/${eventId}/`);
                setEventIdLookup(response);
            }
            catch (error) {
                setHasError(true);
                if (error.status === 404) {
                    return;
                }
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('An error occured while fetching the data of the breadcrumb event link'));
                Sentry.captureException(error);
                // do nothing. The link won't be displayed
            }
        });
    }
    function fetchIssueByGroupId() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (!!storedLinkedEvent || !eventIdLookup) {
                return;
            }
            try {
                const response = yield api.requestPromise(`/organizations/${orgSlug}/issues/${eventIdLookup.groupId}/`);
                const { project, shortId } = response;
                const { groupId } = eventIdLookup;
                setStoredLinkedEvent({ shortId, project, groupId, orgSlug });
            }
            catch (error) {
                setHasError(true);
                if (error.status === 404) {
                    return;
                }
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('An error occured while fetching the data of the breadcrumb event link'));
                Sentry.captureException(error);
                // do nothing. The link won't be displayed
            }
        });
    }
    if (hasError) {
        return null;
    }
    if (!storedLinkedEvent) {
        return <StyledPlaceholder height="16px" width="109px"/>;
    }
    const { shortId, project, groupId } = storedLinkedEvent;
    return (<StyledShortId shortId={shortId} avatar={<projectBadge_1.default project={project} avatarSize={16} hideName/>} to={`/${orgSlug}/${project.slug}/issues/${groupId}/events/${eventId}/`}/>);
}
exports.default = LinkedEvent;
const StyledShortId = (0, styled_1.default)(shortId_1.default) `
  font-weight: 700;
  display: inline-grid;
  margin-right: ${(0, space_1.default)(1)};
`;
const StyledPlaceholder = (0, styled_1.default)(placeholder_1.default) `
  display: inline-flex;
  margin-right: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=linkedEvent.jsx.map