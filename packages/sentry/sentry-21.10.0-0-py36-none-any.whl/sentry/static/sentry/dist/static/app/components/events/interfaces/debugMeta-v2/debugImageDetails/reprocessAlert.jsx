Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const alertLink_1 = (0, tslib_1.__importDefault)(require("app/components/alertLink"));
const locale_1 = require("app/locale");
var ReprocessableEventReason;
(function (ReprocessableEventReason) {
    // It can have many reasons. The event is too old to be reprocessed (very unlikely!)
    // or was not a native event.
    ReprocessableEventReason["UNPROCESSED_EVENT_NOT_FOUND"] = "unprocessed_event.not_found";
    // The event does not exist.
    ReprocessableEventReason["EVENT_NOT_FOUND"] = "event.not_found";
    // A required attachment, such as the original minidump, is missing.
    ReprocessableEventReason["ATTACHMENT_NOT_FOUND"] = "attachment.not_found";
})(ReprocessableEventReason || (ReprocessableEventReason = {}));
function ReprocessAlert({ onReprocessEvent, api, orgSlug, projSlug, eventId }) {
    const [reprocessableEvent, setReprocessableEvent] = (0, react_1.useState)();
    (0, react_1.useEffect)(() => {
        checkEventReprocessable();
    }, []);
    function checkEventReprocessable() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            try {
                const response = yield api.requestPromise(`/projects/${orgSlug}/${projSlug}/events/${eventId}/reprocessable/`);
                setReprocessableEvent(response);
            }
            catch (_a) {
                // do nothing
            }
        });
    }
    if (!reprocessableEvent) {
        return null;
    }
    const { reprocessable, reason } = reprocessableEvent;
    if (reprocessable) {
        return (<alertLink_1.default priority="warning" size="small" onClick={onReprocessEvent} withoutMarginBottom>
        {(0, locale_1.t)('You’ve uploaded new debug files. Reprocess events in this issue to view a better stack trace')}
      </alertLink_1.default>);
    }
    function getAlertInfoMessage() {
        switch (reason) {
            case ReprocessableEventReason.EVENT_NOT_FOUND:
                return (0, locale_1.t)('This event cannot be reprocessed because the event has not been found');
            case ReprocessableEventReason.ATTACHMENT_NOT_FOUND:
                return (0, locale_1.t)('This event cannot be reprocessed because a required attachment is missing');
            case ReprocessableEventReason.UNPROCESSED_EVENT_NOT_FOUND:
            default:
                return (0, locale_1.t)('This event cannot be reprocessed');
        }
    }
    return <StyledAlert type="info">{getAlertInfoMessage()}</StyledAlert>;
}
exports.default = ReprocessAlert;
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  margin-bottom: 0;
`;
//# sourceMappingURL=reprocessAlert.jsx.map