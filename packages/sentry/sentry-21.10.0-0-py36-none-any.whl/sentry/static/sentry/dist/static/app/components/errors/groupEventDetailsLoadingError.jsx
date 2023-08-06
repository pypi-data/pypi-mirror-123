Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const detailedError_1 = (0, tslib_1.__importDefault)(require("app/components/errors/detailedError"));
const locale_1 = require("app/locale");
const GroupEventDetailsLoadingError = ({ onRetry, environments }) => {
    const reasons = [
        (0, locale_1.t)('The events are still processing and are on their way'),
        (0, locale_1.t)('The events have been deleted'),
        (0, locale_1.t)('There is an internal systems error or active issue'),
    ];
    let message;
    if (environments.length === 0) {
        // All Environments case
        message = (<div>
        <p>{(0, locale_1.t)('This could be due to a handful of reasons:')}</p>
        <ol className="detailed-error-list">
          {reasons.map((reason, i) => (<li key={i}>{reason}</li>))}
        </ol>
      </div>);
    }
    else {
        message = (<div>{(0, locale_1.t)('No events were found for the currently selected environments')}</div>);
    }
    return (<detailedError_1.default className="group-event-details-error" onRetry={environments.length === 0 ? onRetry : undefined} heading={(0, locale_1.t)('Sorry, the events for this issue could not be found.')} message={message}/>);
};
exports.default = GroupEventDetailsLoadingError;
//# sourceMappingURL=groupEventDetailsLoadingError.jsx.map